import json
import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit

from kubescope import theme
from kubescope.utils import json_view

application = QApplication.instance() or QApplication([])


@pytest.fixture
def dark():
    theme.set_theme("dark")  # the autouse fixture puts light back after


def _colors(editor: QPlainTextEdit, line: int) -> dict[str, str]:
    """The color of each highlighted piece of one line, by its text."""
    block = editor.document().findBlockByNumber(line)
    return {
        block.text()[item.start : item.start + item.length]: item.format.foreground()
        .color()
        .name()
        for item in block.layout().formats()
    }


def test_json_is_colored_like_monokai(dark) -> None:
    editor = QPlainTextEdit()
    highlighter = json_view.style_json_view(editor)
    document = {"name": "api", "replicas": 3, "ratio": -1.5e2, "paused": False}
    editor.setPlainText(json.dumps(document, indent=2))

    assert highlighter.document() is editor.document()
    assert _colors(editor, 1) == {'"name"': "#9cdcfe", '"api"': "#ce9178"}
    assert _colors(editor, 2)["3"] == "#b5cea8"
    assert _colors(editor, 3)["-150.0"] == "#b5cea8"
    assert _colors(editor, 4)["false"] == "#569cd6"
    assert _colors(editor, 0) == {}  # braces keep the plain text color


def test_a_number_or_word_inside_a_string_stays_a_string(dark) -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)
    editor.setPlainText('{"image": "nginx:1.25 null true", "a b": "x\\"2"}')

    colors = _colors(editor, 0)

    assert colors['"nginx:1.25 null true"'] == "#ce9178"
    assert colors['"a b"'] == "#9cdcfe"
    assert colors['"x\\"2"'] == "#ce9178"


def test_the_view_has_the_monokai_background(dark) -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)

    assert "#1e1e1e" in editor.styleSheet() and "#d4d4d4" in editor.styleSheet()


def test_a_light_theme_gets_a_light_palette() -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)
    editor.setPlainText('{"name": "api", "replicas": 3}')

    assert not json_view.is_dark()
    assert _colors(editor, 0)['"name"'] == "#0451a5"
    assert _colors(editor, 0)['"api"'] == "#a31515"
    assert _colors(editor, 0)["3"] == "#098658"
    assert "#1e1e1e" not in editor.styleSheet()


def test_restyle_follows_a_theme_change(dark) -> None:
    editor = QPlainTextEdit()
    highlighter = json_view.style_json_view(editor)
    editor.setPlainText('{"name": 1}')
    assert _colors(editor, 0)['"name"'] == "#9cdcfe"

    theme.set_theme("light")
    json_view.restyle(editor, highlighter)

    assert _colors(editor, 0)['"name"'] == "#0451a5"
    assert "#1e1e1e" not in editor.styleSheet()
