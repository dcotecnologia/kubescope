import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel

from kubescope.dialogs.extension_details_dialog import (
    ExtensionDetails,
    ExtensionDetailsDialog,
)

application = QApplication.instance() or QApplication([])


def texts(details: ExtensionDetails) -> str:
    dialog = ExtensionDetailsDialog(None, details)
    return " | ".join(label.text() for label in dialog.findChildren(QLabel))


def test_everything_known_about_an_extension_is_shown() -> None:
    text = texts(
        ExtensionDetails(
            name="Gabi",
            id="kubescope.gabi",
            version="1.2.0",
            status="Installed",
            description="The assistant",
            author="DCO",
            source="github dco/gabi@v1.2.0",
            sha256="a" * 64,
            folder="/x/gabi",
            installed_at="2026-01-05",
            updated_at="2026-03-20",
            permissions=("cli", "cluster.read"),
            commands=("chat", "assistant"),
            newer="1.3.0",
            recommended=True,
        )
    )

    for wanted in (
        "kubescope.gabi", "v1.2.0", "Installed", "DCO", "github dco/gabi@v1.2.0",
        "/x/gabi", "2026-01-05", "2026-03-20", "a" * 64, "chat, assistant",
        "v1.3.0", "read your clusters", "add a command to kubescope",
        "KubeScope recommends it",
    ):  # fmt: skip
        assert wanted in text


def test_a_load_error_is_shown_and_an_unknown_one_has_no_permissions_yet() -> None:
    text = texts(
        ExtensionDetails(
            name="X",
            id="a.b",
            version="",
            status="Recommended",
            error="boom",
            known=False,
        )  # fmt: skip
    )

    assert "Could not load: boom" in text
    assert "They are shown when it is downloaded." in text
    assert "KubeScope recommends it" not in text


def test_the_repository_is_a_link_that_opens_outside_the_app() -> None:
    details = ExtensionDetails(
        name="AWS",
        id="kubescope.aws",
        version="1.3.0",
        status="Installed",
        repository="https://github.com/dcotecnologia/kubescope-aws",
    )
    dialog = ExtensionDetailsDialog(None, details)
    links = [one for one in dialog.findChildren(QLabel) if one.openExternalLinks()]
    assert len(links) == 1
    assert 'href="https://github.com/dcotecnologia/kubescope-aws"' in links[0].text()
    assert "Repository" in texts(details)
    assert "Repository" not in texts(
        ExtensionDetails(name="A", id="a.b", version="1", status="Installed")
    )
