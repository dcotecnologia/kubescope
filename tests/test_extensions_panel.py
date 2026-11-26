import io
import os
import shutil
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QInputDialog,
    QLabel,
    QMessageBox,
    QWidget,
)

from kubescope.dialogs.extension_dialog import InstallExtensionDialog
from kubescope.extensions.github import GithubError, Repo
from kubescope.extensions.manifest import MANIFEST_NAME
from kubescope.extensions.store import ExtensionStore, StoreError
from kubescope.ui.ui_settings_page import Ui_SettingsPage
from kubescope.views import extensions_panel
from kubescope.views.extensions_panel import ExtensionsPanel
from tests.qt import present

application = QApplication.instance() or QApplication([])


def manifest(extension: str, version: str = "1.0.0") -> bytes:
    return (
        f'id = "{extension}"\nname = "{extension.split(".")[1].title()}"\n'
        f'version = "{version}"\napi = "0"\nentry = "x:go"\n'
        'description = "Does things"\nauthor = "Someone"\n'
        'permissions = ["cluster.read"]\n'
    ).encode()


def tool_zip(extension: str = "dco.tool", version: str = "1.0.0") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        zipped.writestr(MANIFEST_NAME, manifest(extension, version))
        zipped.writestr("LICENSE", "MIT")
        zipped.writestr("README.md", "x")
        zipped.writestr("src/__init__.py", "")
    return buffer.getvalue()


def make_folder(root: Path, version: str = "1.0.0") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / MANIFEST_NAME).write_bytes(manifest("dco.tool", version))
    (root / "LICENSE").write_text("MIT")
    (root / "README.md").write_text("x")
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "tool.py").write_text("x = 1\n")
    return root


class Action:
    """An entry of the menu of an extension, pressed like a button."""

    def __init__(self, callback) -> None:
        self.callback = callback

    def click(self) -> None:
        self.callback()


@dataclass
class Card:
    title: str
    badge: str
    texts: list[str]
    buttons: dict[str, Action]
    details: Action | None = None


class Setup:
    def __init__(self, tmp_path, monkeypatch, with_bundled: bool = True) -> None:
        bundled = tmp_path / "bundled"
        bundled.mkdir()
        if with_bundled:
            (bundled / "gabi").mkdir()
            (bundled / "gabi" / MANIFEST_NAME).write_bytes(manifest("kubescope.gabi"))
        self.tmp_path = tmp_path
        self.store = ExtensionStore(tmp_path / "ext", bundled)
        self.window = QWidget()
        self.form = Ui_SettingsPage()
        self.form.setupUi(self.window)
        self.messages: list[str] = []
        self.downloads: list[Repo] = []
        self.changes = 0
        self.errors: dict[str, str] = {}
        self.panel = ExtensionsPanel(
            self.form,
            self.store,
            self.window,
            self.run_action,
            lambda _icon, _title, text: self.messages.append(text),
            changed=self.changed,
            load_errors=lambda: self.errors,
        )
        self.monkeypatch = monkeypatch
        self.dialogs: list[InstallExtensionDialog] = []

    def changed(self) -> None:
        self.changes += 1

    def run_action(self, operation, on_success, *arguments, on_error=None, **_):
        self.downloads.append(arguments[0])
        try:
            result = operation(*arguments)
        except GithubError as error:
            assert on_error is not None
            on_error(str(error))
            return
        on_success(result)

    def cards(self) -> list[Card]:
        table = self.panel.table
        found = []
        for row in range(table.rowCount()):
            texts = [
                present(table.item(row, column)).text()
                for column in range(table.columnCount())
            ]
            found.append(Card(texts[0].removeprefix("\u2605 "), texts[2], texts, {}))
        return found

    def card(self, title: str) -> Card:
        """The row of an extension, selected, with what can be done with it
        (the entries of its menu)."""
        table = self.panel.table
        row = next(i for i, one in enumerate(self.cards()) if one.title == title)
        table.selectRow(row)
        shown = self.cards()[row]
        actions = {
            label: Action(callback)
            for label, _variant, callback in self.panel._actions(self.panel.rows[row])
        }
        details = actions.pop("Details", None)
        return Card(shown.title, shown.badge, shown.texts, actions, details)

    def summary(self) -> list[tuple[str, str]]:
        return [(card.title, card.badge) for card in self.cards()]

    def pick_manifest(self, folder) -> None:
        chosen = str(Path(folder) / MANIFEST_NAME) if folder else ""
        self.monkeypatch.setattr(
            QFileDialog, "getOpenFileName", lambda *a, **k: (chosen, "")
        )

    def type_repository(self, text: str, accepted: bool = True) -> None:
        self.monkeypatch.setattr(
            QInputDialog, "getText", lambda *a, **k: (text, accepted)
        )

    def decide(self, accepted: bool) -> None:
        def run(dialog: InstallExtensionDialog) -> QDialog.DialogCode:
            self.dialogs.append(dialog)
            return (
                QDialog.DialogCode.Accepted if accepted else QDialog.DialogCode.Rejected
            )

        self.monkeypatch.setattr(InstallExtensionDialog, "exec", run)

    def confirm(self, yes: bool) -> None:
        answer = (
            QMessageBox.StandardButton.Yes if yes else QMessageBox.StandardButton.No
        )
        self.monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: answer)

    def dialog_text(self) -> str:
        return "\n".join(
            label.text() for label in self.dialogs[-1].findChildren(QLabel)
        )


@pytest.fixture
def setup(tmp_path, monkeypatch):
    return Setup(tmp_path, monkeypatch)


@pytest.fixture(autouse=True)
def every_version_works(monkeypatch):
    """The manifest of a tag is not asked of GitHub: any version works with the
    app, unless a test says otherwise."""
    monkeypatch.setattr(extensions_panel, "fetch_manifest", lambda repo: b"")


