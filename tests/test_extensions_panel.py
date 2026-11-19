import io
import os
import zipfile

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QInputDialog,
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
from tests.qt import cell

application = QApplication.instance() or QApplication([])


def manifest(extension: str, version: str = "1.0.0") -> bytes:
    return (
        f'id = "{extension}"\nname = "{extension.split(".")[1].title()}"\n'
        f'version = "{version}"\napi = "0"\nentry = "x:go"\n'
        'permissions = ["cluster.read"]\n'
    ).encode()


def tool_zip(extension: str = "dco.tool", version: str = "1.0.0") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zipped:
        zipped.writestr(MANIFEST_NAME, manifest(extension, version))
    return buffer.getvalue()


class Setup:
    def __init__(self, tmp_path, monkeypatch) -> None:
        bundled = tmp_path / "bundled"
        (bundled / "gabi").mkdir(parents=True)
        (bundled / "gabi" / MANIFEST_NAME).write_bytes(manifest("dco.gabi"))
        self.store = ExtensionStore(tmp_path / "ext", bundled)
        self.window = QWidget()
        self.form = Ui_SettingsPage()
        self.form.setupUi(self.window)
        self.messages: list[str] = []
        self.downloads: list[Repo] = []
        self.panel = ExtensionsPanel(
            self.form,
            self.store,
            self.window,
            self.run_action,
            lambda _icon, _title, text: self.messages.append(text),
        )
        self.table = self.form.extensionsTable
        self.answers: dict[str, object] = {}
        self.monkeypatch = monkeypatch

    def run_action(self, operation, on_success, *arguments, on_error=None, **_):
        self.downloads.append(arguments[0])
        try:
            result = operation(*arguments)
        except GithubError as error:
            assert on_error is not None
            on_error(str(error))
            return
        on_success(result)

    def pick_file(self, path) -> None:
        self.monkeypatch.setattr(
            QFileDialog, "getOpenFileName", lambda *a, **k: (str(path), "")
        )

    def type_repository(self, text: str, accepted: bool = True) -> None:
        self.monkeypatch.setattr(
            QInputDialog, "getText", lambda *a, **k: (text, accepted)
        )

    def decide(self, accepted: bool) -> list[InstallExtensionDialog]:
        shown: list[InstallExtensionDialog] = []

        def run(dialog: InstallExtensionDialog) -> int:
            shown.append(dialog)
            return (
                QDialog.DialogCode.Accepted if accepted else QDialog.DialogCode.Rejected
            )

        self.monkeypatch.setattr(InstallExtensionDialog, "exec", run)
        return shown

    def confirm(self, yes: bool) -> None:
        answer = (
            QMessageBox.StandardButton.Yes if yes else QMessageBox.StandardButton.No
        )
        self.monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: answer)

    def select(self, name: str) -> None:
        for row in range(self.table.rowCount()):
            if cell(self.table, row, 0).text() == name:
                self.table.selectRow(row)
                return
        raise AssertionError(name)

    def rows(self) -> list[tuple[str, ...]]:
        return [
            tuple(cell(self.table, row, column).text() for column in range(4))
            for row in range(self.table.rowCount())
        ]


@pytest.fixture
def setup(tmp_path, monkeypatch):
    return Setup(tmp_path, monkeypatch)


def zip_file(tmp_path, data: bytes, name: str = "tool.zip"):
    path = tmp_path / name
    path.write_bytes(data)
    return path


def test_the_bundled_extension_is_listed_as_installed(setup) -> None:
    assert setup.rows() == [("Gabi", "1.0.0", "Bundled", "Installed")]


def test_the_buttons_follow_the_selection(setup) -> None:
    form = setup.form
    assert not form.extensionsUninstallButton.isEnabled()
    assert not form.extensionsReinstallButton.isEnabled()

    setup.select("Gabi")  # bundled and installed: it can go, there is nothing to redo

    assert form.extensionsUninstallButton.isEnabled()
    assert not form.extensionsReinstallButton.isEnabled()


def test_a_zip_is_installed_after_the_person_agrees(setup, tmp_path) -> None:
    shown = setup.decide(True)
    setup.pick_file(zip_file(tmp_path, tool_zip()))

    setup.panel.install_from_file()

    assert shown[0].windowTitle() == "Install Tool?"
    assert ("Tool", "1.0.0", "file tool.zip", "Installed") in setup.rows()
    assert setup.messages == []


def test_a_zip_the_person_declines_is_not_installed(setup, tmp_path) -> None:
    setup.decide(False)
    setup.pick_file(zip_file(tmp_path, tool_zip()))

    setup.panel.install_from_file()

    assert [row[0] for row in setup.rows()] == ["Gabi"]
    assert list((tmp_path / "ext" / "staging").iterdir()) == []


def test_choosing_no_file_does_nothing(setup) -> None:
    setup.pick_file("")

    setup.panel.install_from_file()

    assert setup.messages == [] and len(setup.rows()) == 1


def test_a_file_that_cannot_be_read_is_reported(setup, tmp_path) -> None:
    setup.pick_file(tmp_path / "missing.zip")

    setup.panel.install_from_file()

    assert setup.messages[0].startswith("The file could not be read")


