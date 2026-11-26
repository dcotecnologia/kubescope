import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget

from kubescope.extensions.components import ROW_HEIGHT, UiComponents
from kubescope.extensions.testing import png_bytes as testing_png
from kubescope.views.check_header import CheckHeader
from kubescope.views.container_states import BADGE_ROLE, BadgeDelegate
from tests.qt import get_application

application = get_application()
KEPT: list[QWidget] = []  # until the end: a widget that goes first crashes Qt


def test_the_data_table_is_the_table_of_the_lists() -> None:
    table = UiComponents().data_table(["A", "B", "C"], [120, 80])
    KEPT.append(table)
    assert table.columnCount() == 3
    header = table.horizontalHeaderItem(1)
    assert header is not None and header.text() == "B"
    assert table.columnWidth(0) == 120
    assert table.verticalHeader().defaultSectionSize() == ROW_HEIGHT
    assert table.property("variant") == "data"
    assert not table.wordWrap()
    assert isinstance(table.itemDelegate(), BadgeDelegate)
    assert not isinstance(table.horizontalHeader(), CheckHeader)
    assert table.horizontalHeader().defaultAlignment() == Qt.AlignmentFlag.AlignCenter


def test_a_checkable_table_has_the_check_box_header() -> None:
    table = UiComponents().data_table(["A"], [100], checkable=True)
    KEPT.append(table)
    assert isinstance(table.horizontalHeader(), CheckHeader)


def test_the_header_sorter_sorts_the_rows_by_a_click() -> None:
    components = UiComponents()
    table = components.data_table(["A"], [100])
    KEPT.append(table)
    table.setRowCount(2)
    for row, text in enumerate(["b", "a"]):
        table.setItem(row, 0, QTableWidgetItem(text))
    components.header_sorter(table).clicked(0)
    first = table.item(0, 0)
    assert first is not None and first.text() == "a"
    asked: list[tuple[int, bool]] = []
    components.header_sorter(table, lambda c, o: asked.append((c, o))).clicked(0)
    assert asked == [(0, False)]  # ascending first, as `descending`


def test_the_badges_carry_their_colors() -> None:
    components = UiComponents(lambda status: (status, "fill"))
    table = QTableWidget(1, 1)
    KEPT.append(table)
    item = QTableWidgetItem("Active")
    components.set_badge(item, "Active")
    assert item.data(BADGE_ROLE) == ("Active", "fill")
    components.set_badge_colors(item, "#111", "#222")
    assert item.data(BADGE_ROLE) == ("#111", "#222")
    assert isinstance(components.badge_delegate(table), BadgeDelegate)


def test_the_buttons_fields_and_labels_have_the_variants_of_the_app() -> None:
    components = UiComponents()
    clicked: list[int] = []
    button = components.button("Go", "primary", on_click=lambda: clicked.append(1))
    KEPT.append(button)
    button.click()
    assert button.property("variant") == "primary" and clicked == [1]
    assert components.button("Plain").property("variant") == "secondary"
    switch = components.switch_button("Aa", "Match case")
    assert switch.isCheckable() and switch.toolTip() == "Match case"
    search = components.search_box("Search")
    assert search.objectName() == "searchInput" and search.isClearButtonEnabled()
    select = components.filter_select([("All", ""), ("Helm", "helm")])
    assert select.count() == 2 and select.itemData(1) == "helm"
    assert select.property("variant") == "filter"
    assert components.text_field("x").property("variant") == "filter"
    number = components.number_field(1, 10, 5)
    assert number.value() == 5 and number.maximum() == 10
    assert number.property("variant") == "filter"
    clock = components.time_field()
    assert clock.displayFormat() == "HH:mm" and clock.property("variant") == "filter"
    area = components.text_area("one per line", 110)
    assert area.placeholderText() == "one per line" and area.maximumHeight() == 110
    assert not components.text_area().isReadOnly()
    assert components.muted_label("note").property("variant") == "muted"
    iconed = components.button("I", icon=QIcon())
    assert iconed.text() == "I"


