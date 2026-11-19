import sys
from itertools import count
from pathlib import Path

import pytest
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QKeySequenceEdit, QLabel, QMessageBox, QPushButton

from kubescope.extensions.manifest import MANIFEST_NAME
from kubescope.i18n import apply_language, language_name, resolve_language
from kubescope.window import EXTENSION_SECTION_FIRST, EXTENSION_WATCH_MS
from tests.qt import present
from tests.test_window_flows import _ready_window

numbers = count(1)

RECORDER = """
CALLS = []


def activate(ctx):
    CALLS.append("activate")
    ctx.events.on(
        "context_changed", lambda context: CALLS.append(("context", context))
    )
    ctx.events.on("theme_changed", lambda: CALLS.append("theme"))
    ctx.events.on(
        "language_changed", lambda language: CALLS.append(("language", language))
    )
    ctx.events.on("shutdown", lambda: CALLS.append("shutdown"))
    ctx.events.on(
        "write_mode_changed", lambda write_mode: CALLS.append(("write", write_mode))
    )
    ctx.on_unload(lambda: CALLS.append("unload"))
    ctx.register_command(ctx.id + ".ping", lambda: "pong")
    ctx.settings.set("seen", True)
    CALLS.append(("ui", ctx.ui is not None, ctx.app.write_mode, ctx.current_context))
    CTX.append(ctx)


CTX = []
"""


def make_extension(
    tmp_path: Path, code: str = RECORDER, permissions: str = '"ui.window"'
) -> tuple[Path, str, str]:
    """An extension in a folder of its own, with a package nobody else has."""
    number = next(numbers)
    package = f"host_ext_{number}"
    extension = f"dco.host{number}"
    folder = tmp_path / package
    (folder / package).mkdir(parents=True)
    (folder / package / "__init__.py").write_text(code)
    (folder / MANIFEST_NAME).write_text(
        f'id = "{extension}"\nname = "Host {number}"\nversion = "1.0.0"\napi = "0"\n'
        f'entry = "{package}:activate"\npermissions = [{permissions}]\n'
    )
    return folder, package, extension


def install_linked(window, folder: Path) -> None:
    store = window.extension_store
    store.install(store.prepare_link(folder))
    window._sync_extensions()


def calls(package: str) -> list:
    return sys.modules[package].CALLS


@pytest.fixture(autouse=True)
def english_again():
    """A test that changes the language must not leave it changed."""
    yield
    apply_language("en")


@pytest.fixture
def window(monkeypatch):
    window = _ready_window(monkeypatch)
    yield window
    window.close()


def test_an_installed_extension_is_loaded_with_the_window_and_runs(
    window, tmp_path
) -> None:
    folder, package, extension = make_extension(tmp_path)

    install_linked(window, folder)

    assert window.extension_host.commands.invoke(f"{extension}.ping") == "pong"
    assert calls(package)[0] == "activate"
    assert ("ui", True, False, "prod") in calls(package)
    assert window.settings.extension_data(extension) == {"seen": True}


def test_syncing_again_does_not_load_it_twice(window, tmp_path) -> None:
    folder, package, _ = make_extension(tmp_path)
    install_linked(window, folder)

    window._sync_extensions()
    window._sync_extensions()

    assert calls(package).count("activate") == 1


def test_the_extension_hears_the_context_the_theme_and_the_language(
    window, tmp_path, monkeypatch
) -> None:
    folder, package, _ = make_extension(tmp_path)
    install_linked(window, folder)
    monkeypatch.setattr(window, "_sync_aws_menu", lambda: None)
    monkeypatch.setattr(window, "_select_default_namespace", lambda: None)

    window._context_changed()
    window._apply_theme()
    window._show_page(2)  # the form is filled when the page opens
    window.settings_ui.languageCombo.setCurrentIndex(
        window.settings_ui.languageCombo.findData("pt_BR")
    )
    window._save_preferences()

    heard = calls(package)
    assert ("context", "prod") in heard
    assert "theme" in heard
    assert ("language", "pt_BR") in heard


def test_uninstalling_it_unloads_it_and_takes_back_what_it_gave(
    window, tmp_path
) -> None:
    folder, package, extension = make_extension(tmp_path)
    install_linked(window, folder)
    recorded = calls(package)

    window.extension_store.uninstall(extension)
    window._sync_extensions()

    assert "unload" in recorded
    assert not window.extension_host.commands.has(f"{extension}.ping")
    assert extension not in window.extension_loader.loaded
    assert (folder / MANIFEST_NAME).is_file()  # the folder of the author stays


