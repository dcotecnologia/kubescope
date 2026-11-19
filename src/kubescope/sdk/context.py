"""What an extension sees of the app: the contract, never the app itself.

The app hands the extension one `Context` when it starts. The classes
here only describe it (`Protocol`s) together with the permissions and
the errors that belong to the contract; the code behind them lives in
`kubescope.extensions`. Nothing in `kubescope.sdk` imports the app, so
this package can be published on its own.

The permissions catch mistakes and tell the person what an extension
does; they are not a sandbox, because an extension is Python that runs
in the app, so only install one from a source you trust.
"""

from collections.abc import Callable
from typing import Any, Protocol

from kubescope.sdk.events import Events

API_VERSION = "0"  # unstable until it is 1

PERMISSIONS = (
    "cluster.read",
    "cluster.write",
    "subprocess",
    "ui.dock",
    "ui.tab",
    "ui.settings",
    "ui.window",
    "cli",
)


class PermissionDenied(Exception):
    """The extension did not ask for the permission this needs."""


class WriteModeOff(Exception):
    """The person has not turned on the write mode."""


class ClusterAccess(Protocol):
    """The read paths of the cluster; each is a function of
    `kubescope.cluster`."""

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """The read function called `name`."""
        ...


class Settings(Protocol):
    """The preferences of one extension, apart from the app's and the
    others'."""

    def get(self, key: str, default: Any = None) -> Any:
        """What was saved under `key`, or `default`."""
        ...

    def set(self, key: str, value: Any) -> None:
        """Save `value` (anything JSON can hold) under `key`."""
        ...


class Writes(Protocol):
    """The changes to a cluster, only while the write mode is on."""

    def run(self, function: Callable[..., Any], *arguments: Any) -> Any:
        """Call one of the functions of the write mode, or raise
        `WriteModeOff`."""
        ...


class Ui(Protocol):
    """The window, for an extension that asked for `ui.window`; it is None when
    the app runs without one (a command of the terminal)."""

    window: Any  # the main window: the parent of the boxes the extension shows
    central: Any  # the widget that panels in the corner sit on

    def show_message(self, icon: str, title: str, text: str) -> None:
        """Tell the person something; `icon` is information, warning or
        critical."""
        ...

    def run_action(
        self,
        function: Callable[..., Any],
        on_success: Callable[[Any], None],
        *arguments: Any,
        on_error: Callable[[str], None] | None = None,
        quiet: bool = False,
    ) -> None:
        """Call `function` off the UI thread; the answer comes to
        `on_success`."""
        ...

    def style_box(self, box: Any) -> None:
        """Give a message box the buttons of the window."""
        ...

    def show_settings(self, section: str = "") -> None:
        """Go to the Settings, to the section of the extension named
        `section`."""
        ...

    def reserve_corner(self, owner: str, pixels: int) -> None:
        """Keep `pixels` of the corner of the window clear for `owner`; 0 gives
        it back."""
        ...


class App(Protocol):
    """What the extension may know about the app."""

    @property
    def write_mode(self) -> bool:
        """Whether the person turned on the write mode."""
        ...

    @property
    def language(self) -> str:
        """The language chosen in the Settings (`auto` follows the system)."""
        ...


class SettingsPanel(Protocol):
    """What the factory of a section of the Settings builds: a widget that has
    these two methods."""

    def load(self) -> None:
        """Show the preferences as they are saved."""
        ...

    def save(self) -> bool:
        """Keep what the person typed; False (after saying why) stops the
        save."""
        ...


class Context(Protocol):
    """What `activate(ctx)` receives."""

    id: str
    permissions: frozenset[str]
    events: Events
    settings: Settings

    @property
    def cluster(self) -> ClusterAccess:
        """The read paths of the cluster; needs `cluster.read`."""
        ...

    @property
    def writes(self) -> Writes:
        """The writes; needs `cluster.write`."""
        ...

    @property
    def current_context(self) -> str | None:
        """The cluster context the window is on."""
        ...

    def snapshot(self) -> str:
        """What the window shows, in words."""
        ...

    def invoke(self, command: str, /, **arguments: Any) -> Any:
        """Do in the window what the person could do by hand."""
        ...

    @property
    def ui(self) -> Ui | None:
        """The window; needs `ui.window`, and is None without one."""
        ...

    @property
    def app(self) -> App:
        """What the app says about itself."""
        ...

    def register_command(self, name: str, command: Callable[..., Any]) -> None:
        """Offer a command to the app, named `<id of the extension>.<name>`."""
        ...

    def add_shortcut(
        self, action: str, label: str, default: str, handler: Callable[[], None]
    ) -> None:
        """Add a keyboard shortcut the person can change in the Settings; needs
        `ui.window`."""
        ...

    def on_unload(self, callback: Callable[[], None]) -> None:
        """Call `callback` when the extension is unloaded or reloaded, to close
        what it created (a panel, a thread)."""
        ...

    def add_dock(
        self, key: str, factory: Callable[..., Any], shortcut: str = ""
    ) -> None:
        """Add a panel in the corner of the window; needs `ui.dock`."""
        ...

    def add_tab_kind(self, key: str, factory: Callable[..., Any]) -> None:
        """Add a kind of tab; needs `ui.tab`."""
        ...

    def add_settings_section(self, title: str, factory: Callable[..., Any]) -> None:
        """Add a section to the Settings; needs `ui.settings`."""
        ...

    def add_cli_command(self, name: str, run: Callable[[list[str]], int]) -> None:
        """Add a subcommand of `kubescope`; needs `cli`."""
        ...
