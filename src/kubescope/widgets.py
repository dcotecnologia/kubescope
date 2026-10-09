"""Small custom widgets used by the Designer layouts."""

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QSizePolicy, QWidget

TRACK = "#e8eaee"
OK = "#3d9a6d"
WARNING = "#e0a030"
BAD = "#d05560"


class StatusBar(QWidget):
    """A thin bar split into healthy, warning and failing parts of a total;
    what is left over (idle resources) stays as the empty track."""

    HEIGHT = 8

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._parts = (0, 0, 0)
        self._total = 0
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self.HEIGHT)

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(200, self.HEIGHT)

    def set_summary(self, ok: int, warning: int, bad: int, total: int) -> None:
        self._parts = (ok, warning, bad)
        self._total = total
        self.update()

    def paintEvent(self, _event: QPaintEvent) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        radius = self.HEIGHT / 2
        painter.setBrush(QColor(TRACK))
        painter.drawRoundedRect(QRectF(self.rect()), radius, radius)
        if self._total <= 0:
            return
        x = 0.0
        for count, color in zip(self._parts, (OK, WARNING, BAD), strict=True):
            width = self.width() * count / self._total
            if width > 0:
                painter.setBrush(QColor(color))
                painter.drawRoundedRect(
                    QRectF(x, 0, width, self.height()), radius, radius
                )
            x += width