def test_an_extension_that_changed_is_reloaded(window, tmp_path) -> None:
    folder, package, extension = make_extension(tmp_path)
    install_linked(window, folder)
    (folder / MANIFEST_NAME).write_text(
        (folder / MANIFEST_NAME).read_text().replace('"1.0.0"', '"1.1.0"')
    )

    window._sync_extensions()

    assert (
        window.extension_loader.loaded[extension].installed.manifest.version == "1.1.0"
    )
    assert calls(package).count("activate") == 1  # a fresh module, a fresh list
    assert window.extension_host.commands.has(f"{extension}.ping")


def test_an_extension_that_fails_shows_why_and_the_others_run(window, tmp_path) -> None:
    broken, _, bad = make_extension(
        tmp_path, "def activate(ctx):\n    raise RuntimeError('boom\\nmore')\n"
    )
    good, good_package, _ = make_extension(tmp_path)

    install_linked(window, broken)
    install_linked(window, good)

    assert window.extension_loader.loaded[bad].error == "boom"
    assert calls(good_package)[0] == "activate"
    window.settings_ui.extensionsSectionButton.click()
    grid = window.settings_ui.extensionsCardsGrid
    errors = [
        label.text()
        for i in range(grid.count())
        for label in present(present(grid.itemAt(i)).widget()).findChildren(QLabel)
        if label.objectName() == "extensionCardError"
    ]
    assert errors == ["Could not load: boom"]


def test_the_extension_is_lent_the_window_and_the_corner_is_shared(
    window, tmp_path, monkeypatch
) -> None:
    folder, package, extension = make_extension(tmp_path)
    install_linked(window, folder)
    ctx = sys.modules[package].CTX[0]
    shown: list = []
    monkeypatch.setattr(
        window,
        "_show_message",
        lambda icon, title, text: shown.append((icon, title, text)),
    )
    base = window.ui.footerRow.contentsMargins().right()

    ctx.ui.show_message("warning", "Title", "Text")
    ctx.ui.show_message("nonsense", "T", "X")
    ctx.ui.reserve_corner(extension, 30)
    ctx.ui.reserve_corner("another", 12)

    assert shown == [
        (QMessageBox.Icon.Warning, "Title", "Text"),
        (QMessageBox.Icon.Information, "T", "X"),
    ]
    assert ctx.ui.window is window and ctx.ui.central is window.centralWidget()
    gutter = window.ui.footerRow.contentsMargins().right() - base
    assert gutter >= 42  # both of them, and Gabi's own button too
    ctx.ui.reserve_corner(extension, 0)
    assert window.ui.footerRow.contentsMargins().right() - base == gutter - 30


def test_the_window_offers_the_settings_to_an_extension(window, tmp_path) -> None:
    folder, package, _ = make_extension(tmp_path)
    install_linked(window, folder)
    ctx = sys.modules[package].CTX[0]

    ctx.ui.show_settings("anything")

    assert window.pages.currentIndex() == 2


def test_quitting_tells_the_extensions_and_unloads_them(window, tmp_path) -> None:
    folder, package, extension = make_extension(tmp_path)
    install_linked(window, folder)
    recorded = calls(package)

    window._quitting = True
    window.close()

    assert "shutdown" in recorded and "unload" in recorded
    assert extension not in window.extension_loader.loaded


def test_with_nothing_installed_nothing_runs(window) -> None:
    assert window.extension_loader.loaded == {}
    assert window.extension_store.installed() == []


def test_a_window_without_a_loader_yet_syncs_nothing(window) -> None:
    loader = window._extension_loader
    window._extension_loader = None

    window._sync_extensions()
    assert window._extension_errors() == {}

    window._extension_loader = loader


CONTRIBUTOR = """
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

FIRED = []
SAVES = []
PANELS = []
FAIL = {"build": False, "save": None, "handler": False}


class Panel(QWidget):
    def __init__(self):
        super().__init__()
        QVBoxLayout(self).addWidget(QLabel("the panel"))
        self.loads = 0

    def load(self):
        self.loads += 1

    def save(self):
        SAVES.append("save")
        if FAIL["save"] == "raise":
            raise RuntimeError("cannot save")
        return FAIL["save"] is None


def build():
    if FAIL["build"]:
        raise RuntimeError("cannot build")
    panel = Panel()
    PANELS.append(panel)
    return panel


def fire():
    FIRED.append("ask")
    if FAIL["handler"]:
        raise RuntimeError("handler failed")


def activate(ctx):
    ctx.add_shortcut(
        ctx.id + ".ask", "Ask the test", "Ctrl+Alt+T", fire, application=True
    )
    ctx.add_settings_section("Host Test", build)
"""

