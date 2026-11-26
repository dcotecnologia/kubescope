"""Names for the controls that a screen reader would otherwise read as
"button", with no word to tell which one."""

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QAbstractButton, QLineEdit, QToolButton, QWidget


def _own_name(button: QAbstractButton) -> str:
    """The name of a button that Qt makes inside a widget, and that has no
    tooltip: the corner of a table and the clear button of a search box."""
    if button.objectName() == "qt_tableview_cornerbutton":
        return QCoreApplication.translate("Accessibility", "Select all")
    if isinstance(button, QToolButton) and isinstance(button.parent(), QLineEdit):
        return QCoreApplication.translate("Accessibility", "Clear")
    return ""


def name_icon_buttons(root: QWidget) -> list[QAbstractButton]:
    """Give every button without text, and without an accessible name, the one
    of its tooltip; return the ones left with no name at all."""
    unnamed: list[QAbstractButton] = []
    for button in root.findChildren(QAbstractButton):
        if button.text().strip() or button.accessibleName():
            continue
        name = button.toolTip() or _own_name(button)
        if name:
            button.setAccessibleName(name)
        else:
            unnamed.append(button)
    return unnamed