def test_the_labels_boxes_and_items_are_the_ones_of_the_app() -> None:
    components = UiComponents(themed=lambda color: "#123456")
    assert components.label("a", "summary").objectName() == "summaryLabel"
    assert components.label("a", "filter").objectName() == "filterLabel"
    muted = components.label("a", "muted", wrap=True)
    assert muted.property("variant") == "muted" and muted.wordWrap()
    assert not components.label("a").wordWrap()
    box = components.checkbox("Keep", True, lambda checked: None)
    assert box.isChecked()
    toggled: list[bool] = []
    components.checkbox("x", on_toggle=toggled.append).setChecked(True)
    assert toggled == [True]
    button = components.icon_button(QIcon(), "Tip")
    assert button.toolTip() == "Tip" and button.property("variant") == "link"
    command = components.command_box("ls", 64)
    assert command.isReadOnly() and command.toPlainText() == "ls"
    item = components.table_item("cell", "why")
    assert item.toolTip() == "why"
    assert item.foreground().color().name() == "#123456"
    assert components.table_item("plain").toolTip() == ""
    assert components.menu() is not None


def test_the_layouts_and_the_page_hold_what_they_are_given() -> None:
    from PySide6.QtWidgets import QLabel, QPushButton

    components = UiComponents()
    host = QWidget()
    KEPT.append(host)
    first, second = QLabel("a"), QLabel("b")
    row = components.row(first, None, (second, 2), components.column(QLabel("c")))
    assert row.count() == 4
    column = components.column(QLabel("x"), None)
    assert column.count() == 2
    assert components.form([("Name", QLabel("v"))]).rowCount() == 1
    card = components.card(QLabel("in"), name="plugin", min_height=190)
    KEPT.append(card)
    assert card.property("card") is True
    assert card.objectName() == "plugin" and card.minimumHeight() == 190
    assert components.card(QLabel("x")).objectName() == ""
    logo = components.image_label(32)
    assert logo.width() == 32 and logo.alignment() == Qt.AlignmentFlag.AlignCenter
    area, grid = components.grid_scroll(8)
    KEPT.append(area)
    assert grid.spacing() == 8 and area.widget() is not None
    assert "700" in components.label("t", "title").styleSheet()
    assert "700" in components.label("m", "mark").styleSheet()
    body = QLabel("body")
    layout = components.page(
        host,
        filters=components.row(),
        actions=components.row(),
        notice=QLabel("n"),
        body=body,
        footer=components.row(),
    )
    assert layout.count() == 5
    bare_host = QWidget()
    KEPT.append(bare_host)
    assert components.page(bare_host).count() == 0
    dialog = components.dialog(
        None, "Title", components.column(QLabel("b")), [QPushButton("Close")], 400
    )
    KEPT.append(dialog)
    assert dialog.windowTitle() == "Title" and dialog.minimumWidth() == 400
    plain = components.dialog(None, "T", QLabel("w"), [])
    KEPT.append(plain)
    assert plain.minimumWidth() == 0
    area = components.scroll(QLabel("long"))
    KEPT.append(area)
    assert area.widgetResizable()


def test_confirm_says_whether_the_person_accepted(monkeypatch) -> None:
    from PySide6.QtWidgets import QMessageBox

    styled: list[object] = []
    components = UiComponents(style_box=styled.append)
    answer = {"accept": True}

    def fake_exec(box: QMessageBox) -> int:
        buttons = box.buttons()
        box._chosen = buttons[0] if answer["accept"] else buttons[1]  # type: ignore[attr-defined]
        return 0

    monkeypatch.setattr(QMessageBox, "exec", fake_exec)
    monkeypatch.setattr(
        QMessageBox,
        "clickedButton",
        lambda box: box._chosen,  # type: ignore[attr-defined]
    )
    assert components.confirm(None, "Sure?", "Really", "Do it") is True
    answer["accept"] = False
    assert components.confirm(None, "Sure?", "Really") is False
    answer["accept"] = True
    assert components.confirm(None, "Sure?", "Really", "Go", "more", True) is True
    assert len(styled) == 3


def test_the_error_banner_starts_hidden_and_shows_the_error_with_its_details() -> None:
    banner = UiComponents().error_banner("More", "Less", "Close it")
    KEPT.append(banner.frame)
    assert banner.frame.objectName() == "errorBanner" and banner.frame.isHidden()
    banner.show_error("Access denied", "Access denied\nfor the role")
    assert not banner.frame.isHidden() and banner.label.text() == "Access denied"
    assert banner.details_label.text() == "Access denied\nfor the role"
    assert banner.details_label.isHidden()
    banner.toggle_details()
    assert not banner.details_label.isHidden()
    banner.dismiss()
    assert banner.frame.isHidden()


