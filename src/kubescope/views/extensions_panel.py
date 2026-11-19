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
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from datetime import datetime
from functools import partial
from pathlib import Path

from kubescope.sdk.timezone import to_zone
from PySide6.QtCore import QObject, QPoint, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from kubescope.dialogs.extension_details_dialog import (
    ExtensionDetails,
    ExtensionDetailsDialog,
)
from kubescope.dialogs.extension_dialog import InstallExtensionDialog
from kubescope.dialogs.extension_updates_dialog import ExtensionUpdatesDialog
from kubescope.extensions.defaults import DefaultExtension, offered, verify
from kubescope.extensions.github import (
    GithubError,
    Repo,
    download,
    list_tags,
    parse_repo,
    repo_of,
)
from kubescope.extensions.manifest import Manifest
from kubescope.extensions.store import Candidate, ExtensionStore, StoreError
from kubescope.extensions.updates import Update, find, version_key
from kubescope.settings import Settings
from kubescope.theme import themed
from kubescope.ui.ui_settings_page import Ui_SettingsPage
from kubescope.views.container_states import BADGE_ROLE, BadgeDelegate

logger = logging.getLogger(__name__)

FOLDER_SOURCE = "folder "  # how the store remembers an extension from a folder
STAR = "\u2605"  # marks the extensions the app recommends
UPDATE_CHECK_SECONDS = 24 * 3600  # how often GitHub is asked for newer tags
COLUMNS = {
    "name": 0,
    "version": 1,
    "status": 2,
    "author": 3,
    "installed": 4,
    "updated": 5,
    "source": 6,
    "description": 7,
}
WIDTHS = {  # DESCRIPTION takes what is left
    "name": 220,
    "version": 80,
    "status": 150,
    "author": 130,
    "installed": 100,
    "updated": 100,
    "source": 260,
}


