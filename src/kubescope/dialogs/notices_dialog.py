from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtGui import QDesktopServices, QFontDatabase, QTextCursor
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope.utils.notices import NOTICES, Notice, parse_notices, read_notices


class NoticesDialog(QDialog):
    """The licenses of what KubeScope uses: a list of the components, a filter
    for it, and the text of the one chosen."""

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.setWindowTitle(
            QCoreApplication.translate("WorkloadWindow", "Third-party notices")
        )
        self.resize(900, 600)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        self.filter = QLineEdit()
        self.filter.setPlaceholderText(
            QCoreApplication.translate("WorkloadWindow", "Filter the list")
        )
        self.filter.setClearButtonEnabled(True)
        self.filter.textChanged.connect(self._filter)
        layout.addWidget(self.filter)
        columns = QHBoxLayout()
        columns.setSpacing(10)
        self.entries = QListWidget()
        self.entries.setMinimumWidth(240)
        self.entries.setMaximumWidth(320)
        self.entries.currentRowChanged.connect(self._show)
        columns.addWidget(self.entries)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
        columns.addWidget(self.text, 1)
        layout.addLayout(columns, 1)
        self.notices: list[Notice] = []
        text = read_notices()
        if text is None:
            self.text.setPlainText(
                QCoreApplication.translate(
                    "WorkloadWindow",
                    "The notices are not available in this installation.",
                )
            )
        else:
            self.notices = parse_notices(text)
            self.entries.addItems([notice.title for notice in self.notices])
            self.entries.setCurrentRow(0)
        actions = QHBoxLayout()
        open_file = QPushButton(
            QCoreApplication.translate("WorkloadWindow", "Open the file")
        )
        open_file.setProperty("variant", "secondary")
        open_file.setVisible(text is not None)
        open_file.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(str(NOTICES)))
        )
        close_button = QPushButton(
            QCoreApplication.translate("WorkloadWindow", "Close")
        )
        close_button.setProperty("variant", "primary")
        close_button.setDefault(True)
        close_button.clicked.connect(self.accept)
        actions.addWidget(open_file)
        actions.addStretch()
        actions.addWidget(close_button)
        layout.addLayout(actions)

    def _show(self, row: int) -> None:
        self.text.setPlainText(self.notices[row].text)
        self.text.moveCursor(QTextCursor.MoveOperation.Start)

    def _filter(self, query: str) -> None:
        """Show the components whose name has the words typed."""
        words = query.casefold().split()
        first = -1
        for row in range(self.entries.count()):
            item = self.entries.item(row)
            assert item is not None
            shown = all(word in item.text().casefold() for word in words)
            item.setHidden(not shown)
            if shown and first < 0:
                first = row
        current = self.entries.currentItem()
        if first >= 0 and (current is None or current.isHidden()):
            self.entries.setCurrentRow(first)
