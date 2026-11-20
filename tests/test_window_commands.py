"""What the window offers to extensions by name, and what it tells them about
the screen: the commands, the snapshot and the text logs."""

import pytest
from kubescope.sdk.models import PodInfo
from PySide6.QtWidgets import QApplication

from kubescope import window as window_module
from kubescope.settings import Settings
from tests.test_window_flows import _ready_window

POD = PodInfo("ns", "api-1", "Running", 1, 2, "1h", ("app", "sidecar"))


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    yield shown
    shown.close()


class Told:
    """The messages a command reports to the person."""

    def __init__(self, window) -> None:
        self.window = window
        self.messages: list[str] = []

    def __call__(self, name: str, **arguments):
        return self.window.commands.invoke(
            name, report=self.messages.append, **arguments
        )


@pytest.fixture
def run(window):
    return Told(window)


def sync(window, monkeypatch) -> None:
    """Run what is done off the UI thread at once, in the test."""
    monkeypatch.setattr(
        window,
        "_run_action",
        lambda function, done, *a, on_error=None, quiet=False: done(function(*a)),
    )


def test_a_view_only_eks_has_is_refused_elsewhere(window, run) -> None:
    run("open_view", view="nodegroups")

    assert run.messages == ["nodegroups is only in EKS contexts."]


def test_the_pages_are_opened_as_the_person_would(window, run) -> None:
    run("open_page", page="workloads_overview")
    assert window.pages.currentIndex() == 4
    run("open_page", page="settings")
    assert window.pages.currentIndex() == 2
    run("open_page", page="overview")
    assert window.pages.currentIndex() == 0


def test_a_tab_is_found_by_the_words_of_its_title(window, run) -> None:
    window._show_json_dialog("Deployment: api", {"kind": "Deployment"})
    window._show_logs_dialog(POD, "app", "line")
    window._show_page(1)

    run("switch_tab", title="  DEPLOYMENT ")
    assert window.pages.currentIndex() == 3 and window.viewer_tabs.currentIndex() == 0
    run("switch_tab", title="nothing like it")

    assert run.messages == ["There is no open tab nothing like it."]


def test_a_tab_of_another_context_is_not_offered(window, run) -> None:
    window._show_json_dialog("Deployment: api", {"kind": "Deployment"})
    window.context_combo.addItem("other")
    window.context_combo.blockSignals(True)
    window.context_combo.setCurrentText("other")
    window.context_combo.blockSignals(False)

    run("switch_tab", title="Deployment")

    assert window._open_tabs() == [] and len(run.messages) == 1


def logs_of(window, monkeypatch, pods):
    sync(window, monkeypatch)
    shown: list[tuple] = []
    monkeypatch.setattr(
        window_module, "get_pods", lambda context, namespace=None: ([], pods)
    )
    monkeypatch.setattr(
        window_module, "get_pod_logs", lambda *args: f"log of {args[-1]}"
    )
    monkeypatch.setattr(
        window,
        "_show_logs_dialog",
        lambda info, container, text: shown.append((info.name, container, text)),
    )
    return shown


def test_the_logs_of_the_only_main_container_are_opened(
    window, run, monkeypatch
) -> None:
    shown = logs_of(
        window, monkeypatch, [PodInfo("ns", "solo", "Running", 1, 1, "1h", ("app",))]
    )

    run("show_logs", namespace="ns", pod="solo")

    assert shown == [("solo", "app", "log of app")] and run.messages == []


def test_a_pod_with_only_a_setup_container_logs_that_one(
    window, run, monkeypatch
) -> None:
    pod = PodInfo("ns", "job", "Running", 1, 1, "1h", (), init_containers=("migrate",))
    shown = logs_of(window, monkeypatch, [pod])

    run("show_logs", namespace="ns", pod="job")

    assert shown == [("job", "migrate", "log of migrate")]


def test_the_container_asked_for_is_used_and_must_exist(
    window, run, monkeypatch
) -> None:
    shown = logs_of(window, monkeypatch, [POD])

    run("show_logs", namespace="ns", pod="api-1", container="sidecar")
    run("show_logs", namespace="ns", pod="api-1", container="gone")

    assert shown == [("api-1", "sidecar", "log of sidecar")]
    assert run.messages == ["The Pod api-1 has no container gone."]


def test_more_than_one_container_and_none_said_asks_which(
    window, run, monkeypatch
) -> None:
    shown = logs_of(window, monkeypatch, [POD])

    run("show_logs", namespace="ns", pod="api-1")

    assert shown == []
    assert "more than one container (app, sidecar)" in run.messages[0]


def test_a_pod_that_is_not_there_is_said(window, run, monkeypatch) -> None:
    logs_of(window, monkeypatch, [POD])

    run("show_logs", namespace="ns", pod="ghost")

    assert run.messages == ["There is no Pod ghost."]


def test_what_the_list_shows_is_told_in_words(window, monkeypatch) -> None:
    window._show_page(1)
    table = window.table
    window._screen_snapshot()  # an empty list
    table.setRowCount(2)
    table.setColumnCount(2)
    from PySide6.QtWidgets import QTableWidgetItem

    for row, name in enumerate(("api", "web")):
        table.setItem(row, 0, QTableWidgetItem(name))
        table.setItem(row, 1, QTableWidgetItem("Running"))
    table.setColumnHidden(1, False)
    table.setRowHidden(1, True)  # a row the search hides is not shown
    table.selectRow(0)

    text = window._screen_snapshot()

    assert "Rows shown: 1" in text and "web" not in text and "Running" in text


