"""The icons an extension may ask for by name (`Components.icon`), drawn three
times larger so their edges stay smooth."""

from collections.abc import Callable
from math import cos, pi, sin

from PySide6.QtCore import QPointF, QRectF, QSize, Qt
from PySide6.QtGui import (
    QColor,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
)

SIZE = 18
CHAT_SIZE = 22


def _canvas(draw: Callable[[QPainter], None]) -> QIcon:
    size = SIZE * 3
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    draw(painter)
    painter.end()
    return QIcon(
        pixmap.scaled(
            QSize(SIZE, SIZE),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
    )


def _pen(color: str, width: int, join: bool = True) -> QPen:
    pen = QPen(QColor(color), width)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    if join:
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    return pen


def _chat_canvas(paint: Callable[[QPainter], None]) -> QIcon:
    """Drawn at twice the size, for sharp edges (the small round buttons of the
    chat)."""
    pixmap = QPixmap(CHAT_SIZE * 2, CHAT_SIZE * 2)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(2, 2)
    paint(painter)
    painter.end()
    return QIcon(pixmap)


def _chat_pen(color: str, width: float = 2.0) -> QPen:
    pen = QPen(QColor(color), width)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    return pen


def update_icon(color: str) -> QIcon:
    """The arrow that says a newer version is out."""

    def draw(painter: QPainter) -> None:
        painter.setPen(_pen(color, 6))
        painter.drawLine(27, 42, 27, 12)  # an arrow rising from a base
        painter.drawLine(16, 23, 27, 12)
        painter.drawLine(38, 23, 27, 12)
        painter.drawLine(12, 46, 42, 46)

    return _canvas(draw)


def info_icon(color: str) -> QIcon:
    """A circle with an i, for the button of the details."""

    def draw(painter: QPainter) -> None:
        painter.setPen(_pen(color, 5, join=False))
        painter.drawEllipse(7, 7, 40, 40)
        painter.drawLine(27, 25, 27, 38)
        painter.drawPoint(27, 17)

    return _canvas(draw)


def trash_icon(color: str) -> QIcon:
    """A bin, for the button that uninstalls."""

    def draw(painter: QPainter) -> None:
        painter.setPen(_pen(color, 5))
        painter.drawLine(10, 16, 44, 16)  # the lid
        painter.drawLine(21, 16, 21, 10)
        painter.drawLine(33, 16, 33, 10)
        painter.drawLine(21, 10, 33, 10)
        painter.drawLine(14, 16, 17, 44)  # the body
        painter.drawLine(40, 16, 37, 44)
        painter.drawLine(17, 44, 37, 44)

    return _canvas(draw)


def refresh_icon(color: str) -> QIcon:
    """A circular arrow, for the button that reads again or resyncs."""

    def draw(painter: QPainter) -> None:
        painter.setPen(_pen(color, 5))
        center = QPointF(27, 27)
        radius = 16.0
        start, span = 60, 270  # degrees, counterclockwise as Qt counts them
        painter.drawArc(
            QRectF(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius),
            start * 16,
            span * 16,
        )
        end = (start + span) * pi / 180  # the arrow sits where the arc ends
        tip = QPointF(center.x() + radius * cos(end), center.y() - radius * sin(end))
        heading = pi / 2 + end  # the way the arc goes there, on the screen
        back = heading + pi
        for turn in (0.45, -0.45):
            painter.drawLine(
                tip,
                QPointF(
                    tip.x() + 14 * cos(back + turn),
                    tip.y() - 14 * sin(back + turn),
                ),
            )

    return _canvas(draw)


def bell_icon(color: str) -> QIcon:
    """A bell, for the button of the notifications."""

    def draw(painter: QPainter) -> None:
        painter.scale(3, 3)
        body = QPainterPath()
        body.moveTo(9, 2.2)
        body.cubicTo(5.6, 2.2, 4.4, 4.8, 4.4, 7.4)
        body.lineTo(4.4, 10.6)
        body.lineTo(2.8, 12.6)
        body.lineTo(2.8, 13.4)
        body.lineTo(15.2, 13.4)
        body.lineTo(15.2, 12.6)
        body.lineTo(13.6, 10.6)
        body.lineTo(13.6, 7.4)
        body.cubicTo(13.6, 4.8, 12.4, 2.2, 9, 2.2)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawPath(body)
        painter.drawEllipse(QPointF(9, 15.1), 1.9, 1.5)  # the clapper

    return _canvas(draw)


def chat_send_icon(color: str = "#ffffff") -> QIcon:
    """A paper plane."""

    def paint(painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawPolygon(
            QPolygonF([QPointF(3, 3), QPointF(19, 11), QPointF(3, 19), QPointF(6, 11)])
        )

    return _chat_canvas(paint)


def chat_stop_icon(color: str = "#ffffff") -> QIcon:
    """A square."""

    def paint(painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawRoundedRect(QRectF(6, 6, 10, 10), 2, 2)

    return _chat_canvas(paint)


def chat_attach_icon(color: str = "#8696a0") -> QIcon:
    """A plus."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 2.2))
        painter.drawLine(QPointF(11, 4), QPointF(11, 18))
        painter.drawLine(QPointF(4, 11), QPointF(18, 11))

    return _chat_canvas(paint)


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


def chat_sparkle_icon(
    color: str = "#ffffff", size: int = CHAT_SIZE, inside: str = "#3220a0"
) -> QIcon:
    """A speech bubble with the star of an AI inside it."""
    pixmap = QPixmap(size * 2, size * 2)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(2 * size / CHAT_SIZE, 2 * size / CHAT_SIZE)
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


def chat_popout_icon(color: str = "#ffffff") -> QIcon:
    """A square with an arrow leaving it, for taking the chat out of the
    window."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(3, 7, 12, 12), 2, 2)
        painter.drawLine(QPointF(10, 12), QPointF(19, 3))
        painter.drawLine(QPointF(12, 3), QPointF(19, 3))
        painter.drawLine(QPointF(19, 3), QPointF(19, 10))

    return _chat_canvas(paint)


def chat_dock_icon(color: str = "#ffffff") -> QIcon:
    """A square with an arrow entering it, for putting the chat back."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(3, 3, 16, 16), 2, 2)
        painter.drawLine(QPointF(8, 8), QPointF(15, 15))
        painter.drawLine(QPointF(8, 14), QPointF(8, 8))
        painter.drawLine(QPointF(8, 8), QPointF(14, 8))

    return _chat_canvas(paint)


def chat_gear_icon(color: str = "#ffffff") -> QIcon:
    """A cog, for the settings."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(11, 11), 3, 3)
        for step in range(8):
            angle = step * pi / 4
            painter.drawLine(
                QPointF(11 + 6.5 * cos(angle), 11 + 6.5 * sin(angle)),
                QPointF(11 + 9 * cos(angle), 11 + 9 * sin(angle)),
            )
        painter.drawEllipse(QPointF(11, 11), 6.5, 6.5)

    return _chat_canvas(paint)


def chat_trash_icon(color: str = "#ffffff") -> QIcon:
    """A bin, for clearing."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(QPointF(4, 6), QPointF(18, 6))
        painter.drawLine(QPointF(9, 6), QPointF(9, 3.5))
        painter.drawLine(QPointF(9, 3.5), QPointF(13, 3.5))
        painter.drawLine(QPointF(13, 3.5), QPointF(13, 6))
        painter.drawLine(QPointF(6, 6), QPointF(7, 18.5))
        painter.drawLine(QPointF(7, 18.5), QPointF(15, 18.5))
        painter.drawLine(QPointF(15, 18.5), QPointF(16, 6))
        painter.drawLine(QPointF(9.5, 9), QPointF(9.8, 15.5))
        painter.drawLine(QPointF(12.5, 9), QPointF(12.2, 15.5))

    return _chat_canvas(paint)


def chat_close_icon(color: str = "#ffffff") -> QIcon:
    """A cross, for cancelling and closing."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 2.0))
        painter.drawLine(QPointF(5, 5), QPointF(17, 17))
        painter.drawLine(QPointF(17, 5), QPointF(5, 17))

    return _chat_canvas(paint)


def chat_plus_icon(color: str = "#ffffff") -> QIcon:
    """A plus, for a new session."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 2.0))
        painter.drawLine(QPointF(11, 4.5), QPointF(11, 17.5))
        painter.drawLine(QPointF(4.5, 11), QPointF(17.5, 11))

    return _chat_canvas(paint)


def chat_focus_icon(color: str = "#ffffff", active: bool = False) -> QIcon:
    """Four corners that point out, to fill the window with the chat, or in, to
    leave that mode."""

    def paint(painter: QPainter) -> None:
        painter.setPen(_chat_pen(color, 1.8))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        near, far = (8.0, 14.0) if active else (3.5, 18.5)
        sign = -1 if active else 1  # the legs go out of the corners that are in
        for x, y, dx, dy in (
            (near, near, sign, sign),
            (far, near, -sign, sign),
            (near, far, sign, -sign),
            (far, far, -sign, -sign),
        ):
            painter.drawLine(QPointF(x, y), QPointF(x + 4 * dx, y))
            painter.drawLine(QPointF(x, y), QPointF(x, y + 4 * dy))

    return _chat_canvas(paint)


ICONS: dict[str, Callable[[str], QIcon]] = {
    "update": update_icon,
    "info": info_icon,
    "trash": trash_icon,
    "refresh": refresh_icon,
    "bell": bell_icon,
    "send": chat_send_icon,
    "stop": chat_stop_icon,
    "attach": chat_attach_icon,
    "popout": chat_popout_icon,
    "dock": chat_dock_icon,
    "gear": chat_gear_icon,
    "chat-trash": chat_trash_icon,
    "close": chat_close_icon,
    "plus": chat_plus_icon,
}
FOCUS_ICON = chat_focus_icon
SPARKLE_ICON = chat_sparkle_icon
