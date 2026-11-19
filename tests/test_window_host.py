import sys
from itertools import count
from pathlib import Path

import pytest
from PySide6.QtWidgets import QLabel, QMessageBox

from kubescope.extensions.manifest import MANIFEST_NAME
from kubescope.i18n import apply_language
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


def test_the_extension_of_the_app_is_not_run_by_the_loader_yet(window) -> None:
    assert "kubescope.gabi" not in window.extension_loader.loaded
    assert [one.manifest.id for one in window.extension_store.installed()] == [
        "kubescope.gabi"
    ]


def test_a_window_without_a_loader_yet_syncs_nothing(window) -> None:
    loader = window._extension_loader
    window._extension_loader = None

    window._sync_extensions()
    assert window._extension_errors() == {}

    window._extension_loader = loader
