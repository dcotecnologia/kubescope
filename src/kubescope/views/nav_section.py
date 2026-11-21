"""A block of the side menu that folds from its title.

The title of a block (MONITORING, AWS, ...) is clicked to slide away
everything under it, and clicked again to bring it back. It has the
arrow of the entries that fold, at its right.
"""

from collections.abc import Callable

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPropertyAnimation,
    Qt,
    Signal,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QAbstractButton, QWidget

from kubescope.views.nav_chevron import NavChevron

NO_LIMIT = 16777215  # QWIDGETSIZE_MAX: the body is as tall as what is in it
DURATION_MS = 180


class SectionFold(QObject):
    """Fold or unfold the `body` of a block when its `title` is clicked."""

    toggled = Signal(bool)  # the block is folded now, by the person

    def __init__(
        self,
        title: QWidget,
        body: QWidget,
        folded: bool,
        animated: Callable[[], bool],
    ) -> None:
        super().__init__(title)
        self.title = title
        self.body = body
        self.folded = folded
        self.available = True  # whether the block has anything to show at all
        self._animated = animated
        self.chevron = NavChevron(title)
        self.chevron.set_open(not folded)
        self.animation = QPropertyAnimation(body, b"maximumHeight", self)
        self.animation.setDuration(DURATION_MS)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.finished.connect(self._settled)
        if isinstance(title, QAbstractButton):  # an entry of the menu: it clicks
            title.clicked.connect(self.toggle)
        else:  # a title: its release is the click
            title.setCursor(Qt.CursorShape.PointingHandCursor)
            title.installEventFilter(self)
        self._apply()

    def set_available(self, available: bool) -> None:
        """Show or hide the whole block, as its entries do."""
        self.available = available
        self.title.setVisible(available)
        self._apply()

    def toggle(self) -> None:
        self.set_folded(not self.folded)

    def set_folded(self, folded: bool, remember: bool = True) -> None:
        """Slide the block away or back; `remember` tells the window to keep it
        for the next run."""
        if folded == self.folded:
            return
        self.folded = folded
        self.chevron.set_open(not folded)
        self.animation.stop()
        if not self.available or not self._animated():
            self._apply()
        else:
            start = 0 if self.body.isHidden() else self.body.height()
            self.body.show()
            self.animation.setStartValue(start)
            self.animation.setEndValue(0 if folded else self.body.sizeHint().height())
            self.animation.start()
        if remember:
            self.toggled.emit(folded)

    def _apply(self) -> None:
        """The state at once, with no slide."""
        shown = self.available and not self.folded
        self.body.setMaximumHeight(NO_LIMIT)
        self.body.setVisible(shown)

    def _settled(self) -> None:
        self._apply()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if (
            watched is self.title
            and event.type() == QEvent.Type.MouseButtonRelease
            and isinstance(event, QMouseEvent)
            and event.button() == Qt.MouseButton.LeftButton
            and self.title.rect().contains(event.position().toPoint())
        ):
            self.toggle()
            return True
        return False