def test_the_bundled_extension_is_a_card_that_can_be_uninstalled(setup) -> None:
    gabi = setup.card("Gabi")

    assert (gabi.title, gabi.badge) == ("Gabi", "Bundled")
    assert {"v1.0.0", "Someone"} <= set(gabi.texts) and "Does things" in gabi.texts
    assert set(gabi.buttons) == {"Uninstall"}  # nothing to fetch again


def test_a_folder_is_installed_by_its_manifest_after_the_person_agrees(
    setup, tmp_path
) -> None:
    setup.decide(True)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)

    setup.panel.install_from_folder()

    assert setup.summary() == [("Tool", "Installed"), ("Gabi", "Bundled")]  # by id
    assert f"folder {folder}" in setup.card("Tool").texts
    assert set(setup.card("Tool").buttons) == {"Reinstall", "Uninstall"}
    assert (
        "SHA-256" in setup.dialog_text()
        and "Development mode" not in setup.dialog_text()
    )
    assert setup.messages == []


def test_development_mode_links_the_folder_instead_of_copying_it(
    setup, tmp_path
) -> None:
    setup.decide(True)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)
    setup.form.extensionsDevCheck.setChecked(True)

    setup.panel.install_from_folder()

    assert setup.card("Tool").badge == "Development"
    assert set(setup.card("Tool").buttons) == {"Uninstall"}  # it is the folder itself
    assert "Development mode: it runs from this folder" in setup.dialog_text()
    assert "SHA-256" not in setup.dialog_text()
    assert not (tmp_path / "ext" / "installed").exists()
    [linked] = [one for one in setup.store.installed() if one.dev]
    assert linked.folder == folder.resolve()


def test_declining_installs_nothing_and_keeps_the_folder_of_the_author(
    setup, tmp_path
) -> None:
    setup.decide(False)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)
    setup.panel.install_from_folder()
    setup.form.extensionsDevCheck.setChecked(True)
    setup.panel.install_from_folder()

    assert setup.summary() == [("Gabi", "Bundled")]
    assert (folder / MANIFEST_NAME).is_file() and (folder / "src" / "tool.py").is_file()
    assert list((tmp_path / "ext" / "staging").iterdir()) == []


def test_choosing_no_manifest_does_nothing(setup) -> None:
    setup.pick_manifest(None)

    setup.panel.install_from_folder()

    assert setup.messages == [] and len(setup.cards()) == 1


def test_a_folder_without_a_manifest_is_reported(setup, tmp_path) -> None:
    (tmp_path / "empty").mkdir()
    setup.pick_manifest(tmp_path / "empty")

    setup.panel.install_from_folder()
    setup.form.extensionsDevCheck.setChecked(True)
    setup.panel.install_from_folder()

    assert setup.messages == [f"There is no {MANIFEST_NAME} in it"] * 2


def test_a_repository_is_downloaded_and_installed(setup, monkeypatch) -> None:
    setup.decide(True)
    setup.type_repository("dco/tool")
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())

    setup.panel.install_from_github()

    assert setup.downloads == [Repo("dco", "tool")]
    assert "github dco/tool" in setup.card("Tool").texts


def test_a_repository_that_gives_no_extension_is_reported(setup, monkeypatch) -> None:
    setup.type_repository("dco/tool")
    monkeypatch.setattr(extensions_panel, "download", lambda repo: b"not a zip")

    setup.panel.install_from_github()

    assert setup.messages == ["It is not a zip file"]


def test_asking_for_a_repository_and_giving_up_does_nothing(setup) -> None:
    setup.type_repository("dco/tool", accepted=False)
    setup.panel.install_from_github()
    setup.type_repository("   ")
    setup.panel.install_from_github()

    assert setup.downloads == [] and setup.messages == []


def test_a_repository_that_is_not_one_is_reported(setup) -> None:
    setup.type_repository("nonsense")

    setup.panel.install_from_github()

    assert "owner/name" in setup.messages[0] and setup.downloads == []


def test_a_failed_download_is_reported(setup, monkeypatch) -> None:
    setup.type_repository("dco/tool")

    def fail(repo):
        raise GithubError("GitHub answered 404 for dco/tool")

    monkeypatch.setattr(extensions_panel, "download", fail)

    setup.panel.install_from_github()

    assert setup.messages == ["GitHub answered 404 for dco/tool"]


def test_an_install_that_fails_on_disk_is_reported(
    setup, tmp_path, monkeypatch
) -> None:
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))

    def fail(candidate):
        raise StoreError("the disk is full")

    monkeypatch.setattr(setup.store, "install", fail)

    setup.panel.install_from_folder()

    assert setup.messages == ["the disk is full"]


def test_uninstalling_the_bundled_extension_can_be_undone_by_reinstalling(
    setup,
) -> None:
    setup.confirm(True)

    setup.card("Gabi").buttons["Uninstall"].click()

    assert setup.summary() == [("Gabi", "Uninstalled")]
    assert set(setup.card("Gabi").buttons) == {"Reinstall"}

    setup.card("Gabi").buttons["Reinstall"].click()

    assert setup.summary() == [("Gabi", "Bundled")]


def test_uninstalling_asks_first_and_no_leaves_it(setup) -> None:
    setup.confirm(False)

    setup.card("Gabi").buttons["Uninstall"].click()

    assert setup.summary() == [("Gabi", "Bundled")]


def test_an_installed_extension_is_uninstalled_and_its_files_deleted(
    setup, tmp_path
) -> None:
    setup.decide(True)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)
    setup.panel.install_from_folder()
    setup.confirm(True)

    setup.card("Tool").buttons["Uninstall"].click()

    assert setup.summary() == [("Gabi", "Bundled")]
    assert not (tmp_path / "ext" / "installed" / "dco.tool").exists()
    assert (folder / "src" / "tool.py").is_file()  # the original stays


