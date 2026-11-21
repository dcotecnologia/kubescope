from PySide6.QtCore import QUrl

from kubescope.dialogs import notices_dialog
from kubescope.dialogs.notices_dialog import NoticesDialog
from kubescope.utils import notices
from tests.qt import get_application

application = get_application()

RULE = "=" * 78
SAMPLE = (
    f"Notices\n{RULE}\n\nWhat is used.\n\n"
    f"{RULE}\nalpha 1.0\n{RULE}\n\nAlpha license.\n\n"
    f"{RULE}\nBeta and Gamma\n{RULE}\n\nBeta license.\n"
)


def test_the_notices_are_split_into_the_overview_and_one_text_for_each() -> None:
    found = notices.parse_notices(SAMPLE)

    assert [one.title for one in found] == ["Notices", "alpha 1.0", "Beta and Gamma"]
    assert found[0].text.endswith("What is used.")
    assert found[1].text == "Alpha license."
    assert found[2].text == "Beta license."
    assert notices.parse_notices("") == []
    assert [one.title for one in notices.parse_notices("only text")] == ["only text"]


def test_the_notices_the_package_carries_are_read_in_full() -> None:
    text = notices.read_notices()
    assert text is not None

    titles = [one.title for one in notices.parse_notices(text)]

    assert titles[0] == "KubeScope - third-party notices"
    assert any(title.startswith("Qt and Qt for Python") for title in titles)
    assert any(title.startswith("certifi ") for title in titles)
    assert all(one.text for one in notices.parse_notices(text))


def test_an_installation_without_the_notices_says_so(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(notices, "NOTICES", tmp_path / "missing.txt")
    monkeypatch.setattr(notices_dialog, "read_notices", notices.read_notices)

    assert notices.read_notices() is None
    dialog = NoticesDialog(None)

    assert "not available" in dialog.text.toPlainText()
    assert dialog.entries.count() == 0


def test_the_dialog_lists_the_components_and_shows_the_text_of_the_one_chosen(
    monkeypatch,
) -> None:
    monkeypatch.setattr(notices_dialog, "read_notices", lambda: SAMPLE)
    dialog = NoticesDialog(None)

    assert [dialog.entries.item(row).text() for row in range(3)] == [
        "Notices",
        "alpha 1.0",
        "Beta and Gamma",
    ]
    assert dialog.text.toPlainText().endswith("What is used.")  # the first one

    dialog.entries.setCurrentRow(2)
    assert dialog.text.toPlainText() == "Beta license."
    assert dialog.text.isReadOnly()


def test_the_filter_keeps_the_components_with_the_words_and_picks_one(
    monkeypatch,
) -> None:
    monkeypatch.setattr(notices_dialog, "read_notices", lambda: SAMPLE)
    dialog = NoticesDialog(None)

    dialog.filter.setText("gamma beta")  # every word, in any case
    assert [dialog.entries.item(row).isHidden() for row in range(3)] == [
        True,
        True,
        False,
    ]
    assert dialog.text.toPlainText() == "Beta license."

    dialog.filter.setText("alpha")
    assert dialog.text.toPlainText() == "Alpha license."

    dialog.filter.setText("nothing like this")  # no one is left: the text stays
    assert all(dialog.entries.item(row).isHidden() for row in range(3))
    assert dialog.text.toPlainText() == "Alpha license."

    dialog.filter.setText("")
    assert not any(dialog.entries.item(row).isHidden() for row in range(3))


def test_the_dialog_opens_the_file_for_who_wants_it(monkeypatch) -> None:
    opened = []
    monkeypatch.setattr(
        notices_dialog.QDesktopServices, "openUrl", lambda url: opened.append(url)
    )
    dialog = NoticesDialog(None)

    button = next(
        child
        for child in dialog.findChildren(notices_dialog.QPushButton)
        if child.text() == "Open the file"
    )
    button.click()

    assert opened == [QUrl.fromLocalFile(str(notices.NOTICES))]