CONTRIBUTOR_PERMISSIONS = '"ui.window", "ui.settings"'


def contributing(tmp_path, window):
    folder, package, extension = make_extension(
        tmp_path, CONTRIBUTOR, CONTRIBUTOR_PERMISSIONS
    )
    install_linked(window, folder)
    return folder, sys.modules[package], extension


def shortcut_row(window, label: str) -> int | None:
    table = window.settings_ui.shortcutsTable
    for row in range(table.rowCount()):
        if present(table.item(row, 0)).text() == label:
            return row
    return None


def key_of(window, label: str) -> str:
    row = shortcut_row(window, label)
    assert row is not None
    edit = window.settings_ui.shortcutsTable.cellWidget(row, 1)
    assert isinstance(edit, QKeySequenceEdit)
    return edit.keySequence().toString()


def test_a_shortcut_of_an_extension_works_and_is_in_the_settings(
    window, tmp_path
) -> None:
    _, module, extension = contributing(tmp_path, window)
    action = f"{extension}.ask"

    shortcut = window._shortcuts[action]
    shortcut.activated.emit()

    assert shortcut.key().toString() == "Ctrl+Alt+T"
    assert shortcut.context().name == "ApplicationShortcut"
    assert module.FIRED == ["ask"]
    assert key_of(window, "Ask the test") == "Ctrl+Alt+T"


def test_the_key_of_an_extension_is_changed_in_the_settings_like_the_others(
    window, tmp_path
) -> None:
    _, _, extension = contributing(tmp_path, window)
    window._show_page(2)
    row = shortcut_row(window, "Ask the test")
    assert row is not None
    edit = window.settings_ui.shortcutsTable.cellWidget(row, 1)
    assert isinstance(edit, QKeySequenceEdit)

    edit.setKeySequence(QKeySequence("Ctrl+Alt+Y"))
    window._save_preferences()

    assert window.settings.shortcuts[f"{extension}.ask"] == "Ctrl+Alt+Y"
    assert window._shortcuts[f"{extension}.ask"].key().toString() == "Ctrl+Alt+Y"
    # and the default comes back with the button
    window.settings_ui.shortcutsResetButton.click()
    assert key_of(window, "Ask the test") == "Ctrl+Alt+T"


def test_a_failing_shortcut_of_an_extension_does_not_reach_the_window(
    window, tmp_path, caplog
) -> None:
    _, module, extension = contributing(tmp_path, window)
    module.FAIL["handler"] = True

    window._shortcuts[f"{extension}.ask"].activated.emit()

    assert module.FIRED == ["ask"]
    assert f"The extension {extension} failed" in caplog.text


def test_uninstalling_takes_back_the_shortcut_and_the_section(window, tmp_path) -> None:
    _, _, extension = contributing(tmp_path, window)

    window.extension_store.uninstall(extension)
    window._sync_extensions()

    assert f"{extension}.ask" not in window._shortcuts
    assert shortcut_row(window, "Ask the test") is None
    assert window._extension_sections == []
    assert "Host Test" not in [
        b.text()
        for b in window.settings_ui.settingsContent.parent().findChildren(QPushButton)
    ]


def test_a_section_of_an_extension_has_its_button_and_its_card(
    window, tmp_path
) -> None:
    _, module, _ = contributing(tmp_path, window)
    form = window.settings_ui
    content = form.settingsContent
    [entry] = window._extension_sections

    assert entry.id == EXTENSION_SECTION_FIRST and entry.title == "Host Test"
    assert entry.button.text() == "Host Test" and entry.button.isCheckable()
    assert not entry.card.isVisibleTo(content)  # until its button is pressed
    assert module.PANELS[0].loads >= 1

    entry.button.click()

    assert entry.card.isVisibleTo(content) and entry.button.isChecked()
    assert not form.generalCard.isVisibleTo(content)
    assert not form.generalSectionButton.isChecked()
    form.generalSectionButton.click()
    assert not entry.card.isVisibleTo(content) and not entry.button.isChecked()


def test_the_section_is_loaded_when_the_settings_open_and_saved_with_them(
    window, tmp_path
) -> None:
    _, module, _ = contributing(tmp_path, window)
    loads = module.PANELS[0].loads

    window._show_page(2)
    window._save_preferences()

    assert module.PANELS[0].loads > loads
    assert module.SAVES == ["save"]


