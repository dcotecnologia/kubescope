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
        themed: Callable[[str, bool], str],
        pick_item: Callable[[str, str, list[str]], tuple[str, bool]] = lambda *_: (
            "",
            False,
        ),
        show_json: Callable[[str, dict[str, Any]], None] = lambda *_: None,
        open_log: Callable[[str, str, Callable[[], str]], None] = lambda *_: None,
        add_top_bar_button: Callable[[str, QWidget], None] = lambda *_: None,
    ) -> None:
        self.window = window
        self.central = central
        self._message = message
        self.run_action = run_action
        self._style_box = style_box
        self._show_settings = show_settings
        self._reserve_corner = reserve_corner
        self._themed = themed
        self._pick_item = pick_item
        self._show_json = show_json
        self._open_log = open_log
        self._add_top_bar_button = add_top_bar_button

    def show_message(self, icon: str, title: str, text: str) -> None:
        self._message(_ICONS.get(icon, QMessageBox.Icon.Information), title, text)

    def style_box(self, box: Any) -> None:
        self._style_box(box)

    def show_settings(self, section: str = "") -> None:
        self._show_settings(section)

    def themed(self, color: str, text: bool = False) -> str:
        return self._themed(color, text)

    def reserve_corner(self, owner: str, pixels: int) -> None:
        self._reserve_corner(owner, pixels)

    def pick_item(self, title: str, label: str, items: list[str]) -> tuple[str, bool]:
        return self._pick_item(title, label, items)

    def show_json(self, title: str, document: dict[str, Any]) -> None:
        self._show_json(title, document)

    def open_log(self, title: str, name: str, read: Callable[[], str]) -> None:
        self._open_log(title, name, read)

    def add_top_bar_button(self, owner: str, button: QWidget) -> None:
        self._add_top_bar_button(owner, button)
