"""Themes: the built-in Light and Dark, and the ones people make themselves.

The light colors are the source of truth: the style sheet and the code
spell them out. A theme is a map from each light color to the color to
draw instead, applied to the style sheet, the palette, the icons and
every color the code picks. Light softens the whites and the pale tints of the
code into grays; Dark maps every color.

To make colors easy to change, the light colors are grouped into named
roles (page, text, accent, ...). A custom theme is a JSON file in the
themes folder:

{"name": "Midnight", "base": "dark", "colors": {"page": "#0b0f14"}}

It starts from its base theme and replaces the roles it lists.
"""

import json
import logging
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QAbstractButton, QApplication

from kubescope.settings import config_directory

logger = logging.getLogger(__name__)

LIGHT = "light"
DARK = "dark"
DEFAULT_THEME = DARK
WHITE = "#ffffff"

# Each role and the light colors it covers. A custom theme gives one color per
# role, so every light color in a role becomes that one color.
ROLES: dict[str, tuple[str, ...]] = {
    "page": ("#f7f7fa",),
    "surface": (WHITE,),
    "surface_alt": ("#f3f4f7", "#fbfbfc", "#f6f6fa"),
    "track": ("#eceef3", "#e8eaee"),
    "border": ("#e1e3e9", "#e6e7ed", "#e4e5eb", "#dfe2e9", "#e8e9ee", "#d9dce4"),
    "topbar": ("#06234a",),
    "topbar_brand": ("#123764",),
    "topbar_field": ("#0d315d",),
    "topbar_border": ("#2d5077",),
    "topbar_selection": ("#1f4f87",),
    "topbar_text": ("#b8c7dc", "#d2deec"),
    "text": ("#20232a", "#242a33", "#17191e", "#28213f"),
    "title": ("#16375f",),
    "muted": ("#4f5966", "#535d69", "#4d5866", "#3c4149"),
    "subtle": ("#6b7380", "#7b8089", "#8a919c"),
    "accent": ("#3220a0",),
    "accent_strong": ("#3020a5",),
    "accent_hover": ("#4030b8",),
    "accent_disabled": ("#6c5fc4",),
    "focus": ("#6252b5",),
    "badge_text": ("#4d35a8",),
    "accent_soft": ("#eee9f7", "#f0edfa", "#f3f1f9"),
    "selection": ("#d9d3f2",),
    "accent_border": ("#b9b3dc", "#a9a0d6"),
    "good": ("#176b58",),
    "good_bg": ("#e5f4eb",),
    "warning": ("#985415",),
    "warning_bg": ("#fff2de",),
    "bad": ("#a33d45",),
    "bad_bg": ("#fce9ea",),
    "idle": ("#505963",),
    "idle_bg": ("#eff1f3",),
    "problem_row": ("#fbe4e4",),
    "young_row": ("#e2f5e8",),
    "chunk_warning": ("#d58a2b",),
    "chunk_high": ("#c9484f",),
    "bar_ok": ("#3d9a6d",),
    "bar_warning": ("#e0a030",),
    "bar_bad": ("#d05560",),
}
# White drawn as text (on the top bar and the accent buttons) is its own role.
ON_ACCENT = "on_accent"
TOKENS = (*ROLES, ON_ACCENT)
_ROLE_OF = {color: role for role, colors in ROLES.items() for color in colors}


@dataclass(frozen=True)
class Theme:
    id: str
    name: str
    base: str  # the built-in theme this one starts from
    colors: dict[str, str] = field(default_factory=dict)  # light color -> color
    on_accent: str = WHITE
    builtin: bool = False


# The themes that come with the app are JSON files in this folder: Light and
# Dark, which are built in, and the others, which are copied to the themes folder
# the first time they are seen (see install_bundled_themes()).
BUNDLED_DIRECTORY = Path(__file__).resolve().parent / "themes"


