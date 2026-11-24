"""Every text of every language is translated: an empty one would show the
person nothing, or English in the middle of another language."""

import json
from pathlib import Path

import pytest

LANGUAGES = Path(__file__).resolve().parents[1] / "src" / "kubescope" / "languages"
FILES = sorted(LANGUAGES.glob("*.json"))


def empty_texts(node: object, path: str = "") -> list[str]:
    """The path of every text that is left empty."""
    if isinstance(node, dict):
        return [
            found
            for key, value in node.items()
            for found in empty_texts(value, f"{path}/{key}")
        ]
    if isinstance(node, str) and not node.strip():
        return [path]
    return []


def test_there_are_languages_to_check() -> None:
    assert FILES


@pytest.mark.parametrize("file", FILES, ids=lambda file: file.stem)
def test_no_text_is_left_untranslated(file: Path) -> None:
    document = json.loads(file.read_text(encoding="utf-8"))
    assert empty_texts(document.get("strings", {})) == []
