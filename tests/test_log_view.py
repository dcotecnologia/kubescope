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

    assert colors["2026-10-08T05:00:01.123Z"] == "#75715e"
    assert colors["ERROR"] == "#f92672"
    assert "connection" not in colors  # the message keeps the plain color


def test_every_level_has_its_color(dark) -> None:
    expected = {
        "FATAL": "#f92672",
        "WARN": "#fd971f",
        "WARNING": "#fd971f",
        "INFO": "#a6e22e",
        "DEBUG": "#ae81ff",
        "TRACE": "#ae81ff",
    }
    for level, color in expected.items():
        assert _colors(f"2026-10-08T05:00:01Z {level} x")[level] == color


def test_levels_in_brackets_and_in_key_value_lines_are_found(dark) -> None:
    assert _colors("[warn] disk almost full")["warn"] == "#fd971f"
    assert _colors("ts=1 level=info msg=started")["info"] == "#a6e22e"
    assert _colors('{"level":"error","msg":"x"}')["error"] == "#f92672"


def test_ordinary_words_are_not_taken_for_levels() -> None:
    colors = _colors("2026-10-08T05:00:01Z more info about the error rate")

    assert "info" not in colors and "error" not in colors


def test_keys_and_quoted_text_are_colored(dark) -> None:
    colors = _colors('ts=1 user=bob msg="a b" path=/x')

    assert colors["user"] == "#66d9ef" and colors["msg"] == "#66d9ef"
    assert colors['"a b"'] == "#e6db74"
    assert "bob" not in colors


def test_a_timestamp_with_an_offset_is_colored_too(dark) -> None:
    assert _colors("2026-10-08T05:00:01+02:00 hi")["2026-10-08T05:00:01+02:00"] == (
        "#75715e"
    )


def test_light_themes_color_the_logs_with_the_light_palette() -> None:
    colors = _colors('2026-10-08T05:00:01Z ERROR ts=1 msg="x"')

    assert colors["ERROR"] == "#cf222e"
    assert colors["2026-10-08T05:00:01Z"] == "#6e7781"
    assert colors["ts"] == "#0550ae" and colors['"x"'] == "#116329"


def test_a_json_object_in_a_line_gets_its_own_colors(dark) -> None:
    colors = _colors(
        '2026-10-08T05:00:01Z req {"id": 7, "ok": true, "tag": "a b"} done'
    )

    assert colors['"id"'] == "#66d9ef"  # keys
    assert colors['"a b"'] == "#e6db74"  # strings
    assert colors["7"] == "#ae81ff" and colors["true"] == "#ae81ff"
    assert colors["{"] == "#75715e"  # punctuation is dimmed
    assert "done" not in colors and "req" not in colors  # the rest is plain


def test_a_python_dict_and_a_cut_object_are_colored_too(dark) -> None:
    colors = _colors("{'sub': 'x', 'n': -1.5, 'v': None, 'k': 'cut")

    assert colors["'sub'"] == "#66d9ef" and colors["'x'"] == "#e6db74"
    assert colors["-1.5"] == "#ae81ff" and colors["None"] == "#ae81ff"


def test_braces_without_a_key_are_not_an_object(dark) -> None:
    assert "{" not in _colors("rendered {} and {name} 42")
