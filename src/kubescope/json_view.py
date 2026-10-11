"""Color JSON the way the Monokai editor theme does.

The view is dark in every app theme, like a code editor: Monokai is a
dark palette, so it does not follow the light and dark themes of the
window.
"""

import re

from PySide6.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import QPlainTextEdit

BACKGROUND = "#272822"
TEXT = "#f8f8f2"
SELECTION = "#49483e"
KEY = "#66d9ef"
STRING = "#e6db74"
NUMBER = "#ae81ff"
LITERAL = "#ae81ff"  # true, false and null

STYLE = (
    f"QPlainTextEdit {{ background: {BACKGROUND}; color: {TEXT};"
    f" border: 1px solid #3e3d32; border-radius: 5px; padding: 8px;"
    f" selection-background-color: {SELECTION}; selection-color: {TEXT}; }}"
)

_NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
_LITERAL = re.compile(r"\b(?:true|false|null)\b")
_STRING = re.compile(r'"(?:\\.|[^"\\])*"')
_KEY = re.compile(r'"(?:\\.|[^"\\])*"(?=\s*:)')


def _format(color: str) -> QTextCharFormat:
    text_format = QTextCharFormat()
    text_format.setForeground(QColor(color))
    return text_format


class JsonHighlighter(QSyntaxHighlighter):
    """Colors keys, strings, numbers and literals, one line at a time.

    Later rules win, so a number inside a string stays the color of the
    string.
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self._rules = [
            (_NUMBER, _format(NUMBER)),
            (_LITERAL, _format(LITERAL)),
            (_STRING, _format(STRING)),
            (_KEY, _format(KEY)),
        ]

    def highlightBlock(self, text: str) -> None:
        for pattern, text_format in self._rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), text_format)


def style_json_view(editor: QPlainTextEdit) -> JsonHighlighter:
    """Give a read-only editor the Monokai colors; keep the returned
    highlighter alive as long as the editor."""
    editor.setStyleSheet(STYLE)
    return JsonHighlighter(editor.document())