def test_a_linked_extension_is_uninstalled_without_touching_its_folder(
    setup, tmp_path
) -> None:
    setup.decide(True)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)
    setup.form.extensionsDevCheck.setChecked(True)
    setup.panel.install_from_folder()
    setup.confirm(True)

    setup.card("Tool").buttons["Uninstall"].click()

    assert setup.summary() == [("Gabi", "Bundled")]
    assert (folder / "src" / "tool.py").is_file()


def test_a_store_that_refuses_is_reported(setup, monkeypatch) -> None:
    setup.confirm(True)

    def refuse(extension):
        raise StoreError("nope")

    monkeypatch.setattr(setup.store, "uninstall", refuse)
    monkeypatch.setattr(setup.store, "restore_bundled", refuse)
    gabi = setup.panel.rows[0]
    setup.panel.uninstall(gabi)
    setup.panel.reinstall(extensions_panel.Row(gabi.manifest, "bundled", False))

    assert setup.messages == ["nope", "nope"]


def test_a_repository_extension_is_downloaded_again_on_reinstall(
    setup, monkeypatch
) -> None:
    setup.decide(True)
    setup.type_repository("https://github.com/dco/tool/tree/v1")
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())
    setup.panel.install_from_github()
    setup.downloads.clear()

    setup.card("Tool").buttons["Reinstall"].click()

    assert setup.downloads == [Repo("dco", "tool", "v1")]


def test_a_folder_extension_is_copied_again_from_its_folder_on_reinstall(
    setup, tmp_path
) -> None:
    setup.decide(True)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)
    setup.panel.install_from_folder()
    make_folder(folder, version="1.1.0")  # the author changed it
    setup.form.extensionsDevCheck.setChecked(True)  # and a reinstall still copies

    setup.card("Tool").buttons["Reinstall"].click()

    assert {"v1.1.0", "Someone"} <= set(setup.card("Tool").texts)
    assert setup.card("Tool").badge == "Installed"


def test_a_folder_that_is_gone_is_asked_for_again_on_reinstall(setup, tmp_path) -> None:
    setup.decide(True)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)
    setup.panel.install_from_folder()
    shutil.rmtree(folder)
    new = make_folder(tmp_path / "moved", version="2.0.0")
    setup.pick_manifest(new)  # where the person points this time

    setup.card("Tool").buttons["Reinstall"].click()

    assert {"v2.0.0", "Someone"} <= set(setup.card("Tool").texts)


def test_a_remembered_source_that_is_not_a_repository_is_reported(setup) -> None:
    row = extensions_panel.Row(setup.panel.rows[0].manifest, "github ../x", True)

    setup.panel.reinstall(row)

    assert "owner/name" in setup.messages[0]


def test_a_source_that_cannot_be_fetched_again_does_nothing(setup) -> None:
    row = extensions_panel.Row(setup.panel.rows[0].manifest, "other", True)

    setup.panel.reinstall(row)

    assert setup.downloads == [] and setup.messages == []


def test_without_extensions_the_page_says_so(tmp_path, monkeypatch) -> None:
    empty = Setup(tmp_path, monkeypatch, with_bundled=False)

    assert empty.panel.empty_label.text() == "No extension is installed"
    assert not empty.panel.empty_label.isHidden() and empty.panel.table.isHidden()


def test_the_room_of_the_page_goes_to_the_table_or_to_the_empty_note(
    setup, tmp_path, monkeypatch
) -> None:
    grid = setup.panel.form.extensionsCardsGrid
    assert (grid.rowStretch(1), grid.rowStretch(2)) == (1, 0)  # a table to fill

    (tmp_path / "empty").mkdir()
    empty = Setup(tmp_path / "empty", monkeypatch, with_bundled=False)
    grid = empty.panel.form.extensionsCardsGrid
    assert (grid.rowStretch(1), grid.rowStretch(2)) == (0, 1)  # the note, at the top


def test_the_window_is_told_when_something_was_installed_or_removed(
    setup, tmp_path
) -> None:
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))
    setup.confirm(True)

    setup.panel.install_from_folder()
    assert setup.changes == 1
    setup.card("Tool").buttons["Uninstall"].click()
    assert setup.changes == 2
    setup.card("Gabi").buttons["Uninstall"].click()
    setup.card("Gabi").buttons["Reinstall"].click()
    assert setup.changes == 4


def test_declining_or_failing_to_install_tells_the_window_nothing(
    setup, tmp_path
) -> None:
    setup.decide(False)
    setup.pick_manifest(make_folder(tmp_path / "tool"))

    setup.panel.install_from_folder()

    assert setup.changes == 0


def test_a_card_says_why_an_extension_did_not_load(setup) -> None:
    setup.errors = {"kubescope.gabi": "boom"}

    setup.panel.refresh()

    assert "Could not load: boom" in setup.card("Gabi").texts
    setup.errors = {}
    setup.panel.refresh()
    assert not any(t.startswith("Could not load") for t in setup.card("Gabi").texts)


def offered(tmp_path, sha256: str | None = None):
    """A default extension whose pin is what `tool_zip()` has when it is
    prepared."""
    from kubescope.extensions.defaults import DefaultExtension

    if sha256 is None:
        probe = ExtensionStore(tmp_path / "probe")
        sha256 = probe.prepare(tool_zip(), "github dco/tool@v1.0.0").sha256
    return DefaultExtension(
        "dco.tool", "Tool", "Does things", Repo("dco", "tool", "v1.0.0"), sha256
    )


def with_defaults(setup, *wanted):
    setup.panel.defaults = lambda: wanted
    setup.panel.refresh()


def test_what_the_app_offers_is_a_recommended_card_with_a_button_to_install(
    setup, tmp_path
) -> None:
    with_defaults(setup, offered(tmp_path))

    card = setup.card("Tool")

    assert card.badge == "Recommended"
    assert set(card.buttons) == {"Install"}
    assert "github dco/tool@v1.0.0" in card.texts and "v1.0.0" in card.texts
    assert "Does things" in card.texts


