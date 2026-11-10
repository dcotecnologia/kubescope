from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QKeySequenceEdit

from kubescope import window as window_module
from kubescope.models import SearchHit
from kubescope.utils import shortcuts
from kubescope.utils.timezone import set_timezone
from tests.test_window_flows import _ready_window


def _edit(window, action: str) -> QKeySequenceEdit:
    table = window.settings_ui.shortcutsTable
    for row in range(table.rowCount()):
        if table.item(row, 0).data(window_module.Qt.ItemDataRole.UserRole) == action:
            return table.cellWidget(row, 1)
    raise AssertionError(action)


def test_the_shortcuts_go_to_their_screens(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
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


def test_the_filter_and_the_cluster_switch_take_the_focus(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    popups = []
    monkeypatch.setattr(window.context_combo, "showPopup", lambda: popups.append(1))
    window.show()

    window.pages.setCurrentIndex(0)
    window._shortcuts["filter"].activated.emit()
    assert window.pages.currentIndex() == 1  # it goes to the list first
    window._shortcuts["filter"].activated.emit()  # already there

    window._shortcuts["context"].activated.emit()
    assert popups == [1]


def test_the_shortcuts_are_edited_saved_and_applied(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    assert _edit(window, "search").keySequence().toString() == "/"

    _edit(window, "search").setKeySequence(QKeySequence("Ctrl+P"))
    window._save_preferences()

    assert window.settings.shortcuts["search"] == "Ctrl+P"
    assert window._shortcuts["search"].key().toString() == "Ctrl+P"

    window.settings_ui.shortcutsResetButton.click()  # back to the defaults
    assert _edit(window, "search").keySequence().toString() == "/"


def test_two_actions_cannot_share_a_key(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    _edit(window, "pods").setKeySequence(QKeySequence("Ctrl+G"))

    window._save_preferences()

    assert "Ctrl+G" in window.settings_ui.noticeLabel.text()
    assert window.settings.shortcuts == shortcuts.DEFAULTS  # nothing was saved


def test_a_zone_that_is_typed_wrong_goes_back_to_the_chosen_one(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
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


def test_the_search_lists_the_screens_and_opens_the_resource_found(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    opened = []
    monkeypatch.setattr(window, "_open_resource", lambda *args: opened.append(args))
    monkeypatch.setattr(
        window_module,
        "search_resources",
        lambda _context: [SearchHit("Pod", "ns", "api")],
    )
    window._nav_views["pods"].setText("")  # an entry with no label is left out

    window._open_global_search()
    dialog = window._global_search
    assert dialog is not None
    labels = [dialog.results.item(row).text() for row in range(dialog.results.count())]
    assert any(label.startswith("Settings") for label in labels)
    assert not any(label.startswith("Pods") for label in labels)

    window._open_global_search()  # a second time reuses the dialog
    assert window._global_search is dialog
    from tests.test_window_flows import _wait_until

    _wait_until(lambda: dialog.note.text() == "")
    dialog.input.setText("api")
    dialog.results.setCurrentRow(0)
    dialog._choose(dialog.results.item(0))
    assert opened == [("Pod", "ns", "api")]

    for row, view in ((0, 0), (1, 4), (2, 2)):  # the screens that are not lists
        dialog.input.clear()
        dialog.results.item(row).data(window_module.Qt.ItemDataRole.UserRole).run()
        assert window.pages.currentIndex() == view


def test_the_search_without_a_cluster_says_nothing_and_does_not_ask(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.context_combo.clear()
    asked = []
    monkeypatch.setattr(window, "_run_action", lambda *args, **kw: asked.append(args))

    window._open_global_search()
    assert asked == []

    window._close_when_worker_stops = True
    window._global_search = None
    window._open_global_search()  # closing: it does not open
    assert window._global_search is None


def test_a_screen_reached_by_a_shortcut_opens_its_section_of_the_menu(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    submenu = window.network_submenu
    submenu.setMaximumHeight(0)  # the section is closed
    window.settings.menu_collapsed = ["network"]

    window._open_list_view("services")

    assert submenu.maximumHeight() != 0 or window._submenus[submenu].endValue() > 0
    assert window.settings.menu_collapsed == ["network"]  # not kept: it only reveals

    window._reveal_in_menu(window.ui.settingsButton)  # no section holds it
    window._show_page(4)  # the workloads overview has its own entry
