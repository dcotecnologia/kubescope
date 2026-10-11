import pytest

from tools import release_notes

CHANGELOG = """# Changelog

## [Unreleased]

## [0.2.0] - 2026-10-11

### Added

- Something new.

### Changed

- Something changed.

## [0.1.0] - 2026-10-01

The first release.

[Unreleased]: https://example.test/compare/v0.2.0...HEAD
[0.2.0]: https://example.test/compare/v0.1.0...v0.2.0
[0.1.0]: https://example.test/releases/tag/v0.1.0
"""


def test_the_notes_are_the_section_of_the_version() -> None:
    notes = release_notes.release_notes(CHANGELOG, "0.2.0")

    assert notes.startswith("### Added\n\n- Something new.")
    assert "- Something changed." in notes
    assert "first release" not in notes and "2026-10-11" not in notes
    assert notes.endswith(
        "**Full changelog**: https://example.test/compare/v0.1.0...v0.2.0\n"
    )


def test_the_oldest_section_ends_at_the_link_references() -> None:
    notes = release_notes.release_notes(CHANGELOG, "0.1.0")

    assert notes.startswith("The first release.")
    assert "[Unreleased]" not in notes
    assert notes.endswith(
        "**Full changelog**: https://example.test/releases/tag/v0.1.0\n"
    )


def test_a_section_at_the_end_of_the_file_and_without_a_link() -> None:
    notes = release_notes.release_notes(
        "## [1.0.0] - today\n\n- Only entry.\n", "1.0.0"
    )

    assert notes == "- Only entry.\n"


def test_a_version_without_a_section_is_an_error() -> None:
    with pytest.raises(ValueError, match="no section for 9.9.9"):
        release_notes.release_notes(CHANGELOG, "9.9.9")


def test_main_prints_the_notes_of_the_tag(monkeypatch, capsys) -> None:
    monkeypatch.setattr(release_notes.sys, "argv", ["release_notes.py", "v0.2.0"])

    assert release_notes.main() == 0

    assert "### Added" in capsys.readouterr().out


def test_main_explains_a_missing_section_or_missing_argument(monkeypatch) -> None:
    monkeypatch.setattr(release_notes.sys, "argv", ["release_notes.py", "v99.0.0"])
    with pytest.raises(SystemExit, match="no section for 99.0.0"):
        release_notes.main()

    monkeypatch.setattr(release_notes.sys, "argv", ["release_notes.py"])
    with pytest.raises(SystemExit, match="Usage"):
        release_notes.main()
