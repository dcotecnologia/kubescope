"""A conversation with an assistant.

The programs answer one question each, so the session sends the whole
conversation every time. It works the same with any of them and the app
decides what leaves the machine. When the conversation is longer than
the limit, the oldest messages are left out.
"""

from collections.abc import Generator
from dataclasses import dataclass
from typing import Literal

from kubescope.assistant import runner
from kubescope.assistant.runner import Assistant, AssistantError

HISTORY_LIMIT = 40_000  # characters of the conversation that are sent

Role = Literal["user", "assistant"]
_LABELS: dict[Role, str] = {"user": "User", "assistant": "Assistant"}


@dataclass(frozen=True, slots=True)
class Message:
    role: Role
    text: str


class ChatSession:
    def __init__(
        self,
        assistant: Assistant,
        model: str | None = None,
        system: str = runner.SYSTEM_PROMPT,
        limit: int = HISTORY_LIMIT,
    ) -> None:
        self.assistant = assistant
        self.model = model
        self.system = system
        self.limit = limit
        self.messages: list[Message] = []

    def prompt(self) -> str:
        """The conversation to send: the newest messages that fit, and the last
        one is always there."""
        kept: list[Message] = []
        size = 0
        for message in reversed(self.messages):
            size += len(message.text)
            if kept and size > self.limit:
                break
            kept.append(message)
        turns = "\n\n".join(
            f"{_LABELS[message.role]}: {message.text}" for message in reversed(kept)
        )
        return f"{turns}\n\nAnswer the last message of the User as the Assistant."

    def send(self, text: str) -> Generator[str]:
        """Add the question and yield the answer in pieces.

        An answer that was stopped halfway is kept as it is; a failure
        takes the question back, so it can be sent again.
        """
        self.messages.append(Message("user", text))
        answer: list[str] = []
        failed = False
        try:
            for piece in runner.ask(
                self.assistant, self.prompt(), self.model, self.system
            ):
                answer.append(piece)
                yield piece
        except AssistantError:
            failed = True
            raise
        finally:
            if answer and not failed:
                self.messages.append(Message("assistant", "".join(answer)))
            else:
                self.messages.pop()