def test_the_pinned_version_is_downloaded_reviewed_and_installed(
    setup, tmp_path, monkeypatch
) -> None:
    with_defaults(setup, offered(tmp_path))
    setup.decide(True)
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())

    setup.card("Tool").buttons["Install"].click()

    assert setup.downloads == [Repo("dco", "tool", "v1.0.0")]
    assert setup.card("Tool").badge == "Installed"  # no longer only recommended
    assert setup.changes == 1


def test_files_that_are_not_the_pinned_ones_are_refused_and_not_staged(
    setup, tmp_path, monkeypatch
) -> None:
    with_defaults(setup, offered(tmp_path, sha256="f" * 64))
    setup.decide(True)
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())

    setup.card("Tool").buttons["Install"].click()

    assert "not the ones that were checked" in setup.messages[0]
    assert setup.dialogs == []  # the person is not even asked
    assert [card.title for card in setup.cards()] == ["Gabi", "Tool"]
    assert list((tmp_path / "ext" / "staging").iterdir()) == []


def test_another_extension_in_that_place_is_refused(
    setup, tmp_path, monkeypatch
) -> None:
    with_defaults(setup, offered(tmp_path))
    setup.decide(True)
    monkeypatch.setattr(
        extensions_panel, "download", lambda repo: tool_zip("dco.other")
    )

    setup.card("Tool").buttons["Install"].click()

    assert "That is not Gabi" not in setup.messages[0]
    assert "That is not Tool: it is dco.other" in setup.messages[0]


def test_what_is_installed_is_not_recommended_again(setup, tmp_path) -> None:
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))
    setup.panel.install_from_folder()

    with_defaults(setup, offered(tmp_path))

    assert [card.badge for card in setup.cards() if card.title == "Tool"] == [
        "Installed"
    ]


def test_uninstalling_what_the_app_offers_brings_it_back_as_recommended(
    setup, tmp_path, monkeypatch
) -> None:
    with_defaults(setup, offered(tmp_path))
    setup.decide(True)
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())
    setup.card("Tool").buttons["Install"].click()
    setup.confirm(True)

    setup.card("Tool").buttons["Uninstall"].click()

    assert setup.card("Tool").badge == "Recommended"


def test_reinstalling_what_the_app_offers_checks_the_pin_again(
    setup, tmp_path, monkeypatch
) -> None:
    wanted = offered(tmp_path)
    with_defaults(setup, wanted)
    setup.decide(True)
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())
    setup.card("Tool").buttons["Install"].click()
    # the tag now gives other files: the extension of the same id, changed
    monkeypatch.setattr(
        extensions_panel, "download", lambda repo: tool_zip(version="9.9.9")
    )
    setup.dialogs.clear()

    setup.card("Tool").buttons["Reinstall"].click()

    assert "not the ones that were checked" in setup.messages[-1]
    assert setup.dialogs == []


def test_what_the_app_recommends_is_offered_once(setup, tmp_path, monkeypatch) -> None:
    from kubescope.settings import Settings

    settings = Settings()
    with_defaults(setup, offered(tmp_path))
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())

    setup.panel.offer_defaults(settings)

    assert setup.dialogs == []  # no dialog: it is what the app pinned

    assert setup.card("Tool").badge == "Installed"
    assert settings.extensions_offered == ["dco.tool"]
    setup.dialogs.clear()
    setup.panel.store.uninstall("dco.tool")
    setup.panel.offer_defaults(settings)  # said yes once; it does not ask again
    assert setup.downloads == [Repo("dco", "tool", "v1.0.0")]


def test_what_is_only_recommended_is_a_card_and_is_not_installed_by_itself(
    setup, tmp_path, monkeypatch
) -> None:
    from dataclasses import replace

    from kubescope.settings import Settings

    settings = Settings()
    with_defaults(setup, replace(offered(tmp_path), automatic=False))
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())

    setup.panel.offer_defaults(settings)

    assert setup.downloads == [] and settings.extensions_offered == []
    assert setup.card("Tool").badge == "Recommended"


def test_a_row_says_when_it_was_installed_and_last_updated(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.extensions import store as store_module

    moments = iter(["2026-01-05T10:00:00+00:00", "2026-03-20T08:30:00+00:00"])
    monkeypatch.setattr(store_module, "_now", lambda: next(moments))
    monkeypatch.setattr("kubescope.sdk.timezone.to_zone", lambda moment: moment)
    monkeypatch.setattr(extensions_panel, "to_zone", lambda moment: moment)
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))
    setup.panel.install_from_folder()
    setup.pick_manifest(make_folder(tmp_path / "tool", "1.1.0"))
    setup.panel.install_from_folder()

    card = setup.card("Tool")

    assert card.texts[4:6] == ["2026-01-05", "2026-03-20"]  # INSTALLED, UPDATED


def test_what_comes_with_the_app_or_is_only_recommended_has_no_dates(
    setup, tmp_path
) -> None:
    with_defaults(setup, offered(tmp_path))

    assert not [t for t in setup.card("Tool").texts if "installed " in t]
    assert not [t for t in setup.card("Gabi").texts if "installed " in t]


def updates_window(monkeypatch, accept: bool) -> list[list[str]]:
    """Answer the window of the updates, and remember what it listed."""
    from kubescope.dialogs.extension_updates_dialog import ExtensionUpdatesDialog

    shown: list[list[str]] = []

    def run(dialog) -> QDialog.DialogCode:
        shown.append(
            [f"{one.name} {one.current} {one.version}" for one in dialog.updates]
        )
        return QDialog.DialogCode.Accepted if accept else QDialog.DialogCode.Rejected

    monkeypatch.setattr(ExtensionUpdatesDialog, "exec", run)
    return shown