def test_open_file_returns_the_path_chosen(monkeypatch) -> None:
    from PySide6.QtWidgets import QFileDialog

    asked: list[tuple] = []
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileName",
        lambda *args: asked.append(args) or ("/bin/ls", ""),
    )
    assert UiComponents().open_file(None, "Where?", "/usr") == "/bin/ls"
    assert asked == [(None, "Where?", "/usr")]


def test_the_widget_of_a_page_calls_the_hooks_it_was_given() -> None:
    calls: list[str] = []
    widget = UiComponents().widget(
        shown=lambda: calls.append("shown"),
        hidden=lambda: calls.append("hidden"),
        save=lambda: calls.append("save") or True,
    )
    KEPT.append(widget)
    widget.shown()  # type: ignore[attr-defined]
    assert widget.save() is True  # type: ignore[attr-defined]
    widget.show()
    widget.hide()
    assert calls == ["shown", "save", "hidden"]
    assert not hasattr(widget, "load")  # a hook not given is not there
    plain = UiComponents().widget()
    KEPT.append(plain)
    plain.show()
    plain.hide()


def test_copy_text_puts_the_text_on_the_clipboard() -> None:
    from PySide6.QtGui import QGuiApplication

    UiComponents().copy_text("helm install")
    assert QGuiApplication.clipboard().text() == "helm install"


def test_a_timer_and_a_delayed_call_run_what_they_are_given() -> None:
    from PySide6.QtCore import QCoreApplication

    components = UiComponents()
    host = QWidget()
    KEPT.append(host)
    ticks: list[int] = []
    once = components.timer(5, lambda: ticks.append(0), host, single_shot=True)
    assert once.isSingleShot()
    timer = components.timer(5, lambda: ticks.append(1), host)
    assert not timer.is_active()
    timer.start()
    assert timer.is_active()
    timer.stop()
    delayed: list[int] = []
    components.after(0, host, lambda: delayed.append(1))
    QCoreApplication.processEvents()
    import time

    time.sleep(0.01)
    QCoreApplication.processEvents()
    assert delayed == [1]


def test_the_icons_are_asked_for_by_name() -> None:
    components = UiComponents()
    for name in ("update", "info", "trash", "bell"):
        assert not components.icon(name, "#123456").isNull()


def test_a_right_click_hands_over_the_place_and_the_menu_opens_there() -> None:
    from PySide6.QtCore import QPoint

    components = UiComponents()
    table = components.data_table(["A"], [100])
    KEPT.append(table)
    seen: list[tuple[int, int]] = []
    components.on_context_menu(table, lambda x, y: seen.append((x, y)))
    table.customContextMenuRequested.emit(QPoint(3, 4))
    assert seen == [(3, 4)]
    opened: list[QPoint] = []

    class Menu:
        def exec(self, where: QPoint) -> None:
            opened.append(where)

    components.show_menu(Menu(), table, 3, 4)  # type: ignore[arg-type]
    assert len(opened) == 1


def test_the_cell_check_boxes_are_told_by_booleans() -> None:
    components = UiComponents()
    plain = components.table_item("a")
    assert components.item_checked(plain) is None
    boxed = components.table_item("b", checked=True)
    assert components.item_checked(boxed) is True
    components.set_item_checked(boxed, False)
    assert components.item_checked(boxed) is False
    components.set_item_checked(boxed, None)
    assert components.item_checked(boxed) is None


def test_the_check_header_says_what_its_box_shows() -> None:
    from kubescope.views.check_header import CheckHeader

    table = UiComponents().data_table(["A"], [100], checkable=True)
    KEPT.append(table)
    header = table.horizontalHeader()
    assert isinstance(header, CheckHeader)
    for state, shown in (
        (True, Qt.CheckState.Checked),
        (False, Qt.CheckState.Unchecked),
        (None, Qt.CheckState.PartiallyChecked),
    ):
        header.set_checked(state)
        assert header.check_state == shown
        assert header.checked is state


