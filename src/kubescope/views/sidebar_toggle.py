"""The button of the header that hides the side menu and brings it back.

The menu slides toward the left edge until it is gone, and out of it
again, by its width: the width is what moves, so the page grows into the
room it leaves.
"""

from collections.abc import Callable

from PySide6.QtCore import QEasingCurve, QObject, QVariantAnimation, Signal
from PySide6.QtWidgets import QAbstractButton, QWidget

DURATION_MS = 220


class SidebarToggle(QObject):
    """Click the button and the side menu slides away; click it again and it
    slides back."""

    toggled = Signal(bool)  # the menu is hidden now

    def __init__(
        self,
        sidebar: QWidget,
        button: QAbstractButton,
        width: Callable[[], int],
        animated: Callable[[], bool],
        collapsed: bool = False,
    ) -> None:
        super().__init__(sidebar)
        self.sidebar = sidebar
        self.button = button
        self._width = width  # what the menu is wide when it is shown
        self._animated = animated
        self.collapsed = collapsed
        self.animation = QVariantAnimation(self)
        self.animation.setDuration(DURATION_MS)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.valueChanged.connect(self._resize)
        self.animation.finished.connect(self._settled)
        self.button.clicked.connect(self.toggle)
        if collapsed:
            sidebar.hide()

    def toggle(self) -> None:
        self.collapse() if not self.collapsed else self.expand()

    def collapse(self) -> None:
        """Slide the menu away."""
        if self.collapsed:
            return
        self.collapsed = True
        self._slide(self.sidebar.width(), 0)
        self.toggled.emit(True)

    def expand(self) -> None:
        """Bring the menu back at its width."""
        if not self.collapsed:
            return
        self.collapsed = False
        self.sidebar.setFixedWidth(0)
        self.sidebar.show()
        self._slide(0, self._width())
        self.toggled.emit(False)

    def _slide(self, start: int, end: int) -> None:
        self.animation.stop()
        if not self._animated():
            self._resize(end)
            self._settled()
            return
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

    def _resize(self, width: object) -> None:
        self.sidebar.setFixedWidth(int(width))  # type: ignore[call-overload]

    def _settled(self) -> None:
        if self.collapsed:
            self.sidebar.hide()
        else:
            self.sidebar.setFixedWidth(self._width())
