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
    assert _colors(editor, 1) == {'"name"': "#66d9ef", '"api"': "#e6db74"}
    assert _colors(editor, 2)["3"] == "#ae81ff"
    assert _colors(editor, 3)["-150.0"] == "#ae81ff"
    assert _colors(editor, 4)["false"] == "#ae81ff"
    assert _colors(editor, 0) == {}  # braces keep the plain text color


def test_a_number_or_word_inside_a_string_stays_a_string(dark) -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)
    editor.setPlainText('{"image": "nginx:1.25 null true", "a b": "x\\"2"}')

    colors = _colors(editor, 0)

    assert colors['"nginx:1.25 null true"'] == "#e6db74"
    assert colors['"a b"'] == "#66d9ef"
    assert colors['"x\\"2"'] == "#e6db74"


def test_the_view_has_the_monokai_background(dark) -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)

    assert "#272822" in editor.styleSheet() and "#f8f8f2" in editor.styleSheet()


def test_a_light_theme_gets_a_light_palette() -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)
    editor.setPlainText('{"name": "api", "replicas": 3}')

    assert not json_view.is_dark()
    assert _colors(editor, 0)['"name"'] == "#0550ae"
    assert _colors(editor, 0)['"api"'] == "#116329"
    assert _colors(editor, 0)["3"] == "#b35900"
    assert "#272822" not in editor.styleSheet()


def test_restyle_follows_a_theme_change(dark) -> None:
    editor = QPlainTextEdit()
    highlighter = json_view.style_json_view(editor)
    editor.setPlainText('{"name": 1}')
    assert _colors(editor, 0)['"name"'] == "#66d9ef"

    theme.set_theme("light")
    json_view.restyle(editor, highlighter)

    assert _colors(editor, 0)['"name"'] == "#0550ae"
    assert "#272822" not in editor.styleSheet()
