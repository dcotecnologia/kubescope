import json
import os
import threading
import time
from typing import cast

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import (
    QEvent,
    QMimeData,
    QObject,
    QPoint,
    QPointF,
    QRect,
    QStringListModel,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QHelpEvent,
    QMouseEvent,
    QPalette,
    QShortcut,
)
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QComboBox,
    QDialog,
    QMenu,
    QMessageBox,
    QPushButton,
    QStyleOptionViewItem,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
    QWidget,
)

from kubescope import cluster as cluster_module
from kubescope import theme
from kubescope import window as window_module
from kubescope.cluster import ClusterError, LoginAction
from kubescope.models import (
    CONFIG_VIEWS,
    ClusterInfo,
    ClusterOverview,
    ClusterResource,
    EventInfo,
    KindSummary,
    NodeInfo,
    PodInfo,
    Workload,
    WorkloadsOverview,
)
from kubescope.settings import Settings
from kubescope.theme import themed
from kubescope.utils import json_view
from kubescope.utils.updates import Release, UpdateCheck
from kubescope.views.container_states import LINK_ROLE, STATES_ROLE, TIPS_ROLE
from kubescope.views.detail_tab import DetailTab
from kubescope.views.log_tab import LogTab
from kubescope.window import PIN_MIME, VIEWER_MIME
from tests.qt import (
    cell,
    current_tab,
    get_application,
    present,
    tab_at,
    text_at,
)

application = QApplication.instance() or QApplication([])


class FakeRefreshWorker(QObject):
    """Stands in for RefreshWorker: finishes at once with a canned outcome."""

    completed = Signal(list, list)
    failed = Signal(str)
    finished = Signal()
    outcome: tuple = ("ok", ([], []))
    running = False

    def __init__(self, context, namespace, view="deployments") -> None:
        super().__init__()
        self.context, self.namespace, self.view = context, namespace, view
        self.key = (context, namespace, view)

    def isRunning(self) -> bool:
        return self.running

    def start(self) -> None:
        kind, payload = self.outcome
        if kind == "ok":
            self.completed.emit(*payload)
        else:
            self.failed.emit(payload)
        self.finished.emit()


def _detail_tab(window) -> DetailTab:
    return current_tab(window.viewer_tabs, DetailTab)


def _ready_window(monkeypatch):
    """A window with a "prod" context and no real kubectl behind it."""
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    monkeypatch.setattr(
        window_module.WorkloadWindow, "refresh_overview", lambda *_a: None
    )
    monkeypatch.setattr(window_module, "RefreshWorker", FakeRefreshWorker)
    window = window_module.WorkloadWindow()
    _wait_until(lambda: not window._action_workers)  # the kubeconfig read
    window.context_combo.blockSignals(True)
    window.context_combo.addItem("prod")
    window.context_combo.setCurrentIndex(0)
    window.context_combo.blockSignals(False)
    return window


def _wait_until(condition, seconds: float = 3.0) -> None:
    deadline = time.monotonic() + seconds
    while not condition() and time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.005)
    assert condition()


POD = PodInfo("ns", "api-1", "Running", 1, 2, "1h", ("app", "sidecar"))


def test_refresh_worker_adds_restarts_and_usage_to_deployments(monkeypatch) -> None:
    deployment = Workload("a", "Deployment", "api", 1, 1, "1d")
    stateful = Workload("a", "StatefulSet", "db", 1, 1, "1d")
    other = Workload("a", "Deployment", "web", 1, 1, "1d")
    monkeypatch.setattr(
        window_module,
        "get_workloads",
        lambda _c, _n, kinds: (
            ["a"],
            [w for w in (deployment, stateful, other) if w.kind in kinds],
        ),
    )
    monkeypatch.setattr(
        window_module,
        "get_usage",
        lambda *_a: {("a", "Deployment", "api"): (2, 0.5, 100.0)},
    )
    done = []
    worker = window_module.RefreshWorker("ctx", None)
    worker.completed.connect(lambda namespaces, items: done.append((namespaces, items)))

    worker.run()

    namespaces, items = done[0]
    assert namespaces == ["a"]
    assert [(i.name, i.restarts, i.cpu, i.memory) for i in items] == [
        ("api", 2, 0.5, 100.0),
        ("web", 0, None, None),
    ]


def test_refresh_worker_keeps_going_when_usage_fails(monkeypatch) -> None:
    monkeypatch.setattr(
        window_module,
        "get_workloads",
        lambda *_a: (["a"], [Workload("a", "Deployment", "api", 1, 1, "1d")]),
    )

    def broken(*_args):
        raise ClusterError("no metrics")

    monkeypatch.setattr(window_module, "get_usage", broken)
    done = []
    worker = window_module.RefreshWorker("ctx", "a")
    worker.completed.connect(lambda _n, items: done.append(items))

    worker.run()

    assert done[0][0].cpu is None


def test_refresh_worker_loads_pods_and_reports_failures(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "get_pods", lambda *_a: (["ns"], [POD]))
    done, failures = [], []
    worker = window_module.RefreshWorker("ctx", None, "pods")
    worker.completed.connect(lambda namespaces, items: done.append((namespaces, items)))
    worker.failed.connect(failures.append)

    worker.run()
    assert done == [(["ns"], [POD])]

    def broken(*_args):
        raise ClusterError("denied")

    monkeypatch.setattr(window_module, "get_pods", broken)
    worker.run()
    assert failures == ["denied"]


def test_action_worker_returns_results_and_errors() -> None:
    done, failures = [], []
    worker = window_module.ActionWorker(lambda a, b: a + b, (1, 2))
    worker.completed.connect(done.append)
    worker.failed.connect(failures.append)

    worker.run()
    assert done == [3]

    def broken():
        raise ClusterError("nope")

    failing = window_module.ActionWorker(broken, ())
    failing.failed.connect(failures.append)
    failing.run()
    assert failures == ["nope"]


