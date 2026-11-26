import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from kubescope.views.row_menu_button import WIDTH, RowMenuButton
from tests.qt import get_application

application = get_application()


def _table() -> QTableWidget:
    table = QTableWidget(5, 2)
    for row in range(5):
        table.setItem(row, 0, QTableWidgetItem(f"row {row}"))
    table.resize(400, 300)
    table.show()
    return table


def test_the_button_floats_over_the_end_of_the_hovered_row() -> None:
    table = _table()
    button = RowMenuButton(table)
    assert button.isHidden() and button.accessibleName()

    QTest.mouseMove(table.viewport(), QPoint(20, table.rowViewportPosition(2) + 5))
    assert button.isVisible()
    top = table.rowViewportPosition(2)
    assert top <= button.y() < top + table.rowHeight(2)
    assert button.x() + WIDTH <= table.viewport().width()

    table.setRowHidden(3, True)
    button.show_on(3)  # a row that is hidden, or not there, has no button
    assert button.isHidden()
    button.show_on(1)
    button.show_on(99)
    assert button.isHidden()
    table.close()


def test_the_button_asks_for_the_menu_beside_itself() -> None:
    table = _table()
    button = RowMenuButton(table)
    asked: list[QPoint] = []
    button.requested.connect(asked.append)
    button.show_on(1)

    QTest.mouseClick(button, Qt.MouseButton.LeftButton)
    assert len(asked) == 1
    assert table.rowAt(asked[0].y()) == 1
    table.close()


def test_the_button_goes_away_when_the_pointer_leaves() -> None:
    table = _table()
    button = RowMenuButton(table)
    button.show_on(0)
    button._leave()  # nothing under the pointer in a test
    assert button.isHidden()
    table.close()
