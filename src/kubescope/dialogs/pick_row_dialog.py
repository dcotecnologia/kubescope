"""A table to pick one row of, narrowed by what the person types and, when the
rows have a date, by a range of dates (`YYYY-MM-DD`)."""

import datetime
import re

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from kubescope.extensions.components import UiComponents


def _day(text: str) -> datetime.date | None:
    """The day a field says, or nothing while it is empty or not a date yet."""
    try:
        return datetime.date.fromisoformat(text.strip())
    except ValueError:
        return None


def _natural(text: str) -> list[tuple[int, int, str]]:
    """A key that puts `9 KiB` before `10 KiB`."""
    return [
        (0, int(part), "") if part.isdigit() else (1, 0, part.casefold())
        for part in re.split(r"(\d+)", text)
        if part
    ]


class PickRowDialog(QDialog):
    def __init__(
        self,
        parent: QWidget,
        components: UiComponents,
        title: str,
        label: str,
        headers: list[str],
        rows: list[list[str]],
        moments: list[datetime.datetime] | None,
        texts: dict[str, str],
    ) -> None:
        """`texts` are the words of the window: search, from, to, cancel,
        ok."""
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(760, 460)
        self._rows = rows
        self._shown: list[int] = []
        self._days = [one.date() for one in moments] if moments else []
        self._order: tuple[int, bool] | None = None  # the column and if descending
        self.picked = -1  # the index in `rows` of the one chosen
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(QLabel(label))
        filters = QHBoxLayout()
        self.search = components.search_box(texts["search"])
        self.search.setMaximumWidth(16777215)
        self.search.textChanged.connect(self._narrow)
        filters.addWidget(self.search, 1)
        self.first = components.text_field(f"{texts['from']} YYYY-MM-DD")
        self.last = components.text_field(f"{texts['to']} YYYY-MM-DD")
        for edit in (self.first, self.last):
            edit.setFixedWidth(170)
            edit.setClearButtonEnabled(True)
            edit.setVisible(bool(self._days))
            edit.textChanged.connect(self._narrow)
            filters.addWidget(edit)
        layout.addLayout(filters)
        self._components = components
        self.table = components.data_table(headers, [330, 90])
        self.sorter = components.header_sorter(self.table, self._sort)
        self.table.itemDoubleClicked.connect(lambda _item: self._accept())
        layout.addWidget(self.table, 1)
        self.count = QLabel()
        layout.addWidget(self.count)
        actions = QHBoxLayout()
        actions.addStretch()
        cancel = components.button(texts["cancel"], "secondary", on_click=self.reject)
        self.ok = components.button(texts["ok"], "primary", on_click=self._accept)
        self.ok.setDefault(True)
        actions.addWidget(cancel)
        actions.addWidget(self.ok)
        layout.addLayout(actions)
        self.table.itemSelectionChanged.connect(self._sync)
        self._narrow()
        self.search.setFocus()

    def _narrow(self, *_args: object) -> None:
        """Show the rows that have the text and fall in the range."""
        text = self.search.text().casefold()
        low, high = _day(self.first.text()), _day(self.last.text())
        self._shown = [
            index
            for index, row in enumerate(self._rows)
            if text in " ".join(row).casefold()
            and (not self._days or low is None or self._days[index] >= low)
            and (not self._days or high is None or self._days[index] <= high)
        ]
        if self._order is not None:
            column, descending = self._order
            self._shown.sort(
                key=lambda index: _natural(self._rows[index][column]),
                reverse=descending,
            )
        self.table.setRowCount(len(self._shown))
        for line, index in enumerate(self._shown):
            for column, value in enumerate(self._rows[index]):
                self.table.setItem(line, column, self._components.table_item(value))
        if self._shown:
            self.table.selectRow(0)
        self.count.setText(f"{len(self._shown)} / {len(self._rows)}")
        self._sync()

    def _sort(self, column: int, descending: bool) -> None:
        """A click on a header: the rows in the order of that column."""
        self._order = (column, descending)
        self._narrow()

    def _sync(self) -> None:
        self.ok.setEnabled(self.table.currentRow() >= 0)

    def _accept(self) -> None:
        line = self.table.currentRow()
        if line >= 0:
            self.picked = self._shown[line]
            self.accept()
