from PySide6.QtCore import QModelIndex, QPersistentModelIndex, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
)

from kubescope.theme import themed

STATES_ROLE = Qt.ItemDataRole.UserRole + 1
KEEP_TEXT_ROLE = Qt.ItemDataRole.UserRole + 2  # the cell shows its text too
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
    containers of a Pod or the replicas of a workload; the text of the cell is
    kept, aligned to the right, only when the cell asks for it."""

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        states = index.data(STATES_ROLE)
        if not states:
            super().paint(painter, option, index)
            return
        style = option.widget.style() if option.widget else None
        if index.data(KEEP_TEXT_ROLE):
            super().paint(painter, option, index)
        elif style is not None:
            blank = QStyleOptionViewItem(option)
            self.initStyleOption(blank, index)
            blank.text = ""
            style.drawControl(QStyle.ControlElement.CE_ItemViewItem, blank, painter)
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
        if index.data(KEEP_TEXT_ROLE):
            width += hint.width()
        return QSize(width, hint.height())
