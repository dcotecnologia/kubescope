"""The small round-button icons of the chat, drawn so no font has to have
them."""

from math import cos, pi, sin

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
)

SIZE = 22


def _draw(paint) -> QIcon:
    pixmap = QPixmap(SIZE * 2, SIZE * 2)  # drawn at twice the size, for sharp edges
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(2, 2)
    paint(painter)
    painter.end()
    return QIcon(pixmap)


def _pen(color: str, width: float = 2.0) -> QPen:
    pen = QPen(QColor(color), width)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    return pen


def send_icon(color: str = "#ffffff") -> QIcon:
    """A paper plane."""

    def paint(painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawPolygon(
            QPolygonF([QPointF(3, 3), QPointF(19, 11), QPointF(3, 19), QPointF(6, 11)])
        )

    return _draw(paint)


def stop_icon(color: str = "#ffffff") -> QIcon:
    """A square."""

    def paint(painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawRoundedRect(QRectF(6, 6, 10, 10), 2, 2)

    return _draw(paint)


def attach_icon(color: str = "#8696a0") -> QIcon:
    """A plus."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_pen(color, 2.2))
        painter.drawLine(QPointF(11, 4), QPointF(11, 18))
        painter.drawLine(QPointF(4, 11), QPointF(18, 11))

    return _draw(paint)


def _star(painter: QPainter, x: float, y: float, radius: float) -> None:
    """A four-pointed star centered at (x, y)."""
    inner = radius * 0.36
    points = []
    for index in range(8):
        reach = radius if index % 2 == 0 else inner
        angle = index * pi / 4
        points.append(
            QPointF(x + reach * sin(angle), y - reach * cos(angle)),
        )
    painter.drawPolygon(QPolygonF(points))


def sparkle_icon(
    color: str = "#ffffff", size: int = SIZE, inside: str = "#3220a0"
) -> QIcon:
    """A speech bubble with the star of an AI inside it."""
    pixmap = QPixmap(size * 2, size * 2)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(2 * size / SIZE, 2 * size / SIZE)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))
    bubble = QPainterPath()
    bubble.addRoundedRect(QRectF(2, 3, 18, 13.5), 5, 5)
    tail = QPainterPath()
    tail.moveTo(6.5, 15.5)
    tail.lineTo(5, 20)
    tail.lineTo(11, 16)
    tail.closeSubpath()
    painter.drawPath(bubble.united(tail))
    painter.setBrush(QColor(inside))
    _star(painter, 11, 9.7, 5.6)
    painter.end()
    return QIcon(pixmap)


def popout_icon(color: str = "#ffffff") -> QIcon:
    """A square with an arrow leaving it, for taking the chat out of the
    window."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(3, 7, 12, 12), 2, 2)
        painter.drawLine(QPointF(10, 12), QPointF(19, 3))
        painter.drawLine(QPointF(12, 3), QPointF(19, 3))
        painter.drawLine(QPointF(19, 3), QPointF(19, 10))

    return _draw(paint)


def dock_icon(color: str = "#ffffff") -> QIcon:
    """A square with an arrow entering it, for putting the chat back."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(3, 3, 16, 16), 2, 2)
        painter.drawLine(QPointF(8, 8), QPointF(15, 15))
        painter.drawLine(QPointF(8, 14), QPointF(8, 8))
        painter.drawLine(QPointF(8, 8), QPointF(14, 8))

    return _draw(paint)
