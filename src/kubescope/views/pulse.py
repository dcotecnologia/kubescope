"""A ring that spreads from a widget and fades, to say that it just changed.

It is drawn by a child of the widget's parent that lets every click
through, so nothing in the layout moves. The person turns it off with
the animations of the settings.
"""

from PySide6.QtCore import Property, QEasingCurve, QPropertyAnimation, QRect, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from kubescope.views import motion

DURATION_MS = 900
REACH = 10  # pixels the ring spreads to beyond the widget


class _Ring(QWidget):
    def __init__(self, parent: QWidget, color: QColor, radius: int) -> None:
        super().__init__(parent)
        self._color = color
        self._radius = radius
        self._progress = 0.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

    def _get_progress(self) -> float:
        return self._progress

    def _set_progress(self, value: float) -> None:
        self._progress = value
        self.update()

    progress = Property(float, _get_progress, _set_progress)

    def paintEvent(self, _event: object) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(self._color)
        color.setAlphaF(max(0.0, 1.0 - self._progress) * 0.9)
        pen = QPen(color, 2.0)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        spread = self._progress * REACH
        inset = REACH - spread
        rect = self.rect().adjusted(
            round(inset) + 1, round(inset) + 1, -round(inset) - 1, -round(inset) - 1
        )
        painter.drawRoundedRect(rect, self._radius + spread, self._radius + spread)


def pulse(widget: QWidget, color: str, radius: int = 6) -> None:
    """Make a ring spread from `widget` and fade; nothing when the animations
    are off or the widget is not on screen."""
    parent = widget.parentWidget()
    if (
        not motion.ENABLED
        or DURATION_MS <= 0
        or parent is None
        or not widget.isVisible()
    ):
        return
    ring = _Ring(parent, QColor(color), radius)
    area = widget.geometry().adjusted(-REACH, -REACH, REACH, REACH)
    ring.setGeometry(QRect(area))
    ring.show()
    ring.raise_()
    animation = QPropertyAnimation(ring, b"progress", ring)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setDuration(DURATION_MS)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.finished.connect(ring.deleteLater)
    animation.start()
