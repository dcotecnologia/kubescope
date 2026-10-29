"""The `codex` program, as an assistant."""

import json
import tempfile
from collections.abc import Sequence
from typing import Any

from kubescope.assistant.runner import Assistant

# Everything of Codex that can act, off: it is asked to answer, not to work. With
# the sandbox only read-only it could still read any file of the computer.
_OFF = (
    "shell_tool",
    "unified_exec",
    "view_image",
    "apps",
    "plugins",
    "remote_plugin",
    "hooks",
    "browser_use",
    "browser_use_external",
    "browser_use_full_cdp_access",
    "computer_use",
    "in_app_browser",
    "in_app_local_automation",
    "image_generation",
    "multi_agent",
    "skill_mcp_dependency_install",
    "sleep_tool",
)


def options(model: str | None, system: str) -> list[str]:
    """No tools, no saved session, no user configuration (its servers and
    hooks), a read-only sandbox and the temporary folder to work in."""
    arguments = [
        "exec",
        "--json",
        "--color",
        "never",
        "--sandbox",
        "read-only",
        "--ephemeral",
        "--skip-git-repo-check",
        "--ignore-user-config",
        "--ignore-rules",
        "-C",
        tempfile.gettempdir(),
        "-c",
        'web_search="disabled"',
    ]
    for feature in _OFF:
        arguments += ["-c", f"features.{feature}=false"]
    return [*arguments, "-m", model] if model else arguments


def compose(system: str, prompt: str) -> str:
    """Codex has no option for the instructions, so they go before the
    conversation."""
    return f"[Instructions]\n{system}\n\n[Conversation]\n{prompt}"


def image_files(paths: Sequence[str]) -> list[str]:
    """It reads images from files."""
    arguments: list[str] = []
    for path in paths:
        arguments += ["--image", path]
    return arguments


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def parse_line(line: str) -> tuple[str, str]:
    """The text a line of its output adds, and the error it reports.

    Its answer comes whole, not word by word, as a message of the agent.
    """
    try:
        event = _dict(json.loads(line))
    except ValueError:  # not an event: a notice of the program
        return "", ""
    if event.get("type") == "turn.failed":
        message = _dict(event.get("error")).get("message")
        return "", str(message or "The assistant failed")
    item = _dict(event.get("item"))
    if event.get("type") == "item.completed" and item.get("type") == "agent_message":
        text = item.get("text")
        return (f"{text}\n\n" if isinstance(text, str) and text else ""), ""
    return "", ""


GUIDE = "https://learn.chatgpt.com/docs/codex/cli#getting-started"

CODEX = Assistant(
    "codex",
    "Codex",
    "codex",
    options,
    parse_line,
    guide=lambda _language: GUIDE,
    compose=compose,
    image_files=image_files,
)
