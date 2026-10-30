import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem

from kubescope.views import container_states
from kubescope.views.container_states import stamp_age, tick_ages

application = QApplication.instance() or QApplication([])


def test_ages_keep_counting_and_unknown_ones_stay(monkeypatch) -> None:
    table = QTableWidget(1, 2)
    clock = iter([100.0, 107.0])
    monkeypatch.setattr(container_states.time, "monotonic", lambda: next(clock))
    counting, unknown = QTableWidgetItem("10s"), QTableWidgetItem("unknown")
    stamp_age(counting, "10s")
    stamp_age(unknown, "unknown")
    table.setItem(0, 0, counting)
    table.setItem(0, 1, unknown)
    tick_ages(table)
    assert counting.text() == "17s"
    assert unknown.text() == "unknown"


def test_an_age_stops_counting_at_a_minute(monkeypatch) -> None:
    table = QTableWidget(1, 2)
    clock = iter([100.0, 110.0, 120.0])
    monkeypatch.setattr(container_states.time, "monotonic", lambda: next(clock))
    young, old = QTableWidgetItem("55s"), QTableWidgetItem("1m0s")
    stamp_age(young, "55s")
    stamp_age(old, "1m0s")
    table.setItem(0, 0, young)
    table.setItem(0, 1, old)
    tick_ages(table)
    tick_ages(table)

    assert young.text() == "1m5s"  # crossed the minute on this tick
    assert old.text() == "1m0s"  # never counted


def test_a_cell_without_an_item_is_skipped() -> None:
    table = QTableWidget(1, 2)
    item = QTableWidgetItem("1m0s")
    table.setItem(0, 1, item)  # the first cell has no item

    tick_ages(table)

    assert item.text() == "1m0s"


def test_the_window_ticks_the_ages_of_the_tables_it_shows(monkeypatch) -> None:
    from tests.test_window_flows import _ready_window

    window = _ready_window(monkeypatch)
    window.show()
    window._open_list_view("services")
    window.table.setRowCount(1)
    item = QTableWidgetItem("1m0s")
    item.setData(
        container_states.AGE_ROLE, (30.0, container_states.time.monotonic() - 5)
    )
    window.table.setItem(0, 0, item)

    window._tick_ages()

    assert item.text() == "35s"
    window.close()
