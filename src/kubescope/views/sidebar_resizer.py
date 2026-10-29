from PySide6.QtCore import QEvent, QObject, QPoint, Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget

MIN_WIDTH = 180
MAX_WIDTH = 560
GRIP = 6  # the width of the strip at the right edge that is dragged


class _Grip(QWidget):
    """The strip at the right edge of the side menu."""

    dragged = Signal(int)  # the width the menu should have
    released = Signal()
    reset = Signal()

    def __init__(self, sidebar: QWidget) -> None:
        super().__init__(sidebar)
        self._sidebar = sidebar
        self._origin: QPoint | None = None
        self._start = 0
        self.setCursor(Qt.CursorShape.SizeHorCursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._origin = event.globalPosition().toPoint()
        self._start = self._sidebar.width()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._origin is not None:
            moved = event.globalPosition().toPoint() - self._origin
            self.dragged.emit(self._start + moved.x())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._origin is not None:
            self._origin = None
            self.released.emit()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.reset.emit()


class SidebarResizer(QObject):
    """Let the person drag the right edge of the side menu to make it wider or
    narrower, and double-click it to go back to the usual width."""

    width_changed = Signal(int)  # the person finished choosing a width

    def __init__(self, sidebar: QWidget, default: int) -> None:
        super().__init__(sidebar)
        self.sidebar = sidebar
        self.default = default
        self.grip = _Grip(sidebar)
        self.grip.dragged.connect(self.set_width)
        self.grip.released.connect(self._chosen)
        self.grip.reset.connect(self._reset)
        sidebar.installEventFilter(self)
        self.set_width(default)
        self._place()

    def set_width(self, width: int) -> None:
        """Give the menu a width, within what keeps it usable."""
        width = min(max(width, MIN_WIDTH), MAX_WIDTH)
        self.sidebar.setFixedWidth(width)

    def _chosen(self) -> None:
        self.width_changed.emit(self.sidebar.width())

    def _reset(self) -> None:
        self.set_width(self.default)
        self._chosen()

    def _place(self) -> None:
        self.grip.setGeometry(
            self.sidebar.width() - GRIP, 0, GRIP, self.sidebar.height()
        )
        self.grip.raise_()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.sidebar and event.type() == QEvent.Type.Resize:
            self._place()
        return False
