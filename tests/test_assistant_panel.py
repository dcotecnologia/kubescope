import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QApplication, QLabel, QWidget

from kubescope.views import assistant_panel
from kubescope.views.assistant_panel import AssistantDock

application = QApplication.instance() or QApplication([])


@pytest.fixture(autouse=True)
def no_slide(monkeypatch):
    """The panel appears and goes at once, but in the test of the slide."""
    monkeypatch.setattr(assistant_panel, "ANIMATION_MS", 0)


_HOSTS: list[QWidget] = []


@pytest.fixture(autouse=True)
def clear_hosts():
    """Hosts and their docks live until the test ends, then go together."""
    yield
    for host in _HOSTS:
        host.close()
        host.deleteLater()
    _HOSTS.clear()
    application.sendPostedEvents(None, QEvent.Type.DeferredDelete)


def _host(width=800, height=600) -> QWidget:
    host = QWidget()
    _HOSTS.append(host)
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


def test_the_panel_opens_over_the_button_and_never_outgrows_the_window() -> None:
    host = _host()
    dock = AssistantDock(host)
    assert not dock.is_open and dock.panel.isHidden()

    dock.open()
    panel = dock.panel.geometry()
    assert dock.is_open and panel.bottom() + 1 == dock.bubble.geometry().bottom() + 1
    assert panel.contains(dock.bubble.geometry())  # it covers the button
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


def test_the_panel_slides_up_to_open_and_down_to_close(monkeypatch) -> None:
    monkeypatch.setattr(assistant_panel, "ANIMATION_MS", 120)
    host = _host()
    dock = AssistantDock(host)

    dock.open()
    assert dock.is_open and not dock.panel.isHidden()
    start = dock.panel.y()
    assert start > dock._target().y()  # it starts below its place
    assert dock.panel.graphicsEffect() is not None  # and fades in
    _wait(lambda: dock.panel.graphicsEffect() is None)
    assert dock.panel.geometry() == dock._target()

    dock.close()
    assert not dock.is_open and not dock.panel.isHidden()  # still sliding down
    _wait(lambda: dock.panel.isHidden())
    assert dock.panel.graphicsEffect() is None

    dock.close()  # already away: nothing to do
    dock.open()
    dock.close()  # put away before it arrived
    _wait(lambda: dock.panel.isHidden())
    assert not dock.is_open
    host.close()


def test_resizing_while_open_keeps_the_panel_over_the_button() -> None:
    host = _host()
    dock = AssistantDock(host)
    dock.open()

    host.resize(1000, 700)
    application.processEvents()

    assert dock.panel.geometry() == dock._target()
    assert dock.panel.geometry().contains(dock.bubble.geometry())
    host.close()


def _wait(condition, seconds: float = 3.0) -> None:
    import time

    deadline = time.monotonic() + seconds
    while not condition() and time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.005)
    assert condition()


def _press(handle, x: int, y: int) -> None:
    from PySide6.QtCore import QEvent, QPointF, Qt
    from PySide6.QtGui import QMouseEvent

    event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPointF(1, 1),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    handle.mousePressEvent(event)


