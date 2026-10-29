"""The small round-button icons of the chat, drawn so no font has to have
them."""

from math import cos, pi, sin

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap, QPolygonF

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


def mic_icon(color: str = "#8696a0") -> QIcon:
    """A microphone."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(8, 3, 6, 10), 3, 3)
        painter.drawArc(QRectF(5, 7, 12, 9), 0, -180 * 16)
        painter.drawLine(QPointF(11, 16), QPointF(11, 19))

    return _draw(paint)


def _star(painter: QPainter, x: float, y: float, radius: float) -> None:
    """A four-pointed star centered at (x, y)."""
    inner = radius * 0.28
    points = []
    for index in range(8):
        reach = radius if index % 2 == 0 else inner
        angle = index * pi / 4
        points.append(
            QPointF(x + reach * sin(angle), y - reach * cos(angle)),
        )
    painter.drawPolygon(QPolygonF(points))


def sparkle_icon(color: str = "#ffffff", size: int = SIZE) -> QIcon:
    """The sparkles that stand for an AI: a large star and two small ones."""
    pixmap = QPixmap(size * 2, size * 2)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(2 * size / SIZE, 2 * size / SIZE)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))
    _star(painter, 9.5, 12.5, 8)
    _star(painter, 17.5, 5.5, 4)
    _star(painter, 18, 17, 2.8)
    painter.end()
    return QIcon(pixmap)