def test_the_text_of_the_open_tab_is_told(window) -> None:
    window._show_logs_dialog(POD, "app", "line one\nline two")
    window._show_json_dialog("Deployment: api", {"kind": "Deployment"})

    on_details = window._screen_snapshot()
    window.viewer_tabs.setCurrentIndex(0)
    on_logs = window._screen_snapshot()

    assert "Deployment" in on_details and "line one" in on_logs
    assert "Open tabs:" in on_logs and "(shown)" in on_logs


def test_the_overviews_are_told_too(window) -> None:
    window._show_page(0)
    assert isinstance(window._screen_snapshot(), str)
    window._show_page(4)
    assert isinstance(window._screen_snapshot(), str)


def test_the_width_the_person_gave_the_menu_is_kept_and_restored(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._keep_sidebar_width(333)
    assert window.settings.sidebar_width == 333
    window._keep_sidebar_width(window_module.SIDEBAR_WIDTH)  # the usual one: none
    assert window.settings.sidebar_width == 0
    window.close()

    settings = Settings()
    settings.sidebar_width = 300
    settings.save()
    again = _ready_window(monkeypatch)
    assert again.settings.sidebar_width == 300  # read at the start
    again.close()


def test_the_button_of_the_header_hides_the_menu_and_it_stays_hidden(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window_module.motion.ENABLED = False  # no slide: the result at once
    button = window.ui.sidebarToggleButton
    assert button.toolTip() == "Hide the side menu"

    button.click()
    assert window.ui.sidebar.isHidden() and window.settings.sidebar_collapsed
    assert button.toolTip() == "Show the side menu"
    window.close()

    again = _ready_window(monkeypatch)  # read at the start
    assert again.ui.sidebar.isHidden()
    assert again.ui.sidebarToggleButton.toolTip() == "Show the side menu"
    again.ui.sidebarToggleButton.click()
    assert not again.ui.sidebar.isHidden() and not again.settings.sidebar_collapsed
    again.close()


def test_the_card_of_a_section_of_the_settings_goes_down_to_the_bottom(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.resize(1200, 800)
    window.show()
    window._show_page(2)
    form = window.settings_ui
    room = form.settingsScroll.viewport().height()

    for section, card in (
        (3, form.shortcutsCard),
        (4, form.integrationsCard),
        (5, form.extensionsCard),
    ):
        window._show_settings_section(section)
        QApplication.processEvents()
        assert card.height() >= room - 30, section  # no gap under the card

    window._show_settings_section(3)  # filled before: not filled twice
    window._show_settings_section(3)
    inner = form.shortcutsCard.layout()
    assert inner is not None
    spacers = [
        index
        for index in range(inner.count())
        if (item := inner.itemAt(index)) is not None and item.spacerItem()
    ]
    assert len(spacers) == 1
    window.close()


def test_the_title_of_a_block_of_the_menu_folds_it_and_it_stays_folded(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window_module.motion.ENABLED = False
    fold = window.monitoring_fold
    assert not fold.body.isHidden()

    fold.toggle()
    assert fold.body.isHidden()
    assert window.settings.folded_sections == ["section:monitoring"]
    window.close()

    again = _ready_window(monkeypatch)  # read at the start
    assert again.monitoring_fold.folded and again.monitoring_fold.body.isHidden()
    again.monitoring_fold.toggle()
    assert again.settings.folded_sections == []
    again.close()


def test_a_screen_reached_by_a_shortcut_unfolds_its_block_without_keeping_it(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window_module.motion.ENABLED = False
    window.monitoring_fold.toggle()
    assert window.monitoring_fold.body.isHidden()

    window._reveal_in_menu(window.nav_forwards)

    assert not window.monitoring_fold.body.isHidden()
    assert window.settings.folded_sections == ["section:monitoring"]  # as it was kept
    window.close()


def test_a_text_log_that_fails_or_whose_tab_closed_is_handled(
    window, monkeypatch
) -> None:
    sync(window, monkeypatch)
    ui = window.extension_host.ui
    assert ui is not None

    def broken() -> str:
        raise RuntimeError("no logs")

    def failed_run(function, done, *a, on_error=None, quiet=False):
        try:
            done(function(*a))
        except Exception as error:
            assert on_error is not None
            on_error(str(error))

    monkeypatch.setattr(window, "_run_action", failed_run)

    ui.open_log("orders", "error.log", broken)
    tab = window.viewer_tabs.currentWidget()

    assert "no logs" in tab.ui.logStatus.text()
    tab.busy = True
    tab.ui.refreshButton.click()  # busy: nothing starts
    tab.busy = False
    tab.closed = True
    tab.ui.refreshButton.click()  # closed: the answer is dropped
    assert tab.busy is False


def test_the_lists_of_the_menu_are_told_to_an_extension(window, run) -> None:
    views = run("views")

    assert ("pods", "Pods") in views
    assert all(label.strip() for _view, label in views)  # a hidden entry has none
    assert len({view for view, _label in views}) == len(views)
