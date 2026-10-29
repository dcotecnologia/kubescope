from typing import Any, cast

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSize,
    Signal,
)
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope.theme import themed
from kubescope.views.chat_icons import sparkle_icon

BUBBLE = 54  # the round button in the corner
MARGIN = 20
ANIMATION_MS = 220  # the panel slides up and down; 0 shows it at once
SLIDE = 48  # how far below its place the panel starts and ends
BOTTOM = 56  # above the footer of the window, which has links
PANEL = QSize(430, 600)  # the chat, as large as the window leaves room for


def _bubble_style() -> str:
    """The round button of the corner, in the colors of the theme."""
    return (
        f"QPushButton#assistantBubble {{ background: {themed('#3020a5')};"
        f" border: 0; border-radius: {BUBBLE // 2}px; }}"
        f"QPushButton#assistantBubble:hover {{ background: {themed('#4030b8')}; }}"
    )


def _panel_style() -> str:
    """The panel and its header, in the colors of the theme."""
    border = themed("#e1e3e9")
    header = themed("#0d315d")
    ink = themed("#ffffff", text=True)
    edge = themed("#2d5077")
    return (
        f"QFrame#assistantPanel {{ background: {themed('#f7f7fa')};"
        f" border: 1px solid {border}; border-radius: 10px; }}"
        f"QFrame#assistantHeader {{ background: {header};"
        " border-top-left-radius: 10px; border-top-right-radius: 10px; }"
        f"QFrame#assistantHeader QLabel {{ color: {ink}; font-weight: 700; }}"
        f"QFrame#assistantHeader QPushButton {{ background: transparent; color: {ink};"
        f" border: 1px solid {edge}; border-radius: 4px; padding: 2px 8px; }}"
        "QFrame#assistantHeader QPushButton:hover "
        f"{{ background: {themed('#1f4f87')}; }}"
    )


class AssistantPanel(QFrame):
    """The chat as a panel over the window, with a header of its own."""

    clear_requested = Signal()
    closed = Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("assistantPanel")
        self.restyle()
        header = QFrame()
        header.setObjectName("assistantHeader")
        self.title = QLabel(self.tr("Assistant"))
        self.clear_button = QPushButton(self.tr("Clear history"))
        self.close_button = QPushButton("×")
        self.close_button.setToolTip(self.tr("Close"))
        row = QHBoxLayout(header)
        row.setContentsMargins(14, 8, 10, 8)
        row.setSpacing(8)
        row.addWidget(self.title, 1)
        row.addWidget(self.clear_button)
        row.addWidget(self.close_button)
        self.body = QVBoxLayout()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(0)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)
        layout.addWidget(header)
        layout.addLayout(self.body, 1)
        self.clear_button.clicked.connect(self.clear_requested)
        self.close_button.clicked.connect(self.closed)
        self.hide()

    def restyle(self) -> None:
        """Take the colors of the theme in use."""
        self.setStyleSheet(_panel_style())

    def show_chat(self, chat: QWidget | None) -> None:
        """Put a chat in the panel, in place of the one it had."""
        while (item := self.body.takeAt(0)) is not None:
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        if chat is not None:
            self.body.addWidget(chat)


class AssistantDock(QObject):
    """The round button in the corner of a window and the panel it opens.

    Both stay at the corner as the window is resized.
    """

    def __init__(self, host: QWidget) -> None:
        super().__init__(host)
        self.host = host
        self.bubble = QPushButton(host)
        self.bubble.setIconSize(QSize(34, 34))
        self.bubble.setObjectName("assistantBubble")
        self.bubble.setFixedSize(BUBBLE, BUBBLE)
        self.bubble.setToolTip(self.tr("Ask the assistant"))
        self.panel = AssistantPanel(host)
        self._open = False
        self._animation = QParallelAnimationGroup(self)
        self.restyle()
        host.installEventFilter(self)
        self.place()

    def restyle(self) -> None:
        """Take the colors of the theme in use."""
        self.bubble.setStyleSheet(_bubble_style())
        self.bubble.setIcon(
            sparkle_icon(themed("#ffffff", text=True), 34, themed("#3020a5"))
        )
        self.panel.restyle()

    def retranslate(self) -> None:
        self.bubble.setToolTip(self.tr("Ask the assistant"))
        self.panel.title.setText(self.tr("Assistant"))
        self.panel.clear_button.setText(self.tr("Clear history"))
        self.panel.close_button.setToolTip(self.tr("Close"))

    @property
    def is_open(self) -> bool:
        return self._open

    def _target(self) -> QRect:
        """Where the panel sits when open: over the button, which it covers,
        with its corner on the corner of the button, no larger than the room
        the window has."""
        width, height = self.host.width(), self.host.height()
        panel_width = max(min(PANEL.width(), width - 2 * MARGIN), 0)
        panel_height = max(min(PANEL.height(), height - BOTTOM - MARGIN), 0)
        return QRect(
            width - panel_width - MARGIN,
            height - BOTTOM - panel_height,
            panel_width,
            panel_height,
        )

    def _slide_to(self, start: QPoint, end: QPoint, fade: tuple[float, float]) -> None:
        """Move the panel and fade it, together."""
        self._animation.stop()
        effect = QGraphicsOpacityEffect(self.panel)
        self.panel.setGraphicsEffect(effect)
        move = QPropertyAnimation(self.panel, b"pos")
        move.setStartValue(start)
        move.setEndValue(end)
        blend = QPropertyAnimation(effect, b"opacity")
        blend.setStartValue(fade[0])
        blend.setEndValue(fade[1])
        for animation in (move, blend):
            animation.setDuration(ANIMATION_MS)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation = QParallelAnimationGroup(self)
        self._animation.addAnimation(move)
        self._animation.addAnimation(blend)
        self._animation.finished.connect(self._slid)
        self._animation.start()

    def _slid(self) -> None:
        cast(Any, self.panel).setGraphicsEffect(None)  # the effect only fades
        if not self._open:
            self.panel.hide()
        else:
            self.panel.setGeometry(self._target())

    def open(self) -> None:
        self._open = True
        self.panel.setGeometry(self._target())
        self.panel.show()
        self.panel.raise_()
        if ANIMATION_MS > 0:
            target = self.panel.pos()
            self._slide_to(target + QPoint(0, SLIDE), target, (0.0, 1.0))

    def close(self) -> None:
        was_open, self._open = self._open, False
        if not was_open or self.panel.isHidden():
            return
        if ANIMATION_MS > 0:
            here = self.panel.pos()
            self._slide_to(here, here + QPoint(0, SLIDE), (1.0, 0.0))
        else:
            self.panel.hide()

    def place(self) -> None:
        """Put the button in the corner and, when open, the panel over it."""
        width, height = self.host.width(), self.host.height()
        self.bubble.move(width - BUBBLE - MARGIN, height - BUBBLE - BOTTOM)
        if self._open and self._animation.state() != QPropertyAnimation.State.Running:
            self.panel.setGeometry(self._target())
        self.bubble.raise_()
        if self._open:
            self.panel.raise_()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.host and event.type() == QEvent.Type.Resize:
            self.place()
        return False
