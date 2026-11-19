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
from kubescope.ui.ui_settings_page import Ui_SettingsPage

logger = logging.getLogger(__name__)

FOLDER_SOURCE = "folder "  # how the store remembers an extension from a folder
UPDATE_CHECK_SECONDS = 24 * 3600  # how often GitHub is asked for newer tags
CARD_WIDTH = 260  # pixels a card needs at least; two fit in a narrow window
GAP = 14


@dataclass(frozen=True)
class Row:
    manifest: Manifest
    source: str  # "bundled", "folder /x", "github o/r", "dev /x"
    installed: bool
    default: DefaultExtension | None = None  # one the app offers, not installed
    installed_at: str = ""  # UTC, as the store keeps it
    updated_at: str = ""
    update: Update | None = None  # a newer version that can be installed

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
        self.updates_label = QLabel()
        self.updates_label.setObjectName("extensionUpdatesLabel")
        self.updates_label.setProperty("variant", "muted")
        self.updates_label.hide()
        self.check_button = QPushButton(self.tr("Check for updates"))
        self.check_button.setProperty("variant", "secondary")
        form.extensionsButtonsRow.insertWidget(
            form.extensionsButtonsRow.indexOf(form.extensionsInstallRepoButton) + 1,
            self.check_button,
        )
        form.extensionsCardLayout.insertWidget(
            form.extensionsCardLayout.indexOf(form.extensionsCardsHost),
            self.updates_label,
        )
        self.check_button.clicked.connect(lambda: self.check_updates(force=True))
        self.rows: list[Row] = []
        self._columns = 1
        form.extensionsInstallFolderButton.clicked.connect(self.install_from_folder)
        form.extensionsInstallRepoButton.clicked.connect(self.install_from_github)
        form.extensionsCardsHost.installEventFilter(self)
        self.refresh()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """More cards side by side when the page gives room for them."""
        shown = event.type() in (QEvent.Type.Resize, QEvent.Type.Show)
        if shown and self._fit_columns() != self._columns:
            self.render()
        return False

    def _fit_columns(self) -> int:
        width = self.form.extensionsCardsHost.width()
        return max(1, (width + GAP) // (CARD_WIDTH + GAP))

    # what is shown

    def refresh(self) -> None:
        """Read the store again and draw the cards."""
        self.rows = [
            Row(
                one.manifest,
                one.source,
                True,
                installed_at=one.installed_at,
                updated_at=one.updated_at,
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
                self.rows.append(Row(manifest, f"github {one.repo.label}", False, one))
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
        self._after_check()
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
            self._after_check(told=force)

        def failed(_message: str) -> None:
            self._checking = False
            self.check_button.setEnabled(True)

        self.run_action(
            partial(find, installed, defaults, list_tags),
            done,
            on_error=failed,
            quiet=True,
        )

    def _after_check(self, told: bool = False) -> None:
        count = len(self.updates)
        self.updates_label.setVisible(count > 0 or told)
        self.updates_label.setText(
            self.tr("{count} updates available").format(count=count)
            if count
            else self.tr("Everything is up to date")
        )
        self.refresh()

    def render(self) -> None:
        grid = self.form.extensionsCardsGrid
        while (item := grid.takeAt(0)) is not None:
            if widget := item.widget():
                widget.deleteLater()
        for column in range(grid.columnCount()):
            grid.setColumnStretch(column, 0)  # the ones of the last drawing
            grid.setColumnMinimumWidth(column, 0)
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
        if row.default is not None:
            return self.tr("Recommended")
        if row.update is not None:
            return self.tr("Update available")
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
        dates = self._dates(row)
        if dates:
            when = QLabel(dates)
            when.setObjectName("extensionCardDates")
            when.setProperty("variant", "muted")
            layout.addWidget(when)
        description = QLabel(manifest.description)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(description, 1)
        error = self.load_errors().get(manifest.id)
        if error:
            problem = QLabel(self.tr("Could not load: {error}").format(error=error))
            problem.setObjectName("extensionCardError")
            problem.setWordWrap(True)
            problem.setStyleSheet("color: #c0392b;")
            layout.addWidget(problem)
        if not row.bundled:
            source = QLabel(row.source)
            source.setWordWrap(True)
            source.setProperty("variant", "muted")
            source.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            layout.addWidget(source)
        buttons = QHBoxLayout()
        if row.default is not None:
            install = QPushButton(self.tr("Install"))
            install.setProperty("variant", "primary")
            install.clicked.connect(partial(self.install_default, row.default))
            buttons.addWidget(install)
        elif row.update is not None:
            update = QPushButton(
                self.tr("Update to {version}").format(version=row.update.version)
            )
            update.setProperty("variant", "primary")
            update.clicked.connect(partial(self.update, row.update))
            buttons.addWidget(update)
            if self._can_reinstall(row):
                reinstall = QPushButton(self.tr("Reinstall"))
                reinstall.setProperty("variant", "secondary")
                reinstall.clicked.connect(partial(self.reinstall, row))
                buttons.addWidget(reinstall)
        elif not row.installed or self._can_reinstall(row):
            reinstall = QPushButton(self.tr("Reinstall"))
            reinstall.setProperty(
                "variant", "primary" if not row.installed else "secondary"
            )
            reinstall.clicked.connect(partial(self.reinstall, row))
            buttons.addWidget(reinstall)
        if row.installed and row.default is None:
            uninstall = QPushButton(self.tr("Uninstall"))
            uninstall.setProperty("variant", "secondary")
            uninstall.clicked.connect(partial(self.uninstall, row))
            buttons.addWidget(uninstall)
        buttons.addStretch(1)
        layout.addLayout(buttons)
        return card

    def _dates(self, row: Row) -> str:
        """When it was installed and last updated, in lowercase, in the time
        zone of the settings; nothing for what was never installed here."""
        parts = []
        for text, moment in (
            (self.tr("installed {date}"), row.installed_at),
            (self.tr("updated {date}"), row.updated_at),
        ):
            try:
                day = to_zone(datetime.fromisoformat(moment)).strftime("%Y-%m-%d")
            except ValueError:
                continue
            parts.append(text.format(date=day).lower())
        return " · ".join(parts)

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
            on_error=self._warn,
        )

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
            return
        self._install(candidate)

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
