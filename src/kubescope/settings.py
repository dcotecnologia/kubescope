"""User preferences stored as JSON in the platform's config directory."""

import json
import re
from pathlib import Path
from typing import Any

from kubescope.sdk.paths import config_directory
from kubescope.sdk.timezone import is_timezone

from kubescope.utils import shortcuts

# A language is a JSON file named by its code (see kubescope.i18n); "auto" follows
# the system. The choice is checked when it is applied, so a file can add one.
MAX_RECENT = 8  # the screens opened last that the app remembers
TEXT_SIZES = (85, 100, 115, 130, 150)  # percent of the usual size of the text
_LANGUAGE_CODE = re.compile(r"[a-z]{2,3}(_[A-Za-z0-9]+)?")

DEFAULTS: dict[str, Any] = {
    "language": "auto",
    "timezone": "auto",
    "theme": "dark",
    "remember_last_context": True,
    "last_context": None,
    "last_screen": [0, ""],
    "default_namespace": "",
    "context_aliases": {},
    "disabled_contexts": [],
    "hidden_columns": {},
    "list_sort": {},
    "pinned_views": [],
    "recent_screens": [],
    "debug_logging": False,
    "check_updates": True,
    "wrap_log_lines": False,
    "last_update_notice": "",
    "update_checked_at": 0.0,
    "update_checked_for": "",
    "write_mode": False,
    "animations": True,
    "text_size": 100,
    "sidebar_width": 0,
    "sidebar_collapsed": False,
    "menu_collapsed": [],
    "folded_sections": [],
    "section_order": [],
    "run_in_background": True,
    "system_title_bar": False,
    "welcome_dismissed": False,
    "last_seen_version": "",
    "window_geometry": "",
    "kubeconfig_files": [],
    "sign_in_commands": {},
    "terminal": "",
    "shortcuts": {},
    "integration_accounts": [],
    "extensions": {},
    "extensions_offered": [],
    "extension_updates_checked_at": 0.0,
    "extension_updates_seen": [],
}


# What Kubernetes accepts as a namespace name: a DNS label.
_NAMESPACE_NAME = re.compile(r"[a-z0-9]([-a-z0-9]*[a-z0-9])?")


def _clean_accounts(stored: object) -> list[dict[str, Any]]:
    """The cloud accounts saved, each with an id, a cloud, a name and the
    fields that are not secret; what cannot be read is left out."""
    accounts: list[dict[str, Any]] = []
    for item in stored if isinstance(stored, list) else []:
        if not isinstance(item, dict):
            continue
        account, provider, name = item.get("id"), item.get("provider"), item.get("name")
        fields = item.get("fields")
        if not all(
            isinstance(text, str) and text for text in (account, provider, name)
        ):
            continue
        if any(saved["id"] == account for saved in accounts):
            continue
        accounts.append(
            {
                "id": account,
                "provider": provider,
                "name": name,
                "fields": {
                    str(key): value
                    for key, value in (
                        fields if isinstance(fields, dict) else {}
                    ).items()
                    if isinstance(value, str)
                },
            }
        )
    return accounts


GABI = "kubescope.gabi"  # the extension that has the settings of the assistant
GABI_SHORTCUT = "kubescope.gabi.ask"
# the keys of the global search, which became the extension kubescope.search
_SEARCH_SHORTCUTS = {
    "search": "kubescope.search.open",
    "search_alt": "kubescope.search.open_alt",
}
# the keys of the assistant, as the app kept them, and what she calls them now
_GABI_KEYS = {
    "assistant_enabled": "enabled",
    "assistant_panel": "panel",
    "assistant_programs": "programs",
    "assistant_models": "models",
    "assistant_efforts": "efforts",
    "assistant": "assistant",
    "assistant_consent": "consent",
}
_EXTENSION_ID = re.compile(r"[a-z0-9][a-z0-9_.-]{0,99}")


def is_namespace_name(value: str) -> bool:
    return len(value) <= 63 and _NAMESPACE_NAME.fullmatch(value) is not None


def log_directory() -> Path:
    return config_directory() / "logs"