def _load_builtin(theme_id: str) -> Theme:
    """A built-in theme from its file.

    Its `palette` says what each light color becomes, exactly; Light has
    none.
    """
    document = json.loads(
        (BUNDLED_DIRECTORY / f"{theme_id}.json").read_text(encoding="utf-8")
    )
    return Theme(
        theme_id,
        document["name"],
        theme_id,
        dict(document.get("palette", {})),
        builtin=True,
    )


LIGHT_THEME = _load_builtin(LIGHT)
DARK_THEME = _load_builtin(DARK)
BUILTIN = {LIGHT: LIGHT_THEME, DARK: DARK_THEME}
SURFACE = DARK_THEME.colors[WHITE]  # white as a background or border, in Dark

_active = DARK_THEME
_custom: dict[str, Theme] = {}


def themes_directory() -> Path:
    return config_directory() / "themes"


def _valid_color(value: object) -> bool:
    return (
        isinstance(value, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", value) is not None
    )


def parse_theme(theme_id: str, document: object) -> Theme:
    """Build a custom theme from its JSON document; raise ValueError if it is
    not one.

    Roles it does not list keep their base color.
    """
    if not isinstance(document, dict) or not isinstance(document.get("name"), str):
        raise ValueError("a theme needs a name")
    base = document.get("base", LIGHT)
    if base not in BUILTIN:
        raise ValueError(f"unknown base theme {base!r}")
    chosen = document.get("colors", {})
    if not isinstance(chosen, dict):
        raise ValueError("colors must be an object")
    colors = dict(BUILTIN[base].colors)
    on_accent = WHITE
    for token, value in chosen.items():
        if token not in TOKENS or not _valid_color(value):
            raise ValueError(f"bad color for {token!r}")
        if token == ON_ACCENT:
            on_accent = value.lower()
            continue
        for light_color in ROLES[token]:
            colors[light_color] = value.lower()
    return Theme(
        theme_id, document["name"].strip() or theme_id, base, colors, on_accent
    )


def install_bundled_themes(source: Path | None = None) -> list[str]:
    """Make sure the themes that came with the app are in the themes folder.

    Each one whose file is missing is copied again, whether it was never
    there or the person deleted it, so the folder always has them; a
    file that is there is never overwritten, so edits are kept. Light
    and Dark are built in and are not copied. Returns the ids copied
    now.
    """
    source = BUNDLED_DIRECTORY if source is None else source
    added: list[str] = []
    for path in sorted(source.glob("*.json")) if source.is_dir() else []:
        target = themes_directory() / path.name
        if path.stem in BUILTIN or target.exists():
            continue
        try:
            parse_theme(path.stem, json.loads(path.read_text(encoding="utf-8")))
            themes_directory().mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        except (OSError, ValueError) as error:
            logger.warning("Skipping bundled theme %s: %s", path.name, error)
            continue
        added.append(path.stem)
    if added:
        logger.info("Installed bundled themes: %s", ", ".join(added))
    return added


def load_custom_themes() -> dict[str, Theme]:
    """Read every theme file; a damaged one is skipped and logged."""
    themes: dict[str, Theme] = {}
    directory = themes_directory()
    for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            themes[path.stem] = parse_theme(path.stem, document)
        except (OSError, ValueError) as error:
            logger.warning("Skipping theme %s: %s", path.name, error)
    return themes


def available_themes() -> list[Theme]:
    """The built-in themes, then the custom ones by name."""
    custom = sorted(
        (t for t in load_custom_themes().values() if t.id not in BUILTIN),
        key=lambda theme: theme.name.casefold(),
    )
    return [LIGHT_THEME, DARK_THEME, *custom]


def bundled_theme_ids() -> set[str]:
    """The ids of the themes that come with the app, Light and Dark
    included."""
    directory = BUNDLED_DIRECTORY
    if not directory.is_dir():
        return set()
    return {path.stem for path in directory.glob("*.json")}


def can_delete_theme(theme_id: str) -> bool:
    """Only the themes the person made: the ones that come with the app
    stay."""
    return theme_id not in BUILTIN and theme_id not in bundled_theme_ids()


def delete_custom_theme(theme_id: str) -> None:
    """Remove the file of a theme the person made; the ones that come with the
    app cannot go."""
    if not can_delete_theme(theme_id):
        raise ValueError(
            f"The {theme_id} theme comes with the app and cannot be deleted"
        )
    (themes_directory() / f"{theme_id}.json").unlink(missing_ok=True)


def theme_tokens(theme: Theme) -> dict[str, str]:
    """The color of every role under a theme, for showing and editing."""
    tokens = {
        role: theme.colors.get(colors[0], colors[0]) for role, colors in ROLES.items()
    }
    tokens[ON_ACCENT] = theme.on_accent
    return tokens


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-") or "theme"


def save_custom_theme(
    name: str, base: str, tokens: dict[str, str], theme_id: str | None = None
) -> Theme:
    """Write a theme file (a new one, or `theme_id` replaced) and return it.

    Only the roles that differ from the base are stored.
    """
    base_tokens = theme_tokens(BUILTIN[base])
    changed = {t: c.lower() for t, c in tokens.items() if c.lower() != base_tokens[t]}
    if theme_id is None:
        taken = {*BUILTIN, *(p.stem for p in themes_directory().glob("*.json"))}
        stem = slugify(name)
        theme_id, number = stem, 1
        while theme_id in taken:
            number += 1
            theme_id = f"{stem}-{number}"
    document = {"name": name.strip(), "base": base, "colors": changed}
    themes_directory().mkdir(parents=True, exist_ok=True)
    path = themes_directory() / f"{theme_id}.json"
    text = json.dumps(document, indent=4, sort_keys=True)  # as the repository keeps it
    path.write_text(text + "\n", encoding="utf-8")
    return parse_theme(theme_id, document)


def active_theme() -> str:
    return _active.id


def set_theme(name: str) -> None:
    """Make a theme the active one; an unknown name means the default."""
    global _active, _custom
    _custom = load_custom_themes() if name not in BUILTIN else {}
    _active = BUILTIN.get(name) or _custom.get(name) or BUILTIN[DEFAULT_THEME]


def themed(color: str, *, text: bool = False) -> str:
    """The color to use under the active theme.

    `text` marks a color that is drawn as text, so white follows the
    theme's on-accent color there.
    """
    key = color.lower()
    if key == WHITE and text:
        return _active.on_accent
    return _active.colors.get(key, color)


_HEX = re.compile(r"#[0-9a-fA-F]{6}\b")
_DECLARATION = re.compile(r"([a-z-]+)(\s*:\s*)([^;{}]*)")
_TEXT_PROPERTIES = frozenset({"color", "selection-color"})


def themed_stylesheet(stylesheet: str) -> str:
    """Recolor a style sheet written with the light colors."""
    if not _active.colors and _active.on_accent == WHITE:
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

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
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
    for role, color, text in (
        (QPalette.ColorRole.Window, "#f7f7fa", False),
        (QPalette.ColorRole.WindowText, "#20232a", False),
        (QPalette.ColorRole.Base, WHITE, False),
        (QPalette.ColorRole.AlternateBase, "#f3f4f7", False),
        (QPalette.ColorRole.Text, "#20232a", False),
        (QPalette.ColorRole.Button, WHITE, False),
        (QPalette.ColorRole.ButtonText, "#20232a", False),
        (QPalette.ColorRole.ToolTipBase, WHITE, False),
        (QPalette.ColorRole.ToolTipText, "#20232a", False),
        (QPalette.ColorRole.PlaceholderText, "#7b8089", False),
        (QPalette.ColorRole.Highlight, "#6252b5", False),
        (QPalette.ColorRole.HighlightedText, WHITE, True),
        (QPalette.ColorRole.Link, "#3220a0", False),
    ):
        palette.setColor(role, QColor(themed(color, text=text)))
    for role in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(themed("#8a919c")))
    application.setPalette(palette)
