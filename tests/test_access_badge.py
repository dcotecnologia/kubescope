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
    assert window.ui.appFooterLayout.indexOf(window.access_badge) >= 0
    window.close()