def test_something_that_is_not_an_extension_is_reported(setup, tmp_path) -> None:
    setup.pick_file(zip_file(tmp_path, b"not a zip"))

    setup.panel.install_from_file()

    assert setup.messages == ["It is not a zip file"]


def test_a_repository_is_downloaded_and_installed(setup, monkeypatch) -> None:
    setup.decide(True)
    setup.type_repository("dco/tool")
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())

    setup.panel.install_from_github()

    assert setup.downloads == [Repo("dco", "tool")]
    assert ("Tool", "1.0.0", "github dco/tool", "Installed") in setup.rows()


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
    setup.pick_file(zip_file(tmp_path, tool_zip()))

    def fail(candidate):
        raise StoreError("the disk is full")

    monkeypatch.setattr(setup.store, "install", fail)

    setup.panel.install_from_file()

    assert setup.messages == ["the disk is full"]


def test_uninstalling_the_bundled_extension_can_be_undone_by_reinstalling(
    setup,
) -> None:
    setup.select("Gabi")
    setup.confirm(True)

    setup.panel.uninstall()

    assert setup.rows() == [("Gabi", "1.0.0", "Bundled", "Uninstalled")]
    setup.select("Gabi")
    assert not setup.form.extensionsUninstallButton.isEnabled()
    assert setup.form.extensionsReinstallButton.isEnabled()

    setup.panel.reinstall()

    assert setup.rows() == [("Gabi", "1.0.0", "Bundled", "Installed")]


def test_uninstalling_asks_first_and_no_leaves_it(setup, tmp_path) -> None:
    setup.select("Gabi")
    setup.confirm(False)

    setup.panel.uninstall()

    assert setup.rows() == [("Gabi", "1.0.0", "Bundled", "Installed")]


def test_an_installed_extension_is_uninstalled_and_its_files_deleted(
    setup, tmp_path
) -> None:
    setup.decide(True)
    setup.pick_file(zip_file(tmp_path, tool_zip()))
    setup.panel.install_from_file()
    setup.select("Tool")
    setup.confirm(True)

    setup.panel.uninstall()

    assert [row[0] for row in setup.rows()] == ["Gabi"]
    assert not (tmp_path / "ext" / "installed" / "dco.tool").exists()


def test_uninstall_and_reinstall_without_a_selection_do_nothing(setup) -> None:
    setup.confirm(True)

    setup.panel.uninstall()
    setup.panel.reinstall()

    assert setup.rows() == [("Gabi", "1.0.0", "Bundled", "Installed")]


def test_a_store_that_refuses_is_reported(setup, monkeypatch) -> None:
    setup.select("Gabi")
    setup.confirm(True)

    def refuse(extension):
        raise StoreError("nope")

    monkeypatch.setattr(setup.store, "uninstall", refuse)
    monkeypatch.setattr(setup.store, "restore_bundled", refuse)
    setup.panel.uninstall()
    setup.panel.rows = [extensions_panel.Row("dco.gabi", "Gabi", "1", "bundled", False)]
    setup.table.selectRow(0)
    setup.panel.reinstall()

    assert setup.messages == ["nope", "nope"]


def test_a_repository_extension_is_downloaded_again_on_reinstall(
    setup, monkeypatch
) -> None:
    setup.decide(True)
    setup.type_repository("https://github.com/dco/tool/tree/v1")
    monkeypatch.setattr(extensions_panel, "download", lambda repo: tool_zip())
    setup.panel.install_from_github()
    setup.downloads.clear()
    setup.select("Tool")

    setup.panel.reinstall()

    assert setup.downloads == [Repo("dco", "tool", "v1")]


def test_a_zip_extension_asks_for_the_file_again_on_reinstall(setup, tmp_path) -> None:
    setup.decide(True)
    setup.pick_file(zip_file(tmp_path, tool_zip()))
    setup.panel.install_from_file()
    setup.select("Tool")
    setup.pick_file(zip_file(tmp_path, tool_zip(version="1.1.0"), "new.zip"))

    setup.panel.reinstall()

    assert ("Tool", "1.1.0", "file new.zip", "Installed") in setup.rows()


def test_a_remembered_source_that_is_not_a_repository_is_reported(setup) -> None:
    setup.panel.rows = [
        extensions_panel.Row("dco.tool", "Tool", "1", "github ../x", True)
    ]
    setup.table.setRowCount(1)
    setup.table.setItem(0, 0, extensions_panel.QTableWidgetItem("Tool"))
    setup.table.selectRow(0)

    setup.panel.reinstall()

    assert "owner/name" in setup.messages[0]


def test_a_source_that_is_neither_does_nothing_on_reinstall(setup) -> None:
    setup.panel.rows = [extensions_panel.Row("dco.tool", "Tool", "1", "other", True)]
    setup.table.setRowCount(1)
    setup.table.setItem(0, 0, extensions_panel.QTableWidgetItem("Tool"))
    setup.table.selectRow(0)

    setup.panel.reinstall()

    assert setup.downloads == [] and setup.messages == []


def test_the_selection_survives_a_refresh(setup) -> None:
    setup.select("Gabi")

    setup.panel.refresh()

    assert setup.panel._selected() is not None
