import pytest
from PySide6.QtCore import QUrl
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

from kubescope import window as window_module
from kubescope.settings import Settings
from kubescope.utils.updates import Release, UpdateCheck
from tests.test_window_flows import _ready_window


@pytest.fixture(autouse=True)
def quit_on_last_window_closed():
    yield
    QApplication.setQuitOnLastWindowClosed(True)


def _with_tray(monkeypatch, available: bool = True):
    monkeypatch.setattr(
        QSystemTrayIcon, "isSystemTrayAvailable", staticmethod(lambda: available)
    )
    window = _ready_window(monkeypatch)
    window.settings.run_in_background = True
    return window


def test_running_in_the_background_is_on_by_default_and_only_false_turns_it_off(
    tmp_path,
) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.run_in_background is True

    settings.run_in_background = False
    settings.save()
    assert Settings(path).run_in_background is False

    for stored in ('"no"', "0", "null"):
        path.write_text(f'{{"run_in_background": {stored}}}', encoding="utf-8")
        assert Settings(path).run_in_background is True


def test_the_tray_icon_follows_the_setting(monkeypatch) -> None:
    monkeypatch.setattr(
        QSystemTrayIcon, "isSystemTrayAvailable", staticmethod(lambda: True)
    )
    window = _ready_window(monkeypatch)
    window._load_settings_form()
    assert window.settings_ui.backgroundCheck.isChecked() is True
    assert window._tray is not None  # on by default

    window.settings_ui.backgroundCheck.setChecked(False)
    window._save_preferences()
    assert window._tray is None
    assert window.settings.run_in_background is False

    window.settings_ui.backgroundCheck.setChecked(True)
    window._save_preferences()
    assert window._tray is not None
    window.close()


def test_without_a_system_tray_the_window_still_closes_for_real(monkeypatch) -> None:
    window = _with_tray(monkeypatch, available=False)

    window._sync_tray()

    assert window._tray is None
    event = QCloseEvent()
    window.closeEvent(event)
    assert event.isAccepted()


def test_closing_the_window_hides_it_into_the_tray(monkeypatch) -> None:
    window = _with_tray(monkeypatch)
    window._sync_tray()
    window._sync_tray()  # already shown: nothing is added twice
    window.show()
    assert not QApplication.quitOnLastWindowClosed()

    event = QCloseEvent()
    window.closeEvent(event)

    assert not event.isAccepted()
    assert not window.isVisible()
    window._quit()


def test_the_tray_icon_brings_the_window_back_and_hides_it(monkeypatch) -> None:
    window = _with_tray(monkeypatch)
    window._sync_tray()
    trigger = QSystemTrayIcon.ActivationReason.Trigger
    window.show()

    window._tray_activated(trigger)
    assert not window.isVisible()
    window._tray_activated(trigger)
    assert window.isVisible()
    window._tray_activated(QSystemTrayIcon.ActivationReason.Context)
    assert window.isVisible()  # only a plain click toggles it
    window._quit()


def test_quit_in_the_tray_menu_closes_for_real(monkeypatch) -> None:
    window = _with_tray(monkeypatch)
    window._sync_tray()
    window.show()
    assert window._tray is not None
    actions = window._tray.contextMenu().actions()
    assert [action.text() for action in actions if not action.isSeparator()] == [
        "Show KubeScope",
        "About KubeScope",
        "Preferences",
        "Check for updates",
        "Quit",
    ]

    actions[0].trigger()
    actions[-1].trigger()

    assert QApplication.quitOnLastWindowClosed()
    assert not window.isVisible()


def test_the_tray_menu_opens_the_preferences_and_checks_for_updates(
    monkeypatch,
) -> None:
    window = _with_tray(monkeypatch)
    checked = []
    monkeypatch.setattr(window, "check_updates", lambda: checked.append(True))
    window.show()
    window.hide()

    window._show_preferences()
    assert window.isVisible()
    assert window.pages.currentIndex() == 2

    window.hide()
    window._check_updates_from_tray()
    assert window.isVisible()
    assert checked == [True]
    window.close()


