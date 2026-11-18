import ctypes
import os
import sys
from ctypes import wintypes
from unittest.mock import MagicMock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEvent, QPoint, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QWidget,
)

from kubescope.views import window_frame
from kubescope.views.window_frame import RESIZE_MARGIN, WindowFrame, control_icon
from tests.qt import get_application, present


def _frame() -> tuple[QMainWindow, WindowFrame, QFrame, list[QPushButton]]:
    get_application()
    window = QMainWindow()
    window.resize(400, 300)
    central = QWidget()
    window.setCentralWidget(central)
    bar = QFrame(central)
    QHBoxLayout(bar).setContentsMargins(18, 0, 22, 0)
    controls = QWidget(central)
    buttons = [QPushButton(controls) for _ in range(3)]
    return window, WindowFrame(window, bar, controls, *buttons), bar, buttons


def _mouse(kind: QEvent.Type, x: float, y: float, button=Qt.MouseButton.LeftButton):
    point = QPointF(x, y)
    return QMouseEvent(
        kind, point, point, button, button, Qt.KeyboardModifier.NoModifier
    )


def test_the_controls_show_only_while_the_window_draws_its_own_title_bar() -> None:
    window, frame, _bar, buttons = _frame()

    assert not frame.custom and not buttons[0].isVisibleTo(window)
    assert window.contentsMargins().left() == 0
    assert not window.windowFlags() & Qt.WindowType.FramelessWindowHint

    frame.set_custom(True)

    assert frame.custom and all(b.isVisibleTo(window) for b in buttons)
    assert window.contentsMargins().left() == (
        0 if sys.platform == "win32" else RESIZE_MARGIN
    )
    assert window.windowFlags() & Qt.WindowType.FramelessWindowHint
    frame.set_custom(False)
    assert not buttons[2].isVisibleTo(window)
    assert not window.windowFlags() & Qt.WindowType.FramelessWindowHint


def test_the_bar_keeps_its_margin_except_where_the_controls_sit() -> None:
    _window, frame, bar, _buttons = _frame()
    layout = present(bar.layout())

    frame.set_custom(True)
    assert layout.contentsMargins().right() == window_frame.EDGE_PADDING
    frame.set_custom(False)
    assert layout.contentsMargins().right() == 22


def test_changing_the_title_bar_of_a_shown_window_shows_it_again() -> None:
    window, frame, _bar, _buttons = _frame()
    window.show()

    frame.set_custom(True)

    assert window.isVisible()
    window.close()


def test_the_icons_are_drawn_for_every_control() -> None:
    get_application()

    for kind in ("minimize", "maximize", "restore", "close"):
        assert not control_icon(kind).isNull()


def test_the_buttons_minimize_maximize_restore_and_close() -> None:
    window, frame, _bar, (minimize, maximize, close) = _frame()
    frame.set_custom(True)
    window.show()

    minimize.click()
    assert window.isMinimized()
    window.showNormal()

    maximize.click()
    assert window.isMaximized()
    frame.refresh()
    assert frame.edges_at(QPointF(0, 0)) and window.contentsMargins().left() == 0
    maximize.click()
    assert not window.isMaximized()

    closed = []
    window.installEventFilter(_Recorder(window, closed))
    close.click()
    assert closed == [QEvent.Type.Close]


class _Recorder(QWidget):
    def __init__(self, parent, seen: list) -> None:
        super().__init__(parent)
        self._seen = seen

    def eventFilter(self, watched, event) -> bool:
        if event.type() == QEvent.Type.Close:
            self._seen.append(event.type())
        return False


def test_the_edges_of_a_point_in_the_window() -> None:
    window, frame, _bar, _buttons = _frame()
    width, height = window.width(), window.height()

    assert frame.edges_at(QPointF(100, 100)) == Qt.Edge(0)
    assert frame.edges_at(QPointF(0, 100)) == Qt.Edge.LeftEdge
    assert frame.edges_at(QPointF(width - 1, 100)) == Qt.Edge.RightEdge
    assert frame.edges_at(QPointF(100, 0)) == Qt.Edge.TopEdge
    assert frame.edges_at(QPointF(100, height - 1)) == Qt.Edge.BottomEdge
    assert frame.edges_at(QPointF(0, 0)) == Qt.Edge.LeftEdge | Qt.Edge.TopEdge


def test_the_bar_moves_the_window_and_two_clicks_maximize_it(monkeypatch) -> None:
    window, frame, bar, _buttons = _frame()
    window.show()
    moved = []
    monkeypatch.setattr(
        type(present(window.windowHandle())),
        "startSystemMove",
        lambda self: moved.append(True) or True,
    )

    press = _mouse(QEvent.Type.MouseButtonPress, 20, 20)
    assert frame.eventFilter(bar, press) is False  # the system's bar is in charge
    frame.set_custom(True)
    assert frame.eventFilter(bar, press) is True and moved == [True]
    right = _mouse(QEvent.Type.MouseButtonPress, 20, 20, Qt.MouseButton.RightButton)
    assert frame.eventFilter(bar, right) is False
    release = _mouse(QEvent.Type.MouseButtonRelease, 20, 20)
    assert frame.eventFilter(bar, release) is False

    double = _mouse(QEvent.Type.MouseButtonDblClick, 20, 20)
    assert frame.eventFilter(bar, double) is True
    assert window.isMaximized()
    middle = _mouse(
        QEvent.Type.MouseButtonDblClick, 20, 20, Qt.MouseButton.MiddleButton
    )
    assert frame.eventFilter(bar, middle) is False