def _drag(handle, x: int, y: int, kind: str = "move") -> None:
    from PySide6.QtCore import QEvent, QPointF, Qt
    from PySide6.QtGui import QMouseEvent

    types = {
        "move": QEvent.Type.MouseMove,
        "release": QEvent.Type.MouseButtonRelease,
    }
    event = QMouseEvent(
        types[kind],
        QPointF(1, 1),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    if kind == "move":
        handle.mouseMoveEvent(event)
    else:
        handle.mouseReleaseEvent(event)


def test_the_borders_of_the_panel_are_dragged_to_resize_it() -> None:
    host = _host(1000, 800)
    dock = AssistantDock(host)
    dock.open()
    states: list[int] = []
    dock.state_changed.connect(lambda: states.append(1))
    left, top, corner = dock.panel.handles
    before = dock.panel.geometry()

    _drag(left, 500, 500)  # a move with no press does nothing
    _press(left, 500, 500)
    _drag(left, 400, 500)  # 100 to the left: wider
    assert dock.panel.width() == before.width() + 100
    assert dock.panel.height() == before.height()
    assert dock.panel.geometry().right() == before.right()  # the corner stays
    _drag(left, 400, 500, "release")
    assert states == [1]

    _press(top, 500, 500)
    _drag(top, 500, 450)  # 50 up: taller
    assert dock.panel.height() == before.height() + 50
    _drag(top, 500, 450, "release")

    _press(corner, 500, 500)
    _drag(corner, 0, 0)  # as far as it goes: the window limits it
    room = dock._room()
    assert dock.panel.width() == room.width() and dock.panel.height() == room.height()
    _drag(corner, 900, 900)  # the other way: not smaller than the least
    assert dock.panel.width() == assistant_panel.MIN_PANEL.width()
    assert dock.panel.height() == assistant_panel.MIN_PANEL.height()
    _drag(corner, 900, 900, "release")
    _drag(corner, 0, 0, "release")  # nothing pressed: nothing happens
    host.close()


def test_the_size_chosen_is_kept_when_the_window_shrinks_and_grows() -> None:
    host = _host(1000, 800)
    dock = AssistantDock(host)
    dock.open()
    dock.panel.dragged.emit(-100, -80)
    chosen = dock.panel.size()

    host.resize(500, 450)
    application.processEvents()
    assert dock.panel.width() < chosen.width()  # the window has less room

    host.resize(1000, 800)
    application.processEvents()
    assert dock.panel.size() == chosen  # and the choice is back with the room
    host.close()


def test_the_panel_leaves_the_window_for_one_of_its_own_and_comes_back() -> None:
    host = _host(1000, 800)
    dock = AssistantDock(host)
    saved: list[dict] = []
    dock.state_changed.connect(lambda: saved.append(dock.state()))
    dock.open()

    dock.panel.float_button.click()  # detach
    frame = dock._frame
    assert dock.is_floating and dock.is_open and frame is not None
    assert frame.isVisible() and dock.panel.parent() is frame
    assert not any(handle.isVisible() for handle in dock.panel.handles)
    assert dock.panel.float_button.toolTip() == "Put it back in the window"
    assert saved[-1]["floating"] is True

    dock.close()  # the button of the corner puts it away
    assert not frame.isVisible() and not dock.is_open
    dock.open()  # and brings the same window back
    assert frame.isVisible() and dock.is_open

    dock.panel.float_button.click()  # attach again
    assert not dock.is_floating and not frame.isVisible()
    assert dock.panel.parent() is host and dock.is_open
    assert dock.panel.float_button.toolTip() == "Open in a window of its own"
    assert saved[-1]["floating"] is False

    dock.set_floating(False)  # already in the window
    host.close()


def test_the_window_of_the_chat_closes_to_a_place_it_remembers() -> None:
    host = _host(1000, 800)
    dock = AssistantDock(host)
    dock.open()
    dock.set_floating(True)
    frame = dock._frame
    assert frame is not None
    frame.move(120, 90)
    frame.resize(500, 520)
    application.processEvents()
    seen: list[int] = []
    dock.state_changed.connect(lambda: seen.append(1))

    frame.close()  # the cross of the window

    assert not frame.isVisible() and not dock.is_open and seen == [1]
    geometry = dock.state()["geometry"]
    assert geometry and dock.state()["floating"] is True
    dock.open()
    assert frame.isVisible() and frame.width() == 500
    host.close()


def test_a_window_that_moves_is_written_down_after_a_pause(monkeypatch) -> None:
    monkeypatch.setattr(assistant_panel, "SAVE_DELAY_MS", 30)
    host = _host(1000, 800)
    dock = AssistantDock(host)
    dock.set_floating(True)
    frame = dock._frame
    assert frame is not None
    frame.show()
    seen: list[int] = []
    dock.state_changed.connect(lambda: seen.append(1))

    frame.move(200, 150)
    frame.resize(480, 500)
    _wait(lambda: len(seen) >= 1)

    assert len(seen) == 1  # one write for the whole move
    host.close()


def test_the_state_comes_back_in_the_next_run() -> None:
    host = _host(1000, 800)
    first = AssistantDock(host)
    first.open()
    first.panel.dragged.emit(-90, -70)
    first.set_floating(True)
    assert first._frame is not None
    first._frame.resize(470, 530)
    kept = first.state()
    first.close()
    host.close()

    other = _host(1000, 800)
    second = AssistantDock(other)
    second.restore(kept)

    assert second.is_floating and not second.is_open  # it is there, but closed
    assert second._size.width() == kept["width"]
    second.open()
    assert second._frame is not None and second._frame.width() == 470
    other.close()

    third_host = _host(1000, 800)
    third = AssistantDock(third_host)
    third.restore({"width": 500, "height": 520, "geometry": ""})
    assert not third.is_floating and third._size.width() == 500
    third.open()
    assert third.panel.width() == 500
    third.restore({})  # a state with nothing in it changes nothing about the mode
    third_host.close()


def test_the_window_of_the_chat_follows_the_language_and_the_theme(monkeypatch) -> None:
    from kubescope import theme

    host = _host(1000, 800)
    dock = AssistantDock(host)
    dock.set_floating(True)
    frame = dock._frame
    assert frame is not None

    dock.retranslate()
    assert frame.windowTitle() == "Gabi"
    monkeypatch.setattr(theme, "_active", theme.DARK_THEME)
    dock.restyle()
    assert dock.panel.float_button.icon().isNull() is False
    monkeypatch.setattr(theme, "_active", theme.LIGHT_THEME)
    host.close()


def test_the_button_and_the_panel_carry_the_name_of_the_assistant() -> None:
    host = _host()
    dock = AssistantDock(host)

    assert dock.panel.title.text() == "Gabi"
    assert dock.bubble.toolTip() == "Ask Gabi"
    dock.set_floating(True)
    assert dock._frame is not None and dock._frame.windowTitle() == "Gabi"
    dock.retranslate()
    assert dock.panel.title.text() == "Gabi"  # a name is not translated
    host.close()
