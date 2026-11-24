import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from kubescope.views.table_sort import HeaderSorter, move_rows
from tests.qt import get_application

application = get_application()
KEPT: list[QTableWidget] = []  # until the end: a table that goes first crashes Qt


def table(*rows: tuple[str, ...]) -> QTableWidget:
    one = QTableWidget(len(rows), 2)
    KEPT.append(one)
    for row, cells in enumerate(rows):
        for column, text in enumerate(cells):
            one.setItem(row, column, QTableWidgetItem(text))
    return one


def column(one: QTableWidget, index: int) -> list[str]:
    return [one.item(row, index).text() for row in range(one.rowCount())]  # type: ignore[union-attr]


def test_the_rows_move_with_all_their_cells_by_what_the_column_means() -> None:
    one = table(("b", "2d"), ("a", "5m"), ("c", "1h"))

    move_rows(one, 1, Qt.SortOrder.AscendingOrder)

    assert column(one, 1) == ["5m", "1h", "2d"]
    assert column(one, 0) == ["a", "c", "b"]  # each row kept its own cells

    move_rows(one, 0, Qt.SortOrder.DescendingOrder)

    assert column(one, 0) == ["c", "b", "a"]


def test_a_cell_that_is_missing_sorts_as_empty_and_goes_last() -> None:
    one = QTableWidget(2, 2)
    KEPT.append(one)
    one.setItem(0, 0, QTableWidgetItem("x"))  # no second cell
    one.setItem(1, 0, QTableWidgetItem("y"))
    one.setItem(1, 1, QTableWidgetItem("1"))

    move_rows(one, 1, Qt.SortOrder.AscendingOrder)

    assert one.item(0, 0).text() == "y"  # type: ignore[union-attr]
    assert one.item(1, 1) is None


def test_a_click_sorts_a_second_one_reverses_it_and_another_column_starts_over() -> (
    None
):
    one = table(("b", "2"), ("a", "10"), ("c", "1"))
    sorter = HeaderSorter(one)

    sorter.clicked(1)
    assert column(one, 1) == ["1", "2", "10"]
    assert one.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.AscendingOrder  # type: ignore[union-attr]

    sorter.clicked(1)
    assert column(one, 1) == ["10", "2", "1"]

    sorter.clicked(0)
    assert column(one, 0) == ["a", "b", "c"]


def test_a_table_that_is_filled_again_is_put_in_the_order_chosen() -> None:
    one = table(("b", "1"), ("a", "2"))
    sorter = HeaderSorter(one)
    sorter.clicked(0)

    for row, (first, second) in enumerate((("z", "1"), ("y", "2"))):
        one.setItem(row, 0, QTableWidgetItem(first))
        one.setItem(row, 1, QTableWidgetItem(second))
    sorter.reapply()

    assert column(one, 0) == ["y", "z"]


def test_an_owner_that_keeps_the_list_is_told_the_column_and_the_order() -> None:
    one = table(("b", "1"))
    told: list[tuple[int, Qt.SortOrder]] = []
    sorter = HeaderSorter(one, lambda col, order: told.append((col, order)))

    sorter.clicked(1)
    sorter.clicked(1)
    sorter.reapply()  # nothing to move: the owner draws the table

    assert told == [
        (1, Qt.SortOrder.AscendingOrder),
        (1, Qt.SortOrder.DescendingOrder),
    ]
    assert column(one, 0) == ["b"]
