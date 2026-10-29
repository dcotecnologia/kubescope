from collections.abc import Callable, Sequence
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import (
    QBuffer,
    QByteArray,
    QIODevice,
    QMimeData,
    QPointF,
    Qt,
    QThread,
    Signal,
)
from PySide6.QtGui import QColor, QImage, QImageWriter, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from kubescope.assistant import actions, attachments, executor
from kubescope.assistant.actions import Invalid, Request
from kubescope.assistant.attachments import Attachment, AttachmentError
from kubescope.assistant.history import Entry
from kubescope.assistant.runner import COMPANY, NAME, AssistantError
from kubescope.assistant.session import ChatSession, Message
from kubescope.theme import themed
from kubescope.views.chat_icons import attach_icon, send_icon, stop_icon

SHUTDOWN_WAIT_MS = 3000
MAX_FOLLOW_UPS = 5  # reads the assistant may ask for after one question
BUBBLE_WIDTH = 0.82  # of the width of the conversation
DOODLE = 56  # the size of a tile of the pattern behind the messages


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


THUMBNAIL = 220  # width of the picture of an attached image in a bubble
FILE_FILTER = "Images and text files ({patterns});;All files (*)"


class ChatInput(QPlainTextEdit):
    """The message field: a picture pasted into it is attached, not typed."""

    image_pasted = Signal(QImage)

    def canInsertFromMimeData(self, source: QMimeData) -> bool:
        return source.hasImage() or super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source: QMimeData) -> None:
        image = source.imageData() if source.hasImage() else None
        if isinstance(image, QImage) and not image.isNull():
            self.image_pasted.emit(image)
        else:
            super().insertFromMimeData(source)


class AnswerWorker(QThread):
    """Ask the assistant and hand over the answer as it comes."""

    piece = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        session: ChatSession,
        text: str,
        screen: str = "",
        files: tuple[Attachment, ...] = (),
    ) -> None:
        super().__init__()
        self.session = session
        self.text = text
        self.screen = screen
        self.files = files
        self.stopped = False

    def run(self) -> None:
        stream = self.session.send(self.text, self.screen, self.files)
        try:
            for piece in stream:
                if self.stopped:
                    break
                self.piece.emit(piece)
        except AssistantError as error:
            self.failed.emit(str(error))
        finally:
            stream.close()  # stops the program when the answer was cut short


class ReadWorker(QThread):
    """Read the cluster for the assistant."""

    done = Signal(str)

    def __init__(self, read: Callable[[], str]) -> None:
        super().__init__()
        self.read = read

    def run(self) -> None:
        self.done.emit(self.read())


