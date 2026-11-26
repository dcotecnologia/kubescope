"""The actions of a table of an extension, as the lists of the app have them.

The buttons of its row of actions show only while rows are checked (the
bar is for what works on many). For one row there are a ⋯ button on the
row under the pointer and the right click, both with the menu of the
same actions.
"""

from collections.abc import Callable
from functools import partial
from typing import cast

from PySide6.QtCore import QEvent, QMetaMethod, QObject, QPoint, Qt, QTimer
from PySide6.QtGui import QContextMenuEvent, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import QHBoxLayout, QMenu, QPushButton, QTableWidget, QWidget

from kubescope.views.check_header import CheckHeader
from kubescope.views.row_menu_button import RowMenuButton


class RowActions(QObject):
    """Wires a table, its buttons of actions and the bar that holds them."""

    def __init__(
        self,
        table: QTableWidget,
        buttons: list[QPushButton],
        bar: QWidget | None = None,
        open_icon: QIcon | None = None,
        row_keys: Callable[[], dict[str, str]] = lambda: {},
        icon_names: dict[int, str] | None = None,
        row: QHBoxLayout | None = None,
    ) -> None:
        super().__init__(table)
        self._row = row  # the layout the bar is in, where buttons may be added later
        self._row_keys = row_keys
        self._icon_names = icon_names if icon_names is not None else {}
        self._keys: dict[str, QShortcut] = {}
        self.table = table
        self.buttons = buttons
        self.bar = bar
        self._open_icon = open_icon or QIcon()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(0)  # the boxes change in bursts: look once
        self._timer.timeout.connect(self.sync)
        table.itemChanged.connect(lambda _item: self._timer.start())
        model = table.model()
        for signal in (model.rowsInserted, model.rowsRemoved, model.modelReset):
            signal.connect(lambda *_a: self._timer.start())
        header = table.horizontalHeader()
        if isinstance(header, CheckHeader):
            header.toggled.connect(lambda _on: self._timer.start())
        self.menu_button = RowMenuButton(table)
        self.menu_button.requested.connect(self.menu_requested)
        table.viewport().installEventFilter(self)
        self.apply_keys()
        self.sync()
        QTimer.singleShot(0, self, self.adopt)  # buttons the page adds as it is built

    def apply_keys(self, keys: dict[str, str] | None = None) -> None:
        """Put the keys of a row (the ones of the lists of the app, from the
        Settings) on the table: they act while it has the focus."""
        for action, key in (self._row_keys() if keys is None else keys).items():
            shortcut = self._keys.get(action)
            if shortcut is None:
                shortcut = QShortcut(self.table)
                shortcut.setContext(Qt.ShortcutContext.WidgetShortcut)
                shortcut.activated.connect(partial(self.key_pressed, action))
                self._keys[action] = shortcut
            shortcut.setKey(QKeySequence(key))

    def key_pressed(self, action: str) -> None:
        """Enter does the main thing of the page for the row picked (what its
        double click does, else its first button); Delete presses the button
        with the bin."""
        row = self.table.currentRow()
        if row < 0:
            return
        if action == "row_delete":
            self._press(self._button_with_icon("trash"))
        elif self._opens_on_double_click():
            self.table.cellDoubleClicked.emit(row, 0)
        else:
            self._press(next((b for b in self.buttons if self._offered(b)), None))

    def _offered(self, button: QPushButton) -> bool:
        return not button.isHidden() and button.isEnabled()

    def _press(self, button: QPushButton | None) -> None:
        if button is not None and self._offered(button):
            button.click()

    def _button_with_icon(self, name: str) -> QPushButton | None:
        for button in self.buttons:
            if self._icon_names.get(button.icon().cacheKey()) == name:
                return button
        return None

    def has_own_menu(self) -> bool:
        """Whether the page of the extension has its own menu for a row (it
        connected to the right click), which is then the one to open."""
        signal = QMetaMethod.fromSignal(self.table.customContextMenuRequested)
        return self.table.isSignalConnected(signal)

    def menu_requested(self, position: QPoint) -> None:
        """The ⋯ of a row: the menu of the page when it has one, else ours."""
        if self.has_own_menu():
            self.table.selectRow(self.table.rowAt(position.y()))
            self.table.customContextMenuRequested.emit(position)
        else:
            self.show_menu(position)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """The right click: the page's own menu when it has one, else ours."""
        if event.type() == QEvent.Type.ContextMenu and not self.has_own_menu():
            self.show_menu(cast(QContextMenuEvent, event).pos())
            return True
        return False

    def checked_rows(self) -> int:
        """How many rows that show have their box checked."""
        header = self.table.horizontalHeader()
        if not isinstance(header, CheckHeader) or header.column < 0:
            return 0
        count = 0
        for row in range(self.table.rowCount()):
            item = self.table.item(row, header.column)
            if (
                item is not None
                and not self.table.isRowHidden(row)
                and item.checkState() == Qt.CheckState.Checked
            ):
                count += 1
        return count

    def adopt(self) -> None:
        """Take into the bar the buttons the page put in its row of actions
        after the bar was made (a subclass adds its own): the ones before the
        bar go first, the ones after it last."""
        row, bar = self._row, self.bar
        inner = bar.layout() if bar is not None else None
        if row is None or bar is None or not isinstance(inner, QHBoxLayout):
            return
        at = row.indexOf(bar)
        found = []
        for index in range(row.count()):
            item = row.itemAt(index)
            widget = item.widget() if item is not None else None
            if isinstance(widget, QPushButton):
                found.append((index < at, widget))
        for _before, button in found:
            row.removeWidget(button)
        for button in reversed([b for before, b in found if before]):
            inner.insertWidget(0, button)
            self.buttons.insert(0, button)
        for button in [b for before, b in found if not before]:
            inner.addWidget(button)
            self.buttons.append(button)

    def sync(self) -> None:
        """Show the bar of buttons only while rows are checked."""
        self.adopt()
        if self.bar is not None:
            self.bar.setVisible(self.checked_rows() > 0)

    def show_menu(self, position: QPoint) -> None:
        """The menu of the row at `position` (in the viewport): select it, then
        offer the buttons the extension shows, as enabled as they are."""
        row = self.table.rowAt(position.y())
        if row < 0:
            return
        self.table.selectRow(row)
        menu = QMenu(self.table)
        for button in self.buttons:
            if button.isHidden() or not button.text():
                continue
            action = menu.addAction(button.icon(), button.text())
            action.setEnabled(button.isEnabled())
            action.triggered.connect(button.click)
        if menu.isEmpty() and self._opens_on_double_click():
            # a page with no button does its one thing on a double click: say so
            open_row = menu.addAction(self._open_icon, self.tr("Open"))
            open_row.triggered.connect(
                lambda: self.table.cellDoubleClicked.emit(row, 0)
            )
        if not menu.isEmpty():
            menu.exec(self.table.viewport().mapToGlobal(position))

    def _opens_on_double_click(self) -> bool:
        signal = QMetaMethod.fromSignal(self.table.cellDoubleClicked)
        return self.table.isSignalConnected(signal)
