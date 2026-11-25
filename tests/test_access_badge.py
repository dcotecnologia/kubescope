from tests.test_window_flows import _ready_window


def test_the_footer_badge_says_read_only_or_the_write_mode(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    monkeypatch.setattr(window, "_save_settings", lambda: None)

    window.settings.write_mode = False
    window._show_access_note()
    assert window.access_badge.text() == "READ-ONLY"
    assert "read-only" in window.access_badge.toolTip().lower()

    window.settings.write_mode = True
    window._show_access_note()
    assert window.access_badge.text() == "WRITE MODE"
    assert "Actions that change the cluster are on" in window.access_badge.toolTip()
    window.close()


def test_the_badge_has_a_padlock_closed_or_open_and_stays_in_the_middle(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window.show()
    badge = window.access_badge

    window.settings.write_mode = False
    window._show_access_note()
    closed = badge.icon.pixmap().toImage()
    window.settings.write_mode = True
    window._show_access_note()
    opened = badge.icon.pixmap().toImage()
    window.resize(1100, 600)

    assert closed != opened  # the shackle is raised in the write mode
    footer = window.ui.appFooter
    assert abs(badge.x() + badge.width() / 2 - footer.width() / 2) <= 1
    window.close()


def test_a_click_on_the_badge_goes_to_the_choice_of_the_access(monkeypatch) -> None:
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest

    window = _ready_window(monkeypatch)
    window.show()
    window._show_page(0)
    assert window.pages.currentIndex() != 2

    QTest.mouseClick(window.access_badge, Qt.MouseButton.LeftButton, pos=QPoint(8, 8))

    assert window.pages.currentIndex() == 2  # the Settings
    check = window.settings_ui.writeModeCheck
    assert check.isVisible() and window.focusWidget() is check
    window.close()
