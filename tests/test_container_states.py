import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import (
    QApplication,
    QStyleOptionViewItem,
    QTableWidget,
    QTableWidgetItem,
)

from kubescope.views.container_states import (
    BADGE_PADDING,
    BADGE_ROLE,
    PADDING,
    BadgeDelegate,
)

application = QApplication.instance() or QApplication([])


def test_a_badge_asks_for_room_for_its_pill_on_top_of_an_empty_cell() -> None:
    table = QTableWidget(1, 3)  # kept: Qt deletes the delegate with its table
    badge = QTableWidgetItem("Running")  # its text is drawn by the pill
    badge.setData(BADGE_ROLE, ("#176b58", "#e5f4eb"))
    table.setItem(0, 0, badge)
    table.setItem(0, 1, QTableWidgetItem(""))
    table.setItem(0, 2, QTableWidgetItem("Running"))
    delegate = BadgeDelegate(table)
    option = QStyleOptionViewItem()

    def hint(column: int):
        return delegate.sizeHint(option, table.model().index(0, column))

    assert hint(0).width() == hint(1).width() + 2 * BADGE_PADDING + PADDING
    assert hint(0).height() == hint(1).height()
    assert hint(2).width() > hint(1).width()  # a plain cell asks for its text only
