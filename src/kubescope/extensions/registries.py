"""The registries the window fills and the extensions use.

No Qt.
"""

import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from kubescope.sdk import (
    EVENTS,
    CliCommand,
    CommandError,
    DockContribution,
    PageContribution,
    SettingsSection,
    ShortcutContribution,
    TabKind,
)

logger = logging.getLogger(__name__)

Handler = Callable[..., None]
Command = Callable[..., Any]


class EventBus:
    """Handlers by event name; the names are the ones in `EVENTS`.

    A handler that raises is logged and skipped, so one broken extension
    never stops the app or the other extensions.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = {name: [] for name in EVENTS}

    def on(self, event: str, handler: Handler) -> Callable[[], None]:
        if event not in self._handlers:
            raise ValueError(f"unknown event: {event}")
        self._handlers[event].append(handler)

        def off() -> None:
            if handler in self._handlers[event]:
                self._handlers[event].remove(handler)

        return off

    def emit(self, event: str, **payload: Any) -> None:
        """Tell every handler of `event`, in the order they subscribed."""
        if event not in self._handlers:
            raise ValueError(f"unknown event: {event}")
        for handler in list(self._handlers[event]):
            try:
                handler(**payload)
            except Exception:
                logger.exception("an extension failed on the %s event", event)


class CommandRegistry:
    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}

    def register(self, name: str, command: Command) -> None:
        """Offer `command` as `name`; a name belongs to one command only."""
        if name in self._commands:
            raise CommandError(f"the command {name} is already registered")
        self._commands[name] = command

    def unregister(self, name: str) -> None:
        self._commands.pop(name, None)

    def names(self) -> list[str]:
        return sorted(self._commands)

    def has(self, name: str) -> bool:
        return name in self._commands

    def invoke(self, name: str, /, **arguments: Any) -> Any:
        """Run the command `name` and return what it returns."""
        command = self._commands.get(name)
        if command is None:
            raise CommandError(f"there is no command {name}")
        return command(**arguments)


@dataclass
class Contributions:
    """Everything the extensions added, for the window to build."""

    docks: list[DockContribution] = field(default_factory=list)
    tab_kinds: list[TabKind] = field(default_factory=list)
    pages: list[PageContribution] = field(default_factory=list)
    settings_sections: list[SettingsSection] = field(default_factory=list)
    cli_commands: list[CliCommand] = field(default_factory=list)
    shortcuts: list[ShortcutContribution] = field(default_factory=list)

    def remove_extension(self, extension: str) -> None:
        """Drop everything `extension` added."""
        self.docks = [one for one in self.docks if one.extension != extension]
        self.tab_kinds = [one for one in self.tab_kinds if one.extension != extension]
        self.pages = [one for one in self.pages if one.extension != extension]
        self.settings_sections = [
            one for one in self.settings_sections if one.extension != extension
        ]
        self.cli_commands = [
            one for one in self.cli_commands if one.extension != extension
        ]
        self.shortcuts = [one for one in self.shortcuts if one.extension != extension]
