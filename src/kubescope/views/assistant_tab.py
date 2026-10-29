from collections.abc import Callable

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from kubescope.assistant import actions, executor
from kubescope.assistant.actions import Invalid, Request
from kubescope.assistant.runner import AssistantError
from kubescope.assistant.session import ChatSession

SHUTDOWN_WAIT_MS = 3000
MAX_FOLLOW_UPS = 5  # reads the assistant may ask for after one question


class AnswerWorker(QThread):
    """Ask the assistant and hand over the answer as it comes."""

    piece = Signal(str)
    failed = Signal(str)

    def __init__(self, session: ChatSession, text: str) -> None:
        super().__init__()
        self.session = session
        self.text = text
        self.stopped = False

    def run(self) -> None:
        stream = self.session.send(self.text)
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
    """A conversation with the assistant of the system.

    The assistant only asks. Navigation runs at once, a read goes back
    to it as the next message, and a change waits here for the person to
    run it.
    """

    navigate = Signal(object)  # a Request of the app, to show
    write = Signal(object)  # a Request the person confirmed

    def __init__(
        self,
        session: ChatSession,
        context: str,
        write_mode: Callable[[], bool],
        fetch: Callable[[Request, str], str] = executor.fetch,
    ) -> None:
        super().__init__()
        self.session = session
        self.context = context
        self.save_name = "assistant.md"
        self.closed = False
        self._write_mode = write_mode
        self._fetch = fetch
        self._shown: list[tuple[str, str]] = []  # who said what, for the view
        self._answer = ""
        self._follow_ups = 0
        self._failed = False
        self._worker: AnswerWorker | None = None
        self._reader: ReadWorker | None = None

        self.transcript = QTextBrowser()
        self.transcript.setOpenExternalLinks(False)
        self.cards = QVBoxLayout()
        self.input = QPlainTextEdit()
        self.input.setMaximumHeight(90)
        self.input.setPlaceholderText(
            self.tr("Ask about the cluster or ask for an action...")
        )
        self.send_button = QPushButton(self.tr("Send"))
        self.stop_button = QPushButton(self.tr("Stop"))
        self.stop_button.setEnabled(False)
        self.status = QLabel("")
        self.send_button.clicked.connect(self.submit)
        self.stop_button.clicked.connect(self.stop)

        buttons = QVBoxLayout()
        buttons.addWidget(self.send_button)
        buttons.addWidget(self.stop_button)
        row = QHBoxLayout()
        row.addWidget(self.input, 1)
        row.addLayout(buttons)
        layout = QVBoxLayout(self)
        layout.addWidget(self.transcript, 1)
        layout.addLayout(self.cards)
        layout.addWidget(self.status)
        layout.addLayout(row)

    @property
    def busy(self) -> bool:
        return self._worker is not None or self._reader is not None

    def submit(self) -> None:
        """Send what was typed."""
        text = self.input.toPlainText().strip()
        if not text or self.busy:
            return
        self.input.clear()
        self._follow_ups = 0
        self._ask(text, text)

    def stop(self) -> None:
        if self._worker is not None:
            self._worker.stopped = True

    def note(self, text: str) -> None:
        """Say something in the conversation that the assistant does not see,
        such as how an action ended."""
        self._shown.append((self.tr("App"), text))
        self._render()

    def _ask(self, text: str, shown: str) -> None:
        self._shown.append((self.tr("You"), shown))
        self._answer = ""
        self._failed = False
        self._set_busy(True)
        self._worker = worker = AnswerWorker(self.session, text)
        worker.piece.connect(self._on_piece)
        worker.failed.connect(self._on_failed)
        worker.finished.connect(lambda: self._on_finished(worker))
        worker.start()

    def _on_piece(self, piece: str) -> None:
        self._answer += piece
        self._render()

    def _on_failed(self, message: str) -> None:
        self._shown.pop()  # the session took the question back
        self._answer = ""
        self._failed = True
        self.status.setText(
            self.tr("The assistant could not answer: {message}").format(message=message)
        )

    def _on_finished(self, worker: AnswerWorker) -> None:
        self._worker = None
        answer, self._answer = self._answer, ""
        if answer:
            self._shown.append((self.tr("Assistant"), actions.strip(answer)))
            self._act_on(answer)
        self._render()
        if self._reader is None:
            self._set_busy(False)

    def _act_on(self, answer: str) -> None:
        reads: list[Request] = []
        for found in actions.parse(answer):
            if isinstance(found, Invalid):
                self.note(self.tr("Ignored an action: {why}").format(why=found.reason))
            elif found.action.kind == "navigate":
                self.navigate.emit(found)
            elif found.action.kind == "write":
                self._add_card(found)
            else:
                reads.append(found)
        if reads:
            self._read(reads[0])

    def _read(self, request: Request) -> None:
        if self._follow_ups >= MAX_FOLLOW_UPS:
            self.note(self.tr("Stopped reading: too many reads for one question."))
            return
        self._follow_ups += 1
        self._reader = reader = ReadWorker(lambda: self._fetch(request, self.context))
        reader.done.connect(lambda message: self._on_read(request, message))
        reader.finished.connect(lambda: setattr(self, "_reader", None))
        reader.start()

    def _on_read(self, request: Request, message: str) -> None:
        self._reader = None
        self._ask(
            message, self.tr("(read) {what}").format(what=actions.describe(request))
        )

    def _add_card(self, request: Request) -> None:
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(card)
        allowed = self._write_mode()
        text = actions.describe(request)
        if not allowed:
            text += "\n" + self.tr("The write mode is off; turn it on in Settings.")
        label = QLabel(text)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setWordWrap(True)
        run = QPushButton(self.tr("Run"))
        run.setEnabled(allowed)
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

    def _set_busy(self, busy: bool) -> None:
        self.send_button.setEnabled(not busy)
        self.stop_button.setEnabled(busy)
        if busy:
            self.status.setText(self.tr("Thinking..."))
        elif not self._failed:
            self.status.setText("")

    def markdown(self) -> str:
        """The conversation, to show or to save."""
        turns = list(self._shown)
        if self._answer:
            turns.append((self.tr("Assistant"), actions.strip(self._answer)))
        return "\n\n".join(f"**{who}**\n\n{text}" for who, text in turns)

    def _render(self) -> None:
        bar = self.transcript.verticalScrollBar()
        at_end = bar.value() >= bar.maximum() - 2
        self.transcript.setMarkdown(self.markdown())
        if at_end:
            bar.setValue(bar.maximum())

    def shutdown(self) -> None:
        """Stop what is running, before the tab goes."""
        self.closed = True
        for worker in (self._worker, self._reader):
            if worker is not None:
                if isinstance(worker, AnswerWorker):
                    worker.stopped = True
                worker.wait(SHUTDOWN_WAIT_MS)
