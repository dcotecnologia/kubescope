"""The context each extension is handed, behind the permissions it asked for.

`Host` is what the window lends: the registries and a few functions that
read the app. `ExtensionContext` implements `kubescope.sdk.Context` over
it. No Qt.
"""

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from kubescope.extensions.registries import CommandRegistry, Contributions, EventBus
from kubescope.sdk import (
    PERMISSIONS,
    CliCommand,
    ClusterAccess,
    DockContribution,
    PermissionDenied,
    SettingsSection,
    TabKind,
    WriteModeOff,
)


@dataclass
class Host:
    """What the app lends to the extensions."""

    cluster: ClusterAccess  # the read paths, `kubescope.cluster`
    snapshot: Callable[[], str]  # the screen, in words
    current_context: Callable[[], str | None]
    write_mode: Callable[[], bool]
    settings_data: Callable[[str], dict[str, Any]]  # the store of one extension
    save_settings: Callable[[], None]
    events: EventBus = field(default_factory=EventBus)
    commands: CommandRegistry = field(default_factory=CommandRegistry)
    contributions: Contributions = field(default_factory=Contributions)


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


class ExtensionWrites:
    def __init__(self, host: Host) -> None:
        self._host = host

    def run(self, function: Callable[..., Any], *arguments: Any) -> Any:
        if not self._host.write_mode():
            raise WriteModeOff("turn on the write mode to change the cluster")
        return function(*arguments)


class ExtensionContext:
    def __init__(self, extension: str, permissions: frozenset[str], host: Host) -> None:
        unknown = permissions - set(PERMISSIONS)
        if unknown:
            raise ValueError(f"unknown permissions: {', '.join(sorted(unknown))}")
        self.id = extension
        self.permissions = permissions
        self._host = host
        self.events = host.events
        self.settings = ExtensionSettings(
            host.settings_data(extension), host.save_settings
        )

    def _require(self, permission: str) -> None:
        if permission not in self.permissions:
            raise PermissionDenied(f"{self.id} did not ask for {permission}")

    @property
    def cluster(self) -> ClusterAccess:
        self._require("cluster.read")
        return self._host.cluster

    @property
    def writes(self) -> ExtensionWrites:
        self._require("cluster.write")
        return ExtensionWrites(self._host)

    @property
    def current_context(self) -> str | None:
        return self._host.current_context()

    def snapshot(self) -> str:
        return self._host.snapshot()

    def invoke(self, command: str, /, **arguments: Any) -> Any:
        return self._host.commands.invoke(command, **arguments)

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
