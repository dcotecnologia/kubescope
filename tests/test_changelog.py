import pytest
from PySide6.QtWidgets import QDialog, QPushButton

from kubescope.dialogs import changelog_dialog
from kubescope.dialogs.changelog_dialog import ChangelogDialog, changelog_html
from kubescope.utils import changelog
from tests.test_window_flows import _ready_window
from tools import sync_changelog


def test_the_packaged_copy_matches_the_changelog_of_the_repository(
    monkeypatch,
) -> None:
    monkeypatch.setattr("sys.argv", ["sync_changelog.py", "--check"])

    assert sync_changelog.main() == 0, "run `make changelog` after editing CHANGELOG.md"


def test_the_check_fails_when_the_copy_is_missing_or_old(
    monkeypatch, tmp_path, capsys
) -> None:
    source = tmp_path / "CHANGELOG.md"
    source.write_text("# Changelog\n", encoding="utf-8")
    copy = tmp_path / "copy.md"
    monkeypatch.setattr(sync_changelog, "SOURCE", source)
    monkeypatch.setattr(sync_changelog, "OUTPUT", copy)
    monkeypatch.setattr("sys.argv", ["sync_changelog.py", "--check"])
    assert sync_changelog.main() == 1  # no copy yet
    assert "out of date" in capsys.readouterr().out  # and it says what to do

    monkeypatch.setattr("sys.argv", ["sync_changelog.py"])
    assert sync_changelog.main() == 0  # writes it
    assert copy.read_text(encoding="utf-8") == "# Changelog\n"

    source.write_text("# Changelog\n\nmore\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["sync_changelog.py", "--check"])
    assert sync_changelog.main() == 1  # old
    assert "out of date" in capsys.readouterr().out


def test_the_changelog_is_read_from_the_package_or_missing(
    monkeypatch, tmp_path
) -> None:
    assert changelog.read_changelog().startswith("# Changelog")

    monkeypatch.setattr(changelog, "CHANGELOG", tmp_path / "nothing.md")
    assert changelog.read_changelog() is None


def test_the_dialog_shows_the_changelog_and_opens_the_releases(monkeypatch) -> None:
    opened = []
    monkeypatch.setattr(
        changelog_dialog.QDesktopServices, "openUrl", lambda url: opened.append(url)
    )
    monkeypatch.setattr(
        changelog_dialog, "read_changelog", lambda: "# Changelog\n\n- x"
    )

    dialog = ChangelogDialog(None)
    buttons = {b.text(): b for b in dialog.findChildren(QPushButton)}
    buttons["Open the releases on GitHub"].click()

    assert "Changelog" in dialog.text.toPlainText()
    assert opened[0].toString().endswith("/releases")
    assert dialog.text.openExternalLinks()
    buttons["Close"].click()
    assert dialog.result() == QDialog.DialogCode.Accepted


def test_the_dialog_says_when_the_changelog_is_not_there(monkeypatch) -> None:
    monkeypatch.setattr(changelog_dialog, "read_changelog", lambda: None)

    dialog = ChangelogDialog(None)

    assert "not available" in dialog.text.toPlainText()


def test_the_version_in_the_footer_opens_the_changelog(monkeypatch) -> None:
    window = _ready_window(monkeypatch)
    shown = []
    monkeypatch.setattr(QDialog, "exec", lambda dialog: shown.append(dialog) or 0)

    window.ui.footerVersion.click()

    assert len(shown) == 1 and isinstance(shown[0], ChangelogDialog)
    window.close()


SAMPLE = """# Changelog

An introduction that is left out.

## [Unreleased]

### Added

- A **bold** thing with `code` and a [link](https://example.test/x) by @someone
- A wrapped item
  that goes on here <b>escaped</b>

### Fixed

- A fix

## [0.1.0] - 2026-01-02

### Added

- First

[Unreleased]: https://example.test/compare
"""


def test_parse_changelog_reads_versions_sections_and_wrapped_items() -> None:
    versions = changelog.parse_changelog(SAMPLE)

    assert [(v.name, v.date) for v in versions] == [
        ("Unreleased", ""),
        ("0.1.0", "2026-01-02"),
    ]
    added, fixed = versions[0].sections
    assert added[0] == "Added" and len(added[1]) == 2
    assert added[1][1] == "A wrapped item that goes on here <b>escaped</b>"
    assert fixed == ("Fixed", ["A fix"])
    assert versions[1].sections == [("Added", ["First"])]
    assert changelog.parse_changelog("no versions here") == []
    assert changelog.parse_changelog("- a stray item\n### Added\n") == []


def test_the_real_changelog_parses_into_versions() -> None:
    versions = changelog.parse_changelog(changelog.read_changelog())

    assert versions[0].name == "Unreleased"
    assert any(v.name == "0.6.2" for v in versions)
    assert all(items for v in versions for _title, items in v.sections)


def test_inline_markdown_becomes_rich_text_and_the_rest_is_escaped() -> None:
    result = changelog.inline_html(
        "A **bold** `code` [link](https://x.test/a) <b>raw</b> by @me", "#999", "#00f"
    )

    assert "<b>bold</b>" in result
    assert 'font-family: monospace; color: #00f;">code</span>' in result
    assert '<a href="https://x.test/a">link</a>' in result
    assert "&lt;b&gt;raw&lt;/b&gt;" in result
    assert result.endswith('<span style="color: #999;">by @me</span>')
    assert "<a" not in changelog.inline_html("[x](javascript:alert(1))", "", "")


def test_the_changelog_is_laid_out_with_a_heading_per_version() -> None:
    result = changelog_html(changelog.parse_changelog(SAMPLE), current="0.1.0")

    assert result.count("<table") == 2 and "2026-01-02" in result
    assert result.count("INSTALLED") == 1  # only on the version in use
    assert result.count("<hr") == 2
    assert "ADDED" in result and "FIXED" in result
    assert result.count("<li") == 4
    assert changelog_html([changelog.Version("1.0.0", "", [("Other", ["x"])])])


def test_what_is_not_released_yet_is_left_out_of_the_dialog(monkeypatch) -> None:
    monkeypatch.setattr(changelog_dialog, "read_changelog", lambda: SAMPLE)

    dialog = ChangelogDialog(None)
    shown = dialog.text.toPlainText()

    assert "Unreleased" not in shown and "A fix" not in shown
    assert "0.1.0" in shown and "First" in shown


def test_a_changelog_in_another_format_is_shown_as_it_is(monkeypatch) -> None:
    monkeypatch.setattr(
        changelog_dialog, "read_changelog", lambda: "# Just notes\n\ntext"
    )

    dialog = ChangelogDialog(None)

    assert "Just notes" in dialog.text.toPlainText()


def test_a_bundle_with_an_old_changelog_is_refused(monkeypatch, tmp_path) -> None:
    source = tmp_path / "CHANGELOG.md"
    source.write_text("new\n", encoding="utf-8")
    monkeypatch.setattr(sync_changelog, "SOURCE", source)
    bundle = tmp_path / "bundle"
    shipped = bundle / "_internal" / "kubescope" / "assets" / "CHANGELOG.md"

    with pytest.raises(SystemExit, match="old changelog"):
        sync_changelog.check_bundle(bundle)  # no copy in the bundle

    shipped.parent.mkdir(parents=True)
    shipped.write_text("old\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="old changelog"):
        sync_changelog.check_bundle(bundle)

    shipped.write_text("new\n", encoding="utf-8")
    sync_changelog.check_bundle(bundle)  # current: fine
