import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QAction, QContextMenuEvent
from PySide6.QtWidgets import QMenu, QPushButton, QTableWidgetItem, QWidget

from kubescope.extensions.components import UiComponents
from kubescope.views import row_actions as row_actions_module
from kubescope.views.row_actions import RowActions
from tests.qt import get_application

application = get_application()
KEPT: list = []
KEYS = {"row_details": "Return", "row_details_alt": "Enter", "row_delete": "Delete"}


class FakeMenu(QMenu):
    """Writes down what it offers instead of opening, and picks `pick`."""

    seen: list[list[str]] = []
    pick: int | None = None

    def exec(self, *_args, **_kwargs) -> QAction:  # type: ignore[override]
        FakeMenu.seen.append([a.text() for a in self.actions() if a.text()])
        if FakeMenu.pick is not None:
            self.actions()[FakeMenu.pick].trigger()
        return QAction(self)


def _fake_menu(monkeypatch, pick: int | None = None) -> list[list[str]]:
    FakeMenu.seen = []
    FakeMenu.pick = pick
    monkeypatch.setattr(row_actions_module, "QMenu", FakeMenu)
    return FakeMenu.seen


def _page(checkable: bool = True, keys=None):
    components = UiComponents(row_keys=lambda: dict(keys or {}))
    host = QWidget()
    table = components.data_table(["", "NAME"], (30, 100), checkable=checkable)
    if checkable:
        table.horizontalHeader().set_column(0)  # type: ignore[attr-defined]
    table.setRowCount(3)
    for row in range(3):
        box = QTableWidgetItem()
        box.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        box.setCheckState(Qt.CheckState.Unchecked)
        table.setItem(row, 0, box)
        table.setItem(row, 1, QTableWidgetItem(f"row {row}"))
    clicked: list[str] = []
    details = components.button(
        "Details",
        icon=components.icon("info", "#3220a0"),
        on_click=lambda: clicked.append("details"),
    )
    update = components.button("Update", on_click=lambda: clicked.append("update"))
    remove = components.button(
        "Uninstall",
        icon=components.icon("trash", "#3220a0"),
        on_click=lambda: clicked.append("uninstall"),
    )
    summary = components.label("3 items")
    components.page(
        host,
        actions=components.row(summary, None, details, update, remove),
        body=table,
    )
    host.resize(500, 300)
    host.show()
    KEPT.append(host)
    return host, table, details, update, summary, clicked


def _bar(actions: RowActions) -> QWidget:
    assert actions.bar is not None
    return actions.bar


def _box(table, row: int) -> QTableWidgetItem:
    item = table.item(row, 0)
    assert item is not None
    return item


def _actions(table) -> RowActions:
    found = table.findChildren(RowActions)
    assert len(found) == 1
    return found[0]


def _at(table, row: int) -> QPoint:
    return QPoint(10, table.rowViewportPosition(row) + 5)


def test_the_buttons_show_only_while_rows_are_checked() -> None:
    _host, table, details, _update, summary, _clicked = _page()
    actions = _actions(table)
    assert summary.isVisible() and not _bar(actions).isVisible()  # only the buttons go
    assert details.parentWidget() is _bar(actions)

    _box(table, 1).setCheckState(Qt.CheckState.Checked)
    actions.sync()
    assert _bar(actions).isVisible() and details.isVisibleTo(_bar(actions))

    table.setRowHidden(1, True)  # a checked row that is filtered out does not count
    actions.sync()
    assert not _bar(actions).isVisible()
    table.setRowHidden(1, False)
    _box(table, 1).setCheckState(Qt.CheckState.Unchecked)
    actions.sync()
    assert not _bar(actions).isVisible()


def test_a_table_with_no_boxes_has_no_bar_but_has_the_menu(monkeypatch) -> None:
    _host, table, *_rest = _page(checkable=False)
    actions = _actions(table)
    assert actions.checked_rows() == 0 and not _bar(actions).isVisible()
    seen = _fake_menu(monkeypatch)
    actions.show_menu(_at(table, 1))
    assert seen == [["Details", "Update", "Uninstall"]]


