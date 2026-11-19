import io
import os
import zipfile
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
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
    return buffer.getvalue()


def make_folder(root: Path, version: str = "1.0.0") -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / MANIFEST_NAME).write_bytes(manifest("dco.tool", version))
    (root / "tool.py").write_text("x = 1\n")
    return root


@dataclass
class Card:
    title: str
    badge: str
    texts: list[str]
    buttons: dict[str, QPushButton]


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
        grid = self.form.extensionsCardsGrid
        found = []
        for index in range(grid.count()):
            widget = present(present(grid.itemAt(index)).widget())
            labels = widget.findChildren(QLabel)
            title = widget.findChild(QLabel, "extensionCardTitle")
            badge = widget.findChild(QLabel, "extensionCardBadge")
            found.append(
                Card(
                    title.text() if title else "",
                    badge.text() if badge else "",
                    [label.text() for label in labels],
                    {b.text(): b for b in widget.findChildren(QPushButton)},
                )
            )
        return found

    def card(self, title: str) -> Card:
        return next(card for card in self.cards() if card.title == title)

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


def test_the_bundled_extension_is_a_card_that_can_be_uninstalled(setup) -> None:
    [gabi] = setup.cards()

    assert (gabi.title, gabi.badge) == ("Gabi", "Bundled")
    assert "v1.0.0 · Someone" in gabi.texts and "Does things" in gabi.texts
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
    assert (folder / MANIFEST_NAME).is_file() and (folder / "tool.py").is_file()
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
    assert (folder / "tool.py").is_file()  # the original stays


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
    assert (folder / "tool.py").is_file()


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

    assert "v1.1.0 · Someone" in setup.card("Tool").texts
    assert setup.card("Tool").badge == "Installed"


def test_a_folder_that_is_gone_is_asked_for_again_on_reinstall(setup, tmp_path) -> None:
    setup.decide(True)
    folder = make_folder(tmp_path / "tool")
    setup.pick_manifest(folder)
    setup.panel.install_from_folder()
    (folder / MANIFEST_NAME).unlink()
    (folder / "tool.py").unlink()
    folder.rmdir()
    new = make_folder(tmp_path / "moved", version="2.0.0")
    setup.pick_manifest(new)  # where the person points this time

    setup.card("Tool").buttons["Reinstall"].click()

    assert "v2.0.0 · Someone" in setup.card("Tool").texts


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

    assert [
        label.text() for label in empty.form.extensionsCardsHost.findChildren(QLabel)
    ] == ["No extension is installed"]


def test_more_cards_sit_side_by_side_when_the_page_has_room(setup, tmp_path) -> None:
    setup.decide(True)
    setup.pick_manifest(make_folder(tmp_path / "tool"))
    setup.panel.install_from_folder()
    host = setup.form.extensionsCardsHost
    grid = setup.form.extensionsCardsGrid

    host.resize(200, 300)
    setup.panel.eventFilter(host, QEvent(QEvent.Type.Resize))
    narrow = [grid.getItemPosition(i)[:2] for i in range(grid.count())]
    host.resize(900, 300)
    assert setup.panel.eventFilter(host, QEvent(QEvent.Type.Resize)) is False
    wide = [grid.getItemPosition(i)[:2] for i in range(grid.count())]
    setup.panel.eventFilter(host, QEvent(QEvent.Type.Resize))  # the same width again

    assert narrow == [(0, 0), (1, 0)] and wide == [(0, 0), (0, 1)]
    assert setup.panel.eventFilter(host, QEvent(QEvent.Type.Show)) is False


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


def test_the_cards_fill_the_width_after_the_page_gets_narrower(setup, tmp_path) -> None:
    with_defaults(setup, offered(tmp_path))
    grid = setup.panel.form.extensionsCardsGrid
    host = setup.panel.form.extensionsCardsHost
    setup.panel.window.show()
    widths = {}
    for page in (1100, 700):
        setup.panel.window.resize(page, 600)
        application.processEvents()
        application.processEvents()
        widths[page] = [grid.itemAt(i).widget().width() for i in range(grid.count())]

    row = widths[700][:2] if host.width() >= 2 * 260 + 14 else widths[700][:1]
    assert sum(row) + 14 * (len(row) - 1) >= host.width() - 4  # the whole width


def test_a_card_says_in_lowercase_when_it_was_installed_and_last_updated(
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

    assert "installed 2026-01-05 · updated 2026-03-20" in card.texts
    assert not any(text.startswith("Installed ") for text in card.texts)


def test_what_comes_with_the_app_or_is_only_recommended_has_no_dates(
    setup, tmp_path
) -> None:
    with_defaults(setup, offered(tmp_path))

    assert not [t for t in setup.card("Tool").texts if "installed " in t]
    assert not [t for t in setup.card("Gabi").texts if "installed " in t]


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

    setup.panel.check_updates(settings)

    assert asked == [Repo("dco", "tool")] and saved == [1]
    assert setup.card("Tool").badge == "Update available"
    assert settings.extension_updates_checked_at > 0
    setup.panel.check_updates(settings)  # within a day: not again
    assert len(asked) == 1
    setup.panel.check_updates(settings, force=True)  # unless the person asks
    assert len(asked) == 2


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
