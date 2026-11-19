"""The Extensions section of the Settings: what is installed, and the buttons
to install, uninstall and reinstall.

An extension is installed from a zip the person picks or from a GitHub
repository, and only after a dialog shows what it is. The archive of a
repository is downloaded off the UI thread.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QObject
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from kubescope.dialogs.extension_dialog import InstallExtensionDialog
from kubescope.extensions.archive import MAX_ARCHIVE
from kubescope.extensions.github import (
    GithubError,
    Repo,
    download,
    parse_repo,
    repo_of,
)
from kubescope.extensions.store import ExtensionStore, StoreError
from kubescope.ui.ui_settings_page import Ui_SettingsPage

logger = logging.getLogger(__name__)

FILE_SOURCE = "file "  # how the store remembers an extension from a zip


@dataclass(frozen=True)
class Row:
    id: str
    name: str
    version: str
    source: str
    installed: bool


class ExtensionsPanel(QObject):
    def __init__(
        self,
        form: Ui_SettingsPage,
        store: ExtensionStore,
        window: QWidget,
        run_action: Callable[..., None],
        show_message: Callable[[QMessageBox.Icon, str, str], None],
    ) -> None:
        super().__init__(window)
        self.form = form
        self.store = store
        self.window = window
        self.run_action = run_action
        self.show_message = show_message
        self.rows: list[Row] = []
        form.extensionsInstallFileButton.clicked.connect(self.install_from_file)
        form.extensionsInstallRepoButton.clicked.connect(self.install_from_github)
        form.extensionsReinstallButton.clicked.connect(self.reinstall)
        form.extensionsUninstallButton.clicked.connect(self.uninstall)
        form.extensionsTable.itemSelectionChanged.connect(self._update_buttons)
        self.refresh()

    # what is shown

    def refresh(self) -> None:
        """Read the store again and show it, keeping the selection."""
        kept = self._selected()
        self.rows = [
            Row(
                one.manifest.id,
                one.manifest.name,
                one.manifest.version,
                one.source,
                True,
            )
            for one in self.store.installed()
        ] + [
            Row(manifest.id, manifest.name, manifest.version, "bundled", False)
            for manifest in self.store.removed_bundled()
        ]
        table = self.form.extensionsTable
        table.setRowCount(len(self.rows))
        for index, row in enumerate(self.rows):
            source = self.tr("Bundled") if row.source == "bundled" else row.source
            status = self.tr("Installed") if row.installed else self.tr("Uninstalled")
            for column, text in enumerate((row.name, row.version, source, status)):
                table.setItem(index, column, QTableWidgetItem(text))
        if kept is not None:
            for index, row in enumerate(self.rows):
                if row.id == kept.id:
                    table.selectRow(index)
        self._update_buttons()

    def _selected(self) -> Row | None:
        chosen = self.form.extensionsTable.selectedItems()
        if not chosen or chosen[0].row() >= len(self.rows):
            return None
        return self.rows[chosen[0].row()]

    def _update_buttons(self) -> None:
        row = self._selected()
        self.form.extensionsUninstallButton.setEnabled(
            row is not None and row.installed
        )
        self.form.extensionsReinstallButton.setEnabled(
            row is not None
            and (not row.installed or row.source.startswith(("github ", FILE_SOURCE)))
        )

    def _warn(self, text: str) -> None:
        self.show_message(QMessageBox.Icon.Warning, self.tr("Extensions"), text)

    # install

    def install_from_file(self) -> None:
        chosen, _ = QFileDialog.getOpenFileName(
            self.window,
            self.tr("Choose the zip of an extension"),
            "",
            self.tr("Zip files (*.zip)"),
        )
        if not chosen:
            return
        path = Path(chosen)
        try:
            with path.open("rb") as handle:
                data = handle.read(MAX_ARCHIVE + 1)
        except OSError as error:
            self._warn(
                self.tr("The file could not be read: {reason}").format(
                    reason=error.strerror or str(error)
                )
            )
            return
        self._review(data, f"{FILE_SOURCE}{path.name}")

    def install_from_github(self) -> None:
        text, accepted = QInputDialog.getText(
            self.window,
            self.tr("Install from GitHub"),
            self.tr("Repository (owner/name, or its GitHub address):"),
        )
        if not accepted or not text.strip():
            return
        try:
            repo = parse_repo(text)
        except GithubError as error:
            self._warn(str(error))
            return
        self._download(repo)

    def _download(self, repo: Repo) -> None:
        self.run_action(
            download,
            lambda data: self._review(data, repo.source),
            repo,
            on_error=self._warn,
        )

    def _review(self, data: bytes, source: str) -> None:
        """Show what the archive is and install it if the person agrees."""
        try:
            candidate = self.store.prepare(data, source)
        except StoreError as error:
            self._warn(str(error))
            return
        dialog = InstallExtensionDialog(self.window, candidate)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.store.discard(candidate)
            return
        try:
            self.store.install(candidate)
        except (StoreError, OSError) as error:
            logger.warning("Could not install an extension: %s", error)
            self._warn(str(error))
        self.refresh()

    # uninstall and reinstall

    def uninstall(self) -> None:
        row = self._selected()
        if row is None or not row.installed:
            return
        text = (
            self.tr(
                "{name} comes with KubeScope. Uninstall it? You can reinstall it here."
            )
            if row.source == "bundled"
            else self.tr("Uninstall {name}? Its files are deleted.")
        ).format(name=row.name)
        answer = QMessageBox.question(
            self.window,
            self.tr("Extensions"),
            text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.store.uninstall(row.id)
        except StoreError as error:
            self._warn(str(error))
        self.refresh()

    def reinstall(self) -> None:
        row = self._selected()
        if row is None:
            return
        if not row.installed:  # a bundled one the person uninstalled
            try:
                self.store.restore_bundled(row.id)
            except StoreError as error:
                self._warn(str(error))
            self.refresh()
            return
        if row.source.startswith(FILE_SOURCE):
            self.install_from_file()  # the zip is asked for again
            return
        try:
            repo = repo_of(row.source)
        except GithubError as error:
            self._warn(str(error))
            return
        if repo is not None:
            self._download(repo)
