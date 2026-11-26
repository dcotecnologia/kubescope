import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from kubescope import window as window_module
from tests.test_window_flows import _ready_window

KEY = "extension:kubescope.plugins/Plugins/Plugins/Installed"


@pytest.fixture
def window(monkeypatch):
    shown = _ready_window(monkeypatch)
    yield shown
    shown._close_when_worker_stops = False
    shown.close()


def test_the_page_of_an_extension_is_remembered_as_the_screen(
    window, monkeypatch
) -> None:
    window.settings.remember_last_context = True
    monkeypatch.setattr(window.extension_pages, "current_key", lambda: KEY)
    window.pages.setCurrentIndex(5)  # a page that is not one of the app's own
    window._remember_screen()
    assert window.settings.last_screen == (window_module.EXTENSION_SCREEN, KEY)

    monkeypatch.setattr(window.extension_pages, "current_key", lambda: "")
    window._remember_screen()  # none of the extensions: nothing is written
    assert window.settings.last_screen == (window_module.EXTENSION_SCREEN, KEY)

    window.settings.remember_last_context = False
    window.settings.last_screen = (0, "")
    monkeypatch.setattr(window.extension_pages, "current_key", lambda: KEY)
    window._remember_screen()
    assert window.settings.last_screen == (0, "")  # the person asked not to


def test_the_app_opens_on_the_page_of_an_extension_when_it_is_there(
    window, monkeypatch
) -> None:
    window.settings.remember_last_context = True
    window.settings.last_screen = (window_module.EXTENSION_SCREEN, KEY)
    opened: list[str] = []
    present: list[object] = []
    monkeypatch.setattr(
        window.extension_pages,
        "button_for",
        lambda key: present[0] if present else None,
    )
    monkeypatch.setattr(window.extension_pages, "open_key", opened.append)

    window._restore_screen()  # the extension has not put its page in the menu yet
    assert opened == [] and window._pending_screen == KEY

    present.append(object())  # it runs now
    window._open_pending_screen()
    assert opened == [KEY] and window._pending_screen == ""
    window._open_pending_screen()  # once only
    assert opened == [KEY]
