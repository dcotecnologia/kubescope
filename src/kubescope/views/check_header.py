"""A table header with a check box in one of its sections, to check every row
at once, as the lists of Lens have."""

from PySide6.QtCore import QPointF, QRect, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QHeaderView, QWidget

from kubescope.theme import themed

BOX = 16  # px, the same as the boxes of the rows
LEFT = 8  # px between the left edge of the section and the box
SHIFT = LEFT + BOX + 8  # what the title of the section moves to the right


class CheckHeader(QHeaderView):
    """The header of a table; `set_column` puts a check box in the section of
    that column, `set_check_state` says what it shows, and `toggled` says what the
    person asked: every row checked (True) or none (False)."""

    toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.column = -1
        self.check_state = Qt.CheckState.Unchecked

    def set_column(self, column: int) -> None:
        """The column whose section has the check box; -1 for none."""
        if column != self.column:
            self.column = column
            self.viewport().update()

    @property
    def checked(self) -> bool | None:
        """What the box shows: checked, not, or `None` for some rows."""
        if self.check_state == Qt.CheckState.PartiallyChecked:
            return None
        return self.check_state == Qt.CheckState.Checked

    def set_checked(self, state: bool | None) -> None:
        """What the box shows: checked, not, or `None` for some rows."""
        self.set_check_state(
            Qt.CheckState.PartiallyChecked
            if state is None
            else Qt.CheckState.Checked
            if state
            else Qt.CheckState.Unchecked
        )

    def set_check_state(self, state: Qt.CheckState) -> None:
        if state != self.check_state:
            self.check_state = state
            self.viewport().update()

    def _box(self) -> QRect:
        left = self.sectionViewportPosition(self.column)
        top = (self.height() - BOX) // 2
        return QRect(left + LEFT, top, BOX, BOX)

    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        if logicalIndex != self.column:
            super().paintSection(painter, rect, logicalIndex)
            return
        painter.save()
        super().paintSection(painter, rect.adjusted(SHIFT, 0, 0, 0), logicalIndex)
        painter.restore()
        strip = QRect(rect.left(), rect.top(), SHIFT, rect.height())
        painter.fillRect(strip, QColor(themed("#fbfbfc")))  # as the section is
        painter.setPen(QColor(themed("#dfe2e9")))
        painter.drawLine(strip.bottomLeft(), strip.bottomRight())
        self._draw_box(painter, QRectF(self._box()))

    def _draw_box(self, painter: QPainter, box: QRectF) -> None:
        checked = self.check_state != Qt.CheckState.Unchecked
        accent = QColor(themed("#6252b5"))
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        border = accent if checked else QColor(themed("#8a919c"))
        painter.setPen(QPen(border, 2))
        painter.setBrush(accent if checked else QColor(themed("#ffffff")))
        painter.drawRoundedRect(box.adjusted(1, 1, -1, -1), 5, 5)
        if checked:
            painter.setPen(QPen(QColor(themed("#ffffff")), 2))
            if self.check_state == Qt.CheckState.PartiallyChecked:
                y = box.center().y()
                painter.drawLine(
                    QPointF(box.left() + 4, y), QPointF(box.right() - 4, y)
                )
            else:
                tick = QPainterPath()
                tick.moveTo(box.left() + 4, box.center().y())
                tick.lineTo(box.center().x() - 1, box.bottom() - 4.5)
                tick.lineTo(box.right() - 3.5, box.top() + 4.5)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawPath(tick)
        painter.restore()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if (
            self.column >= 0
            and e.button() == Qt.MouseButton.LeftButton
            and self._box().adjusted(-4, -4, 4, 4).contains(e.position().toPoint())
        ):
            self.toggled.emit(self.check_state != Qt.CheckState.Checked)
            return  # it is not a click to sort
        super().mousePressEvent(e)