def test_the_strip_around_the_window_shows_a_cursor_and_resizes(monkeypatch) -> None:
    window, frame, _bar, _buttons = _frame()
    frame.set_custom(True)
    window.show()
    resized = []
    monkeypatch.setattr(
        type(present(window.windowHandle())),
        "startSystemResize",
        lambda self, edges: resized.append(edges) or True,
    )

    move = _mouse(QEvent.Type.MouseMove, 1, 100, Qt.MouseButton.NoButton)
    assert frame.eventFilter(window, move) is False
    assert window.cursor().shape() == Qt.CursorShape.SizeHorCursor
    inside = _mouse(QEvent.Type.MouseMove, 100, 100, Qt.MouseButton.NoButton)
    frame.eventFilter(window, inside)
    assert window.cursor().shape() == Qt.CursorShape.ArrowCursor

    assert frame.eventFilter(window, _mouse(QEvent.Type.MouseButtonPress, 1, 100))
    assert resized == [Qt.Edge.LeftEdge]
    assert not frame.eventFilter(window, _mouse(QEvent.Type.MouseButtonPress, 100, 100))
    assert resized == [Qt.Edge.LeftEdge]


def test_the_resize_cursor_goes_when_the_mouse_enters_the_window() -> None:
    window, frame, _bar, _buttons = _frame()
    frame.set_custom(True)
    window.setCursor(Qt.CursorShape.SizeHorCursor)

    central = present(window.centralWidget())
    entered = frame.eventFilter(central, QEvent(QEvent.Type.Enter))

    assert entered is False
    assert window.cursor().shape() == Qt.CursorShape.ArrowCursor
    other = QEvent(QEvent.Type.Leave)
    assert frame.eventFilter(central, other) is False
    move = _mouse(QEvent.Type.MouseMove, 100, 100, Qt.MouseButton.NoButton)
    assert frame.eventFilter(central, move) is False  # only entering matters
    assert frame.eventFilter(window, QEvent(QEvent.Type.Enter)) is False


def test_a_window_that_fills_the_screen_has_no_strip_to_resize_from() -> None:
    window, frame, _bar, _buttons = _frame()
    frame.set_custom(True)
    window.showMaximized()

    move = _mouse(QEvent.Type.MouseMove, 1, 100, Qt.MouseButton.NoButton)

    assert frame.eventFilter(window, move) is False
    assert window.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert QPoint(0, 0) == QPoint()


def _on_windows(monkeypatch) -> None:
    monkeypatch.setattr(sys, "platform", "win32")


def test_windows_is_given_a_sizing_frame_for_the_window_without_a_title_bar(
    monkeypatch,
) -> None:
    window, frame, _bar, _buttons = _frame()
    windll = MagicMock()
    windll.user32.GetWindowLongPtrW.return_value = 0
    monkeypatch.setattr(ctypes, "windll", windll, raising=False)
    _on_windows(monkeypatch)

    frame._allow_system_resize()

    windll.user32.SetWindowLongPtrW.assert_called_once()
    windll.user32.SetWindowPos.assert_called_once()
    windll.dwmapi.DwmExtendFrameIntoClientArea.assert_called_once()
    windll.dwmapi.DwmSetWindowAttribute.assert_called_once()
    assert window.windowFlags() is not None


def _message(kind: int, w_param: int = 0, l_param: int = 0):
    msg = wintypes.MSG()
    msg.message, msg.wParam, msg.lParam = kind, w_param, l_param
    return msg


def test_windows_resizes_the_window_from_its_own_edge(monkeypatch) -> None:
    window, frame, _bar, _buttons = _frame()
    frame.set_custom(True)
    _on_windows(monkeypatch)
    event = b"windows_generic_MSG"

    def hit(msg) -> int | None:
        return frame.native_hit(event, ctypes.addressof(msg))

    assert frame.native_hit(b"xcb_generic_event_t", 0) is None
    assert hit(_message(window_frame._WM_NCCALCSIZE, 1)) == 0
    assert hit(_message(0x0001)) is None
    point = window.mapToGlobal(QPoint(1, 100))
    l_param = ((point.y() & 0xFFFF) << 16) | (point.x() & 0xFFFF)
    assert hit(_message(window_frame._WM_NCHITTEST, 0, l_param)) == 10


def test_the_window_hands_native_events_to_its_frame(monkeypatch) -> None:
    from kubescope import window as window_module

    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    window = window_module.WorkloadWindow()

    monkeypatch.setattr(window._frame, "native_hit", lambda *_args: 12)
    assert window.nativeEvent(b"windows_generic_MSG", 0) == (True, 12)

    monkeypatch.setattr(window._frame, "native_hit", lambda *_args: None)
    monkeypatch.setattr(QMainWindow, "nativeEvent", lambda *_args: (False, 0))
    assert window.nativeEvent(b"other", 0) == (False, 0)