def default_context_name(context: str) -> str:
    """The name a context shows with when it has no alias of its own: the last
    part of it, so `arn:aws:eks:us-east-1:123:cluster/shop-prd` is `shop-
    prd`."""
    return context.rsplit("/", 1)[-1].rsplit(":", 1)[-1] or context


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
        except OSError, ValueError:
            pass
        self._adopt_assistant_keys(stored)
        self._adopt_search_keys(stored)
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
        disabled = self._data["disabled_contexts"]
        self._data["disabled_contexts"] = (
            sorted({context for context in disabled if isinstance(context, str)})
            if isinstance(disabled, list)
            else []
        )
        stored_columns = self._data["hidden_columns"]
        self._data["hidden_columns"] = {
            str(view): sorted({int(column) for column in columns})
            for view, columns in (
                stored_columns.items() if isinstance(stored_columns, dict) else []
            )
            if isinstance(columns, list)
            and all(isinstance(column, int) and column >= 0 for column in columns)
        }
        stored_sort = self._data["list_sort"]
        self._data["list_sort"] = {
            str(view): [sort[0], sort[1]]
            for view, sort in (
                stored_sort.items() if isinstance(stored_sort, dict) else []
            )
            if isinstance(sort, list)
            and len(sort) == 2
            and isinstance(sort[0], int)
            and not isinstance(sort[0], bool)
            and sort[0] >= 0
            and sort[1] in ("asc", "desc")
        }
        recent = self._data["recent_screens"]
        self._data["recent_screens"] = (
            list(
                dict.fromkeys(
                    key for key in recent if isinstance(key, str) and key.strip()
                )
            )[:MAX_RECENT]
            if isinstance(recent, list)
            else []
        )
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
        self._data["shortcuts"] = shortcuts.clean(self._data["shortcuts"])
        self._data["integration_accounts"] = _clean_accounts(
            self._data["integration_accounts"]
        )
        stored_extensions = self._data["extensions"]
        self._data["extensions"] = {
            name: data
            for name, data in (
                stored_extensions.items() if isinstance(stored_extensions, dict) else []
            )
            if isinstance(name, str)
            and _EXTENSION_ID.fullmatch(name)
            and isinstance(data, dict)
        }
        namespace = self._data["default_namespace"]
        if not (isinstance(namespace, str) and is_namespace_name(namespace)):
            self._data["default_namespace"] = ""  # empty means all namespaces
        self.language = self._data["language"]
        self.timezone = self._data["timezone"]
        self.theme = self._data["theme"]

    @staticmethod
    def _adopt_assistant_keys(stored: dict[str, Any]) -> None:
        """What the app kept for the assistant before Gabi became an extension
        moves under her id, so that nobody loses the preferences, the consent
        or the key of the shortcut; what she already has there is not
        replaced."""
        extensions = stored.get("extensions")
        extensions = extensions if isinstance(extensions, dict) else {}
        mine = extensions.get(GABI)
        mine = dict(mine) if isinstance(mine, dict) else {}
        for old, new in _GABI_KEYS.items():
            if old in stored and new not in mine:
                mine[new] = stored[old]
        pressed = stored.get("shortcuts")
        if isinstance(pressed, dict) and "assistant" in pressed:
            kept = {**pressed}
            asked = kept.pop("assistant")
            kept.setdefault(GABI_SHORTCUT, asked)
            stored["shortcuts"] = kept
        if mine:
            stored["extensions"] = {**extensions, GABI: mine}

    @staticmethod
    def _adopt_search_keys(stored: dict[str, Any]) -> None:
        """The keys the person chose for the global search, before it became an
        extension, move under the actions of the extension; what it already has
        there is not replaced."""
        pressed = stored.get("shortcuts")
        if not isinstance(pressed, dict):
            return
        kept = {**pressed}
        for old, new in _SEARCH_SHORTCUTS.items():
            if old in kept:
                asked = kept.pop(old)
                kept.setdefault(new, asked)
        stored["shortcuts"] = kept

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
    def timezone(self) -> str:
        """The local time ("auto") or an IANA zone name."""
        return self._data["timezone"]

    @timezone.setter
    def timezone(self, value: str) -> None:
        self._data["timezone"] = value if is_timezone(value) else "auto"

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
    def shortcuts(self) -> dict[str, str]:
        """Action -> key, every action present; an empty key turns it off."""
        return dict(self._data["shortcuts"])

    @shortcuts.setter
    def shortcuts(self, value: dict[str, str]) -> None:
        self._data["shortcuts"] = shortcuts.clean(value)

    @property
    def extensions_offered(self) -> list[str]:
        """The extensions the app already offered to install, so that it asks
        once and does not ask again after the person said no (or uninstalled
        one)."""
        value = self._data["extensions_offered"]
        return (
            list(
                dict.fromkeys(
                    one
                    for one in value
                    if isinstance(one, str) and _EXTENSION_ID.fullmatch(one)
                )
            )
            if isinstance(value, list)
            else []
        )

    @property
    def extension_updates_checked_at(self) -> float:
        """When the extensions were last looked at for a newer version, in
        seconds since the epoch; 0 when never."""
        value = self._data["extension_updates_checked_at"]
        valid = isinstance(value, int | float) and not isinstance(value, bool)
        return float(value) if valid and value > 0 else 0.0

    @property
    def extension_updates_seen(self) -> list[str]:
        """The newer versions of extensions that the person was told about, as
        `id@version`, so that the window that offers them shows once for each,
        not at every start."""
        value = self._data["extension_updates_seen"]
        return (
            [one for one in value if isinstance(one, str) and len(one) <= 120][-200:]
            if isinstance(value, list)
            else []
        )

    def see_extension_updates(self, keys: list[str]) -> None:
        self._data["extension_updates_seen"] = [
            *dict.fromkeys([*self.extension_updates_seen, *keys])
        ][-200:]

    def record_extension_updates_check(self, now: float) -> None:
        self._data["extension_updates_checked_at"] = float(now)

    def offered(self, extension: str) -> None:
        """Remember that `extension` was offered."""
        if extension not in self.extensions_offered:
            self._data["extensions_offered"] = [*self.extensions_offered, extension]

    def extension_data(self, extension: str) -> dict[str, Any]:
        """The preferences of one extension: a dictionary that is saved with
        the rest of the settings, and that no other extension sees.

        What the extension puts in it must be something JSON can hold.
        """
        if not _EXTENSION_ID.fullmatch(extension):
            raise ValueError(f"{extension!r} is not the id of an extension")
        return self._data["extensions"].setdefault(extension, {})

    @property
    def integration_accounts(self) -> list[dict[str, Any]]:
        """The cloud accounts plugged in: id, cloud, name and the fields that
        are not secret.

        The secrets are never saved.
        """
        return [dict(account) for account in self._data["integration_accounts"]]

    @integration_accounts.setter
    def integration_accounts(self, value: list[dict[str, Any]]) -> None:
        self._data["integration_accounts"] = _clean_accounts(value)

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

    def record_update_check(self, version: str, now: float) -> None:
        """Note that a check found `version` to be the newest, at `now`
        (seconds since the epoch)."""
        self._data["update_checked_at"] = float(now)
        self._data["update_checked_for"] = str(version)

    @property
    def update_checked_at(self) -> float:
        """When a check last found the running version to be the newest, in
        seconds since the epoch; 0 when it never did."""
        value = self._data["update_checked_at"]
        valid = isinstance(value, int | float) and not isinstance(value, bool)
        return float(value) if valid else 0.0

    @property
    def update_checked_for(self) -> str:
        """The version that check found to be the newest."""
        value = self._data["update_checked_for"]
        return value if isinstance(value, str) else ""

    def update_check_is_fresh(self, version: str, now: float, within: float) -> bool:
        """Whether a check made less than `within` seconds ago found `version`
        to be the newest, so asking GitHub again would only spend its limit."""
        at = self.update_checked_at
        return self.update_checked_for == version and at > 0 and 0 <= now - at < within

    @property
    def terminal(self) -> str:
        """The terminal the person chose to open the programs that need one:
        the name of one the app knows, or a command line of their own (like
        `alacritty -e`); empty uses the first one found."""
        value = self._data["terminal"]
        return value.strip() if isinstance(value, str) and len(value) <= 300 else ""

    @terminal.setter
    def terminal(self, value: str) -> None:
        self._data["terminal"] = str(value).strip()

    @property
    def sidebar_collapsed(self) -> bool:
        """Whether the side menu was hidden with the button of the header."""
        return self._data["sidebar_collapsed"] is True

    @sidebar_collapsed.setter
    def sidebar_collapsed(self, value: bool) -> None:
        self._data["sidebar_collapsed"] = bool(value)

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
    def menu_collapsed(self) -> list[str]:
        """The sections of the side menu the person closed; every one is open
        until they do.

        Only the known ones are read.
        """
        value = self._data["menu_collapsed"]
        known = ("workloads", "network", "config")
        return (
            sorted({name for name in value if name in known})
            if isinstance(value, list)
            else []
        )

    @menu_collapsed.setter
    def menu_collapsed(self, value: list[str]) -> None:
        self._data["menu_collapsed"] = list(value)

    @property
    def folded_sections(self) -> list[str]:
        """The blocks of the side menu (MONITORING, AWS, ...) the person folded
        from their title, by name; every one is open until they do."""
        value = self._data["folded_sections"]
        if not isinstance(value, list):
            return []
        return sorted(
            {
                name
                for name in value
                if isinstance(name, str) and name and len(name) <= 80
            }
        )

    @folded_sections.setter
    def folded_sections(self, value: list[str]) -> None:
        self._data["folded_sections"] = list(value)

    @property
    def section_order(self) -> list[str]:
        """The blocks of the side menu (MONITORING, AWS, ...) in the order the
        person gave them, by name; the ones not named come after, in the usual
        order."""
        value = self._data["section_order"]
        if not isinstance(value, list):
            return []
        names: list[str] = []
        for name in value:
            if isinstance(name, str) and name and len(name) <= 80 and name not in names:
                names.append(name)
        return names

    @section_order.setter
    def section_order(self, value: list[str]) -> None:
        self._data["section_order"] = list(value)

    @property
    def sidebar_width(self) -> int:
        """The width the person gave the side menu; 0 when they gave none, so
        it keeps its usual one."""
        value = self._data["sidebar_width"]
        return value if type(value) is int and 150 <= value <= 800 else 0

    @sidebar_width.setter
    def sidebar_width(self, value: int) -> None:
        self._data["sidebar_width"] = int(value)

    @property
    def animations(self) -> bool:
        """Whether windows and lists rise into place as they show; on unless
        the person turned it off."""
        return self._data["animations"] is not False

    @animations.setter
    def animations(self, value: bool) -> None:
        self._data["animations"] = bool(value)

    @property
    def text_size(self) -> int:
        """The size of the text of the app, as a percentage of the usual one;
        one of `TEXT_SIZES`, else 100."""
        value = self._data["text_size"]
        return value if value in TEXT_SIZES and not isinstance(value, bool) else 100

    @text_size.setter
    def text_size(self, value: int) -> None:
        self._data["text_size"] = value if value in TEXT_SIZES else 100

    @property
    def welcome_dismissed(self) -> bool:
        """True once the person chose never to see the welcome message
        again."""
        return self._data["welcome_dismissed"] is True

    @welcome_dismissed.setter
    def welcome_dismissed(self, value: bool) -> None:
        self._data["welcome_dismissed"] = bool(value)

    @property
    def last_seen_version(self) -> str:
        """The version of the app that last showed the welcome page; empty when
        none did, which is also what an update is told from."""
        value = self._data["last_seen_version"]
        return value if isinstance(value, str) and len(value) <= 40 else ""

    @last_seen_version.setter
    def last_seen_version(self, value: str) -> None:
        self._data["last_seen_version"] = str(value)

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

    @property
    def disabled_contexts(self) -> set[str]:
        """The contexts the person disconnected: the app leaves them out of the
        selector at the top."""
        return set(self._data["disabled_contexts"])

    def set_disabled_contexts(self, contexts: set[str]) -> None:
        self._data["disabled_contexts"] = sorted(contexts)

    def hidden_columns(self, view: str) -> set[int]:
        return set(self._data["hidden_columns"].get(view, []))

    def set_hidden_columns(self, view: str, columns: set[int]) -> None:
        self._data["hidden_columns"][view] = sorted(columns)

    def list_sort(self, view: str) -> tuple[int, bool] | None:
        """The column a list was sorted by and whether it was descending, as
        the person left it."""
        sort = self._data["list_sort"].get(view)
        return (sort[0], sort[1] == "desc") if sort else None

    def set_list_sort(self, view: str, column: int, descending: bool) -> None:
        self._data["list_sort"][view] = [column, "desc" if descending else "asc"]

    def pinned_views(self) -> list[str]:
        return list(self._data["pinned_views"])

    def set_pinned_views(self, views: list[str]) -> None:
        self._data["pinned_views"] = list(dict.fromkeys(views))

    def recent_screens(self) -> list[str]:
        """The lists and pages of extensions opened last, the latest first."""
        return list(self._data["recent_screens"])

    def add_recent_screen(self, key: str) -> None:
        """Put a screen first among the ones opened last."""
        kept = [one for one in self._data["recent_screens"] if one != key]
        self._data["recent_screens"] = [key, *kept][:MAX_RECENT]

    def display_name(self, context: str) -> str:
        return self._data["context_aliases"].get(context) or default_context_name(
            context
        )
