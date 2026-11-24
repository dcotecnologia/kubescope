import pytest
from PySide6.QtWidgets import (
    QDialog,
    QPushButton,
    QSpinBox,
)

from kubescope import forwards
from kubescope import window as window_module
from kubescope.forwards import FAILED, RUNNING, STOPPED, Forward
from tests.test_window_flows import _ready_window
from tests.test_window_write import SERVICE, SERVICE_DOCUMENT


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    monkeypatch.setattr(shown.forward_runner, "start", _Starts())
    monkeypatch.setattr(window_module.forwards, "port_in_use", lambda port: False)
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


class _Starts:
    """Stands in for the runner: notes what the window asks it to start."""

    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def __call__(self, *arguments):
        self.calls.append(arguments)
        title, kind, command, env, local, target = arguments
        return Forward(1, title, kind, command, env, local, target)


def _buttons(dialog) -> dict[str, QPushButton]:
    return {button.text(): button for button in dialog.findChildren(QPushButton)}


def _run(monkeypatch, action) -> None:
    def fake_exec(dialog) -> int:
        action(dialog)
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)


def test_a_kubectl_forward_is_run_from_its_dialog_and_listed(
    window, monkeypatch
) -> None:
    monkeypatch.setattr(window, "_context", lambda: "prod")
    seen = {}

    def click_run(dialog) -> None:
        buttons = _buttons(dialog)
        seen["buttons"] = {
            name: (button.property("variant"), button.minimumWidth())
            for name, button in buttons.items()
            if name in ("Copy", "Run in KubeScope", "Close")
        }
        dialog.findChild(QSpinBox).setValue(9090)
        buttons["Run in KubeScope"].click()
        seen["result"] = dialog.result()

    _run(monkeypatch, click_run)

    window._show_forward_command(SERVICE, SERVICE_DOCUMENT)

    assert {variant for variant, _width in seen["buttons"].values()} == {"secondary"}
    assert len({width for _variant, width in seen["buttons"].values()}) == 1
    title, kind, command, env, local, target = window.forward_runner.start.calls[0]
    assert (title, kind, local, target) == ("Service api", "kubectl", 9090, "api:80")
    assert command[:3] == ["kubectl", "--context", "prod"]
    assert command[-2:] == ["service/api", "9090:80"] and env == {}
    assert seen["result"] == QDialog.DialogCode.Accepted
    assert window.pages.currentIndex() == 5


def test_a_forward_to_a_port_in_use_is_not_started(window, monkeypatch) -> None:
    monkeypatch.setattr(window_module.forwards, "port_in_use", lambda port: True)
    messages = []
    monkeypatch.setattr(
        window, "_show_message", lambda icon, title, text: messages.append(text)
    )
    _run(monkeypatch, lambda dialog: _buttons(dialog)["Run in KubeScope"].click())

    window._show_forward_command(SERVICE, SERVICE_DOCUMENT)

    assert "already in use" in messages[0]
    assert window.forward_runner.start.calls == []
    assert window.pages.currentIndex() != 5


def _list(window, *items: Forward) -> None:
    window.forward_runner.items.extend(items)
    window.forward_runner.changed.emit()


def test_the_forwards_page_lists_their_status_and_stops_them(
    window, monkeypatch
) -> None:
    runner = window.forward_runner
    running = Forward(1, "Service api", "kubectl", ["k"], {}, 8080, "api:80", RUNNING)
    failed = Forward(2, "RDS db", "ssm", ["a"], {}, 15432, "h:5432", FAILED, "busy")
    stopped = Forward(3, "Pod x", "kubectl", ["k"], {}, 1, "x:1", STOPPED)
    stops = []
    monkeypatch.setattr(runner, "stop", lambda forward: stops.append(forward.number))
    ui = window.forwards_ui
    assert not ui.stopAllButton.isEnabled() and window.nav_forwards.text() == "Forwards"

    _list(window, running, failed, stopped)

    table = ui.forwardsTable
    assert [table.item(row, 4).text() for row in range(3)] == [
        "Running", "Failed", "Stopped",
    ]  # fmt: skip
    assert table.item(0, 2).text() == "127.0.0.1:8080"
    assert table.item(1, 1).text() == "SSM" and table.item(1, 5).text() == "busy"
    assert window.nav_forwards.text() == "Forwards (1)"
    assert ui.stopAllButton.isEnabled() and ui.clearButton.isEnabled()

    table.selectRow(1)  # a forward that is over has nothing to stop
    assert not ui.stopButton.isEnabled()
    table.selectRow(0)
    assert ui.stopButton.isEnabled()
    ui.stopButton.click()
    assert stops == [1]

    table.setCurrentCell(-1, -1)
    window._stop_selected_forward()  # nothing selected
    assert stops == [1]

    ui.clearButton.click()  # only the finished ones go
    assert [item.number for item in runner.items] == [1]
    window.nav_forwards.click()
    assert window.pages.currentIndex() == 5 and window.nav_forwards.isChecked()
    assert window.ui.pageTitle.text() == "Port forwards"
    window._retranslate()


def test_the_forwards_end_with_the_app(window, monkeypatch) -> None:
    ended = []
    monkeypatch.setattr(window.forward_runner, "stop_all", lambda: ended.append("stop"))
    monkeypatch.setattr(window.forward_runner, "wait", lambda: ended.append("wait"))
    window._tray = None

    window.close()

    assert ended == ["stop", "wait"]


def test_the_unknown_status_of_a_forward_is_shown_as_it_is(window) -> None:
    assert window._forward_status_text(forwards.STARTING) == "Starting"
    assert window._forward_status_text("odd") == "odd"


def test_the_selected_forward_stays_selected_when_the_list_is_drawn_again(
    window,
) -> None:
    _list(
        window,
        Forward(1, "A", "kubectl", ["k"], {}, 1, "a:1", RUNNING),
        Forward(2, "B", "kubectl", ["k"], {}, 2, "b:2", RUNNING),
    )
    table = window.forwards_ui.forwardsTable
    table.selectRow(1)

    window.forward_runner.changed.emit()  # a status changed: drawn again

    assert table.currentRow() == 1


def test_a_forward_that_fails_is_told_in_the_banner(window) -> None:
    failed = Forward(
        1, "RDS orders", "ssm", ["aws"], {}, 15432, "h:5432", FAILED, "error: busy"
    )

    window.forward_runner.failed.emit(failed)

    assert not window.permission_banner.isHidden()
    assert "RDS orders: error: busy" in window.ui.permissionDetailsText.text()


def test_a_click_on_a_header_sorts_the_forwards_and_the_buttons_follow_the_row(
    window, monkeypatch
) -> None:
    runner = window.forward_runner
    first = Forward(1, "Service b", "kubectl", ["k"], {}, 9000, "b:80", RUNNING)
    second = Forward(2, "Service a", "kubectl", ["k"], {}, 8000, "a:80", RUNNING)
    stops = []
    monkeypatch.setattr(runner, "stop", lambda forward: stops.append(forward.number))
    _list(window, first, second)
    table = window.forwards_ui.forwardsTable
    assert [table.item(row, 0).text() for row in range(2)] == [
        "Service b",
        "Service a",
    ]

    window.forwards_sorter.clicked(0)

    assert [table.item(row, 0).text() for row in range(2)] == [
        "Service a",
        "Service b",
    ]
    table.selectRow(0)  # the row on screen, not the one the runner keeps first
    window.forwards_ui.stopButton.click()
    assert stops == [2]

    window.forwards_sorter.clicked(2)  # the port, a number
    window.forwards_sorter.clicked(2)
    assert table.item(0, 2).text() == "127.0.0.1:9000"
