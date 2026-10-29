"""User preferences stored as JSON in the platform's config directory."""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

CONFIG_DIR_ENV = "KUBESCOPE_CONFIG_DIR"
# A language is a JSON file named by its code (see kubescope.i18n); "auto" follows
# the system. The choice is checked when it is applied, so a file can add one.
_LANGUAGE_CODE = re.compile(r"[a-z]{2,3}(_[A-Za-z0-9]+)?")

DEFAULTS: dict[str, Any] = {
    "language": "auto",
    "theme": "dark",
    "remember_last_context": True,
    "last_context": None,
    "last_screen": [0, ""],
    "default_namespace": "",
    "context_aliases": {},
    "hidden_columns": {},
    "pinned_views": [],
    "debug_logging": False,
    "check_updates": True,
    "wrap_log_lines": False,
    "last_update_notice": "",
    "write_mode": False,
    "assistant": "",
    "assistant_consent": False,
    "run_in_background": True,
    "system_title_bar": False,
    "welcome_dismissed": False,
    "window_geometry": "",
    "kubeconfig_files": [],
    "sign_in_commands": {},
}


# What Kubernetes accepts as a namespace name: a DNS label.
_NAMESPACE_NAME = re.compile(r"[a-z0-9]([-a-z0-9]*[a-z0-9])?")


def is_namespace_name(value: str) -> bool:
    return len(value) <= 63 and _NAMESPACE_NAME.fullmatch(value) is not None


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


