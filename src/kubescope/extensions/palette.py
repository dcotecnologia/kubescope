"""The window that finds a screen, an action or a resource as one types, like a
command palette (`kubescope.sdk.Components.palette`)."""

from collections.abc import Callable
from dataclasses import dataclass

from kubescope.sdk.models import SearchHit, match_rank
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

MAX_RESULTS = 50
TOP_OFFSET = 70  # the distance from the top of the window, like a command palette


def style(themed: Callable[[str, bool], str]) -> str:
    """The style sheet of the window, in the colors of the theme in use."""
    return f"""
QFrame#searchPanel {{
    background: {themed("#ffffff", False)};
    border: 1px solid {themed("#d9dce4", False)}; border-radius: 10px;
}}
QListWidget#searchResults {{
    background: transparent; border: 0; outline: 0; color: {themed("#20232a", True)};
}}
QListWidget#searchResults::item {{ padding: 6px 10px; border-radius: 5px; }}
QListWidget#searchResults::item:selected {{
    background: {themed("#d9d3f2", False)}; color: {themed("#20232a", True)};
}}
QLabel#searchNote {{ color: {themed("#6b7380", True)}; padding: 0 4px; }}
"""


@dataclass(frozen=True, slots=True)
class SearchEntry:
    """One thing the search can go to: a screen, an action or a resource."""

    label: str
    detail: str
    run: Callable[[], None]


class Palette(QDialog):
    """Type to find a screen, an action or a resource of any namespace."""

    def __init__(
        self,
        parent: QWidget | None = None,
        themed: Callable[[str, bool], str] = lambda color, text: color,
        title: str = "Search",
        placeholder: str = "Search screens, actions and resources...",
        loading: str = "Loading resources...",
        actions: Callable[[], list[SearchEntry]] = lambda: [],
    ) -> None:
        super().__init__(parent)
        self._themed = themed
        self._actions = actions  # what the app itself can do, asked each time it opens
        self._loading = loading
        self.setWindowTitle(title)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.resize(580, 420)
        self._entries: list[SearchEntry] = []
        self._resources: list[SearchEntry] = []
        self.input = QLineEdit(self)
        self.input.setPlaceholderText(placeholder)
        self.input.setClearButtonEnabled(True)
        self.input.installEventFilter(self)
        self.input.setProperty("variant", "filter")
        self.results = QListWidget(self)
        self.results.setObjectName("searchResults")
        self.results.setUniformItemSizes(True)
        self.results.setFrameShape(QFrame.Shape.NoFrame)
        self.results.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.note = QLabel(self)
        self.note.setObjectName("searchNote")
        panel = QFrame(self)
        panel.setObjectName("searchPanel")
        inside = QVBoxLayout(panel)
        inside.setContentsMargins(12, 12, 12, 12)
        inside.setSpacing(8)
        inside.addWidget(self.input)
        inside.addWidget(self.results, 1)
        inside.addWidget(self.note)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(panel)
        self.setStyleSheet(style(themed))
        self.input.textChanged.connect(self._filter)
        self.results.itemActivated.connect(self._choose)
        self.results.itemClicked.connect(self._choose)

    def open_with(self, entries: list[SearchEntry]) -> None:
        """Show the window with the screens and actions; resources come
        later."""
        self._entries = [*entries, *self._actions()]
        self._resources = []
        self.input.clear()
        self.note.setText(self._loading)
        self.setStyleSheet(style(self._themed))  # the theme may have changed
        self._filter()
        parent = self.parentWidget()
        if parent is not None:
            area = parent.frameGeometry()
            self.move(area.center().x() - self.width() // 2, area.top() + TOP_OFFSET)
        self.show()
        self.input.setFocus()

    def set_resources(
        self, hits: list[SearchHit], run: Callable[[SearchHit], None]
    ) -> None:
        self._resources = [
            SearchEntry(
                hit.name,
                f"{hit.kind} · {hit.namespace}" if hit.namespace else hit.kind,
                lambda hit=hit: run(hit),
            )
            for hit in hits
        ]
        self.note.setText("")
        self._filter()

    def resources_failed(self, message: str) -> None:
        self.note.setText(message)

    def _filter(self) -> None:
        query = self.input.text().strip()
        pool = [*self._entries, *self._resources]
        if query:
            ranked = []
            for entry in pool:
                rank = match_rank(query, f"{entry.label} {entry.detail}")
                if rank is not None:
                    ranked.append((rank, entry))
            ranked.sort(key=lambda pair: pair[0])  # stable: keeps the order in a rank
            pool = [entry for _rank, entry in ranked]
        else:
            pool = self._entries  # nothing typed: the screens and actions only
        self.results.clear()
        for entry in pool[:MAX_RESULTS]:
            item = QListWidgetItem(
                f"{entry.label}    {entry.detail}" if entry.detail else entry.label
            )
            item.setData(Qt.ItemDataRole.UserRole, entry)
            self.results.addItem(item)
        if self.results.count():
            self.results.setCurrentRow(0)

    def _choose(self, item: QListWidgetItem) -> None:
        entry = item.data(Qt.ItemDataRole.UserRole)
        self.accept()
        entry.run()

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.WindowDeactivate and self.isVisible():
            self.reject()  # a click outside closes it, like a menu
        return super().event(event)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if (
            watched is self.input
            and isinstance(event, QKeyEvent)
            and event.type() == QEvent.Type.KeyPress
        ):
            key = event.key()
            if key in (Qt.Key.Key_Down, Qt.Key.Key_Up):
                step = 1 if key == Qt.Key.Key_Down else -1
                row = self.results.currentRow() + step
                self.results.setCurrentRow(
                    min(max(row, 0), max(self.results.count() - 1, 0))
                )
                return True
            if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                current = self.results.currentItem()
                if current is not None:
                    self._choose(current)
                return True
        return super().eventFilter(watched, event)