def test_the_menu_selects_the_row_and_runs_the_action_of_the_button(
    monkeypatch,
) -> None:
    _host, table, _details, update, _summary, clicked = _page()
    actions = _actions(table)
    update.setVisible(False)  # the extension decided it is not for this row
    seen = _fake_menu(monkeypatch, pick=0)
    actions.show_menu(_at(table, 2))
    assert table.currentRow() == 2  # the row of the menu is the one picked
    assert seen == [["Details", "Uninstall"]] and clicked == ["details"]
    actions.show_menu(QPoint(10, 10_000))  # below the rows: no menu
    assert len(seen) == 1


def test_a_page_with_its_own_menu_keeps_it_for_the_dots_and_the_right_click(
    monkeypatch,
) -> None:
    _host, table, *_rest = _page()
    actions = _actions(table)
    seen = _fake_menu(monkeypatch)
    assert not actions.has_own_menu()

    asked: list[QPoint] = []
    table.customContextMenuRequested.connect(asked.append)  # the page's own menu
    assert actions.has_own_menu()
    position = _at(table, 1)
    actions.menu_requested(position)  # the dots: the page's menu, not ours
    assert asked == [position] and seen == [] and table.currentRow() == 1

    event = QContextMenuEvent(
        QContextMenuEvent.Reason.Mouse, position, table.viewport().mapToGlobal(position)
    )
    assert actions.eventFilter(table.viewport(), event) is False  # left to the page
    assert seen == []


def test_the_menu_of_a_page_without_one_comes_from_the_buttons(monkeypatch) -> None:
    _host, table, *_rest = _page()
    actions = _actions(table)
    seen = _fake_menu(monkeypatch)
    position = _at(table, 1)
    event = QContextMenuEvent(
        QContextMenuEvent.Reason.Mouse, position, table.viewport().mapToGlobal(position)
    )
    assert actions.eventFilter(table.viewport(), event) is True  # ours
    actions.menu_requested(position)
    assert seen == [["Details", "Update", "Uninstall"]] * 2


def test_a_page_with_no_button_offers_what_its_double_click_does(monkeypatch) -> None:
    components = UiComponents()
    host = QWidget()
    table = components.data_table(["NAME"], (100,))
    table.setRowCount(2)
    table.setItem(0, 0, QTableWidgetItem("a"))
    components.page(host, body=table)  # no row of actions at all
    host.resize(300, 200)
    host.show()
    KEPT.append(host)
    actions = _actions(table)
    assert actions.bar is None and actions.buttons == []

    seen = _fake_menu(monkeypatch, pick=0)
    actions.show_menu(QPoint(10, 5))
    assert seen == []  # nothing is connected to a double click: no entry

    opened: list[tuple[int, int]] = []
    table.cellDoubleClicked.connect(lambda row, column: opened.append((row, column)))
    actions.show_menu(QPoint(10, 5))
    assert seen == [["Open"]] and opened == [(0, 0)]
    assert actions.menu_button.accessibleName() != ""
    actions.menu_button.show_on(0)
    assert actions.menu_button.isVisible()


