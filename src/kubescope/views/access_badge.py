"""The badge in the footer that says what access the app has to the
clusters."""

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from kubescope.views.lock_icon import lock_pixmap


class AccessBadge(QFrame):
    """A small pill: a padlock, closed for read-only and open for the write
    mode, and the name of the access."""

    clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("accessBadge")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 0, 7, 0)
        layout.setSpacing(4)
        self.icon = QLabel()
        self.icon.setStyleSheet("background: transparent; border: 0;")
        self.label = QLabel()
        for label in (self.icon, self.label):  # the click is the badge's
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout.addWidget(self.icon)
        layout.addWidget(self.label)
        self.setFixedHeight(16)
        self._keeper: _Centered | None = None
        if parent is not None:  # it stays in the middle of what holds it
            self._keeper = _Centered(self, parent)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
            event.position().toPoint()
        ):
            self.clicked.emit()
        super().mouseReleaseEvent(event)

    def text(self) -> str:
        return self.label.text()

    def show_access(self, text: str, tone: QColor, unlocked: bool, tip: str) -> None:
        """Draw the badge in the color `tone`."""
        red, green, blue = tone.red(), tone.green(), tone.blue()
        self.setStyleSheet(
            f"QFrame#accessBadge {{ background: rgba({red}, {green}, {blue}, 38);"
            f" border: 1px solid rgba({red}, {green}, {blue}, 130);"
            " border-radius: 8px; }"
            f"QFrame#accessBadge QLabel {{ color: {tone.name()}; border: 0;"
            " background: transparent; font-size: 8px; font-weight: 700; }"
        )
        self.label.setText(text.upper())
        self.icon.setPixmap(lock_pixmap(tone, unlocked))
        self.setToolTip(tip)
        self.adjustSize()
        if self._keeper is not None:
            self._keeper.place()


class _Centered(QObject):
    """Keeps a widget in the middle of its parent, whatever the layout beside
    it, as the parent is resized."""

    def __init__(self, widget: QWidget, parent: QWidget) -> None:
        super().__init__(widget)
        self.widget = widget
        self.parent_widget = parent
        parent.installEventFilter(self)

    def place(self) -> None:
        parent, widget = self.parent_widget, self.widget
        widget.move(
            (parent.width() - widget.width()) // 2,
            (parent.height() - widget.height()) // 2,
        )
        widget.raise_()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Resize:
            self.place()
        return False
