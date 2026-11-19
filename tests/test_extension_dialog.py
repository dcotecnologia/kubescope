import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path

from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

from kubescope.dialogs.extension_dialog import InstallExtensionDialog
from kubescope.extensions.manifest import Manifest
from kubescope.extensions.store import Candidate

application = QApplication.instance() or QApplication([])
PARENT = QWidget()  # the dialog is deleted with its parent, so it must outlive them


def candidate(
    permissions=("cluster.read", "ui.dock"),
    description="",
    author="",
    replaces: Manifest | None = None,
    changed: bool = False,
    dev: bool = False,
) -> Candidate:
    return Candidate(
        manifest=Manifest(
            "dco.tool",
            "Tool",
            "1.2.0",
            "tool:go",
            frozenset(permissions),
            description,
            author,
        ),
        source="github dco/tool@v1",
        sha256="ab" * 32,
        folder=Path("staged"),
        replaces=replaces,
        content_changed=changed,
        dev=dev,
    )


def texts(dialog: InstallExtensionDialog) -> str:
    return "\n".join(label.text() for label in dialog.findChildren(QLabel))


def test_it_says_where_the_extension_came_from_and_what_it_asks() -> None:
    dialog = InstallExtensionDialog(PARENT, candidate())

    text = texts(dialog)
    assert dialog.windowTitle() == "Install Tool?"
    assert "1.2.0" in text and "github dco/tool@v1" in text
    assert "ab" * 32 in text
    assert "• read your clusters (cluster.read)" in text
    assert "• add a panel to the window (ui.dock)" in text
    assert "runs with your permissions" in text


def test_the_description_and_the_author_show_when_there_are() -> None:
    plain = texts(InstallExtensionDialog(PARENT, candidate()))
    full = texts(
        InstallExtensionDialog(
            PARENT, candidate(description="Does things", author="DCO")
        )
    )

    assert "Does things" not in plain and "DCO" not in plain
    assert "Does things" in full and "DCO" in full


def test_an_extension_that_asks_for_nothing_says_so() -> None:
    assert "none" in texts(InstallExtensionDialog(PARENT, candidate(permissions=())))


def test_a_replacement_says_which_version_and_whether_the_content_differs() -> None:
    older = Manifest("dco.tool", "Tool", "1.0.0", "tool:go", frozenset())

    same = texts(InstallExtensionDialog(PARENT, candidate(replaces=older)))
    different = texts(
        InstallExtensionDialog(PARENT, candidate(replaces=older, changed=True))
    )

    assert "It replaces the version 1.0.0." in same
    assert "different" not in same
    assert "Its content is different from the one you installed." in different


def test_cancel_is_the_default_and_install_accepts() -> None:
    dialog = InstallExtensionDialog(PARENT, candidate())
    buttons = {b.text(): b for b in dialog.findChildren(QPushButton)}

    assert buttons["Cancel"].isDefault() and not buttons["Install"].isDefault()
    buttons["Install"].click()
    assert dialog.result() == dialog.DialogCode.Accepted


def test_development_mode_says_it_runs_from_the_folder_and_has_no_hash() -> None:
    dialog = InstallExtensionDialog(PARENT, candidate(dev=True))

    text = texts(dialog)
    assert "Development mode: it runs from this folder" in text
    assert "SHA-256" not in text
    assert "SHA-256" in texts(InstallExtensionDialog(PARENT, candidate()))


def test_every_permission_the_sdk_knows_is_explained_to_the_person() -> None:
    from kubescope_sdk import PERMISSIONS

    dialog = InstallExtensionDialog(PARENT, candidate(permissions=PERMISSIONS))

    for name in PERMISSIONS:
        assert f"({name})" in texts(dialog)
