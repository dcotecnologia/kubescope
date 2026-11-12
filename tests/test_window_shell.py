import pytest
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QComboBox, QDialog, QMenu, QPushButton

from kubescope import window as window_module
from kubescope.cluster import ClusterError
from kubescope.models import PodInfo
from tests.test_window_flows import POD, _ready_window, _wait_until


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    monkeypatch.setattr(shown, "_context", lambda: "prod")
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def _fake_menu(monkeypatch, shown) -> None:
    """A menu that does not open: it keeps the actions it was asked to show."""

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            shown.append(self.actions())
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)


def _run(monkeypatch, action) -> None:
    def fake_exec(dialog) -> int:
        action(dialog)
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)


def _buttons(dialog) -> dict[str, QPushButton]:
    return {button.text(): button for button in dialog.findChildren(QPushButton)}


def test_a_pod_shell_opens_in_the_terminal_of_the_system(window, monkeypatch) -> None:
    opened = []
    monkeypatch.setattr(
        window_module,
        "open_in_terminal",
        lambda command, env: opened.append((command, env)),
    )
    seen = {}

    def click(dialog) -> None:
        dialog.findChild(QComboBox).setCurrentIndex(1)  # the sidecar
        buttons = _buttons(dialog)
        seen["labels"] = sorted(buttons)
        buttons["Open in terminal"].click()
        seen["result"] = dialog.result()

    _run(monkeypatch, click)

    window._show_shell_command(POD)

    command, env = opened[0]
    assert command[:3] == ["kubectl", "--context", "prod"]
    assert "sidecar" in command and env == {}
    assert seen["result"] == QDialog.DialogCode.Accepted
    assert "Open in terminal" in seen["labels"] and "Copy" in seen["labels"]


def test_a_terminal_that_cannot_be_opened_says_so_in_the_banner_and_keeps_the_dialog(
    window, monkeypatch
) -> None:
    def no_terminal(command, env):
        raise ClusterError("No terminal found. Run this in a terminal: kubectl")

    monkeypatch.setattr(window_module, "open_in_terminal", no_terminal)
    seen = {}

    def click(dialog) -> None:
        _buttons(dialog)["Open in terminal"].click()
        seen["result"] = dialog.result()

    _run(monkeypatch, click)

    window._show_shell_command(PodInfo("ns", "api-1", "Running", 1, 1, "1h", ("app",)))

    assert not window.permission_banner.isHidden()
    assert "No terminal found" in window.ui.permissionDetailsText.text()
    assert seen["result"] != QDialog.DialogCode.Accepted


def _nodes(window, monkeypatch):
    window.nodes_table.setRowCount(1)
    window.nodes_table.setItem(0, 0, window_module.QTableWidgetItem("ip-10-0-0-1"))
    shown = []
    _fake_menu(monkeypatch, shown)
    return window.nodes_table.visualItemRect(
        window.nodes_table.item(0, 0)
    ).center(), shown


def test_a_node_offers_a_shell_through_ssm_only_in_the_write_mode(
    window, monkeypatch
) -> None:
    position, shown = _nodes(window, monkeypatch)

    window.settings.write_mode = False
    window._show_node_menu(position)
    assert shown == []

    window.settings.write_mode = True
    window._show_node_menu(position)
    assert [action.text() for action in shown[0]] == ["Shell (SSM)"]
    window._show_node_menu(window_module.QPoint(5, 5000))  # below the rows
    assert len(shown) == 1


def test_the_shell_of_a_node_finds_its_instance_and_opens_in_a_terminal(
    window, monkeypatch
) -> None:
    asked = []
    monkeypatch.setattr(
        window_module,
        "get_node_instance",
        lambda context, node: (
            asked.append((context, node)) or ("i-0abc", "us-east-1", "work")
        ),
    )
    monkeypatch.setattr(
        window_module, "context_environment", lambda context: {"AWS_PROFILE": "work"}
    )
    opened = []
    monkeypatch.setattr(
        window_module,
        "open_in_terminal",
        lambda command, env: opened.append((command, env)),
    )
    seen = {}

    def click(dialog) -> None:
        from PySide6.QtWidgets import QLabel, QPlainTextEdit

        seen["texts"] = [label.text() for label in dialog.findChildren(QLabel)]
        seen["command"] = dialog.findChild(QPlainTextEdit).toPlainText()
        _buttons(dialog)["Open in terminal"].click()

    _run(monkeypatch, click)

    window._node_shell("ip-10-0-0-1")
    _wait_until(lambda: opened)

    assert asked == [("prod", "ip-10-0-0-1")]
    assert "Node ip-10-0-0-1 is the EC2 instance i-0abc." in seen["texts"]
    assert "i-0abc" in seen["command"] and "--profile work" in seen["command"]
    assert opened[0][0][:4] == ["aws", "ssm", "start-session", "--target"]
    assert opened[0][1] == {"AWS_PROFILE": "work"}
