from PySide6.QtCore import QEvent, QObject, QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QLabel, QPushButton

from kubescope.theme import themed

SIZE = 14
RIGHT = 12  # the space between the chevron and the edge of the button


class NavChevron(QLabel):
    """The arrow at the right of a side menu entry that has entries under it:
    pointing down while they show, to the right while they are folded."""

    def __init__(self, button: QPushButton) -> None:
        super().__init__(button)
        self._button = button
        self._open = True
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.resize(SIZE, SIZE)
        button.installEventFilter(self)
        self.refresh()
        self.place()

    def set_open(self, opened: bool) -> None:
        self._open = opened
        self.refresh()

    def refresh(self) -> None:
        """Draw it again, in the colors of the theme in use."""
        scale = 3  # drawn three times larger so the edges stay smooth
        pixmap = QPixmap(SIZE * scale, SIZE * scale)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.scale(scale, scale)
        pen = QPen(QColor(themed("#6b7380")), 1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        if self._open:
            painter.drawPolyline([QPointF(3.5, 5.5), QPointF(7, 9), QPointF(10.5, 5.5)])
        else:
            painter.drawPolyline([QPointF(5.5, 3.5), QPointF(9, 7), QPointF(5.5, 10.5)])
        painter.end()
        pixmap.setDevicePixelRatio(scale)
        self.setPixmap(pixmap)

    def place(self) -> None:
        button = self._button
        self.move(button.width() - SIZE - RIGHT, (button.height() - SIZE) // 2)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # also called while the button is torn down, when this is half gone
        if watched is getattr(self, "_button", None) and (
            event.type() == QEvent.Type.Resize
        ):
            self.place()
        return False
