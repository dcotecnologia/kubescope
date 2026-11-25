import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QTableWidget, QWidget

from kubescope.views.table_look import TableLook, install_table_look
from tests.qt import get_application

application = get_application()
KEPT: list[QWidget] = []  # until the end: a widget that goes first crashes Qt


def test_a_table_gets_centered_headers_and_texts_cut_not_wrapped() -> None:
    table = QTableWidget(2, 1)
    table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
    KEPT.append(table)
    look = TableLook()
    KEPT.append(look)  # type: ignore[arg-type]
    assert not look.eventFilter(table, QEvent(QEvent.Type.Show))
    assert table.horizontalHeader().defaultAlignment() == Qt.AlignmentFlag.AlignCenter
    assert not table.wordWrap()
    assert table.textElideMode() == Qt.TextElideMode.ElideRight


def test_the_filter_is_installed_on_the_application() -> None:
    install_table_look(application)
