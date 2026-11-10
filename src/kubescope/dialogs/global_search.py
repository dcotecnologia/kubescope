from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtCore import QCoreApplication, QEvent, QObject, Qt
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

from kubescope.models import SearchHit, match_rank
from kubescope.theme import themed_stylesheet

MAX_RESULTS = 50
TOP_OFFSET = 70  # the distance from the top of the window, like a command palette

# Written with the light colors; themed_stylesheet recolors it to the theme.
STYLE = """
QFrame#searchPanel {
    background: #ffffff; border: 1px solid #d9dce4; border-radius: 10px;
}
QListWidget#searchResults {
    background: transparent; border: 0; outline: 0; color: #20232a;
}
QListWidget#searchResults::item { padding: 6px 10px; border-radius: 5px; }
QListWidget#searchResults::item:selected {
    background: #d9d3f2; color: #20232a;
}
QLabel#searchNote { color: #6b7380; padding: 0 4px; }
"""


@dataclass(frozen=True, slots=True)
class SearchEntry:
    """One thing the search can go to: a screen, an action or a resource."""

    label: str
    detail: str
    run: Callable[[], None]


class GlobalSearch(QDialog):
    """Type to find a screen, an action or a resource of any namespace."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        translate = QCoreApplication.translate
        self.setWindowTitle(translate("GlobalSearch", "Search"))
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
        self.input.setPlaceholderText(
            translate("GlobalSearch", "Search screens, actions and resources...")
        )
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
        inside.setContentsMargins(12, 12, 12, 10)
        inside.setSpacing(8)
        inside.addWidget(self.input)
        inside.addWidget(self.results, 1)
        inside.addWidget(self.note)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(panel)
        self.setStyleSheet(themed_stylesheet(STYLE))
        self.input.textChanged.connect(self._filter)
        self.results.itemActivated.connect(self._choose)
        self.results.itemClicked.connect(self._choose)

    def open_with(self, entries: list[SearchEntry]) -> None:
        """Show the dialog with the screens and actions; resources come
        later."""
        self._entries = list(entries)
        self._resources = []
        self.input.clear()
        self.note.setText(
            QCoreApplication.translate("GlobalSearch", "Loading resources...")
        )
        self.setStyleSheet(themed_stylesheet(STYLE))  # the theme may have changed
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
            ranked.sort(
                key=lambda pair: pair[0]
            )  # stable: keeps the order inside a rank
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
