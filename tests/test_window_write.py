from kubescope.sdk import NOTIFICATION
from kubescope.sdk.models import ClusterResource, PodInfo, Workload
from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QLabel,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
)

from kubescope import window as window_module
from kubescope import writes
from kubescope.cluster import ClusterError
from kubescope.writes import MAX_REPLICAS
from tests.test_window_flows import POD, _ready_window

API = Workload("ns", "Deployment", "api", 2, 3, "1d")
SINGLE = PodInfo("ns", "solo", "Running", 1, 1, "1h", ("app",))


reviews: list = []  # the access reviews, which the person did not ask for


def _window(monkeypatch, write_mode: bool = True):
    window = _ready_window(monkeypatch)
    window.settings.write_mode = write_mode
    ran = []
    reviews.clear()

    def record(op, ok, *args, **kwargs) -> None:
        if op.__name__ == "allowed_actions":
            reviews.append((args, ok, kwargs))
        else:
            ran.append((op.__name__, args, kwargs))

    monkeypatch.setattr(window, "_run_action", record)
    return window, ran


def _fake_menu(monkeypatch, seen: list) -> None:
    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            seen.append([action.text() for action in self.actions()])
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)


def test_the_row_menu_offers_writes_only_in_the_write_mode(monkeypatch) -> None:
    window, _ran = _window(monkeypatch, write_mode=False)
    window.show()
    seen: list = []
    _fake_menu(monkeypatch, seen)
    window._show_workloads(["ns"], [API])
    pos = QPoint(5, window.table.rowViewportPosition(0) + 2)

    window._show_row_menu(pos)
    assert seen[-1] == ["Pods", "Details", "Logs"]  # read-only: nothing else

    window.settings.write_mode = True
    window._show_row_menu(pos)
    assert seen[-1] == ["Pods", "Details", "Logs", "", "Scale", "Restart", "Delete"]

    window._open_list_view("statefulsets")
    window._show_workloads(["ns"], [Workload("ns", "StatefulSet", "db", 1, 1, "1d")])
    window._show_row_menu(pos)
    assert seen[-1] == ["Pods", "Details", "Logs", "", "Forward", "Delete"]

    window._open_list_view("pods")
    window._show_pods(["ns"], [POD])
    window._show_row_menu(pos)
    assert seen[-1] == [
        "Details",
        "Logs",
        "",
        "Shell command",
        "Evict",
        "Delete",
        "Forward",
    ]
    window.close()


def test_confirming_runs_the_action_and_cancelling_does_not(monkeypatch) -> None:
    window, ran = _window(monkeypatch)
    answer = {"yes": False}
    asked = []

    def confirm(title, text, action):
        asked.append(action)
        return answer["yes"]

    monkeypatch.setattr(window, "_confirm", confirm)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    calls = (
        lambda: window._delete_pod(POD),
        lambda: window._evict_pod(POD),
        lambda: window._restart_deployment(API),
    )

    for call in calls:
        call()  # cancelled
    assert ran == []

    answer["yes"] = True
    for call in calls:
        call()

    assert [(name, args) for name, args, _k in ran] == [
        ("delete_pod", ("prod", "ns", "api-1")),
        ("evict_pod", ("prod", "ns", "api-1")),
        ("restart_deployment", ("prod", "ns", "api")),
    ]
    assert all(k["on_error"] == window._show_write_error for _n, _a, k in ran)
    assert asked == ["Delete", "Evict", "Restart"] * 2


def test_scaling_asks_for_the_count_and_skips_a_no_change(monkeypatch) -> None:
    window, ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    answers = iter([(5, True), (3, True), (7, False)])
    prompts = []

    def ask(title, label, current):
        prompts.append((label, current))
        return next(answers)

    monkeypatch.setattr(window, "_ask_replicas", ask)

    window._scale_deployment(API)  # 3 -> 5
    window._scale_deployment(API)  # 3 -> 3: nothing to do
    window._scale_deployment(API)  # cancelled

    assert [(n, a) for n, a, _k in ran] == [
        ("scale_deployment", ("prod", "ns", "api", 5))
    ]
    assert prompts[0] == ("Replicas of api in ns:", 3)


