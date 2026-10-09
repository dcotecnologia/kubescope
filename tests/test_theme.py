import os
import re
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from kubescope import theme
from kubescope.theme import (
    SURFACE,
    ButtonCursor,
    active_theme,
    apply_theme,
    set_theme,
    themed,
    themed_stylesheet,
)

ROOT = Path(__file__).resolve().parents[1]
application = QApplication.instance() or QApplication([])


def test_light_theme_sets_a_light_palette_and_greys_disabled_text() -> None:
    apply_theme(application)

    palette = application.palette()
    assert application.style().objectName().lower() == "fusion"
    assert palette.color(QPalette.ColorRole.Window).lightness() > 200
    disabled = palette.color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text)
    assert disabled.name() == "#8a919c"


def test_enabled_buttons_get_a_pointing_hand_and_disabled_ones_an_arrow() -> None:
    apply_theme(application)
    apply_theme(application)  # installing twice must not stack filters
    assert len(application.findChildren(ButtonCursor)) == 1

    button = QPushButton("Go")
    button.ensurePolished()
    assert button.cursor().shape() == Qt.CursorShape.PointingHandCursor

    button.setEnabled(False)
    assert button.cursor().shape() == Qt.CursorShape.ArrowCursor
    button.setEnabled(True)
    assert button.cursor().shape() == Qt.CursorShape.PointingHandCursor

    label = QLabel("text")
    label.ensurePolished()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor


def test_light_colors_pass_through_and_dark_ones_are_mapped() -> None:
    assert themed("#20232a") == "#20232a"
    assert (
        themed_stylesheet("QLabel { color: #20232a; }") == "QLabel { color: #20232a; }"
    )

    set_theme("dark")
    assert active_theme() == "dark"
    assert themed("#20232A") == "#e6e9ee"  # case does not matter
    assert themed("#e0a030") == "#e0a030"  # the same warning orange in both themes
    assert themed("#123456") == "#123456"  # unknown colors are left alone

    set_theme("neon")  # not a theme: back to the default
    assert active_theme() == "light"


def test_white_is_a_surface_in_dark_but_stays_white_as_text() -> None:
    set_theme("dark")

    assert themed("#ffffff") == SURFACE
    assert themed("#ffffff", text=True) == "#ffffff"

    recolored = themed_stylesheet(
        "QComboBox#contextCombo { background: #0d315d; color: #ffffff;"
        " border: 1px solid #2d5077; selection-color: #ffffff; }\n"
        'QFrame[card="true"] { background: #ffffff; border: 1px solid #dfe2e9; }\n'
        "QComboBox#c:disabled { color: #6b7380; }"
    )
    assert "color: #ffffff;" in recolored and "selection-color: #ffffff" in recolored
    assert f"background: {SURFACE}" in recolored
    assert "#13171d" in recolored and "#2b3036" in recolored  # navy becomes black
    assert "border: 1px solid #2d333d" in recolored
    assert "color: #7f8a99" in recolored


def test_the_dark_top_bar_is_black_not_navy() -> None:
    set_theme("dark")

    def lightness(color: str) -> int:
        return QColor(color).lightness()

    assert lightness(themed("#06234a")) < 15  # the bar itself
    assert lightness(themed("#0d315d")) < 30  # the context selector on it
    for navy in ("#06234a", "#123764", "#0d315d", "#2d5077", "#1f4f87"):
        color = QColor(themed(navy))
        assert abs(color.red() - color.blue()) < 16  # no blue tint left


def test_every_color_the_app_uses_has_a_dark_counterpart() -> None:
    sources = [
        ROOT / "src/kubescope/ui/main_window.ui",
        ROOT / "src/kubescope/window.py",
        ROOT / "src/kubescope/widgets.py",
    ]
    used = {
        color.lower()
        for source in sources
        for color in re.findall(
            r"#[0-9a-fA-F]{6}\b", source.read_text(encoding="utf-8")
        )
    }
    # white is handled by themed(); the warning orange is the same in both themes
    unmapped = used - set(theme._DARK) - {"#ffffff", "#e0a030"}

    assert unmapped == set(), f"add dark counterparts for {sorted(unmapped)}"


def test_applying_a_theme_switches_the_palette() -> None:
    apply_theme(application, "dark")
    assert application.palette().color(QPalette.ColorRole.Window).name() == "#11141a"
    disabled = application.palette().color(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text
    )
    assert disabled.name() == "#6b7380"

    apply_theme(application, "light")
    assert application.palette().color(QPalette.ColorRole.Window).name() == "#f7f7fa"


def test_a_theme_always_runs_on_the_fusion_style() -> None:
    application.setStyle("Windows")
    assert application.style().objectName().lower() != "fusion"

    apply_theme(application, "dark")

    assert application.style().objectName().lower() == "fusion"
    apply_theme(application, "light")
    assert application.style().objectName().lower() == "fusion"
