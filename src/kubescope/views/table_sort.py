"""Sort a table when its header is clicked: ascending first, descending on the
next click on the same one, the way the lists of the app do.

Ages, numbers and versions sort by what they mean (`natural_key` of the
SDK), not by their letters. Two ways to do it: the sorter moves the rows
of the table (`HeaderSorter(table)`), for a table whose rows carry all
they need in their items; or it tells the owner which column and order
(`HeaderSorter(table, apply)`), for a table whose rows stand for a list
the owner keeps and draws again in that order.
"""

from collections.abc import Callable

from kubescope.sdk.models import natural_key
from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


class HeaderSorter(QObject):
    def __init__(
        self,
        table: QTableWidget,
        apply: Callable[[int, Qt.SortOrder], None] | None = None,
    ) -> None:
        super().__init__(table)
        self.table = table
        self.state: tuple[int, Qt.SortOrder] | None = None
        self._apply = apply
        header = table.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.clicked)

    def clicked(self, column: int) -> None:
        """A click on a header: sort by it, or reverse it if it is the one."""
        if self.state is not None and self.state[0] == column:
            flipped = self.state[1] == Qt.SortOrder.AscendingOrder
            order = (
                Qt.SortOrder.DescendingOrder if flipped else Qt.SortOrder.AscendingOrder
            )
        else:
            order = Qt.SortOrder.AscendingOrder
        self.state = (column, order)
        header = self.table.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(column, order)
        if self._apply is not None:
            self._apply(column, order)
        else:
            self.reapply()

    def reapply(self) -> None:
        """Put the rows in the order of the header clicked, again (the table
        was filled again, in the order it was read)."""
        if self.state is not None and self._apply is None:
            move_rows(self.table, *self.state)


def move_rows(table: QTableWidget, column: int, order: Qt.SortOrder) -> None:
    """Order the rows of a table by the text of a column."""
    rows = table.rowCount()
    columns = table.columnCount()
    taken: list[list[QTableWidgetItem | None]] = [
        [table.takeItem(row, one) for one in range(columns)] for row in range(rows)
    ]

    def key(cells: list[QTableWidgetItem | None]) -> tuple:
        item = cells[column] if column < len(cells) else None
        return natural_key(item.text() if item is not None else "")

    taken.sort(key=key, reverse=order == Qt.SortOrder.DescendingOrder)
    table.clearSelection()
    for row, cells in enumerate(taken):
        for one, item in enumerate(cells):
            if item is not None:
                table.setItem(row, one, item)
