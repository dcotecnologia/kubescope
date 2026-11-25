"""The look every table of the application shares: the headers centered, and a
text that does not fit its cell cut with an ellipsis, never wrapped.

One filter for the whole application, so the tables of the extensions
have it too. The texts of the cells stay at the left.
"""

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QTableView


class TableLook(QObject):
    """Gives a table the shared look when it is first shown."""

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Show and isinstance(watched, QTableView):
            self._apply(watched)
        return False

    @staticmethod
    def _apply(table: QTableView) -> None:
        header = table.horizontalHeader()
        if header is not None:
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setTextElideMode(Qt.TextElideMode.ElideRight)
        table.setWordWrap(False)
        table.setTextElideMode(Qt.TextElideMode.ElideRight)


_look: list[TableLook] = []  # kept as long as the application lives


def install_table_look(application: QApplication) -> None:
    look = TableLook()
    _look.append(look)
    application.installEventFilter(look)
