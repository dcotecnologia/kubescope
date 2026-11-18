import ctypes
import sys
from ctypes import wintypes
from typing import cast

from PySide6.QtCore import QEvent, QObject, QPoint, QPointF, QSize, Qt
from PySide6.QtGui import QIcon, QMouseEvent, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget

RESIZE_MARGIN = 5  # the strip around the window that a drag resizes from
EDGE_PADDING = 6  # what the controls leave of the top bar on their right

_WATCHED = (
    QEvent.Type.Enter,
    QEvent.Type.MouseButtonPress,
    QEvent.Type.MouseButtonDblClick,
    QEvent.Type.MouseMove,
)

_CURSORS = {
    Qt.Edge.LeftEdge: Qt.CursorShape.SizeHorCursor,
    Qt.Edge.RightEdge: Qt.CursorShape.SizeHorCursor,
    Qt.Edge.TopEdge: Qt.CursorShape.SizeVerCursor,
    Qt.Edge.BottomEdge: Qt.CursorShape.SizeVerCursor,
    Qt.Edge.LeftEdge | Qt.Edge.TopEdge: Qt.CursorShape.SizeFDiagCursor,
    Qt.Edge.RightEdge | Qt.Edge.BottomEdge: Qt.CursorShape.SizeFDiagCursor,
    Qt.Edge.RightEdge | Qt.Edge.TopEdge: Qt.CursorShape.SizeBDiagCursor,
    Qt.Edge.LeftEdge | Qt.Edge.BottomEdge: Qt.CursorShape.SizeBDiagCursor,
}


_WM_NCHITTEST = 0x0084
_WM_NCCALCSIZE = 0x0083
_GWL_STYLE = -16
_STYLE_BITS = 0x00040000 | 0x00020000 | 0x00010000  # thick frame, minimize, maximize
_CORNER_PREFERENCE = 33
_ROUND = 2
_SWP_REFRESH = 0x0001 | 0x0002 | 0x0004 | 0x0010 | 0x0020  # no size/move/z/activate
_HIT = {  # what Windows is told a point on the resize strip is
    Qt.Edge.LeftEdge: 10,
    Qt.Edge.RightEdge: 11,
    Qt.Edge.TopEdge: 12,
    Qt.Edge.LeftEdge | Qt.Edge.TopEdge: 13,
    Qt.Edge.RightEdge | Qt.Edge.TopEdge: 14,
    Qt.Edge.BottomEdge: 15,
    Qt.Edge.LeftEdge | Qt.Edge.BottomEdge: 16,
    Qt.Edge.RightEdge | Qt.Edge.BottomEdge: 17,
}


