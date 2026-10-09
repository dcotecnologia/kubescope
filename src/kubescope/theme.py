"""Fixed light look so system dark themes never leak into unstyled widgets."""

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QAbstractButton, QApplication

_ROLES = {
    QPalette.ColorRole.Window: "#f7f7fa",
    QPalette.ColorRole.WindowText: "#20232a",
    QPalette.ColorRole.Base: "#ffffff",
    QPalette.ColorRole.AlternateBase: "#f3f4f7",
    QPalette.ColorRole.Text: "#20232a",
    QPalette.ColorRole.Button: "#ffffff",
    QPalette.ColorRole.ButtonText: "#20232a",
    QPalette.ColorRole.ToolTipBase: "#ffffff",
    QPalette.ColorRole.ToolTipText: "#20232a",
    QPalette.ColorRole.PlaceholderText: "#7b8089",
    QPalette.ColorRole.Highlight: "#6252b5",
    QPalette.ColorRole.HighlightedText: "#ffffff",
    QPalette.ColorRole.Link: "#3220a0",
}
_DISABLED = (
    QPalette.ColorRole.WindowText,
    QPalette.ColorRole.Text,
    QPalette.ColorRole.ButtonText,
)


class ButtonCursor(QObject):
    """Show a pointing hand over every enabled button, in every window and
    dialog; style sheets cannot set a cursor."""

    _EVENTS = (QEvent.Type.Polish, QEvent.Type.EnabledChange)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if event.type() in self._EVENTS and isinstance(watched, QAbstractButton):
            watched.setCursor(
                Qt.CursorShape.PointingHandCursor
                if watched.isEnabled()
                else Qt.CursorShape.ArrowCursor
            )
        return False


def apply_light_theme(application: QApplication) -> None:
    if application.findChild(ButtonCursor) is None:
        application.installEventFilter(ButtonCursor(application))
    application.setStyle("Fusion")
    palette = QPalette()
    for role, color in _ROLES.items():
        palette.setColor(role, QColor(color))
    for role in _DISABLED:
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor("#8a919c"))
    application.setPalette(palette)
