from typing import Any, cast

from PySide6.QtCore import (
    QByteArray,
    QEasingCurve,
    QEvent,
    QObject,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QCloseEvent, QMouseEvent, QMoveEvent, QResizeEvent
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
from kubescope.views.chat_icons import dock_icon, popout_icon, sparkle_icon

BUBBLE = 54  # the round button in the corner
MARGIN = 20
ANIMATION_MS = 220  # the panel slides up and down; 0 shows it at once
SLIDE = 48  # how far below its place the panel starts and ends
BOTTOM = 6  # the button sits in the corner of the footer, which leaves room for it
PANEL = QSize(430, 600)  # the size of the chat the first time
MIN_PANEL = QSize(320, 360)  # the least the person can make it
EDGE = 6  # the width of the strip that is grabbed to resize
SAVE_DELAY_MS = 400  # a moved or resized window is written down after this


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


class ResizeHandle(QWidget):
    """A strip of the border of the panel that is dragged to resize it.

    The panel is anchored at its bottom right, so it grows toward the
    top left.
    """

    dragged = Signal(int, int)  # how far the pointer moved since the press
    released = Signal()

    def __init__(self, parent: QWidget, left: bool, top: bool) -> None:
        super().__init__(parent)
        self.left, self.top = left, top
        self._origin: QPoint | None = None
        cursor = {
            (True, True): Qt.CursorShape.SizeFDiagCursor,
            (True, False): Qt.CursorShape.SizeHorCursor,
            (False, True): Qt.CursorShape.SizeVerCursor,
        }[(left, top)]
        self.setCursor(cursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._origin = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._origin is None:
            return
        moved = event.globalPosition().toPoint() - self._origin
        self.dragged.emit(moved.x() if self.left else 0, moved.y() if self.top else 0)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._origin is not None:
            self._origin = None
            self.released.emit()


class AssistantPanel(QFrame):
    """The chat as a panel over the window, with a header of its own."""

    clear_requested = Signal()
    closed = Signal()
    float_requested = Signal()  # take it out of the window, or put it back
    dragged = Signal(int, int)  # the border was dragged: how far
    released = Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("assistantPanel")
        self.restyle()
        header = QFrame()
        header.setObjectName("assistantHeader")
        self.title = QLabel(self.tr("Assistant"))
        self.clear_button = QPushButton(self.tr("Clear history"))
        self.float_button = QPushButton()
        self.float_button.setFixedWidth(34)
        self.close_button = QPushButton("×")
        self.close_button.setToolTip(self.tr("Close"))
        row = QHBoxLayout(header)
        row.setContentsMargins(14, 8, 10, 8)
        row.setSpacing(8)
        row.addWidget(self.title, 1)
        row.addWidget(self.clear_button)
        row.addWidget(self.float_button)
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
        self.float_button.clicked.connect(self.float_requested)
        self.close_button.clicked.connect(self.closed)
        self.handles = [
            ResizeHandle(self, left=True, top=False),
            ResizeHandle(self, left=False, top=True),
            ResizeHandle(self, left=True, top=True),
        ]
        for handle in self.handles:
            handle.dragged.connect(self.dragged)
            handle.released.connect(self.released)
        self.set_floating(False)
        self.hide()

    def set_floating(self, floating: bool) -> None:
        """Out of the window the system resizes it; in it, the borders do."""
        for handle in self.handles:
            handle.setVisible(not floating)
        self.float_button.setIcon(
            dock_icon(themed("#ffffff", text=True))
            if floating
            else popout_icon(themed("#ffffff", text=True))
        )
        self.float_button.setToolTip(
            self.tr("Put it back in the window")
            if floating
            else self.tr("Open in a window of its own")
        )
        self._floating = floating

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        width, height = self.width(), self.height()
        left, top, corner = self.handles
        left.setGeometry(0, EDGE * 2, EDGE, max(height - EDGE * 2, 0))
        top.setGeometry(EDGE * 2, 0, max(width - EDGE * 2, 0), EDGE)
        corner.setGeometry(0, 0, EDGE * 2, EDGE * 2)
        for handle in self.handles:
            handle.raise_()

    def restyle(self) -> None:
        """Take the colors of the theme in use."""
        self.setStyleSheet(_panel_style())
        if hasattr(self, "float_button"):
            self.set_floating(self._floating)

    def show_chat(self, chat: QWidget | None) -> None:
        """Put a chat in the panel, in place of the one it had."""
        while (item := self.body.takeAt(0)) is not None:
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        if chat is not None:
            self.body.addWidget(chat)


class FloatingFrame(QWidget):
    """The window of the chat when it is taken out of the main window."""

    closing = Signal()
    moved = Signal()  # it was moved or resized

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle(self.tr("Assistant"))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.holder = layout

    def closeEvent(self, event: QCloseEvent) -> None:
        self.hide()
        event.ignore()  # it is only put away, with its place kept
        self.closing.emit()

    def moveEvent(self, event: QMoveEvent) -> None:
        super().moveEvent(event)
        self.moved.emit()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.moved.emit()


class AssistantDock(QObject):
    """The round button in the corner of a window and the panel it opens.

    Both stay at the corner as the window is resized. The panel can be
    made larger or smaller by its borders and taken out into a window of
    its own; its size, whether it is out and where, are kept.
    """

    state_changed = Signal()  # the size, the mode or the place changed

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
        self._size = QSize(
            PANEL
        )  # what the person asked for; the window may allow less
        self._drag_start = QSize()
        self._floating = False
        self._frame: FloatingFrame | None = None
        self._geometry = QByteArray()
        self._animation = QParallelAnimationGroup(self)
        self._save = QTimer(self)
        self._save.setSingleShot(True)
        self._save.setInterval(SAVE_DELAY_MS)
        self._save.timeout.connect(self.state_changed)
        self.panel.float_requested.connect(self.toggle_floating)
        self.panel.dragged.connect(self._resize_by)
        self.panel.released.connect(self._end_drag)
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
        self.panel.set_floating(self._floating)
        if self._frame is not None:
            self._frame.setWindowTitle(self.tr("Assistant"))

    @property
    def is_open(self) -> bool:
        return self._open

    @property
    def is_floating(self) -> bool:
        return self._floating

    def _room(self) -> QSize:
        """The most the window leaves for the panel."""
        return QSize(
            max(self.host.width() - 2 * MARGIN, 0),
            max(self.host.height() - BOTTOM - MARGIN, 0),
        )

    def _target(self) -> QRect:
        """Where the panel sits when open in the window: over the button, which
        it covers, with its corner on the corner of the button, as large as the
        person made it and the window allows."""
        room = self._room()
        width = min(max(self._size.width(), MIN_PANEL.width()), room.width())
        height = min(max(self._size.height(), MIN_PANEL.height()), room.height())
        return QRect(
            self.host.width() - width - MARGIN,
            self.host.height() - BOTTOM - height,
            width,
            height,
        )

    def _resize_by(self, dx: int, dy: int) -> None:
        """A border was dragged: the panel grows toward the top left."""
        if self._drag_start.isEmpty():
            self._drag_start = self._target().size()
        room = self._room()
        self._size = QSize(
            min(max(self._drag_start.width() - dx, MIN_PANEL.width()), room.width()),
            min(max(self._drag_start.height() - dy, MIN_PANEL.height()), room.height()),
        )
        self.panel.setGeometry(self._target())

    def _end_drag(self) -> None:
        """The border was let go: the size is the person's, to keep."""
        self._drag_start = QSize()
        self.state_changed.emit()

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
        if self._floating:
            self._show_frame()
            return
        self._drag_start = QSize()
        self.panel.setGeometry(self._target())
        self.panel.show()
        self.panel.raise_()
        if ANIMATION_MS > 0:
            target = self.panel.pos()
            self._slide_to(target + QPoint(0, SLIDE), target, (0.0, 1.0))

    def close(self) -> None:
        was_open, self._open = self._open, False
        if self._floating:
            if self._frame is not None:
                self._frame.hide()
            return
        if not was_open or self.panel.isHidden():
            return
        if ANIMATION_MS > 0:
            here = self.panel.pos()
            self._slide_to(here, here + QPoint(0, SLIDE), (1.0, 0.0))
        else:
            self.panel.hide()

    def _make_frame(self) -> FloatingFrame:
        frame = FloatingFrame(self.host.window())
        frame.closing.connect(self._frame_closed)
        frame.moved.connect(self._save.start)
        return frame

    def _show_frame(self) -> None:
        """Show the window of the chat, where it was left."""
        if self._frame is None:
            self._frame = self._make_frame()
            self._frame.holder.addWidget(self.panel)
        frame = self._frame
        if not frame.isVisible():
            placed = not self._geometry.isEmpty() and frame.restoreGeometry(
                self._geometry
            )
            if not placed:
                frame.resize(self._size)
        self.panel.show()
        frame.show()
        frame.raise_()
        frame.activateWindow()

    def _frame_closed(self) -> None:
        self._open = False
        self.state_changed.emit()

    def set_floating(self, floating: bool) -> None:
        """Take the panel out of the window into one of its own, or put it
        back."""
        if floating == self._floating:
            return
        was_open = self._open
        if floating:
            self._animation.stop()
            cast(Any, self.panel).setGraphicsEffect(None)
            self._floating = True
            self.panel.set_floating(True)
            self._open = was_open
            if was_open:
                self._show_frame()
            else:
                if self._frame is None:
                    self._frame = self._make_frame()
                    self._frame.holder.addWidget(self.panel)
        else:
            if self._frame is not None:
                self._geometry = self._frame.saveGeometry()
                self._frame.hide()
            self._floating = False
            self.panel.set_floating(False)
            self.panel.setParent(self.host)
            self.panel.hide()
            self._open = False
            if was_open:
                self.open()
        self.state_changed.emit()

    def toggle_floating(self) -> None:
        self.set_floating(not self._floating)

    def state(self) -> dict[str, Any]:
        """What is kept of the panel between runs."""
        geometry = ""
        if self._frame is not None and self._floating:
            self._geometry = self._frame.saveGeometry()
        if not self._geometry.isEmpty():
            geometry = bytes(self._geometry.toBase64().data()).decode("ascii")
        return {
            "width": self._size.width(),
            "height": self._size.height(),
            "floating": self._floating,
            "geometry": geometry,
        }

    def restore(self, state: dict[str, Any]) -> None:
        """Take back what `state` kept; the panel itself stays closed."""
        self._size = QSize(
            state.get("width", PANEL.width()), state.get("height", PANEL.height())
        )
        geometry = state.get("geometry", "")
        self._geometry = QByteArray.fromBase64(QByteArray(geometry.encode("ascii")))
        if state.get("floating") is True and not self._floating:
            self.set_floating(True)

    def place(self) -> None:
        """Put the button in the corner and, when open, the panel over it."""
        width, height = self.host.width(), self.host.height()
        self.bubble.move(width - BUBBLE - MARGIN, height - BUBBLE - BOTTOM)
        if (
            self._open
            and not self._floating
            and self._animation.state() != QPropertyAnimation.State.Running
        ):
            self.panel.setGeometry(self._target())
        self.bubble.raise_()
        if self._open and not self._floating:
            self.panel.raise_()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.host and event.type() == QEvent.Type.Resize:
            self.place()
        return False
