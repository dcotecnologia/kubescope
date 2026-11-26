import ctypes
import ctypes.util
import os
import sys
from ctypes import wintypes
from typing import cast

from PySide6.QtCore import QEvent, QObject, QPoint, QPointF, QRectF, QSize, Qt
from PySide6.QtGui import (
    QGuiApplication,
    QIcon,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRegion,
)
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget

RESIZE_MARGIN = 5  # the strip around the window that a drag resizes from
CORNER_RADIUS = 10  # px of the corners of a window that draws its own frame
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


def has_compositor() -> bool:
    """Whether the desktop lets a window show what is behind it, which smooth
    corners need.

    Wayland always does; on X11 a compositing manager says so.
    """
    if QGuiApplication.platformName() == "wayland":
        return True
    if QGuiApplication.platformName() not in ("xcb", ""):
        return False
    name = ctypes.util.find_library("X11")
    if name is None or not os.environ.get("DISPLAY"):
        return False
    try:
        xlib = ctypes.CDLL(name)
        xlib.XOpenDisplay.restype = ctypes.c_void_p
        xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
        xlib.XInternAtom.restype = ctypes.c_ulong
        xlib.XInternAtom.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
        xlib.XGetSelectionOwner.restype = ctypes.c_ulong
        xlib.XGetSelectionOwner.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        xlib.XDefaultScreen.argtypes = [ctypes.c_void_p]
        xlib.XCloseDisplay.argtypes = [ctypes.c_void_p]
        display = xlib.XOpenDisplay(None)
        if not display:
            return False
        try:
            screen = xlib.XDefaultScreen(display)
            atom = xlib.XInternAtom(display, f"_NET_WM_CM_S{screen}".encode(), 0)
            return bool(xlib.XGetSelectionOwner(display, atom))
        finally:
            xlib.XCloseDisplay(display)
    except OSError, AttributeError:
        return False


class _Corners(QWidget):
    """Cuts the four corners of the content of the window, smoothly: it is
    painted last, over everything, and clears what lies outside the rounded
    outline (the strip that resizes the window included), so the desktop shows
    through there."""

    def __init__(self, window: QWidget) -> None:
        super().__init__(window)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.hide()

    def paintEvent(self, event: object) -> None:
        window = self.parentWidget()
        body = window.contentsRect() if window is not None else self.rect()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
        outside = QPainterPath()
        outside.addRect(QRectF(self.rect()))
        inside = QPainterPath()
        inside.addRoundedRect(QRectF(body), CORNER_RADIUS, CORNER_RADIUS)
        painter.fillPath(outside.subtracted(inside), Qt.GlobalColor.black)
        painter.end()


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
        self._corners = _Corners(window)
        self._compositor: bool | None = None  # asked of the desktop the first time
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
        window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, self.alpha)
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
        self._round(filled)

    def _round(self, filled: bool | None = None) -> None:
        """Round the corners of a window that draws its own frame, as the
        windows of the desktop have, except while it fills the screen: smooth
        where the desktop has a compositor, cut with a mask where it has not.

        Windows rounds its own through the system.
        """
        window = self._window
        if filled is None:
            filled = window.isMaximized() or window.isFullScreen()
        rounded = self.rounds and not filled
        smooth = rounded and self.alpha
        self._corners.setGeometry(window.rect())
        self._corners.setVisible(smooth)
        if smooth:
            self._corners.raise_()
        if rounded and not self.alpha and QGuiApplication.platformName() == "xcb":
            outline = QPainterPath()
            radius = CORNER_RADIUS + RESIZE_MARGIN  # the content is inset by the strip
            outline.addRoundedRect(
                0, 0, window.width(), window.height(), radius, radius
            )
            window.setMask(QRegion(outline.toFillPolygon().toPolygon()))
        else:
            window.clearMask()

    @property
    def rounds(self) -> bool:
        """Whether this window cuts its own corners."""
        return self.custom and sys.platform != "win32"

    @property
    def alpha(self) -> bool:
        """Whether it cuts them smoothly, which needs it to let the desktop
        show through."""
        if self._compositor is None:
            self._compositor = has_compositor()
        return self.rounds and self._compositor

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
        if kind == QEvent.Type.Resize and watched is self._window:
            self._round()  # the outline follows the size
            return False
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
