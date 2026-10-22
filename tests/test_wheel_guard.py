from typing import cast

from PySide6.QtCore import QEvent, QObject, QPoint, QPointF, Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QApplication, QComboBox, QSpinBox, QWidget

from kubescope.utils import wheel_guard
from kubescope.utils.wheel_guard import WheelGuard, install_wheel_guard


def _wheel() -> QWheelEvent:
    return QWheelEvent(
        QPointF(2, 2),
        QPointF(2, 2),
        QPoint(0, 0),
        QPoint(0, -120),
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
        Qt.ScrollPhase.NoScrollPhase,
        False,
    )


class Page(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.wheeled = 0

    def wheelEvent(self, event) -> None:
        self.wheeled += 1


def test_the_wheel_goes_to_the_page_and_never_changes_a_select() -> None:
    guard = WheelGuard()
    page = Page()
    combo = QComboBox(page)
    combo.addItems(["a", "b", "c"])
    spin = QSpinBox(page)
    page.show()

    assert guard.eventFilter(combo, _wheel()) is True  # swallowed, not changed
    assert guard.eventFilter(spin, _wheel()) is True
    assert guard.eventFilter(spin.lineEdit(), _wheel()) is True  # inside the spin box
    assert page.wheeled == 3 and combo.currentIndex() == 0

    combo.setFocus()
    QApplication.processEvents()
    assert guard.eventFilter(combo, _wheel()) is True  # focus changes nothing

    assert guard.eventFilter(page, _wheel()) is False  # not a select
    assert guard.eventFilter(combo, QEvent(QEvent.Type.Show)) is False
    assert guard.eventFilter(QObject(), _wheel()) is False  # not even a widget
    lone = QComboBox()  # no widget around it: nothing to pass the wheel to
    assert guard.eventFilter(lone, _wheel()) is True
    page.close()


def test_the_guard_is_installed_on_the_application() -> None:
    installed = []

    class Application:
        def installEventFilter(self, guard) -> None:
            installed.append(guard)

    before = len(wheel_guard._guards)
    install_wheel_guard(cast(QApplication, Application()))

    assert len(installed) == 1 and len(wheel_guard._guards) == before + 1
