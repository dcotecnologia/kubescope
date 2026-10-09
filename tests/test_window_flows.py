import os
import threading
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QObject, QPoint, QTimer, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QInputDialog,
    QMenu,
    QMessageBox,
    QPushButton,
    QTableWidget,
)

from kubescope import window as window_module
from kubescope.cluster import KubectlError, LoginAction
from kubescope.models import (
    ClusterOverview,
    EventInfo,
    KindSummary,
    NodeInfo,
    PodInfo,
    Workload,
    WorkloadsOverview,
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

    def isRunning(self) -> bool:  # noqa: N802
        return self.running

    def start(self) -> None:
        kind, payload = self.outcome
        if kind == "ok":
            self.completed.emit(*payload)
        else:
            self.failed.emit(payload)
        self.finished.emit()


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
        raise KubectlError("no metrics")

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
        raise KubectlError("denied")

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
        raise KubectlError("nope")

    failing = window_module.ActionWorker(broken, ())
    failing.failed.connect(failures.append)
    failing.run()
    assert failures == ["nope"]


def test_loading_spins_the_button_and_leaves_the_cursor_alone(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._tick_spinner()  # nothing to animate yet
    primary, secondary = window.refresh_button, window.details_button
    original = primary.text()

    end = window._begin_loading(primary, "Wait")
    nested = window._begin_loading(secondary, "Other")
    window._begin_loading(None, "ignored")
    assert QApplication.overrideCursor() is None  # never a busy cursor
    assert primary.text() == "Wait"
    assert secondary.text() != "Other"  # only one spinner at a time

    window._spinner_button = secondary
    window._tick_spinner()
    window._spinner_button = primary
    end()
    end()  # a second call changes nothing
    assert primary.text() == original
    nested()
    window._end_loading(None)
    assert QApplication.overrideCursor() is None
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
    assert window._worker is None

    window.context_combo.addItem("prod")
    running = FakeRefreshWorker("prod", None)
    running.running = True
    window._worker = running
    window.refresh()
    assert window._worker is running
    window.close()


def test_refresh_requeues_when_the_view_changed_mid_request(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    queued = []
    monkeypatch.setattr(
        QTimer, "singleShot", staticmethod(lambda *args: queued.append(args))
    )
    window._worker = FakeRefreshWorker("prod", None, "pods")
    window._view = "deployments"

    window._refresh_finished()

    assert queued and window.refresh_button.isEnabled()
    window.close()


def test_actions_run_in_workers_and_report_back(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    results, errors = [], []

    window._run_action(lambda: "ok", results.append)
    _wait_until(lambda: results and not window._action_workers)
    window._run_action(lambda: "quiet", results.append, quiet=True)
    _wait_until(lambda: len(results) == 2 and not window._action_workers)

    def broken():
        raise KubectlError("denied")

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
    window._worker = running

    event = QCloseEvent()
    window.closeEvent(event)
    assert not event.isAccepted() and window._close_when_worker_stops
    assert not window.isVisible()  # closing feels instant
    assert cancelled == [True]
    assert QApplication.quitOnLastWindowClosed() is False

    window._worker = None
    window._action_workers = [running]
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
    monkeypatch.setattr(
        QMessageBox, "information", staticmethod(lambda *a: messages.append(a[2]))
    )
    monkeypatch.setattr(
        window, "_run_action", lambda op, _ok, *a, **_k: dispatched.append(a)
    )
    other = PodInfo("ns", "api-2", "Running", 1, 1, "1h", ("app",))
    empty = PodInfo("ns", "bare", "Running", 0, 0, "1h", ())
    answers = iter([("api-2", True), ("api-1", False), ("sidecar", True)])
    monkeypatch.setattr(
        QInputDialog, "getItem", staticmethod(lambda *_a: next(answers))
    )

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
        raise KubectlError("Unable to read kubeconfig")

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
        def exec(self, *_args) -> None:
            actions = self.actions()
            assert actions[2].isEnabled() is False
            actions[0].toggle()

    monkeypatch.setattr(window_module, "QMenu", FakeMenu)

    window._show_column_menu(QPoint(0, 0))

    assert window.table.isColumnHidden(0)
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
    tab = window.viewer_tabs.widget(0)
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
        raise KubectlError("Error loading SSO Token: Token does not exist")

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
    assert [table.item(row, 4).text() for row in range(4)] == [
        "Complete",
        "Failed",
        "Running",
        "Pending",
    ]
    assert table.item(0, 3).text() == "3/3"
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
    assert [table.item(row, 3).text() for row in range(3)] == [
        "0 3 * * *",
        "@daily",
        "* * * * *",
    ]
    assert [table.item(row, 4).text() for row in range(3)] == [
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


def test_an_answer_for_a_view_the_person_left_is_dropped(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    late = []
    monkeypatch.setattr(window, "_show_workloads", lambda *a: late.append(a))
    FakeRefreshWorker.outcome = (
        "ok",
        (["ns"], [Workload("ns", "Deployment", "api", 1, 1, "1d")]),
    )
    window._open_list_view("pods")  # changes the view before refresh() runs

    window.refresh()
    assert window._worker.view == "pods"

    window._view = "deployments"
    window._worker.completed.emit(["ns"], [])  # the pods request answers late
    assert late == []
    FakeRefreshWorker.outcome = ("ok", ([], []))
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
    assert layout.indexOf(window.nav_pods) == 1
    assert window.nav_workloads_overview.text() == "Overview"
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
    assert [table.item(0, c).text() for c in range(8)] == [
        "Warning",
        "kubelet",
        "ns",
        "Pod: api-1",
        "Back-off",
        "12",
        "2h",
        "5m",
    ]
    assert table.item(0, 4).toolTip() == "Back-off"
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
        (page.jobsLink, "jobs"),
        (page.cronjobsLink, "cronjobs"),
    ):
        link.click()
        assert window._view == view and window.pages.currentIndex() == 1

    assert not page.daemonsetsLink.isEnabled()  # counted, but there is no list
    assert not page.replicasetsLink.isEnabled()
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
