"""The `claude` program, as an assistant."""

import json
from typing import Any

from kubescope.assistant.runner import SYSTEM_PROMPT, Assistant


def options(model: str | None) -> list[str]:
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
        SYSTEM_PROMPT,
    ]
    return [*arguments, "--model", model] if model else arguments


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


CLAUDE = Assistant("claude", "Claude", "claude", options, parse_line)