def test_the_keys_of_a_row_work_in_the_tables_of_the_extensions() -> None:
    _host, table, _details, _update, _summary, clicked = _page(keys=KEYS)
    actions = _actions(table)
    shortcuts = {a: s.key().toString() for a, s in actions._keys.items()}
    assert shortcuts == {
        "row_details": "Return",
        "row_details_alt": "Enter",
        "row_delete": "Del",
    }
    assert all(
        s.context() == Qt.ShortcutContext.WidgetShortcut for s in actions._keys.values()
    )

    actions.key_pressed("row_details")  # no row picked
    actions.key_pressed("row_delete")
    assert clicked == []

    table.selectRow(1)
    actions.key_pressed("row_details")  # no double click: the first button
    actions.key_pressed("row_delete")  # the button with the bin
    assert clicked == ["details", "uninstall"]

    opened: list[int] = []
    table.cellDoubleClicked.connect(lambda row, _c: opened.append(row))
    actions.key_pressed("row_details_alt")  # now what the double click does
    assert opened == [1] and clicked == ["details", "uninstall"]

    actions.apply_keys({"row_details": "Ctrl+J"})  # the Settings changed it
    assert actions._keys["row_details"].key().toString() == "Ctrl+J"


def test_the_menu_of_an_extension_wears_the_icons_of_the_actions() -> None:
    icon = UiComponents().icon("info", "#3220a0")
    components = UiComponents(menu_icons=lambda: {"Logs": icon, "Forward": icon})
    table = components.data_table(["NAME"], (100,))
    FakeMenu.seen = []
    FakeMenu.pick = None
    menu = FakeMenu()
    for text in ("Logs", "Forward with SSM", "Elsewhere", "Plain"):
        menu.addAction(text)
    menu.addSeparator()
    own = menu.addAction(icon, "Own icon")
    components.show_menu(menu, table, 0, 0)
    icons = {a.text(): not a.icon().isNull() for a in menu.actions() if a.text()}
    assert icons == {
        "Logs": True,
        "Forward with SSM": True,  # the icon of Forward
        "Elsewhere": False,
        "Plain": False,
        "Own icon": True,
    }
    assert own.icon().cacheKey() == icon.cacheKey()  # one that has its own is kept


def test_a_button_added_after_the_page_goes_into_the_bar_too(monkeypatch) -> None:
    components = UiComponents()
    host = QWidget()
    table = components.data_table(["", "NAME"], (30, 100), checkable=True)
    details = components.button("Details")
    row = components.row(components.label("3 items"), None, details)
    components.page(host, actions=row, body=table)
    KEPT.append(host)
    actions = _actions(table)
    assert _bar(actions) is details.parentWidget()

    before = components.button("Resync")  # a subclass puts its button before Details
    row.insertWidget(row.count() - 1, before)
    after = components.button("Last")
    row.addWidget(after)
    actions.adopt()

    inner = _bar(actions).layout()
    assert inner is not None
    order = []
    for index in range(inner.count()):
        item = inner.itemAt(index)
        assert item is not None
        button = item.widget()
        assert isinstance(button, QPushButton)
        order.append(button.text())
    assert order == ["Resync", "Details", "Last"]
    assert [b.text() for b in actions.buttons] == order
    seen = _fake_menu(monkeypatch)
    actions.show_menu(QPoint(10, 5))
    assert seen == [] or seen == [order]  # the row 0 may not exist: no menu then


def test_delete_does_nothing_on_a_page_with_no_button_with_a_bin() -> None:
    _host, table, _details, _update, _summary, clicked = _page(keys=KEYS)
    actions = _actions(table)
    actions._icon_names.clear()  # none of its buttons has the bin of the app
    table.selectRow(1)
    actions.key_pressed("row_delete")
    assert clicked == []


def test_the_menu_of_a_page_wears_the_icons_of_the_buttons_of_its_table(
    monkeypatch,
) -> None:
    components = UiComponents()
    host = QWidget()
    table = components.data_table(["NAME"], (100,))
    details = components.button("Details", icon=components.icon("info", "#3220a0"))
    nothing = components.button("Plain")  # a button with no icon gives none
    components.page(host, actions=components.row(details, nothing), body=table)
    KEPT.append(host)
    menu = FakeMenu()
    asked = menu.addAction("Details")
    plain = menu.addAction("Plain")
    FakeMenu.pick = None
    components.show_menu(menu, table, 0, 0)
    assert not asked.icon().isNull() and plain.icon().isNull()
