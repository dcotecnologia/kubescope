"""Color Pod logs with the palette of the JSON view, which follows the theme.

It colors the timestamp the cluster puts first on each line, the log
level, the keys of `key=value` lines and a JSON object (or a Python dict
with single quotes) written in the line. The text is never changed.
"""

import re

from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtWidgets import QPlainTextEdit

from kubescope.json_view import (
    Palette,
    current_palette,
    stylesheet,
    text_format,
)

_LEVELS = {
    "error": "error",
    "err": "error",
    "fatal": "error",
    "panic": "error",
    "critical": "error",
    "warn": "warning",
    "warning": "warning",
    "info": "info",
    "debug": "debug",
    "trace": "debug",
}
_NAMES = "|".join(sorted(_LEVELS, key=len, reverse=True))
_TIMESTAMP = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+(?:Z|[+-]\d\d:\d\d)?")
_KEY = re.compile(r"(?<![\w\"])[A-Za-z_][\w.-]*(?==)")
_QUOTED = re.compile(r'"(?:\\.|[^"\\])*"')
# an upper case word, a [bracketed] one, or the value of level=... or "level":"..."
_LEVEL = re.compile(
    rf"\b(?:{_NAMES.upper()})\b"
    rf"|(?<=\[)(?i:{_NAMES})(?=\])"
    rf"|(?<=level=)(?i:{_NAMES})\b"
    rf"|(?<=\"level\":\")(?i:{_NAMES})(?=\")"
)
# a JSON object starts at a brace followed by a quoted key; it may use ' like a
# Python dict does
_OBJECT = re.compile(r"\{\s*[\"']")
_JSON_STRING = r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'"
_JSON_KEY = re.compile(rf"(?:{_JSON_STRING})(?=\s*:)")
_JSON_TEXT = re.compile(_JSON_STRING)
_JSON_NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b")
_JSON_LITERAL = re.compile(r"\b(?:true|false|null|True|False|None)\b")
_JSON_PUNCTUATION = re.compile(r"[{}\[\],:]")


class LogHighlighter(QSyntaxHighlighter):
    """Colors one log line at a time; later rules win."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.set_palette(current_palette())

    def set_palette(self, palette: Palette) -> None:
        self._key = text_format(palette.key)
        self._quoted = text_format(palette.string)
        self._timestamp = text_format(palette.timestamp)
        self._number = text_format(palette.number)
        self._levels = {
            name: text_format(getattr(palette, name))
            for name in ("error", "warning", "info", "debug")
        }
        self.rehighlight()

    def highlightBlock(self, text: str) -> None:
        for match in _KEY.finditer(text):
            self.setFormat(match.start(), match.end() - match.start(), self._key)
        for match in _QUOTED.finditer(text):
            self.setFormat(match.start(), match.end() - match.start(), self._quoted)
        self._color_object(text)
        for match in _LEVEL.finditer(text):
            level = self._levels[_LEVELS[match.group().lower()]]
            self.setFormat(match.start(), match.end() - match.start(), level)
        stamp = _TIMESTAMP.match(text)
        if stamp:
            self.setFormat(0, stamp.end(), self._timestamp)

    def _color_object(self, text: str) -> None:
        """Color the JSON object of the line, from its first brace to its last
        one (or the end of the line when it is cut short)."""
        start = _OBJECT.search(text)
        if start is None:
            return
        end = text.rfind("}") + 1
        begin = start.start()
        body = text[begin : end if end > begin else len(text)]
        for pattern, fmt in (
            (_JSON_NUMBER, self._number),
            (_JSON_LITERAL, self._number),
            (_JSON_PUNCTUATION, self._timestamp),
            (_JSON_TEXT, self._quoted),
            (_JSON_KEY, self._key),
        ):
            for match in pattern.finditer(body):
                self.setFormat(begin + match.start(), match.end() - match.start(), fmt)


def style_log_view(editor: QPlainTextEdit) -> LogHighlighter:
    """Give a log editor the colors of the theme; keep the returned highlighter
    alive as long as the editor."""
    editor.setStyleSheet(stylesheet(current_palette()))
    return LogHighlighter(editor.document())
