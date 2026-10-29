"""Files the person attaches to a question for the assistant.

An image goes to the assistant as an image, if its program takes them. A
text file (a log, a manifest) goes into the question as text, after the
redaction of tokens and keys. They are sent, not kept: the history holds
only the names. No Qt.
"""

import base64
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from kubescope.utils.diagnostics import redact

MAX_IMAGE_BYTES = 5 * 2**20  # what the services take for one image
MAX_TEXT_BYTES = 200 * 2**10
MAX_ATTACHMENTS = 4
IMAGE_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}
TEXT_TYPES = frozenset(
    {
        ".txt",
        ".log",
        ".yaml",
        ".yml",
        ".json",
        ".md",
        ".csv",
        ".conf",
        ".ini",
        ".toml",
        ".xml",
        ".sh",
        ".py",
        ".go",
        ".tf",
    }
)

Kind = Literal["image", "text"]


class AttachmentError(Exception):
    """The file cannot be attached; the message says why."""


@dataclass(frozen=True, slots=True)
class Attachment:
    name: str
    kind: Kind
    data: bytes
    media_type: str = "text/plain"

    @property
    def text(self) -> str:
        """The content of a text file, redacted."""
        return redact(self.data.decode("utf-8", errors="replace"))

    @property
    def base64(self) -> str:
        return base64.b64encode(self.data).decode("ascii")


def load(path: Path) -> Attachment:
    """Read a file to attach, checking its kind and size."""
    suffix = path.suffix.lower()
    try:
        size = path.stat().st_size
        if suffix in IMAGE_TYPES:
            if size > MAX_IMAGE_BYTES:
                raise AttachmentError(
                    f"{path.name} is larger than {MAX_IMAGE_BYTES // 2**20} MiB"
                )
            return Attachment(
                path.name, "image", path.read_bytes(), IMAGE_TYPES[suffix]
            )
        if suffix not in TEXT_TYPES:
            raise AttachmentError(f"{path.name} is not an image or a text file")
        if size > MAX_TEXT_BYTES:
            raise AttachmentError(
                f"{path.name} is larger than {MAX_TEXT_BYTES // 2**10} KiB"
            )
        data = path.read_bytes()
    except OSError as error:
        raise AttachmentError(
            f"{path.name} cannot be read: {error.strerror}"
        ) from error
    if b"\x00" in data:
        raise AttachmentError(f"{path.name} is not text")
    return Attachment(path.name, "text", data)


def text_block(attachments: tuple[Attachment, ...]) -> str:
    """The text files, to put after the question."""
    return "\n\n".join(
        f"Attached file {item.name}:\n```\n{item.text}\n```"
        for item in attachments
        if item.kind == "text"
    )


def images(attachments: tuple[Attachment, ...]) -> tuple[Attachment, ...]:
    return tuple(item for item in attachments if item.kind == "image")
