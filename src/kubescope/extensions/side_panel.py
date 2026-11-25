"""The panel that slides in from the right edge of the window, with a title,
buttons in its header and a list of cards, and the card of a notice and the
button with a counter that opens it, for the extensions that have such a list
(`kubescope.sdk.Components.side_panel`, `notice_card`, `counter_button`)."""

from collections.abc import Callable, Sequence
from typing import Any

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPoint,
    QPointF,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QIcon,
    QKeySequence,
    QMouseEvent,
    QPainter,
    QShortcut,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

WIDTH = 400  # the usual width, which can be dragged
MIN_WIDTH = 300
MAX_WIDTH = 900
GRIP = 6  # the strip at the left edge that is dragged
SLIDE_MS = 220
BADGE = QColor("#e5484d")


def style(themed: Callable[[str, bool], str]) -> str:
    """The style sheet of the panel and its cards, in the colors of the theme
    in use."""
    return f"""
QFrame#sidePanel {{
    background: {themed("#ffffff", False)};
    border-left: 1px solid {themed("#e1e3e9", False)};
}}
QLabel#sidePanelTitle {{
    color: {themed("#17191e", True)}; font-size: 15px; font-weight: 700;
}}
QLabel#sidePanelEmpty {{ color: {themed("#6b7380", True)}; }}
QScrollArea#sidePanelScroll, QWidget#sidePanelList {{
    background: transparent; border: 0;
}}
QFrame#noticeCard {{
    background: {themed("#f3f4f7", False)};
    border: 1px solid {themed("#e1e3e9", False)}; border-radius: 8px;
}}
QFrame#noticeCard[level="error"] {{
    border-left: 3px solid {themed("#a33d45", False)};
}}
QFrame#noticeCard[level="info"], QFrame#noticeCard[level="normal"] {{
    border-left: 3px solid {themed("#3220a0", False)};
}}
QFrame#noticeCard[level="warning"] {{
    border-left: 3px solid {themed("#985415", False)};
}}
QLabel#noticeReason {{
    color: {themed("#20232a", True)}; font-weight: 700;
}}
QLabel#noticeMessage {{ color: {themed("#20232a", True)}; }}
QFrame#noticeCard[read="false"] {{
    background: {themed("#eee9f7", False)};
    border-top-color: {themed("#b9b3dc", False)};
    border-right-color: {themed("#b9b3dc", False)};
    border-bottom-color: {themed("#b9b3dc", False)};
}}  /* the left edge keeps the color of the level */
QFrame#noticeCard[read="true"] QLabel {{
    color: {themed("#6b7380", True)};
}}
QLabel#noticeMeta {{ color: {themed("#6b7380", True)}; font-size: 10px; }}
"""


class _Grip(QWidget):
    """The strip at the left edge of the panel, which is dragged to make it
    wider or narrower."""

    dragged = Signal(int)  # the width the panel should have
    released = Signal()

    def __init__(self, panel: QWidget) -> None:
        super().__init__(panel)
        self._panel = panel
        self._origin: QPointF | None = None
        self._start = 0
        self.setCursor(Qt.CursorShape.SizeHorCursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._origin = event.globalPosition()
        self._start = self._panel.width()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._origin is not None:
            moved = event.globalPosition() - self._origin
            self.dragged.emit(self._start - int(moved.x()))  # leftward is wider

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._origin is not None:
            self._origin = None
            self.released.emit()


class NoticeCard(QFrame):
    """One notice of the list: a title and a kind, where it is about, its
    message, when it began, and the links under it.

    A click on the card calls
    `on_click`.
    """

    def __init__(
        self,
        title: str,
        kind: str,
        about: str,
        message: str,
        when: str,
        level: str,
        unread: bool,
        tip: str,
        on_click: Callable[[], None],
        actions: Sequence[tuple[str, Callable[[], None]]],
        link: Callable[[str], QPushButton],
    ) -> None:
        super().__init__()
        self._on_click = on_click
        self.unread = unread
        self.setObjectName("noticeCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("read", "false" if unread else "true")
        self.setToolTip(tip)  # a click reads it, and nothing else
        self.setProperty("level", level)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 9, 12, 9)
        layout.setSpacing(3)
        reason = QLabel(title)
        reason.setObjectName("noticeReason")
        reason.setWordWrap(True)
        meta = QLabel(kind)
        meta.setObjectName("noticeMeta")
        head = QHBoxLayout()
        head.addWidget(reason)
        head.addStretch(1)
        head.addWidget(meta)
        layout.addLayout(head)
        if about:
            where = QLabel(about)
            where.setObjectName("noticeMeta")
            where.setWordWrap(True)
            layout.addWidget(where)
        text = QLabel(message)
        text.setObjectName("noticeMessage")
        text.setWordWrap(True)
        layout.addWidget(text)
        stamp = QLabel(when)
        stamp.setObjectName("noticeMeta")
        layout.addWidget(stamp)
        self.buttons: list[QPushButton] = []
        if actions:
            row = QHBoxLayout()
            row.setSpacing(10)
            for label, callback in actions:
                button = link(label)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.setStyleSheet("font-size: 11px; padding: 0;")
                button.clicked.connect(lambda _c=False, run=callback: run())
                row.addWidget(button)
                self.buttons.append(button)
            row.addStretch(1)
            layout.addLayout(row)
        for label in self.findChildren(QLabel):  # the click is the card's
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        if not unread:  # read: crossed out
            for label in (reason, text):
                font = label.font()
                font.setStrikeOut(True)
                font.setBold(False)
                label.setFont(font)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
            event.position().toPoint()
        ):
            self._on_click()
        super().mouseReleaseEvent(event)