@dataclass(frozen=True)
class Row:
    manifest: Manifest
    source: str  # "bundled", "folder /x", "github o/r", "dev /x"
    installed: bool
    default: DefaultExtension | None = None  # one the app offers, not installed
    installed_at: str = ""  # UTC, as the store keeps it
    updated_at: str = ""
    update: Update | None = None  # a newer version that can be installed
    sha256: str = ""
    folder: str = ""
    recommended: bool = False  # the app recommends it, installed or not

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
        changed: Callable[[], None] = lambda: None,
        load_errors: Callable[[], dict[str, str]] = dict,
        defaults: Callable[[], Sequence[DefaultExtension]] = offered,
        save_settings: Callable[[], None] = lambda: None,
    ) -> None:
        super().__init__(window)
        self.form = form
        self.store = store
        self.window = window
        self.run_action = run_action
        self.show_message = show_message
        self.changed = changed  # what was installed or removed is to be loaded
        self.load_errors = load_errors  # why an extension did not load
        self.defaults = defaults  # what the app offers to install
        self.save_settings = save_settings
        self.updates: list[Update] = []  # newer versions of what is installed
        self._checking = False
        self.updates_row = QWidget()
        updates_layout = QHBoxLayout(self.updates_row)
        updates_layout.setContentsMargins(0, 0, 0, 0)
        self.updates_label = QLabel()
        self.updates_label.setObjectName("extensionUpdatesLabel")
        self.updates_label.setProperty("variant", "muted")
        self.updates_button = QPushButton(self.tr("Update..."))
        self.updates_button.setProperty("variant", "primary")
        self.updates_button.clicked.connect(self.show_updates)
        updates_layout.addWidget(self.updates_label)
        updates_layout.addWidget(self.updates_button)
        updates_layout.addStretch(1)
        self.updates_row.hide()
        self._queue: list[Update] = []  # what is being updated, one at a time
        self.check_button = QPushButton(self.tr("Check for updates"))
        self.check_button.setProperty("variant", "secondary")
        form.extensionsButtonsRow.insertWidget(
            form.extensionsButtonsRow.indexOf(form.extensionsInstallRepoButton) + 1,
            self.check_button,
        )
        form.extensionsCardLayout.insertWidget(
            form.extensionsCardLayout.indexOf(form.extensionsCardsHost),
            self.updates_row,
        )
        self.check_button.clicked.connect(lambda: self.check_updates(force=True))
        self._build_table()
        # Development mode goes under the buttons: all four in a row make the
        # page wider than a narrow window
        form.extensionsButtonsRow.removeWidget(form.extensionsDevCheck)
        form.extensionsCardLayout.insertWidget(
            form.extensionsCardLayout.indexOf(form.extensionsButtonsRow) + 1,
            form.extensionsDevCheck,
        )
        self.rows: list[Row] = []
        form.extensionsInstallFolderButton.clicked.connect(self.install_from_folder)
        form.extensionsInstallRepoButton.clicked.connect(self.install_from_github)
        self.refresh()

    # what is shown

    def refresh(self) -> None:
        """Read the store again and draw the cards."""
        recommended = {one.id for one in self.defaults()}
        self.rows = [
            Row(
                one.manifest,
                one.source,
                True,
                installed_at=one.installed_at,
                updated_at=one.updated_at,
                sha256=one.sha256,
                folder=str(one.folder),
                recommended=one.manifest.id in recommended,
            )
            for one in self.store.installed()
        ] + [
            Row(manifest, "bundled", False) for manifest in self.store.removed_bundled()
        ]
        self.rows = [replace(row, update=self._update_of(row)) for row in self.rows]
        have = {row.manifest.id for row in self.rows}
        for one in self.defaults():
            if one.id not in have:  # offered, and not here
                manifest = Manifest(
                    one.id, one.name, one.repo.ref.lstrip("v"), "", frozenset()
                )
                manifest = replace(manifest, description=one.description)
                self.rows.append(
                    Row(
                        manifest,
                        f"github {one.repo.label}",
                        False,
                        one,
                        sha256=one.sha256,
                        recommended=True,
                    )
                )
        self.render()

    def _update_of(self, row: Row) -> Update | None:
        """The newer version of an installed extension, if one was found and it
        is still newer than what is installed."""
        current = version_key(row.manifest.version)
        for update in self.updates:
            latest = version_key(update.latest)
            if (
                row.installed
                and update.extension == row.manifest.id
                and current is not None
                and latest is not None
                and latest > current
            ):
                return update
        return None

    # looking for newer versions

    def check_updates(
        self, settings: Settings | None = None, force: bool = False
    ) -> None:
        """Look for newer versions of what is installed.

        What the app pins needs no network and is always looked at; the
        tags of other repositories are asked of GitHub only when the
        Settings allow it, and at most once a day unless the person
        asks.
        """
        installed = self.store.installed()
        defaults = list(self.defaults())
        self.updates = find(installed, defaults, None)
        self._after_check(settings, announce=not force)
        if self._checking:
            return
        allowed = settings is None or settings.check_updates
        fresh = (
            settings is not None
            and not force
            and 0
            <= time.time() - settings.extension_updates_checked_at
            < UPDATE_CHECK_SECONDS
        )
        if not allowed and not force or fresh:
            return
        self._checking = True
        self.check_button.setEnabled(False)

        def done(found: list[Update]) -> None:
            self._checking = False
            self.check_button.setEnabled(True)
            self.updates = found
            if settings is not None:
                settings.record_extension_updates_check(time.time())
                self.save_settings()
            self._after_check(settings, told=force, announce=True, force=force)

        def failed(_message: str) -> None:
            self._checking = False
            self.check_button.setEnabled(True)

        self.run_action(
            partial(find, installed, defaults, list_tags),
            done,
            on_error=failed,
            quiet=True,
        )

    def _after_check(
        self,
        settings: Settings | None = None,
        told: bool = False,
        announce: bool = False,
        force: bool = False,
    ) -> None:
        count = len(self.updates)
        self.updates_row.setVisible(count > 0 or told)
        self.updates_button.setVisible(count > 0)
        self.updates_label.setText(
            self.tr("{count} updates available").format(count=count)
            if count
            else self.tr("Everything is up to date")
        )
        self.refresh()
        if announce and count and settings is not None:
            self._announce(settings, force)

    def _announce(self, settings: Settings, force: bool) -> None:
        """Show the window of the updates, once for each new version found, or
        whenever the person asked to look."""
        keys = [f"{one.extension}@{one.latest}" for one in self.updates]
        new = [key for key in keys if key not in settings.extension_updates_seen]
        if not new and not force:
            return
        settings.see_extension_updates(keys)
        self.save_settings()
        self.show_updates()

    def show_updates(self) -> None:
        """The window that offers the newer versions: Update goes through them
        one at a time."""
        if not self.updates:
            return
        dialog = ExtensionUpdatesDialog(self.window, self.updates)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._queue = list(self.updates)
            self._next_update()

    def _next_update(self) -> None:
        """Download the next version of the queue, the way any install is: the
        person is shown it before it replaces what is installed."""
        while self._queue:
            update = self._queue.pop(0)
            current = {one.manifest.id: one for one in self.store.installed()}.get(
                update.extension
            )
            if current is None or (version_key(update.latest) or (0, 0, 0)) <= (
                version_key(current.manifest.version) or (0, 0, 0)
            ):
                continue  # already updated, or gone
            self.update(update)
            return

    def _build_table(self) -> None:
        """The table of the extensions, with the buttons for the one selected
        above it, as the other lists of the app have."""
        grid = self.form.extensionsCardsGrid
        self.actions = QWidget()
        self.actions_row = QHBoxLayout(self.actions)
        self.actions_row.setContentsMargins(0, 0, 0, 0)
        self.actions_row.setSpacing(8)
        self.count_label = QLabel()
        self.count_label.setProperty("variant", "muted")
        self.table = QTableWidget(0, len(COLUMNS))
        self.table.setObjectName("extensionsTable")
        self.table.setHorizontalHeaderLabels(
            [
                self.tr("NAME"),
                self.tr("VERSION"),
                self.tr("STATUS"),
                self.tr("AUTHOR"),
                self.tr("INSTALLED"),
                self.tr("UPDATED"),
                self.tr("SOURCE"),
                self.tr("DESCRIPTION"),
            ]
        )
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setShowGrid(False)
        self.table.setProperty("variant", "data")
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(46)  # as the Pods table
        self.table.setMinimumHeight(260)
        self.table.setItemDelegateForColumn(
            COLUMNS["status"], BadgeDelegate(self.table)
        )
        for column, width in WIDTHS.items():
            self.table.setColumnWidth(COLUMNS[column], width)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._menu)
        self.table.itemSelectionChanged.connect(self._sync_actions)
        self.table.cellDoubleClicked.connect(self._double_clicked)
        self.empty_label = QLabel(self.tr("No extension is installed"))
        grid.addWidget(self.actions, 0, 0)
        grid.addWidget(self.table, 1, 0)
        grid.addWidget(self.empty_label, 2, 0)
        grid.setColumnStretch(0, 1)
        grid.setRowStretch(1, 1)

    def render(self) -> None:
        """One row for each extension; the one that was selected stays so."""
        selected = self._selected_id()
        self.empty_label.setVisible(not self.rows)
        self.table.setVisible(bool(self.rows))
        self.table.setRowCount(len(self.rows))
        for index, row in enumerate(self.rows):
            manifest = row.manifest
            error = self.load_errors().get(manifest.id)
            status = self._badge(row)
            cells = {
                "name": f"{STAR} {manifest.name}" if row.recommended else manifest.name,
                "version": f"v{manifest.version}",
                "status": status,
                "author": manifest.author,
                "installed": self._day(row.installed_at),
                "updated": self._day(row.updated_at),
                "source": "" if row.bundled else row.source,
                "description": (
                    self.tr("Could not load: {error}").format(error=error)
                    if error
                    else manifest.description
                ),
            }
            for name, text in cells.items():
                item = QTableWidgetItem(text)
                item.setToolTip(manifest.description or text)
                if name == "status":
                    item.setData(BADGE_ROLE, self._status_colors(status, bool(error)))
                if name == "name" and row.recommended:
                    item.setToolTip(self.tr("Recommended by KubeScope"))
                    item.setForeground(QColor(themed("#3220a0", text=True)))
                if name == "description" and error:
                    item.setForeground(QColor(themed("#a33d45", text=True)))
                self.table.setItem(index, COLUMNS[name], item)
        if selected:
            for index, row in enumerate(self.rows):
                if row.manifest.id == selected:
                    self.table.selectRow(index)
        self.count_label.setText(
            self.tr("{count} extensions").format(count=len(self.rows))
        )
        self._sync_actions()

    def _selected_id(self) -> str:
        row = self._selected_row()
        return row.manifest.id if row is not None else ""

    def _selected_row(self) -> Row | None:
        index = self.table.currentRow()
        selected = self.table.selectionModel().hasSelection()
        return self.rows[index] if selected and 0 <= index < len(self.rows) else None

    def _status_colors(self, status: str, failed: bool) -> tuple[str, str]:
        """The text and fill colors of the badge of a status."""
        if failed:
            return themed("#a33d45"), themed("#fce9ea")
        if status in (self.tr("Installed"), self.tr("Bundled")):
            return themed("#176b58"), themed("#e5f4eb")
        if status in (self.tr("Update available"), self.tr("Development")):
            return themed("#985415"), themed("#fff2de")
        if status == self.tr("Recommended"):
            return themed("#3220a0"), themed("#f3f1f9")
        return themed("#505963"), themed("#eff1f3")

    def _sync_actions(self) -> None:
        """The line above the table only counts; what can be done with an
        extension is in its right-click menu, and Details is a double click."""
        while (item := self.actions_row.takeAt(0)) is not None:
            widget = item.widget()
            if widget is not None and widget is not self.count_label:
                widget.hide()
                widget.deleteLater()
        self.actions_row.addWidget(self.count_label)
        self.actions_row.addStretch(1)

    def _actions(self, row: Row) -> list[tuple[str, str, Callable[[], None]]]:
        """What can be done with an extension, as (label, variant, what to
        call)."""
        found: list[tuple[str, str, Callable[[], None]]] = [
            (self.tr("Details"), "secondary", partial(self.details, row))
        ]
        if row.default is not None:
            found.append(
                (
                    self.tr("Install"),
                    "primary",
                    partial(self.install_default, row.default),
                )
            )
            return found
        if row.update is not None:
            found.append(
                (
                    self.tr("Update to {version}").format(version=row.update.version),
                    "primary",
                    partial(self.update, row.update),
                )
            )
        if not row.installed or self._can_reinstall(row):
            found.append(
                (
                    self.tr("Reinstall"),
                    "primary" if not row.installed else "secondary",
                    partial(self.reinstall, row),
                )
            )
        if row.installed:
            found.append(
                (self.tr("Uninstall"), "secondary", partial(self.uninstall, row))
            )
        return found

    def _double_clicked(self, index: int, _column: int) -> None:
        if 0 <= index < len(self.rows):
            self.details(self.rows[index])

    def details(self, row: Row) -> None:
        """Everything about one extension, in a dialog."""
        manifest = row.manifest
        known = row.installed or not row.default
        ExtensionDetailsDialog(
            self.window,
            ExtensionDetails(
                name=manifest.name,
                id=manifest.id,
                version=manifest.version,
                status=self._badge(row),
                description=manifest.description,
                author=manifest.author,
                source="" if row.bundled else row.source,
                sha256=row.sha256,
                folder=row.folder if row.installed else "",
                installed_at=self._day(row.installed_at),
                updated_at=self._day(row.updated_at),
                permissions=tuple(sorted(manifest.permissions)),
                commands=manifest.commands,
                error=self.load_errors().get(manifest.id, ""),
                recommended=row.recommended,
                known=known,
                newer=row.update.version if row.update else "",
            ),
        ).exec()

    def _menu(self, position: QPoint) -> None:
        """Right-click on an extension: what can be done with it."""
        index = self.table.rowAt(position.y())
        if not 0 <= index < len(self.rows):
            return
        self.table.selectRow(index)
        menu = QMenu(self.table)
        for label, _variant, callback in self._actions(self.rows[index]):
            menu.addAction(label, callback)
        self._show_menu(menu, self.table.viewport().mapToGlobal(position))

    @staticmethod
    def _show_menu(menu: QMenu, where: QPoint) -> None:
        menu.exec(where)

    def _day(self, moment: str) -> str:
        """A day in the time zone of the settings, empty when there is none."""
        try:
            return to_zone(datetime.fromisoformat(moment)).strftime("%Y-%m-%d")
        except ValueError:
            return ""

    def _badge(self, row: Row) -> str:
        if row.default is not None:
            return self.tr("Recommended")
        if row.update is not None:
            return self.tr("Update available")
        if not row.installed:
            return self.tr("Uninstalled")
        if row.dev:
            return self.tr("Development")
        return self.tr("Bundled") if row.bundled else self.tr("Installed")

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

    def offer_defaults(self, settings: Settings) -> None:
        """The first time, offer what the app recommends: it is downloaded and
        a dialog asks before anything is installed.

        It is asked once, whatever the answer, and what is left can be
        installed from the cards.
        """
        have = {one.manifest.id for one in self.store.installed()}
        for one in self.defaults():
            if (
                not one.automatic
                or one.id in have
                or one.id in settings.extensions_offered
            ):
                continue
            settings.offered(one.id)
            settings.save()
            self._download(one.repo, one, review=False)

    def update(self, update: Update) -> None:
        """Download the newer version; the same dialog as any install shows
        what is new before it replaces the one that is installed."""
        self._download(update.repo, update.pin)

    def install_default(self, wanted: DefaultExtension) -> None:
        """Download the version of an extension that the app offers, which is
        installed only if its files are the ones that were pinned."""
        self._download(wanted.repo, wanted)

    def _download(
        self, repo: Repo, pin: DefaultExtension | None = None, review: bool = True
    ) -> None:
        self.run_action(
            download,
            lambda data: self._prepared(
                self.store.prepare, data, repo.source, pin=pin, review=review
            ),
            repo,
            on_error=self._download_failed,
        )

    def _download_failed(self, text: str) -> None:
        self._warn(text)
        self._next_update()

    def _prepared(
        self,
        prepare: Callable[..., Candidate],
        *arguments: object,
        pin: DefaultExtension | None = None,
        review: bool = True,
    ) -> None:
        try:
            candidate = prepare(*arguments)
            if pin is not None:
                try:
                    verify(candidate, pin)
                except StoreError:
                    self.store.discard(candidate)
                    raise
        except StoreError as error:
            self._warn(str(error))
            self._next_update()
            return
        if review:
            self._review(candidate)
        else:  # only a pinned one gets here
            self._install(candidate)

    def _review(self, candidate: Candidate) -> None:
        """Show what the extension is and install it if the person agrees."""
        dialog = InstallExtensionDialog(self.window, candidate)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            self.store.discard(candidate)
            self._next_update()
            return
        self._install(candidate)
        self._next_update()

    def _install(self, candidate: Candidate) -> None:
        try:
            self.store.install(candidate)
        except (StoreError, OSError) as error:
            logger.warning("Could not install an extension: %s", error)
            self._warn(str(error))
        self.refresh()
        self.changed()

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
        self.changed()

    def reinstall(self, row: Row) -> None:
        if not row.installed:  # a bundled one the person uninstalled
            try:
                self.store.restore_bundled(row.manifest.id)
            except StoreError as error:
                self._warn(str(error))
            self.refresh()
            self.changed()
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
            pin = next(  # one the app offers is checked against what was pinned
                (
                    one
                    for one in self.defaults()
                    if one.id == row.manifest.id and one.repo == repo
                ),
                None,
            )
            self._download(repo, pin)
