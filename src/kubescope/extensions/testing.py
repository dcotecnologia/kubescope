"""What the tests of an extension use to run its pages, so they import no Qt
class: the application, the widgets of a page found by kind, the dialogs and
menus that must not block, and a click.

An extension is tested with the real components of the app (a
development dependency of its tests), which draw on the offscreen
platform.
"""

import os
import struct
import zlib
from collections.abc import Callable, Iterator
from typing import Any

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QCoreApplication, QEvent, QPointF, Qt  # noqa: E402
from PySide6.QtGui import QMouseEvent  # noqa: E402
from PySide6.QtWidgets import (  # noqa: E402
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTimeEdit,
    QWidget,
)

from kubescope.views.container_states import BADGE_ROLE  # noqa: E402

KINDS: dict[str, type[QWidget]] = {
    "button": QPushButton,
    "label": QLabel,
    "combo": QComboBox,
    "text": QPlainTextEdit,
    "table": QTableWidget,
    "check": QCheckBox,
    "line": QLineEdit,
    "spin": QSpinBox,
    "time": QTimeEdit,
    "frame": QFrame,
    "scroll": QScrollArea,
    "list": QListWidget,
}


def application() -> QApplication:
    """The application of the tests, made when it is first asked."""
    existing = QApplication.instance()
    return existing if isinstance(existing, QApplication) else QApplication([])


def settle() -> None:
    """Let what was posted (a timer of 0, a deletion) happen."""
    QCoreApplication.processEvents()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)


def cleanup() -> Iterator[None]:
    """For the fixture of a test: delete the windows it showed before the
    application goes away, because a window that outlives it crashes the run
    when it ends."""
    application()
    before = set(QApplication.topLevelWidgets())
    yield
    for widget in set(QApplication.topLevelWidgets()) - before:
        widget.close()
        widget.deleteLater()
    settle()


def find_all(widget: Any, kind: str) -> list[Any]:
    """Every widget of that kind (`button`, `label`, `combo`, `text`, `table`,
    `check`, `line`, `spin`, `time`, `frame`, `scroll`, `list`) in `widget`."""
    return list(widget.findChildren(KINDS[kind]))


def find(widget: Any, kind: str) -> Any:
    """The first widget of that kind in `widget`."""
    return widget.findChild(KINDS[kind])


def buttons(widget: Any) -> dict[str, Any]:
    """The buttons in `widget`, by their text."""
    return {one.text(): one for one in find_all(widget, "button")}


def texts(widget: Any, kind: str = "label") -> list[str]:
    """The text of every widget of that kind in `widget`."""
    return [
        one.toPlainText() if kind == "text" else one.text()
        for one in find_all(widget, kind)
    ]


def badge_of(item: Any) -> Any:
    """The colors a cell was given as a badge, or `None`."""
    return item.data(BADGE_ROLE)


def refuse_modals(monkeypatch: Any) -> None:
    """A test that opens a dialog, a message box or a menu fails instead of
    hanging."""

    def refuse(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("a modal window was opened and nobody answers it")

    monkeypatch.setattr(QDialog, "exec", refuse)
    monkeypatch.setattr(QMessageBox, "exec", refuse)
    monkeypatch.setattr(QMenu, "exec", refuse)


def answer_dialogs(monkeypatch: Any, act: Callable[[Any], Any]) -> None:
    """Run `act(dialog)` when a dialog is executed, and take it as `Rejected`
    unless it says otherwise by returning a number."""
    monkeypatch.setattr(QDialog, "exec", lambda dialog: act(dialog) or 0)


def click(
    widget: Any, x: float = 5, y: float = 5, kind: str = "press", button: str = "left"
) -> None:
    """A click (`press`, `release` or `move`) of the `left` or `right` button
    on a widget, at a place of it."""
    types = {
        "press": QEvent.Type.MouseButtonPress,
        "release": QEvent.Type.MouseButtonRelease,
        "move": QEvent.Type.MouseMove,
    }
    which = {
        "left": Qt.MouseButton.LeftButton,
        "right": Qt.MouseButton.RightButton,
    }[button]
    point = QPointF(x, y)
    QApplication.sendEvent(
        widget,
        QMouseEvent(
            types[kind],
            point,
            widget.mapToGlobal(point),
            which,
            which,
            Qt.KeyboardModifier.NoModifier,
        ),
    )


def still_panels(monkeypatch: Any) -> None:
    """The panels of the app (the chat's, the notices') show and go at once, so
    a test does not wait for their slide."""
    from kubescope.extensions import chat_dock, side_panel

    monkeypatch.setattr(chat_dock, "ANIMATION_MS", 0)
    monkeypatch.setattr(side_panel, "SLIDE_MS", 0)


def png_bytes(
    width: int = 8, height: int = 8, color: tuple[int, int, int] = (255, 0, 0)
) -> bytes:
    """A solid picture, as the bytes of a PNG, made by hand so a test needs no
    image class."""

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    row = b"\x00" + bytes(color) * width
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(row * height))
        + chunk(b"IEND", b"")
    )


def write_png(path: Any, **options: Any) -> None:
    """Write a solid picture to `path`."""
    path.write_bytes(png_bytes(**options))