class SidePanel(QFrame):
    """Sits on `host`, under the top bar, and slides in and out at its right
    edge.

    Its header has the `actions` buttons and a close button; under it a
    scroll area holds the cards `show_cards` is given.
    """

    def __init__(
        self,
        host: QWidget,
        title: str,
        actions: Sequence[QPushButton],
        close_button: QPushButton,
        themed: Callable[[str, bool], str],
        top: Callable[[], int],
        empty_text: str = "",
    ) -> None:
        super().__init__(host)
        self.host = host
        self._themed = themed
        self._top = top
        self._empty_text = empty_text
        self.setObjectName("sidePanel")
        self._width = WIDTH
        self.setFixedWidth(WIDTH)
        self.hide()
        self.opened = False
        self.on_closed: Callable[[], None] = lambda: None
        self.on_resized: Callable[[int], None] = lambda width: None
        # a place on the screen that belongs to the panel's own button: a click
        # there is not a click outside, which would close the panel
        self.is_inside: Callable[[QPoint], bool] = lambda position: False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        header = QHBoxLayout()
        label = QLabel(title)
        label.setObjectName("sidePanelTitle")
        header.addWidget(label)
        header.addStretch(1)
        for button in actions:
            header.addWidget(button)
        self.close_button = close_button
        header.addWidget(close_button)
        close_button.clicked.connect(self.close_panel)
        layout.addLayout(header)

        self.scroller = QScrollArea()
        self.scroller.setObjectName("sidePanelScroll")
        self.scroller.setWidgetResizable(True)
        self.scroller.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._place: int | None = None  # where the list was before it was drawn
        self.list = QWidget()
        self.list.setObjectName("sidePanelList")
        self.rows = QVBoxLayout(self.list)
        self.rows.setContentsMargins(0, 0, 4, 0)
        self.rows.setSpacing(8)
        self.scroller.setWidget(self.list)
        layout.addWidget(self.scroller, 1)
        self.scroller.verticalScrollBar().rangeChanged.connect(self._restore_place)

        self.animation = QPropertyAnimation(self, b"pos", self)
        self.animation.setDuration(SLIDE_MS)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self._slid)
        # Esc closes it, but only while it is open, so the key stays free for
        # the rest of the window the rest of the time
        self._escape = QShortcut(QKeySequence(Qt.Key.Key_Escape), host)
        self._escape.setContext(Qt.ShortcutContext.WindowShortcut)
        self._escape.setEnabled(False)
        self._escape.activated.connect(self.close_panel)
        self.grip = _Grip(self)
        self.grip.dragged.connect(self.set_panel_width)
        self.grip.released.connect(lambda: self.on_resized(self._width))
        host.installEventFilter(self)
        self.restyle()

    def restyle(self) -> None:
        self.setStyleSheet(style(self._themed))

    def show_cards(self, cards: Sequence[QWidget]) -> None:
        """Draw the cards, with the place of the list kept."""
        bar = self.scroller.verticalScrollBar()
        place = bar.value()
        while (child := self.rows.takeAt(0)) is not None:
            if (widget := child.widget()) is not None:
                widget.deleteLater()
        if not cards:
            empty = QLabel(self._empty_text)
            empty.setObjectName("sidePanelEmpty")
            empty.setWordWrap(True)
            self.rows.addWidget(empty)
        for card in cards:
            self.rows.addWidget(card)
        self.rows.addStretch(1)
        self._place = place if place else None  # given back once the list is long
        QTimer.singleShot(300, self.scroller, self._forget_place)

    def set_panel_width(self, width: int) -> None:
        """Give the panel a width, within what keeps it usable; while it is
        open it stays at the right edge."""
        self._width = min(max(width, MIN_WIDTH), MAX_WIDTH)
        if self.opened and self.animation.state() != QPropertyAnimation.State.Running:
            shown, _hidden = self._geometry()
            self.move(shown)
        else:
            self.setFixedWidth(self._fitted())
        self._place_grip()

    def _fitted(self) -> int:
        """The width it has now: the one chosen, as far as the window lets."""
        room = max(self.host.width() - 40, 200)
        return min(self._width, MAX_WIDTH, room)

    def _place_grip(self) -> None:
        self.grip.setGeometry(0, 0, GRIP, self.height())
        self.grip.raise_()

    def _restore_place(self, _minimum: int, maximum: int) -> None:
        """The list grew back to where the person was: put them there."""
        if self._place is not None and maximum >= self._place:
            self.scroller.verticalScrollBar().setValue(self._place)
            self._place = None

    def _forget_place(self) -> None:
        self._place = None

    def _geometry(self) -> tuple[QPoint, QPoint]:
        top = self._top()
        width = self._fitted()
        self.setFixedSize(width, max(self.host.height() - top, 0))
        self._place_grip()
        shown = QPoint(self.host.width() - width, top)
        return shown, QPoint(self.host.width(), top)

    def open_panel(self) -> None:
        shown, hidden = self._geometry()
        self.opened = True
        self._escape.setEnabled(True)
        app = QApplication.instance()
        if app is not None:  # a click anywhere else of the window closes it
            app.installEventFilter(self)
        self.move(hidden)
        self.show()
        self.raise_()
        self.animation.stop()
        self.animation.setStartValue(hidden)
        self.animation.setEndValue(shown)
        self.animation.start()

    def close_panel(self) -> None:
        if not self.opened:
            return
        shown, hidden = self._geometry()
        self.opened = False
        self._escape.setEnabled(False)
        app = QApplication.instance()
        if app is not None:
            app.removeEventFilter(self)
        self.animation.stop()
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(hidden)
        self.animation.start()
        self.on_closed()

    def _slid(self) -> None:
        if not self.opened:
            self.hide()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Follow the window as it is resized, and close the panel when a click
        of the window falls outside of it."""
        if (
            self.opened
            and event.type() == QEvent.Type.MouseButtonPress
            and isinstance(watched, QWidget)
            and watched.window() is self.window()
            and isinstance(event, QMouseEvent)
        ):
            position = event.globalPosition().toPoint()
            # a press that nothing takes goes up to the parent, which this sees too:
            # it is the place of the click that says where it was, and what is
            # inside the panel (its grip and its cards) is the panel's own
            own = watched is self or self.isAncestorOf(watched)
            inside = self.rect().contains(self.mapFromGlobal(position))
            if not own and not inside and not self.is_inside(position):
                self.close_panel()
        if (
            watched is self.host
            and event.type() == QEvent.Type.Resize
            and self.opened
            and self.animation.state() != QPropertyAnimation.State.Running
        ):
            shown, _hidden = self._geometry()
            self.move(shown)
        return False


class CounterButton(QPushButton):
    """A flat 32 px button like the one of the Settings, which shows a red
    badge with a count when something was not read."""

    def __init__(
        self,
        icon: QIcon,
        tooltip: str,
        themed: Callable[[str, bool], str],
        name: str,
    ) -> None:
        super().__init__()
        self.unread = 0
        self._name = name
        self.setObjectName(name)
        self.setFixedSize(32, 32)
        self.setIcon(icon)
        self.setIconSize(QSize(18, 18))
        self.setToolTip(tooltip)
        self.setCheckable(True)
        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.restyle(themed)

    def restyle(self, themed: Callable[[str, bool], str]) -> None:
        """Dress it as the Settings button beside it is, in the colors of the
        theme in use: the top bar has colors of its own in each theme, and the
        light ones written here would show through in the others."""
        hover = themed("#0d315d", False)
        selected = themed("#1f4f87", False)
        name = self._name
        self.setStyleSheet(
            f"QPushButton#{name} {{ background: transparent;"
            " border: 1px solid transparent; border-radius: 4px; padding: 0; }"
            f"QPushButton#{name}:hover {{ background: {hover}; }}"
            f"QPushButton#{name}:checked {{ background: {selected}; }}"
        )

    def set_unread(self, count: int) -> None:
        self.unread = max(count, 0)
        self.update()

    def badge_text(self) -> str:
        return "99+" if self.unread > 99 else str(self.unread)

    def paintEvent(self, event: Any) -> None:
        super().paintEvent(event)
        if not self.unread:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        text = self.badge_text()
        font = QFont(self.font())
        font.setPixelSize(9)
        font.setBold(True)
        painter.setFont(font)
        width = max(14, painter.fontMetrics().horizontalAdvance(text) + 8)
        rect = QRectF(self.width() - width - 1, 1, width, 14)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(BADGE)
        painter.drawRoundedRect(rect, 7, 7)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
