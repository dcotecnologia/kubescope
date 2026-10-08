"""User preferences stored as JSON in the platform's config directory."""

import json
import os
import sys
from pathlib import Path
from typing import Any

CONFIG_DIR_ENV = "KUBESCOPE_CONFIG_DIR"
LANGUAGE_CHOICES = ("auto", "en", "pt")

DEFAULTS: dict[str, Any] = {
    "language": "auto",
    "remember_last_context": True,
    "last_context": None,
    "context_aliases": {},
}


def config_directory() -> Path:
    override = os.environ.get(CONFIG_DIR_ENV)
    if override:
        return Path(override)
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return base / "kubescope"


class Settings:
    """Loads tolerant of missing or damaged files and saves atomically."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or config_directory() / "settings.json"
        self._data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        stored: dict[str, Any] = {}
        try:
            document = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(document, dict):
                stored = document
        except (OSError, ValueError):
            pass
        self._data = {**DEFAULTS, **{k: stored[k] for k in DEFAULTS if k in stored}}
        self._data["context_aliases"] = {
            str(context): str(alias).strip()
            for context, alias in dict(
                self._data["context_aliases"]
                if isinstance(self._data["context_aliases"], dict)
                else {}
            ).items()
            if str(alias).strip()
        }
        if self._data["language"] not in LANGUAGE_CHOICES:
            self._data["language"] = DEFAULTS["language"]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)

    @property
    def language(self) -> str:
        return self._data["language"]

    @language.setter
    def language(self, value: str) -> None:
        self._data["language"] = value if value in LANGUAGE_CHOICES else "auto"

    @property
    def remember_last_context(self) -> bool:
        return bool(self._data["remember_last_context"])

    @remember_last_context.setter
    def remember_last_context(self, value: bool) -> None:
        self._data["remember_last_context"] = bool(value)

    @property
    def last_context(self) -> str | None:
        return self._data["last_context"]

    @last_context.setter
    def last_context(self, value: str | None) -> None:
        self._data["last_context"] = value

    @property
    def context_aliases(self) -> dict[str, str]:
        return dict(self._data["context_aliases"])

    def set_context_aliases(self, aliases: dict[str, str]) -> None:
        self._data["context_aliases"] = {
            context: alias.strip()
            for context, alias in aliases.items()
            if alias.strip()
        }

    def display_name(self, context: str) -> str:
        return self._data["context_aliases"].get(context) or context