def update_for(tmp_path, version="1.1.0"):
    from kubescope.extensions.updates import Update

    return Update(
        "dco.tool", "Tool", "1.0.0", f"v{version}", Repo("dco", "tool", f"v{version}")
    )


def installed_tool(setup, tmp_path, source="github dco/tool@v1.0.0") -> None:
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))
    setup.panel.install_from_folder()
    setup.panel.store._installed["dco.tool"]["source"] = source
    setup.panel.refresh()


def test_a_newer_version_is_a_badge_and_a_button_that_downloads_it(
    setup, tmp_path, monkeypatch
) -> None:
    installed_tool(setup, tmp_path)
    setup.panel.updates = [update_for(tmp_path)]
    setup.panel.refresh()

    card = setup.card("Tool")

    assert card.badge == "Update available"
    assert {"Update to 1.1.0", "Reinstall", "Uninstall"} <= set(card.buttons)
    monkeypatch.setattr(
        extensions_panel, "download", lambda repo: tool_zip(version="1.1.0")
    )
    setup.decide(True)

    card.buttons["Update to 1.1.0"].click()

    assert setup.downloads[-1] == Repo("dco", "tool", "v1.1.0")
    assert setup.card("Tool").badge == "Installed"  # no longer behind
    assert "v1.1.0" in setup.card("Tool").texts or "v1.1.0" in " ".join(
        setup.card("Tool").texts
    )


def test_an_update_that_is_not_newer_any_more_is_not_offered(setup, tmp_path) -> None:
    installed_tool(setup, tmp_path)
    setup.panel.updates = [update_for(tmp_path, "1.0.0")]
    setup.panel.refresh()

    assert setup.card("Tool").badge == "Installed"


