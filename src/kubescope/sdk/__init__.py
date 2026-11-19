"""The API the extensions of KubeScope are written against.

An extension imports from here and from nothing else of the app. This
package imports nothing of the app either, so it can be published on its
own. The API is unstable while `API_VERSION` is below 1.
"""

from kubescope.sdk.commands import CommandError
from kubescope.sdk.context import (
    API_VERSION,
    PERMISSIONS,
    App,
    ClusterAccess,
    Context,
    PermissionDenied,
    Settings,
    SettingsPanel,
    Ui,
    WriteModeOff,
    Writes,
)
from kubescope.sdk.contributions import (
    CliCommand,
    DockContribution,
    SettingsSection,
    ShortcutContribution,
    TabKind,
)
from kubescope.sdk.events import (
    CONTEXT_CHANGED,
    EVENTS,
    LANGUAGE_CHANGED,
    SHUTDOWN,
    THEME_CHANGED,
    Events,
)

__all__ = [
    "API_VERSION",
    "App",
    "CONTEXT_CHANGED",
    "EVENTS",
    "LANGUAGE_CHANGED",
    "PERMISSIONS",
    "SHUTDOWN",
    "THEME_CHANGED",
    "CliCommand",
    "ClusterAccess",
    "CommandError",
    "Context",
    "DockContribution",
    "Events",
    "PermissionDenied",
    "Settings",
    "SettingsPanel",
    "SettingsSection",
    "ShortcutContribution",
    "TabKind",
    "Ui",
    "WriteModeOff",
    "Writes",
]
