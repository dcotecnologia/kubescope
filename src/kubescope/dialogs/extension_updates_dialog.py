from collections.abc import Sequence

from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from kubescope.extensions.updates import Update
from kubescope.views.table_sort import HeaderSorter


class ExtensionUpdatesDialog(QDialog):
    """The extensions that have a newer version, from which version to which.

    Update starts with the first one: each is downloaded and shown in
    the same dialog as any install, with its permissions and its hash,
    before anything of it is replaced. Later leaves them for now.
    """

    def __init__(self, parent: QWidget | None, updates: Sequence[Update]) -> None:
        super().__init__(parent)
        self.updates = list(updates)
        self.setWindowTitle(self.tr("Update extensions"))
        self.setMinimumSize(520, 300)
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        heading = QLabel(
            self.tr("{count} extensions have a newer version").format(
                count=len(self.updates)
            )
        )
        heading.setStyleSheet("font-size: 16px; font-weight: 700;")
        layout.addWidget(heading)
        intro = QLabel(
            self.tr(
                "Each one is downloaded and shown to you, with its permissions, "
                "before it replaces the one you have."
            )
        )
        intro.setWordWrap(True)
        intro.setProperty("variant", "muted")
        layout.addWidget(intro)
        self.table = QTableWidget(len(self.updates), 3)
        self.table.setHorizontalHeaderLabels(
            [self.tr("EXTENSION"), self.tr("INSTALLED"), self.tr("NEW")]
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setShowGrid(False)
        self.table.setProperty("variant", "data")
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 260)
        self.table.setColumnWidth(1, 110)
        for row, update in enumerate(self.updates):
            for column, text in enumerate(
                (update.name, f"v{update.current}", f"v{update.version}")
            ):
                self.table.setItem(row, column, QTableWidgetItem(text))
        HeaderSorter(self.table)  # a click on a header sorts
        layout.addWidget(self.table, 1)
        buttons = QHBoxLayout()
        buttons.addStretch(1)
        later = QPushButton(self.tr("Later"))
        later.setProperty("variant", "secondary")
        later.clicked.connect(self.reject)
        self.update_button = QPushButton(self.tr("Update"))
        self.update_button.setProperty("variant", "primary")
        self.update_button.setDefault(True)
        self.update_button.clicked.connect(self.accept)
        buttons.addWidget(later)
        buttons.addWidget(self.update_button)
        layout.addLayout(buttons)
