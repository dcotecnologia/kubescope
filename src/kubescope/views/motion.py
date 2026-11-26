"""The slide up of a window or a list when it first shows.

The widget fades in while it rises a few pixels to its place. It is
drawn by an effect, so nothing moves in its layout and nothing else has
to know. The person can turn it off in the settings.
"""

import re
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
    QTimer,
    QVariantAnimation,
)
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QDialog, QGraphicsEffect, QLabel, QProgressBar, QWidget

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


def slide_up(widget: QWidget, delay_ms: int = 0) -> None:
    """Let a widget rise into its place, after `delay_ms` (the widget waits
    unseen); nothing when the animations are off or the widget is already being
    drawn by an effect."""
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
    if delay_ms > 0:
        effect.setProperty("progress", 0.0)  # unseen until its turn
        QTimer.singleShot(delay_ms, animation.start)
    else:
        animation.start()


COUNT_MS = 750
_NUMBER = re.compile(r"\d+(?:([.,])(\d+))?")


def count_up(label: QLabel, text: str) -> None:
    """Show `text` in a label, counting its first number up from the one the
    label had (or from zero) so a value that changed is seen changing.

    The text is set at once when the animations are off, when the label
    already shows it, or when it has no number ("—").
    """
    previous = cast(str, label.property("countedText") or "")
    label.setText(text)
    label.setProperty("countedText", text)
    running = cast(QVariantAnimation | None, label.property("countAnimation"))
    if running is not None:
        running.stop()
    found = _NUMBER.search(text)
    if not ENABLED or COUNT_MS <= 0 or found is None or text == previous:
        return
    separator = found.group(1) or "."
    decimals = len(found.group(2) or "")
    target = float(found.group(0).replace(",", "."))
    before = _NUMBER.search(previous)
    start = float(before.group(0).replace(",", ".")) if before else 0.0
    if start == target:
        return

    def show(value: float) -> None:
        number = f"{value:.{decimals}f}".replace(".", separator)
        label.setText(text[: found.start()] + number + text[found.end() :])

    animation = QVariantAnimation(label)
    animation.setStartValue(start)
    animation.setEndValue(target)
    animation.setDuration(COUNT_MS)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.valueChanged.connect(show)
    animation.finished.connect(lambda: label.setText(text))
    label.setProperty("countAnimation", animation)
    show(start)  # from the first frame, not after a flash of the final text
    animation.start()


def fill_bar(bar: QProgressBar, percent: int) -> None:
    """Let a bar grow (or shrink) to its value instead of jumping."""
    if not ENABLED or COUNT_MS <= 0:
        bar.setValue(percent)
        return
    running = cast(QPropertyAnimation | None, bar.property("fillAnimation"))
    if running is not None:
        running.stop()
    animation = QPropertyAnimation(bar, b"value", bar)
    animation.setStartValue(bar.value())
    animation.setEndValue(percent)
    animation.setDuration(COUNT_MS)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.finished.connect(lambda: bar.setValue(percent))
    bar.setProperty("fillAnimation", animation)
    animation.start()


class DialogSlide(QObject):
    """Make every dialog of the app rise as it opens."""

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Show and isinstance(watched, QDialog):
            slide_up(watched)
        return False
