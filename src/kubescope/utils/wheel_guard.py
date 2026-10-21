from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QAbstractSpinBox, QApplication, QComboBox, QWidget


class WheelGuard(QObject):
    """Keeps the wheel from changing a select just because the cursor rests on
    it while the page scrolls: a select changes by a click on its list or the
    keys, never by the wheel. The wheel goes to the widget around it instead.

    The event may reach the line edit inside a spin box or an editable select,
    so the select is looked for upwards."""

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() != QEvent.Type.Wheel or not isinstance(watched, QWidget):
            return False
        select = watched
        while select is not None and not isinstance(
            select, QComboBox | QAbstractSpinBox
        ):
            select = select.parentWidget()
        if select is None:
            return False
        parent = select.parentWidget()
        if parent is not None:
            QApplication.sendEvent(parent, event)
        return True


_guards: list[WheelGuard] = []  # kept alive as long as the application


def install_wheel_guard(application: QApplication) -> None:
    guard = WheelGuard()
    _guards.append(guard)
    application.installEventFilter(guard)