def test_the_pinned_version_is_offered_without_asking_github(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.extensions.defaults import DefaultExtension

    installed_tool(setup, tmp_path)
    pin = DefaultExtension(
        "dco.tool", "Tool", "d", Repo("dco", "tool", "v1.0.1"), "a" * 64
    )
    setup.panel.defaults = lambda: [pin]
    setup.panel.run_action = lambda function, done, *a, **k: done(function(*a))
    asked = []
    monkeypatch.setattr(
        extensions_panel, "list_tags", lambda repo: asked.append(repo) or []
    )

    setup.panel.check_updates()

    assert setup.card("Tool").badge == "Update available"
    assert setup.panel.updates[0].pin is pin and asked == []
    assert setup.panel.updates_label.text() == "1 updates available"


def test_other_repositories_are_asked_once_a_day_and_the_time_is_kept(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.settings import Settings

    installed_tool(setup, tmp_path)
    setup.panel.defaults = lambda: []
    settings = Settings()
    saved = []
    setup.panel.save_settings = lambda: saved.append(1)
    setup.panel.run_action = lambda function, done, *a, **k: done(function(*a))
    asked = []
    monkeypatch.setattr(
        extensions_panel,
        "list_tags",
        lambda repo: asked.append(repo) or ["v1.2.0", "v1.1.0"],
    )
    updates_window(monkeypatch, accept=False)

    setup.panel.check_updates(settings)

    assert asked == [Repo("dco", "tool")] and saved  # the time, and what was seen
    assert setup.card("Tool").badge == "Update available"
    assert settings.extension_updates_checked_at > 0
    setup.panel.check_updates(settings)  # within a day: not again
    assert len(asked) == 1
    setup.panel.check_updates(settings, force=True)  # unless the person asks
    assert len(asked) == 2


def test_an_uninstalled_recommendation_shows_its_version_even_after_a_recent_check(
    setup, monkeypatch
) -> None:
    from kubescope.extensions.defaults import DefaultExtension
    from kubescope.settings import Settings

    setup.panel.defaults = lambda: [
        DefaultExtension(
            "kubescope.aws",
            "AWS",
            "Does things",
            Repo("dcotecnologia", "kubescope-aws"),
            author="DCO Tecnologia",
        )
    ]
    settings = Settings()
    settings.record_extension_updates_check(time.time())
    setup.panel.run_action = lambda operation, done, *args, **kwargs: done(
        operation(*args)
    )
    asked = []

    def tags(repo: Repo) -> list[str]:
        asked.append(repo)
        return ["v1.0.0", "v1.1.0-rc1"]

    monkeypatch.setattr(extensions_panel, "list_tags", tags)

    setup.panel.check_updates(settings)

    assert setup.card("AWS").texts[1] == "v1.0.0"
    assert setup.card("AWS").texts[3] == "DCO Tecnologia"
    assert asked == [Repo("dcotecnologia", "kubescope-aws")]


def test_a_failed_recommendation_check_reenables_the_button(setup) -> None:
    from kubescope.extensions.defaults import DefaultExtension
    from kubescope.settings import Settings

    setup.panel.defaults = lambda: [
        DefaultExtension(
            "kubescope.aws",
            "AWS",
            "Does things",
            Repo("dcotecnologia", "kubescope-aws"),
        )
    ]

    def fail(_operation, _done, *args, on_error=None, **kwargs) -> None:
        assert on_error is not None
        on_error("offline")

    setup.panel.run_action = fail

    setup.panel.check_updates(Settings())

    assert setup.panel.check_button.isEnabled()
    assert setup.panel._recommended_versions_checked == {"kubescope.aws"}


def test_with_the_updates_check_off_github_is_not_asked(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.settings import Settings

    installed_tool(setup, tmp_path)
    settings = Settings()
    settings.check_updates = False
    setup.panel.run_action = lambda function, done, *a, **k: done(function(*a))
    monkeypatch.setattr(
        extensions_panel, "list_tags", lambda repo: pytest.fail("asked")
    )

    setup.panel.check_updates(settings)

    assert setup.card("Tool").badge == "Installed"


def test_the_button_checks_even_when_it_was_checked_today(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.settings import Settings

    installed_tool(setup, tmp_path)
    setup.panel.run_action = lambda function, done, *a, **k: done(function(*a))
    monkeypatch.setattr(extensions_panel, "list_tags", lambda repo: [])

    setup.panel.check_button.click()

    assert setup.panel.updates_label.text() == "Everything is up to date"
    assert setup.panel.check_button.isEnabled()
    assert Settings().extension_updates_checked_at == 0.0  # no settings were given


def test_the_extensions_are_a_table_that_fills_the_width_at_any_size(
    setup, tmp_path
) -> None:
    with_defaults(setup, offered(tmp_path))
    host = setup.panel.form.extensionsCardsHost
    table = setup.panel.table
    setup.panel.window.show()

    for page in (1100, 700, 400):
        setup.panel.window.resize(page, 600)
        application.processEvents()
        application.processEvents()

        assert table.width() >= host.width() - 4  # the whole width
        assert table.rowCount() == 2
    assert host.minimumSizeHint().width() < 400  # it never makes the page wider


def test_the_buttons_do_not_make_the_page_wider_than_a_narrow_window(setup) -> None:
    form = setup.panel.form

    assert form.extensionsCard.minimumSizeHint().width() < 500
    row = form.extensionsButtonsRow
    layout = form.extensionsCardLayout
    assert layout.indexOf(form.extensionsDevCheck) == layout.indexOf(row) + 1


def test_right_click_offers_what_the_buttons_offer_and_the_selection_stays(
    setup, tmp_path, monkeypatch
) -> None:
    from PySide6.QtCore import QPoint

    with_defaults(setup, offered(tmp_path))
    table = setup.panel.table
    offered_actions: list[list[str]] = []
    monkeypatch.setattr(
        setup.panel,
        "_show_menu",
        lambda menu, where: offered_actions.append([a.text() for a in menu.actions()]),
    )
    setup.panel.window.show()

    setup.panel._menu(QPoint(5, table.rowViewportPosition(1) + 5))
    setup.panel._menu(QPoint(5, 10_000))  # below the rows: nothing

    assert offered_actions == [["Details", "Install"]]  # the recommended one is row 1
    setup.panel.refresh()
    assert setup.panel._selected_row() is not None
    assert setup.panel._selected_row().manifest.id == "dco.tool"  # type: ignore[union-attr]
    assert setup.panel.count_label.text() == "2 extensions"


def test_what_the_app_recommends_has_a_star_whether_or_not_it_is_installed(
    setup, tmp_path
) -> None:
    with_defaults(setup, offered(tmp_path))
    table = setup.panel.table

    names = [present(table.item(row, 0)).text() for row in range(table.rowCount())]

    assert names == ["Gabi", "\u2605 Tool"]  # only the recommended one
    from dataclasses import replace

    setup.panel.defaults = lambda: [
        replace(offered(tmp_path), id="kubescope.gabi", name="Gabi"),
    ]
    setup.panel.refresh()
    assert present(table.item(0, 0)).text() == "\u2605 Gabi"  # installed, and still


def opened_details(setup, monkeypatch):
    from kubescope.dialogs import extension_details_dialog as module

    shown = []

    def run(dialog) -> int:
        shown.append(
            (
                dialog.windowTitle(),
                " | ".join(label.text() for label in dialog.findChildren(QLabel)),
            )
        )
        return 0

    monkeypatch.setattr(module.ExtensionDetailsDialog, "exec", run)
    return shown


def test_details_show_everything_about_an_installed_extension(
    setup, tmp_path, monkeypatch
) -> None:
    shown = opened_details(setup, monkeypatch)
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))
    setup.panel.install_from_folder()

    card = setup.card("Tool")
    assert card.details is not None
    card.details.click()

    [(title, text)] = shown
    assert title == "Tool"
    for wanted in (
        "dco.tool",
        "v1.0.0",
        "Someone",
        "Does things",
        "folder ",
        "read your clusters",
    ):
        assert wanted in text
    assert "Installed" in text and "Updated" in text and "SHA-256" in text


def test_double_click_and_the_menu_open_the_details_too(
    setup, tmp_path, monkeypatch
) -> None:
    shown = opened_details(setup, monkeypatch)

    setup.panel._double_clicked(0, 0)
    setup.panel._double_clicked(9, 0)  # nothing there

    assert [title for title, _ in shown] == ["Gabi"]
    labels = [
        text
        for _label, _variant, text in [
            (a, b, c) for a, b, c in setup.panel._actions(setup.panel.rows[0])
        ]
    ]
    assert labels[0] is not None


def test_the_details_of_what_is_not_downloaded_say_the_permissions_come_later(
    setup, tmp_path, monkeypatch
) -> None:
    shown = opened_details(setup, monkeypatch)
    with_defaults(setup, offered(tmp_path))

    setup.card("Tool").details.click()  # type: ignore[union-attr]

    [(_, text)] = shown
    assert "They are shown when it is downloaded." in text
    assert "KubeScope recommends it" in text and "Recommended" in text


def test_details_say_that_a_newer_version_is_there_and_why_it_did_not_load(
    setup, tmp_path, monkeypatch
) -> None:
    shown = opened_details(setup, monkeypatch)
    setup.load_errors = {"dco.gabi": "boom"}
    installed_tool(setup, tmp_path)
    setup.panel.updates = [update_for(tmp_path)]
    setup.panel.refresh()

    setup.card("Tool").details.click()  # type: ignore[union-attr]

    assert "Newer version" in shown[0][1] and "v1.1.0" in shown[0][1]


def test_the_window_of_the_updates_is_shown_once_for_each_new_version(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.settings import Settings

    installed_tool(setup, tmp_path)
    settings = Settings()
    setup.panel.run_action = lambda function, done, *a, **k: done(function(*a))
    monkeypatch.setattr(extensions_panel, "list_tags", lambda repo: ["v1.1.0"])
    shown = updates_window(monkeypatch, accept=False)

    setup.panel.check_updates(settings, force=False)

    assert shown == [["Tool 1.0.0 1.1.0"]]
    assert settings.extension_updates_seen == ["dco.tool@v1.1.0"]
    setup.panel.check_updates(settings, force=True)  # asked: shown again
    assert len(shown) == 2
    settings.record_extension_updates_check(0)
    setup.panel._queue.clear()
    setup.panel.updates = []
    setup.panel.check_updates(settings)  # the same version: not told again
    assert len(shown) == 2
    monkeypatch.setattr(extensions_panel, "list_tags", lambda repo: ["v1.2.0"])
    setup.panel.check_updates(settings, force=True)
    assert len(shown) == 3 and shown[-1] == ["Tool 1.0.0 1.2.0"]


def test_the_button_opens_the_window_and_later_changes_nothing(
    setup, tmp_path, monkeypatch
) -> None:
    installed_tool(setup, tmp_path)
    setup.panel.updates = [update_for(tmp_path)]
    setup.panel._after_check()
    shown = updates_window(monkeypatch, accept=False)

    setup.panel.updates_button.click()

    assert shown == [["Tool 1.0.0 1.1.0"]]
    assert setup.downloads == [] and setup.panel.updates_button.isHidden() is False
    setup.panel.updates = []
    setup.panel.show_updates()  # nothing to offer: no window
    assert len(shown) == 1


def test_update_goes_through_the_extensions_one_at_a_time_and_shows_each(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.extensions.updates import Update

    installed_tool(setup, tmp_path)
    setup.panel.updates = [
        update_for(tmp_path),
        Update("dco.gone", "Gone", "1.0.0", "v2.0.0", Repo("dco", "gone", "v2.0.0")),
    ]
    updates_window(monkeypatch, accept=True)
    monkeypatch.setattr(
        extensions_panel, "download", lambda repo: tool_zip(version="1.1.0")
    )
    setup.decide(True)  # the install dialog of each

    setup.panel.show_updates()

    assert setup.downloads == [Repo("dco", "tool", "v1.1.0")]  # the other is gone
    assert setup.card("Tool").badge == "Installed" and setup.changes >= 1
    assert setup.panel._queue == []


def test_a_refused_or_failed_update_does_not_stop_the_next_one(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.extensions.github import GithubError
    from kubescope.extensions.updates import Update

    installed_tool(setup, tmp_path)
    second = Update(
        "kubescope.gabi", "Gabi", "1.0.0", "v1.1.0", Repo("dco", "gabi", "v1.1.0")
    )
    setup.panel.updates = [second, update_for(tmp_path)]
    updates_window(monkeypatch, accept=True)

    def download(repo):
        if repo.name == "gabi":
            raise GithubError("rate limit")
        return tool_zip(version="1.1.0")

    monkeypatch.setattr(extensions_panel, "download", download)
    setup.decide(False)  # the person says no to the dialog of the install

    setup.panel.show_updates()

    assert [repo.name for repo in setup.downloads] == ["gabi", "tool"]
    assert "rate limit" in setup.messages[0]
    assert setup.card("Tool").texts[1] == "v1.0.0"  # declined: nothing replaced
    assert setup.panel._queue == []


def test_the_buttons_that_install_or_look_for_updates_look_alike(setup) -> None:
    form = setup.panel.form

    variants = {
        button.property("variant")
        for button in (
            form.extensionsInstallFolderButton,
            form.extensionsInstallRepoButton,
            setup.panel.check_button,
        )
    }

    assert variants == {"secondary"}


def latest_of_tool():
    from kubescope.extensions.defaults import DefaultExtension

    return DefaultExtension("dco.tool", "Tool", "Does things", Repo("dco", "tool"))


def test_what_is_recommended_without_a_tag_is_the_latest_release(
    setup, monkeypatch
) -> None:
    with_defaults(setup, latest_of_tool())
    setup.decide(True)
    downloaded = []
    monkeypatch.setattr(
        extensions_panel, "list_tags", lambda repo: ["v1.1.0", "main", "v1.2.0"]
    )
    monkeypatch.setattr(
        extensions_panel,
        "download",
        lambda repo: downloaded.append(repo) or tool_zip(version="1.2.0"),
    )

    setup.card("Tool").buttons["Install"].click()

    assert downloaded == [Repo("dco", "tool", "v1.2.0")]  # the highest final tag
    assert setup.card("Tool").badge == "Installed"
    assert setup.store.source_of("dco.tool") == "github dco/tool@v1.2.0"


def test_a_recommended_repository_without_a_release_says_so(setup, monkeypatch) -> None:
    with_defaults(setup, latest_of_tool())
    setup.decide(True)
    monkeypatch.setattr(extensions_panel, "list_tags", lambda repo: ["main"])
    monkeypatch.setattr(
        extensions_panel, "download", lambda repo: pytest.fail("downloaded")
    )

    setup.card("Tool").buttons["Install"].click()

    assert "dco/tool has no release yet" in setup.messages[0]
    assert setup.card("Tool").badge == "Recommended"


def test_a_repository_the_person_types_is_taken_as_typed_not_as_its_latest_tag(
    setup, monkeypatch
) -> None:
    setup.decide(True)
    setup.type_repository("dco/tool")
    downloaded = []
    monkeypatch.setattr(
        extensions_panel, "list_tags", lambda repo: pytest.fail("looked for tags")
    )
    monkeypatch.setattr(
        extensions_panel,
        "download",
        lambda repo: downloaded.append(repo) or tool_zip(),
    )

    setup.panel.install_from_github()

    assert downloaded == [Repo("dco", "tool")]


def test_a_check_that_is_running_is_not_started_again(setup) -> None:
    setup.panel._checking = True
    calls = []
    setup.panel.run_action = lambda *a, **k: calls.append(1)

    setup.panel.check_updates(force=True)

    assert calls == []


def test_the_menu_of_the_table_is_shown_where_the_person_clicked(setup) -> None:
    from PySide6.QtCore import QPoint, QTimer
    from PySide6.QtWidgets import QMenu

    menu = QMenu()
    menu.addAction("Details")
    QTimer.singleShot(0, menu.close)  # nobody answers it: close it at once

    setup.panel._show_menu(menu, QPoint(0, 0))

    assert not menu.isVisible()


def test_what_cannot_be_downloaded_by_default_is_quiet_and_tried_again_next_start(
    setup, monkeypatch
) -> None:
    from kubescope.extensions.github import GithubError
    from kubescope.settings import Settings

    settings = Settings()
    with_defaults(setup, latest_of_tool())
    monkeypatch.setattr(
        extensions_panel,
        "list_tags",
        lambda repo: (_ for _ in ()).throw(GithubError("GitHub answered 403")),
    )

    setup.panel.offer_defaults(settings)

    assert setup.messages == []  # nothing is said
    assert settings.extensions_offered == []  # and it is tried again at the next start
    monkeypatch.setattr(extensions_panel, "list_tags", lambda repo: ["v1.0.0"])
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())
    setup.panel.offer_defaults(settings)
    assert settings.extensions_offered == ["dco.tool"]


def test_a_default_that_cannot_be_installed_is_not_marked_as_offered(
    setup, tmp_path, monkeypatch
) -> None:
    from kubescope.settings import Settings

    settings = Settings()
    with_defaults(setup, offered(tmp_path))
    monkeypatch.setattr(
        extensions_panel, "download", lambda repo: tool_zip("dco.other")
    )  # not the extension it should be

    setup.panel.offer_defaults(settings)

    assert setup.messages == [] and settings.extensions_offered == []


def test_what_ships_with_the_app_is_installed_without_the_network(
    setup, monkeypatch
) -> None:
    from kubescope.extensions.offline import Snapshot
    from kubescope.settings import Settings

    settings = Settings()
    with_defaults(setup, latest_of_tool())
    setup.panel.snapshots = lambda extension: Snapshot(
        tool_zip(version="1.3.0"), Repo("dco", "tool", "v1.3.0")
    )
    monkeypatch.setattr(
        extensions_panel, "list_tags", lambda repo: pytest.fail("looked for tags")
    )
    monkeypatch.setattr(
        extensions_panel, "download", lambda repo: pytest.fail("downloaded")
    )

    setup.panel.offer_defaults(settings)

    assert setup.card("Tool").badge == "Installed"
    assert setup.store.source_of("dco.tool") == "github dco/tool@v1.3.0"
    assert settings.extensions_offered == ["dco.tool"] and setup.messages == []


def test_a_copy_that_is_not_the_extension_is_not_installed(setup) -> None:
    from kubescope.extensions.offline import Snapshot
    from kubescope.settings import Settings

    settings = Settings()
    with_defaults(setup, latest_of_tool())
    setup.panel.snapshots = lambda extension: Snapshot(
        tool_zip("dco.other"), Repo("dco", "tool", "v1.0.0")
    )

    setup.panel.offer_defaults(settings)

    assert settings.extensions_offered == [] and setup.messages == []
    assert [card.title for card in setup.cards()] == ["Gabi", "Tool"]


def test_a_click_on_a_header_sorts_the_extensions_and_the_row_keeps_its_actions(
    setup, tmp_path
) -> None:
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))
    setup.panel.install_from_folder()
    assert [card.title for card in setup.cards()] == ["Tool", "Gabi"]

    setup.panel.sorter.clicked(0)  # the name
    assert [card.title for card in setup.cards()] == ["Gabi", "Tool"]

    setup.panel.sorter.clicked(0)
    assert [card.title for card in setup.cards()] == ["Tool", "Gabi"]

    assert setup.card("Gabi").title == "Gabi"  # the row selected is its own extension


def test_the_table_of_the_updates_sorts_when_a_header_is_clicked() -> None:
    from kubescope.dialogs.extension_updates_dialog import ExtensionUpdatesDialog
    from kubescope.extensions.updates import Update

    updates = [
        Update("dco.b", "Bravo", "1.9.0", "v1.10.0", Repo("dco", "b", "v1.10.0")),
        Update("dco.a", "Alpha", "1.0.0", "v1.1.0", Repo("dco", "a", "v1.1.0")),
    ]
    dialog = ExtensionUpdatesDialog(None, updates)

    def names() -> list[str]:
        return [present(dialog.table.item(row, 0)).text() for row in range(2)]

    assert names() == ["Bravo", "Alpha"]

    dialog.table.horizontalHeader().sectionClicked.emit(0)

    assert names() == ["Alpha", "Bravo"]


def test_the_repository_of_an_extension_is_where_it_came_from_or_is_offered() -> None:
    from types import SimpleNamespace

    def row(source, default=None, extension="dco.other"):
        return SimpleNamespace(
            source=source, default=default, manifest=SimpleNamespace(id=extension)
        )

    repository = cast(Any, ExtensionsPanel._repository)  # a row is only read
    assert (
        repository(row("github dcotecnologia/kubescope-aws@v1.3.0"))
        == "https://github.com/dcotecnologia/kubescope-aws"
    )
    offered = SimpleNamespace(repo=Repo("dcotecnologia", "kubescope-search"))
    assert (
        repository(row("bundled", offered))
        == "https://github.com/dcotecnologia/kubescope-search"
    )
    assert (  # the one the app has inside it is looked up in the offers by its id
        repository(row("bundled", None, "kubescope.aws"))
        == "https://github.com/dcotecnologia/kubescope-aws"
    )
    assert repository(row("folder /x")) == ""  # one of the author's own folders
