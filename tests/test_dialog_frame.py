import pytest
from PySide6.QtCore import QEvent, QObject, QPoint, Qt
from PySide6.QtGui import QWindow
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)

from kubescope.views import dialog_frame
from kubescope.views.dialog_frame import BAR_HEIGHT, DialogFrames, TitleBar
from tests.qt import get_application

application = get_application()


@pytest.fixture(autouse=True)
def _frames():
    """The filter of the application, on while a test runs and off after."""
    frame = dialog_frame.frames(application)
    frame.custom = True
    before = set(application.topLevelWidgets())
    yield frame
    frame.custom = False
    for widget in set(application.topLevelWidgets()) - before:
        widget.close()
        widget.deleteLater()
    application.sendPostedEvents(None, QEvent.Type.DeferredDelete)


def _dialog(fixed: bool = False) -> QDialog:
    dialog = QDialog()
    dialog.setWindowTitle("Hello")
    QVBoxLayout(dialog).addWidget(QLabel("content"))
    if fixed:
        dialog.setFixedSize(300, 200)
    return dialog


def _close(dialog: QWidget) -> QPushButton:
    button = _bar(dialog).findChild(QPushButton)
    assert button is not None
    return button


def _bar(dialog: QWidget) -> TitleBar:
    bar = dialog.findChild(TitleBar)
    assert bar is not None
    return bar


def test_a_dialog_gets_the_bar_of_the_app_when_it_is_shown() -> None:
    dialog = _dialog()
    dialog.show()

    assert dialog.windowFlags() & Qt.WindowType.FramelessWindowHint
    bar = _bar(dialog)
    assert bar.title.text() == "Hello" and bar.height() == BAR_HEIGHT
    assert dialog.contentsMargins().top() == BAR_HEIGHT  # the layout leaves room
    assert bar.grip is not None and dialog.findChild(QSizeGrip) is bar.grip

    dialog.setWindowTitle("Other")
    dialog.resize(500, 400)
    assert bar.title.text() == "Other" and bar.width() == 500
    assert bar.grip.geometry().right() <= 500


def test_the_close_button_rejects_a_dialog_and_closes_a_window() -> None:
    dialog = _dialog()
    dialog.show()
    _close(dialog).click()
    assert not dialog.isVisible() and dialog.result() == QDialog.DialogCode.Rejected

    window = QWidget(None, Qt.WindowType.Window)
    QVBoxLayout(window)
    window.show()
    _close(window).click()
    assert not window.isVisible()


def test_a_dialog_of_a_fixed_size_has_no_corner_to_drag() -> None:
    dialog = _dialog(fixed=True)
    dialog.show()
    assert _bar(dialog).grip is None


def test_the_bar_moves_the_window_with_the_left_button(monkeypatch) -> None:
    dialog = _dialog()
    dialog.show()
    moves = []
    monkeypatch.setattr(QWindow, "startSystemMove", lambda self: moves.append(1))

    QTest.mouseClick(_bar(dialog), Qt.MouseButton.LeftButton, pos=QPoint(5, 5))
    QTest.mouseClick(_bar(dialog), Qt.MouseButton.RightButton, pos=QPoint(5, 5))

    assert moves == [1]


def test_what_is_not_an_ordinary_window_is_left_alone() -> None:
    main = QMainWindow()
    popup = QWidget(None, Qt.WindowType.Popup)
    QVBoxLayout(popup)
    bare = QDialog()  # no layout
    files = QFileDialog()
    own = _dialog()
    own.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
    parent = _dialog()
    child = QWidget(parent)
    QVBoxLayout(child)

    for widget in (main, popup, bare, files, own, child):
        assert not DialogFrames.eligible(widget)
    assert DialogFrames.eligible(_dialog())

    for widget in (popup, bare, own):
        widget.show()
        assert widget.findChild(TitleBar) is None


def test_with_the_system_bar_on_nothing_changes(_frames) -> None:
    _frames.custom = False
    dialog = _dialog()
    dialog.show()
    assert dialog.findChild(TitleBar) is None
    assert not dialog.windowFlags() & Qt.WindowType.FramelessWindowHint


def test_a_window_is_framed_only_once() -> None:
    dialog = _dialog()
    dialog.show()
    dialog.hide()
    dialog.show()
    assert len(dialog.findChildren(TitleBar)) == 1


def test_the_filter_is_made_once_and_ignores_other_objects() -> None:
    assert dialog_frame.frames(application) is dialog_frame.frames(application)
    assert (
        dialog_frame.frames(application).eventFilter(
            QObject(), QEvent(QEvent.Type.Polish)
        )
        is False
    )