@pytest.mark.parametrize("how", ["no", "raise"])
def test_a_section_that_refuses_or_fails_keeps_the_settings_from_saving(
    window, tmp_path, how
) -> None:
    _, module, _ = contributing(tmp_path, window)
    window._show_page(2)
    before = window.settings.remember_last_context
    window.settings_ui.rememberCheck.setChecked(not before)
    module.FAIL["save"] = how

    window._save_preferences()

    assert module.SAVES == ["save"]
    assert window.settings.remember_last_context is before  # nothing was applied


def test_a_section_that_cannot_be_built_is_left_out_and_the_rest_runs(
    window, tmp_path, caplog
) -> None:
    folder, _, extension = make_extension(
        tmp_path,
        CONTRIBUTOR.replace('"build": False', '"build": True'),
        CONTRIBUTOR_PERMISSIONS,
    )

    install_linked(window, folder)  # it loads, and its section fails to build

    assert window._extension_sections == []
    assert f"{extension}" in caplog.text and "could not build" in caplog.text
    assert f"{extension}.ask" in window._shortcuts  # the shortcut is there anyway


def test_an_extension_can_take_the_person_to_its_section(window, tmp_path) -> None:
    _, _, _ = contributing(tmp_path, window)
    [entry] = window._extension_sections

    window.extension_host.ui.show_settings("host TEST")

    assert window.pages.currentIndex() == 2 and entry.button.isChecked()


def test_an_extension_run_from_its_folder_is_reloaded_when_its_files_change(
    window, tmp_path
) -> None:
    folder, module, extension = contributing(tmp_path, window)
    package_file = next(folder.glob("host_ext_*/__init__.py"))
    assert extension in window._extension_watchers

    window._reload_changed_extensions()  # nothing changed
    assert shortcut_row(window, "Ask the test") is not None
    package_file.write_text(
        package_file.read_text().replace("Ask the test", "Ask the reloaded one")
    )
    window._reload_changed_extensions()

    assert shortcut_row(window, "Ask the test") is None
    assert shortcut_row(window, "Ask the reloaded one") is not None
    assert [one.title for one in window._extension_sections] == ["Host Test"]
    window._reload_changed_extensions()  # and it is told once
    assert shortcut_row(window, "Ask the reloaded one") is not None


def test_only_what_runs_from_its_folder_is_watched(window, tmp_path) -> None:
    folder, _, extension = make_extension(tmp_path)
    store = window.extension_store

    store.install(store.prepare_folder(folder))  # a copy, not the author's folder
    window._sync_extensions()

    assert window._extension_watchers == {}
    assert window._extension_timer.isActive()
    assert window._extension_timer.interval() == EXTENSION_WATCH_MS
    store.uninstall(extension)
    window._sync_extensions()


def test_the_watcher_goes_when_the_extension_does(window, tmp_path) -> None:
    _, _, extension = contributing(tmp_path, window)
    assert extension in window._extension_watchers

    window.extension_store.uninstall(extension)
    window._sync_extensions()

    assert window._extension_watchers == {}


def test_the_extension_asks_the_window_for_the_colors_of_the_theme(
    window, tmp_path
) -> None:
    from kubescope import theme

    folder, package, _ = make_extension(tmp_path)
    install_linked(window, folder)
    ui = sys.modules[package].CTX[0].ui

    assert ui.themed("#ffffff", False) == theme.themed("#ffffff")
    assert ui.themed("#ffffff", True) == theme.themed("#ffffff", text=True)


def test_the_extension_is_told_the_language_by_name_and_has_its_folder(
    window, tmp_path
) -> None:
    folder, package, extension = make_extension(tmp_path, permissions='"ui.window"')
    install_linked(window, folder)
    ctx = sys.modules[package].CTX[0]

    assert ctx.app.language_name == language_name(window.settings.language)
    assert ctx.app.resolved_language == resolve_language(window.settings.language)
    assert ctx.app.language_names[0] == "English" and len(ctx.app.language_names) > 5
    assert ctx.data_directory.name == extension
    assert ctx.data_directory.parent.name == "extension-data"


def test_the_extension_hears_when_the_write_mode_changes(window, tmp_path) -> None:
    folder, package, _ = make_extension(tmp_path)
    install_linked(window, folder)
    window._show_page(2)

    window.settings_ui.writeModeCheck.setChecked(True)
    window._save_preferences()
    window._save_preferences()  # the same again is not a change
    window.settings_ui.writeModeCheck.setChecked(False)
    window._save_preferences()

    assert [c for c in calls(package) if c[0:1] == ("write",)] == [
        ("write", True),
        ("write", False),
    ]
