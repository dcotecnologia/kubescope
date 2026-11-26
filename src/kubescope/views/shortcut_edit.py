"""The box of a shortcut in the Settings: it records a key only after the
person asked to, so a key pressed while the page is open (or the box just has
the focus) changes nothing."""

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QFocusEvent, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QKeySequenceEdit, QWidget

START_KEYS = (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space)


class ShortcutEdit(QKeySequenceEdit):
    """Click it, or press Enter or Space with it in focus, to record a key;
    leaving it stops the recording."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.recording = False
        self.editingFinished.connect(self._stop)
        self.setToolTip(self.tr("Click, then press the keys. Backspace clears it."))

    def _stop(self) -> None:
        self.recording = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.recording = True
        super().mousePressEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.recording = False
        super().focusOutEvent(event)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Type.ShortcutOverride and not self.recording:
            return QWidget.event(self, event)  # the shortcuts of the window stay on
        return super().event(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self.recording:
            super().keyPressEvent(event)
        elif event.key() in START_KEYS and not event.modifiers():
            self.recording = True  # asked from the keyboard
        else:
            event.ignore()

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if self.recording:
            super().keyReleaseEvent(event)
        else:
            event.ignore()