def test_images_labels_grids_and_resizes_are_made_for_the_extension(
    monkeypatch,
) -> None:
    from PySide6.QtWidgets import QLabel

    components = UiComponents()
    made = components.image(testing_png(40, 20), 16)
    assert made is not None and made.width() == 16
    assert components.image(b"not an image", 16) is None
    logo = components.image_label(16)
    components.set_image(logo, made)
    assert not logo.pixmap().isNull()

    assert (
        components.label("a", align="right").alignment() == Qt.AlignmentFlag.AlignRight
    )
    area, grid = components.grid_scroll()
    KEPT.append(area)
    components.grid_cell(grid, QLabel("x"), 0, 0)
    components.grid_cell(grid, QLabel("y"), 1, 0, 2, center=True)
    assert grid.count() == 2

    host = QWidget()
    KEPT.append(host)
    resized: list[int] = []
    components.on_resize(host, lambda: resized.append(1))
    host.resize(300, 200)
    host.show()
    host.resize(310, 210)
    assert resized
    assert components.is_alive(host)
    assert components.bottom_of(host, host) == host.height()
    opened: list[str] = []
    monkeypatch.setattr(
        "kubescope.extensions.components.QDesktopServices.openUrl",
        lambda url: opened.append(url.toString()),
    )
    components.open_url("https://example.org")
    assert opened == ["https://example.org"]


def test_the_texts_of_an_extension_are_translated_by_the_app() -> None:
    from kubescope.sdk import translate

    assert translate("Ctx", "Hello") == "Hello"  # no language loaded: as it is


def test_the_time_fields_the_spacers_and_the_matrix_of_boxes() -> None:
    components = UiComponents()
    clock = components.time_field()
    components.set_time(clock, "08:30")
    assert components.time_text(clock) == "08:30"
    assert components.spacer(12).height() == 12
    frame, boxes = components.check_matrix(
        ["Show", "Tell"], [("error", "Errors"), ("info", "Updates")]
    )
    KEPT.append(frame)
    assert len(boxes) == 2 and set(boxes[0]) == {"error", "info"}
    boxes[1]["info"].setChecked(True)
    assert boxes[1]["info"].isChecked() and not boxes[0]["info"].isChecked()


def test_a_question_and_a_guide_are_answered_by_the_buttons(monkeypatch) -> None:
    from PySide6.QtWidgets import QMessageBox

    styled: list[object] = []
    components = UiComponents(style_box=styled.append)
    monkeypatch.setattr(QMessageBox, "exec", lambda box: QMessageBox.StandardButton.Yes)
    assert components.ask(None, "Sure?", "Really?") is True
    monkeypatch.setattr(QMessageBox, "exec", lambda box: QMessageBox.StandardButton.No)
    assert components.ask(None, "Sure?", "Really?") is False

    ran: list[str] = []

    def press_first(box: QMessageBox) -> int:
        box.buttons()[0].click()
        return 0

    monkeypatch.setattr(QMessageBox, "exec", press_first)
    components.guide(
        None,
        "Setup",
        "Install it",
        "1. Install\n2. Sign in",
        [("Open Settings", lambda: ran.append("settings")), ("Guide", lambda: None)],
        "Close",
    )
    assert ran == ["settings"] and len(styled) == 3


def test_the_window_is_let_shrink_and_gets_back_its_minimum() -> None:
    from PySide6.QtCore import QSize

    components = UiComponents()
    window = QWidget()
    KEPT.append(window)
    window.setMinimumSize(QSize(400, 300))
    components.let_window_shrink(window, True)
    components.let_window_shrink(window, True)  # once only
    assert window.minimumSize() == QSize(0, 0)
    components.let_window_shrink(window, False)
    assert window.minimumSize() == QSize(400, 300)
    components.let_window_shrink(window, False)  # nothing to give back


def test_the_icons_with_options_and_the_chat_dock_come_from_the_components() -> None:
    components = UiComponents()
    assert not components.icon("focus", "#ffffff", active=True).isNull()
    assert not components.icon("sparkle", "#ffffff", size=14, inside="#000000").isNull()
    host = QWidget()
    dock = components.chat_dock(host, "Gabi", {})
    assert dock.host is host
    host.close()