def control_icon(kind: str) -> QIcon:
    """A white window control for the top bar, which is dark in every theme."""
    scale = 3  # drawn three times larger so the edges stay smooth
    pixmap = QPixmap(14 * scale, 14 * scale)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(scale, scale)
    pen = QPen(Qt.GlobalColor.white, 1.2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    if kind == "minimize":
        painter.drawLine(QPointF(3, 10), QPointF(11, 10))
    elif kind == "maximize":
        painter.drawRect(3, 3, 8, 8)
    elif kind == "restore":
        painter.drawRect(3, 5, 6, 6)
        painter.drawPolyline([QPointF(5, 5), QPointF(5, 3), QPointF(11, 3)])
        painter.drawPolyline([QPointF(11, 3), QPointF(11, 9), QPointF(9, 9)])
    else:
        painter.drawLine(QPointF(3, 3), QPointF(11, 11))
        painter.drawLine(QPointF(11, 3), QPointF(3, 11))
    painter.end()
    pixmap.setDevicePixelRatio(scale)
    return QIcon(pixmap)


class WindowFrame(QObject):
    """Draws the window's own title bar: the top bar moves the window and holds
    its controls, and a strip around the window resizes it.

    With the system's title bar on, it steps aside.
    """

    custom = False  # also what a frame says while it is being torn down

    def __init__(
        self,
        window: QMainWindow,
        bar: QWidget,
        controls: QWidget,
        minimize: QPushButton,
        maximize: QPushButton,
        close: QPushButton,
    ) -> None:
        super().__init__(window)
        self._window = window
        self._bar = bar
        self._controls = controls
        self._maximize = maximize
        minimize.setIcon(control_icon("minimize"))
        minimize.setIconSize(QSize(14, 14))
        maximize.setIconSize(QSize(14, 14))
        close.setIcon(control_icon("close"))
        close.setIconSize(QSize(14, 14))
        minimize.clicked.connect(window.showMinimized)
        maximize.clicked.connect(self.toggle_maximized)
        close.clicked.connect(window.close)
        layout = bar.layout()
        assert layout is not None
        self._layout = layout
        self._margins = layout.contentsMargins()
        self.custom = False
        self.set_custom(False)
        window.setMouseTracking(True)
        window.installEventFilter(self)
        bar.installEventFilter(self)
        central = window.centralWidget()
        assert central is not None
        central.installEventFilter(self)

    def set_custom(self, custom: bool) -> None:
        """Draw the title bar here (True) or leave it to the system (False)."""
        window = self._window
        visible = window.isVisible()
        self.custom = custom
        window.setWindowFlag(Qt.WindowType.FramelessWindowHint, custom)
        if visible:
            window.show()  # changing a window's flags hides it
        if custom:
            self._allow_system_resize()
        self._controls.setVisible(custom)
        margins = self._margins  # the controls go to the edge of the bar
        self._layout.setContentsMargins(
            margins.left(),
            margins.top(),
            6 if custom else margins.right(),
            margins.bottom(),
        )
        self.refresh()

    def _allow_system_resize(self) -> None:
        """Windows only resizes a window that has a sizing frame, and a window
        without a title bar has none: give it one, and draw nothing of it."""
        if sys.platform != "win32":
            return
        user32 = ctypes.windll.user32
        hwnd = wintypes.HWND(int(self._window.winId()))
        get, set_ = user32.GetWindowLongPtrW, user32.SetWindowLongPtrW
        get.restype, get.argtypes = ctypes.c_ssize_t, [wintypes.HWND, ctypes.c_int]
        set_.restype = ctypes.c_ssize_t
        set_.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
        set_(hwnd, _GWL_STYLE, get(hwnd, _GWL_STYLE) | _STYLE_BITS)
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, _SWP_REFRESH)
        # What the system draws on its own windows: a shadow, a thin border and
        # (on Windows 11) rounded corners. Older versions ignore what they lack.
        dwm = ctypes.windll.dwmapi
        dwm.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(wintypes.RECT(0, 0, 1, 0)))
        corners = ctypes.c_int(_ROUND)
        dwm.DwmSetWindowAttribute(
            hwnd, _CORNER_PREFERENCE, ctypes.byref(corners), ctypes.sizeof(corners)
        )

    def refresh(self) -> None:
        """Follow the window's state: the right icon, and no resize strip while
        it fills the screen."""
        window = self._window
        filled = window.isMaximized() or window.isFullScreen()
        # Windows resizes from the window's own edge, so it needs no strip
        strip = self.custom and not filled and sys.platform != "win32"
        margin = RESIZE_MARGIN if strip else 0
        window.setContentsMargins(margin, margin, margin, margin)
        self._maximize.setIcon(control_icon("restore" if filled else "maximize"))

    def toggle_maximized(self) -> None:
        window = self._window
        if window.isMaximized():
            window.showNormal()
        else:
            window.showMaximized()

    def edges_at(self, position: QPointF) -> Qt.Edge:
        """The edges of the window that a point lies on."""
        window = self._window
        edges = Qt.Edge(0)
        if position.x() < RESIZE_MARGIN:
            edges |= Qt.Edge.LeftEdge
        elif position.x() >= window.width() - RESIZE_MARGIN:
            edges |= Qt.Edge.RightEdge
        if position.y() < RESIZE_MARGIN:
            edges |= Qt.Edge.TopEdge
        elif position.y() >= window.height() - RESIZE_MARGIN:
            edges |= Qt.Edge.BottomEdge
        return edges

    def native_hit(self, event_type: object, message: object) -> int | None:
        """On Windows, the part of the window a pointer is on, when it is on the
        resize strip: the system then resizes the window itself. None otherwise."""
        if (
            sys.platform != "win32"
            or not self.custom
            or bytes(cast(bytes, event_type)) != b"windows_generic_MSG"
            or self._window.isMaximized()
            or self._window.isFullScreen()
        ):
            return None
        msg = wintypes.MSG.from_address(int(cast(int, message)))
        if msg.message == _WM_NCCALCSIZE and msg.wParam:
            return 0  # the whole window is client area: no frame is drawn
        if msg.message != _WM_NCHITTEST:
            return None
        x = ctypes.c_short(msg.lParam & 0xFFFF).value
        y = ctypes.c_short((msg.lParam >> 16) & 0xFFFF).value
        ratio = self._window.devicePixelRatio()
        point = self._window.mapFromGlobal(QPoint(round(x / ratio), round(y / ratio)))
        return _HIT.get(self.edges_at(QPointF(point)))

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if not self.custom:
            return False
        kind = event.type()
        if kind not in _WATCHED:  # the rest also arrives while the window dies
            return False
        if watched is self._window.centralWidget():
            if kind == QEvent.Type.Enter:
                self._window.unsetCursor()  # the resize cursor is for the strip
            return False
        mouse = cast(QMouseEvent, event)  # only read once `kind` says so
        if watched is self._bar:
            if kind == QEvent.Type.MouseButtonPress:
                if mouse.button() == Qt.MouseButton.LeftButton:
                    handle = self._window.windowHandle()
                    assert handle is not None
                    handle.startSystemMove()
                    return True
            elif (
                kind == QEvent.Type.MouseButtonDblClick
                and mouse.button() == Qt.MouseButton.LeftButton
            ):
                self.toggle_maximized()
                return True
            return False
        if self._window.isMaximized() or self._window.isFullScreen():
            return False
        if kind == QEvent.Type.MouseMove:
            edges = self.edges_at(mouse.position())
            if edges in _CURSORS:
                self._window.setCursor(_CURSORS[edges])
            else:
                self._window.unsetCursor()
        elif kind == QEvent.Type.MouseButtonPress:
            edges = self.edges_at(mouse.position())
            if edges:
                handle = self._window.windowHandle()
                assert handle is not None
                handle.startSystemResize(edges)
                return True
        return False
