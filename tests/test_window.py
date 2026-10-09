import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableWidgetItem

from kubescope import window as window_module
from kubescope.models import ClusterOverview, NodeInfo, PodInfo, Workload

application = QApplication.instance() or QApplication([])


def _inline_actions(_self, operation, on_success, *arguments, **_kwargs) -> None:
    """Stand-in for _run_action: only the kubeconfig read runs, and at once, so
    a test sees the contexts right after building the window."""
    if operation is window_module.list_contexts:
        on_success(operation(*arguments))


def test_workload_actions_dispatch_and_follow_visible_selection(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()
    workload = Workload("arquitteh", "Deployment", "api", 1, 1, "1h")
    window._workloads = [workload]
    window.table.setRowCount(1)
    window.table.setItem(0, 0, QTableWidgetItem(workload.name))
    window.table.selectRow(0)

    dispatched = []

    def capture_action(operation, _callback, *arguments) -> None:
        dispatched.append((operation.__name__, arguments))

    monkeypatch.setattr(window, "_run_action", capture_action)
    window.pods_button.click()
    window.details_button.click()
    window.logs_button.click()

    assert [operation for operation, _arguments in dispatched] == [
        "get_workload_pods",
        "get_resource_details",
        "get_workload_pods",
    ]
    assert dispatched[1][1] == ("", "Deployment", "arquitteh", "api")

    window.search_input.setText("no-match")

    assert window.table.isRowHidden(0)
    assert all(
        not button.isEnabled()
        for button in (window.pods_button, window.details_button, window.logs_button)
    )
    window.close()


def _overview() -> ClusterOverview:
    node = NodeInfo(
        name="node-a",
        ready=True,
        roles="worker",
        version="v1.30.0",
        age="3d",
        cpu_allocatable=4.0,
        memory_allocatable=8 * 2**30,
        pods_allocatable=50,
        pods_running=10,
        cpu_requests=3.0,
        memory_requests=2 * 2**30,
    )
    return ClusterOverview(
        nodes=(node,),
        namespaces=4,
        deployments=7,
        statefulsets=1,
        daemonsets=2,
        pods_total=12,
        pods_running=10,
        pods_pending=1,
        pods_failed=1,
    )


def test_overview_page_shows_cluster_totals(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    requested: list = []
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(
        window_module.WorkloadWindow,
        "_run_action",
        lambda _self, _operation, _ok, *args, **_kw: requested.append(args),
    )
    window = window_module.WorkloadWindow()
    window.context_combo.addItem("prod")
    page = window.overview_ui

    window._show_overview("prod", _overview())

    assert window.pages.currentIndex() == 0
    assert page.nodesValue.text() == "1 / 1"
    assert page.podsValue.text() == "10 / 50"
    assert page.cpuValue.text() == "3.0 / 4.0"
    assert page.memValue.text() == "2.0 GiB / 8.0 GiB"
    assert page.cpuBar.value() == 75
    assert page.cpuBar.property("level") == "warn"
    assert page.deploymentsValue.text() == "7"
    assert window.nodes_table.rowCount() == 1
    assert window.nodes_table.item(0, 0).text() == "node-a"
    assert "metrics-server" in page.noticeLabel.text()
    window.close()


def test_navigation_switches_pages_and_loads_overview(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    requested: list = []
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(
        window_module.WorkloadWindow,
        "_run_action",
        lambda _self, operation, _ok, *args, **_kw: (
            requested.append(args)
            if operation.__name__ == "get_cluster_overview"
            else None  # the login check runs too; it has its own tests
        ),
    )
    window = window_module.WorkloadWindow()
    window.context_combo.addItem("prod")
    assert requested == [("prod",)]  # selecting a context loads the overview
    window._overview_context = "prod"
    window._overview_busy = False
    requested.clear()

    window.nav_deployments.click()
    assert window.pages.currentIndex() == 1
    assert window.ui.pageTitle.text() == "Deployments"
    assert requested == []

    window.nav_overview.click()
    assert window.pages.currentIndex() == 0
    assert window.ui.pageTitle.text() == "Overview"
    assert requested == []  # already loaded for this context

    window.context_combo.addItem("staging")
    window.context_combo.setCurrentText("staging")
    assert requested[-1] == ("staging",)
    window.close()


def test_context_aliases_show_in_combo_but_actions_use_real_name(
    monkeypatch, tmp_path
) -> None:
    from kubescope.settings import Settings

    settings = Settings(tmp_path / "settings.json")
    settings.set_context_aliases({"arn:aws:eks:prod": "Production"})
    monkeypatch.setattr(
        window_module,
        "list_contexts",
        lambda: (["arn:aws:eks:prod", "dev"], "dev"),
    )
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(window_module.WorkloadWindow, "_run_action", _inline_actions)

    window = window_module.WorkloadWindow(settings)
    window.context_combo.setCurrentIndex(0)

    assert window.context_combo.itemText(0) == "Production"
    assert window.context_combo.itemText(1) == "dev"
    assert window._context() == "arn:aws:eks:prod"
    window.close()


def test_last_context_is_remembered_and_restored(monkeypatch, tmp_path) -> None:
    from kubescope.settings import Settings

    path = tmp_path / "settings.json"
    monkeypatch.setattr(window_module, "list_contexts", lambda: (["a", "b"], "a"))
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(window_module.WorkloadWindow, "_run_action", _inline_actions)
    first = window_module.WorkloadWindow(Settings(path))
    first.context_combo.setCurrentIndex(1)
    first.close()

    second = window_module.WorkloadWindow(Settings(path))

    assert second._context() == "b"
    second.close()


def test_settings_page_saves_preferences_and_switches_language(
    monkeypatch, tmp_path
) -> None:
    from kubescope import i18n
    from kubescope.settings import Settings

    path = tmp_path / "settings.json"
    monkeypatch.setattr(window_module, "list_contexts", lambda: (["prod"], "prod"))
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(window_module.WorkloadWindow, "_run_action", _inline_actions)
    window = window_module.WorkloadWindow(Settings(path))
    try:
        window.ui.settingsButton.click()
        form = window.settings_ui
        assert window.pages.currentIndex() == 2
        assert window.ui.pageTitle.text() == "Settings"
        assert form.contextsTable.rowCount() == 1

        form.contextsTable.item(0, 1).setText("Prod ✓")
        form.languageCombo.setCurrentIndex(form.languageCombo.findData("pt"))
        form.saveButton.click()
        application.processEvents()  # Qt delivers LanguageChange via the event loop

        assert window.context_combo.itemText(0) == "Prod ✓"
        assert window.ui.pageTitle.text() == "Configurações"
        assert window.nav_overview.text() == "Visão geral"
        saved = Settings(path)
        assert saved.language == "pt"
        assert saved.context_aliases == {"prod": "Prod ✓"}
    finally:
        i18n.apply_language("en")
        window.close()


def test_portuguese_translation_is_bundled() -> None:
    from PySide6.QtCore import QCoreApplication

    from kubescope import i18n

    assert i18n.resolve_language("pt") == "pt"
    assert i18n.resolve_language("xx") in i18n.LANGUAGES
    try:
        assert i18n.apply_language("pt") == "pt"
        assert QCoreApplication.translate("MainWindow", "Refresh") == "Atualizar"
    finally:
        i18n.apply_language("en")
    assert QCoreApplication.translate("MainWindow", "Refresh") == "Refresh"


def test_details_and_logs_open_as_closable_tabs(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()
    assert not window.nav_viewer.isVisibleTo(window)
    assert window.viewer_tabs.count() == 0

    window._show_json_dialog("Deployment: api", {"kind": "Deployment"})
    pod = PodInfo("default", "api-1", "Running", 1, 1, "1d", ("app",))
    window._show_logs_dialog(pod, "app", "line 1\nline 2")

    assert window.pages.currentIndex() == 3
    assert window.nav_viewer.isVisibleTo(window)
    assert window.viewer_tabs.count() == 2
    assert window.viewer_tabs.tabText(0) == "Deployment: api"
    assert window.viewer_tabs.tabText(1) == "Logs: api-1 / app"
    assert window.viewer_tabs.widget(1).ui.logText.toPlainText() == "line 1\nline 2"
    assert window.viewer_tabs.widget(0).isReadOnly()

    window.viewer_tabs.tabCloseRequested.emit(0)
    assert window.viewer_tabs.count() == 1
    assert window.pages.currentIndex() == 3
    window.viewer_tabs.tabCloseRequested.emit(0)
    assert window.viewer_tabs.count() == 0
    assert not window.nav_viewer.isVisibleTo(window)
    assert window.pages.currentIndex() == 1  # back to the workloads list
    window.close()


def test_single_pod_and_container_skip_the_choice_prompts(monkeypatch) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()
    dispatched = []
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda operation, _ok, *args, **_kw: dispatched.append((operation, args)),
    )

    def fail(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("no prompt expected")

    monkeypatch.setattr(window_module.QInputDialog, "getItem", fail)
    pod = PodInfo("default", "api-1", "Running", 1, 1, "1d", ("app",))

    window._choose_pod_for_logs("ctx", [pod])

    assert dispatched[0][0].__name__ == "get_pod_logs"
    assert dispatched[0][1] == ("ctx", "default", "api-1", "app")
    window.close()


def _open_log_tab(monkeypatch):
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    # selecting a context must not start real kubectl workers in tests
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(window_module.WorkloadWindow, "_run_action", _inline_actions)
    window = window_module.WorkloadWindow()
    window.context_combo.addItem("prod")
    window.context_combo.setCurrentIndex(0)
    pod = PodInfo("default", "api-1", "Running", 1, 1, "1d", ("app",))
    window._show_logs_dialog(pod, "app", "line 1")
    return window, window.viewer_tabs.widget(0)


def test_log_tab_refreshes_quietly_with_the_pods_context(monkeypatch) -> None:
    window, tab = _open_log_tab(monkeypatch)
    calls = []
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda operation, ok, *args, **kw: calls.append((operation, ok, args, kw)),
    )

    window._refresh_log(tab, force=True)

    operation, ok, args, kwargs = calls[0]
    assert operation.__name__ == "get_pod_logs"
    assert args == ("prod", "default", "api-1", "app")
    assert kwargs["quiet"] is True  # no busy cursor every few seconds
    assert tab.busy
    window._refresh_log(tab, force=True)  # one request in flight at a time
    assert len(calls) == 1

    ok("line 1\nline 2")
    assert not tab.busy
    assert tab.ui.logText.toPlainText() == "line 1\nline 2"
    assert "Updated at" in tab.ui.logStatus.text()
    window.close()


def test_log_tab_does_not_poll_when_paused_or_hidden(monkeypatch) -> None:
    window, tab = _open_log_tab(monkeypatch)
    calls = []
    monkeypatch.setattr(window, "_run_action", lambda *a, **k: calls.append(a))

    window._refresh_log(tab)  # window is not shown: nothing on screen
    assert calls == []

    window.show()
    tab.ui.autoCheck.setChecked(False)
    window._refresh_log(tab)  # paused by the user
    assert calls == []

    tab.ui.autoCheck.setChecked(True)
    window._refresh_log(tab)
    assert len(calls) == 1

    window.nav_deployments.click()  # another page is visible now
    tab.busy = False
    window._refresh_log(tab)
    assert len(calls) == 1
    window.close()


def test_log_tab_keeps_scroll_position_unless_following_the_end(monkeypatch) -> None:
    window, tab = _open_log_tab(monkeypatch)
    window.resize(900, 500)
    window.show()
    lines = "\n".join(f"line {number}" for number in range(400))
    tab.set_logs(lines)
    scrollbar = tab.ui.logText.verticalScrollBar()
    application.processEvents()
    scrollbar.setValue(scrollbar.maximum())

    tab.set_logs(lines + "\nnew line")
    assert scrollbar.value() == scrollbar.maximum()  # was following the end

    scrollbar.setValue(10)
    tab.set_logs(lines + "\nnew line\nanother")
    assert scrollbar.value() == 10  # user scrolled up: do not jump

    tab.set_error("boom")
    assert "boom" in tab.ui.logStatus.text()
    window.close()


def test_closed_log_tab_ignores_late_results(monkeypatch) -> None:
    window, tab = _open_log_tab(monkeypatch)
    calls = []
    monkeypatch.setattr(window, "_run_action", lambda op, ok, *a, **k: calls.append(ok))
    window._refresh_log(tab, force=True)

    window.viewer_tabs.tabCloseRequested.emit(0)

    assert tab.closed
    calls[0]("late")  # must not touch the deleted tab
    window._refresh_log(tab, force=True)
    assert len(calls) == 1
    window.close()


def test_app_icon_is_published_in_several_sizes() -> None:
    from kubescope.app import ICON_PATH, ICON_SIZES, load_app_icon

    icon = load_app_icon()

    assert ICON_PATH.is_file()
    assert not icon.isNull()
    assert {size.width() for size in icon.availableSizes()} == set(ICON_SIZES)


def test_footer_names_the_company_and_the_license(monkeypatch) -> None:
    from kubescope import i18n

    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()
    try:
        assert "DCO Tecnologia" in window.ui.footerLicense.text()
        assert "MIT License" in window.ui.footerLicense.text()

        i18n.apply_language("pt")
        application.processEvents()
        assert "DCO Tecnologia" in window.ui.footerLicense.text()
        assert "Licença MIT" in window.ui.footerLicense.text()
    finally:
        i18n.apply_language("en")
        window.close()


def _sortable_window(monkeypatch):
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()
    workloads = [
        Workload("b", "Deployment", "api", 3, 3, "1d"),
        Workload("a", "Deployment", "web", 1, 4, "2d"),
        Workload("c", "StatefulSet", "db", 0, 1, "9d"),
    ]
    window._show_workloads(["a", "b", "c"], list(workloads))
    return window


def _column_names(window) -> list[str]:
    return [window.table.item(row, 2).text() for row in range(window.table.rowCount())]


def test_clicking_a_header_sorts_and_clicking_again_reverses(monkeypatch) -> None:
    window = _sortable_window(monkeypatch)
    header = window.table.horizontalHeader()
    assert _column_names(window) == ["api", "web", "db"]  # as returned

    header.sectionClicked.emit(2)  # NAME ascending
    assert _column_names(window) == ["api", "db", "web"]
    assert header.sortIndicatorSection() == 2
    assert header.sortIndicatorOrder() == Qt.SortOrder.AscendingOrder

    header.sectionClicked.emit(2)  # again: descending
    assert _column_names(window) == ["web", "db", "api"]
    assert header.sortIndicatorOrder() == Qt.SortOrder.DescendingOrder

    header.sectionClicked.emit(4)  # STATUS: another column starts ascending
    assert _column_names(window) == ["db", "web", "api"]  # worst first
    assert header.sortIndicatorOrder() == Qt.SortOrder.AscendingOrder
    window.close()


def test_sorting_keeps_the_selection_and_survives_a_refresh(monkeypatch) -> None:
    window = _sortable_window(monkeypatch)
    window.table.selectRow(0)  # "api"
    assert window._selected_workload().name == "api"

    window.table.horizontalHeader().sectionClicked.emit(2)
    window.table.horizontalHeader().sectionClicked.emit(2)  # descending

    assert _column_names(window) == ["web", "db", "api"]
    assert window._selected_workload().name == "api"  # still the same workload
    assert window.table.currentRow() == 2

    fresh = [
        Workload("a", "Deployment", "zeta", 1, 1, "1h"),
        Workload("a", "Deployment", "alpha", 1, 1, "1h"),
    ]
    window._show_workloads(["a"], fresh)
    assert _column_names(window) == ["zeta", "alpha"]  # refresh keeps the order
    window.close()


def test_settings_page_shows_long_context_names_in_full(monkeypatch) -> None:
    arn = "arn:aws:eks:us-east-1:123456789012:cluster/prd-api"
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([arn], arn))
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    monkeypatch.setattr(window_module.WorkloadWindow, "_run_action", _inline_actions)
    window = window_module.WorkloadWindow()

    window.ui.settingsButton.click()
    table = window.settings_ui.contextsTable

    assert table.item(0, 0).text() == arn
    assert table.item(0, 0).toolTip() == arn  # hover shows the whole name
    assert table.textElideMode() == Qt.TextElideMode.ElideMiddle
    header = table.horizontalHeader()
    assert header.sectionResizeMode(0) == header.ResizeMode.Interactive
    window.close()


def test_pods_menu_lists_pods_and_deployments_menu_lists_deployments(
    monkeypatch,
) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    window = window_module.WorkloadWindow()

    window.nav_pods.click()
    assert window.pages.currentIndex() == 1
    assert window.ui.pageTitle.text() == "Pods"
    assert window.table.horizontalHeaderItem(1).text() == "CONTAINERS"
    assert not window.pods_button.isVisibleTo(window)

    pods = [
        PodInfo("default", "web-1", "Running", 1, 1, "2d", ("app",)),
        PodInfo("default", "job-1", "Failed", 0, 2, "1h", ("a", "b")),
    ]
    window._show_pods(["default"], pods)
    assert window.table.rowCount() == 2
    assert window.table.item(0, 2).text() == "web-1"
    assert window.table.item(1, 4).text() == "Failed"

    window.table.selectRow(1)
    assert window._selected_pod().name == "job-1"
    window.table.horizontalHeader().sectionClicked.emit(4)  # worst phase first
    assert window.table.item(0, 2).text() == "job-1"

    window.nav_deployments.click()
    assert window.ui.pageTitle.text() == "Deployments"
    assert window.table.horizontalHeaderItem(1).text() == "KIND"
    assert window.pods_button.isVisibleTo(window)
    window.close()


def test_workloads_menu_slides_open_the_pods_and_deployments_entries(
    monkeypatch,
) -> None:
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()
    assert window.submenu.maximumHeight() == 0

    window.nav_workloads.click()
    animation = window._submenu_animation
    assert animation.endValue() > 0
    animation.setCurrentTime(animation.duration())
    assert window.submenu.maximumHeight() == animation.endValue()

    window.nav_workloads.click()
    assert animation.endValue() == 0
    window.close()


def test_hidden_columns_are_applied_and_saved(monkeypatch, tmp_path) -> None:
    from kubescope.settings import Settings

    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    monkeypatch.setattr(window_module.WorkloadWindow, "refresh", lambda *_a: None)
    path = tmp_path / "settings.json"
    window = window_module.WorkloadWindow(Settings(path))
    assert window.table.columnCount() == 9

    window._set_column_visible(6, False)
    assert window.table.isColumnHidden(6)
    window.close()

    reopened = window_module.WorkloadWindow(Settings(path))
    assert reopened.table.isColumnHidden(6)
    assert not reopened.table.isColumnHidden(5)
    reopened.close()
