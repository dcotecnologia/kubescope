"""The slide up of a window or a list when it first shows.

The widget fades in while it rises a few pixels to its place. It is
drawn by an effect, so nothing moves in its layout and nothing else has
to know. The person can turn it off in the settings.
"""

from typing import Any, cast

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QEvent,
    QObject,
    QPoint,
    QPropertyAnimation,
    QRect,
    QRectF,
    Qt,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QDialog, QGraphicsEffect, QWidget

ENABLED = True
DURATION_MS = 260
DISTANCE = 18  # pixels below its place that the widget starts from


class SlideUpEffect(QGraphicsEffect):
    """Draw the widget lower and fainter, by `progress` from 0 to 1."""

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self._progress = 0.0

    def _get_progress(self) -> float:
        return self._progress

    def _set_progress(self, value: float) -> None:
        self._progress = value
        self.update()

    progress = Property(float, _get_progress, _set_progress)

    def boundingRectFor(self, rect: QRectF | QRect) -> QRectF:
        return QRectF(rect).adjusted(0, 0, 0, DISTANCE)

    def draw(self, painter: QPainter) -> None:
        offset = QPoint()
        pixmap = self.sourcePixmap(Qt.CoordinateSystem.LogicalCoordinates, offset)
        if pixmap.isNull():
            return
        painter.setOpacity(self._progress)
        painter.drawPixmap(
            offset + QPoint(0, round((1 - self._progress) * DISTANCE)), pixmap
        )


def slide_up(widget: QWidget) -> None:
    """Let a widget rise into its place; nothing when the animations are off or
    the widget is already being drawn by an effect."""
    if not ENABLED or DURATION_MS <= 0 or widget.graphicsEffect() is not None:
        return
    effect = SlideUpEffect(widget)
    widget.setGraphicsEffect(effect)
    animation = QPropertyAnimation(effect, b"progress", widget)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setDuration(DURATION_MS)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.finished.connect(lambda: cast(Any, widget).setGraphicsEffect(None))
    animation.start()


class DialogSlide(QObject):
    """Make every dialog of the app rise as it opens."""

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Show and isinstance(watched, QDialog):
            slide_up(watched)
        return False
