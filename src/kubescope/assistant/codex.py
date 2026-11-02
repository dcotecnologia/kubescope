"""The `codex` program, as an assistant."""

import json
import tempfile
import tomllib
from collections.abc import Sequence
from pathlib import Path
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


def defaults() -> tuple[str, str]:
    """The model and the effort in the configuration of Codex, which it is not
    allowed to read here (`--ignore-user-config`), so they are told to it."""
    try:
        data = tomllib.loads(
            (Path.home() / ".codex" / "config.toml").read_text(encoding="utf-8")
        )
    except OSError, ValueError:
        return "", ""
    model, effort = data.get("model"), data.get("model_reasoning_effort")
    return (
        model if isinstance(model, str) else "",
        effort if isinstance(effort, str) else "",
    )


def listed_models() -> tuple[str, ...]:
    """The models Codex lists for the person, from the cache it keeps; none
    when it has not been run yet or the cache cannot be read."""
    try:
        cache = json.loads(
            (Path.home() / ".codex" / "models_cache.json").read_text(encoding="utf-8")
        )
        return tuple(
            model["slug"]
            for model in cache["models"]
            if model.get("visibility") == "list" and isinstance(model["slug"], str)
        )
    except OSError, ValueError, KeyError, TypeError, AttributeError:
        return ()


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
    models=listed_models(),
    efforts=("low", "medium", "high", "xhigh", "max", "ultra"),
    effort_options=lambda effort: ["-c", f'model_reasoning_effort="{effort}"'],
    defaults=defaults,
)
