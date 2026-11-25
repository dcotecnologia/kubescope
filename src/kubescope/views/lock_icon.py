"""A small padlock, drawn, closed or open."""

from PySide6.QtCore import QLineF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap


def lock_pixmap(
    color: QColor, unlocked: bool, size: int = 11, ratio: float = 2.0
) -> QPixmap:
    """A padlock of `size` pixels in `color`; the shackle is raised and to one
    side when `unlocked`."""
    pixmap = QPixmap(round(size * ratio), round(size * ratio))
    pixmap.setDevicePixelRatio(ratio)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    body = QRectF(size * 0.14, size * 0.46, size * 0.72, size * 0.46)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(color)
    painter.drawRoundedRect(body, size * 0.1, size * 0.1)
    pen = QPen(color, max(size * 0.14, 1.2))
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    left, right = size * 0.3, size * 0.7
    top = size * 0.08
    if unlocked:  # raised: the left end hangs free above the body
        height = size * 0.5
        painter.drawArc(QRectF(left, size * 0.02, right - left, height), 0, 180 * 16)
        painter.drawLine(QLineF(right, size * 0.02 + height / 2, right, body.top()))
    else:
        height = size * 0.7
        painter.drawArc(QRectF(left, top, right - left, height), 0, 180 * 16)
        painter.drawLine(QLineF(left, top + height / 2, left, body.top()))
        painter.drawLine(QLineF(right, top + height / 2, right, body.top()))
    painter.end()
    return pixmap
