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
    counting, unknown = QTableWidgetItem("1m0s"), QTableWidgetItem("unknown")
    stamp_age(counting, "1m0s")
    stamp_age(unknown, "unknown")
    table.setItem(0, 0, counting)
    table.setItem(0, 1, unknown)
    tick_ages(table)
    assert counting.text() == "1m7s"
    assert unknown.text() == "unknown"
