import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QCoreApplication, QRect, Qt
from PySide6.QtWidgets import QLabel, QWidget

from kubescope.views.flow_layout import FlowLayout
from tests.qt import get_application
from tests.test_window_flows import _ready_window

application = get_application()
KEPT: list[QWidget] = []  # until the end: a widget that goes first crashes Qt


def bar(count=4, width=100, height=20):
    holder = QWidget()
    KEPT.append(holder)
    flow = FlowLayout(holder, horizontal=10, vertical=6)
    labels = []
    for index in range(count):
        label = QLabel(f"w{index}")
        label.setFixedSize(width, height)
        flow.addWidget(label)
        labels.append(label)
    return holder, flow, labels


def test_the_widgets_go_on_a_row_and_then_wrap_to_the_next_one() -> None:
    _holder, flow, labels = bar()

    flow.setGeometry(QRect(0, 0, 250, 100))  # two fit on a row: 100 + 10 + 100

    assert [(label.x(), label.y()) for label in labels] == [
        (0, 0),
        (110, 0),
        (0, 26),
        (110, 26),
    ]
    assert flow.heightForWidth(250) == 46 and flow.hasHeightForWidth()
    assert flow.heightForWidth(1000) == 20  # all four on one row


def test_a_hidden_widget_takes_no_room_and_the_minimum_is_the_widest_one() -> None:
    holder, flow, labels = bar(count=3, width=80)
    labels[1].setFixedSize(150, 20)
    holder.show()
    labels[0].hide()

    flow.setGeometry(QRect(0, 0, 400, 100))

    assert labels[1].x() == 0  # the first one that shows starts the row
    assert flow.minimumSize().width() == 150
    assert flow.sizeHint() == flow.minimumSize()
    assert flow.expandingDirections() == Qt.Orientation(0)


def test_the_items_can_be_read_and_taken_away() -> None:
    _holder, flow, labels = bar(count=2)

    assert flow.count() == 2 and flow.itemAt(0) is not None
    assert flow.itemAt(5) is None and flow.takeAt(5) is None
    taken = flow.takeAt(0)
    assert taken is not None and flow.count() == 1
    labels[0].deleteLater()


def test_the_filters_of_the_events_wrap_instead_of_standing_over_each_other(
    monkeypatch,
) -> None:
    window = _ready_window(monkeypatch)
    window._open_list_view("events")
    window.show()
    window.setMinimumSize(0, 0)
    filters = window.ui.filtersBar

    for width in (1300, 800, 600):
        window.resize(width, 700)
        QCoreApplication.processEvents()
        shown = [
            widget
            for widget in filters.findChildren(QWidget)
            if widget.parent() is filters and widget.isVisibleTo(filters)
        ]
        for index, one in enumerate(shown):
            for other in shown[index + 1 :]:
                assert not one.geometry().intersects(other.geometry()), (
                    width,
                    one.objectName(),
                    other.objectName(),
                )
    assert filters.height() > 38  # a second row
    window.close()
