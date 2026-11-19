"""The Extensions section of the Settings: a card for each extension, and the
ways to install one.

An extension is installed from a folder (the person picks its
`kubescope-extension.toml`, and the folder it is in is installed) or
from a GitHub repository, and only after a dialog shows what it is. In
development mode a folder is not copied: it runs from where it is, which
is what an author wants while writing it. The archive of a repository is
downloaded off the UI thread.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope.dialogs.extension_dialog import InstallExtensionDialog
from kubescope.extensions.github import (
    GithubError,
    Repo,
    download,
    parse_repo,
    repo_of,
)
from kubescope.extensions.manifest import Manifest
from kubescope.extensions.store import Candidate, ExtensionStore, StoreError
from kubescope.ui.ui_settings_page import Ui_SettingsPage

logger = logging.getLogger(__name__)

FOLDER_SOURCE = "folder "  # how the store remembers an extension from a folder
CARD_WIDTH = 300  # pixels a card needs at least
GAP = 14


@dataclass(frozen=True)
class Row:
    manifest: Manifest
    source: str  # "bundled", "folder /x", "github o/r", "dev /x"
    installed: bool

    @property
    def bundled(self) -> bool:
        return self.source == "bundled"

    @property
    def dev(self) -> bool:
        return self.source.startswith("dev ")


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
        self._columns = 1
        form.extensionsInstallFolderButton.clicked.connect(self.install_from_folder)
        form.extensionsInstallRepoButton.clicked.connect(self.install_from_github)
        form.extensionsCardsHost.installEventFilter(self)
        self.refresh()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """More cards side by side when the page gives room for them."""
        if event.type() == QEvent.Type.Resize and self._fit_columns() != self._columns:
            self.render()
        return False

    def _fit_columns(self) -> int:
        width = self.form.extensionsCardsHost.width()
        return max(1, (width + GAP) // (CARD_WIDTH + GAP))

    # what is shown

    def refresh(self) -> None:
        """Read the store again and draw the cards."""
        self.rows = [
            Row(one.manifest, one.source, True) for one in self.store.installed()
        ] + [
            Row(manifest, "bundled", False) for manifest in self.store.removed_bundled()
        ]
        self.render()

    def render(self) -> None:
        grid = self.form.extensionsCardsGrid
        while (item := grid.takeAt(0)) is not None:
            if widget := item.widget():
                widget.deleteLater()
        columns = self._columns = self._fit_columns()
        if not self.rows:
            grid.addWidget(QLabel(self.tr("No extension is installed")), 0, 0)
            return
        for index, row in enumerate(self.rows):
            grid.addWidget(self._card(row), index // columns, index % columns)
        for column in range(columns):
            grid.setColumnStretch(column, 1)
        grid.setRowStretch((len(self.rows) + columns - 1) // columns, 1)

    def _badge(self, row: Row) -> str:
        if not row.installed:
            return self.tr("Uninstalled")
        if row.dev:
            return self.tr("Development")
        return self.tr("Bundled") if row.bundled else self.tr("Installed")

    def _card(self, row: Row) -> QFrame:
        manifest = row.manifest
        card = QFrame()
        card.setObjectName("extensionCard")
        card.setProperty("card", "true")  # the look of the app's other cards
        card.setMinimumHeight(170)
        layout = QVBoxLayout(card)
        top = QHBoxLayout()
        title = QLabel(manifest.name)
        title.setObjectName("extensionCardTitle")
        title.setStyleSheet("font-size: 16px; font-weight: 700;")
        title.setWordWrap(True)
        top.addWidget(title, 1)
        badge = QLabel(self._badge(row))
        badge.setObjectName("extensionCardBadge")
        badge.setStyleSheet("font-weight: 700;")
        top.addWidget(badge)
        layout.addLayout(top)
        meta = f"v{manifest.version}" + (
            f" · {manifest.author}" if manifest.author else ""
        )
        layout.addWidget(QLabel(meta))
        description = QLabel(manifest.description)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(description, 1)
        if not row.bundled:
            source = QLabel(row.source)
            source.setWordWrap(True)
            source.setProperty("variant", "muted")
            source.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(source)
        buttons = QHBoxLayout()
        if not row.installed or self._can_reinstall(row):
            reinstall = QPushButton(self.tr("Reinstall"))
            reinstall.setProperty(
                "variant", "primary" if not row.installed else "secondary"
            )
            reinstall.clicked.connect(partial(self.reinstall, row))
            buttons.addWidget(reinstall)
        if row.installed:
            uninstall = QPushButton(self.tr("Uninstall"))
            uninstall.setProperty("variant", "secondary")
            uninstall.clicked.connect(partial(self.uninstall, row))
            buttons.addWidget(uninstall)
        buttons.addStretch(1)
        layout.addLayout(buttons)
        return card

    @staticmethod
    def _can_reinstall(row: Row) -> bool:
        """An installed extension that can be fetched again from where it
        came."""
        return row.source.startswith(("github ", FOLDER_SOURCE))

    def _warn(self, text: str) -> None:
        self.show_message(QMessageBox.Icon.Warning, self.tr("Extensions"), text)

    # install

    def install_from_folder(self) -> None:
        """Pick the manifest of an extension; its folder is what is
        installed."""
        chosen, _ = QFileDialog.getOpenFileName(
            self.window,
            self.tr("Choose the kubescope-extension.toml of the extension"),
            "",
            self.tr("Extension manifest (kubescope-extension.toml)"),
        )
        if chosen:
            self._install_folder(
                Path(chosen).parent, self.form.extensionsDevCheck.isChecked()
            )

    def _install_folder(self, folder: Path, dev: bool) -> None:
        try:
            candidate = (
                self.store.prepare_link(folder)
                if dev
                else self.store.prepare_folder(folder)
            )
        except StoreError as error:
            self._warn(str(error))
            return
        self._review(candidate)

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
            lambda data: self._prepared(self.store.prepare, data, repo.source),
            repo,
            on_error=self._warn,
        )

    def _prepared(self, prepare: Callable[..., Candidate], *arguments: object) -> None:
        try:
            candidate = prepare(*arguments)
        except StoreError as error:
            self._warn(str(error))
            return
        self._review(candidate)

    def _review(self, candidate: Candidate) -> None:
        """Show what the extension is and install it if the person agrees."""
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

    def uninstall(self, row: Row) -> None:
        name = row.manifest.name
        text = (
            self.tr(
                "{name} comes with KubeScope. Uninstall it? You can reinstall it here."
            )
            if row.bundled
            else self.tr("Uninstall {name}? Its files are deleted.")
        ).format(name=name)
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
            self.store.uninstall(row.manifest.id)
        except StoreError as error:
            self._warn(str(error))
        self.refresh()

    def reinstall(self, row: Row) -> None:
        if not row.installed:  # a bundled one the person uninstalled
            try:
                self.store.restore_bundled(row.manifest.id)
            except StoreError as error:
                self._warn(str(error))
            self.refresh()
            return
        if row.source.startswith(FOLDER_SOURCE):
            folder = Path(row.source.removeprefix(FOLDER_SOURCE))
            if folder.is_dir():
                self._install_folder(folder, dev=False)  # a copy, as it was
            else:  # it is not where it was: ask for it again
                self.install_from_folder()
            return
        try:
            repo = repo_of(row.source)
        except GithubError as error:
            self._warn(str(error))
            return
        if repo is not None:
            self._download(repo)
