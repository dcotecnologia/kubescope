"""Color JSON, and the logs next to it, to match the theme in use.

The dark themes get the palette of VS Code's Dark+; the light ones the
of Light+. A palette is picked when a view is made and again when the
theme changes.
"""

import re
from dataclasses import dataclass

from PySide6.QtGui import QColor, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import QPlainTextEdit

from kubescope.theme import WHITE, themed


@dataclass(frozen=True)
class Palette:
    background: str
    text: str
    selection: str
    border: str
    key: str
    string: str
    number: str
    literal: str  # true, false and null
    timestamp: str  # for logs: what is not the message
    error: str
    warning: str
    info: str
    debug: str


DARK_PLUS = Palette(
    background="#1e1e1e",
    text="#d4d4d4",
    selection="#264f78",
    border="#3c3c3c",
    key="#9cdcfe",
    string="#ce9178",
    number="#b5cea8",
    literal="#569cd6",
    timestamp="#6a9955",
    error="#f48771",
    warning="#cca700",
    info="#4ec9b0",
    debug="#c586c0",
)


def is_dark() -> bool:
    """Whether the theme in use has a dark surface."""
    return QColor(themed(WHITE)).lightness() < 128


def current_palette() -> Palette:
    if is_dark():
        return DARK_PLUS
    return Palette(
        background=themed(WHITE),
        text=themed("#242a33"),
        selection=themed("#d9d3f2"),
        border=themed("#dfe2e9"),
        key="#0451a5",
        string="#a31515",
        number="#098658",
        literal="#0000ff",
        timestamp="#008000",
        error="#cd3131",
        warning="#bf8803",
        info="#267f99",
        debug="#af00db",
    )


def stylesheet(palette: Palette) -> str:
    return (
        f"QPlainTextEdit {{ background: {palette.background}; color: {palette.text};"
        f" border: 1px solid {palette.border}; border-radius: 5px; padding: 8px;"
        f" selection-background-color: {palette.selection};"
        f" selection-color: {palette.text}; }}"
    )


_NUMBER = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
_LITERAL = re.compile(r"\b(?:true|false|null)\b")
_STRING = re.compile(r'"(?:\\.|[^"\\])*"')
_KEY = re.compile(r'"(?:\\.|[^"\\])*"(?=\s*:)')


def text_format(color: str) -> QTextCharFormat:
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
        self.set_palette(current_palette())

    def set_palette(self, palette: Palette) -> None:
        number, literal, string, key = (
            text_format(palette.number),
            text_format(palette.literal),
            text_format(palette.string),
            text_format(palette.key),
        )
        self._rules = [
            (_NUMBER, number),
            (_LITERAL, literal),
            (_STRING, string),
            (_KEY, key),
        ]
        self.rehighlight()

    def highlightBlock(self, text: str) -> None:
        for pattern, fmt in self._rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)


def style_json_view(editor: QPlainTextEdit) -> JsonHighlighter:
    """Give a read-only editor the colors of the theme; keep the returned
    highlighter alive as long as the editor."""
    editor.setStyleSheet(stylesheet(current_palette()))
    return JsonHighlighter(editor.document())


def restyle(editor: QPlainTextEdit, highlighter: QSyntaxHighlighter) -> None:
    """Redo the colors of a view after the theme changed."""
    palette = current_palette()
    editor.setStyleSheet(stylesheet(palette))
    highlighter.set_palette(palette)
