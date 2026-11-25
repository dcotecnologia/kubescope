import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QComboBox, QWidget

from kubescope.views.drop_down import GAP, open_below
from tests.qt import get_application

application = get_application()
KEPT: list[QWidget] = []  # until the end: a widget that goes first crashes Qt


def _combo() -> QComboBox:
    host = QWidget()
    host.resize(400, 300)
    combo = QComboBox(host)
    combo.addItems(["prod", "staging", "a-longer-context-name"])
    combo.setGeometry(20, 20, 150, 32)
    KEPT.append(host)
    host.show()
    return combo


def test_the_list_hangs_from_the_bottom_edge_as_wide_as_the_select() -> None:
    combo = _combo()
    open_below(combo, lambda color, _text: color)

    combo.showPopup()

    popup = combo.view().window()
    below = combo.mapToGlobal(QPoint(0, combo.height() + GAP))
    assert popup.pos() == below
    assert popup.width() >= combo.width()
    combo.hidePopup()


def test_the_colors_are_asked_again_when_the_theme_changes() -> None:
    combo = _combo()
    open_below(combo, lambda color, _text: "#111111")
    first = combo.view().window().styleSheet()
    open_below(combo, lambda color, _text: "#222222")  # the same select, a new theme

    assert "#111111" in first
    assert "#222222" in combo.view().window().styleSheet()
    assert len(combo.findChildren(type(combo._below))) == 1  # type: ignore[attr-defined]
