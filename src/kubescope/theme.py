"""Fixed light look so system dark themes never leak into unstyled widgets."""

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

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


def apply_light_theme(application: QApplication) -> None:
    application.setStyle("Fusion")
    palette = QPalette()
    for role, color in _ROLES.items():
        palette.setColor(role, QColor(color))
    for role in _DISABLED:
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor("#8a919c"))
    application.setPalette(palette)
