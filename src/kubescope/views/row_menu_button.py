"""The "⋯" that shows at the end of the row under the pointer and opens the
menu of that row, so what the right click offers is in sight too."""

from PySide6.QtCore import QCoreApplication, QEvent, QObject, QPoint, QTimer, Signal
from PySide6.QtWidgets import QTableWidget, QToolButton

WIDTH = 26
MARGIN = 6  # from the right edge of the table


class RowMenuButton(QToolButton):
    """A button floating over the right end of the hovered row of a table."""

    requested = Signal(QPoint)  # where the menu belongs: in the viewport

    def __init__(self, table: QTableWidget) -> None:
        super().__init__(table.viewport())
        self._table = table
        self.setText("⋯")
        label = QCoreApplication.translate("RowMenuButton", "Actions for this row")
        self.setToolTip(label)
        self.setAccessibleName(label)
        self.setAutoRaise(True)
        self.setProperty("rowMenu", True)
        self.hide()
        table.viewport().setMouseTracking(True)
        table.viewport().installEventFilter(self)
        table.verticalScrollBar().valueChanged.connect(self.hide)
        self.clicked.connect(self._clicked)

    def _clicked(self) -> None:
        self.requested.emit(QPoint(self.x(), self.y() + self.height() // 2))

    def show_on(self, row: int) -> None:
        """Float over the end of `row`, or hide when there is no such row."""
        if row < 0 or row >= self._table.rowCount() or self._table.isRowHidden(row):
            self.hide()
            return
        height = max(self._table.rowHeight(row) - 8, 16)
        self.setFixedSize(WIDTH, height)
        viewport = self._table.viewport()
        self.move(
            viewport.width() - WIDTH - MARGIN,
            self._table.rowViewportPosition(row)
            + (self._table.rowHeight(row) - height) // 2,
        )
        self.show()
        self.raise_()

    def _leave(self) -> None:
        if not self.underMouse() and not self._table.viewport().underMouse():
            self.hide()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.MouseMove:
            self.show_on(self._table.rowAt(event.position().toPoint().y()))  # type: ignore[attr-defined]
        elif event.type() == QEvent.Type.Leave:
            QTimer.singleShot(60, self._leave)  # the pointer may be on the button
        return False