def test_about_gives_the_legal_details_and_opens_what_is_asked(monkeypatch) -> None:
    window = _with_tray(monkeypatch)
    opened = []
    monkeypatch.setattr(
        window_module.QDesktopServices, "openUrl", lambda url: opened.append(url)
    )
    seen = []

    class FakeBox(QMessageBox):
        label = ""

        def exec(self) -> int:
            seen.append((self.text(), self.informativeText()))
            self._pressed = {b.text(): b for b in self.buttons()}[FakeBox.label]
            return 0

        def clickedButton(self):
            return self._pressed

    monkeypatch.setattr(window_module, "QMessageBox", FakeBox)

    for label in ("Open on GitHub", "License", "Third-party notices", "Close"):
        FakeBox.label = label
        window._show_about()

    title, details = seen[0]
    assert title == f"KubeScope {window_module.__version__}"
    for text in ("Copyright © 2026 DCO Tecnologia", "MIT License", "without warranty"):
        assert text in details
    for text in ("LGPL-3.0", "registered trademark of The Linux Foundation"):
        assert text in details
    assert [url.toString() for url in opened] == [
        window_module.PROJECT_URL,
        window_module.LICENSE_URL,
        QUrl.fromLocalFile(str(window_module.NOTICES_PATH)).toString(),
    ]
    assert window_module.NOTICES_PATH.is_file()
    window.close()


def _answer(window, status, release=None):
    window._update_result = UpdateCheck(status, release)
    window._update_checked()


def test_a_new_version_is_notified_through_the_tray(monkeypatch) -> None:
    window = _with_tray(monkeypatch)
    window._sync_tray()
    shown = []
    monkeypatch.setattr(window._tray, "showMessage", lambda *a: shown.append(a[1]))
    saved = []
    monkeypatch.setattr(window, "_save_settings", lambda: saved.append(True))
    release = Release("9.9.9", "https://example.test")

    for _ in range(2):  # the hourly check, twice the same day
        window._rechecking = True
        _answer(window, "available", release)

    assert shown == ["Version 9.9.9 is available"]
    assert saved == [True]
    window.settings.last_update_notice = "2000-01-01"
    window._rechecking = True
    _answer(window, "available", release)
    assert len(shown) == 2
    _answer(window, "available", release)  # a check the person asked for
    _answer(window, "available", release)
    assert len(shown) == 4
    window.close()


def test_there_is_no_notification_without_a_tray(monkeypatch) -> None:
    window = _with_tray(monkeypatch, available=False)
    window._sync_tray()

    for rechecking in (True, False):
        window._rechecking = rechecking
        _answer(window, "available", Release("9.9.9", "https://example.test"))

    assert window.settings.last_update_notice == ""
    window.close()


def test_the_hourly_check_runs_quietly_and_only_when_allowed(monkeypatch) -> None:
    window = _with_tray(monkeypatch)
    checked = []
    monkeypatch.setattr(window, "check_updates", lambda: checked.append(True))

    window.settings.check_updates = False
    window._recheck_updates()
    assert checked == []

    window.settings.check_updates = True
    window._recheck_updates()
    assert checked == [True]
    _answer(window, "current")
    assert window.ui.updateNotice.isHidden()  # "Up to date" is for a click
    window._update_state = "checking"
    window._recheck_updates()
    assert checked == [True]
    assert window._update_recheck.interval() == 60 * 60 * 1000
    window.close()


def test_the_last_update_notice_keeps_a_day_and_ignores_anything_else(
    tmp_path,
) -> None:
    path = tmp_path / "settings.json"
    settings = Settings(path)
    assert settings.last_update_notice == ""

    settings.last_update_notice = "2026-10-20"
    settings.save()
    assert Settings(path).last_update_notice == "2026-10-20"

    path.write_text('{"last_update_notice": 5}', encoding="utf-8")
    assert Settings(path).last_update_notice == ""
