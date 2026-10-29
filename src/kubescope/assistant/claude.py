"""The `claude` program, as an assistant."""

import json
from collections.abc import Sequence
from typing import Any

from kubescope.assistant.attachments import Attachment
from kubescope.assistant.runner import Assistant


def options(model: str | None, system: str) -> list[str]:
    """No tools, so it cannot read a file or run a command, and no saved
    session."""
    arguments = [
        "-p",
        "--output-format",
        "stream-json",
        "--verbose",
        "--include-partial-messages",
        "--tools",
        "",
        "--no-session-persistence",
        "--system-prompt",
        system,
    ]
    return [*arguments, "--model", model] if model else arguments


def image_options(model: str | None, system: str) -> list[str]:
    """The same, reading the question as a message, which can hold images."""
    return [*options(model, system), "--input-format", "stream-json"]


def image_payload(prompt: str, images: Sequence[Attachment]) -> str:
    """The question and its images as the one message the program reads."""
    content: list[dict[str, Any]] = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image.media_type,
                "data": image.base64,
            },
        }
        for image in images
    ]
    content.append({"type": "text", "text": prompt})
    message = {"type": "user", "message": {"role": "user", "content": content}}
    return json.dumps(message) + "\n"


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def parse_line(line: str) -> tuple[str, str]:
    """The text a line of its output adds, and the error it reports."""
    try:
        event = _dict(json.loads(line))
    except ValueError:  # not an event: a notice of the program
        return "", ""
    if event.get("type") == "result" and event.get("is_error"):
        return "", str(event.get("result") or "The assistant failed")
    delta = _dict(_dict(event.get("event")).get("delta"))
    text = delta.get("text")
    return (text if isinstance(text, str) else ""), ""


def guide(language: str) -> str:
    """The quickstart of Claude Code, in Portuguese or English."""
    return (
        f"https://code.claude.com/docs/{'pt' if language == 'pt' else 'en'}/quickstart"
    )


CLAUDE = Assistant(
    "claude",
    "Claude Code",
    "claude",
    options,
    parse_line,
    image_options,
    image_payload,
    guide=guide,
)
