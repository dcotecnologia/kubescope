"""The pre-formatted elements of the app that an extension is lent
(`kubescope.sdk.Components`): its tables, the sorting of their headers and its
badges, so a page looks like the others without a copy of their code."""

from collections.abc import Callable, Sequence
from typing import Any

from kubescope.sdk import set_translator
from PySide6.QtCore import (
    QCoreApplication,
    QEvent,
    QObject,
    QPoint,
    QSize,
    Qt,
    QTime,
    QTimer,
    QUrl,
)
from PySide6.QtGui import (
    QColor,
    QDesktopServices,
    QFontDatabase,
    QGuiApplication,
    QIcon,
    QPixmap,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from kubescope.extensions import background as background_module
from kubescope.extensions.chat_dock import AssistantDock
from kubescope.extensions.chat_view import ChatView
from kubescope.extensions.icons import FOCUS_ICON, ICONS, SPARKLE_ICON
from kubescope.extensions.palette import Palette, SearchEntry
from kubescope.extensions.side_panel import CounterButton, NoticeCard, SidePanel
from kubescope.views.check_header import CheckHeader
from kubescope.views.container_states import BADGE_ROLE, BadgeDelegate
from kubescope.views.error_banner import ErrorBanner
from kubescope.views.row_actions import RowActions
from kubescope.views.search_bar import embed_switches
from kubescope.views.table_sort import HeaderSorter

ROW_HEIGHT = 46  # as the rows of the Pods
FIELD_HEIGHT = 28  # as the search box and the selects of the lists
TEXT_COLOR = "#242a33"  # of the text of a cell
MARGINS = (32, 24, 32, 22)  # around the content of a page


set_translator(lambda context, text: QCoreApplication.translate(context, text))


_ALIGN = {
    "left": Qt.AlignmentFlag.AlignLeft,
    "right": Qt.AlignmentFlag.AlignRight,
    "center": Qt.AlignmentFlag.AlignCenter,
    "top-left": Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
}


class Timer(QTimer):
    """A timer an extension starts and stops."""

    def is_active(self) -> bool:
        return self.isActive()


class _Resizes(QObject):
    """Tells a callback when a widget is resized."""

    def __init__(self, widget: QWidget, callback: Callable[[], None]) -> None:
        super().__init__(widget)
        self._callback = callback
        widget.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Resize:
            self._callback()
        return False


class HookedWidget(QWidget):
    """The widget of a page or a section of the Settings of an extension: the
    app calls the hooks the extension gave (`shown` when the page is opened,
    `load` and `save` for a section of the Settings), and `hidden` is called
    when it is hidden."""

    def __init__(
        self,
        hidden: Callable[[], None] | None = None,
        **hooks: Callable[..., Any] | None,
    ) -> None:
        super().__init__()
        self._hidden = hidden
        for name, hook in hooks.items():
            if hook is not None:
                setattr(self, name, hook)

    def hideEvent(self, event: Any) -> None:
        if self._hidden is not None:
            self._hidden()
        super().hideEvent(event)


class UiComponents:
    """What an extension builds its pages with."""

    def __init__(
        self,
        badge_colors: Callable[[str], tuple[str, str]] = lambda _s: ("", ""),
        themed: Callable[[str], str] = lambda color: color,
        style_box: Callable[[QMessageBox], None] = lambda _box: None,
        themed_text: Callable[[str, bool], str] | None = None,
        palette_actions: Callable[[], list[SearchEntry]] = lambda: [],
        menu_icons: Callable[[], dict[str, QIcon]] = lambda: {},
        row_keys: Callable[[], dict[str, str]] = lambda: {},
    ) -> None:
        self._row_keys = row_keys
        self._icon_names: dict[int, str] = {}  # the icons of the app, by name
        self._palette_actions = palette_actions
        self._menu_icons = menu_icons
        self._badge_colors = badge_colors
        self._themed = themed
        self._style_box = style_box
        self._themed_text = themed_text
        self._minimums: dict[int, QSize] = {}

    def _themed_pair(self, color: str, text: bool = False) -> str:
        """A color of the design as the theme in use shows it; `text` is for
        the color of a text on the background of the theme."""
        if self._themed_text is not None:
            return self._themed_text(color, text)
        return self._themed(color)

    def data_table(
        self, headers: Sequence[str], widths: Sequence[int], checkable: bool = False
    ) -> QTableWidget:
        table = QTableWidget(0, len(headers))
        table.setProperty("variant", "data")
        if checkable:
            table.setHorizontalHeader(CheckHeader(table))
        table.setHorizontalHeaderLabels(list(headers))
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(ROW_HEIGHT)
        table.setShowGrid(False)  # the rows draw their own divider
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionsClickable(True)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setTextElideMode(Qt.TextElideMode.ElideRight)
        table.setWordWrap(False)
        table.setTextElideMode(Qt.TextElideMode.ElideRight)
        for column, width in enumerate(widths):
            table.setColumnWidth(column, width)
        table.setItemDelegate(BadgeDelegate(table))
        return table

    def header_sorter(
        self,
        table: QTableWidget,
        apply: Callable[[int, bool], None] | None = None,
    ) -> HeaderSorter:
        """`apply(column, descending)` is told what a click on a header
        asked."""
        return HeaderSorter(
            table,
            None
            if apply is None
            else lambda column, order: apply(
                column, order == Qt.SortOrder.DescendingOrder
            ),
        )

    def badge_delegate(self, parent: Any) -> BadgeDelegate:
        return BadgeDelegate(parent)

    def set_badge(self, item: Any, status: str) -> None:
        item.setData(BADGE_ROLE, self._badge_colors(status))

    def set_badge_colors(self, item: Any, text: str, fill: str) -> None:
        item.setData(BADGE_ROLE, (text, fill))

    def button(
        self,
        text: str,
        variant: str = "secondary",
        icon: QIcon | None = None,
        on_click: Callable[[], None] | None = None,
    ) -> QPushButton:
        button = QPushButton(text)
        button.setProperty("variant", variant)
        if variant == "link":
            button.setCursor(Qt.CursorShape.PointingHandCursor)
        if icon is not None:
            button.setIcon(icon)
        if on_click is not None:
            button.clicked.connect(lambda _checked=False: on_click())
        return button

    def switch_button(self, text: str, tip: str) -> QPushButton:
        button = self.button(text)
        button.setCheckable(True)
        button.setToolTip(tip)
        button.setFixedSize(FIELD_HEIGHT, FIELD_HEIGHT)
        button.setProperty("searchSwitch", True)
        return button

    def search_box(self, placeholder: str = "") -> QLineEdit:
        box = QLineEdit()
        box.setObjectName("searchInput")
        box.setMinimumSize(240, FIELD_HEIGHT)
        box.setMaximumWidth(300)
        box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        box.setPlaceholderText(placeholder)
        box.setClearButtonEnabled(True)
        return box

    def filter_select(self, items: Sequence[tuple[str, Any]] = ()) -> QComboBox:
        combo = QComboBox()
        combo.setProperty("variant", "filter")
        combo.setMinimumSize(170, FIELD_HEIGHT)
        for text, data in items:
            combo.addItem(text, data)
        return combo

    def text_field(self, placeholder: str = "") -> QLineEdit:
        field = QLineEdit()
        field.setProperty("variant", "filter")
        field.setMinimumHeight(FIELD_HEIGHT)
        field.setPlaceholderText(placeholder)
        return field

    def number_field(self, minimum: int, maximum: int, value: int = 0) -> QSpinBox:
        field = QSpinBox()
        field.setProperty("variant", "filter")
        field.setRange(minimum, maximum)
        field.setValue(value)
        return field

    def time_field(self) -> QTimeEdit:
        field = QTimeEdit()
        field.setProperty("variant", "filter")
        field.setDisplayFormat("HH:mm")
        return field

    def set_time(self, field: QTimeEdit, text: str) -> None:
        """Show a time given as `HH:mm` in a time field."""
        field.setTime(QTime.fromString(text, "HH:mm"))

    def time_text(self, field: QTimeEdit) -> str:
        """The time of a time field, as `HH:mm`."""
        return str(field.time().toString("HH:mm"))

    def spacer(self, height: int) -> QWidget:
        """Empty room `height` pixels high between the parts of a column."""
        space = QWidget()
        space.setFixedHeight(height)
        return space

    def check_matrix(
        self, headers: Sequence[str], rows: Sequence[tuple[str, str]]
    ) -> tuple[QFrame, list[dict[str, QCheckBox]]]:
        """A table of check boxes: a column for each of `headers` and a line
        for each `(key, text)` of `rows`.

        The frame, and for each header a dict of the boxes by key.
        """
        table = QFrame()
        table.setObjectName("checkMatrix")
        table.setStyleSheet(
            "QFrame#checkMatrix { border: 1px solid rgba(128, 128, 128, 90);"
            " border-radius: 8px; }"
            "QFrame#checkMatrix QLabel, QFrame#checkMatrix QCheckBox"
            " { border: 0; }"
            "QFrame#checkMatrix QFrame#checkMatrixRule"
            " { background: rgba(128, 128, 128, 60); border: 0; }"
        )
        grid = QGridLayout(table)
        grid.setContentsMargins(14, 8, 14, 8)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        grid.setColumnStretch(0, 1)
        center = Qt.AlignmentFlag.AlignCenter
        for column, text in enumerate(headers, start=1):
            head = self.label(text.upper(), "muted", wrap=True, align="center")
            head.setMinimumWidth(120)
            head.setContentsMargins(0, 4, 0, 8)
            grid.addWidget(head, 0, column)
        boxes: list[dict[str, QCheckBox]] = [{} for _ in headers]
        for number, (key, text) in enumerate(rows, start=1):
            rule = QFrame()
            rule.setObjectName("checkMatrixRule")
            rule.setFixedHeight(1)
            grid.addWidget(rule, number * 2 - 1, 0, 1, len(headers) + 1)
            name = self.label(text)
            name.setMinimumHeight(36)
            grid.addWidget(name, number * 2, 0)
            for column, found in enumerate(boxes, start=1):
                found[key] = self.checkbox("")
                grid.addWidget(found[key], number * 2, column, center)
        return table, boxes

    def text_area(self, placeholder: str = "", max_height: int = 0) -> QPlainTextEdit:
        area = QPlainTextEdit()
        area.setPlaceholderText(placeholder)
        if max_height:
            area.setMaximumHeight(max_height)
        return area

    def muted_label(self, text: str = "") -> QLabel:
        label = QLabel(text)
        label.setProperty("variant", "muted")
        return label

    # what a page is made of

    def label(
        self, text: str = "", variant: str = "", wrap: bool = False, align: str = ""
    ) -> QLabel:
        label = QLabel(text)
        if variant == "summary":
            label.setObjectName("summaryLabel")
        elif variant == "filter":
            label.setObjectName("filterLabel")
        elif variant == "title":
            label.setStyleSheet("font-size: 16px; font-weight: 700;")
        elif variant == "mark":
            label.setStyleSheet("font-weight: 700;")
        elif variant:
            label.setProperty("variant", variant)
        label.setWordWrap(wrap)
        if align:
            label.setAlignment(_ALIGN[align])
        return label

    def checkbox(
        self,
        text: str,
        checked: bool = False,
        on_toggle: Callable[[bool], None] | None = None,
    ) -> QCheckBox:
        box = QCheckBox(text)
        box.setChecked(checked)
        if on_toggle is not None:
            box.toggled.connect(on_toggle)
        return box

    def icon_button(
        self,
        icon: QIcon,
        tip: str,
        on_click: Callable[[], None] | None = None,
        variant: str = "link",
    ) -> QPushButton:
        button = self.button("", variant, icon, on_click)
        button.setToolTip(tip)
        return button

    def command_box(self, text: str = "", height: int = 96) -> QPlainTextEdit:
        box = QPlainTextEdit()
        box.setReadOnly(True)
        box.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
        box.setFixedHeight(height)
        box.setPlainText(text)
        return box

    def table_item(
        self, text: str, tip: str = "", checked: bool | None = None
    ) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setForeground(QColor(self._themed(TEXT_COLOR)))
        if tip:
            item.setToolTip(tip)
        if checked is not None:
            self.set_item_checked(item, checked)
        return item

    def set_item_checked(self, item: QTableWidgetItem, checked: bool | None) -> None:
        """Give a cell a check box, checked or not; `None` takes it away."""
        if checked is None:
            item.setData(Qt.ItemDataRole.CheckStateRole, None)
            return
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        )

    def item_checked(self, item: QTableWidgetItem) -> bool | None:
        """Whether the check box of a cell is checked; `None` when it has
        none."""
        if item.data(Qt.ItemDataRole.CheckStateRole) is None:
            return None
        return item.checkState() == Qt.CheckState.Checked

    def menu(self, parent: QWidget | None = None) -> QMenu:
        return QMenu(parent)

    def scroll(self, content: QWidget) -> QScrollArea:
        area = QScrollArea()
        area.setFrameShape(QFrame.Shape.NoFrame)
        area.setWidgetResizable(True)
        area.setWidget(content)
        return area

    def card(self, *items: Any, name: str = "", min_height: int = 0) -> QFrame:
        card = QFrame()
        if name:
            card.setObjectName(name)
        card.setProperty("card", True)
        if min_height:
            card.setMinimumHeight(min_height)
        self._fill(QVBoxLayout(card), items)
        return card

    def image_label(self, size: int) -> QLabel:
        label = QLabel()
        label.setFixedSize(size, size)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def grid_scroll(self, spacing: int = 12) -> tuple[QScrollArea, QGridLayout]:
        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(spacing)
        return self.scroll(content), grid

    # layouts: a widget, a layout, `None` for a stretch, or `(widget, stretch)`

    @staticmethod
    def _fill(layout: QLayout, items: Sequence[Any]) -> QLayout:
        box = layout if isinstance(layout, (QHBoxLayout, QVBoxLayout)) else None
        for item in items:
            if item is None:
                assert box is not None
                box.addStretch(1)
            elif isinstance(item, tuple):
                assert box is not None
                box.addWidget(item[0], item[1])
            elif isinstance(item, QLayout):
                assert box is not None
                box.addLayout(item)
            else:
                layout.addWidget(item)
        return layout

    @staticmethod
    def _embed_search_switches(items: Sequence[Any]) -> list[Any]:
        """A search box followed by switches (the Aa and .* of the lists) is one
        control: the switches go inside the box, as in the lists of the app, and
        the rest of the items stay as they were."""
        kept: list[Any] = []
        waiting: list[QPushButton] = []

        def flush() -> None:
            if waiting:  # the first switch is the left-most, so the last goes first
                embed_switches(kept[-1], list(reversed(waiting)))
                waiting.clear()

        for item in items:
            is_switch = isinstance(item, QPushButton) and item.property("searchSwitch")
            after_search = (
                bool(kept)
                and isinstance(kept[-1], QLineEdit)
                and kept[-1].objectName() == "searchInput"
            )
            if is_switch and after_search:
                waiting.append(item)
                continue
            flush()
            kept.append(item)
        flush()
        return kept

    def row(self, *items: Any, spacing: int = 12) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(spacing)
        self._fill(layout, self._embed_search_switches(items))
        return layout

    def column(self, *items: Any, spacing: int = 10) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(spacing)
        self._fill(layout, items)
        return layout

    def form(self, rows: Sequence[tuple[str, QWidget]]) -> QFormLayout:
        layout = QFormLayout()
        for label, field in rows:
            layout.addRow(label, field)
        return layout

    def _row_actions(self, actions: QLayout | None, table: QTableWidget) -> None:
        """Give a table the actions of the lists of the app: its buttons go
        into one bar that shows only while rows are checked, and the ⋯ of a row
        and the right click offer the same actions (a table with no button
        offers what its double click does).

        The extension keeps its buttons and decides, as before, which of
        them it shows.
        """
        open_icon = self.icon("popout", self._themed_pair("#3220a0", True))
        buttons: list[QPushButton] = []
        bar: QWidget | None = None
        if isinstance(actions, QHBoxLayout):
            first = -1
            for index in range(actions.count()):
                item = actions.itemAt(index)
                widget = item.widget() if item is not None else None
                if isinstance(widget, QPushButton):
                    first = index if first < 0 else first
                    buttons.append(widget)
            if buttons:
                for button in buttons:
                    actions.removeWidget(button)
                bar = QWidget()
                inner = QHBoxLayout(bar)
                inner.setContentsMargins(0, 0, 0, 0)
                inner.setSpacing(actions.spacing() if actions.spacing() >= 0 else 12)
                for button in buttons:
                    inner.addWidget(button)
                actions.insertWidget(first, bar)
        RowActions(table, buttons, bar, open_icon, self._row_keys, self._icon_names)

    def page(
        self,
        parent: QWidget,
        *,
        filters: QLayout | None = None,
        actions: QLayout | None = None,
        notice: QWidget | None = None,
        body: QWidget | None = None,
        footer: QLayout | None = None,
    ) -> QVBoxLayout:
        """Lay `parent` out as the pages of the app: the filters, the actions,
        a notice, the body (it takes what is left) and the footer."""
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(*MARGINS)
        layout.setSpacing(14)
        if isinstance(body, QTableWidget):
            self._row_actions(actions, body)
        for part in (filters, actions):
            if part is not None:
                layout.addLayout(part)
        if notice is not None:
            layout.addWidget(notice)
        if body is not None:
            layout.addWidget(body, 1)
        if footer is not None:
            layout.addLayout(footer)
        return layout

    def dialog(
        self,
        parent: QWidget | None,
        title: str,
        body: Any,
        buttons: Sequence[QPushButton],
        width: int = 0,
    ) -> QDialog:
        """A dialog with `body` (a layout or a widget) above a row of `buttons`
        at the right."""
        dialog = QDialog(parent)
        dialog.setWindowTitle(title)
        if width:
            dialog.setMinimumWidth(width)
        layout = QVBoxLayout(dialog)
        if isinstance(body, QLayout):
            layout.addLayout(body)
        else:
            layout.addWidget(body)
        footer = QHBoxLayout()
        footer.addStretch(1)
        for button in buttons:
            footer.addWidget(button)
        layout.addLayout(footer)
        return dialog

    def confirm(
        self,
        parent: QWidget | None,
        title: str,
        text: str,
        ok: str = "OK",
        detail: str = "",
        warning: bool = False,
    ) -> bool:
        icon = QMessageBox.Icon.Warning if warning else QMessageBox.Icon.Question
        box = QMessageBox(icon, title, text, parent=parent)
        if detail:
            box.setInformativeText(detail)
        accept = box.addButton(ok, QMessageBox.ButtonRole.AcceptRole)
        cancel = box.addButton(QMessageBox.StandardButton.Cancel)
        box.setDefaultButton(cancel)  # an Enter does not go through with it
        self._style_box(box)
        box.exec()
        return box.clickedButton() is accept

    def widget(
        self,
        shown: Callable[[], None] | None = None,
        hidden: Callable[[], None] | None = None,
        load: Callable[[], None] | None = None,
        save: Callable[[], bool] | None = None,
    ) -> HookedWidget:
        return HookedWidget(hidden, shown=shown, load=load, save=save)

    def side_panel(
        self,
        host: QWidget,
        title: str,
        actions: Sequence[QPushButton],
        top: Callable[[], int],
        close_text: str = "✕",
        empty_text: str = "",
    ) -> SidePanel:
        close = self.button(close_text, "link")
        return SidePanel(
            host,
            title,
            actions,
            close,
            lambda color, text=False: self._themed_pair(color, text),
            top,
            empty_text,
        )

    def notice_card(
        self,
        title: str,
        kind: str,
        about: str,
        message: str,
        when: str,
        level: str,
        unread: bool,
        tip: str,
        on_click: Callable[[], None],
        actions: Sequence[tuple[str, Callable[[], None]]] = (),
    ) -> NoticeCard:
        return NoticeCard(
            title,
            kind,
            about,
            message,
            when,
            level,
            unread,
            tip,
            on_click,
            actions,
            lambda text: self.button(text, "link"),
        )

    def counter_button(
        self, icon: QIcon, tip: str, name: str = "counterButton"
    ) -> CounterButton:
        return CounterButton(
            icon, tip, lambda color, text=False: self._themed_pair(color, text), name
        )

    def timer(
        self,
        interval_ms: int,
        callback: Callable[[], None],
        owner: Any = None,
        single_shot: bool = False,
    ) -> Timer:
        """A timer that calls `callback` every `interval_ms` once started (or
        once, with `single_shot`); it goes away with `owner`."""
        timer = Timer(owner)
        timer.setInterval(interval_ms)
        timer.setSingleShot(single_shot)
        timer.timeout.connect(callback)
        return timer

    def after(self, delay_ms: int, owner: Any, callback: Callable[[], None]) -> None:
        """Call `callback` once, in `delay_ms`, unless `owner` is gone."""
        QTimer.singleShot(delay_ms, owner, callback)

    def icon(self, name: str, color: str, **options: Any) -> QIcon:
        """An icon of the app by name in `color`; `options` are those of the
        icon (the `size` and `inside` color of `sparkle`, `active` of
        `focus`)."""
        if name == "focus":
            return FOCUS_ICON(color, **options)
        if name == "sparkle":
            return SPARKLE_ICON(color, **options)
        icon = ICONS[name](color)
        self._icon_names[icon.cacheKey()] = name
        return icon

    def background(
        self,
        function: Callable[[], Any],
        on_piece: Callable[[Any], None] | None = None,
        on_done: Callable[[Any], None] | None = None,
        on_error: Callable[[str], None] | None = None,
        on_finished: Callable[[], None] | None = None,
        stream: bool = False,
    ) -> background_module.Background:
        return background_module.start(
            function, on_piece, on_done, on_error, on_finished, stream
        )

    def chat_view(self, texts: dict[str, str]) -> ChatView:
        """The conversation with an assistant, laid out as a chat, with its
        composer; `texts` are its words in the language of the app."""
        return ChatView(texts)

    def chat_dock(
        self, host: QWidget, name: str, texts: dict[str, str]
    ) -> AssistantDock:
        """The round button in the corner of `host` and the chat panel it
        opens; `texts` are the words of the panel in the language of the app,
        by their English text."""
        return AssistantDock(host, name, texts)

    def open_url(self, url: str) -> None:
        QDesktopServices.openUrl(QUrl(url))

    def on_context_menu(
        self, table: QWidget, handler: Callable[[int, int], None]
    ) -> None:
        """Call `handler(x, y)` on a right click in a table, with the place in
        its rows; open the menu with `show_menu`."""
        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table.customContextMenuRequested.connect(
            lambda point: handler(point.x(), point.y())
        )

    def show_menu(self, menu: QMenu, table: Any, x: int, y: int) -> None:
        """Open `menu` at the place `(x, y)` of the rows of `table`, with the
        icon of the action of the lists of the app (or of a button of the page)
        beside each entry that has none."""
        self._add_menu_icons(menu, table)
        menu.exec(table.viewport().mapToGlobal(QPoint(x, y)))

    def _add_menu_icons(self, menu: QMenu, table: Any) -> None:
        if not isinstance(menu, QMenu):
            return
        known = dict(self._menu_icons())
        for row_actions in table.findChildren(RowActions):
            for button in row_actions.buttons:
                if button.text() and not button.icon().isNull():
                    known[button.text()] = button.icon()
        for action in menu.actions():
            if not action.icon().isNull() or action.isSeparator():
                continue
            text = action.text().replace("&", "")
            named = [word for word in known if text.startswith(word)]
            if named:  # "Forward with SSM" takes the icon of "Forward"
                action.setIcon(known[max(named, key=len)])

    def image(self, data: bytes, size: int) -> QPixmap | None:
        """An image of those bytes, scaled to fit `size` pixels; `None` when it
        is not one that can be drawn."""
        pixmap = QPixmap()
        if not pixmap.loadFromData(data):
            return None
        return pixmap.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def set_image(self, label: QLabel, image: Any) -> None:
        label.setPixmap(image)

    def on_resize(self, widget: QWidget, callback: Callable[[], None]) -> None:
        """Call `callback` when `widget` is resized."""
        _Resizes(widget, callback)

    def grid_cell(
        self,
        grid: Any,
        widget: QWidget,
        row: int,
        column: int,
        column_span: int = 1,
        center: bool = False,
    ) -> None:
        """Put `widget` in a cell of a grid (from `grid_scroll`), over
        `column_span` columns, centered in them when asked."""
        if center:
            grid.addWidget(
                widget, row, column, 1, column_span, Qt.AlignmentFlag.AlignCenter
            )
        else:
            grid.addWidget(widget, row, column, 1, column_span)

    def bottom_of(self, widget: QWidget, host: QWidget) -> int:
        """Where the bottom edge of `widget` is, as a y in the coordinates of
        `host`."""
        return widget.mapTo(host, QPoint(0, widget.height())).y()

    def is_alive(self, widget: Any) -> bool:
        """Whether a widget still exists: the app deletes a page it built when
        it builds its menu again."""
        from shiboken6 import isValid

        return bool(isValid(widget))

    def ask(self, parent: QWidget | None, title: str, text: str) -> bool:
        """A Yes or No question; True for Yes, and No is the default."""
        box = QMessageBox(QMessageBox.Icon.Question, title, text, parent=parent)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        box.setDefaultButton(QMessageBox.StandardButton.No)
        self._style_box(box)
        return box.exec() == QMessageBox.StandardButton.Yes

    def guide(
        self,
        parent: QWidget | None,
        title: str,
        text: str,
        detail: str,
        buttons: Sequence[tuple[str, Callable[[], None]]],
        close_text: str,
    ) -> None:
        """A message with a longer `detail` and a button for each `(text,
        callback)`, which runs its callback and closes it, and a last one that
        only closes it."""
        box = QMessageBox(QMessageBox.Icon.Information, title, text, parent=parent)
        box.setInformativeText(detail)
        for number, (label, callback) in enumerate(buttons):
            role = (
                QMessageBox.ButtonRole.AcceptRole
                if number == 0
                else QMessageBox.ButtonRole.ActionRole
            )
            button = box.addButton(label, role)
            button.clicked.connect(lambda _checked=False, run=callback: run())
        box.addButton(close_text, QMessageBox.ButtonRole.RejectRole)
        self._style_box(box)
        box.exec()

    def let_window_shrink(self, window: QWidget, shrink: bool) -> None:
        """Let `window` be made as small as its layout allows (a page that
        needs no width), or give back the least it asked."""
        key = id(window)
        if shrink and key not in self._minimums:
            self._minimums[key] = window.minimumSize()
            window.setMinimumSize(QSize(0, 0))
        elif not shrink and key in self._minimums:
            window.setMinimumSize(self._minimums.pop(key))

    def palette(
        self,
        parent: QWidget | None,
        title: str,
        placeholder: str,
        loading: str,
    ) -> Palette:
        return Palette(
            parent,
            lambda color, text=False: self._themed_pair(color, text),
            title,
            placeholder,
            loading,
            self._palette_actions,
        )

    def copy_text(self, text: str) -> None:
        clipboard = QGuiApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(text)

    def open_file(self, parent: QWidget | None, title: str, start: str = "") -> str:
        path, _filter = QFileDialog.getOpenFileName(parent, title, start)
        return path

    def error_banner(
        self,
        details_text: str = "Details",
        hide_text: str = "Hide",
        dismiss_text: str = "Dismiss",
    ) -> ErrorBanner:
        """A red banner for what went wrong: `show_error(text, details)` shows
        a line with the whole error one click away; it starts hidden.

        Put
        `banner.frame` in the page.
        """
        frame = QFrame()
        frame.setObjectName("errorBanner")
        frame.hide()
        label = self.label(wrap=True)
        details = self.button(details_text, "link")
        details.setFlat(True)
        dismiss = self.button(dismiss_text, "link")
        dismiss.setFlat(True)
        details_label = self.label(wrap=True)
        details_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        details_label.hide()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(6)
        layout.addLayout(self.row((label, 1), details, dismiss, spacing=6))
        layout.addWidget(details_label)
        return ErrorBanner(
            frame, label, details, dismiss, details_label, (details_text, hide_text)
        )
