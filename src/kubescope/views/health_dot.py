"""The dot beside the cluster selector that says whether the cluster
answers."""

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget

SIZE = 10
# state -> color of the dot
COLORS = {
    "unknown": "#8a93a3",  # not asked yet, or asking
    "ok": "#2fb67c",  # the last answer came
    "error": "#e5534b",  # the cluster could not be reached
    "auth": "#e8a23b",  # it needs the person to sign in
}


class HealthDot(QWidget):
    """A small colored circle with the state in its tooltip."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = "unknown"
        self.setFixedSize(QSize(SIZE + 6, SIZE + 6))
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

    def set_state(self, state: str, tooltip: str) -> None:
        self.state = state if state in COLORS else "unknown"
        self.setToolTip(tooltip)
        self.setAccessibleName(tooltip)
        self.update()

    @property
    def color(self) -> QColor:
        return QColor(COLORS[self.state])

    def paintEvent(self, _event: object) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.color)
        margin = (self.width() - SIZE) // 2
        painter.drawEllipse(margin, margin, SIZE, SIZE)