def log_directory() -> Path:
    return config_directory() / "logs"


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
        stored_columns = self._data["hidden_columns"]
        self._data["hidden_columns"] = {
            str(view): sorted({int(column) for column in columns})
            for view, columns in (
                stored_columns.items() if isinstance(stored_columns, dict) else []
            )
            if isinstance(columns, list)
            and all(isinstance(column, int) and column >= 0 for column in columns)
        }
        pinned = self._data["pinned_views"]
        self._data["pinned_views"] = list(
            dict.fromkeys(
                view for view in pinned if isinstance(view, str) and view.strip()
            )
            if isinstance(pinned, list)
            else []
        )
        files = self._data["kubeconfig_files"]
        self._data["kubeconfig_files"] = (
            [path.strip() for path in files if isinstance(path, str) and path.strip()]
            if isinstance(files, list)
            else []
        )
        commands = self._data["sign_in_commands"]
        self._data["sign_in_commands"] = {
            program.strip(): command.strip()
            for program, command in (
                commands.items() if isinstance(commands, dict) else []
            )
            if isinstance(program, str)
            and isinstance(command, str)
            and program.strip()
            and command.strip()
        }
        namespace = self._data["default_namespace"]
        if not (isinstance(namespace, str) and is_namespace_name(namespace)):
            self._data["default_namespace"] = ""  # empty means all namespaces
        self.language = self._data["language"]
        self.theme = self._data["theme"]

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
        valid = isinstance(value, str) and _LANGUAGE_CODE.fullmatch(value)
        self._data["language"] = value if valid or value == "auto" else "auto"

    @property
    def theme(self) -> str:
        return self._data["theme"]

    @theme.setter
    def theme(self, value: str) -> None:
        """The id of a built-in or custom theme; one that no longer exists
        falls back to the default when it is applied."""
        valid = isinstance(value, str) and value.strip() != ""
        self._data["theme"] = value if valid else DEFAULTS["theme"]

    @property
    def remember_last_context(self) -> bool:
        return bool(self._data["remember_last_context"])

    @remember_last_context.setter
    def remember_last_context(self, value: bool) -> None:
        self._data["remember_last_context"] = bool(value)

    @property
    def debug_logging(self) -> bool:
        return self._data["debug_logging"] is True

    @debug_logging.setter
    def debug_logging(self, value: bool) -> None:
        self._data["debug_logging"] = bool(value)

    @property
    def kubeconfig_files(self) -> list[str]:
        """Kubeconfig files to read instead of KUBECONFIG; empty means the
        default ones."""
        return list(self._data["kubeconfig_files"])

    @kubeconfig_files.setter
    def kubeconfig_files(self, value: list[str]) -> None:
        self._data["kubeconfig_files"] = [
            path.strip() for path in value if path.strip()
        ]

    @property
    def sign_in_commands(self) -> dict[str, str]:
        """Sign-in program of a kubeconfig (like `oci`) -> the command that
        signs in (like `oci session authenticate`)."""
        return dict(self._data["sign_in_commands"])

    @sign_in_commands.setter
    def sign_in_commands(self, value: dict[str, str]) -> None:
        self._data["sign_in_commands"] = {
            program.strip(): command.strip()
            for program, command in value.items()
            if program.strip() and command.strip()
        }

    @property
    def window_geometry(self) -> str:
        """The size, position and maximized state of the window, as the base64
        text Qt saved it; empty until the window has been closed once."""
        value = self._data["window_geometry"]
        return value if isinstance(value, str) else ""

    @window_geometry.setter
    def window_geometry(self, value: str) -> None:
        self._data["window_geometry"] = str(value)

    @property
    def check_updates(self) -> bool:
        return self._data["check_updates"] is not False

    @check_updates.setter
    def check_updates(self, value: bool) -> None:
        self._data["check_updates"] = bool(value)

    @property
    def wrap_log_lines(self) -> bool:
        """Whether the logs break long lines to the width of the view."""
        return self._data["wrap_log_lines"] is True

    @wrap_log_lines.setter
    def wrap_log_lines(self, value: bool) -> None:
        self._data["wrap_log_lines"] = bool(value)

    @property
    def last_update_notice(self) -> str:
        """The day (YYYY-MM-DD) the system was last told of a new version."""
        value = self._data["last_update_notice"]
        return value if isinstance(value, str) else ""

    @last_update_notice.setter
    def last_update_notice(self, value: str) -> None:
        self._data["last_update_notice"] = str(value)

    @property
    def run_in_background(self) -> bool:
        """Whether closing the window leaves the app running in the system
        tray; on unless the person turned it off."""
        return self._data["run_in_background"] is not False

    @run_in_background.setter
    def run_in_background(self, value: bool) -> None:
        self._data["run_in_background"] = bool(value)

    @property
    def system_title_bar(self) -> bool:
        """Whether the window keeps the title bar of the system instead of
        drawing its own in the top bar; off unless the setting is exactly
        true."""
        return self._data["system_title_bar"] is True

    @system_title_bar.setter
    def system_title_bar(self, value: bool) -> None:
        self._data["system_title_bar"] = bool(value)

    @property
    def write_mode(self) -> bool:
        """True when the person allowed the actions that change a cluster; off
        unless the setting is exactly true."""
        return self._data["write_mode"] is True

    @write_mode.setter
    def write_mode(self, value: bool) -> None:
        self._data["write_mode"] = bool(value)

    @property
    def assistant(self) -> str:
        """The program the person chose for the assistant; empty leaves it to
        the first one the system has."""
        value = self._data["assistant"]
        return value if isinstance(value, str) else ""

    @assistant.setter
    def assistant(self, value: str) -> None:
        self._data["assistant"] = str(value)

    @property
    def assistant_consent(self) -> bool:
        """True once the person agreed that what they ask the assistant, with
        the cluster data it reads, leaves this computer; off unless exactly
        true."""
        return self._data["assistant_consent"] is True

    @assistant_consent.setter
    def assistant_consent(self, value: bool) -> None:
        self._data["assistant_consent"] = bool(value)

    @property
    def welcome_dismissed(self) -> bool:
        """True once the person chose never to see the welcome message
        again."""
        return self._data["welcome_dismissed"] is True

    @welcome_dismissed.setter
    def welcome_dismissed(self, value: bool) -> None:
        self._data["welcome_dismissed"] = bool(value)

    @property
    def last_context(self) -> str | None:
        return self._data["last_context"]

    @last_context.setter
    def last_context(self, value: str | None) -> None:
        self._data["last_context"] = value

    @property
    def last_screen(self) -> tuple[int, str]:
        """The page number and the list the app was left on."""
        value = self._data["last_screen"]
        if (
            isinstance(value, list)
            and len(value) == 2
            and isinstance(value[0], int)
            and isinstance(value[1], str)
        ):
            return value[0], value[1]
        return 0, ""

    @last_screen.setter
    def last_screen(self, value: tuple[int, str]) -> None:
        self._data["last_screen"] = [value[0], value[1]]

    @property
    def default_namespace(self) -> str:
        """The namespace each context opens on; empty for all of them."""
        return self._data["default_namespace"]

    @default_namespace.setter
    def default_namespace(self, value: str) -> None:
        self._data["default_namespace"] = value if is_namespace_name(value) else ""

    @property
    def context_aliases(self) -> dict[str, str]:
        return dict(self._data["context_aliases"])

    def set_context_aliases(self, aliases: dict[str, str]) -> None:
        self._data["context_aliases"] = {
            context: alias.strip()
            for context, alias in aliases.items()
            if alias.strip()
        }

    def hidden_columns(self, view: str) -> set[int]:
        return set(self._data["hidden_columns"].get(view, []))

    def set_hidden_columns(self, view: str, columns: set[int]) -> None:
        self._data["hidden_columns"][view] = sorted(columns)

    def pinned_views(self) -> list[str]:
        return list(self._data["pinned_views"])

    def set_pinned_views(self, views: list[str]) -> None:
        self._data["pinned_views"] = list(dict.fromkeys(views))

    def display_name(self, context: str) -> str:
        return self._data["context_aliases"].get(context) or context
