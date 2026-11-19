from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope.dialogs.extension_dialog import permission_lines


@dataclass(frozen=True)
class ExtensionDetails:
    """What is known of an extension, as the table of the Settings has it."""

    name: str
    id: str
    version: str
    status: str
    description: str = ""
    author: str = ""
    source: str = ""
    sha256: str = ""
    folder: str = ""
    installed_at: str = ""  # a day, already in the time zone of the settings
    updated_at: str = ""
    permissions: tuple[str, ...] = ()
    commands: tuple[str, ...] = ()
    error: str = ""
    recommended: bool = False
    known: bool = True  # False for one that is not downloaded: its files are unknown
    newer: str = ""  # the version that can be installed, if there is one


class ExtensionDetailsDialog(QDialog):
    """Everything about one extension: who made it, where it came from, what it
    may do, and when it was installed and updated."""

    def __init__(self, parent: QWidget | None, details: ExtensionDetails) -> None:
        super().__init__(parent)
        self.setWindowTitle(details.name)
        self.setMinimumWidth(560)
        layout = QVBoxLayout(self)
        heading = QLabel(details.name)
        heading.setStyleSheet("font-size: 18px; font-weight: 700;")
        layout.addWidget(heading)
        if details.description:
            description = QLabel(details.description)
            description.setWordWrap(True)
            layout.addWidget(description)
        form = QFormLayout()
        layout.addLayout(form)
        rows = [
            (self.tr("Id"), details.id),
            (self.tr("Version"), f"v{details.version}" if details.version else ""),
            (self.tr("Status"), details.status),
            (self.tr("Author"), details.author),
            (self.tr("Source"), details.source),
            (self.tr("Folder"), details.folder),
            (self.tr("Installed"), details.installed_at),
            (self.tr("Updated"), details.updated_at),
            (self.tr("SHA-256"), details.sha256),
        ]
        if details.newer:
            rows.append((self.tr("Newer version"), f"v{details.newer}"))
        if details.commands:
            rows.append((self.tr("Commands"), ", ".join(details.commands)))
        for label, value in rows:
            if value:
                form.addRow(label, self._selectable(value))
        form.addRow(
            self.tr("Permissions"),
            self._selectable(
                permission_lines(details.permissions)
                if details.known
                else self.tr("They are shown when it is downloaded.")
            ),
        )
        if details.error:
            problem = QLabel(
                self.tr("Could not load: {error}").format(error=details.error)
            )
            problem.setWordWrap(True)
            problem.setStyleSheet("color: #c0392b;")
            layout.addWidget(problem)
        if details.recommended:
            recommended = QLabel(
                self.tr(
                    "KubeScope recommends it: what it installs is pinned to a "
                    "version and to the hash of its files."
                )
            )
            recommended.setWordWrap(True)
            recommended.setProperty("variant", "muted")
            layout.addWidget(recommended)
        row = QHBoxLayout()
        row.addStretch(1)
        close = QPushButton(self.tr("Close"))
        close.setProperty("variant", "secondary")
        close.setDefault(True)
        close.clicked.connect(self.accept)
        row.addWidget(close)
        layout.addLayout(row)

    @staticmethod
    def _selectable(text: str) -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        return label
