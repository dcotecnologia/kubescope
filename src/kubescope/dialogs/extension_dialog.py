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

from kubescope.extensions.store import Candidate


class InstallExtensionDialog(QDialog):
    """What an extension is, shown before any of it runs.

    An extension is code that runs with the person's permissions, so the
    dialog says where it came from, which version it is, what it asks to
    do and the sha256 of its archive, and what it replaces. Cancel is
    the default; accepting it installs.
    """

    def __init__(self, parent: QWidget | None, candidate: Candidate) -> None:
        super().__init__(parent)
        manifest = candidate.manifest
        self.setWindowTitle(self.tr("Install {name}?").format(name=manifest.name))
        self.setMinimumWidth(560)
        layout = QVBoxLayout(self)
        if manifest.description:
            description = QLabel(manifest.description)
            description.setWordWrap(True)
            layout.addWidget(description)
        form = QFormLayout()
        layout.addLayout(form)
        form.addRow(self.tr("Version"), QLabel(manifest.version))
        if manifest.author:
            form.addRow(self.tr("Author"), QLabel(manifest.author))
        form.addRow(self.tr("Source"), self._selectable(candidate.source))
        form.addRow(
            self.tr("Permissions"), self._selectable(self._permissions(candidate))
        )
        if candidate.dev:
            development = QLabel(
                self.tr(
                    "Development mode: it runs from this folder, without a copy, "
                    "and reloads when its files change."
                )
            )
            development.setWordWrap(True)
            layout.addWidget(development)
        else:
            form.addRow(self.tr("SHA-256"), self._selectable(candidate.sha256))
        if candidate.replaces is not None:
            version = candidate.replaces.version
            notes = [
                self.tr("It replaces the version {version}.").format(version=version)
            ]
            if candidate.content_changed:
                notes.append(
                    self.tr("Its content is different from the one you installed.")
                )
            replaces = QLabel(" ".join(notes))
            replaces.setWordWrap(True)
            layout.addWidget(replaces)
        warning = QLabel(
            self.tr(
                "An extension is code that runs with your permissions. Install it "
                "only if you trust where it came from."
            )
        )
        warning.setWordWrap(True)
        warning.setProperty("variant", "muted")
        layout.addWidget(warning)
        row = QHBoxLayout()
        row.addStretch(1)
        self.install_button = QPushButton(self.tr("Install"))
        self.install_button.setProperty("variant", "primary")
        self.install_button.clicked.connect(self.accept)
        cancel = QPushButton(self.tr("Cancel"))
        cancel.setProperty("variant", "secondary")
        cancel.setDefault(True)
        cancel.clicked.connect(self.reject)
        row.addWidget(cancel)
        row.addWidget(self.install_button)
        layout.addLayout(row)

    @staticmethod
    def _selectable(text: str) -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        return label

    def _permissions(self, candidate: Candidate) -> str:
        meaning = {
            "cluster.read": self.tr("read your clusters"),
            "cluster.write": self.tr("change your clusters, in the write mode"),
            "subprocess": self.tr("run programs of this computer"),
            "ui.dock": self.tr("add a panel to the window"),
            "ui.tab": self.tr("add a kind of tab"),
            "ui.page": self.tr("add a page to the side menu"),
            "ui.settings": self.tr("add a section to the Settings"),
            "ui.window": self.tr(
                "use the window: show messages, run tasks and add shortcuts"
            ),
            "cli": self.tr("add a command to kubescope"),
        }
        names = sorted(candidate.manifest.permissions)
        if not names:
            return self.tr("none")
        return "\n".join(f"• {meaning[name]} ({name})" for name in names)
