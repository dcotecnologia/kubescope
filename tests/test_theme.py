import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

from kubescope.theme import apply_light_theme

application = QApplication.instance() or QApplication([])


def test_light_theme_sets_a_light_palette_and_greys_disabled_text() -> None:
    apply_light_theme(application)

    palette = application.palette()
    assert application.style().objectName().lower() == "fusion"
    assert palette.color(QPalette.ColorRole.Window).lightness() > 200
    disabled = palette.color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text)
    assert disabled.name() == "#8a919c"
