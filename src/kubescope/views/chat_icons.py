"""The small icons of the buttons that save, close and confirm, drawn so no
font has to have them."""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import QAbstractButton

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


def save_icon(color: str = "#ffffff") -> QIcon:
    """A floppy disk, for saving changes."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        body = QPainterPath()
        body.moveTo(4, 3)
        body.lineTo(15, 3)
        body.lineTo(19, 7)
        body.lineTo(19, 17)
        body.quadTo(19, 19, 17, 19)
        body.lineTo(5, 19)
        body.quadTo(3, 19, 3, 17)
        body.lineTo(3, 5)
        body.quadTo(3, 3, 4, 3)
        painter.drawPath(body)
        painter.drawRect(QRectF(7, 3, 6, 4))
        painter.drawRoundedRect(QRectF(6, 12, 10, 7), 1, 1)

    return _draw(paint)


def close_icon(color: str = "#ffffff") -> QIcon:
    """A cross, for cancelling and closing."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_pen(color, 2.0))
        painter.drawLine(QPointF(5, 5), QPointF(17, 17))
        painter.drawLine(QPointF(17, 5), QPointF(5, 17))

    return _draw(paint)


def check_icon(color: str = "#ffffff") -> QIcon:
    """A tick, for what was done."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_pen(color, 2.4))
        painter.drawLine(QPointF(4.5, 11.5), QPointF(9, 16))
        painter.drawLine(QPointF(9, 16), QPointF(17.5, 6))

    return _draw(paint)


def icon_only(button: QAbstractButton, tip: str, icon: QIcon) -> None:
    """Show a button as its icon alone, with the words as its tip."""
    button.setText("")
    button.setIcon(icon)
    button.setToolTip(tip)
    button.setFixedSize(36, 36)
