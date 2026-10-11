import json
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit

from kubescope import json_view

application = QApplication.instance() or QApplication([])


def _colors(editor: QPlainTextEdit, line: int) -> dict[str, str]:
    """The color of each highlighted piece of one line, by its text."""
    block = editor.document().findBlockByNumber(line)
    return {
        block.text()[item.start : item.start + item.length]: item.format.foreground()
        .color()
        .name()
        for item in block.layout().formats()
    }


def test_json_is_colored_like_monokai() -> None:
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


def test_a_number_or_word_inside_a_string_stays_a_string() -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)
    editor.setPlainText('{"image": "nginx:1.25 null true", "a b": "x\\"2"}')

    colors = _colors(editor, 0)

    assert colors['"nginx:1.25 null true"'] == "#e6db74"
    assert colors['"a b"'] == "#66d9ef"
    assert colors['"x\\"2"'] == "#e6db74"


def test_the_view_has_the_monokai_background() -> None:
    editor = QPlainTextEdit()
    json_view.style_json_view(editor)

    assert "#272822" in editor.styleSheet() and "#f8f8f2" in editor.styleSheet()
