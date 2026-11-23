import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QTableWidget

from kubescope.views.check_header import CheckHeader

application = QApplication.instance() or QApplication([])


def make() -> tuple[QTableWidget, CheckHeader]:
    table = QTableWidget(2, 3)
    header = CheckHeader(table)
    table.setHorizontalHeader(header)
    table.setHorizontalHeaderLabels(["A", "B", "C"])
    table.resize(500, 200)
    table.show()
    return table, header


def test_a_header_has_a_box_in_one_section_and_draws_it() -> None:
    _table, header = make()
    header.set_column(1)

    for state in (
        Qt.CheckState.Unchecked,
        Qt.CheckState.PartiallyChecked,
        Qt.CheckState.Checked,
    ):
        header.set_check_state(state)
        image = header.grab().toImage()
        box = header._box()
        corner = image.pixelColor(box.center())
        assert (corner.red(), corner.green(), corner.blue()) != (0, 0, 0)
    header.set_check_state(Qt.CheckState.Checked)
    header.set_check_state(Qt.CheckState.Checked)  # the same: nothing to repaint
    header.set_column(1)  # the same column: nothing to repaint


def test_a_click_on_the_box_asks_to_check_all_or_none_and_does_not_sort() -> None:
    _table, header = make()
    header.set_column(1)
    asked: list[bool] = []
    header.toggled.connect(asked.append)
    box = header._box().center()

    QTest.mouseClick(header.viewport(), Qt.MouseButton.LeftButton, pos=box)
    header.set_check_state(Qt.CheckState.Checked)
    QTest.mouseClick(header.viewport(), Qt.MouseButton.LeftButton, pos=box)
    header.set_check_state(Qt.CheckState.PartiallyChecked)
    QTest.mouseClick(header.viewport(), Qt.MouseButton.LeftButton, pos=box)

    assert asked == [True, False, True]  # a partial one asks for all


def test_a_click_elsewhere_or_without_a_box_asks_nothing() -> None:
    _table, header = make()
    asked: list[bool] = []
    header.toggled.connect(asked.append)
    elsewhere = QPoint(header.sectionViewportPosition(2) + 40, 5)

    QTest.mouseClick(
        header.viewport(), Qt.MouseButton.LeftButton, pos=elsewhere
    )  # no box
    header.set_column(1)
    QTest.mouseClick(header.viewport(), Qt.MouseButton.LeftButton, pos=elsewhere)
    QTest.mouseClick(
        header.viewport(), Qt.MouseButton.RightButton, pos=header._box().center()
    )

    assert asked == []
