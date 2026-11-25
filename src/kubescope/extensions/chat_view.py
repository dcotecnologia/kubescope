"""The window of a chat with an assistant: the conversation as bubbles, the
message field with its buttons, what is attached and the ring that says how
full the conversation is (`kubescope.sdk.Components.chat_view`).

It draws and reports what the person does; what the assistant answers is
the extension's.
"""

import tempfile
from collections.abc import Callable, Sequence
from math import ceil
from pathlib import Path
from typing import Protocol

from PySide6.QtCore import (
    QBuffer,
    QByteArray,
    QIODevice,
    QMimeData,
    QPointF,
    QRectF,
    QSize,
    Qt,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QDesktopServices,
    QImage,
    QImageWriter,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QResizeEvent,
    QWheelEvent,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from kubescope.extensions.icons import (
    chat_attach_icon as attach_icon,
)
from kubescope.extensions.icons import (
    chat_send_icon as send_icon,
)
from kubescope.extensions.icons import (
    chat_stop_icon as stop_icon,
)
from kubescope.theme import themed

BUBBLE_WIDTH = 0.82  # of the width of the conversation
DOODLE = 56  # the size of a tile of the pattern behind the messages
FILE_FILTER = "Images and text files ({patterns});;All files (*)"


class Attached(Protocol):
    """What the chat needs of a file attached to a message."""

    name: str
    kind: str  # `image` or `text`
    data: bytes

    @property
    def text(self) -> str: ...


class ChatBackground(QWidget):
    """The wall behind the messages: a plain color with a faint pattern, like a
    chat of a phone."""

    def __init__(self) -> None:
        super().__init__()
        self.color = QColor(themed("#f7f7fa"))
        self.ink = QColor(themed("#6b7380"))

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), self.color)
        faint = QColor(self.ink)
        faint.setAlpha(26)
        painter.setPen(QPen(faint, 1.4))
        for row in range(0, self.height() // DOODLE + 1):
            for column in range(0, self.width() // DOODLE + 1):
                x = column * DOODLE + (DOODLE // 2 if row % 2 else 0)
                y = row * DOODLE
                shape = (row + column) % 3
                if shape == 0:
                    painter.drawEllipse(QPointF(x + 14, y + 14), 5, 5)
                elif shape == 1:
                    painter.drawLine(QPointF(x + 8, y + 14), QPointF(x + 20, y + 14))
                    painter.drawLine(QPointF(x + 14, y + 8), QPointF(x + 14, y + 20))
                else:
                    painter.drawRect(int(x + 9), int(y + 9), 10, 10)


CARD = 88  # the side of the card of an attachment, above the message field
PILL_THUMB = 18  # the side of the small picture in the pill of a sent message
LONG_PASTE = 2000  # a pasted text this long is attached as a file, not typed


class MessageText(QTextBrowser):
    """The text of a message, as high as the text is and as wide as the text
    needs up to the room it has.

    A label that wraps its text guesses how wide to be and can draw the
    text in a size other than the one it measured; this one measures and
    draws the same document, and the person can select what is in it.
    """

    def __init__(self, markdown: bool) -> None:
        super().__init__()
        self._markdown = markdown
        self._text = ""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setOpenExternalLinks(True)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(24)
        self.document().setDocumentMargin(0)
        self.setStyleSheet("QTextBrowser { background: transparent; border: 0; }")

    def text(self) -> str:
        return self._text

    def textFormat(self) -> Qt.TextFormat:
        return Qt.TextFormat.MarkdownText if self._markdown else Qt.TextFormat.PlainText

    def setText(self, text: str) -> None:
        self._text = text
        if self._markdown:
            self.setMarkdown(text)
        else:
            self.setPlainText(text)
        self._fit()
        self.updateGeometry()

    def _fit(self) -> None:
        """Make it as high as its text is at the width it has."""
        width = self.viewport().width()
        document = self.document()
        document.setTextWidth(width if width > 0 else -1)
        self.setFixedHeight(max(ceil(document.size().height()), 1))

    def sizeHint(self) -> QSize:
        """As wide as the text is when it is not wrapped, and as high as it is
        then."""
        document = self.document()
        document.setTextWidth(-1)
        width = ceil(document.idealWidth()) + 1
        height = ceil(document.size().height())
        self._fit()  # back to the width it has
        return QSize(width, height)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._fit()

    def wheelEvent(self, event: QWheelEvent) -> None:
        event.ignore()  # the conversation is the one that scrolls


class ClickableFrame(QFrame):
    """A frame that can be clicked, like an attachment."""

    clicked = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
            event.position().toPoint()
        ):
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class ChatInput(QPlainTextEdit):
    """The message field: a picture pasted into it is attached, not typed, and
    Enter sends the message, while Shift+Enter goes to the next line."""

    image_pasted = Signal(QImage)
    files_pasted = Signal(object)  # the paths of files pasted from a file manager
    text_pasted = Signal(str)  # a long text, to attach instead of typing
    submitted = Signal()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        enter = event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)
        if enter and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.submitted.emit()
            return
        super().keyPressEvent(event)

    def canInsertFromMimeData(self, source: QMimeData) -> bool:
        return (
            source.hasImage()
            or source.hasUrls()
            or super().canInsertFromMimeData(source)
        )

    def insertFromMimeData(self, source: QMimeData) -> None:
        image = source.imageData() if source.hasImage() else None
        paths = [Path(url.toLocalFile()) for url in source.urls() if url.isLocalFile()]
        if isinstance(image, QImage) and not image.isNull():
            self.image_pasted.emit(image)
        elif paths:
            self.files_pasted.emit(paths)
        elif source.hasText() and len(source.text()) >= LONG_PASTE:
            self.text_pasted.emit(source.text())
        else:
            super().insertFromMimeData(source)


class ContextRing(QWidget):
    """A small ring that fills as the conversation grows toward the point where
    it is compacted; a click asks for its menu."""

    clicked = Signal()
    SIZE = 18

    def __init__(self) -> None:
        super().__init__()
        self.fraction = 0.0
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_fraction(self, fraction: float) -> None:
        self.fraction = min(max(fraction, 0.0), 1.0)
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        area = QRectF(3, 3, self.SIZE - 6, self.SIZE - 6)
        track = QColor(themed("#6b7380", text=True))
        track.setAlpha(80)
        painter.setPen(QPen(track, 2.0))
        painter.drawEllipse(area)
        if self.fraction <= 0:
            return
        if self.fraction >= 1.0:
            color = themed("#a33d45", text=True)  # about to be compacted
        elif self.fraction >= 0.75:
            color = themed("#985415", text=True)
        else:
            color = themed("#6c5fc4")
        pen = QPen(QColor(color), 2.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(area, 90 * 16, -round(360 * 16 * self.fraction))

    def mouseReleaseEvent(self, event) -> None:
        self.clicked.emit()


class ChatView(QWidget):
    """The conversation laid out as a chat: what the person writes on the
    right, what comes back on the left, and the composer under it.

    `texts` are its words in the language of the app, by their English text
    (the welcome, the placeholder of the field, the tips of the buttons...).
    The signals say what the person does: `submitted` (Enter or Send),
    `stop_requested`, `attach_requested`, `image_pasted`, `files_pasted`,
    `text_pasted` and `ring_clicked`.
    """

    submitted = Signal()
    stop_requested = Signal()
    attach_requested = Signal()
    image_pasted = Signal(bytes)  # the PNG of a picture pasted into the field
    files_pasted = Signal(object)  # the paths of files pasted from a file manager
    text_pasted = Signal(str)  # a long text, to attach instead of typing
    ring_clicked = Signal()
    usage_expired = Signal()  # the cache of the prompt is over: say it again

    def __init__(self, texts: dict[str, str]) -> None:
        super().__init__()
        self._texts = dict(texts)
        self._opened: tempfile.TemporaryDirectory[str] | None = None
        self._bubbles: list[QFrame] = []
        self._labels: list[MessageText] = []
        self._bubble_info: list[tuple[str, QLabel | None, str]] = []
        self._at_end = True  # the view follows the newest message
        self._chips: list[Attached] = []
        self._chip_handlers: tuple[
            Callable[[Attached], None], Callable[[Attached], None]
        ] = (lambda _i: None, lambda _i: None)

        self.thread_scroll = QScrollArea()
        self.thread_scroll.setWidgetResizable(True)
        self.thread_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.thread_view = ChatBackground()
        self.thread_layout = QVBoxLayout(self.thread_view)
        self.thread_layout.addStretch(1)
        self.welcome = QLabel(self._t("welcome"))
        self.welcome.setWordWrap(True)
        self.welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thread_layout.insertWidget(0, self.welcome)  # until the first message
        self.thread_scroll.setWidget(self.thread_view)
        bar = self.thread_scroll.verticalScrollBar()
        bar.rangeChanged.connect(self._follow_the_end)
        bar.valueChanged.connect(self._scrolled)
        self.cards = QVBoxLayout()
        self.input = ChatInput()
        self.input.setObjectName("assistantInput")
        self.input.setMaximumHeight(72)
        self.input.setMinimumHeight(40)
        self.input.setPlaceholderText(self._t("placeholder"))
        self.send_button = self._round_button(self._t("Send"))
        self.stop_button = self._round_button(self._t("Stop"))
        self.stop_button.setEnabled(False)
        self.stop_button.hide()
        self.attach_button = self._round_button(self._t("Attach"))
        self.attach_button.clicked.connect(self.attach_requested)
        self.input.image_pasted.connect(self._image_pasted)
        self.input.files_pasted.connect(self.files_pasted)
        self.input.text_pasted.connect(self.text_pasted)
        self.input.submitted.connect(self.submitted)
        self.chips = QHBoxLayout()
        self.chips.setSpacing(6)
        self.chip_bar = QWidget()
        self.chip_bar.setLayout(self.chips)
        self.chip_bar.hide()
        self.status = QLabel("")
        self.status.hide()
        self.usage_label = QLabel("")  # the tokens, under the box of the question
        self.usage_label.setObjectName("assistantUsage")
        self.usage_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        # the color of the placeholder of the box above it
        self.usage_label.setStyleSheet("QLabel { color: palette(placeholder-text); }")
        self.usage_label.hide()
        self.ring = ContextRing()
        self.ring.hide()
        self.ring.clicked.connect(self.ring_clicked)
        self._cache_timer = QTimer(self)  # tells when the cache of the prompt expires
        self._cache_timer.setSingleShot(True)
        self._cache_timer.timeout.connect(self.usage_expired)
        self.send_button.clicked.connect(self.submitted)
        self.stop_button.clicked.connect(self.stop_requested)

        composer = QFrame()
        composer.setObjectName("assistantComposer")
        column = QVBoxLayout(composer)
        column.setContentsMargins(8, 6, 8, 8)
        column.setSpacing(6)
        row = QHBoxLayout()
        row.setSpacing(6)
        row.addWidget(self.attach_button, 0, Qt.AlignmentFlag.AlignBottom)
        row.addWidget(self.input, 1)
        row.addWidget(self.send_button, 0, Qt.AlignmentFlag.AlignBottom)
        row.addWidget(self.stop_button, 0, Qt.AlignmentFlag.AlignBottom)
        self.status.setWordWrap(True)
        self.cards.setSpacing(6)
        column.addLayout(self.cards)
        column.addWidget(self.chip_bar)
        column.addWidget(self.status)
        column.addLayout(row)
        usage_row = QHBoxLayout()
        usage_row.setSpacing(6)
        usage_row.addStretch(1)
        usage_row.addWidget(self.usage_label)
        usage_row.addWidget(self.ring)
        column.addLayout(usage_row)
        self.composer = composer
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.thread_scroll, 1)
        layout.addWidget(composer)
        self._restyle_thread()
        self._style_buttons()

    def _t(self, text: str) -> str:
        """A text of the chat in the language of the app, as the extension gave
        it."""
        return self._texts.get(text, text)

    def set_texts(self, texts: dict[str, str]) -> None:
        """The language changed: say it again in the new words."""
        self._texts = dict(texts)
        self.welcome.setText(self._t("welcome"))
        self.input.setPlaceholderText(self._t("placeholder"))
        self.send_button.setToolTip(self._t("Send"))
        self.stop_button.setToolTip(self._t("Stop"))
        self.attach_button.setToolTip(self._t("Attach"))

    @staticmethod
    def _round_button(tip: str) -> QPushButton:
        button = QPushButton()
        button.setToolTip(tip)
        button.setFixedSize(40, 40)
        return button

    def _image_pasted(self, image: QImage) -> None:
        data = QByteArray()
        buffer = QBuffer(data)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        QImageWriter(buffer, QByteArray(b"PNG")).write(image)
        self.image_pasted.emit(bytes(data.data()))

    # ----- colors

    @staticmethod
    def colors() -> tuple[str, str, str, str, str, str]:
        """The colors of the chat, from the theme in use: the wall, the
        person's bubble, the other bubbles, the text, the quiet text and the
        ticks."""
        return (
            themed("#f7f7fa"),
            themed("#e5f4eb"),
            themed("#ffffff"),
            themed("#20232a"),
            themed("#6b7380"),
            themed("#176b58"),
        )

    def _style_buttons(self) -> None:
        """Color the round buttons from the theme in use."""
        on_accent = themed("#ffffff", text=True)
        quiet = self.colors()[4]
        solid = (
            (self.send_button, send_icon(on_accent), themed("#3020a5")),
            (self.stop_button, stop_icon(on_accent), themed("#a33d45")),
        )
        for button, icon, color in solid:
            button.setIcon(icon)
            button.setStyleSheet(
                f"QPushButton {{ background: {color}; border: 0;"
                " border-radius: 20px; }"
                f"QPushButton:disabled {{ background: {themed('#6c5fc4')}; }}"
            )
        self.attach_button.setIcon(attach_icon(quiet))
        self.attach_button.setStyleSheet(
            "QPushButton { background: transparent; border: 0;"
            " border-radius: 20px; }"
            f"QPushButton:hover {{ background: {themed('#eceef3')}; }}"
        )

    def _restyle_thread(self) -> None:
        background, _own, other, ink, quiet, _tick = self.colors()
        self.thread_view.color = QColor(background)
        self.thread_view.ink = QColor(quiet)
        self.thread_view.update()
        self.composer.setStyleSheet(
            f"QFrame#assistantComposer {{ background: {background}; }}"
        )
        self.welcome.setStyleSheet(
            f"QLabel {{ background: {other}; color: {quiet}; border-radius: 10px;"
            " padding: 12px 16px; }"
        )
        self.input.setStyleSheet(
            f"QPlainTextEdit#assistantInput {{ background: {other}; color: {ink};"
            " border: 0; border-radius: 18px; padding: 6px 12px; }"
        )

    def restyle(self) -> None:
        """Take the colors of the theme in use, for what is already shown."""
        self._restyle_thread()
        self._style_buttons()
        self.show_chips(self._chips, *self._chip_handlers)
        for bubble, (role, stamp, clock) in zip(
            self._bubbles, self._bubble_info, strict=True
        ):
            self._style_bubble(bubble, role, stamp, clock)

    # ----- the composer

    def set_busy(self, busy: bool) -> None:
        """While the assistant answers, Send is Stop."""
        self.send_button.setEnabled(not busy)
        self.stop_button.setEnabled(busy)
        self.send_button.setVisible(not busy)
        self.stop_button.setVisible(busy)

    def show_status(self, text: str) -> None:
        """Say what is going on, taking no room when there is nothing to
        say."""
        self.status.setText(text)
        self.status.setVisible(bool(text))

    def set_usage(
        self, text: str, tip: str, fraction: float, ring_tip: str, expires_in: int
    ) -> None:
        """Say what the session used in tokens, under the box of the question;
        the line is made again `expires_in` ms later (0: never)."""
        self.usage_label.setText(text)
        self.usage_label.setToolTip(tip)
        self.usage_label.setVisible(bool(text))
        self.ring.setVisible(bool(text))
        self.ring.set_fraction(fraction)
        self.ring.setToolTip(ring_tip)
        if expires_in:
            self._cache_timer.start(expires_in)
        else:
            self._cache_timer.stop()

    def show_ring_menu(
        self,
        lines: Sequence[str],
        compact_text: str,
        can_compact: bool,
        on_compact: Callable[[], None],
        auto_text: str,
        auto_on: bool,
        on_auto: Callable[[bool], None],
    ) -> QMenu:
        """The menu of the ring: what it tells, a way to compact now and a
        switch to compact by itself."""
        menu = QMenu(self)
        for line in lines:
            if line:
                menu.addAction(line).setEnabled(False)
        menu.addSeparator()
        now = menu.addAction(compact_text)
        now.setEnabled(can_compact)
        now.triggered.connect(on_compact)
        auto = menu.addAction(auto_text)
        auto.setCheckable(True)
        auto.setChecked(auto_on)
        auto.toggled.connect(on_auto)
        menu.popup(self.ring.mapToGlobal(self.ring.rect().bottomLeft()))
        return menu

    def add_action_card(
        self,
        text: str,
        run_text: str,
        cancel_text: str,
        on_run: Callable[[], None],
        on_cancel: Callable[[], None],
    ) -> QFrame:
        """A change the assistant asked for, which waits for the person to run
        it or to dismiss it."""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(card)
        label = QLabel(text)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setWordWrap(True)
        run = QPushButton(run_text)
        cancel = QPushButton(cancel_text)
        layout.addWidget(label, 1)
        layout.addWidget(run)
        layout.addWidget(cancel)
        run.clicked.connect(lambda: on_run())
        cancel.clicked.connect(lambda: on_cancel())
        self.cards.addWidget(card)
        return card

    def remove_card(self, card: QWidget) -> None:
        self.cards.removeWidget(card)
        card.deleteLater()

    # ----- what is attached

    def choose_files(self, title: str, patterns: str) -> list[Path]:
        """Ask the person which files to attach."""
        paths, _filter = QFileDialog.getOpenFileNames(
            self,
            title,
            str(Path.home()),
            self._t(FILE_FILTER).format(patterns=patterns),
        )
        return [Path(path) for path in paths]

    def show_chips(
        self,
        items: Sequence[Attached],
        on_open: Callable[[Attached], None],
        on_detach: Callable[[Attached], None],
    ) -> None:
        """Show what is attached, each with a × to take it off."""
        self._chips = list(items)
        self._chip_handlers = (on_open, on_detach)
        while (entry := self.chips.takeAt(0)) is not None:
            if (widget := entry.widget()) is not None:
                widget.deleteLater()
        for item in items:
            self.chips.addWidget(self._card(item, on_open, on_detach))
        self.chips.addStretch(1)
        self.chip_bar.setVisible(bool(items))

    def open_attachment(self, item: Attached) -> str:
        """Open an attachment with the program the system uses for its kind;
        the text of why not, or an empty one.

        Attachments are not kept, so a copy goes to a folder that lives
        as long as this chat.
        """
        if self._opened is None:
            self._opened = tempfile.TemporaryDirectory(prefix="kubescope-")
        path = Path(self._opened.name) / Path(item.name).name
        try:
            path.write_bytes(item.data)
            path.chmod(0o600)
        except OSError as error:
            return str(error.strerror or error)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        return ""

    @staticmethod
    def _rounded(pixmap: QPixmap, side: int, radius: int) -> QPixmap:
        """The picture cropped to a square with rounded corners."""
        scaled = pixmap.scaled(
            side,
            side,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        result = QPixmap(side, side)
        result.fill(Qt.GlobalColor.transparent)
        painter = QPainter(result)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        clip = QPainterPath()
        clip.addRoundedRect(0, 0, side, side, radius, radius)
        painter.setClipPath(clip)
        painter.drawPixmap(
            (side - scaled.width()) // 2, (side - scaled.height()) // 2, scaled
        )
        painter.end()
        return result

    def _card(
        self,
        item: Attached,
        on_open: Callable[[Attached], None],
        on_detach: Callable[[Attached], None],
    ) -> QFrame:
        """An attachment above the message field: the picture of an image, or
        the first lines of a text, with a × to take it off."""
        _wall, _own, other, ink, quiet, _tick = self.colors()
        card = ClickableFrame()
        card.clicked.connect(lambda one=item: on_open(one))
        card.setFixedSize(CARD, CARD)
        card.setToolTip(self._t("Open {name}").format(name=item.name))
        card.setStyleSheet(
            f"QFrame {{ background: {other}; border: 1px solid {quiet};"
            f" border-radius: 10px; }} QLabel {{ color: {ink}; border: 0;"
            " background: transparent; }"
        )
        pixmap = QPixmap()
        if item.kind == "image" and pixmap.loadFromData(item.data):
            picture = QLabel(card)
            picture.setPixmap(self._rounded(pixmap, CARD, 10))
            picture.setGeometry(0, 0, CARD, CARD)
        else:
            lines = item.text.splitlines()[:5]
            preview = QLabel("\n".join(line[:18] for line in lines), card)
            preview.setStyleSheet(f"color: {quiet}; font-size: 8px;")
            preview.setGeometry(8, 6, CARD - 16, CARD - 30)
            preview.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            name = QLabel(
                card.fontMetrics().elidedText(
                    item.name, Qt.TextElideMode.ElideMiddle, CARD - 16
                ),
                card,
            )
            name.setStyleSheet("font-size: 10px; font-weight: bold;")
            name.setGeometry(8, CARD - 22, CARD - 16, 16)
        remove = QPushButton("×", card)
        remove.setFixedSize(18, 18)
        remove.move(CARD - 22, 4)
        remove.setStyleSheet(
            f"QPushButton {{ color: {ink}; background: {other}; border: 1px solid"
            f" {quiet}; border-radius: 9px; padding: 0; }}"
        )
        remove.clicked.connect(lambda _checked=False, one=item: on_detach(one))
        return card

    # ----- the conversation

    def add_bubble(
        self,
        role: str,
        text: str,
        clock: str,
        files: Sequence[Attached] = (),
        on_open: Callable[[Attached], None] = lambda _item: None,
    ) -> MessageText:
        """Put a bubble at the end: the person's on the right, the others on
        the left."""
        label = MessageText(markdown=role == "assistant")
        label.setText(text)
        label.setVisible(bool(text) or not files)
        bubble = QFrame()
        bubble.setObjectName("assistantBubbleOf" + role)
        inside = QVBoxLayout(bubble)
        inside.setContentsMargins(10, 6, 10, 4)
        inside.setSpacing(2)
        for item in files:
            inside.addWidget(self._picture(item, on_open))
        inside.addWidget(label)
        stamp = None
        if role != "app":
            stamp = QLabel()
            stamp.setTextFormat(Qt.TextFormat.RichText)
            stamp.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            inside.addWidget(stamp)
        self._style_bubble(bubble, role, stamp, clock)
        line = QHBoxLayout()
        line.setContentsMargins(8, 2, 8, 2)
        if role == "user":
            line.addStretch(1)
            line.addWidget(bubble)
        else:
            line.addWidget(bubble)
            line.addStretch(1)
        self.thread_layout.insertLayout(self.thread_layout.count() - 1, line)
        self.welcome.hide()
        self._bubbles.append(bubble)
        self._labels.append(label)
        self._bubble_info.append((role, stamp, clock))
        self._fit()
        return label

    def drop_last_bubble(self) -> None:
        if self._bubbles:
            self._bubbles.pop().parentWidget()
            label = self._labels.pop()
            self._bubble_info.pop()
            self.welcome.setVisible(not self._bubbles)
            frame = label.parentWidget()
            assert frame is not None
            line = self.thread_layout.itemAt(self.thread_layout.count() - 2)
            assert line is not None
            self.thread_layout.removeItem(line)
            frame.deleteLater()

    def _picture(self, item: Attached, on_open: Callable[[Attached], None]) -> QFrame:
        """What an attachment looks like in a sent message: a pill with a small
        picture, the name and what it holds (the size of an image, the lines of
        a text)."""
        pill = ClickableFrame()
        pill.clicked.connect(lambda one=item: on_open(one))
        pill.setObjectName("attachmentPill")
        row = QHBoxLayout(pill)
        row.setContentsMargins(6, 3, 8, 3)
        row.setSpacing(6)
        pixmap = QPixmap()
        icon = QLabel()
        if item.kind == "image" and pixmap.loadFromData(item.data):
            icon.setPixmap(self._rounded(pixmap, PILL_THUMB, 4))
            detail = f"{pixmap.width()}×{pixmap.height()}"
        else:
            icon.setPixmap(
                self.style()
                .standardIcon(self.style().StandardPixmap.SP_FileIcon)
                .pixmap(PILL_THUMB, PILL_THUMB)
            )
            detail = self._t("{count} lines").format(count=len(item.data.splitlines()))
        name = QLabel(item.name)
        name.setStyleSheet("font-weight: bold;")
        meta = QLabel(detail)
        meta.setObjectName("attachmentMeta")
        for widget in (icon, name, meta):
            row.addWidget(widget)
        pill.setToolTip(self._t("Open {name}").format(name=item.name))
        pill.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        return pill

    def _style_bubble(
        self, bubble: QFrame, role: str, stamp: QLabel | None, clock: str
    ) -> None:
        """Color a bubble from the theme in use."""
        _background, own, other, ink, quiet, tick_color = self.colors()
        color = own if role == "user" else other
        edge = f"border: 1px dashed {quiet};" if role == "app" else ""
        text_color = quiet if role == "app" else ink
        name = f"QFrame#assistantBubbleOf{role}"
        tail = (
            "border-top-right-radius: 2px;"
            if role == "user"
            else "border-top-left-radius: 2px;"
        )
        bubble.setStyleSheet(
            f"{name} {{ background: {color}; {edge} border-radius: 10px; {tail} }}"
            f"{name} QLabel {{ color: {text_color}; background: transparent; }}"
            f"{name} QTextBrowser {{ color: {text_color}; background: transparent; }}"
            f"{name} QFrame#attachmentPill {{ background: rgba(0, 0, 0, 40);"
            f" border: 1px solid {quiet}; border-radius: 6px; }}"
            f"{name} QLabel#attachmentMeta {{ color: {quiet}; }}"
        )
        if stamp is not None:
            ticks = (
                f' <span style="color: {tick_color}">✓✓</span>'
                if role == "user"
                else ""
            )
            stamp.setText(clock + ticks)
            stamp.setStyleSheet(f"font-size: 10px; color: {quiet};")

    def _fit(self) -> None:
        """Keep the bubbles within a share of the width, so a long answer wraps
        and the sides stay visible."""
        limit = int(self.thread_scroll.viewport().width() * BUBBLE_WIDTH)
        for bubble in self._bubbles:
            bubble.setMaximumWidth(max(limit, 160))

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._fit()

    def _follow_the_end(self, _low: int, high: int) -> None:
        """The conversation grew: stay on the newest message, unless the person
        scrolled up to read."""
        if self._at_end:
            self.thread_scroll.verticalScrollBar().setValue(high)

    def _scrolled(self, value: int) -> None:
        self._at_end = value >= self.thread_scroll.verticalScrollBar().maximum() - 2
