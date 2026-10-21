from PySide6.QtCore import QModelIndex, QPersistentModelIndex, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QHelpEvent, QPainter
from PySide6.QtWidgets import (
    QAbstractItemView,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QToolTip,
)

from kubescope.theme import themed

STATES_ROLE = Qt.ItemDataRole.UserRole + 1
LINK_ROLE = Qt.ItemDataRole.UserRole + 4  # (kind, namespace, name) a cell opens
TIPS_ROLE = Qt.ItemDataRole.UserRole + 3  # what each square says when pointed at
# state of a container -> its square: running, pending, error or terminated
STATE_COLORS = {
    "running": "#3cb95a",
    "pending": "#e0a526",
    "error": "#d64550",
    "terminated": "#8b94a0",
}
SQUARE = 12
GAP = 4
PADDING = 8


class ContainerStatesDelegate(QStyledItemDelegate):
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
        super().paint(painter, option, index)
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
