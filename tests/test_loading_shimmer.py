import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QColor, QImage
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from kubescope.views.loading_shimmer import (
    CYCLE_MS,
    INTERVAL_MS,
    LoadingShimmer,
)
from tests.qt import get_application

application = get_application()
KEPT: list[QTableWidget] = []  # until the end: a table that goes first crashes Qt


def make(rows=0, animated=True) -> tuple[QTableWidget, LoadingShimmer]:
    table = QTableWidget(rows, 3)
    KEPT.append(table)
    for row in range(rows):
        table.setItem(row, 0, QTableWidgetItem("x"))
    table.resize(500, 300)
    table.show()
    return table, LoadingShimmer(table, lambda: "#3220a0", lambda: animated)


def painted(shimmer: LoadingShimmer) -> int:
    """How many pixels of the shimmer are not transparent."""
    image = QImage(shimmer.size(), QImage.Format.Format_ARGB32)
    image.fill(QColor(0, 0, 0, 0))
    shimmer.render(image)
    return sum(
        image.pixelColor(x, y).alpha() > 0
        for x in range(0, image.width(), 3)
        for y in range(0, image.height(), 3)
    )


def test_it_covers_the_viewport_and_shows_only_while_the_table_loads() -> None:
    table, shimmer = make()
    assert shimmer.isHidden()

    shimmer.set_active(True)

    assert not shimmer.isHidden() and shimmer._timer.isActive()
    assert shimmer.geometry() == table.viewport().rect()
    table.resize(700, 400)  # it follows the table
    QCoreApplication.processEvents()
    assert shimmer.geometry() == table.viewport().rect()

    shimmer.set_active(True)  # nothing changes when it is asked again
    shimmer.set_active(False)

    assert shimmer.isHidden() and not shimmer._timer.isActive()


def test_an_empty_table_shows_bars_where_the_rows_will_be() -> None:
    _table, shimmer = make()
    shimmer.set_active(True)

    assert painted(shimmer) > 0


def test_a_table_with_rows_shows_nothing() -> None:
    _table, shimmer = make(rows=2)
    shimmer.set_active(True)

    assert painted(shimmer) == 0


def test_the_bars_are_where_the_columns_are_and_skip_the_hidden_ones() -> None:
    table, shimmer = make()
    shimmer.set_active(True)
    with_all = shimmer._bar_paths().boundingRect().width()

    table.setColumnHidden(2, True)

    assert shimmer._bar_paths().boundingRect().width() < with_all
    table.setColumnWidth(0, 4)  # a column with no room has no bar
    shimmer._bar_paths()


def test_the_band_crosses_the_bars_and_starts_again() -> None:
    _table, shimmer = make()
    shimmer.set_active(True)

    for _ in range(CYCLE_MS // INTERVAL_MS + 2):
        shimmer._tick()

    assert 0 <= shimmer._elapsed < CYCLE_MS
    assert painted(shimmer) > 0


def test_with_the_animations_off_the_bars_stand_still() -> None:
    _table, shimmer = make(animated=False)

    shimmer.set_active(True)

    assert not shimmer._timer.isActive() and painted(shimmer) > 0


def test_a_table_that_is_empty_says_so_in_the_middle_and_loses_it_with_a_row() -> None:
    table, shimmer = make()

    shimmer.set_message("Nothing to show here")

    assert not shimmer.isHidden() and painted(shimmer) > 0

    table.setRowCount(1)
    table.setItem(0, 0, QTableWidgetItem("x"))

    assert painted(shimmer) == 0  # a row shows: the text is not drawn

    shimmer.set_message("")
    assert shimmer.isHidden()


def test_a_table_whose_rows_are_all_hidden_by_a_search_says_so_too() -> None:
    table, shimmer = make(rows=2)
    table.setRowHidden(0, True)
    table.setRowHidden(1, True)

    shimmer.set_message("No result matches the search")

    assert painted(shimmer) > 0
    table.setRowHidden(1, False)
    assert painted(shimmer) == 0


def test_the_text_waits_for_the_loading_to_end() -> None:
    _table, shimmer = make()
    shimmer.set_active(True)

    shimmer.set_message("Nothing to show here")  # loading: the bars say it
    assert shimmer._message == ""

    shimmer.set_active(False)
    shimmer.set_message("Nothing to show here")
    assert shimmer._message == "Nothing to show here"
