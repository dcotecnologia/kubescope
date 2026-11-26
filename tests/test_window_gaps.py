import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QPushButton, QTableWidgetItem, QWidget

from kubescope import window as window_module
from kubescope.cluster import KubeProblem
from kubescope.extensions.components import UiComponents
from kubescope.views.row_actions import RowActions
from tests.test_window_flows import _ready_window


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def test_the_clusters_are_checked_once_a_run(window, monkeypatch) -> None:
    asked: list[object] = []
    monkeypatch.setattr(window, "_run_action", lambda *args, **_kw: asked.append(args))
    window._kube_checked = False
    window._run_kube_checks()
    window._run_kube_checks()
    assert len(asked) == 1


def test_a_dismissed_problem_or_a_banner_already_up_is_left_alone(
    window, monkeypatch
) -> None:
    monkeypatch.setattr(window, "_save_settings", lambda: None)
    problem = KubeProblem("login_missing", "aws", ("prod",))
    window.settings.dismiss_check(problem.key)
    window.error_banner.dismiss()
    window._show_kube_problems([problem])  # dismissed: nothing is shown
    assert window.error_banner.frame.isHidden()

    other = KubeProblem("login_missing", "az", ("blue",))
    window.error_banner.show_error("Something else failed", "details")
    window._show_kube_problems([other])  # another banner is up: it stays
    assert window.error_banner.label.text() == "Something else failed"


def test_the_cards_rise_once_for_a_cluster(window, monkeypatch) -> None:
    rose: list[int] = []
    monkeypatch.setattr(
        window_module.motion, "slide_up", lambda *_a, **_k: rose.append(1)
    )
    window._cards_risen_for = ""
    window._rise_overview_cards("prod")
    first = len(rose)
    window._rise_overview_cards("prod")  # the same cluster: they stay
    assert first == 8 and len(rose) == first


def test_a_saved_width_of_the_name_column_keeps_it_from_being_fitted(window) -> None:
    window._open_list_view("pods")
    window.settings.set_column_width("pods", 2, 300)
    window._name_fitted.discard("pods")
    window._apply_saved_widths()
    assert "pods" in window._name_fitted and window.table.columnWidth(2) == 300


def test_one_section_alone_is_not_a_joined_bar(window, monkeypatch) -> None:
    only = window.settings_ui.generalSectionButton
    monkeypatch.setattr(window._settings_sections, "buttons", lambda: [only])
    window._join_section_tabs()
    assert only.property("segment") == ""


def test_only_the_buttons_of_the_menu_count_for_its_width(window) -> None:
    window.settings.sidebar_width = 0
    stray = QPushButton("A button that is not an entry of the menu " * 4)
    stray.setParent(window.ui.sidebarNav)  # no "nav" property
    assert window._menu_width() <= window_module.SIDEBAR_MAX
    needed = window._menu_width()
    stray.setProperty("nav", "true")
    assert window._menu_width() >= needed  # it counts only once it is an entry
    stray.deleteLater()


def test_the_extensions_get_the_keys_and_the_icons_of_the_rows(window) -> None:
    keys = window._row_keys()
    assert set(keys) == {"row_details", "row_details_alt", "row_delete"}

    components = UiComponents(row_keys=window._row_keys)
    table = components.data_table(["NAME"], (100,))
    table.setRowCount(1)
    table.setItem(0, 0, QTableWidgetItem("a"))
    components.page(QWidget(window), body=table)  # a page in the window
    actions = table.findChildren(RowActions)[0]
    window.settings.shortcuts = {**window.settings.shortcuts, "row_details": "Ctrl+J"}
    window._apply_row_keys()
    assert actions._keys["row_details"].key().toString() == "Ctrl+J"

    icons = window._menu_icons()
    assert window.details_button.text() in icons
    assert not icons[window.details_button.text()].isNull()


def test_the_search_goes_to_a_page_of_an_extension_that_runs(
    window, monkeypatch
) -> None:
    key = "extension:x/Plugins/Plugins/Installed"
    entry_button = QPushButton("Installed")
    opened: list[str] = []
    monkeypatch.setattr(window.extension_pages, "button_for", lambda _key: entry_button)
    monkeypatch.setattr(window.extension_pages, "open_key", opened.append)

    entry = window._screen_entry(key, "Recent")
    assert entry is not None and entry.label == "Installed" and entry.first
    entry.run()
    assert opened == [key]
