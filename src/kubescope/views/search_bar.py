"""A search bar for a read-only text view, with the match case (Aa) and regular
expression (.*) switches: it marks every match, selects the current one and
moves between them."""

import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QKeyEvent, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QTextEdit,
    QWidget,
)

HEIGHT = 38  # like the search box of the lists
MAX_MARKED = 2000  # the matches painted at once; all of them are still counted


def _units(text: str) -> int:
    """The length of the text in UTF-16 units, which the document counts in."""
    return len(text.encode("utf-16-le")) // 2


def compile_query(query: str, match_case: bool, regex: bool) -> re.Pattern[str] | None:
    """The pattern of a search, None for an empty one.

    Raises `re.error` for a regular expression that does not compile.
    """
    if not query:
        return None
    return re.compile(query if regex else re.escape(query), 0 if match_case else re.I)


def switch_button(text: str, tip: str) -> QPushButton:
    """The Aa and .* switches of a search box."""
    button = QPushButton(text)
    button.setCheckable(True)
    button.setToolTip(tip)
    button.setFixedSize(38, HEIGHT)
    button.setProperty("variant", "secondary")
    return button


def find_spans(
    text: str, query: str, match_case: bool, regex: bool
) -> list[tuple[int, int]]:
    """The (start, end) of each non-empty match of the query, in order.

    Raises `re.error` for a regular expression that does not compile.
    """
    pattern = compile_query(query, match_case, regex)
    if pattern is None:
        return []
    return [
        match.span() for match in pattern.finditer(text) if match.end() > match.start()
    ]


def _document_offsets(text: str, spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """The spans in the document's own positions: they differ from the string's
    only after a character outside the Basic Multilingual Plane."""
    if text.isascii():
        return spans
    offsets = []
    index = unit = 0
    for start, end in spans:
        unit += _units(text[index:start])
        first = unit
        unit += _units(text[start:end])
        index = end
        offsets.append((first, unit))
    return offsets


class _SearchInput(QLineEdit):
    """The search box: Escape in it asks the bar to clear the search."""

    escaped = Signal()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.escaped.emit()
            return
        super().keyPressEvent(event)


class SearchBar(QWidget):
    """Searches the text of `editor`; keep the editor's text and this bar in
    step by calling `refresh` after the text changes."""

    edited = Signal()  # the person changed what to look for

    def __init__(self, editor: QPlainTextEdit) -> None:
        super().__init__()
        self.editor = editor
        self._spans: list[tuple[int, int]] = []
        self._current = -1
        self._format = QTextCharFormat()
        self._format.setBackground(QColor(255, 200, 0, 90))

        self.input = _SearchInput()
        self.input.setPlaceholderText(self.tr("Search"))
        self.input.setClearButtonEnabled(True)
        self.input.setProperty("variant", "filter")
        self.input.setFixedHeight(HEIGHT)
        self.input.setMinimumWidth(200)
        self.case_button = switch_button("Aa", self.tr("Match case"))
        self.regex_button = switch_button(".*", self.tr("Regular expression"))
        self.count_label = QLabel()
        self.count_label.setProperty("variant", "muted")
        self.count_label.setMinimumWidth(96)  # "12 of 345" without being cut
        self.previous_button = self._step("↑", self.tr("Previous match"))
        self.next_button = self._step("↓", self.tr("Next match"))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(self.input, 1)
        for widget in (
            self.case_button,
            self.regex_button,
            self.previous_button,
            self.next_button,
            self.count_label,
        ):
            layout.addWidget(widget)

        self.input.textChanged.connect(self._edited)
        self.input.returnPressed.connect(self._enter)
        self.case_button.toggled.connect(self._edited)
        self.regex_button.toggled.connect(self._edited)
        self.input.escaped.connect(self._escape)
        # bound methods, not lambdas: a lambda keeps the bar alive until the app ends
        self.previous_button.clicked.connect(self._previous)
        self.next_button.clicked.connect(self._next)

    def _step(self, text: str, tip: str) -> QPushButton:
        button = QPushButton(text)
        button.setToolTip(tip)
        button.setFixedSize(34, HEIGHT)
        button.setProperty("variant", "secondary")
        return button

    def focus(self) -> None:
        self.input.setFocus()
        self.input.selectAll()

    def _escape(self) -> None:
        """Escape clears the search and gives the focus back to the text."""
        self.input.clear()
        self.editor.setFocus()

    def _previous(self) -> None:
        self.step(-1)

    def _next(self) -> None:
        self.step(1)

    def _enter(self) -> None:
        shift = QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier
        self.step(-1 if shift else 1)

    def _edited(self, *_args: object) -> None:
        self.edited.emit()
        self._search(from_cursor=True)

    def refresh(self) -> None:
        """Look again after the text changed, without moving the view."""
        self._search(from_cursor=False)

    def step(self, step: int) -> None:
        """Go to the next (1) or previous (-1) match, round the ends."""
        if self._spans:
            self._current = (self._current + step) % len(self._spans)
            self._show_current()

    def _search(self, from_cursor: bool) -> None:
        text = self.editor.toPlainText()
        try:
            spans = find_spans(
                text,
                self.input.text(),
                self.case_button.isChecked(),
                self.regex_button.isChecked(),
            )
        except re.error as error:
            self._spans, self._current = [], -1
            self.input.setToolTip(str(error))
            self._paint(self.tr("Invalid expression"))
            return
        self.input.setToolTip("")
        self._spans = _document_offsets(text, spans)
        if not self._spans:
            self._current = -1
        elif from_cursor:  # the first match from where the person is
            where = self.editor.textCursor().selectionStart()
            self._current = next(
                (i for i, span in enumerate(self._spans) if span[0] >= where), 0
            )
        else:
            self._current = min(max(self._current, 0), len(self._spans) - 1)
        self._paint()
        if from_cursor and self._spans:
            self._show_current()

    def _show_current(self) -> None:
        start, end = self._spans[self._current]
        cursor = QTextCursor(self.editor.document())
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        self.editor.setTextCursor(cursor)
        self.editor.centerCursor()
        self._paint()

    def _paint(self, note: str = "") -> None:
        """Mark the matches in the text and say how many there are."""
        selections = []
        for start, end in self._spans[:MAX_MARKED]:
            cursor = QTextCursor(self.editor.document())
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            selection = QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.format = self._format
            selections.append(selection)
        self.editor.setExtraSelections(selections)
        if note:
            self.count_label.setText(note)
        elif self._spans:
            self.count_label.setText(
                self.tr("{current} of {total}").format(
                    current=self._current + 1, total=len(self._spans)
                )
            )
        else:
            self.count_label.setText(self.tr("No results") if self.input.text() else "")
