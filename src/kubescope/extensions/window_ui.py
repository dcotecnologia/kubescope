"""The services of the window that an extension may use
(`kubescope.sdk.Ui`)."""

from collections.abc import Callable
from typing import Any

from PySide6.QtWidgets import QMessageBox, QWidget

_ICONS = {
    "information": QMessageBox.Icon.Information,
    "warning": QMessageBox.Icon.Warning,
    "critical": QMessageBox.Icon.Critical,
}


class WindowUi:
    """What an extension is lent of the window.

    Every call goes to the window as it is when the call is made.
    """

    def __init__(
        self,
        window: QWidget,
        central: QWidget,
        message: Callable[[QMessageBox.Icon, str, str], None],
        run_action: Callable[..., None],
        style_box: Callable[[QMessageBox], None],
        show_settings: Callable[[str], None],
        reserve_corner: Callable[[str, int], None],
    ) -> None:
        self.window = window
        self.central = central
        self._message = message
        self.run_action = run_action
        self._style_box = style_box
        self._show_settings = show_settings
        self._reserve_corner = reserve_corner

    def show_message(self, icon: str, title: str, text: str) -> None:
        self._message(_ICONS.get(icon, QMessageBox.Icon.Information), title, text)

    def style_box(self, box: Any) -> None:
        self._style_box(box)

    def show_settings(self, section: str = "") -> None:
        self._show_settings(section)

    def reserve_corner(self, owner: str, pixels: int) -> None:
        self._reserve_corner(owner, pixels)