class AssistantTab(QWidget):
    """A conversation with the assistant of the system, laid out as a chat:
    what the person writes on the right, what comes back on the left.

    The assistant only asks. Navigation runs at once, a read goes back
    to it as the next message, and a change waits here for the person to
    run it.
    """

    navigate = Signal(object)  # a Request of the app, to show
    write = Signal(object)  # a Request the person confirmed
    changed = Signal()  # the conversation has a new entry to keep

    def __init__(
        self,
        session: ChatSession,
        context: str,
        write_mode: Callable[[], bool],
        fetch: Callable[[Request, str], str] = executor.fetch,
        screen: Callable[[], str] = lambda: "",
        history: Sequence[Entry] = (),
        takes_images: bool = True,
    ) -> None:
        super().__init__()
        self.session = session
        self.context = context
        self.save_name = "assistant.txt"
        self.closed = False
        self._write_mode = write_mode
        self._fetch = fetch
        self._screen = screen
        self._takes_images = takes_images
        self._pending: list[Attachment] = []  # attached, not sent yet
        self._entries: list[Entry] = []  # (role, text) of what is shown
        self._bubbles: list[QFrame] = []
        self._labels: list[QLabel] = []
        self._bubble_info: list[tuple[str, QLabel | None, str]] = []
        self._stream: QLabel | None = None  # the bubble of the answer coming in
        self._answer = ""
        self._follow_ups = 0
        self._failed = False
        self._at_end = True  # the view follows the newest message
        self._worker: AnswerWorker | None = None
        self._reader: ReadWorker | None = None

        self.thread_scroll = QScrollArea()
        self.thread_scroll.setWidgetResizable(True)
        self.thread_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.thread_view = ChatBackground()
        self.thread_layout = QVBoxLayout(self.thread_view)
        self.thread_layout.addStretch(1)
        self.welcome = QLabel(
            self.tr(
                "Hi, I'm {name}, from {company}. I know Kubernetes and KubeScope "
                "well. Ask me about what you see on the screen, ask me to look into "
                "a problem, or ask me to take you somewhere in the app."
            ).format(name=NAME, company=COMPANY)
        )
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
        self.input.setPlaceholderText(
            self.tr("Ask Gabi about the cluster or ask for an action...")
        )
        self.send_button = self._round_button(self.tr("Send"))
        self.stop_button = self._round_button(self.tr("Stop"))
        self.stop_button.setEnabled(False)
        self.stop_button.hide()
        self.attach_button = self._round_button(self.tr("Attach"))
        self.attach_button.clicked.connect(self._choose_files)
        self.input.image_pasted.connect(self.attach_image)
        self.chips = QHBoxLayout()
        self.chips.setSpacing(6)
        self.chip_bar = QWidget()
        self.chip_bar.setLayout(self.chips)
        self.chip_bar.hide()
        self.status = QLabel("")
        self.status.hide()
        self.send_button.clicked.connect(self.submit)
        self.stop_button.clicked.connect(self.stop)

        composer = QFrame()
        composer.setObjectName("assistantComposer")
        bar = QVBoxLayout(composer)
        bar.setContentsMargins(8, 6, 8, 8)
        bar.setSpacing(6)
        row = QHBoxLayout()
        row.setSpacing(6)
        row.addWidget(self.attach_button, 0, Qt.AlignmentFlag.AlignBottom)
        row.addWidget(self.input, 1)
        row.addWidget(self.send_button, 0, Qt.AlignmentFlag.AlignBottom)
        row.addWidget(self.stop_button, 0, Qt.AlignmentFlag.AlignBottom)
        self.status.setWordWrap(True)
        self.cards.setSpacing(6)
        bar.addLayout(self.cards)
        bar.addWidget(self.chip_bar)
        bar.addWidget(self.status)
        bar.addLayout(row)
        self.composer = composer
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.thread_scroll, 1)
        layout.addWidget(composer)
        self._restyle_thread()
        self._style_buttons()
        for role, text in history:
            self._entries.append((role, text))
            self._add_bubble(role, text)
            if role in ("user", "assistant"):
                self.session.messages.append(Message(role, text))  # type: ignore[arg-type]

    @staticmethod
    def _round_button(tip: str) -> QPushButton:
        button = QPushButton()
        button.setToolTip(tip)
        button.setFixedSize(40, 40)
        return button

    def _style_buttons(self) -> None:
        """Color the round buttons from the theme in use."""
        on_accent = themed("#ffffff", text=True)
        quiet = self._palette()[4]
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

    @property
    def busy(self) -> bool:
        return self._worker is not None or self._reader is not None

    def entries(self) -> list[Entry]:
        """What is shown, oldest first, for the history."""
        return list(self._entries)

    def submit(self) -> None:
        """Send what was typed."""
        text = self.input.toPlainText().strip()
        if (not text and not self._pending) or self.busy:
            return
        files, self._pending = tuple(self._pending), []
        self._refresh_chips()
        self.input.clear()
        self._follow_ups = 0
        self._ask(text or self.tr("See what is attached."), "user", text, files)

    def _choose_files(self) -> None:
        """Pick the files to attach."""
        patterns = " ".join(
            f"*{suffix}"
            for suffix in (*attachments.IMAGE_TYPES, *attachments.TEXT_TYPES)
        )
        paths, _filter = QFileDialog.getOpenFileNames(
            self,
            self.tr("Attach"),
            str(Path.home()),
            self.tr(FILE_FILTER).format(patterns=patterns),
        )
        for path in paths:
            self.attach(Path(path))

    def attach(self, path: Path) -> None:
        """Attach a file to the next question, saying why when it cannot be."""
        try:
            self._keep(attachments.load(path))
        except AttachmentError as error:
            self._show_status(str(error))

    def attach_image(self, image: QImage) -> None:
        """Attach a picture, such as one pasted from the clipboard."""
        data = QByteArray()
        buffer = QBuffer(data)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        QImageWriter(buffer, QByteArray(b"PNG")).write(image)
        number = 1 + sum(item.name.startswith("pasted-") for item in self._pending)
        try:
            if data.size() > attachments.MAX_IMAGE_BYTES:
                raise AttachmentError(self.tr("The picture is too large."))
            self._keep(
                Attachment(
                    f"pasted-{number}.png", "image", bytes(data.data()), "image/png"
                )
            )
        except AttachmentError as error:
            self._show_status(str(error))

    def _keep(self, item: Attachment) -> None:
        if len(self._pending) >= attachments.MAX_ATTACHMENTS:
            raise AttachmentError(
                self.tr("At most {count} files go with a question.").format(
                    count=attachments.MAX_ATTACHMENTS
                )
            )
        if item.kind == "image" and not self._takes_images:
            raise AttachmentError(
                self.tr("This assistant takes text files only, not {name}.").format(
                    name=item.name
                )
            )
        self._pending.append(item)
        self._refresh_chips()
        self._show_status("")

    def _refresh_chips(self) -> None:
        """Show what is attached, each with a × to take it off."""
        while (entry := self.chips.takeAt(0)) is not None:
            if (widget := entry.widget()) is not None:
                widget.deleteLater()
        _wall, own, other, ink, quiet, _tick = self._palette()
        for item in self._pending:
            chip = QFrame()
            chip.setStyleSheet(
                f"QFrame {{ background: {other}; border: 1px solid {quiet};"
                f" border-radius: 10px; }} QLabel {{ color: {ink}; border: 0; }}"
            )
            row = QHBoxLayout(chip)
            row.setContentsMargins(8, 2, 4, 2)
            row.setSpacing(4)
            row.addWidget(QLabel(item.name))
            remove = QPushButton("×")
            remove.setFixedSize(18, 18)
            remove.setStyleSheet(
                f"QPushButton {{ color: {ink}; border: 0; background: transparent; }}"
            )
            remove.clicked.connect(lambda _checked=False, one=item: self._detach(one))
            row.addWidget(remove)
            self.chips.addWidget(chip)
        self.chips.addStretch(1)
        self.chip_bar.setVisible(bool(self._pending))

    def _detach(self, item: Attachment) -> None:
        self._pending.remove(item)
        self._refresh_chips()

    def stop(self) -> None:
        if self._worker is not None:
            self._worker.stopped = True

    def note(self, text: str) -> None:
        """Say something in the conversation that the assistant does not see,
        such as how an action ended."""
        self._add_entry("app", text)
        self.changed.emit()

    @staticmethod
    def _palette() -> tuple[str, str, str, str, str, str]:
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

    def _restyle_thread(self) -> None:
        background, _own, other, ink, quiet, _tick = self._palette()
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

    def _add_entry(self, role: str, text: str) -> None:
        self._entries.append((role, text))
        self._add_bubble(role, text)

    def _add_bubble(
        self, role: str, text: str, files: tuple[Attachment, ...] = ()
    ) -> QLabel:
        """Put a bubble at the end: the person's on the right, the others on
        the left."""
        label = QLabel()
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setTextFormat(
            Qt.TextFormat.MarkdownText
            if role == "assistant"
            else Qt.TextFormat.PlainText
        )
        label.setText(text)
        label.setVisible(bool(text) or not files)
        bubble = QFrame()
        bubble.setObjectName("assistantBubbleOf" + role)
        inside = QVBoxLayout(bubble)
        inside.setContentsMargins(10, 6, 10, 4)
        inside.setSpacing(2)
        for item in files:
            inside.addWidget(self._picture(item))
        inside.addWidget(label)
        stamp = None
        if role != "app":
            stamp = QLabel()
            stamp.setTextFormat(Qt.TextFormat.RichText)
            stamp.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            inside.addWidget(stamp)
        clock = datetime.now().strftime("%H:%M")
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

    def _picture(self, item: Attachment) -> QLabel:
        """What an attachment looks like in a bubble: the image, or the name of
        the file."""
        picture = QLabel()
        pixmap = QPixmap()
        if item.kind == "image" and pixmap.loadFromData(item.data):
            picture.setPixmap(
                pixmap.scaledToWidth(
                    min(THUMBNAIL, pixmap.width()),
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            picture.setText(item.name)
        return picture

    def _style_bubble(
        self, bubble: QFrame, role: str, stamp: QLabel | None, clock: str
    ) -> None:
        """Color a bubble from the theme in use."""
        _background, own, other, ink, quiet, tick_color = self._palette()
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
        )
        if stamp is not None:
            ticks = (
                f' <span style="color: {tick_color}">✓✓</span>'
                if role == "user"
                else ""
            )
            stamp.setText(clock + ticks)
            stamp.setStyleSheet(f"font-size: 10px; color: {quiet};")

    def restyle(self) -> None:
        """Take the colors of the theme in use, for what is already shown."""
        self._restyle_thread()
        self._style_buttons()
        self._refresh_chips()
        for bubble, (role, stamp, clock) in zip(
            self._bubbles, self._bubble_info, strict=True
        ):
            self._style_bubble(bubble, role, stamp, clock)

    def _fit(self) -> None:
        """Keep the bubbles within a share of the width, so a long answer wraps
        and the sides stay visible."""
        limit = int(self.thread_scroll.viewport().width() * BUBBLE_WIDTH)
        for bubble in self._bubbles:
            bubble.setMaximumWidth(max(limit, 160))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit()

    def _follow_the_end(self, _low: int, high: int) -> None:
        """The conversation grew: stay on the newest message, unless the person
        scrolled up to read."""
        if self._at_end:
            self.thread_scroll.verticalScrollBar().setValue(high)

    def _scrolled(self, value: int) -> None:
        self._at_end = value >= self.thread_scroll.verticalScrollBar().maximum() - 2

    def _ask(
        self,
        text: str,
        role: str,
        shown: str,
        files: tuple[Attachment, ...] = (),
    ) -> None:
        kept = shown
        if files:
            names = ", ".join(item.name for item in files)
            kept = f"{shown}\n" if shown else ""
            kept += self.tr("(attached: {names})").format(names=names)
        self._entries.append((role, kept))  # the files themselves are not kept
        self._add_bubble(role, shown, files)
        self._answer = ""
        self._stream = None
        self._failed = False
        self._set_busy(True)
        self._worker = worker = AnswerWorker(self.session, text, self._screen(), files)
        worker.piece.connect(self._on_piece)
        worker.failed.connect(self._on_failed)
        worker.finished.connect(lambda: self._on_finished(worker))
        worker.start()

    def _on_piece(self, piece: str) -> None:
        self._answer += piece
        shown = actions.strip(self._answer)
        if self._stream is None:
            self._stream = self._add_bubble("assistant", shown)
        else:
            self._stream.setText(shown)

    def _drop_last_bubble(self) -> None:
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

    def _on_failed(self, message: str) -> None:
        if self._stream is not None:  # the half of an answer that came
            self._drop_last_bubble()
            self._stream = None
        self._entries.pop()  # the session took the question back
        self._drop_last_bubble()
        self._answer = ""
        self._failed = True
        self.status.setText(
            self.tr("The assistant could not answer: {message}").format(message=message)
        )

    def _on_finished(self, worker: AnswerWorker) -> None:
        self._worker = None
        answer, self._answer = self._answer, ""
        stream, self._stream = self._stream, None
        if answer and stream is not None:
            stream.setText(actions.strip(answer))
            self._entries.append(("assistant", actions.strip(answer)))
            self._act_on(answer)
        if not self._failed:
            self.changed.emit()
        if self._reader is None:
            self._set_busy(False)

    def _act_on(self, answer: str) -> None:
        reads: list[Request] = []
        for found in actions.parse(answer):
            if isinstance(found, Invalid):
                self._add_entry(
                    "app", self.tr("Ignored an action: {why}").format(why=found.reason)
                )
            elif found.action.kind == "navigate":
                self.navigate.emit(found)
            elif found.action.kind == "write" and not self._write_mode():
                self._add_entry(
                    "app",
                    self.tr(
                        "Read-only mode: nothing was changed. Turn on the write mode "
                        "in Settings to allow {what}."
                    ).format(what=actions.describe(found)),
                )
            elif found.action.kind == "write":
                self._add_card(found)
            else:
                reads.append(found)
        if reads:
            self._read(reads[0])

    def _read(self, request: Request) -> None:
        if self._follow_ups >= MAX_FOLLOW_UPS:
            self._add_entry(
                "app", self.tr("Stopped reading: too many reads for one question.")
            )
            return
        self._follow_ups += 1
        self._reader = reader = ReadWorker(lambda: self._fetch(request, self.context))
        reader.done.connect(lambda message: self._on_read(request, message))
        reader.finished.connect(lambda: setattr(self, "_reader", None))
        reader.start()

    def _on_read(self, request: Request, message: str) -> None:
        self._reader = None
        self._ask(
            message,
            "app",
            self.tr("(read) {what}").format(what=actions.describe(request)),
        )

    def _add_card(self, request: Request) -> None:
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(card)
        label = QLabel(actions.describe(request))
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setWordWrap(True)
        run = QPushButton(self.tr("Run"))
        cancel = QPushButton(self.tr("Cancel"))
        layout.addWidget(label, 1)
        layout.addWidget(run)
        layout.addWidget(cancel)
        run.clicked.connect(lambda: self._confirm(card, request))
        cancel.clicked.connect(lambda: self._dismiss(card))
        self.cards.addWidget(card)

    def _confirm(self, card: QWidget, request: Request) -> None:
        self._dismiss(card)
        self.write.emit(request)

    def _dismiss(self, card: QWidget) -> None:
        self.cards.removeWidget(card)
        card.deleteLater()

    def _show_status(self, text: str) -> None:
        """Say what is going on, taking no room when there is nothing to
        say."""
        self.status.setText(text)
        self.status.setVisible(bool(text))

    def _set_busy(self, busy: bool) -> None:
        self.send_button.setEnabled(not busy)
        self.stop_button.setEnabled(busy)
        self.send_button.setVisible(not busy)
        self.stop_button.setVisible(busy)
        if busy:
            self._show_status(self.tr("Thinking..."))
        elif not self._failed:
            self._show_status("")

    def markdown(self) -> str:
        """The conversation, to read or to save."""
        who = {
            "user": self.tr("You"),
            "assistant": NAME,
            "app": self.tr("App"),
        }
        turns = list(self._entries)
        if self._stream is not None and self._answer:
            turns.append(("assistant", actions.strip(self._answer)))
        return "\n\n".join(f"**{who[role]}**\n\n{text}" for role, text in turns)

    def shutdown(self) -> None:
        """Stop what is running, before the tab goes."""
        self.closed = True
        for worker in (self._worker, self._reader):
            if worker is not None:
                if isinstance(worker, AnswerWorker):
                    worker.stopped = True
                worker.wait(SHUTDOWN_WAIT_MS)
