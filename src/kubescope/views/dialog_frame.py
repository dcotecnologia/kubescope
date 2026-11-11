from typing import cast

from PySide6.QtCore import QEvent, QObject, QSize, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizeGrip,
    QWidget,
)

from kubescope.theme import themed
from kubescope.views.window_frame import control_icon

BAR_HEIGHT = 34
GRIP = 16  # the corner that resizes a window that can be resized
_WINDOWS = (Qt.WindowType.Window, Qt.WindowType.Dialog)


class DialogFrames(QObject):
    """Gives every dialog and window of the app the title bar of the main
    window, while the app is set to draw its own: a bar that moves the window
    and closes it, and a corner that resizes it.

    It is installed once, on the application, and acts on a window as it
    is first shown.
    """

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.custom = False  # the app's setting; a window already open is left as it is

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if (
            self.custom
            and event.type() == QEvent.Type.Polish
            and isinstance(watched, QWidget)
            and self.eligible(watched)
        ):
            self.frame(watched)
        return False

    @staticmethod
    def eligible(widget: QWidget) -> bool:
        """A window of the app with a layout that has not been framed: not the
        main window (it has its own bar), a menu or a tip, or a dialog the
        system draws."""
        return (
            widget.isWindow()
            and widget.windowType() in _WINDOWS
            and not isinstance(widget, QMainWindow | QFileDialog)
            and not widget.windowFlags() & Qt.WindowType.FramelessWindowHint
            and widget.layout() is not None
            and widget.property("ownBar") is None
        )

    def frame(self, widget: QWidget) -> None:
        widget.setProperty("ownBar", True)
        widget.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        bar = TitleBar(widget)
        widget.setContentsMargins(0, BAR_HEIGHT, 0, 0)  # the layout leaves room
        if widget.minimumSize() != widget.maximumSize():
            bar.grip = QSizeGrip(widget)
        bar.place()


class TitleBar(QFrame):
    """The bar at the top of a window: its title and a button to close it."""

    def __init__(self, window: QWidget) -> None:
        super().__init__(window)
        self.window_ = window
        self.grip: QSizeGrip | None = None
        self.setObjectName("dialogBar")
        self.setStyleSheet(
            f"QFrame#dialogBar {{ background: {themed('#06234a')}; }}"
            " QLabel { color: #ffffff; font-weight: bold; background: transparent; }"
            " QPushButton { border: 0; background: transparent; }"
            " QPushButton:hover { background: rgba(255, 255, 255, 40); }"
        )
        row = QHBoxLayout(self)
        row.setContentsMargins(14, 0, 4, 0)
        self.title = QLabel(window.windowTitle())
        close = QPushButton()
        close.setIcon(control_icon("close"))
        close.setIconSize(QSize(14, 14))
        close.setFixedSize(30, 26)
        close.clicked.connect(self.close_window)
        row.addWidget(self.title, 1)
        row.addWidget(close)
        window.installEventFilter(self)

    def close_window(self) -> None:
        if isinstance(self.window_, QDialog):
            self.window_.reject()
        else:
            self.window_.close()

    def place(self) -> None:
        """Put the bar along the top and the grip in the corner."""
        width, height = self.window_.width(), self.window_.height()
        self.setGeometry(0, 0, width, BAR_HEIGHT)
        self.raise_()
        if self.grip is not None:
            self.grip.setGeometry(width - GRIP, height - GRIP, GRIP, GRIP)
            self.grip.raise_()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # also called while the window is being torn down, when this is half gone
        if watched is getattr(self, "window_", None):
            if event.type() == QEvent.Type.Resize:
                self.place()
            elif event.type() == QEvent.Type.WindowTitleChange:
                self.title.setText(self.window_.windowTitle())
        return False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        handle = self.window_.windowHandle()
        if event.button() == Qt.MouseButton.LeftButton and handle is not None:
            handle.startSystemMove()
            return
        super().mousePressEvent(event)


def frames(application: QObject) -> DialogFrames:
    """The one filter of the application, made on first use."""
    found = application.findChild(DialogFrames)
    if found is None:
        found = DialogFrames(application)
        application.installEventFilter(found)
    return cast(DialogFrames, found)
