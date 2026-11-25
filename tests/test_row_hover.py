import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget

from kubescope.views.row_hover import RowHover, _Band, install_row_hover
from tests.qt import get_application

application = get_application()
KEPT: list[QWidget] = []  # until the end: a widget that goes first crashes Qt


def _table() -> tuple[QTableWidget, RowHover]:
    table = QTableWidget(5, 2)
    for row in range(5):
        table.setItem(row, 0, QTableWidgetItem(f"row {row}"))
    table.resize(300, 200)
    KEPT.append(table)
    hover = RowHover()
    KEPT.append(hover)  # type: ignore[arg-type]
    table.installEventFilter(hover)
    table.show()
    QApplication.sendEvent(table, QEvent(QEvent.Type.Show))  # as the app-wide one
    return table, hover


def _move(table: QTableWidget, y: float) -> None:
    viewport = table.viewport()
    assert viewport is not None
    event = QMouseEvent(
        QEvent.Type.MouseMove,
        QPointF(10, y),
        QPointF(10, y),
        Qt.MouseButton.NoButton,
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
    )
    QApplication.sendEvent(viewport, event)


def test_the_band_follows_the_cursor_row_by_row_and_leaves_with_it() -> None:
    table, _hover = _table()
    band = table.viewport().findChild(_Band)
    assert band is not None

    _move(table, table.rowViewportPosition(2) + 3)
    assert band.isVisible() and band.y() == table.rowViewportPosition(2)
    assert band.height() == table.rowHeight(2)

    _move(table, table.rowViewportPosition(4) + 3)
    assert band.y() == table.rowViewportPosition(4)

    _move(table, 195)  # below the last row
    assert not band.isVisible()

    _move(table, 5)
    QApplication.sendEvent(table.viewport(), QEvent(QEvent.Type.Leave))
    assert not band.isVisible()
    assert not band.grab().isNull()  # it paints


def test_one_filter_for_the_application_and_the_scroll_hides_the_band() -> None:
    install_row_hover(application)
    table, _hover = _table()
    band = table.viewport().findChild(_Band)
    assert band is not None
    _move(table, 5)
    assert band.isVisible()

    table.verticalScrollBar().valueChanged.emit(1)

    assert not band.isVisible()
