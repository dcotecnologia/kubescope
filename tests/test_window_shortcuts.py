import pytest
from kubescope.sdk.timezone import set_timezone
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QKeySequenceEdit

from kubescope import window as window_module
from kubescope.utils import shortcuts
from tests.test_window_flows import _ready_window


@pytest.fixture
def window(monkeypatch):
    """A window that is closed afterwards, so no worker outlives the test."""
    shown = _ready_window(monkeypatch)
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def _edit(window, action: str) -> QKeySequenceEdit:
    table = window.settings_ui.shortcutsTable
    for row in range(table.rowCount()):
        if table.item(row, 0).data(window_module.Qt.ItemDataRole.UserRole) == action:
            return table.cellWidget(row, 1)
    raise AssertionError(action)


def test_the_shortcuts_go_to_their_screens(window, monkeypatch) -> None:
    monkeypatch.setattr(window, "_open_list_view", lambda view: opened.append(view))
    opened: list[str] = []

    for action in ("pods", "deployments", "services"):
        window._shortcuts[action].activated.emit()
    assert opened == ["pods", "deployments", "services"]

    window._shortcuts["settings"].activated.emit()
    assert window.pages.currentIndex() == 2
    window._shortcuts["overview"].activated.emit()
    assert window.pages.currentIndex() == 0

    window._shortcuts["help"].activated.emit()  # the cheat sheet is the settings
    assert window.pages.currentIndex() == 2
    assert window.settings_ui.shortcutsCard.isVisibleTo(
        window.settings_ui.settingsContent
    )


def test_the_filter_and_the_cluster_switch_take_the_focus(window, monkeypatch) -> None:
    popups = []
    monkeypatch.setattr(window.context_combo, "showPopup", lambda: popups.append(1))
    window.show()

    window.pages.setCurrentIndex(0)
    window._shortcuts["filter"].activated.emit()
    assert window.pages.currentIndex() == 1  # it goes to the list first
    window._shortcuts["filter"].activated.emit()  # already there

    window._shortcuts["context"].activated.emit()
    assert popups == [1]


def test_the_shortcuts_are_edited_saved_and_applied(window, monkeypatch) -> None:
    window._load_settings_form()
    assert _edit(window, "overview").keySequence().toString() == "G, O"

    _edit(window, "overview").setKeySequence(QKeySequence("Ctrl+P"))
    window._save_preferences()

    assert window.settings.shortcuts["overview"] == "Ctrl+P"
    assert window._shortcuts["overview"].key().toString() == "Ctrl+P"

    window.settings_ui.shortcutsResetButton.click()  # back to the defaults
    assert _edit(window, "overview").keySequence().toString() == "G, O"


def test_two_actions_cannot_share_a_key(window, monkeypatch) -> None:
    window._load_settings_form()
    _edit(window, "pods").setKeySequence(QKeySequence("Ctrl+R"))

    window._save_preferences()

    assert "Ctrl+R" in window.settings_ui.noticeLabel.text()
    assert window.settings.shortcuts == shortcuts.DEFAULTS  # nothing was saved


def test_a_zone_that_is_typed_wrong_goes_back_to_the_chosen_one(
    window, monkeypatch
) -> None:
    window._load_settings_form()
    combo = window.settings_ui.timezoneCombo
    line = combo.lineEdit()
    assert line is not None

    line.setText("Asia/Tokyo")
    line.editingFinished.emit()
    assert combo.currentData() == "Asia/Tokyo"

    line.setText("not a zone")
    line.editingFinished.emit()
    assert combo.currentData() == "Asia/Tokyo"
    assert line.text() == "Asia/Tokyo"

    window.settings_ui.timezoneCombo.setCurrentIndex(0)  # local time
    window._save_preferences()
    assert window.settings.timezone == "auto"
    set_timezone("auto")


def test_a_screen_reached_by_a_shortcut_opens_its_section_of_the_menu(
    window, monkeypatch
) -> None:
    window.show()
    submenu = window.network_submenu
    submenu.setMaximumHeight(0)  # the section is closed
    window.settings.menu_collapsed = ["network"]

    window._open_list_view("services")

    assert submenu.maximumHeight() != 0 or window._submenus[submenu].endValue() > 0
    assert window.settings.menu_collapsed == ["network"]  # not kept: it only reveals

    window._reveal_in_menu(window.ui.settingsButton)  # no section holds it
    window._show_page(4)  # the workloads overview has its own entry
