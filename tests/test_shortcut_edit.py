import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QFocusEvent, QKeyEvent, QKeySequence
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QWidget

from kubescope.views.shortcut_edit import ShortcutEdit
from tests.qt import get_application

application = get_application()


def _edit() -> ShortcutEdit:
    host = QWidget()
    edit = ShortcutEdit(host)
    edit.setKeySequence(QKeySequence("Ctrl+R"))
    host.show()
    edit.setFocus()
    edit.host = host  # type: ignore[attr-defined]  # kept alive with the box
    return edit


def test_a_key_pressed_with_the_box_in_focus_changes_nothing() -> None:
    edit = _edit()
    QTest.keyClick(edit, Qt.Key.Key_P, Qt.KeyboardModifier.ControlModifier)
    QTest.keyClick(edit, Qt.Key.Key_Backspace)
    assert edit.keySequence().toString() == "Ctrl+R"
    assert not edit.recording


def test_a_key_that_is_a_shortcut_of_the_window_is_left_to_it() -> None:
    edit = _edit()
    event = QKeyEvent(
        QEvent.Type.ShortcutOverride,
        Qt.Key.Key_R,
        Qt.KeyboardModifier.ControlModifier,
    )
    event.setAccepted(False)
    edit.event(event)
    assert not event.isAccepted()  # not asked to record: the shortcut can fire


def test_a_click_or_enter_starts_the_recording_and_leaving_stops_it() -> None:
    edit = _edit()
    QTest.mouseClick(edit, Qt.MouseButton.LeftButton)
    assert edit.recording
    QTest.keyClick(edit, Qt.Key.Key_P, Qt.KeyboardModifier.ControlModifier)
    assert edit.keySequence().toString() == "Ctrl+P"

    edit.focusOutEvent(QFocusEvent(QEvent.Type.FocusOut))  # the person goes elsewhere
    assert not edit.recording

    edit.setFocus()
    QTest.keyClick(edit, Qt.Key.Key_Return)  # from the keyboard
    assert edit.recording
    QTest.keyClick(edit, Qt.Key.Key_Q, Qt.KeyboardModifier.ControlModifier)
    assert edit.keySequence().toString() == "Ctrl+Q"
    edit.editingFinished.emit()  # the box is done with the sequence
    assert not edit.recording
