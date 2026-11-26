"""A select whose list always opens below it, in a rounded card.

The list of a select is drawn over the select by some styles, and above
it when the screen is short below. Here it hangs from the bottom edge,
as wide as the select, whatever the style.
"""

from collections.abc import Callable

from PySide6.QtCore import QEvent, QObject, QPoint, Qt
from PySide6.QtWidgets import QComboBox, QFrame, QWidget

GAP = 4  # pixels between the select and its list
ROWS = 10  # the rows the list shows before it scrolls


class OpenBelow(QObject):
    """Moves the list of a select to hang from its bottom edge when it
    shows."""

    def __init__(self, combo: QComboBox) -> None:
        super().__init__(combo)
        self.combo = combo

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Show and isinstance(watched, QWidget):
            combo = self.combo
            width = max(combo.width(), watched.width())
            watched.setFixedWidth(width)
            watched.move(combo.mapToGlobal(QPoint(0, combo.height() + GAP)))
        return False


def open_below(combo: QComboBox, style: Callable[[str, bool], str]) -> None:
    """Make the list of `combo` open below it, with rounded corners, roomy rows
    and the colors `style` gives for the theme (called as `style(color, text)`
    with the colors of the top bar)."""
    container = combo.view().window()
    if getattr(combo, "_below", None) is None:
        below = OpenBelow(combo)
        container.installEventFilter(below)
        combo._below = below  # type: ignore[attr-defined]  # kept as long as it lives
        combo.setMaxVisibleItems(ROWS)
        combo.view().setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        container.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        container.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint, True)
        container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        if isinstance(container, QFrame):
            container.setFrameShape(QFrame.Shape.NoFrame)
    container.setStyleSheet(
        "QFrame { background: transparent; border: 0; }"
        "QAbstractItemView {"
        f" background: {style('#0d315d', False)};"
        f" color: {style('#ffffff', True)};"
        f" border: 1px solid {style('#2d5077', False)}; border-radius: 10px;"
        " padding: 5px; outline: 0; }"
        "QAbstractItemView::item { min-height: 26px; padding: 0 10px;"
        " border-radius: 6px; }"
        f"QAbstractItemView::item:hover {{ background: {style('#16406f', False)}; }}"
        "QAbstractItemView::item:selected {"
        f" background: {style('#1f4f87', False)};"
        f" color: {style('#ffffff', True)}; }}"
    )