def test_loading_spins_the_button_and_leaves_the_cursor_alone(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._tick_spinner()  # nothing to animate yet
    labelled, other = window.details_button, window.logs_button
    original = labelled.text()
    assert original  # this one has a text, which shows the label meanwhile

    end = window._begin_loading(labelled, "Wait")
    nested = window._begin_loading(other, "Other")
    window._begin_loading(None, "ignored")
    assert QApplication.overrideCursor() is None  # never a busy cursor
    assert labelled.text() == "Wait"
    assert other.text() != "Other"  # only one spinner at a time

    window._spinner_button = other
    window._tick_spinner()
    window._spinner_button = labelled
    end()
    end()  # a second call changes nothing
    assert labelled.text() == original
    nested()
    window._end_loading(None)
    assert QApplication.overrideCursor() is None
    window.close()


def test_refresh_buttons_show_only_an_icon_and_keep_it_spinning(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    pods = PodInfo("ns", "api-1", "Running", 1, 1, "1h", ("app",))
    window._show_logs_dialog(pods, "app", "line")
    buttons = {
        "list": window.refresh_button,
        "cluster overview": window.overview_refresh_button,
        "workloads overview": window.workloads_refresh_button,
        "logs": tab_at(window.viewer_tabs, 0, LogTab).ui.refreshButton,
    }

    for name, button in buttons.items():
        assert button.text() == "", name
        assert button.toolTip().startswith("Refresh"), name
        assert not button.icon().isNull(), name
        assert button.property("iconOnly") == "true", name

    button = window.refresh_button
    end = window._begin_loading(button, "Refreshing...")
    assert button.text() == ""  # it spins; no label is squeezed into the icon
    spinning = button.icon().cacheKey()
    window._tick_spinner()
    assert button.icon().cacheKey() != spinning
    end()
    assert button.text() == "" and not button.icon().isNull()
    window.close()


def test_refresh_fills_the_table_or_shows_the_error(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    workload = Workload("ns", "Deployment", "api", 1, 1, "1d")
    FakeRefreshWorker.outcome = ("ok", (["ns"], [workload]))

    window.refresh()
    assert window.table.rowCount() == 1
    assert window.refresh_button.isEnabled()

    FakeRefreshWorker.outcome = ("ok", (["ns"], [POD]))
    window._open_list_view("pods")
    window.refresh()
    assert window.table.rowCount() == 1

    FakeRefreshWorker.outcome = ("error", "Unable to connect to the server")
    window.refresh()
    assert window.table.rowCount() == 0
    assert "Unable to connect" in window.status_label.toolTip()
    FakeRefreshWorker.outcome = ("ok", ([], []))
    window.close()


def test_refresh_does_nothing_without_a_context_or_while_running(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.context_combo.clear()
    window.refresh()
    assert window._workers == {}

    window.context_combo.addItem("prod")
    running = FakeRefreshWorker("prod", None)
    running.running = True
    window._workers["deployments"] = cast(window_module.RefreshWorker, running)
    window.refresh()
    assert window._workers["deployments"] is running
    window.close()


def test_each_list_loads_in_parallel_with_the_others(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.context_combo.addItem("prod")
    pods = FakeRefreshWorker("prod", None, "pods")
    pods.running = True
    window._workers["pods"] = cast(window_module.RefreshWorker, pods)
    window._view = "deployments"

    window.refresh()  # does not wait for the Pods request

    assert window._workers["pods"] is pods
    assert window._workers["deployments"] is not pods
    assert window.context_combo.isEnabled()  # a list loading never locks it
    window._view = "pods"  # back on the list that is loading: it spins
    window._sync_loading()
    assert window.refresh_button.isEnabled()  # as the way to cancel
    pods.running = False
    window._refresh_finished()
    assert window.context_combo.isEnabled() and window.refresh_button.isEnabled()
    window.close()


def test_another_context_cancels_the_list_that_is_loading(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    cancelled = []
    monkeypatch.setattr(window_module, "cancel_running", lambda: cancelled.append(1))
    window.context_combo.addItem("other")
    running = FakeRefreshWorker("prod", None)
    running.running = True
    window._workers["deployments"] = cast(window_module.RefreshWorker, running)

    window.context_combo.setCurrentIndex(window.context_combo.count() - 1)

    assert cancelled and running in window._retired
    assert window._workers["deployments"] is not running
    assert window._workers["deployments"].context == "other"
    running.running = False
    window._refresh_finished(running)
    assert running not in window._retired
    window.close()


def test_the_refresh_button_cancels_a_load_and_hides_its_answer(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    monkeypatch.setattr(window_module, "cancel_running", lambda: None)
    running = FakeRefreshWorker("prod", None)
    running.running = True
    window._workers["deployments"] = cast(window_module.RefreshWorker, running)

    window._refresh_or_cancel()

    assert "deployments" not in window._workers and running in window._retired
    window.close()


def test_contexts_are_listed_alphabetically(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._contexts = ["zeta", "Beta", "alpha"]
    window._fill_contexts(None)

    names = [window.context_combo.itemData(i) for i in range(3)]

    assert names == ["alpha", "Beta", "zeta"]
    window.close()


def test_an_answer_for_a_list_the_person_left_is_kept_for_when_they_return(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    shown = []
    monkeypatch.setattr(window, "_show_pods", lambda *a: shown.append(("pods", a)))
    monkeypatch.setattr(window, "_show_workloads", lambda *a: shown.append(("w", a)))
    window.context_combo.addItem("prod")
    window._view = "deployments"

    window._answered("prod", None, "pods", ["ns"], ["pod"])  # pods answers late
    assert shown == []

    window._open_list_view("pods")  # back on Pods: the kept answer shows at once
    assert shown == [("pods", (["ns"], ["pod"]))]

    window._answered("prod", None, "pods", ["ns"], ["fresh"])  # the fresh one
    window._open_list_view("deployments")
    window._answered("prod", None, "deployments", ["ns"], ["dep"])
    assert shown[-1] == ("w", (["ns"], ["dep"]))
    window.close()


def test_a_failure_only_shows_for_the_list_the_person_is_on(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    errors = []
    monkeypatch.setattr(window, "_show_error", errors.append)
    window.context_combo.addItem("prod")
    FakeRefreshWorker.outcome = ("fail", "boom")

    window.refresh()  # the deployments list is on screen
    assert errors == ["boom"]

    window.refresh()
    worker = window._workers["deployments"]
    window._view = "pods"  # the person moved on before it failed
    worker.failed.emit("late")
    assert errors == ["boom", "boom"]
    FakeRefreshWorker.outcome = ("ok", ([], []))
    window.close()


def test_actions_run_in_workers_and_report_back(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    results, errors = [], []

    window._run_action(lambda: "ok", results.append)
    _wait_until(lambda: results and not window._action_workers)
    window._run_action(lambda: "quiet", results.append, quiet=True)
    _wait_until(lambda: len(results) == 2 and not window._action_workers)

    def broken():
        raise ClusterError("denied")

    window._run_action(broken, results.append, on_error=errors.append)
    _wait_until(lambda: errors and not window._action_workers)
    shown = []
    monkeypatch.setattr(window, "_show_action_error", shown.append)
    window._run_action(broken, results.append)
    _wait_until(lambda: shown and not window._action_workers)

    button = QPushButton()
    monkeypatch.setattr(window, "sender", lambda: button)
    window._run_action(lambda: "from button", results.append)
    _wait_until(lambda: len(results) == 3 and not window._action_workers)
    assert results == ["ok", "quiet", "from button"]
    assert errors == ["denied"] and shown == ["denied"]
    assert QApplication.overrideCursor() is None  # no busy cursor while loading
    window.close()


def test_actions_are_ignored_while_the_window_waits_to_close(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._close_when_worker_stops = True

    window._run_action(lambda: "x", lambda _r: None)

    assert window._action_workers == []
    closed = []
    monkeypatch.setattr(window, "close", lambda: closed.append("close"))
    monkeypatch.setattr(
        QApplication, "quit", staticmethod(lambda: closed.append("quit"))
    )
    window._finish_deferred_close()
    assert closed == ["close", "quit"]  # the app ends once the last worker is done


def test_closing_hides_the_window_and_stops_the_running_requests(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    cancelled = []
    monkeypatch.setattr(window_module, "cancel_running", lambda: cancelled.append(True))
    monkeypatch.setattr(
        QApplication, "quit", staticmethod(lambda: cancelled.append("quit"))
    )
    running = FakeRefreshWorker("prod", None)
    running.running = True
    window._workers = {"deployments": cast(window_module.RefreshWorker, running)}

    event = QCloseEvent()
    window.closeEvent(event)
    assert not event.isAccepted() and window._close_when_worker_stops
    assert not window.isVisible()  # closing feels instant
    assert cancelled == [True]
    assert QApplication.quitOnLastWindowClosed() is False

    window._workers = {}
    window._action_workers = [cast(window_module.ActionWorker, running)]
    window._finish_deferred_close()  # an action is still running: not yet
    assert "quit" not in cancelled
    window._action_workers = []
    window._finish_deferred_close()  # the last one is done
    assert cancelled[-1] == "quit"

    QApplication.setQuitOnLastWindowClosed(True)
    window._close_when_worker_stops = False
    event = QCloseEvent()
    window.closeEvent(event)
    assert event.isAccepted()


def test_no_error_box_while_the_window_is_closing(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    shown = []
    monkeypatch.setattr(QMessageBox, "exec", lambda box: shown.append(box.text()))

    window._close_when_worker_stops = True
    window._show_action_error("kubectl exited with -15")
    assert shown == []

    window._close_when_worker_stops = False
    window._show_action_error("kubectl exited with 1")
    assert shown
    window.close()


def test_actions_without_a_selection_do_nothing(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    dispatched = []
    monkeypatch.setattr(window, "_run_action", lambda *a, **_k: dispatched.append(a))

    window._view_workload_pods()
    window._view_details()
    window._view_logs()
    window._view_workload_details()
    window._view_workload_logs()

    assert dispatched == []
    window.close()


def test_pod_view_actions_use_the_selected_pod(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._view = "pods"
    monkeypatch.setattr(window, "_selected_pod", lambda: POD)
    dispatched, chosen = [], []
    monkeypatch.setattr(
        window, "_run_action", lambda op, _ok, *a, **_k: dispatched.append((op, a))
    )
    monkeypatch.setattr(
        window, "_choose_container_for_logs", lambda *a: chosen.append(a)
    )

    window._view_details()
    window._view_logs()

    assert dispatched[0][0].__name__ == "get_resource_details"
    assert dispatched[0][1] == ("prod", "Pod", "ns", "api-1")
    assert chosen == [("prod", POD)]
    window.close()


def test_workload_details_and_logs_dispatch_for_the_selection(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    workload = Workload("ns", "Deployment", "api", 1, 1, "1d")
    monkeypatch.setattr(window, "_selected_workload", lambda: workload)
    dispatched = []
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda op, ok, *a, **_k: dispatched.append((op.__name__, ok, a)),
    )
    shown = []
    monkeypatch.setattr(window, "_show_json_dialog", lambda *a: shown.append(a))
    monkeypatch.setattr(window, "_choose_pod_for_logs", lambda *a: shown.append(a))

    window._view_workload_details()
    window._view_workload_logs()
    window._view_workload_pods()
    monkeypatch.setattr(window, "_show_pods_dialog", lambda *a: shown.append(a))
    for _name, callback, _args in dispatched:
        callback([POD])

    assert [name for name, _cb, _a in dispatched] == [
        "get_resource_details",
        "get_workload_pods",
        "get_workload_pods",
    ]
    assert len(shown) == 3
    window.close()


def test_pods_dialog_lists_pods_and_opens_details_and_logs(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    workload = Workload("ns", "Deployment", "api", 1, 1, "1d")
    dispatched, chosen = [], []
    monkeypatch.setattr(
        window, "_run_action", lambda op, _ok, *a, **_k: dispatched.append((op, a))
    )
    monkeypatch.setattr(
        window, "_choose_container_for_logs", lambda *a: chosen.append(a)
    )
    seen = {}

    def fake_exec(dialog) -> int:
        table = dialog.findChild(QTableWidget, "podsTable")
        details = dialog.findChild(QPushButton, "detailsButton")
        logs = dialog.findChild(QPushButton, "logsButton")
        seen["rows"] = table.rowCount()
        details.clicked.emit()  # nothing selected yet
        logs.clicked.emit()
        table.selectRow(0)
        seen["enabled"] = details.isEnabled() and logs.isEnabled()
        details.clicked.emit()
        logs.clicked.emit()
        table.cellDoubleClicked.emit(0, 0)
        dialog.findChild(QPushButton, "closeButton").click()
        return 0

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    window._show_pods_dialog(workload, [POD])

    assert seen == {"rows": 1, "enabled": True}
    assert len(dispatched) == 2 and chosen == [("prod", POD)]

    seen.clear()
    window._show_pods_dialog(workload, [])
    assert seen["rows"] == 0
    window.close()


def test_choosing_pods_and_containers_for_logs(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    messages, dispatched = [], []
    monkeypatch.setattr(QMessageBox, "exec", lambda box: messages.append(box.text()))
    monkeypatch.setattr(
        window, "_run_action", lambda op, _ok, *a, **_k: dispatched.append(a)
    )
    other = PodInfo("ns", "api-2", "Running", 1, 1, "1h", ("app",))
    empty = PodInfo("ns", "bare", "Running", 0, 0, "1h", ())
    answers = iter([("api-2", True), ("api-1", False), ("sidecar", True)])
    monkeypatch.setattr(window, "_pick_item", lambda *_a: next(answers))

    window._choose_pod_for_logs("prod", [])
    window._choose_pod_for_logs("prod", [POD, other])  # picks api-2
    window._choose_pod_for_logs("prod", [POD, other])  # cancelled
    window._choose_container_for_logs("prod", empty)
    window._choose_container_for_logs("prod", POD)  # picks sidecar

    assert len(messages) == 2
    assert dispatched == [
        ("prod", "ns", "api-2", "app"),
        ("prod", "ns", "api-1", "sidecar"),
    ]
    window.close()


def test_init_containers_can_be_chosen_for_logs(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    dispatched, offered = [], []
    monkeypatch.setattr(
        window, "_run_action", lambda op, _ok, *a, **_k: dispatched.append(a)
    )

    def pick(_title, _label, items):
        offered.append(items)
        return "migrate", True

    monkeypatch.setattr(window, "_pick_item", pick)
    pod = PodInfo(
        "ns", "api", "Running", 1, 1, "1h", ("app",), init_containers=("migrate",)
    )

    window._choose_container_for_logs("prod", pod)

    assert offered == [["migrate", "app"]]
    assert dispatched == [("prod", "ns", "api", "migrate")]
    window.close()


def test_item_picker_is_a_filter_styled_select(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    seen = {}

    def fake_exec(dialog):
        combo = dialog.findChild(QComboBox)
        seen["variant"] = combo.property("variant")
        seen["items"] = [combo.itemText(i) for i in range(combo.count())]
        combo.setCurrentIndex(1)
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(QDialog, "exec", fake_exec)

    assert window._pick_item("Logs", "Pick:", ["app", "sidecar"]) == ("sidecar", True)
    assert seen == {"variant": "filter", "items": ["app", "sidecar"]}

    monkeypatch.setattr(QDialog, "exec", lambda _dialog: QDialog.DialogCode.Rejected)
    assert window._pick_item("Logs", "Pick:", ["app"])[1] is False
    window.close()


def test_errors_are_shown_in_a_message_box_and_in_the_status(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    executed = []
    monkeypatch.setattr(QMessageBox, "exec", lambda box: executed.append(box.text()))

    window._show_action_error("Unable to connect to the server")
    window._show_error("Unable to connect to the server")
    window._show_overview_error("Unable to connect to the server")

    assert executed and window.table.rowCount() == 0
    assert "Unable to connect" in window.overview_ui.noticeLabel.toolTip()
    window.close()


def test_overview_for_another_context_is_refetched(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    calls = []
    monkeypatch.setattr(window, "refresh_overview", lambda: calls.append(True))

    window._show_overview("other", ClusterOverview())

    assert calls == [True] and window._overview_context is None
    window.close()


def test_a_kubeconfig_error_disables_the_controls(monkeypatch) -> None:
    def broken():
        raise ClusterError("Unable to read kubeconfig")

    monkeypatch.setattr(window_module, "list_contexts", broken)
    window = window_module.WorkloadWindow()
    _wait_until(lambda: not window._action_workers)

    assert not window.context_combo.isEnabled()
    assert not window.refresh_button.isEnabled()
    assert "kubeconfig" in window.status_label.text()
    window.close()


def test_header_menu_toggles_columns_and_keeps_the_name(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            actions = self.actions()  # no namespace and no kind: never shown
            assert actions[0].text() == "NAME" and actions[0].isEnabled() is False
            actions[1].toggle()
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)

    window._show_column_menu(QPoint(0, 0))

    assert window.table.isColumnHidden(3)
    window.close()


def test_row_menu_selects_the_row_and_offers_the_actions(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    window._show_workloads(
        ["ns"],
        [
            Workload("ns", "Deployment", "api", 1, 1, "1d"),
            Workload("ns", "Deployment", "web", 1, 1, "1d"),
        ],
    )
    seen = []

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            seen.append([action.text() for action in self.actions()])
            self.actions()[1].trigger()  # Details
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)
    clicked = []
    monkeypatch.setattr(window, "_view_details", lambda: clicked.append(True))
    window.details_button.clicked.disconnect()
    window.details_button.clicked.connect(window._view_details)

    second = window.table.rowViewportPosition(1) + 2
    window._show_row_menu(QPoint(5, second))  # on the second row

    assert window.table.currentRow() == 1
    assert seen == [["Pods", "Details", "Logs"]] and clicked

    window._show_row_menu(QPoint(5, 5000))  # below the rows: no menu
    assert len(seen) == 1
    window._open_list_view("pods")
    window._show_pods(["ns"], [PodInfo("ns", "p", "Running", 1, 1, "1d", ("c",))])
    window._show_row_menu(QPoint(5, 20))
    assert seen[-1] == ["Details", "Logs"]  # a Pod has no Pods of its own
    window.close()


def test_settings_save_failures_are_logged_not_raised(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    def broken():
        raise OSError("disk full")

    monkeypatch.setattr(window.settings, "save", broken)
    window._save_settings()
    window._load_settings_form()  # no contexts: shows the hint
    assert "No contexts" in window.settings_ui.contextsHint.text()
    window.close()


def test_log_tab_shows_refresh_errors_unless_it_was_closed(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._show_logs_dialog(POD, "app", "line 1")
    tab = tab_at(window.viewer_tabs, 0, LogTab)
    calls = []
    monkeypatch.setattr(
        window, "_run_action", lambda op, ok, *a, **k: calls.append(k["on_error"])
    )

    window._refresh_log(tab, force=True)
    calls[0]("Unable to connect to the server")
    assert not tab.busy
    assert "Unable to connect" in tab.ui.logStatus.text()

    tab.busy = True
    tab.closed = True
    calls[0]("late failure")  # must not touch a closed tab
    assert not tab.busy
    assert "late failure" not in tab.ui.logStatus.text()
    window.close()


def test_overview_without_pod_or_metrics_data_shows_dashes(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    window._render_overview(ClusterOverview())
    assert window.overview_ui.podsValue.text() == "—"
    assert window.overview_ui.podsCaption.text() == ""

    node = NodeInfo(
        name="n",
        ready=True,
        roles="worker",
        version="v1",
        age="1d",
        cpu_allocatable=4.0,
        memory_allocatable=8 * 2**30,
        pods_allocatable=10,
        pods_running=1,
        cpu_requests=1.0,
        memory_requests=2**30,
        cpu_usage=0.5,
        memory_usage=2**30,
    )
    window._render_overview(ClusterOverview(nodes=(node,), metrics_available=True))
    assert "usage" in window.overview_ui.cpuCaption.text()
    assert "usage" in window.overview_ui.memCaption.text()
    window.close()


def _login_window(monkeypatch):
    window = _ready_window(monkeypatch)
    ran = []
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda op, ok, *args, **kw: ran.append((op.__name__, ok, args, kw)),
    )
    return window, ran


def test_contexts_load_in_the_background(monkeypatch) -> None:
    release = []
    started = []

    def slow_contexts():
        started.append(True)
        _wait_until(lambda: release, seconds=3.0)
        return ["a", "b"], "b"

    monkeypatch.setattr(window_module, "list_contexts", slow_contexts)
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(
        window_module.WorkloadWindow, "refresh_overview", lambda *_a: None
    )
    monkeypatch.setattr(window_module.WorkloadWindow, "_check_login", lambda *_a: None)

    window = window_module.WorkloadWindow()  # returns while kubectl is still busy

    assert "Loading contexts" in window.status_label.text()
    assert window.context_combo.count() == 0
    assert not window.refresh_button.isEnabled()
    release.append(True)
    _wait_until(lambda: window.context_combo.count() == 2)
    assert window._context() == "b"
    window.close()


def test_no_contexts_in_the_kubeconfig_is_reported(monkeypatch) -> None:
    window = _ready_window(monkeypatch)  # list_contexts returns nothing

    assert "No contexts found" in window.status_label.text()
    assert not window.refresh_button.isEnabled()
    assert not window.no_contexts_banner.isHidden()
    assert "No cluster contexts" in window.ui.noContextsLabel.text()
    window.close()


SSO = LoginAction(["aws", "sso", "login", "--profile", "work"], "work", False)
KEYS = LoginAction(["aws", "configure", "--profile", "work"], "work", True)


def test_login_check_runs_once_per_context_and_shows_the_profile(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)

    window._check_login()
    window._check_login()  # one check at a time
    assert [(name, args) for name, _ok, args, _kw in ran] == [
        ("check_login", ("prod",))
    ]
    assert ran[0][3]["quiet"] is True

    ran[0][1]((True, SSO))
    assert not window.login_button.isHidden()
    assert window.login_button.text() == "Sign in to AWS (work)"
    assert "Not signed in to AWS (profile work)" in window.status_label.text()
    assert window._login_checking is False
    window.close()


def test_access_key_profiles_offer_to_configure_the_credentials(monkeypatch) -> None:
    window, _ran = _login_window(monkeypatch)

    window._show_login("prod", (True, KEYS))
    assert window.login_button.text() == "Configure AWS credentials (work)"
    assert "work are missing or invalid" in window.status_label.text()

    default = LoginAction(["aws", "configure"], None, True)
    window._show_login("prod", (True, default))
    assert "(default)" in window.login_button.text()
    window.close()


def test_google_cloud_and_azure_contexts_offer_to_sign_in(monkeypatch) -> None:
    window, _ran = _login_window(monkeypatch)

    google = LoginAction(["gcloud", "auth", "login"], None, False, "Google Cloud")
    window._show_login("prod", (True, google))
    assert window.login_button.text() == "Sign in to Google Cloud"
    assert "Not signed in to Google Cloud" in window.status_label.text()

    azure = LoginAction(["az", "login"], None, False, "Azure")
    window._show_login("prod", (True, azure))
    assert window.login_button.text() == "Sign in to Azure"

    named = LoginAction(["az", "login"], "my-subscription", False, "Azure")
    window._show_login("prod", (True, named))
    assert window.login_button.text() == "Sign in to Azure (my-subscription)"
    window.close()


def test_login_check_failures_and_other_results_hide_the_button(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window.login_button.setVisible(True)

    window._show_login("prod", (False, None))
    assert window.login_button.isHidden()

    window._show_login("other", (True, SSO))  # a stale answer is ignored
    assert window._login_action is None

    window._show_login("prod", (True, None))  # not an AWS context: no button
    assert window.login_button.isHidden()

    window._check_login()
    ran[0][3]["on_error"](Exception("boom"))
    assert window._login_checking is False

    window.context_combo.clear()
    window._check_login()  # no context: nothing to check
    assert len(ran) == 1
    window.close()


def test_context_change_and_refresh_recheck_the_login(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window._login_action = SSO
    window.login_button.setVisible(True)

    window._context_changed()

    assert window._login_action is None
    assert window.login_button.isHidden()
    assert ran[0][0] == "check_login"
    ran[0][3]["on_error"](None)
    window.refresh_button.clicked.emit()
    assert [name for name, *_rest in ran].count("check_login") == 2
    window.close()


def test_sso_sign_in_runs_the_command_and_reloads_the_data(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window._sign_in()  # nothing to run without an action
    assert ran == []

    window._login_action = SSO
    window._sign_in()
    name, done, args, kwargs = ran[0]
    assert (name, args) == ("run_login", (SSO,))
    assert kwargs["on_error"] == window._show_action_error

    refreshed = []
    monkeypatch.setattr(window, "refresh", lambda: refreshed.append("list"))
    monkeypatch.setattr(
        window, "refresh_overview", lambda: refreshed.append("overview")
    )
    window._overview_context = "prod"
    done(None)
    assert refreshed == ["list", "overview"]
    assert window._login_action is None
    window.close()


def test_access_key_sign_in_waits_for_the_terminal(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window._login_action = KEYS
    window.login_button.setVisible(True)
    refreshed = []
    monkeypatch.setattr(window, "refresh", lambda: refreshed.append("list"))

    window._sign_in()
    ran[0][1](None)

    assert refreshed == [] and window._login_action == KEYS
    assert "terminal that opened" in window.status_label.text()
    window.close()


def test_authentication_errors_trigger_a_login_check(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)

    window._show_error("Unable to connect: i/o timeout")
    window._show_overview_error("Unable to connect: i/o timeout")
    assert ran == []

    window._show_error("error: You must be logged in to the server (Unauthorized)")
    window._login_checking = False
    window._show_overview_error("the SSO session has expired")
    assert [name for name, *_rest in ran] == ["check_login", "check_login"]
    window.close()


def test_actions_never_run_on_the_main_thread(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    threads = []
    results = []

    def operation():
        threads.append(threading.current_thread())
        return "done"

    window._run_action(operation, results.append)

    assert QApplication.overrideCursor() is None
    _wait_until(lambda: results and not window._action_workers)
    assert threads[0] is not threading.main_thread()
    window.close()


def test_expected_cluster_errors_are_not_logged_as_errors(monkeypatch, caplog) -> None:
    def expired(*_args):
        raise ClusterError("Error loading SSO Token: Token does not exist")

    monkeypatch.setattr(window_module, "get_pods", expired)
    monkeypatch.setattr(window_module, "get_workloads", lambda *_a: (["a"], []))
    monkeypatch.setattr(window_module, "get_usage", expired)
    failures = []

    with caplog.at_level("INFO"):
        pods = window_module.RefreshWorker("ctx", None, "pods")
        pods.failed.connect(failures.append)
        pods.run()
        window_module.RefreshWorker("ctx", None).run()  # usage is optional
        action = window_module.ActionWorker(expired, ())
        action.failed.connect(failures.append)
        action.run()

    assert len(failures) == 2 and "SSO Token" in failures[0]
    assert caplog.records == []


def test_unexpected_failures_are_still_logged_with_a_traceback(
    monkeypatch, caplog
) -> None:
    def broken(*_args):
        raise RuntimeError("a bug")

    monkeypatch.setattr(window_module, "get_pods", broken)
    monkeypatch.setattr(window_module, "get_workloads", lambda *_a: (["a"], []))
    monkeypatch.setattr(window_module, "get_usage", broken)

    with caplog.at_level("INFO"):
        window_module.RefreshWorker("ctx", None, "pods").run()
        window_module.RefreshWorker("ctx", None).run()
        window_module.ActionWorker(broken, ()).run()

    assert len(caplog.records) == 3
    assert all(record.exc_info for record in caplog.records)


def test_debug_mode_is_switched_from_the_settings_page(monkeypatch, tmp_path) -> None:
    window = _ready_window(monkeypatch)
    configured = []
    monkeypatch.setattr(
        window_module, "configure_logging", lambda **kwargs: configured.append(kwargs)
    )
    form = window.settings_ui

    window._load_settings_form()
    assert form.debugCheck.isChecked() is False
    assert "never Pod logs" in form.debugHint.text()
    assert str(window_module.log_file()) in form.debugHint.text()

    form.debugCheck.setChecked(True)
    window._save_preferences()
    assert window.settings.debug_logging is True
    assert configured == [{"to_file": True}]

    window._save_preferences()  # unchanged: the log is not reconfigured
    assert len(configured) == 1

    form.debugCheck.setChecked(False)
    window._save_preferences()
    assert configured[-1] == {"to_file": False}
    window.close()


def test_the_log_folder_opens_in_the_file_manager(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    opened = []
    monkeypatch.setattr(
        window_module.QDesktopServices,
        "openUrl",
        staticmethod(lambda url: opened.append(url.toLocalFile())),
    )

    window.settings_ui.openLogsButton.click()

    folder = window_module.log_directory()
    assert opened == [str(folder)] and folder.is_dir()
    window.close()


def test_the_app_logs_what_it_does(monkeypatch, caplog) -> None:
    caplog.set_level("DEBUG", logger="kubescope")
    window = _ready_window(monkeypatch)
    FakeRefreshWorker.outcome = (
        "ok",
        (["ns"], [Workload("ns", "Deployment", "api", 1, 1, "1d")]),
    )
    window.refresh()
    FakeRefreshWorker.outcome = ("error", "Unable to connect\nsecond line")
    window.refresh()
    window._open_list_view("pods")
    FakeRefreshWorker.outcome = ("ok", ([], []))

    messages = [record.getMessage() for record in caplog.records]
    assert any("Loaded 0 context(s)" in m for m in messages)
    assert any("Refreshing deployments in prod (namespace all)" in m for m in messages)
    assert any("Loaded 1 workload(s) in 1 namespace(s)" in m for m in messages)
    assert any(m == "Refresh failed: Unable to connect" for m in messages)
    assert any("Opening the pods list" in m for m in messages)
    assert any(m.startswith("Action: ") for m in messages)
    window.close()


def _header(window, column: int) -> str:
    return window.table.horizontalHeaderItem(column).text()


def test_every_workload_list_has_its_menu_entry_title_and_columns(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    expected = {
        "navStatefulSets": ("StatefulSets", "READY", "statefulsets"),
        "navJobs": ("Jobs", "COMPLETIONS", "jobs"),
        "navCronJobs": ("CronJobs", "SCHEDULE", "cronjobs"),
        "navDeployments": ("Deployments", "READY", "deployments"),
    }
    for name, (title, ready_header, view) in expected.items():
        getattr(window.ui, name).click()
        assert window._view == view
        assert window.ui.pageTitle.text() == title
        assert _header(window, 3) == ready_header
        assert window.pods_button.isVisibleTo(window)  # their Pods can be listed
        assert getattr(window.ui, name).isChecked()

    window.nav_pods.click()
    assert not window.pods_button.isVisibleTo(window)
    window.close()


def test_switching_between_workload_kinds_clears_the_old_rows(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._workloads = [Workload("ns", "Deployment", "api", 1, 1, "1d")]

    window._open_list_view("jobs")

    assert window._workloads == []
    window.close()


def test_jobs_and_cron_jobs_render_their_own_states(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._open_list_view("jobs")
    window._show_workloads(
        ["ops"],
        [
            Workload("ops", "Job", "backup", 3, 3, "1d", state="Complete"),
            Workload("ops", "Job", "sync", 0, 1, "5m", state="Failed"),
            Workload("ops", "Job", "load", 0, 1, "1m", state="Running"),
            Workload("ops", "Job", "wait", 0, 1, "1m", state="Pending"),
        ],
    )
    table = window.table
    assert [cell(table, row, 4).text() for row in range(4)] == [
        "Complete",
        "Failed",
        "Running",
        "Pending",
    ]
    assert cell(table, 0, 3).text() == "3/3"
    assert "4 Jobs in 1 namespaces" in window.status_label.text()
    assert window.summary_label.text() == "4 of 4 Jobs"

    window._open_list_view("cronjobs")
    window._show_workloads(
        ["ops"],
        [
            Workload(
                "ops",
                "CronJob",
                "nightly",
                0,
                0,
                "9d",
                state="Scheduled",
                schedule="0 3 * * *",
            ),
            Workload(
                "ops",
                "CronJob",
                "paused",
                0,
                0,
                "9d",
                state="Suspended",
                schedule="@daily",
            ),
            Workload(
                "ops",
                "CronJob",
                "busy",
                1,
                0,
                "9d",
                state="Active",
                schedule="* * * * *",
            ),
        ],
    )
    assert [cell(table, row, 3).text() for row in range(3)] == [
        "0 3 * * *",
        "@daily",
        "* * * * *",
    ]
    assert [cell(table, row, 4).text() for row in range(3)] == [
        "Scheduled",
        "Suspended",
        "Active",
    ]
    assert "3 CronJobs in 1 namespaces" in window.status_label.text()
    assert window.summary_label.text() == "3 of 3 CronJobs"

    window._open_list_view("statefulsets")
    window._show_workloads(["ops"], [Workload("ops", "StatefulSet", "db", 1, 1, "2d")])
    assert "1 StatefulSets in 1 namespaces" in window.status_label.text()
    assert window.summary_label.text() == "1 of 1 StatefulSets"
    window.close()


def test_daemon_set_replica_set_and_controller_lists_open(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    for view, kind, title in (
        ("daemonsets", "DaemonSet", "DaemonSets"),
        ("replicasets", "ReplicaSet", "ReplicaSets"),
        ("replicationcontrollers", "ReplicationController", "ReplicationControllers"),
    ):
        window._open_list_view(view)
        window._show_workloads(["ops"], [Workload("ops", kind, "x", 1, 2, "2d")])

        assert window.ui.pageTitle.text() == title
        assert f"1 {title} in 1 namespaces" in window.status_label.text()
        assert window.summary_label.text() == f"1 of 1 {title}"
        assert cell(window.table, 0, 1).text() == kind
        assert cell(window.table, 0, 4).text() == "Degraded"
    window.close()


def test_cron_job_lists_skip_the_pod_usage_lookup(monkeypatch) -> None:
    cron = Workload("ops", "CronJob", "nightly", 0, 0, "1d", state="Scheduled")
    monkeypatch.setattr(window_module, "get_workloads", lambda *_a: (["ops"], [cron]))

    def forbidden(*_args):
        raise AssertionError("a CronJob has no Pods of its own to measure")

    monkeypatch.setattr(window_module, "get_usage", forbidden)
    done = []
    worker = window_module.RefreshWorker("ctx", None, "cronjobs")
    worker.completed.connect(lambda _n, items: done.append(items))

    worker.run()

    assert done[0][0].name == "nightly" and done[0][0].cpu is None


def _workloads_overview(**changes) -> WorkloadsOverview:
    kinds = {
        "Pod": KindSummary(18, 17, 1, 0),
        "Deployment": KindSummary(17, 15, 2, 0),
        "DaemonSet": KindSummary(0),
        "StatefulSet": KindSummary(1, 1, 0, 0),
        "ReplicaSet": KindSummary(161, 17, 0, 1),
        "Job": KindSummary(4, 3, 0, 1),
        "CronJob": KindSummary(0),
    }
    events = (
        EventInfo("Warning", "kubelet", "ns", "Pod: api-1", "Back-off", 12, "2h", "5m"),
        EventInfo("Normal", "ctl", "ns", "Deployment: web", "Scaled up", 1, "1d", "1d"),
    )
    return WorkloadsOverview(**{"kinds": kinds, "events": events, **changes})


def test_workloads_overview_is_the_first_entry_of_the_workloads_menu(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    layout = window.ui.workloadsSubmenuLayout

    assert layout.indexOf(window.nav_workloads_overview) == 0
    assert window.nav_workloads_overview.text() == "Overview"
    window.close()


def test_menu_entries_are_in_alphabetical_order(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    ui = window.ui
    for layout, skipped in (
        (ui.workloadsSubmenuLayout, 1),  # the Overview stays first
        (ui.networkSubmenuLayout, 0),
        (ui.configSubmenuLayout, 0),
    ):
        names = [
            text_at(layout, index).casefold()
            for index in range(skipped, layout.count())
        ]
        assert names == sorted(names)
    window.close()


def test_opening_the_workloads_overview_loads_it_once_per_context(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)

    window.nav_workloads_overview.click()

    assert window.pages.currentIndex() == 4
    assert window.ui.pageTitle.text() == "Workloads overview"
    assert window.nav_workloads_overview.isChecked()
    assert [(name, args) for name, _ok, args, _kw in ran] == [
        ("get_workloads_overview", ("prod",))
    ]
    assert "Loading workloads" in window.workloads_ui.noticeLabel.text()

    window.refresh_workloads_overview()  # one request at a time
    assert len(ran) == 1

    ran[0][1](_workloads_overview())
    window.nav_workloads_overview.click()  # loaded for this context: no reload
    assert len(ran) == 1
    window.close()


def test_the_overview_shows_counts_bars_and_events(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window.nav_workloads_overview.click()

    ran[0][1](_workloads_overview())

    page = window.workloads_ui
    assert page.podsLink.text() == "Pods (18)"
    assert page.replicasetsLink.text() == "ReplicaSets (161)"
    assert page.daemonsetsLink.text() == "DaemonSets (0)"
    assert page.noticeLabel.text() == ""
    table = window.workloads_table
    assert table.rowCount() == 2
    assert [cell(table, 0, c).text() for c in range(8)] == [
        "Warning",
        "kubelet",
        "ns",
        "Pod: api-1",
        "Back-off",
        "12",
        "2h",
        "5m",
    ]
    assert cell(table, 0, 4).toolTip() == "Back-off"
    window.close()


def test_unreadable_sections_are_named_and_shown_as_dashes(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window.nav_workloads_overview.click()
    kinds = _workloads_overview().kinds
    del kinds["ReplicaSet"]

    ran[0][1](_workloads_overview(kinds=kinds, unreadable=("ReplicaSet", "Event")))

    page = window.workloads_ui
    assert page.replicasetsLink.text() == "ReplicaSets (—)"
    assert page.noticeLabel.text() == "Could not read: ReplicaSet, Event"
    window.close()


def test_the_overview_links_open_the_lists_that_exist(monkeypatch) -> None:
    window, _ran = _login_window(monkeypatch)
    page = window.workloads_ui
    monkeypatch.setattr(window, "refresh", lambda: None)

    for link, view in (
        (page.podsLink, "pods"),
        (page.deploymentsLink, "deployments"),
        (page.statefulsetsLink, "statefulsets"),
        (page.daemonsetsLink, "daemonsets"),
        (page.replicasetsLink, "replicasets"),
        (page.jobsLink, "jobs"),
        (page.cronjobsLink, "cronjobs"),
    ):
        assert link.isEnabled()
        link.click()
        assert window._view == view and window.pages.currentIndex() == 1
    window.close()


def test_overview_answers_for_another_context_are_requested_again(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window.nav_workloads_overview.click()

    window._show_workloads_overview("other", _workloads_overview())

    assert [name for name, *_rest in ran] == ["get_workloads_overview"] * 2
    assert window._workloads_overview_context is None
    window.close()


def test_a_context_change_reloads_the_overview_when_it_is_showing(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window.nav_workloads_overview.click()
    ran[0][1](_workloads_overview())
    assert len(ran) == 1

    window._context_changed()

    assert [name for name, *_rest in ran].count("get_workloads_overview") == 2
    window.close()


def test_overview_errors_are_explained_and_authentication_is_rechecked(
    monkeypatch,
) -> None:
    window, ran = _login_window(monkeypatch)
    window.nav_workloads_overview.click()

    ran[0][3]["on_error"]("Unable to connect: i/o timeout")
    assert "Cluster unreachable" in window.workloads_ui.noticeLabel.text()
    assert not window._workloads_overview_busy
    assert [name for name, *_rest in ran] == ["get_workloads_overview"]

    window.refresh_workloads_overview()
    window._workloads_overview_busy = True
    window._show_workloads_overview_error("You must be logged in (Unauthorized)")
    assert [name for name, *_rest in ran][-1] == "check_login"
    window.close()


def test_the_overview_follows_a_language_change(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window.nav_workloads_overview.click()
    ran[0][1](_workloads_overview())

    window._retranslate()

    assert window.workloads_ui.podsLink.text() == "Pods (18)"  # counts survive
    assert window.workloads_table.rowCount() == 2
    window.close()


def test_the_theme_is_chosen_in_settings_and_applied_at_once(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.settings.theme = "light"
    window._open_list_view("pods")
    window._show_pods(["ns"], [POD])
    window._overview = ClusterOverview()
    window._workloads_overview = _workloads_overview()
    form = window.settings_ui

    window._load_settings_form()
    assert [form.themeCombo.itemData(i) for i in range(2)] == ["light", "dark"]
    assert form.themeCombo.currentData() == "light"
    light_style = window.styleSheet()
    assert "#f7f7fa" in light_style and "#11141a" not in light_style
    light_icon = window_module._chevron_icon_path()

    form.themeCombo.setCurrentIndex(form.themeCombo.findData("dark"))
    window._save_preferences()

    assert window.settings.theme == "dark"
    assert "#11141a" in window.styleSheet() and "#f7f7fa" not in window.styleSheet()
    assert cell(window.table, 0, 4).foreground().color().name() == themed("#176b58")
    assert "dark" in window_module._chevron_icon_path() != light_icon
    assert QApplication.palette().color(QPalette.ColorRole.Window).name() == "#11141a"

    window._save_preferences()  # unchanged: nothing is restyled again
    form.themeCombo.setCurrentIndex(form.themeCombo.findData("light"))
    window._save_preferences()
    assert window.styleSheet() == light_style
    window.close()


def test_the_window_starts_in_the_saved_theme(monkeypatch, tmp_path) -> None:
    from kubescope.settings import Settings
    from kubescope.theme import apply_theme

    settings = Settings(tmp_path / "settings.json")
    settings.theme = "dark"
    apply_theme(get_application(), settings.theme)

    window = _ready_window(monkeypatch)

    assert "#11141a" in window.styleSheet()
    window.close()
    apply_theme(get_application(), "light")


def _accept_editor(monkeypatch, *, name=None, page=None, result=None):
    """Answer the theme editor as a person would, without showing it."""
    from kubescope.dialogs.theme_editor import ThemeEditor

    seen = []

    def fake_exec(dialog) -> int:
        seen.append(dialog)
        if isinstance(dialog, ThemeEditor):
            if name is not None:
                dialog.name_edit.setText(name)
            if page is not None:
                dialog._tokens["page"] = page
        return QDialog.DialogCode.Accepted if result is None else result

    monkeypatch.setattr(QDialog, "exec", fake_exec)
    return seen


def test_a_new_theme_is_made_in_the_editor_and_then_chosen(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.settings.theme = "light"
    page = window.settings_ui
    window._load_settings_form()
    assert [page.themeCombo.itemData(i) for i in range(page.themeCombo.count())] == [
        "light",
        "dark",
    ]
    assert not page.editThemeButton.isEnabled()  # built-in themes are fixed
    seen = _accept_editor(monkeypatch, name="Ocean", page="#001122")

    page.newThemeButton.click()

    assert seen[0].values()[0] == "Ocean"
    assert page.themeCombo.currentData() == "ocean"
    assert page.themeCombo.currentText() == "Ocean"
    assert page.editThemeButton.isEnabled()
    assert window.settings.theme == "light"  # chosen, but not applied until saved

    page.saveButton.click()
    assert window.settings.theme == "ocean"
    assert "#001122" in window.styleSheet()
    window.close()


def test_cancelling_the_editor_creates_nothing(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    _accept_editor(monkeypatch, name="Nope", result=QDialog.DialogCode.Rejected)

    window.settings_ui.newThemeButton.click()
    window.settings_ui.editThemeButton.setEnabled(True)
    window._edit_theme()  # also cancelled: the built-in Light is not changed

    assert window.settings_ui.themeCombo.count() == 2
    assert not list(window_module.themes_directory().glob("*.json"))
    window.close()


def test_editing_the_theme_in_use_restyles_the_window_at_once(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    _accept_editor(monkeypatch, name="Ocean", page="#001122")
    window.settings_ui.newThemeButton.click()
    window.settings_ui.saveButton.click()
    assert "#001122" in window.styleSheet()

    _accept_editor(monkeypatch, page="#334455")
    window._edit_theme()

    assert "#334455" in window.styleSheet() and "#001122" not in window.styleSheet()
    assert window.settings_ui.themeCombo.currentData() == "ocean"

    # editing one that is not in use leaves the look alone
    window.settings_ui.themeCombo.setCurrentIndex(0)
    window.settings.theme = "light"
    window._apply_theme()
    _accept_editor(monkeypatch, name="Other", page="#778899")
    window.settings_ui.newThemeButton.click()
    window.settings_ui.themeCombo.setCurrentIndex(
        window.settings_ui.themeCombo.findData("ocean")
    )
    _accept_editor(monkeypatch, page="#556677")
    window._edit_theme()
    assert "#556677" not in window.styleSheet()
    window.close()


def test_a_theme_that_was_deleted_falls_back_to_the_default(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.settings.theme = "gone"

    window._load_settings_form()

    assert window.settings_ui.themeCombo.currentData() == "dark"
    window._apply_theme()
    assert "#11141a" in window.styleSheet()
    window.close()


def test_the_themes_folder_opens_in_the_file_manager(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    opened = []
    monkeypatch.setattr(
        window_module.QDesktopServices,
        "openUrl",
        staticmethod(lambda url: opened.append(url.toLocalFile())),
    )

    window.settings_ui.openThemesButton.click()

    folder = window_module.themes_directory()
    assert opened == [str(folder)] and folder.is_dir()
    window.close()


def test_the_footer_shows_the_version_and_links_to_the_project(monkeypatch) -> None:
    import kubescope

    window = _ready_window(monkeypatch)
    opened = []
    monkeypatch.setattr(
        window_module.QDesktopServices,
        "openUrl",
        staticmethod(lambda url: opened.append(url.toString())),
    )

    assert window.ui.footerVersion.text() == f"Version {kubescope.__version__}"
    assert kubescope.PROJECT_URL in window.ui.githubLink.toolTip()

    window.ui.githubLink.click()
    assert opened == [kubescope.PROJECT_URL]

    window.ui.companyLink.click()
    assert opened[-1] == "https://dcotecnologia.com"

    window.ui.licenseLink.click()  # the real license, on GitHub
    assert opened[-1] == f"{kubescope.PROJECT_URL}/blob/main/LICENSE"

    window._retranslate()  # a language change rewrites the .ui texts
    assert window.ui.footerVersion.text() == f"Version {kubescope.__version__}"
    window.close()


def test_the_top_bar_shows_the_logo(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    assert not window.ui.topLogo.pixmap().isNull()
    window.close()


def test_clicking_through_the_lists_quickly_loads_only_the_last_one(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    started = []
    monkeypatch.setattr(window, "refresh", lambda *_a: started.append(window._view))
    window._list_timer.timeout.disconnect()
    window._list_timer.timeout.connect(window.refresh)

    window._open_list_view("pods")
    window._open_list_view("deployments")
    window._open_list_view("jobs")
    assert started == [] and "Loading" in window.status_label.text()
    _wait_until(lambda: started)

    assert started == ["jobs"]
    window.close()


def _resource_window(monkeypatch):
    window = _ready_window(monkeypatch)
    window.context_combo.addItem("prod")
    return window


def test_each_network_list_opens_with_its_own_columns(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    expected = {
        "services": ("Services", "Service", 4),
        "endpointslices": ("Endpoint Slices", "EndpointSlice", 3),
        "endpoints": ("Endpoints", "Endpoints", 1),
        "ingresses": ("Ingresses", "Ingress", 4),
        "ingressclasses": ("Ingress Classes", "IngressClass", 2),
        "networkpolicies": ("Network Policies", "NetworkPolicy", 2),
    }
    for view, (title, kind, extra) in expected.items():
        window._open_list_view(view)
        values = tuple(f"v{n}" for n in range(extra))
        window._show_resources(
            ["ops"],
            [
                ClusterResource(
                    "" if kind == "IngressClass" else "ops", kind, "x", values, "2d"
                )
            ],
        )

        assert window.ui.pageTitle.text() == title
        assert window.table.columnCount() == extra + 4  # namespace, kind, name, age
        assert cell(window.table, 0, 1).text() == kind
        assert cell(window.table, 0, 3).text() == "v0"
        assert cell(window.table, 0, extra + 3).text() == "2d"
        assert window.summary_label.text() == f"1 of 1 {title}"
        assert window.pods_button.isHidden() and window.logs_button.isHidden()
        assert not window.details_button.isHidden()
    assert cell(window.table, 0, 0).text() == "ops"
    window._open_list_view("ingressclasses")
    window._show_resources(
        ["ops"], [ClusterResource("", "IngressClass", "x", ("c", "p"), "1d")]
    )
    assert cell(window.table, 0, 0).text() == "—"  # cluster-wide: no namespace
    window.close()


def test_each_config_list_opens_with_its_own_columns(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    expected = {
        "configmaps": ("Config Maps", "ConfigMap", 1),
        "secrets": ("Secrets", "Secret", 2),
        "resourcequotas": ("Resource Quotas", "ResourceQuota", 1),
        "limitranges": ("Limit Ranges", "LimitRange", 1),
        "horizontalpodautoscalers": (
            "Horizontal Pod Autoscalers",
            "HorizontalPodAutoscaler",
            4,
        ),
        "poddisruptionbudgets": ("Pod Disruption Budgets", "PodDisruptionBudget", 3),
        "priorityclasses": ("Priority Classes", "PriorityClass", 2),
        "runtimeclasses": ("Runtime Classes", "RuntimeClass", 1),
        "leases": ("Leases", "Lease", 1),
        "mutatingwebhooks": (
            "Mutating Webhook Configurations",
            "MutatingWebhookConfiguration",
            1,
        ),
        "validatingwebhooks": (
            "Validating Webhook Configurations",
            "ValidatingWebhookConfiguration",
            1,
        ),
        "nodegroups": ("Node Groups", "NodeGroup", 5),
        "addons": ("Add-ons", "Addon", 3),
    }
    assert set(expected) == set(CONFIG_VIEWS)
    for view, (title, kind, extra) in expected.items():
        window._open_list_view(view)
        values = tuple(f"v{n}" for n in range(extra))
        window._show_resources(
            ["ops"], [ClusterResource("ops", kind, "x", values, "2d")]
        )

        assert window.ui.pageTitle.text() == title
        assert window.table.columnCount() == extra + 4  # namespace, kind, name, age
        assert cell(window.table, 0, 1).text() == kind
        assert cell(window.table, 0, 3).text() == "v0"
        assert window.summary_label.text() == f"1 of 1 {title}"
        assert window.pods_button.isHidden() and window.logs_button.isHidden()
        assert not window.details_button.isHidden()
        assert "1" in window.status_label.text()
    window.close()


def test_namespace_and_kind_columns_are_never_shown(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    window._fill_namespaces(["ops"])
    menu_columns = []

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            menu_columns.extend(action.text() for action in self.actions())
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)
    rows = {
        "nodegroups": ClusterResource("", "NodeGroup", "x", ("A", "v"), "1d"),
        "services": ClusterResource("ops", "Service", "x", ("a", "b", "c", "d"), "1d"),
    }
    for view, row in rows.items():
        window._open_list_view(view)
        window._show_resources([], [row])
        assert window.table.isColumnHidden(0) and window.table.isColumnHidden(1)
        assert not window.table.isColumnHidden(2)
        menu_columns.clear()
        window._show_column_menu(QPoint(0, 0))
        assert "NAMESPACE" not in menu_columns and "KIND" not in menu_columns
        assert "NAME" in menu_columns
    window._open_list_view("deployments")
    assert window.table.isColumnHidden(0) and window.table.isColumnHidden(1)
    window._open_list_view("pods")
    assert window.table.isColumnHidden(0) and window.table.isColumnHidden(1)
    window._fill_namespaces(["ops"])
    window._open_list_view("nodegroups")
    window._show_resources([], [rows["nodegroups"]])
    assert window.ui.filtersBar.isHidden() and window._namespaces == ["ops"]
    assert window.ui.filtersBar.isHidden()
    window.search_input.setText("zzz")  # stale text must not hide the rows
    window._filter_rows()
    assert not window.table.isRowHidden(0)
    window.search_input.setText("")
    window._open_list_view("services")
    assert not window.ui.filtersBar.isHidden()
    window.close()


def test_the_overview_shows_the_cluster_info_of_an_eks_context(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    ran = []
    monkeypatch.setattr(window, "_run_action", lambda *a, **k: ran.append((a, k)))
    info = ClusterInfo(
        "Active",
        "1.37",
        "eks.4",
        "2026-02-11 13:16",
        "EKS",
        "https://api",
        "<arn>",
        "r",
        "o",
        vpc_id="vpc-1",
        subnets=("subnet-a", "subnet-b"),
        endpoint_access="Public",
    )

    window._show_eks_entries("prod", True)
    (operation, on_success, context), options = ran[-1]
    assert operation.__name__ == "get_cluster_info" and context == "prod"
    on_success(info)

    card = window.overview_ui.clusterInfoCard
    grid = window.overview_ui.clusterInfoGrid
    assert not card.isHidden() and grid.count() == 9
    texts = [text_at(grid, i) for i in range(grid.count())]
    assert "Kubernetes version" in texts[1] and "1.37" in texts[1]
    assert "&lt;arn&gt;" in texts[6]  # values are escaped
    networking = window.overview_ui.networkingGrid
    cells = [text_at(networking, i) for i in range(networking.count())]
    assert not window.overview_ui.networkingCard.isHidden() and len(cells) == 8
    assert "vpc-1" in cells[0] and "None" in cells[2] and "Public" in cells[3]
    assert "subnet-a<br>subnet-b" in cells[7]  # one subnet per line

    window._show_cluster_info("other", None)  # a stale answer is ignored
    assert not card.isHidden()
    window._retranslate()  # a language change redraws the labels
    assert grid.count() == 9

    options["on_error"]("denied")  # not readable: the card goes away
    assert card.isHidden() and grid.count() == 0
    assert window.overview_ui.networkingCard.isHidden()
    on_success(info)
    window._show_eks_entries("prod", False)  # not EKS (any more)
    assert card.isHidden()
    window.close()


def test_the_node_groups_entry_follows_the_context(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    ran = []
    monkeypatch.setattr(window, "_run_action", lambda *a, **k: ran.append((a, k)))
    window.show()
    window._update_eks_entries()
    (operation, on_success, context), options = ran[0]
    assert operation.__name__ == "is_eks_context" and context == "prod"
    assert window.ui.navNodeGroups.isHidden()

    on_success(True)
    assert not window.ui.navNodeGroups.isHidden()
    window._show_eks_entries("other", False)  # a stale answer is ignored
    assert not window.ui.navNodeGroups.isHidden()

    window._open_list_view("nodegroups")
    window._context_changed()  # until the new context answers, nothing from AWS
    assert window.ui.navNodeGroups.isHidden()
    assert not window.ui.navAddons.isHidden()  # Helm releases need no AWS
    assert (
        window.overview_ui.clusterInfoCard.isHidden() and window._view == "deployments"
    )
    on_success(True)
    window._open_list_view("nodegroups")
    options["on_error"]("boom")  # not EKS (or unreadable): the entry goes away
    assert window.ui.navNodeGroups.isHidden() and window._view == "deployments"

    window.context_combo.clear()
    window.ui.navNodeGroups.setVisible(True)
    window._update_eks_entries()  # no context: nothing to ask
    assert window.ui.navNodeGroups.isHidden() and len(ran) >= 1
    window.close()


def test_the_config_menu_opens_and_lists_every_entry(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    assert not window.nav_config.isCheckable()

    window._toggle_submenu(window.config_submenu)
    window._submenus[window.config_submenu].stop()

    assert window._submenus[window.config_submenu].endValue() > 0
    for view in set(CONFIG_VIEWS) - {"nodegroups"}:
        assert window._nav_views[view].parent() is window.config_submenu
    assert window._nav_views["nodegroups"].parent() is not window.config_submenu
    window.close()


def test_network_lists_sort_filter_and_show_details(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    window._open_list_view("services")
    window._show_resources(
        ["ops"],
        [
            ClusterResource(
                "ops", "Service", "web", ("ClusterIP", "1", "—", "80/TCP"), "2d"
            ),
            ClusterResource(
                "ops", "Service", "api", ("NodePort", "2", "—", "80/TCP"), "5h"
            ),
        ],
    )
    window._sort_rows(2)  # by name
    assert [cell(window.table, r, 2).text() for r in range(2)] == ["api", "web"]
    window.search_input.setText("web")
    assert window.summary_label.text() == "1 of 2 Services"
    window.search_input.setText("")

    window.table.selectRow(1)
    assert present(window._selected_row()).name == "web"
    dispatched = []
    monkeypatch.setattr(window, "_run_action", lambda *a, **k: dispatched.append(a))
    window._view_details()
    assert dispatched[0][0].__name__ == "get_resource_details"
    assert dispatched[0][2:] == ("prod", "Service", "ops", "web")
    window.close()


def test_changing_network_kind_clears_rows_and_errors_empty_the_list(
    monkeypatch,
) -> None:
    window = _resource_window(monkeypatch)
    window._open_list_view("services")
    window._show_resources(
        ["ops"], [ClusterResource("ops", "Service", "web", ("a",) * 4, "1d")]
    )
    window._open_list_view("endpoints")  # other columns: the old rows go
    assert window._resources == [] and window.table.rowCount() == 0

    window._show_resources(
        ["ops"], [ClusterResource("ops", "Endpoints", "web", ("x",), "1d")]
    )
    window._show_error("boom")
    assert window._resources == []
    window.close()


def test_the_network_worker_loads_the_kind_of_its_view(monkeypatch) -> None:
    monkeypatch.setattr(
        window_module,
        "get_resources",
        lambda context, namespace, kind: (["ops"], [(context, namespace, kind)]),
    )
    done = []
    worker = window_module.RefreshWorker("ctx", "ops", "ingresses")
    worker.completed.connect(lambda namespaces, items: done.append((namespaces, items)))

    worker.run()

    assert done == [(["ops"], [("ctx", "ops", "Ingress")])]


def test_the_two_menus_open_and_close_independently(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    window.show()

    def settle() -> None:
        for animation in window._submenus.values():
            animation.setCurrentTime(animation.duration())

    window.nav_workloads.click()
    settle()
    window.nav_network.click()  # opening Network leaves Workloads open
    settle()
    assert window.submenu.maximumHeight() > 0
    assert window.network_submenu.maximumHeight() > 0

    window.nav_workloads.click()
    settle()
    assert window.submenu.maximumHeight() == 0
    assert window.network_submenu.maximumHeight() > 0
    window.close()


def test_the_menu_scrolls_when_both_lists_do_not_fit(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    window.resize(1100, 520)
    window.show()
    window.nav_workloads.click()
    window.nav_network.click()
    for animation in window._submenus.values():
        animation.setCurrentTime(animation.duration())
    application.processEvents()

    scroll = window.ui.sidebarScroll
    assert scroll.verticalScrollBar().maximum() > 0  # more menu than room
    assert not window.ui.settingsButton.isHidden()  # Settings stays in view


FORBIDDEN = (
    'Error from server (Forbidden): pods is forbidden: User "x" cannot list '
    'resource "pods" in API group "" at the cluster scope'
)


def test_a_forbidden_list_shows_the_permission_banner(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    assert window.permission_banner.isHidden()

    window._show_error(FORBIDDEN)

    assert not window.permission_banner.isHidden()
    assert "not allowed to list pods" in window.ui.permissionLabel.text()
    window.ui.permissionDismiss.click()
    assert window.permission_banner.isHidden()

    window._show_error("connection refused")  # not a permission problem
    assert window.permission_banner.isHidden()
    window.close()


def test_a_forbidden_action_shows_the_banner_instead_of_a_dialog(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    boxes = []
    monkeypatch.setattr(QMessageBox, "exec", lambda box: boxes.append(box.text()))

    window._show_action_error("pods is forbidden")  # kubectl names no action

    assert boxes == []
    assert "not allowed to do this" in window.ui.permissionLabel.text()
    window._show_action_error("connection refused")
    assert boxes  # other failures still get their dialog
    window.close()


def test_the_permission_banner_goes_away_once_a_list_loads(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    window._show_error(FORBIDDEN)
    assert not window.permission_banner.isHidden()

    window._answered("prod", None, window._view, ["ns"], [])
    assert window.permission_banner.isHidden()

    window._show_error(FORBIDDEN)
    window._context_changed()  # another cluster: the old refusal no longer applies
    assert window.permission_banner.isHidden()
    window.close()


def test_details_open_as_colored_json(monkeypatch) -> None:
    theme.set_theme("dark")
    window = _ready_window(monkeypatch)

    window._show_json_dialog("Pod: api", {"kind": "Pod", "replicas": 2})

    editor = _detail_tab(window).editor
    assert '"kind": "Pod"' in editor.toPlainText()
    assert isinstance(_detail_tab(window).highlighter, json_view.JsonHighlighter)
    assert "#1e1e1e" in editor.styleSheet()
    window.close()


def _two_context_window(monkeypatch):
    window = _ready_window(monkeypatch)
    monkeypatch.setattr(window, "_check_login", lambda *_a: None)
    monkeypatch.setattr(window, "refresh", lambda *_a: None)
    window.context_combo.clear()
    for name in ("a", "b"):
        window.context_combo.addItem(name, name)
    window.context_combo.setCurrentIndex(0)
    return window


def test_each_context_keeps_its_last_overviews(monkeypatch) -> None:
    window = _two_context_window(monkeypatch)
    window._show_overview("a", ClusterOverview(namespaces=7))
    window._show_workloads_overview("a", _workloads_overview())
    assert window.overview_ui.namespacesValue.text() == "7"

    window.context_combo.setCurrentIndex(1)  # nothing known about b: no old numbers
    assert window.overview_ui.namespacesValue.text() == "—"
    assert window.workloads_ui.podsLink.text() == "Pods (—)"
    assert window.workloads_table.rowCount() == 0
    assert window._overview is None and window._workloads_overview is None

    window.context_combo.setCurrentIndex(0)  # a again: its last answer is back
    assert window.overview_ui.namespacesValue.text() == "7"
    assert window.workloads_ui.podsLink.text() == "Pods (18)"
    assert window.workloads_table.rowCount() == 2
    assert window._overview_context is None  # fresh data is still requested
    window.close()


def test_an_overview_for_another_context_is_kept_for_later(monkeypatch) -> None:
    window = _two_context_window(monkeypatch)
    monkeypatch.setattr(window, "refresh_overview", lambda: None)
    monkeypatch.setattr(window, "refresh_workloads_overview", lambda: None)

    window._show_overview("b", ClusterOverview(namespaces=3))
    window._show_workloads_overview("b", _workloads_overview())

    assert window._overviews["b"].namespaces == 3 and "b" in window._workloads_overviews
    assert window.overview_ui.namespacesValue.text() == "—"  # a is on screen
    window.close()


def test_lists_show_the_last_answer_for_the_context_and_namespace(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    monkeypatch.setattr(window, "_check_login", lambda *_a: None)
    window.context_combo.clear()
    for name in ("a", "b"):
        window.context_combo.addItem(name, name)
    api = Workload("ns", "Deployment", "api", 1, 1, "1d")
    web = Workload("ns", "Deployment", "web", 1, 1, "1d")
    window._answers[("a", None, "deployments")] = (["ns"], [api])
    window._answers[("b", None, "deployments")] = (["ns"], [web])
    FakeRefreshWorker.outcome = ("ok", (["ns"], [api]))  # never answers for b

    window.context_combo.setCurrentIndex(0)
    window.refresh()  # a, all namespaces
    assert cell(window.table, 0, 2).text() == "api"

    window._workers.clear()
    FakeRefreshWorker.outcome = ("fail", "boom")  # b's fresh answer is slow
    monkeypatch.setattr(window, "_show_error", lambda *_a: None)
    window.context_combo.setCurrentIndex(1)
    window.refresh()
    assert cell(window.table, 0, 2).text() == "web"  # b's own answer, not a's

    window._workers.clear()
    window.context_combo.setCurrentIndex(0)
    window._answers.pop(("a", None, "deployments"))
    window._shown_key = None
    window.refresh()  # nothing kept for a now: an empty table, not b's rows
    assert window.table.rowCount() == 0
    FakeRefreshWorker.outcome = ("ok", ([], []))
    window.close()


def test_contexts_open_on_the_default_namespace(monkeypatch) -> None:
    window = _two_context_window(monkeypatch)
    window.settings.default_namespace = "team-a"

    window.context_combo.setCurrentIndex(1)  # a context change applies it
    assert window.namespace_combo.currentData() == "team-a"
    window._select_default_namespace()  # already there: the same item is kept
    assert window.namespace_combo.count() == 2

    window.settings.default_namespace = ""
    window._select_default_namespace()
    assert window.namespace_combo.currentData() == ""
    window.close()


def test_a_default_namespace_the_cluster_lacks_falls_back_to_all(monkeypatch) -> None:
    window = _two_context_window(monkeypatch)
    window.settings.default_namespace = "gone"
    window._select_default_namespace()
    started = []
    monkeypatch.setattr(window._list_timer, "start", lambda: started.append(True))

    window._fill_namespaces(["ops", "dev"])  # the cluster does not list it

    assert window.namespace_combo.currentData() == "" and started == [True]
    window._fill_namespaces(["ops", "dev"])  # all namespaces: nothing to redo
    assert started == [True]
    window.close()


def test_the_default_namespace_is_typed_with_the_clusters_namespaces_offered(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    monkeypatch.setattr(window, "_save_settings", lambda: None)
    window._namespaces = ["ops", "dev"]
    window._load_settings_form()
    edit = window.settings_ui.defaultNamespaceEdit
    assert edit.text() == "" and edit.placeholderText() == "All namespaces"
    assert cast(QStringListModel, present(edit.completer()).model()).stringList() == [
        "dev",
        "ops",
    ]

    edit.setText(" ops ")  # a name that no cluster lists is accepted too
    window._save_preferences()
    assert window.settings.default_namespace == "ops"

    window._namespaces = ["other"]
    window._load_settings_form()
    assert edit.text() == "ops"  # the saved one stays, whatever the cluster has

    edit.setText("")
    window._save_preferences()
    assert window.settings.default_namespace == ""
    window.close()


def test_save_writes_the_open_tab_to_the_chosen_file(monkeypatch, tmp_path) -> None:
    window = _ready_window(monkeypatch)
    window._show_json_dialog("Deployment: api", {"kind": "Deployment"})
    asked = []
    target = tmp_path / "details.json"

    def choose(_parent, _title, suggestion):
        asked.append(suggestion)
        return str(target), ""

    monkeypatch.setattr(window_module.QFileDialog, "getSaveFileName", choose)

    window.save_button.click()

    assert asked[0].endswith("Deployment-api.json")
    assert json.loads(target.read_text(encoding="utf-8")) == {"kind": "Deployment"}
    window.close()


def test_save_writes_the_shown_logs(monkeypatch, tmp_path) -> None:
    window = _ready_window(monkeypatch)
    window._show_logs_dialog(POD, "app", "2026-10-08T05:00:01Z INFO started")
    asked = []
    target = tmp_path / "logs.txt"
    monkeypatch.setattr(
        window_module.QFileDialog,
        "getSaveFileName",
        lambda _p, _t, suggestion: asked.append(suggestion) or (str(target), ""),
    )

    window._save_viewer_tab()

    assert asked[0].endswith("api-1-app.log")
    assert target.read_text(encoding="utf-8") == "2026-10-08T05:00:01Z INFO started"
    window.close()


def test_save_does_nothing_when_cancelled_and_reports_a_failed_write(
    monkeypatch, tmp_path
) -> None:
    window = _ready_window(monkeypatch)
    window._save_viewer_tab()  # no tab open: nothing to save
    window._show_json_dialog("Pod: x", {"a": 1})
    shown = []
    monkeypatch.setattr(QMessageBox, "exec", lambda box: shown.append(box.text()))

    monkeypatch.setattr(
        window_module.QFileDialog, "getSaveFileName", lambda *_a: ("", "")
    )
    window._save_viewer_tab()
    assert shown == []

    monkeypatch.setattr(
        window_module.QFileDialog,
        "getSaveFileName",
        lambda *_a: (str(tmp_path / "missing" / "x.json"), ""),
    )
    window._save_viewer_tab()
    assert shown and "could not be written" in shown[0]
    window.close()


def test_the_save_button_is_an_icon_with_a_tooltip(monkeypatch) -> None:
    window = _ready_window(monkeypatch)

    assert window.save_button.text() == "" and not window.save_button.icon().isNull()
    assert window.save_button.toolTip()
    window._retranslate()
    assert window.save_button.toolTip()
    window.close()


def test_a_theme_change_redraws_the_icons_of_open_log_tabs(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._show_logs_dialog(POD, "app", "2026-10-08T05:00:01Z INFO started")
    tab = current_tab(window.viewer_tabs, LogTab)
    before = tab.ui.refreshButton.icon().pixmap(18, 18).toImage()

    window.settings.theme = "dark"
    window._apply_theme()

    after = tab.ui.refreshButton.icon().pixmap(18, 18).toImage()
    assert not after.isNull() and after != before  # drawn in the new accent
    window.settings.theme = "light"
    window._apply_theme()
    window.close()


def test_a_theme_change_recolors_open_json_and_log_tabs(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._show_json_dialog("Pod: api", {"kind": "Pod"})
    json_editor = _detail_tab(window).editor
    window._show_logs_dialog(POD, "app", "2026-10-08T05:00:01Z INFO started")
    log_tab = current_tab(window.viewer_tabs, LogTab)
    assert "#1e1e1e" not in json_editor.styleSheet()  # light

    window.settings.theme = "dark"
    window._apply_theme()

    assert "#1e1e1e" in json_editor.styleSheet()
    assert "#1e1e1e" in log_tab.ui.logText.styleSheet()
    window.settings.theme = "light"
    window._apply_theme()
    assert "#1e1e1e" not in json_editor.styleSheet()
    window.close()


def test_ctrl_r_and_f5_press_the_refresh_button_of_the_page_on_screen(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    pressed = []
    for name, button in (
        ("overview", window.overview_refresh_button),
        ("list", window.refresh_button),
        ("workloads", window.workloads_refresh_button),
    ):
        button.setEnabled(True)
        button.clicked.connect(lambda _checked=False, name=name: pressed.append(name))
    window._show_logs_dialog(POD, "app", "2026-10-08T05:00:01Z INFO started")
    logs = current_tab(window.viewer_tabs, LogTab)
    logs.ui.refreshButton.clicked.connect(lambda: pressed.append("logs"))

    keys = sorted(
        shortcut.key().toString() for shortcut in window.findChildren(QShortcut)
    )
    assert keys == ["Ctrl+R", "F5"]

    for page in (0, 1, 4, 3):
        window.pages.setCurrentIndex(page)
        window._press_refresh()
    assert pressed == ["overview", "list", "workloads", "logs"]

    window._show_json_dialog("Pod: api", {"kind": "Pod"})  # no refresh on this tab
    window._press_refresh()
    window.pages.setCurrentIndex(2)  # settings have none either
    window._press_refresh()
    assert len(pressed) == 4

    window.refresh_button.setEnabled(False)  # busy: the button cannot be pressed
    window.pages.setCurrentIndex(1)
    window._press_refresh()
    assert len(pressed) == 4
    window.close()


RELEASE = Release(
    "0.3.0", "https://github.com/dcotecnologia/kubescope/releases/tag/v0.3.0"
)


def _update_window(monkeypatch, search_ms: int = 0):
    monkeypatch.setattr(window_module, "UPDATE_SEARCH_MS", search_ms)
    return _login_window(monkeypatch)


def test_the_update_icon_checks_on_demand_and_reports_each_outcome(monkeypatch) -> None:
    window, ran = _update_window(monkeypatch)
    ui = window.ui
    assert window._update_state == "idle"
    assert ui.updateButton.toolTip() == "Check for updates"

    ui.updateButton.click()
    ui.updateButton.click()  # one check at a time
    assert [name for name, *_rest in ran] == ["check_for_update"]
    assert ran[0][3]["quiet"] is True
    assert window._update_state == "checking" and window._update_timer.isActive()
    assert "Checking" in ui.updateButton.toolTip()

    ran[0][1](UpdateCheck("current"))
    assert window._update_state == "current" and not window._update_timer.isActive()
    assert "up to date" in ui.updateButton.toolTip()
    assert not ui.updateNotice.isHidden() and ui.updateNotice.text() == "Up to date"
    assert window._update_notice_timer.isActive()

    window._update_notice_timer.timeout.emit()  # the notice goes away by itself
    assert ui.updateNotice.isHidden()

    ui.updateButton.click()  # checking again from the up-to-date state
    assert ui.updateNotice.isHidden()
    ran[1][3]["on_error"]("boom")
    assert window._update_state == "failed"
    assert ui.updateNotice.text() == "Could not check"
    assert "Could not check" in ui.updateButton.toolTip()
    window.close()


def test_a_check_looks_like_a_search_for_at_least_five_seconds(monkeypatch) -> None:
    window, ran = _update_window(monkeypatch, search_ms=300)

    window.check_updates()
    ran[0][1](UpdateCheck("available", RELEASE))  # the answer is already here
    assert window._update_state == "checking"  # but it is shown later
    assert window._update_delay.isActive()

    _wait_until(lambda: window._update_state == "available")
    assert window._update_release == RELEASE
    window.close()


def test_an_available_update_opens_the_update_dialog(monkeypatch) -> None:
    window, ran = _update_window(monkeypatch)
    shown = []

    class FakeDialog:
        restart_command = None

        def __init__(self, parent, current, release, install):
            shown.append((parent, current, release, install))

        def exec(self):
            return QDialog.DialogCode.Rejected

    monkeypatch.setattr(window_module, "UpdateDialog", FakeDialog)
    ui = window.ui

    window.check_updates()
    assert ui.updateLink.isHidden()
    ran[0][1](UpdateCheck("available", RELEASE))
    assert window._update_state == "available" and window._update_timer.isActive()
    assert not ui.updateLink.isHidden() and ui.updateLink.text() == "Update available"
    assert "0.3.0" in ui.updateButton.toolTip()
    frames = {ui.updateButton.icon().cacheKey()}
    window._tick_update()
    frames.add(ui.updateButton.icon().cacheKey())
    assert len(frames) == 2  # the icon pulses

    ui.updateLink.click()
    ui.updateButton.click()
    assert [entry[2] for entry in shown] == [RELEASE, RELEASE]
    assert len(ran) == 1  # opening the dialog does not check again

    window._update_release = None  # nothing to update to
    window._update_app()
    assert len(shown) == 2

    window.check_updates()  # the right-click menu checks again
    assert ui.updateLink.isHidden()
    window.close()


def test_a_finished_update_restarts_the_app(monkeypatch) -> None:
    window, _ran = _update_window(monkeypatch)
    window._update_release = RELEASE
    restarted, quit_calls = [], []

    class FakeDialog:
        restart_command = ["kubescope"]

        def __init__(self, *_args):
            pass

        def exec(self):
            return QDialog.DialogCode.Accepted

    monkeypatch.setattr(window_module, "UpdateDialog", FakeDialog)
    monkeypatch.setattr(window_module, "restart", restarted.append)
    monkeypatch.setattr(
        QApplication, "quit", staticmethod(lambda: quit_calls.append(1))
    )

    window._update_app()

    assert restarted == [["kubescope"]] and quit_calls == [1]


def test_the_update_icon_spins_while_checking(monkeypatch) -> None:
    window, _ran = _update_window(monkeypatch)
    window.check_updates()
    first = window.ui.updateButton.icon().cacheKey()

    window._tick_update()

    assert window.ui.updateButton.icon().cacheKey() != first
    window.close()


def test_the_update_menu_checks_again(monkeypatch) -> None:
    window, ran = _update_window(monkeypatch)
    shown = []

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            shown.append([action.text() for action in self.actions()])
            self.actions()[0].trigger()
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)

    window._show_update_menu(QPoint(1, 1))

    assert shown == [["Check for updates again"]]
    assert [name for name, *_rest in ran] == ["check_for_update"]
    window.close()


def test_the_update_check_runs_at_start_only_when_settings_allow(monkeypatch) -> None:
    window, ran = _update_window(monkeypatch)
    window.settings.check_updates = False
    window.start_update_check()
    assert ran == []

    window.settings.check_updates = True
    window.start_update_check()
    assert [name for name, *_rest in ran] == ["check_for_update"]
    window.close()


def test_the_update_check_is_switched_from_the_settings_page(monkeypatch) -> None:
    window, ran = _update_window(monkeypatch)
    form = window.settings_ui

    window._load_settings_form()
    assert form.updatesCheck.isChecked() is True

    window._save_preferences()  # still on: no new check
    assert ran == []

    form.updatesCheck.setChecked(False)
    window._save_preferences()
    assert window.settings.check_updates is False

    form.updatesCheck.setChecked(True)
    window._save_preferences()
    assert window.settings.check_updates is True
    assert [name for name, *_rest in ran] == ["check_for_update"]
    window.close()


def test_the_update_check_really_runs_in_the_background(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "UPDATE_SEARCH_MS", 0)
    window = _ready_window(monkeypatch)
    monkeypatch.setattr(
        window_module, "check_for_update", lambda: UpdateCheck("available", RELEASE)
    )

    window.check_updates()
    _wait_until(lambda: window._update_state == "available")

    assert window._update_release == RELEASE
    window.close()


def test_a_check_keeps_searching_for_at_least_five_seconds(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    monkeypatch.setattr(window_module, "UPDATE_SEARCH_MS", 5000)
    clock = [100.0]
    monkeypatch.setattr(window_module.time, "monotonic", lambda: clock[0])

    window.check_updates()
    clock[0] += 0.4  # the answer came back quickly
    ran[0][1](UpdateCheck("current"))

    assert window._update_state == "checking"  # still searching
    assert 4000 <= window._update_delay.remainingTime() <= 5000
    window._update_delay.timeout.emit()
    assert window._update_state == "current"
    assert window.ui.updateNotice.text() == "Up to date"
    assert not window.ui.updateNotice.isHidden()

    window.check_updates()
    clock[0] += 7  # a slow answer is shown at once
    ran[1][1](UpdateCheck("current"))
    assert window._update_state == "current"
    window.close()


def test_the_up_to_date_text_goes_away_by_itself(monkeypatch) -> None:
    window, ran = _login_window(monkeypatch)
    window.check_updates()
    ran[0][1](UpdateCheck("current"))
    assert not window.ui.updateNotice.isHidden()
    assert window._update_notice_timer.isActive()

    window._update_notice_timer.timeout.emit()
    assert window.ui.updateNotice.isHidden()

    window.check_updates()  # a new check hides the old text at once
    assert window.ui.updateNotice.isHidden()
    ran[1][3]["on_error"]("offline")
    assert window.ui.updateNotice.text() == "Could not check"
    window.close()


def test_the_window_opens_at_the_size_it_was_closed_with(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    first = window.size()
    window.resize(first.width(), first.height() + 10)  # the test screen is narrow
    resized = window.size()
    assert resized != first
    window.close()
    assert window.settings.window_geometry

    reopened = window_module.WorkloadWindow(window.settings)
    assert reopened.size() == resized
    reopened.close()


def test_a_damaged_saved_geometry_is_ignored(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.settings.window_geometry = "not a geometry"

    reopened = window_module.WorkloadWindow(window.settings)

    assert reopened.isVisible() is False and reopened.width() > 0
    reopened.close()
    window.close()


def test_the_settings_page_lists_kubeconfig_files_and_sign_in_commands(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.settings.kubeconfig_files = ["/home/me/work.yaml"]
    window.settings.sign_in_commands = {"oci": "oci session authenticate"}
    window._load_settings_form()
    form = window.settings_ui

    assert [form.kubeconfigList.item(i).text() for i in range(1)] == [
        "/home/me/work.yaml"
    ]
    assert form.loginTable.rowCount() == 1
    assert cell(form.loginTable, 0, 0).text() == "oci"
    assert cell(form.loginTable, 0, 1).text() == "oci session authenticate"
    window.close()


def test_kubeconfig_files_are_added_removed_and_applied(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    reloaded = []
    monkeypatch.setattr(window, "_load_contexts", lambda: reloaded.append(True))
    chosen = iter([("/home/me/a.yaml", ""), ("/home/me/a.yaml", ""), ("", "")])
    monkeypatch.setattr(
        window_module.QFileDialog, "getOpenFileName", lambda *_a, **_k: next(chosen)
    )
    form = window.settings_ui
    window._load_settings_form()

    window._add_kubeconfig_file()
    window._add_kubeconfig_file()  # the same file twice counts once
    window._add_kubeconfig_file()  # a cancelled dialog adds nothing
    assert form.kubeconfigList.count() == 1

    window._save_preferences()
    assert window.settings.kubeconfig_files == ["/home/me/a.yaml"]
    assert cluster_module._kubeconfig_files == ["/home/me/a.yaml"]
    assert reloaded == [True]  # the contexts come from other files now

    window._save_preferences()  # unchanged: nothing reloads
    assert reloaded == [True]

    form.kubeconfigList.setCurrentRow(0)
    window._remove_kubeconfig_file()
    window._save_preferences()
    assert window.settings.kubeconfig_files == []
    assert reloaded == [True, True]
    window.close()


def test_sign_in_commands_are_edited_in_the_settings_page(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    form = window.settings_ui
    window._load_settings_form()

    window._add_login_row("oci", "oci session authenticate")
    window._add_login_row()  # an empty row is ignored
    window._save_preferences()
    assert window.settings.sign_in_commands == {"oci": "oci session authenticate"}
    assert form.noticeLabel.text() == "Settings saved."

    form.loginTable.setCurrentCell(0, 0)
    window._remove_login_row()
    window._remove_login_row()  # nothing selected anymore: nothing happens
    window._save_preferences()
    assert window.settings.sign_in_commands == {}
    window.close()


@pytest.mark.parametrize(
    ("program", "command"), [("oci", 'oci "unclosed'), ("", "oci login"), ("oci", "")]
)
def test_an_invalid_sign_in_command_is_not_saved(monkeypatch, program, command) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    window._add_login_row(program, command)

    window._save_preferences()

    assert "row 1 is not valid" in window.settings_ui.noticeLabel.text()
    assert window.settings.sign_in_commands == {}
    window.close()


def test_the_window_gives_the_cluster_layer_its_settings_at_start(monkeypatch) -> None:
    settings = Settings()
    settings.kubeconfig_files = ["/x.yaml"]
    settings.sign_in_commands = {"oci": "oci login"}
    settings.save()

    window = _ready_window(monkeypatch)

    assert cluster_module._kubeconfig_files == ["/x.yaml"]
    assert cluster_module._custom_logins == {"oci": "oci login"}
    window.close()


def test_the_kubeconfig_and_sign_in_tables_show_only_with_rows(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    form = window.settings_ui
    window.show()
    window._load_settings_form()
    assert form.kubeconfigList.isHidden() and form.kubeconfigRemoveButton.isHidden()
    assert form.loginTable.isHidden() and form.loginRemoveButton.isHidden()
    assert not form.kubeconfigAddButton.isHidden()  # adding is always possible
    assert not form.loginAddButton.isHidden()

    window._add_login_row("oci", "oci login")
    assert not form.loginTable.isHidden() and not form.loginRemoveButton.isHidden()
    form.loginTable.setCurrentCell(0, 0)
    window._remove_login_row()
    assert form.loginTable.isHidden() and form.loginRemoveButton.isHidden()

    form.kubeconfigList.addItem("/home/me/a.yaml")
    window._show_config_tables()
    assert not form.kubeconfigList.isHidden()
    form.kubeconfigList.setCurrentRow(0)
    window._remove_kubeconfig_file()
    assert form.kubeconfigList.isHidden()
    window.close()


def test_clearing_the_cache_forgets_answers_overviews_and_sign_ins(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    forgotten = []
    monkeypatch.setattr(window_module, "forget_clients", lambda: forgotten.append(True))
    window._answers[("prod", None, "pods")] = (["ns"], [])
    window._overviews["prod"] = ClusterOverview()
    window._workloads_overviews["prod"] = WorkloadsOverview(kinds={}, events=())
    window._overview = ClusterOverview()
    window._shown_key = ("prod", None, "pods")
    window._overview_context = window._workloads_overview_context = "prod"

    window.settings_ui.clearCacheButton.click()

    assert forgotten == [True]
    assert not window._answers and not window._overviews
    assert not window._workloads_overviews
    assert window._overview is None and window._shown_key is None
    assert window._overview_context is None
    assert window._workloads_overview_context is None
    assert "Cache cleared" in window.settings_ui.noticeLabel.text()
    window.close()


def test_a_list_can_be_pinned_to_the_top_of_the_menu(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    assert window.ui.pinnedBar.isHidden()

    window._toggle_pin("secrets")
    window._toggle_pin("pods")

    texts = [button.text() for button in window._pinned_buttons]
    assert texts == ["Secrets", "Pods"] and not window.ui.pinnedBar.isHidden()
    assert window.settings.pinned_views() == ["secrets", "pods"]
    window._pinned_buttons[0].click()
    assert window._view == "secrets"
    assert window._pinned_buttons[0].isChecked()
    assert not window._pinned_buttons[1].isChecked()

    tab = present(window._pinned_buttons[0].parentWidget())
    assert tab.property("active") == "true"
    assert (
        present(window._pinned_buttons[1].parentWidget()).property("active") == "false"
    )
    tab.findChildren(QPushButton)[1].click()  # the × takes it back
    assert [b.text() for b in window._pinned_buttons] == ["Pods"]
    window._toggle_pin("pods")
    assert window.ui.pinnedBar.isHidden()
    window.close()


def test_the_overview_pages_can_be_pinned_to_the_top(monkeypatch) -> None:
    window = _resource_window(monkeypatch)

    window._toggle_pin("workloads-overview")
    window._toggle_pin("cluster-overview")

    assert [b.text() for b in window._pinned_buttons] == ["Overview", "Cluster"]
    window._pinned_buttons[0].click()
    assert window.pages.currentIndex() == 4
    assert window._pinned_buttons[0].isChecked()
    assert not window._pinned_buttons[1].isChecked()
    window._pinned_buttons[1].click()
    assert window.pages.currentIndex() == 0
    window._toggle_pin("workloads-overview")
    window._toggle_pin("cluster-overview")

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            self.actions()[0].trigger()
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)
    window.nav_overview.customContextMenuRequested.emit(QPoint(1, 1))
    assert window.settings.pinned_views() == ["cluster-overview"]
    window._pinned_buttons[0].customContextMenuRequested.emit(QPoint(1, 1))
    assert window.settings.pinned_views() == []
    window.close()


def test_a_window_opens_with_the_overviews_already_pinned(
    monkeypatch, tmp_path
) -> None:
    settings = Settings(tmp_path / "settings.json")
    settings.set_pinned_views(["cluster-overview", "workloads-overview"])
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    monkeypatch.setattr(
        window_module.WorkloadWindow, "refresh_overview", lambda *_a: None
    )

    window = window_module.WorkloadWindow(settings)

    assert [b.text() for b in window._pinned_buttons] == ["Cluster", "Overview"]
    window.close()


def test_pinned_tabs_can_be_dragged_to_reorder_them(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    window.show()
    for view in ("secrets", "pods", "leases"):
        window._toggle_pin(view)
    started = []

    class FakeDrag:
        def __init__(self, source) -> None:
            self.source = source

        def setMimeData(self, mime) -> None:
            self.mime = mime

        def setPixmap(self, _pixmap) -> None:
            pass

        def setHotSpot(self, _point) -> None:
            pass

        def exec(self, _action) -> None:
            started.append((self.source, bytes(self.mime.data(PIN_MIME)).decode()))

    monkeypatch.setattr(window_module, "QDrag", FakeDrag)
    first = window._pinned_buttons[0]
    start = QPointF(5, 5)

    def mouse(kind, position, button=Qt.MouseButton.LeftButton, buttons=None):
        return QMouseEvent(
            kind,
            position,
            window.mapToGlobal(position.toPoint()),
            button,
            button if buttons is None else buttons,
            Qt.KeyboardModifier.NoModifier,
        )

    # a small move is a click, not a drag
    window.eventFilter(first, mouse(QEvent.Type.MouseButtonPress, start))
    window.eventFilter(first, mouse(QEvent.Type.MouseMove, QPointF(6, 5)))
    assert not started
    # another button forgets the drag; moving then starts nothing
    window.eventFilter(
        first, mouse(QEvent.Type.MouseButtonPress, start, Qt.MouseButton.RightButton)
    )
    window.eventFilter(first, mouse(QEvent.Type.MouseMove, QPointF(80, 5)))
    assert not started
    # a finished click, and a mouse moving with no button down, never drag
    window.eventFilter(first, mouse(QEvent.Type.MouseButtonPress, start))
    window.eventFilter(first, mouse(QEvent.Type.MouseButtonRelease, start))
    window.eventFilter(first, mouse(QEvent.Type.MouseMove, QPointF(80, 5)))
    assert not started
    window.eventFilter(first, mouse(QEvent.Type.MouseButtonPress, start))
    assert not window.eventFilter(
        first,
        mouse(QEvent.Type.MouseMove, QPointF(80, 5), buttons=Qt.MouseButton.NoButton),
    )
    assert not started
    assert window.eventFilter(first, mouse(QEvent.Type.MouseMove, QPointF(80, 5)))
    assert started == [(first.parentWidget(), "secrets")]
    window.eventFilter(first, mouse(QEvent.Type.MouseMove, QPointF(90, 5)))
    assert len(started) == 1

    bar = window.ui.pinnedBar
    mime = QMimeData()
    mime.setData(PIN_MIME, b"secrets")

    class FakeDragEvent(QEvent):
        def __init__(self, kind, x, data) -> None:
            super().__init__(kind)
            self._x, self._data = x, data

        def mimeData(self):
            return self._data

        def position(self):
            return QPointF(self._x, 5)

        def acceptProposedAction(self) -> None:
            pass

    def drop(kind, x, data=mime):
        return FakeDragEvent(kind, x, data)

    foreign = QMimeData()
    foreign.setText("x")
    assert not window.eventFilter(bar, drop(QEvent.Type.DragEnter, 1, foreign))
    assert window.eventFilter(bar, drop(QEvent.Type.DragEnter, 1))
    marker = window._drop_marker
    assert window.eventFilter(bar, drop(QEvent.Type.DragMove, 1))
    assert marker.isVisibleTo(bar)  # the line shows where it would land
    before = marker.x()
    last = present(window._pinned_buttons[-1].parentWidget())
    right_of_all = last.mapTo(bar, last.rect().bottomRight()).x() + 10
    assert window.eventFilter(bar, drop(QEvent.Type.DragMove, right_of_all))
    assert marker.x() > before
    assert not window.eventFilter(bar, FakeDragEvent(QEvent.Type.DragLeave, 0, mime))
    assert marker.isHidden()
    assert window.eventFilter(bar, drop(QEvent.Type.Drop, right_of_all))
    _wait_until(lambda: window.settings.pinned_views() == ["pods", "leases", "secrets"])
    assert [b.text() for b in window._pinned_buttons] == ["Pods", "Leases", "Secrets"]

    window._move_tab(("pin", "secrets"), 0)  # before every other tab
    assert window.settings.pinned_views() == ["secrets", "pods", "leases"]
    window._move_tab(("pin", "secrets"), 0)  # already there: nothing changes
    window._move_tab(("pin", "unknown"), 0)
    assert window.settings.pinned_views() == ["secrets", "pods", "leases"]
    window.close()


def test_open_details_and_logs_tabs_move_and_close_like_the_pinned_ones(
    monkeypatch,
) -> None:
    window = _resource_window(monkeypatch)
    window.show()
    window._toggle_pin("pods")
    for title in ("First", "Second", "Third"):
        window._add_viewer_tab(QWidget(), title)

    def shown() -> list[str]:
        return [button.toolTip() or button.text() for button in window._pinned_buttons]

    def titles() -> list[str]:
        return [
            window.viewer_tabs.tabText(i) for i in range(window.viewer_tabs.count())
        ]

    bar = window.ui.pinnedBar
    mime = QMimeData()
    mime.setData(VIEWER_MIME, b"0")

    class FakeDragEvent(QEvent):
        def __init__(self, kind, x) -> None:
            super().__init__(kind)
            self._x = x

        def mimeData(self):
            return mime

        def position(self):
            return QPointF(self._x, 5)

        def acceptProposedAction(self) -> None:
            pass

    started = []

    class FakeDrag:
        def __init__(self, source) -> None:
            self.source = source

        def setMimeData(self, data) -> None:
            started.append(bytes(data.data(VIEWER_MIME)).decode())

        def setPixmap(self, _pixmap) -> None:
            pass

        def setHotSpot(self, _point) -> None:
            pass

        def exec(self, _action) -> None:
            pass

    monkeypatch.setattr(window_module, "QDrag", FakeDrag)
    first = window._pinned_buttons[1]  # after the pinned Pods
    press = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(5, 5),
        first.mapToGlobal(QPoint(5, 5)),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    move = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(80, 5),
        first.mapToGlobal(QPoint(80, 5)),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    window.eventFilter(first, press)
    assert window.eventFilter(first, move)
    assert started == ["0"]

    last = present(window._pinned_buttons[-1].parentWidget())
    right_of_all = last.mapTo(bar, last.rect().bottomRight()).x() + 10
    assert window.eventFilter(bar, FakeDragEvent(QEvent.Type.DragMove, right_of_all))
    assert window._drop_marker.isVisibleTo(bar)
    assert window.eventFilter(bar, FakeDragEvent(QEvent.Type.Drop, right_of_all))
    _wait_until(lambda: shown() == ["Pods", "Second", "Third", "First"])
    assert window.settings.pinned_views() == ["pods"]

    # a Details or Logs tab goes in front of a pinned one, and back behind it
    window._move_tab(("viewer", window.viewer_tabs.widget(0)), 0)
    assert shown() == ["First", "Pods", "Second", "Third"]
    window._move_tab(("viewer", window.viewer_tabs.widget(0)), right_of_all)
    assert shown() == ["Pods", "Second", "Third", "First"]
    # and a pinned one goes among them, which is remembered with the pinned
    window._toggle_pin("secrets")
    assert shown() == ["Pods", "Second", "Third", "First", "Secrets"]
    window._move_tab(("pin", "secrets"), 0)
    assert shown() == ["Secrets", "Pods", "Second", "Third", "First"]
    assert window.settings.pinned_views() == ["secrets", "pods"]
    window._toggle_pin("secrets")
    assert shown() == ["Pods", "Second", "Third", "First"]
    mime.setData(VIEWER_MIME, b"9")  # a tab that is no longer there
    assert not window.eventFilter(bar, FakeDragEvent(QEvent.Type.DragMove, 5))

    # the middle button closes the tab
    middle = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(5, 5),
        first.mapToGlobal(QPoint(5, 5)),
        Qt.MouseButton.MiddleButton,
        Qt.MouseButton.MiddleButton,
        Qt.KeyboardModifier.NoModifier,
    )
    assert window.eventFilter(window._pinned_buttons[1], middle)
    assert titles() == ["First", "Third"]  # the bar showed Second there
    window.close()


def _welcome_window(monkeypatch, pressed: str | None):
    """A window whose welcome box is answered by pressing the button
    `pressed`."""
    window = _ready_window(monkeypatch)
    window.settings.welcome_dismissed = False
    shown = []
    opened = []

    class FakeBox(QMessageBox):
        def exec(self) -> int:
            shown.append(self.text())
            buttons = {b.text(): b for b in self.buttons()}
            self._pressed = buttons.get(pressed or "")
            return 0

        def clickedButton(self) -> QAbstractButton:
            return cast(QAbstractButton, self._pressed)

    monkeypatch.setattr(window_module, "QMessageBox", FakeBox)
    monkeypatch.setattr(
        window_module.QDesktopServices, "openUrl", lambda url: opened.append(url)
    )
    return window, shown, opened


def test_the_welcome_invites_to_contribute_and_opens_github(monkeypatch) -> None:
    window, shown, opened = _welcome_window(monkeypatch, "Open on GitHub")

    window.show_welcome()

    assert shown == ["Welcome to KubeScope"]
    assert [url.toString() for url in opened] == [window_module.PROJECT_URL]
    assert window.settings.welcome_dismissed is False  # it comes back next time
    window.close()


def test_the_welcome_can_open_the_sponsor_page(monkeypatch) -> None:
    window, _shown, opened = _welcome_window(monkeypatch, "Sponsor on GitHub")

    window.show_welcome()

    assert [url.toString() for url in opened] == [window_module.SPONSOR_URL]
    assert window.settings.welcome_dismissed is False
    window.close()


def test_the_welcome_can_be_dismissed_for_good(monkeypatch) -> None:
    window, shown, _opened = _welcome_window(monkeypatch, "Don't show again")

    window.show_welcome()
    assert window.settings.welcome_dismissed is True
    window.show_welcome()  # dismissed: no second box

    assert len(shown) == 1
    window.close()


def test_maybe_later_closes_the_welcome_but_keeps_it_for_next_time(
    monkeypatch,
) -> None:
    window, shown, opened = _welcome_window(monkeypatch, "Maybe later")

    window.show_welcome()

    assert len(shown) == 1 and not opened
    assert window.settings.welcome_dismissed is False
    window.close()


def test_the_pin_menu_offers_pin_or_unpin(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    offered = []

    class FakeMenu(QMenu):
        def exec(self, *_args, **_kwargs) -> QAction:
            action = self.actions()[0]
            offered.append(action.text())
            action.trigger()
            return QAction(self)  # the choice is not read

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)
    window._nav_views["leases"].customContextMenuRequested.emit(QPoint(1, 1))
    assert window.settings.pinned_views() == ["leases"]
    window._pinned_buttons[0].customContextMenuRequested.emit(QPoint(1, 1))

    assert offered == ["Pin to the top", "Close"]  # on the tab: close = unpin
    assert window.settings.pinned_views() == [] and window.ui.pinnedBar.isHidden()
    window.close()


def test_pinned_lists_that_are_not_available_stay_out_of_the_menu(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    window.settings.set_pinned_views(["nodegroups", "unknown", "pods"])
    window._render_pinned()
    assert [b.text() for b in window._pinned_buttons] == ["Pods"]

    window._show_eks_entries("prod", True)  # an EKS context: Node Groups is there
    assert [b.text() for b in window._pinned_buttons] == ["Node Groups", "Pods"]
    window._retranslate()  # a language change keeps them
    assert len(window._pinned_buttons) == 2
    window._show_eks_entries("prod", False)
    assert [b.text() for b in window._pinned_buttons] == ["Pods"]
    window.close()


def test_two_quick_clicks_pin_a_list_and_the_middle_button_unpins_it(
    monkeypatch,
) -> None:
    window = _resource_window(monkeypatch)
    entry = window._nav_views["leases"]

    QTest.mouseDClick(entry, Qt.MouseButton.LeftButton)
    assert window.settings.pinned_views() == ["leases"]
    QTest.mouseDClick(entry, Qt.MouseButton.LeftButton)  # already there: it stays
    assert window.settings.pinned_views() == ["leases"]
    QTest.mouseClick(entry, Qt.MouseButton.RightButton)  # other buttons do nothing
    assert window.settings.pinned_views() == ["leases"]

    tab_button = window._pinned_buttons[0]
    QTest.mouseClick(tab_button, Qt.MouseButton.LeftButton)  # a plain click opens it
    assert window._view == "leases" and window.settings.pinned_views() == ["leases"]
    tab_button = window._pinned_buttons[0]  # the bar was redrawn by that click
    QTest.mouseClick(tab_button, Qt.MouseButton.MiddleButton)
    assert window.settings.pinned_views() == [] and window._pinned_buttons == []

    window._toggle_pin("pods")
    tab = present(window._pinned_buttons[0].parentWidget())
    QTest.mouseClick(tab, Qt.MouseButton.MiddleButton)  # anywhere on the tab
    assert window.settings.pinned_views() == []
    window.close()


def test_aws_words_are_shown_in_the_interface_language(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    assert window._aws_value("ACTIVE") == "Active"
    assert window._aws_value("CREATE_FAILED") == "Creation failed"
    assert window._aws_value("Public and private") == "Public and private"
    assert window._aws_value("SOMETHING_NEW") == "SOMETHING_NEW"  # unknown: as it came

    window._open_list_view("nodegroups")
    window._show_resources(
        [],
        [
            ClusterResource(
                "", "NodeGroup", "ng", ("DELETE_FAILED", "m5", "1", "A", "v"), "1d"
            )
        ],
    )
    assert cell(window.table, 0, 3).text() == "Deletion failed"
    window.close()


def test_a_custom_theme_can_be_deleted_after_confirming(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    page = window.settings_ui
    assert not page.deleteThemeButton.isEnabled()  # the built-in themes stay
    window._delete_theme()  # a built-in one is selected: nothing happens
    _accept_editor(monkeypatch, name="Ocean", page="#001122")
    page.newThemeButton.click()
    assert page.deleteThemeButton.isEnabled()
    answer = {"yes": False}
    monkeypatch.setattr(window, "_confirm", lambda *_a: answer["yes"])

    page.deleteThemeButton.click()  # cancelled
    assert page.themeCombo.count() == 3

    answer["yes"] = True
    page.deleteThemeButton.click()
    assert page.themeCombo.count() == 2
    assert not list(window_module.themes_directory().glob("*.json"))
    window.close()


def test_deleting_the_theme_in_use_goes_back_to_the_default(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    page = window.settings_ui
    _accept_editor(monkeypatch, name="Ocean", page="#001122")
    page.newThemeButton.click()
    page.saveButton.click()
    assert window.settings.theme == "ocean" and "#001122" in window.styleSheet()
    monkeypatch.setattr(window, "_confirm", lambda *_a: True)

    window._delete_theme()

    assert window.settings.theme == "dark"
    assert page.themeCombo.currentData() == "dark"
    assert "#001122" not in window.styleSheet()
    window.close()


def test_a_theme_file_that_cannot_be_removed_is_reported(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    _accept_editor(monkeypatch, name="Ocean", page="#001122")
    window.settings_ui.newThemeButton.click()
    monkeypatch.setattr(window, "_confirm", lambda *_a: True)
    shown = []
    monkeypatch.setattr(window, "_show_write_error", shown.append)

    def broken(_theme_id):
        raise OSError("read-only folder")

    monkeypatch.setattr(window_module, "delete_custom_theme", broken)
    window._delete_theme()

    assert shown == ["read-only folder"]
    assert window.settings_ui.themeCombo.count() == 3  # still there
    window.close()


def test_a_bundled_theme_can_be_edited_but_not_deleted(monkeypatch, tmp_path) -> None:
    bundled = tmp_path / "bundled"
    bundled.mkdir()
    (bundled / "reef.json").write_text('{"name": "Reef", "base": "dark"}')
    monkeypatch.setattr(theme, "BUNDLED_DIRECTORY", bundled)
    theme.install_bundled_themes(bundled)
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    page = window.settings_ui

    page.themeCombo.setCurrentIndex(page.themeCombo.findData("reef"))

    assert page.editThemeButton.isEnabled()
    assert not page.deleteThemeButton.isEnabled()
    monkeypatch.setattr(window, "_confirm", lambda *_a: True)
    window._delete_theme()  # even asked directly, it stays
    assert (window_module.themes_directory() / "reef.json").exists()
    window.close()


def test_pod_details_follow_the_live_usage(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    samples = iter([(0.25, 2.0**27), None])
    calls = []

    def run(operation, on_success, *arguments, **options):
        calls.append((operation, arguments, options["quiet"]))
        on_success(next(samples))

    monkeypatch.setattr(window, "_run_action", run)

    window._show_json_dialog("Pod: api-1", {"kind": "Pod"}, POD)

    tab = _detail_tab(window)
    assert calls == [(window_module.get_pod_usage, ("prod", "ns", "api-1"), True)]
    assert tab.cpu_chart.samples == [0.25]
    assert tab.memory_chart.samples == [2.0**27]

    window._refresh_usage(tab, POD, True)  # another sample, none this time
    assert tab.usage_note.text().startswith("Live usage needs metrics-server")
    assert not tab.cpu_chart.isVisibleTo(tab)

    tab.busy = True
    window._refresh_usage(tab, POD, True)  # one is in flight
    tab.busy = False
    window.pages.setCurrentIndex(1)
    window._refresh_usage(tab, POD)  # not on screen
    tab.closed = True
    window._refresh_usage(tab, POD, True)
    assert len(calls) == 2
    window.close()


def test_usage_errors_and_a_closed_tab_are_ignored(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    outcomes = []

    def run(_operation, on_success, *_arguments, on_error, quiet):
        outcomes.append((on_success, on_error))

    monkeypatch.setattr(window, "_run_action", run)
    window._show_json_dialog("Pod: api-1", {"kind": "Pod"}, POD)
    tab = _detail_tab(window)
    assert tab.busy

    outcomes[0][1]("boom")  # a failed sample only frees the tab for the next
    assert not tab.busy

    window._refresh_usage(tab, POD, True)
    tab.closed = True
    outcomes[1][0]((1.0, 1.0))
    assert tab.cpu_chart.samples == []
    window.close()


def test_details_can_switch_between_the_overview_and_the_raw_json(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window._show_json_dialog("Deployment: api", {"kind": "Deployment"})
    tab = _detail_tab(window)
    assert not tab.showing_raw
    assert not tab.usage_box.isVisibleTo(tab)  # only Pods have live usage

    tab.raw_button.click()
    assert tab.showing_raw
    tab.overview_button.click()
    assert not tab.showing_raw
    window.close()


def test_details_overview_shows_sections_subsections_and_tables(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    document = {
        "kind": "Pod",
        "metadata": {"name": "api-1", "labels": {"a": "b", "c": "d"}},
        "spec": {
            "containers": [
                {
                    "name": "app",
                    "command": ["sh", "-c"],
                    "env": [{"name": "A", "value": "1"}],
                    "nested": [{"name": "n", "x": {"y": [{"k": 1, "z": {"q": 1}}]}}],
                    "script": "line 1\nline 2",
                }
            ]
        },
    }

    window._show_json_dialog("Pod: api-1", document)

    tab = _detail_tab(window)
    tab.restyle()
    texts = [label.text() for label in tab.findChildren(window_module.QLabel)]
    assert "containers: app" in texts
    assert "containers: app / nested: n" in texts
    assert "sh" in texts and "line 1\nline 2" in texts
    assert tab.findChildren(QTableWidget)
    window.close()


def test_a_tab_is_shown_only_in_its_own_context(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._show_json_dialog("Pod: x", {"a": 1})
    assert len(window._pinned_buttons) == 1
    assert window.pages.currentIndex() == 3

    window.context_combo.addItem("stage")
    window.context_combo.setCurrentIndex(1)

    assert window._pinned_buttons == []  # kept open, but not shown here
    assert window.viewer_tabs.count() == 1
    assert window.pages.currentIndex() == 1

    window.context_combo.setCurrentIndex(0)

    assert len(window._pinned_buttons) == 1
    window.close()


def test_changing_context_lands_on_a_tab_of_the_new_context(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.context_combo.addItem("stage")
    window._show_json_dialog("Pod: prod", {"a": 1})
    window.context_combo.setCurrentIndex(1)
    window._show_json_dialog("Pod: stage", {"a": 2})
    window.viewer_tabs.setCurrentIndex(0)  # the prod tab, still the shown one

    window._leave_other_context_tab()

    assert window.viewer_tabs.currentIndex() == 1
    window.close()


def test_the_name_column_starts_wide_enough_for_its_names(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.table.setRowCount(1)
    window.table.setItem(0, 2, QTableWidgetItem("a-very-long-name-" * 6))

    window._fit_name_column()
    fitted = window.table.columnWidth(2)
    window.table.setColumnWidth(2, 50)
    window._fit_name_column()  # once per list: the width is theirs now

    assert fitted > 260
    assert window.table.columnWidth(2) == 50
    window.close()


def test_the_cluster_info_is_read_again_once_the_overview_loads(monkeypatch) -> None:
    window = _resource_window(monkeypatch)
    ran = []
    monkeypatch.setattr(window, "_run_action", lambda *a, **k: ran.append((a, k)))
    monkeypatch.setattr(window, "_context", lambda: "prod")
    window._show_eks_entries("prod", True)
    ran[-1][1]["on_error"]("not signed in")  # read before the sign-in
    ran.clear()

    window._show_overview("prod", ClusterOverview())

    assert [call[0][0].__name__ for call in ran] == ["get_cluster_info"]


def test_pods_and_workloads_draw_colored_squares_for_their_states(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.resize(1000, 600)
    window.show()
    window._open_list_view("pods")
    window._show_pods(
        ["ns"],
        [
            PodInfo(
                "ns",
                "p",
                "Running",
                1,
                2,
                "1d",
                ("app", "side"),
                container_states=("running", "error"),
            ),
            PodInfo("ns", "q", "Running", 0, 0, "1d", ()),  # nothing to draw
        ],
    )
    item = cell(window.table, 0, 3)
    assert item.text() == "1/2" and item.data(STATES_ROLE) == ("running", "error")
    assert item.data(TIPS_ROLE) == ("app: Running", "side: Error")
    assert cell(window.table, 1, 3).data(STATES_ROLE) is None

    window.table.viewport().grab()  # paints the squares and the plain cell
    delegate = window.table.itemDelegateForColumn(3)
    option = QStyleOptionViewItem()
    index = window.table.model().index(0, 3)
    assert delegate.sizeHint(option, index).width() > 2 * 8 + 2 * 12 + 4
    plain = window.table.model().index(1, 3)
    assert delegate.sizeHint(option, plain).width() >= 0

    shown = []
    monkeypatch.setattr(
        QToolTip, "showText", lambda _pos, text, *_a: shown.append(text)
    )
    hidden = []
    monkeypatch.setattr(QToolTip, "hideText", lambda: hidden.append(True))
    option.rect = QRect(0, 0, 120, 30)

    def hover(x: int, at=index) -> None:
        event = QHelpEvent(QEvent.Type.ToolTip, QPoint(x, 10), QPoint(x, 10))
        delegate.helpEvent(event, window.table, option, at)

    hover(8 + 16 + 2)  # on the second square
    hover(8 + 12 + 1)  # in the gap between two
    hover(100)  # past the last
    hover(5, plain)  # a cell without squares
    assert shown == ["side: Error"] and len(hidden) == 2

    window._open_list_view("deployments")
    window._show_workloads(
        ["ns"],
        [
            Workload("ns", "Deployment", "api", 1, 2, "1d"),
            Workload("ns", "CronJob", "job", 0, 0, "1d", schedule="* * * * *"),
        ],
    )
    assert cell(window.table, 0, 3).data(STATES_ROLE) == ("running", "pending")
    assert cell(window.table, 1, 3).data(STATES_ROLE) is None
    window.table.viewport().grab()
    kept = window.table.model().index(0, 3)
    assert window.table.itemDelegateForColumn(3).sizeHint(option, kept).width() > 44
    window.close()


def test_a_pod_links_to_its_node_and_controller(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    window._open_list_view("pods")
    pod = PodInfo(
        "ns", "p", "Running", 1, 1, "1d", ("c",), owner=("Deployment", "api"), node="n1"
    )
    window._show_pods(["ns"], [pod, PodInfo("ns", "q", "Pending", 0, 1, "1d", ("c",))])
    ran = []
    monkeypatch.setattr(window, "_run_action", lambda *a, **k: ran.append(a))

    assert cell(window.table, 0, 8).data(LINK_ROLE) == ("Deployment", "ns", "api")
    assert cell(window.table, 0, 9).data(LINK_ROLE) == ("Node", "", "n1")
    assert "Open Node n1" in cell(window.table, 0, 9).toolTip()
    assert cell(window.table, 1, 9).data(LINK_ROLE) is None  # not scheduled yet

    window._open_link(window.table, 0, 9)
    operation, on_success, context, kind, namespace, name = ran[-1]
    assert operation.__name__ == "get_resource_details"
    assert (kind, namespace, name) == ("Node", "", "n1")
    opened = []
    monkeypatch.setattr(window, "_show_json_dialog", lambda *a: opened.append(a))
    on_success({"kind": "Node"})
    assert opened == [("Node: n1", {"kind": "Node"})]

    count = len(ran)
    window._open_link(window.table, 1, 9)  # nothing to open
    window._open_link(window.table, 5, 5)  # no such cell
    assert len(ran) == count

    window._hover_cell(window.table, 0, 9)
    assert window.table.viewport().cursor().shape() == Qt.CursorShape.PointingHandCursor
    window._hover_cell(window.table, 1, 9)
    assert window.table.viewport().cursor().shape() == Qt.CursorShape.ArrowCursor
    window._hover_cell(window.table, 5, 5)
    assert window.table.viewport().cursor().shape() == Qt.CursorShape.ArrowCursor
    window.close()


def test_the_events_link_to_the_resource_they_are_about(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._render_events(_workloads_overview())
    table = window.workloads_table

    assert cell(table, 0, 3).data(LINK_ROLE) == ("Pod", "ns", "api-1")
    assert cell(table, 1, 3).data(LINK_ROLE) == ("Deployment", "ns", "web")
    assert cell(table, 0, 4).data(LINK_ROLE) is None
    window.close()


def test_the_list_on_screen_is_read_again_quietly_while_it_is_looked_at(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    window._open_list_view("pods")
    calls = []
    monkeypatch.setattr(window, "refresh", lambda *a, **k: calls.append(k))

    window._refresh_live()
    assert calls == [{"quiet": True}]

    window._show_page(2)  # Settings: nothing to keep fresh
    window._open_list_view("nodegroups")  # not a list of the namespaces
    window._show_page(1)
    window._refresh_live()
    window._open_list_view("pods")
    window.showMinimized()
    window._refresh_live()
    assert len(calls) == 1
    window.close()


def test_a_quiet_read_leaves_the_status_and_the_spinner_alone(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._open_list_view("pods")
    window._set_status(lambda: "kept")
    FakeRefreshWorker.outcome = ("ok", ([], []))

    window.refresh(quiet=True)

    assert window.status_label.text() != "Loading resources..."
    window.close()


def test_the_selected_row_stays_selected_when_the_rows_change(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    window._open_list_view("pods")

    def pod(name: str) -> PodInfo:
        return PodInfo("ns", name, "Running", 1, 1, "1d", ("c",))

    window._show_pods(["ns"], [pod("a"), pod("b"), pod("c")])
    window.table.selectRow(2)
    assert present(window._selected_pod()).name == "c"

    window._show_answer("pods", ["ns"], [pod("new"), pod("a"), pod("c")])
    assert (
        present(window._selected_pod()).name == "c"
    )  # it moved to row 2, still the one

    window._show_answer("pods", ["ns"], [pod("a"), pod("new")])  # it is gone
    assert window._selected_pod() is None

    window._open_list_view("deployments")
    deployments = [
        Workload("ns", "Deployment", "api", 1, 1, "1d"),
        Workload("ns", "StatefulSet", "api", 1, 1, "1d"),
    ]
    window._show_answer("deployments", ["ns"], deployments)
    window.table.selectRow(1)
    window._show_answer("deployments", ["ns"], deployments[::-1])
    assert (
        present(window._selected_workload()).kind == "StatefulSet"
    )  # kind tells them apart

    window._open_list_view("services")
    row = ClusterResource("ns", "Service", "x", ("a", "b", "c", "d"), "1d")
    window._show_answer("services", [], [row])
    window.table.selectRow(0)
    window._show_answer("services", [], [row])
    assert window._selected_resource() == row
    window.close()
