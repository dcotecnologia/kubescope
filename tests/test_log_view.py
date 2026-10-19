import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPlainTextEdit

from kubescope import theme
from kubescope.utils import log_view

application = QApplication.instance() or QApplication([])


@pytest.fixture
def dark():
    theme.set_theme("dark")  # the autouse fixture puts light back after


def _colors(text: str) -> dict[str, str]:
    """The color of each highlighted piece of the first line, by its text."""
    editor = QPlainTextEdit()
    log_view.style_log_view(editor)
    editor.setPlainText(text)
    block = editor.document().firstBlock()
    return {
        block.text()[item.start : item.start + item.length]: item.format.foreground()
        .color()
        .name()
        for item in block.layout().formats()
    }


def test_the_timestamp_and_the_level_get_their_colors(dark) -> None:
    colors = _colors("2026-10-08T05:00:01.123Z ERROR connection lost")

    assert colors["2026-10-08T05:00:01.123Z"] == "#6a9955"
    assert colors["ERROR"] == "#f48771"
    assert "connection" not in colors  # the message keeps the plain color


def test_every_level_has_its_color(dark) -> None:
    expected = {
        "FATAL": "#f48771",
        "WARN": "#cca700",
        "WARNING": "#cca700",
        "INFO": "#4ec9b0",
        "DEBUG": "#c586c0",
        "TRACE": "#c586c0",
    }
    for level, color in expected.items():
        assert _colors(f"2026-10-08T05:00:01Z {level} x")[level] == color


def test_levels_in_brackets_and_in_key_value_lines_are_found(dark) -> None:
    assert _colors("[warn] disk almost full")["warn"] == "#cca700"
    assert _colors("ts=1 level=info msg=started")["info"] == "#4ec9b0"
    assert _colors('{"level":"error","msg":"x"}')["error"] == "#f48771"


def test_ordinary_words_are_not_taken_for_levels() -> None:
    colors = _colors("2026-10-08T05:00:01Z more info about the error rate")

    assert "info" not in colors and "error" not in colors


def test_keys_and_quoted_text_are_colored(dark) -> None:
    colors = _colors('ts=1 user=bob msg="a b" path=/x')

    assert colors["user"] == "#9cdcfe" and colors["msg"] == "#9cdcfe"
    assert colors['"a b"'] == "#ce9178"
    assert "bob" not in colors


def test_a_timestamp_with_an_offset_is_colored_too(dark) -> None:
    assert _colors("2026-10-08T05:00:01+02:00 hi")["2026-10-08T05:00:01+02:00"] == (
        "#6a9955"
    )


def test_light_themes_color_the_logs_with_the_light_palette() -> None:
    colors = _colors('2026-10-08T05:00:01Z ERROR ts=1 msg="x"')

    assert colors["ERROR"] == "#cd3131"
    assert colors["2026-10-08T05:00:01Z"] == "#008000"
    assert colors["ts"] == "#0451a5" and colors['"x"'] == "#a31515"


def test_a_json_object_in_a_line_gets_its_own_colors(dark) -> None:
    colors = _colors(
        '2026-10-08T05:00:01Z req {"id": 7, "ok": true, "tag": "a b"} done'
    )

    assert colors['"id"'] == "#9cdcfe"  # keys
    assert colors['"a b"'] == "#ce9178"  # strings
    assert colors["7"] == "#b5cea8" and colors["true"] == "#569cd6"
    assert colors["{"] == "#6a9955"  # punctuation is dimmed
    assert "done" not in colors and "req" not in colors  # the rest is plain


def test_a_python_dict_and_a_cut_object_are_colored_too(dark) -> None:
    colors = _colors("{'sub': 'x', 'n': -1.5, 'v': None, 'k': 'cut")

    assert colors["'sub'"] == "#9cdcfe" and colors["'x'"] == "#ce9178"
    assert colors["-1.5"] == "#b5cea8" and colors["None"] == "#569cd6"


def test_braces_without_a_key_are_not_an_object(dark) -> None:
    assert "{" not in _colors("rendered {} and {name} 42")
