import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel, QWidget

from kubescope.views import assistant_panel
from kubescope.views.assistant_panel import AssistantDock

application = QApplication.instance() or QApplication([])


def _host(width=800, height=600) -> QWidget:
    host = QWidget()
    host.resize(width, height)
    host.show()
    application.processEvents()
    return host


def test_the_button_sits_in_the_corner_and_follows_the_window() -> None:
    host = _host()
    dock = AssistantDock(host)
    size, margin = assistant_panel.BUBBLE, assistant_panel.MARGIN
    bottom = assistant_panel.BOTTOM  # above the footer of the window

    assert dock.bubble.geometry().right() + 1 == 800 - margin
    assert dock.bubble.geometry().bottom() + 1 == 600 - bottom

    host.resize(1000, 700)
    application.processEvents()
    assert dock.bubble.x() == 1000 - size - margin
    assert dock.bubble.y() == 700 - size - bottom
    host.close()


def test_the_panel_opens_above_the_button_and_never_outgrows_the_window() -> None:
    host = _host()
    dock = AssistantDock(host)
    assert not dock.is_open and dock.panel.isHidden()

    dock.open()
    panel = dock.panel.geometry()
    assert dock.is_open and panel.bottom() < dock.bubble.y()
    assert panel.width() == assistant_panel.PANEL.width()
    assert panel.right() + 1 == 800 - assistant_panel.MARGIN

    host.resize(300, 200)
    application.processEvents()
    small = dock.panel.geometry()
    assert small.width() <= 300 - 2 * assistant_panel.MARGIN
    assert small.height() >= 0 and small.x() >= 0

    host.resize(10, 10)  # no room at all: the sizes stop at zero
    application.processEvents()
    assert dock.panel.width() == 0 and dock.panel.height() == 0

    dock.close()
    assert not dock.is_open
    host.close()


def test_the_panel_swaps_the_chat_it_shows_and_can_show_none() -> None:
    host = _host()
    dock = AssistantDock(host)
    first, second = QLabel("one"), QLabel("two")

    dock.panel.show_chat(first)
    assert dock.panel.body.count() == 1
    dock.panel.show_chat(second)
    assert dock.panel.body.count() == 1 and first.parent() is None
    dock.panel.show_chat(None)
    assert dock.panel.body.count() == 0

    dock.retranslate()
    assert dock.panel.clear_button.text() == "Clear history"
    host.close()


def test_the_buttons_of_the_panel_say_so() -> None:
    host = _host()
    dock = AssistantDock(host)
    seen: list[str] = []
    dock.panel.clear_requested.connect(lambda: seen.append("clear"))
    dock.panel.closed.connect(lambda: seen.append("closed"))

    dock.panel.clear_button.click()
    dock.panel.close_button.click()

    assert seen == ["clear", "closed"]
    host.close()


def test_the_button_and_the_panel_take_the_colors_of_the_theme(monkeypatch) -> None:
    from kubescope import theme

    host = _host()
    dock = AssistantDock(host)
    monkeypatch.setattr(theme, "_active", theme.LIGHT_THEME)
    dock.restyle()
    light = (dock.bubble.styleSheet(), dock.panel.styleSheet())

    monkeypatch.setattr(theme, "_active", theme.DARK_THEME)
    dock.restyle()

    assert (dock.bubble.styleSheet(), dock.panel.styleSheet()) != light
    assert theme.themed("#3020a5") in dock.bubble.styleSheet()  # as Save changes
    assert theme.themed("#f7f7fa") in dock.panel.styleSheet()
    host.close()