def test_the_confirmation_defaults_to_cancel_and_reports_the_choice(
    monkeypatch,
) -> None:
    window, _ran = _window(monkeypatch)
    defaults = []

    def click_first(box):
        defaults.append(box.defaultButton().text())
        box.buttons()[0].click()

    monkeypatch.setattr(QMessageBox, "exec", click_first)
    assert window._confirm("Delete Pod", "Delete it?", "Delete") is True

    def click_cancel(box):
        box.buttons()[1].click()

    monkeypatch.setattr(QMessageBox, "exec", click_cancel)
    assert window._confirm("Delete Pod", "Delete it?", "Delete") is False
    assert defaults == ["Cancel"]
    window.close()


def test_the_replicas_dialog_returns_the_chosen_count(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    seen = {}

    def fake_exec(dialog):
        spin = dialog.findChild(QSpinBox)
        seen["range"] = (spin.minimum(), spin.maximum(), spin.value())
        spin.setValue(9)
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(QDialog, "exec", fake_exec)
    assert window._ask_replicas("Scale", "Replicas:", 3) == (9, True)
    assert seen["range"] == (0, MAX_REPLICAS, 3)

    monkeypatch.setattr(QDialog, "exec", lambda _d: QDialog.DialogCode.Rejected)
    assert window._ask_replicas("Scale", "Replicas:", 3)[1] is False
    window.close()


def test_a_finished_write_says_so_and_refreshes(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    refreshed = []
    monkeypatch.setattr(window, "refresh", lambda: refreshed.append(True))

    window._write_done("Deleted the Pod api-1")

    assert window.status_label.text() == "Deleted the Pod api-1"
    assert refreshed == [True]


def test_a_failed_write_shows_the_cluster_message_in_the_banner(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)

    window._show_write_error("pods is forbidden\nmore detail")
    assert "not allowed to do this" in window.ui.permissionLabel.text()
    assert window.ui.permissionDetailsText.text() == "pods is forbidden\nmore detail"

    window.permission_banner.hide()
    window._close_when_worker_stops = True
    window._show_write_error("cancelled")  # the window is closing: nothing shown
    assert window.permission_banner.isHidden()
    window._close_when_worker_stops = False
    window.close()


def test_run_write_dispatches_with_the_write_error_handler(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    captured = []
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda op, ok, *a, **k: captured.append((ok, a, k)),
    )
    done = []
    monkeypatch.setattr(
        window, "_write_done", lambda message, after=None: done.append(message)
    )

    window._run_write(print, "Did it", "x")
    ok, args, kwargs = captured[0]
    ok(None)

    assert args == ("x",) and kwargs == {"on_error": window._show_write_error}
    assert done == ["Did it"]
    window.close()


def test_the_shell_dialog_lets_the_person_pick_the_container(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    seen = {}

    def fake_exec(dialog) -> int:
        combo = dialog.findChild(QComboBox)
        box = dialog.findChild(QPlainTextEdit)
        buttons = {b.text(): b for b in dialog.findChildren(QPushButton)}
        seen["variant"] = combo.property("variant")
        seen["items"] = [combo.itemText(i) for i in range(combo.count())]
        seen["readonly"] = box.isReadOnly()
        seen["first"] = box.toPlainText()
        combo.setCurrentIndex(1)  # the command follows the container
        seen["second"] = box.toPlainText()
        buttons["Copy"].click()
        seen["clipboard"] = QApplication.clipboard().text()
        buttons["Close"].click()
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._show_shell_command(POD)  # app and sidecar

    assert seen["variant"] == "filter" and seen["readonly"] is True
    assert seen["items"] == ["app", "sidecar"]
    assert seen["first"] == writes.shell_commands("prod", "ns", "api-1", "app")[0][1]
    assert (
        seen["second"] == writes.shell_commands("prod", "ns", "api-1", "sidecar")[0][1]
    )
    assert seen["clipboard"] == seen["second"]
    window.close()


def test_a_pod_without_containers_has_no_shell_command(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    infos = []
    monkeypatch.setattr(QMessageBox, "exec", lambda box: infos.append(box.text()))

    window._show_shell_command(PodInfo("ns", "bare", "Running", 0, 0, "1h", ()))

    assert infos == ["Pod bare has no containers."]
    window.close()


def test_the_pods_dialog_menu_offers_the_writes_and_closes_first(monkeypatch) -> None:
    window, ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    monkeypatch.setattr(window, "_confirm", lambda *_a: True)
    workload = Workload("ns", "Deployment", "api", 1, 1, "1d")
    seen: list = []
    pick = {"index": 2}  # Delete...

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            seen.append([action.text() for action in self.actions()])
            self.actions()[pick["index"]].trigger()
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)
    closed = []

    def fake_exec(dialog) -> int:
        dialog.accepted.connect(lambda: closed.append(True))
        table = dialog.findChild(QTableWidget, "podsTable")
        position = QPoint(5, table.rowViewportPosition(0) + 2)
        table.customContextMenuRequested.emit(QPoint(5, 5000))  # no row
        assert seen == []
        window.settings.write_mode = False
        table.customContextMenuRequested.emit(position)  # read-only
        assert seen == []
        window.settings.write_mode = True
        table.customContextMenuRequested.emit(position)
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._show_pods_dialog(workload, [POD])

    assert seen == [["Shell command", "Evict", "Delete", "Forward"]]
    assert closed == [True]
    assert [(n, a) for n, a, _k in ran] == [("delete_pod", ("prod", "ns", "api-1"))]
    window.close()


def test_the_write_mode_is_switched_from_the_settings_page(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    form = window.settings_ui

    window._load_settings_form()
    assert form.writeModeCheck.isChecked() is False  # read-only by default

    window._save_preferences()  # unchanged: nothing logged as a change
    assert window.settings.write_mode is False

    assert "read-only" in window.ui.sidebarNote.text()

    form.writeModeCheck.setChecked(True)
    window._save_preferences()
    assert window.settings.write_mode is True
    assert window.ui.sidebarNote.text().startswith("WRITE MODE")  # the note follows

    window._retranslate()
    assert window.ui.sidebarNote.text().startswith("WRITE MODE")

    form.writeModeCheck.setChecked(False)
    window._save_preferences()
    assert "read-only" in window.ui.sidebarNote.text()
    form.writeModeCheck.setChecked(True)
    window._save_preferences()

    window._load_settings_form()
    assert form.writeModeCheck.isChecked() is True
    window.close()


def _visible_write_buttons(window) -> list[str]:
    """The write actions offered for the row picked: the bar of buttons shows
    only while rows are checked, and the menu of the row has what is
    offered."""
    return [
        button.text()
        for button in window.write_buttons.values()
        if button in window._offered
    ]


def _shown_write_buttons(window) -> list[str]:
    """The write actions the view and the mode have, once a row is picked."""
    return [
        button.text()
        for shape, button in window.write_buttons.items()
        if shape in window._shown_shapes
    ]


def test_the_write_buttons_follow_the_view_and_the_write_mode(monkeypatch) -> None:
    window, _ran = _window(monkeypatch, write_mode=False)
    window.show()
    window._show_workloads(["ns"], [API])
    assert _shown_write_buttons(window) == []  # read-only: none

    window.settings.write_mode = True
    window._apply_view_buttons()
    assert _shown_write_buttons(window) == ["Scale", "Restart", "Delete"]
    assert all(not b.isEnabled() for b in window.write_buttons.values())  # no row
    assert _visible_write_buttons(window) == []  # and none is offered
    assert not any(b.isVisibleTo(window) for b in window.write_buttons.values())

    window.table.selectRow(0)
    assert window.write_buttons["scale"].isEnabled()

    window._open_list_view("statefulsets")
    assert _shown_write_buttons(window) == ["Forward", "Delete"]

    window._open_list_view("daemonsets")
    assert _shown_write_buttons(window) == ["Delete"]
    assert window._write_entries() == []  # no row to delete

    window._open_list_view("pods")
    window._show_pods(["ns"], [POD])
    assert _shown_write_buttons(window) == [
        "Shell command",
        "Evict",
        "Forward",
        "Delete",
    ]

    window.settings.write_mode = False
    window._apply_view_buttons()
    assert _shown_write_buttons(window) == []
    window.close()


def test_a_write_button_does_what_its_menu_entry_does(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    window.show()
    calls = []
    monkeypatch.setattr(
        window, "_scale_deployment", lambda w: calls.append(("scale", w))
    )
    monkeypatch.setattr(
        window, "_restart_deployment", lambda w: calls.append(("restart", w))
    )
    window._show_workloads(["ns"], [API])
    window.table.selectRow(0)

    window.write_buttons["scale"].click()
    window.write_buttons["reload"].click()
    asked = []
    monkeypatch.setattr(window, "_confirm", lambda *a: asked.append(a[2]) or False)
    window.write_buttons["delete"].click()  # cancelled: nothing is deleted

    assert calls == [("scale", API), ("restart", API)]
    assert asked == ["Delete"]
    window.close()


def test_the_write_buttons_are_drawn_in_the_theme_and_the_language(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    window.show()
    window._open_list_view("pods")

    window._apply_style()
    assert all(not b.icon().isNull() for b in window.write_buttons.values())

    window._retranslate()  # the texts are set again
    assert window.write_buttons["evict"].text() == "Evict"
    window.close()


SERVICE = ClusterResource("ns", "Service", "api", ("ClusterIP",), "1d")
SERVICE_DOCUMENT = {
    "spec": {"ports": [{"port": 80, "name": "http"}, {"port": 8443, "name": "tls"}]}
}


def _services_window(monkeypatch):
    window, ran = _window(monkeypatch)
    window.show()
    window._open_list_view("services")
    window._show_resources(["ns"], [SERVICE])
    window.table.selectRow(0)
    return window, ran


def test_a_service_offers_forward_as_a_button_and_a_menu_entry(monkeypatch) -> None:
    window, _ran = _services_window(monkeypatch)
    seen: list = []
    _fake_menu(monkeypatch, seen)
    calls = []
    monkeypatch.setattr(window, "_forward_service", lambda s: calls.append(s))

    assert _visible_write_buttons(window) == ["Forward", "Delete"]
    window.write_buttons["forward"].click()
    window._show_row_menu(QPoint(5, window.table.rowViewportPosition(0) + 2))

    assert calls == [SERVICE]
    assert seen[-1] == ["Details", "", "Forward", "Delete"]

    window.settings.write_mode = False
    window._apply_view_buttons()
    assert _visible_write_buttons(window) == []
    window.close()


def test_forward_reads_the_ports_of_the_service(monkeypatch) -> None:
    window, ran = _services_window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")

    window._forward_service(SERVICE)

    assert ran == [("get_resource_details", ("prod", "Service", "ns", "api"), {})]
    window.close()


def test_the_forward_dialog_builds_the_command_for_the_chosen_ports(
    monkeypatch,
) -> None:
    window, _ran = _services_window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    seen = {}

    def fake_exec(dialog) -> int:
        combo = dialog.findChild(QComboBox)
        local = dialog.findChild(QSpinBox)
        box = dialog.findChild(QPlainTextEdit)
        buttons = {b.text(): b for b in dialog.findChildren(QPushButton)}
        seen["variants"] = (combo.property("variant"), local.property("variant"))
        seen["first"] = (local.value(), box.toPlainText())
        local.setValue(9000)
        seen["local"] = box.toPlainText()
        combo.setCurrentIndex(1)  # 8443: the local port follows
        seen["second"] = (local.value(), box.toPlainText())
        buttons["Copy"].click()
        seen["clipboard"] = QApplication.clipboard().text()
        buttons["Close"].click()
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._show_forward_command(SERVICE, SERVICE_DOCUMENT)

    assert seen["variants"] == ("filter", "filter")
    assert seen["first"] == (
        8080,
        writes.forward_commands("prod", "ns", "api", 80, 8080)[0][1],
    )
    assert seen["local"] == writes.forward_commands("prod", "ns", "api", 80, 9000)[0][1]
    assert seen["second"] == (
        8443,
        writes.forward_commands("prod", "ns", "api", 8443, 8443)[0][1],
    )
    assert seen["clipboard"] == seen["second"][1]
    window.close()


def test_a_service_without_tcp_ports_cannot_be_forwarded(monkeypatch) -> None:
    window, _ran = _services_window(monkeypatch)
    infos = []
    monkeypatch.setattr(QMessageBox, "exec", lambda box: infos.append(box.text()))

    window._show_forward_command(SERVICE, {"spec": {"ports": []}})

    assert infos == ["Service api has no TCP ports to forward."]
    window.close()


def test_a_pod_and_a_statefulset_read_their_ports_and_their_services(
    monkeypatch,
) -> None:
    window, ran = _window(monkeypatch)
    window.show()
    monkeypatch.setattr(window, "_context", lambda: "prod")

    window._forward("Pod", POD)
    window._forward("StatefulSet", Workload("ns", "StatefulSet", "db", 1, 1, "1d"))

    assert [(n, a) for n, a, _k in ran] == [
        ("get_forward_sources", ("prod", "Pod", POD.namespace, POD.name)),
        ("get_forward_sources", ("prod", "StatefulSet", "ns", "db")),
    ]
    window.close()


def test_the_forward_dialog_lists_the_ports_of_the_services_too(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    seen = {}

    def fake_exec(dialog) -> int:
        combo = dialog.findChild(QComboBox)
        seen["items"] = [combo.itemText(i) for i in range(combo.count())]
        seen["command"] = dialog.findChild(QPlainTextEdit).toPlainText()
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)
    db = Workload("ns", "StatefulSet", "db", 1, 1, "1d")
    document = {
        "spec": {
            "template": {
                "metadata": {"labels": {"app": "db"}},
                "spec": {"containers": [{}]},
            }
        }
    }
    services = [
        {
            "metadata": {"name": "db"},
            "spec": {"selector": {"app": "db"}, "ports": [{"port": 5432}]},
        }
    ]

    window._show_forward_command(db, document, "StatefulSet", services)

    assert seen["items"] == ["5432 (Service db)"]
    assert (
        seen["command"]
        == writes.forward_commands("prod", "ns", "db", 5432, 5432, "statefulset")[0][1]
    )
    window.close()


def test_without_any_port_the_person_types_the_one_the_pod_listens_on(
    monkeypatch,
) -> None:
    window, _ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    seen = {}

    def fake_exec(dialog) -> int:
        remote, local = dialog.findChildren(QSpinBox)
        assert dialog.findChild(QComboBox) is None
        box = dialog.findChild(QPlainTextEdit)
        seen["first"] = (remote.value(), local.value(), box.toPlainText())
        remote.setValue(80)  # below 1024: the local port is shifted up
        seen["second"] = (local.value(), box.toPlainText())
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._show_forward_command(POD, {"spec": {"containers": [{}]}}, "Pod", [])

    assert seen["first"] == (
        8080,
        8080,
        writes.forward_commands("prod", POD.namespace, POD.name, 8080, 8080, "pod")[0][
            1
        ],
    )
    assert seen["second"] == (
        8080,
        writes.forward_commands("prod", POD.namespace, POD.name, 80, 8080, "pod")[0][1],
    )
    window.close()


def test_on_windows_the_command_dialog_has_a_box_for_each_shell(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    monkeypatch.setattr(writes.sys, "platform", "win32")
    seen = {}

    def fake_exec(dialog) -> int:
        boxes = dialog.findChildren(QPlainTextEdit)
        copies = [b for b in dialog.findChildren(QPushButton) if b.text() == "Copy"]
        labels = [label.text() for label in dialog.findChildren(QLabel)]
        seen["texts"] = [box.toPlainText() for box in boxes]
        dialog.findChild(QComboBox).setCurrentIndex(1)  # the boxes follow it
        seen["after"] = [box.toPlainText() for box in boxes]
        copies[1].click()
        seen["clipboard"] = QApplication.clipboard().text()
        seen["labels"] = [t for t in labels if t in ("PowerShell", "cmd")]
        seen["copies"] = len(copies)
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._show_shell_command(POD)

    expected = writes.shell_commands("prod", "ns", "api-1", "sidecar")
    assert seen["labels"] == ["PowerShell", "cmd"] and seen["copies"] == 2
    assert seen["after"] == [command for _shell, command in expected]
    assert seen["clipboard"] == expected[1][1]  # the cmd one
    assert "'" in seen["texts"][0] and '"' in seen["texts"][1]
    window.close()


def test_the_buttons_and_menus_offer_only_what_the_cluster_allows(
    monkeypatch,
) -> None:
    window, _ran = _window(monkeypatch)
    window.show()
    monkeypatch.setattr(window, "_context", lambda: "prod")
    seen: list = []
    _fake_menu(monkeypatch, seen)
    window._open_list_view("pods")
    window._show_pods(["ns"], [POD])
    window.table.selectRow(0)

    assert reviews[0][0] == ("prod", "ns")  # asked, no answer yet
    assert _visible_write_buttons(window) == [
        "Shell command",
        "Evict",
        "Forward",
        "Delete",
    ]

    window._permissions_read(("prod", "ns"), frozenset({"shell", "forward"}))

    assert _visible_write_buttons(window) == ["Shell command", "Forward"]
    window._show_row_menu(QPoint(5, window.table.rowViewportPosition(0) + 2))
    assert seen[-1] == ["Details", "Logs", "", "Shell command", "Forward"]
    assert len(reviews) == 1  # the answer is kept

    window._permissions_read(("prod", "ns"), frozenset())
    assert _visible_write_buttons(window) == []
    window.close()


def test_the_permissions_are_asked_again_when_old_or_cleared(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    window.show()
    monkeypatch.setattr(window, "_context", lambda: "prod")
    window._open_list_view("pods")
    window._show_pods(["ns"], [POD])
    window.table.selectRow(0)
    key = ("prod", "ns")
    window._permissions_read(key, frozenset({"shell"}))
    asked = len(reviews)

    window._update_workload_actions()
    assert len(reviews) == asked

    window._permissions[key] = (-1e9, frozenset({"shell"}))  # long ago
    window._update_workload_actions()
    assert len(reviews) == asked + 1
    window._update_workload_actions()  # still waiting for that answer
    assert len(reviews) == asked + 1

    # a failed review is tried again at the next selection
    reviews[-1][2]["on_error"]("boom")
    window._update_workload_actions()
    assert len(reviews) == asked + 2

    window.settings.write_mode = False
    window._update_workload_actions()
    assert len(reviews) == asked + 2  # read-only never asks
    window.close()


EVENT = ClusterResource(
    "ns", "Event", "api.1", ("Warning", "BackOff", "Pod/api", "Back-off", "3"), "1m"
)
CLASS = ClusterResource("", "PriorityClass", "high", ("1000", "false"), "1d")


def test_delete_asks_and_deletes_any_resource(monkeypatch) -> None:
    window, ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    answer = {"yes": False}
    questions = []

    def confirm(title, text, action):
        questions.append((title, text))
        return answer["yes"]

    monkeypatch.setattr(window, "_confirm", confirm)

    window._delete_resource(API)  # cancelled
    assert ran == []

    answer["yes"] = True
    window._delete_resource(API)
    window._delete_resource(CLASS)

    assert [(n, a) for n, a, _k in ran] == [
        ("delete_resource", ("prod", "Deployment", "ns", "api")),
        ("delete_resource", ("prod", "PriorityClass", "", "high")),
    ]
    assert questions[0][1] == "Delete the Deployment api in ns?"
    assert questions[-1] == ("Delete PriorityClass", "Delete the PriorityClass high?")


def test_an_event_offers_edit_and_delete(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    window.show()
    window._open_list_view("events")
    window._show_resources(["ns"], [EVENT])
    window.table.selectRow(0)

    assert _visible_write_buttons(window) == ["Edit", "Delete"]
    assert [entry[0] for entry in window._write_entries()] == ["edit", "delete"]
    window.close()


def _edit(monkeypatch, text):
    window, ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")
    messages = []
    monkeypatch.setattr(window, "_show_message", lambda *a, **k: messages.append(a))

    def fake_exec(dialog):
        if text is None:
            return QDialog.DialogCode.Rejected
        dialog.findChild(QPlainTextEdit).setPlainText(text)
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(QDialog, "exec", fake_exec)
    window._edit_dialog(EVENT, {"kind": "Event"})
    return ran, messages


def test_editing_an_event_replaces_it_with_the_edited_json(monkeypatch) -> None:
    ran, messages = _edit(monkeypatch, '{"kind": "Event", "message": "new"}')

    assert [(n, a) for n, a, _k in ran] == [
        (
            "replace_resource",
            ("prod", "Event", "ns", "api.1", {"kind": "Event", "message": "new"}),
        )
    ]
    assert messages == []


def test_editing_refuses_what_is_not_a_json_object(monkeypatch) -> None:
    for text in ("{not json", "[1]"):
        ran, messages = _edit(monkeypatch, text)
        assert ran == [] and messages[0][1] == "Invalid JSON"


def test_cancelling_the_edit_changes_nothing(monkeypatch) -> None:
    ran, messages = _edit(monkeypatch, None)

    assert ran == [] and messages == []


def test_editing_reads_the_event_first(monkeypatch) -> None:
    window, ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_context", lambda: "prod")

    window._edit_resource(EVENT)

    assert [(n, a) for n, a, _k in ran] == [
        ("get_resource_details", ("prod", "Event", "ns", "api.1"))
    ]


def test_what_was_done_is_told_with_a_notice_of_the_system(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    notices: list[tuple] = []
    monkeypatch.setattr(
        window, "_system_notification", lambda *args: notices.append(args) or True
    )
    after: list[int] = []

    window._write_done("Deleted the Pod solo", lambda: after.append(1))
    window._write_done("Scaled api")

    assert notices == [
        ("KubeScope", "Deleted the Pod solo", None),
        ("KubeScope", "Scaled api", None),
    ]
    assert after == [1]
    window.close()


def test_a_deleted_pod_is_watched_until_another_is_ready_in_its_place(
    monkeypatch,
) -> None:
    window, _ran = _window(monkeypatch)
    told: list[str] = []
    monkeypatch.setattr(
        window, "_notify", lambda message, _category="action": told.append(message)
    )
    later: list = []
    monkeypatch.setattr(
        window_module.QTimer, "singleShot", lambda _ms, call: later.append(call)
    )
    answers = iter(
        [
            ClusterError("offline"),  # a look that fails is tried again
            ([], [PodInfo("ns", "solo-new", "Pending", 0, 1, "1s", ("app",))]),
            ([], [PodInfo("ns", "solo-new", "Running", 1, 1, "3s", ("app",))]),
        ]
    )

    def run_action(_operation, on_success, *_arguments, on_error=None, **_kwargs):
        answer = next(answers)
        if isinstance(answer, Exception):
            assert on_error is not None
            on_error(str(answer))
        else:
            on_success(answer)

    monkeypatch.setattr(window, "_run_action", run_action)

    window._watch_replacement(SINGLE)
    assert told == [] and len(later) == 1
    later.pop()()  # the next look: a Pod that is not ready yet
    assert told == [] and len(later) == 1
    later.pop()()  # the next: it is ready

    assert told == ["solo was replaced by solo-new, which is ready"]
    assert later == []
    window.close()


def test_a_pod_that_does_not_come_back_in_time_is_told_too(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    told: list[str] = []
    monkeypatch.setattr(
        window, "_notify", lambda message, _category="action": told.append(message)
    )
    monkeypatch.setattr(window_module, "WATCH_SECONDS", 0.0)
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda _op, on_success, *_a, **_k: on_success(([], [])),
    )

    window._watch_replacement(SINGLE)

    assert told == ["No new Pod for solo is ready yet"]
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda _op, _ok, *_a, on_error, **_k: on_error("offline"),
    )
    told.clear()
    window._watch_replacement(SINGLE)  # a failed look after the time is up
    assert told == ["No new Pod for solo is ready yet"]
    window.close()


def test_deleting_or_evicting_a_pod_watches_for_its_replacement(monkeypatch) -> None:
    window, _ran = _window(monkeypatch)
    monkeypatch.setattr(window, "_confirm", lambda *_a: True)
    watched: list[str] = []
    monkeypatch.setattr(
        window, "_watch_replacement", lambda pod: watched.append(pod.name)
    )
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda _op, ok, *_a, **_k: ok(None),
    )
    monkeypatch.setattr(window, "refresh", lambda *a, **k: None)
    monkeypatch.setattr(window, "_system_notification", lambda *a: True)

    window._delete_pod(SINGLE)
    window._evict_pod(SINGLE)

    assert watched == ["solo", "solo"]
    window.close()


def test_what_was_done_goes_to_the_notifications_when_they_are_there(
    monkeypatch,
) -> None:
    window, _ran = _window(monkeypatch)
    direct: list[tuple] = []
    monkeypatch.setattr(
        window, "_system_notification", lambda *args: direct.append(args) or True
    )
    heard: list[dict] = []
    window.extension_host.events.on(NOTIFICATION, lambda **notice: heard.append(notice))
    monkeypatch.setattr(window, "_context", lambda: "prod")

    window._notify("Scaled api")
    window._notify("web is ready", "pod")
    window._tell("Gabi", "done", None)  # no category: the system at once

    assert [(n["category"], n["message"], n["context"]) for n in heard] == [
        ("action", "Scaled api", "prod"),
        ("pod", "web is ready", "prod"),
    ]
    assert heard[0]["key"] != heard[1]["key"] and heard[0]["system"] is True
    assert direct == [("Gabi", "done", None)]
    window.close()
