import time

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFont, QHelpEvent, QPainter
from PySide6.QtWidgets import (
    QAbstractItemView,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
)

from kubescope.models import age_seconds, format_age
from kubescope.theme import themed

STATES_ROLE = Qt.ItemDataRole.UserRole + 1
LINK_ROLE = Qt.ItemDataRole.UserRole + 4  # (kind, namespace, name) a cell opens
TIPS_ROLE = Qt.ItemDataRole.UserRole + 3  # what each square says when pointed at
# state of a container -> its square: running, pending, error or terminated
BADGE_ROLE = Qt.ItemDataRole.UserRole + 5  # (text color, fill color) of a badge
TINT_ROLE = Qt.ItemDataRole.UserRole + 6  # the color a whole row is washed with
AGE_ROLE = Qt.ItemDataRole.UserRole + 7  # (seconds old, clock when that was read)
STATE_COLORS = {
    "running": "#3cb95a",
    "pending": "#e0a526",
    "error": "#d64550",
    "terminated": "#8b94a0",
}
SQUARE = 12
GAP = 4
PADDING = 8


BADGE_PADDING = 10
BADGE_HEIGHT = 20


class BadgeDelegate(QStyledItemDelegate):
    """Draws the text of a cell as a badge, a rounded outlined pill, when the
    cell carries the colors of one; any other cell is drawn as usual.

    A cell that carries a row tint is washed with it first: the style sheet of
    the tables styles the items, which leaves their background role unused.
    """

    def initStyleOption(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        super().initStyleOption(option, index)
        if index.data(BADGE_ROLE):
            option.text = ""  # the badge draws the text

    @staticmethod
    def _font(option: QStyleOptionViewItem) -> QFont:
        font = QFont(option.font)
        font.setBold(True)
        return font

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        tint = index.data(TINT_ROLE)
        if tint and not option.state & QStyle.StateFlag.State_Selected:
            painter.fillRect(option.rect, tint)
        colors = index.data(BADGE_ROLE)
        super().paint(painter, option, index)  # the cell, without text for a badge
        if not colors:
            return
        text_color, fill = (QColor(color) for color in colors)
        text = str(index.data(Qt.ItemDataRole.DisplayRole) or "")
        font = self._font(option)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setFont(font)
        width = painter.fontMetrics().horizontalAdvance(text) + 2 * BADGE_PADDING
        rect = QRectF(
            option.rect.left() + PADDING,
            option.rect.top() + (option.rect.height() - BADGE_HEIGHT) / 2,
            min(width, option.rect.width() - PADDING),
            BADGE_HEIGHT,
        )
        border = QColor(text_color)
        border.setAlpha(90)
        painter.setPen(border)
        painter.setBrush(fill)
        painter.drawRoundedRect(rect, BADGE_HEIGHT / 2, BADGE_HEIGHT / 2)
        painter.setPen(text_color)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
        painter.restore()

    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QSize:
        hint = super().sizeHint(option, index)
        if not index.data(BADGE_ROLE):
            return hint
        return QSize(hint.width() + 2 * BADGE_PADDING + PADDING, hint.height())


class ContainerStatesDelegate(BadgeDelegate):
    """Draws a small colored square for each state a cell carries, such as the
    containers of a Pod or the replicas of a workload; the text of the cell,
    aligned to the right, says how many."""

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        states = index.data(STATES_ROLE)
        super().paint(painter, option, index)  # a badge or the plain cell
        if not states:
            return
        top = option.rect.top() + (option.rect.height() - SQUARE) / 2
        left = option.rect.left() + PADDING
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        for number, state in enumerate(states):
            color = STATE_COLORS.get(state, STATE_COLORS["terminated"])
            painter.setBrush(QColor(themed(color)))
            x = left + number * (SQUARE + GAP)
            painter.drawRoundedRect(QRectF(x, top, SQUARE, SQUARE), 2, 2)
        painter.restore()

    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> QSize:
        states = index.data(STATES_ROLE)
        if not states:
            return super().sizeHint(option, index)
        hint = super().sizeHint(option, index)
        width = 2 * PADDING + len(states) * SQUARE + (len(states) - 1) * GAP
        return QSize(width + hint.width(), hint.height())

    def helpEvent(
        self,
        event: QHelpEvent,
        view: QAbstractItemView,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> bool:
        tips = index.data(TIPS_ROLE)
        if not tips:
            return super().helpEvent(event, view, option, index)
        offset = event.pos().x() - option.rect.left() - PADDING
        number, within = divmod(offset, SQUARE + GAP)
        if 0 <= number < len(tips) and within < SQUARE:
            QToolTip.showText(event.globalPos(), tips[number], view)
        else:
            QToolTip.hideText()
        return True


LIVE_AGE_SECONDS = 60  # only a young age is worth redrawing every second


def stamp_age(item: QTableWidgetItem, age: str) -> None:
    """Mark a cell as an age that counts the seconds while it is under a
    minute; older and unknown ages stay as they are, until the list reloads."""
    seconds = age_seconds(age)
    if seconds < LIVE_AGE_SECONDS:
        item.setData(AGE_ROLE, (seconds, time.monotonic()))


def tick_ages(table: QTableWidget) -> None:
    """Move every counting age of a table on to now."""
    now = time.monotonic()
    for row in range(table.rowCount()):
        for column in range(table.columnCount()):
            item = table.item(row, column)
            if item is None:
                continue
            stamp = item.data(AGE_ROLE)
            if stamp is not None:
                seconds = stamp[0] + now - stamp[1]
                text = format_age(seconds)
                if item.text() != text:
                    item.setText(text)
                if seconds >= LIVE_AGE_SECONDS:
                    item.setData(AGE_ROLE, None)  # a minute old: stop counting
