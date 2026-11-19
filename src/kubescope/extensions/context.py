"""The context each extension is handed, behind the permissions it asked for.

`Host` is what the window lends: the registries and a few functions that
read the app. `ExtensionContext` implements `kubescope.sdk.Context` over
it. No Qt.
"""

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kubescope.sdk.paths import config_directory

from kubescope.extensions.cluster_access import WritesBridge
from kubescope.extensions.registries import CommandRegistry, Contributions, EventBus
from kubescope.sdk import (
    PERMISSIONS,
    Cli,
    CliCommand,
    ClusterAccess,
    CommandError,
    DockContribution,
    PermissionDenied,
    SettingsSection,
    ShortcutContribution,
    TabKind,
    Ui,
    Writes,
)

logger = logging.getLogger(__name__)


def data_directory(extension: str) -> Path:
    """The folder that is an extension's own, for what it writes down."""
    return config_directory() / "extension-data" / extension


@dataclass
class Host:
    """What the app lends to the extensions."""

    cluster: ClusterAccess  # the read paths, `kubescope.cluster`
    snapshot: Callable[[], str]  # the screen, in words
    current_context: Callable[[], str | None]
    write_mode: Callable[[], bool]
    settings_data: Callable[[str], dict[str, Any]]  # the store of one extension
    save_settings: Callable[[], None]
    language: Callable[[], str] = lambda: "auto"
    resolved_language: Callable[[], str] = lambda: "en"
    language_name: Callable[[], str] = lambda: "English"
    data_directory: Callable[[str], Path] = lambda extension: Path(extension)
    ui: Ui | None = None  # None while the app runs without a window
    cli: Cli | None = None  # set while a command of the terminal runs
    events: EventBus = field(default_factory=EventBus)
    commands: CommandRegistry = field(default_factory=CommandRegistry)
    contributions: Contributions = field(default_factory=Contributions)


class AppInfo:
    """What the app says about itself, read when asked."""

    def __init__(self, host: Host) -> None:
        self._host = host

    @property
    def write_mode(self) -> bool:
        return self._host.write_mode()

    @property
    def language(self) -> str:
        return self._host.language()

    @property
    def resolved_language(self) -> str:
        return self._host.resolved_language()

    @property
    def language_name(self) -> str:
        return self._host.language_name()


class ExtensionSettings:
    def __init__(self, data: dict[str, Any], save: Callable[[], None]) -> None:
        self._data = data
        self._save = save

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        json.dumps(value)  # only what the settings file can hold
        self._data[key] = value
        self._save()


class ScopedEvents:
    """The events as one extension sees them: what it subscribes to is
    remembered, so that unloading it stops every handler."""

    def __init__(self, bus: EventBus) -> None:
        self._bus = bus
        self._offs: list[Callable[[], None]] = []

    def on(self, event: str, handler: Callable[..., None]) -> Callable[[], None]:
        off = self._bus.on(event, handler)
        self._offs.append(off)
        return off

    def close(self) -> None:
        for off in self._offs:
            off()
        self._offs.clear()


class ExtensionContext:
    def __init__(self, extension: str, permissions: frozenset[str], host: Host) -> None:
        unknown = permissions - set(PERMISSIONS)
        if unknown:
            raise ValueError(f"unknown permissions: {', '.join(sorted(unknown))}")
        self.id = extension
        self.permissions = permissions
        self._host = host
        self.events = ScopedEvents(host.events)
        self._cleanups: list[Callable[[], None]] = []
        self._commands: list[str] = []
        self.app = AppInfo(host)
        self.settings = ExtensionSettings(
            host.settings_data(extension), host.save_settings
        )

    def on_unload(self, callback: Callable[[], None]) -> None:
        """Call `callback` when the extension is unloaded (the app quits, it is
        uninstalled, or it is reloaded), to close what it created."""
        self._cleanups.append(callback)

    def close(self) -> None:
        """The extension is unloaded: run its cleanups, stop its handlers and
        drop what it added."""
        while self._cleanups:
            try:
                self._cleanups.pop()()
            except Exception:
                logger.exception("A cleanup of the extension %s failed", self.id)
        for name in self._commands:
            self._host.commands.unregister(name)
        self._commands.clear()
        self.events.close()
        self._host.contributions.remove_extension(self.id)

    def _require(self, permission: str) -> None:
        if permission not in self.permissions:
            raise PermissionDenied(f"{self.id} did not ask for {permission}")

    @property
    def cluster(self) -> ClusterAccess:
        self._require("cluster.read")
        return self._host.cluster

    @property
    def writes(self) -> Writes:
        self._require("cluster.write")
        return WritesBridge(self._host.write_mode)

    @property
    def current_context(self) -> str | None:
        return self._host.current_context()

    def snapshot(self) -> str:
        return self._host.snapshot()

    def invoke(self, command: str, /, **arguments: Any) -> Any:
        return self._host.commands.invoke(command, **arguments)

    @property
    def cli(self) -> Cli | None:
        self._require("cli")
        return self._host.cli

    @property
    def data_directory(self) -> Path:
        return self._host.data_directory(self.id)

    @property
    def ui(self) -> Ui | None:
        self._require("ui.window")
        return self._host.ui

    def register_command(self, name: str, command: Callable[..., Any]) -> None:
        if not name.startswith(f"{self.id}."):
            raise CommandError(
                f"the name of a command of {self.id} starts with {self.id}."
            )
        self._host.commands.register(name, command)
        self._commands.append(name)

    def add_shortcut(
        self,
        action: str,
        label: str,
        default: str,
        handler: Callable[[], None],
        application: bool = False,
    ) -> None:
        self._require("ui.window")
        self._host.contributions.shortcuts.append(
            ShortcutContribution(self.id, action, label, default, handler, application)
        )

    def add_dock(
        self, key: str, factory: Callable[..., Any], shortcut: str = ""
    ) -> None:
        self._require("ui.dock")
        self._host.contributions.docks.append(
            DockContribution(self.id, key, factory, shortcut)
        )

    def add_tab_kind(self, key: str, factory: Callable[..., Any]) -> None:
        self._require("ui.tab")
        self._host.contributions.tab_kinds.append(TabKind(self.id, key, factory))

    def add_settings_section(self, title: str, factory: Callable[..., Any]) -> None:
        self._require("ui.settings")
        self._host.contributions.settings_sections.append(
            SettingsSection(self.id, title, factory)
        )

    def add_cli_command(self, name: str, run: Callable[[list[str]], int]) -> None:
        self._require("cli")
        self._host.contributions.cli_commands.append(CliCommand(self.id, name, run))
