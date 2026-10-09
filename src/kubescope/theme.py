"""Light and dark looks, chosen in Settings.

The light colors are the source of truth: the style sheet and the code
spell them out. The dark theme is a map from each light color to its
dark counterpart, applied to the style sheet and to every color the code
picks. A fixed palette keeps system themes from leaking into unstyled
widgets.
"""

import re

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QAbstractButton, QApplication

THEMES = ("light", "dark")
DEFAULT_THEME = "light"

_ROLES = {
    "light": {
        QPalette.ColorRole.Window: "#f7f7fa",
        QPalette.ColorRole.WindowText: "#20232a",
        QPalette.ColorRole.Base: "#ffffff",
        QPalette.ColorRole.AlternateBase: "#f3f4f7",
        QPalette.ColorRole.Text: "#20232a",
        QPalette.ColorRole.Button: "#ffffff",
        QPalette.ColorRole.ButtonText: "#20232a",
        QPalette.ColorRole.ToolTipBase: "#ffffff",
        QPalette.ColorRole.ToolTipText: "#20232a",
        QPalette.ColorRole.PlaceholderText: "#7b8089",
        QPalette.ColorRole.Highlight: "#6252b5",
        QPalette.ColorRole.HighlightedText: "#ffffff",
        QPalette.ColorRole.Link: "#3220a0",
    },
    "dark": {
        QPalette.ColorRole.Window: "#11141a",
        QPalette.ColorRole.WindowText: "#e6e9ee",
        QPalette.ColorRole.Base: "#1a1e26",
        QPalette.ColorRole.AlternateBase: "#20252e",
        QPalette.ColorRole.Text: "#e6e9ee",
        QPalette.ColorRole.Button: "#1a1e26",
        QPalette.ColorRole.ButtonText: "#e6e9ee",
        QPalette.ColorRole.ToolTipBase: "#20252e",
        QPalette.ColorRole.ToolTipText: "#e6e9ee",
        QPalette.ColorRole.PlaceholderText: "#7f8a99",
        QPalette.ColorRole.Highlight: "#8472e0",
        QPalette.ColorRole.HighlightedText: "#ffffff",
        QPalette.ColorRole.Link: "#a99af5",
    },
}
_DISABLED = {"light": "#8a919c", "dark": "#6b7380"}
_DISABLED_ROLES = (
    QPalette.ColorRole.WindowText,
    QPalette.ColorRole.Text,
    QPalette.ColorRole.ButtonText,
)

# Each light color and what replaces it in the dark theme. White is special: as a
# background or border it becomes the dark surface, but as text (on the navy top
# bar and the purple buttons) it stays white; see themed().
SURFACE = "#1a1e26"
_DARK = {
    # backgrounds and borders; the top bar is near black in the dark theme
    "#f7f7fa": "#11141a",
    "#f3f4f7": "#20252e",
    "#fbfbfc": "#1d222b",
    "#f6f6fa": "#20252e",
    "#eceef3": "#2a303a",
    "#e8eaee": "#2a303a",
    "#e1e3e9": "#2a303a",
    "#e6e7ed": "#2a303a",
    "#e4e5eb": "#2a303a",
    "#dfe2e9": "#2d333d",
    "#e8e9ee": "#262c36",
    "#d9dce4": "#343b47",
    "#06234a": "#07090c",
    "#123764": "#11151a",
    "#0d315d": "#13171d",
    "#2d5077": "#2b3036",
    "#1f4f87": "#2c3137",
    # text
    "#20232a": "#e6e9ee",
    "#242a33": "#e1e5ea",
    "#17191e": "#f1f3f6",
    "#16375f": "#cfe0f7",
    "#4f5966": "#9ba6b4",
    "#535d69": "#98a3b1",
    "#4d5866": "#9aa5b3",
    "#3c4149": "#aab4c1",
    "#6b7380": "#7f8a99",
    "#7b8089": "#7f8a99",
    "#8a919c": "#6b7380",
    "#b8c7dc": "#9aa4b0",
    "#d2deec": "#b8c0cb",
    "#28213f": "#ece8ff",
    # accent
    "#3220a0": "#a99af5",
    "#3020a5": "#5a46d4",
    "#4030b8": "#6b58e6",
    "#6c5fc4": "#4b3f96",
    "#6252b5": "#8472e0",
    "#4d35a8": "#b8a9f5",
    "#eee9f7": "#2a2447",
    "#f0edfa": "#2a2447",
    "#f3f1f9": "#262140",
    "#d9d3f2": "#3b3260",
    "#b9b3dc": "#5b4fa0",
    "#a9a0d6": "#5b4fa0",
    # status
    "#176b58": "#5fd0a8",
    "#e5f4eb": "#173a2e",
    "#985415": "#f0b455",
    "#fff2de": "#3d3118",
    "#a33d45": "#ff8a92",
    "#fce9ea": "#3d2226",
    "#505963": "#aab3be",
    "#eff1f3": "#2a303a",
    "#fbe4e4": "#3a2124",
    "#e2f5e8": "#1c3329",
    "#d58a2b": "#e0a030",
    "#c9484f": "#e0606a",
    "#3d9a6d": "#3fae7a",
    "#d05560": "#e0606a",
}

_active = DEFAULT_THEME


def active_theme() -> str:
    return _active


def set_theme(name: str) -> None:
    global _active
    _active = name if name in THEMES else DEFAULT_THEME


def themed(color: str, *, text: bool = False) -> str:
    """The color to use under the active theme.

    `text` marks a color that is drawn as text, so white stays white on
    the dark navy and purple surfaces.
    """
    key = color.lower()
    if _active == "light":
        return color
    if key == "#ffffff":
        return color if text else SURFACE
    return _DARK.get(key, color)


_HEX = re.compile(r"#[0-9a-fA-F]{6}\b")
_DECLARATION = re.compile(r"([a-z-]+)(\s*:\s*)([^;{}]*)")
_TEXT_PROPERTIES = frozenset({"color", "selection-color"})


def themed_stylesheet(stylesheet: str) -> str:
    """Recolor a style sheet written with the light colors."""
    if _active == "light":
        return stylesheet

    def declaration(match: re.Match[str]) -> str:
        prop, separator, value = match.groups()
        text = prop in _TEXT_PROPERTIES
        recolored = _HEX.sub(lambda hit: themed(hit.group(0), text=text), value)
        return f"{prop}{separator}{recolored}"

    return _DECLARATION.sub(declaration, stylesheet)


class ButtonCursor(QObject):
    """Show a pointing hand over every enabled button, in every window and
    dialog; style sheets cannot set a cursor."""

    _EVENTS = (QEvent.Type.Polish, QEvent.Type.EnabledChange)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if event.type() in self._EVENTS and isinstance(watched, QAbstractButton):
            watched.setCursor(
                Qt.CursorShape.PointingHandCursor
                if watched.isEnabled()
                else Qt.CursorShape.ArrowCursor
            )
        return False


def apply_theme(application: QApplication, name: str = DEFAULT_THEME) -> None:
    """Switch the whole application to a theme; windows restyle themselves."""
    set_theme(name)
    if application.findChild(ButtonCursor) is None:
        application.installEventFilter(ButtonCursor(application))
    if application.style().objectName().lower() != "fusion":
        application.setStyle("Fusion")  # restyling every widget again is slow
    palette = QPalette()
    for role, color in _ROLES[_active].items():
        palette.setColor(role, QColor(color))
    for role in _DISABLED_ROLES:
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(_DISABLED[_active]))
    application.setPalette(palette)
