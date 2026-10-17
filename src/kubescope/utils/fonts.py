"""The fonts the app ships, so it looks the same on every system.

Noto Sans is the interface font and Noto Sans Mono shows code: JSON and
logs. Both are under the SIL Open Font License (see
assets/fonts/LICENSE.txt).
"""

import logging
from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)

# __file__ points into the bundle once frozen, so anchor on the package
FONTS_DIRECTORY = Path(__file__).resolve().parent.parent / "assets" / "fonts"
UI_FAMILY = "Noto Sans"
CODE_FAMILY = "Noto Sans Mono"
UI_POINT_SIZE = 9


def load_fonts() -> list[str]:
    """Register the shipped font files; return the families that were added."""
    families: list[str] = []
    for path in sorted(FONTS_DIRECTORY.glob("*.ttf")):
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id < 0:
            logger.warning("Could not load the font %s", path.name)
            continue
        families.extend(
            family
            for family in QFontDatabase.applicationFontFamilies(font_id)
            if family not in families
        )
    return families


def code_font() -> QFont:
    """The font for JSON and logs; any monospace one if ours is missing."""
    font = QFont(CODE_FAMILY)
    font.setStyleHint(QFont.StyleHint.Monospace)
    return font


def apply_fonts(application: QApplication) -> None:
    """Load the shipped fonts and make Noto Sans the font of every widget."""
    load_fonts()
    application.setFont(QFont(UI_FAMILY, UI_POINT_SIZE))
