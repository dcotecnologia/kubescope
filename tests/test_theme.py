import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from kubescope.theme import ButtonCursor, apply_light_theme

application = QApplication.instance() or QApplication([])


def test_light_theme_sets_a_light_palette_and_greys_disabled_text() -> None:
    apply_light_theme(application)

    palette = application.palette()
    assert application.style().objectName().lower() == "fusion"
    assert palette.color(QPalette.ColorRole.Window).lightness() > 200
    disabled = palette.color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text)
    assert disabled.name() == "#8a919c"


def test_enabled_buttons_get_a_pointing_hand_and_disabled_ones_an_arrow() -> None:
    apply_light_theme(application)
    apply_light_theme(application)  # installing twice must not stack filters
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
