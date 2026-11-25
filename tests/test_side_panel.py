import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QCoreApplication, QEvent, QPoint, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

from kubescope.extensions.components import UiComponents
from kubescope.extensions.side_panel import (
    MAX_WIDTH,
    MIN_WIDTH,
    WIDTH,
    NoticeCard,
    SidePanel,
    style,
)
from tests.qt import get_application

application = get_application()
KEPT: list[object] = []  # until the end: a widget that goes first crashes Qt
COMPONENTS = UiComponents()


def make_panel(host: QWidget | None = None) -> SidePanel:
    host = host or QWidget()
    host.resize(900, 600)
    KEPT.append(host)
    actions = [COMPONENTS.button("Mark all"), COMPONENTS.button("Clear")]
    panel = COMPONENTS.side_panel(
        host, "Notifications", actions, lambda: 50, "x", "Nothing"
    )
    panel.actions = actions  # type: ignore[attr-defined]
    return panel


def card(message: str = "it broke", unread: bool = True, **extra: object) -> NoticeCard:
    clicks: list[str] = extra.pop("clicks", [])  # type: ignore[assignment]
    made = COMPONENTS.notice_card(
        str(extra.get("title", "Boom")),
        "Error",
        str(extra.get("about", "prod · Pod/api")),
        message,
        "3m ago",
        "error",
        unread,
        "Mark as read",
        lambda: clicks.append(message),
        extra.get("actions", ()),  # type: ignore[arg-type]
    )
    KEPT.append(made)
    return made


def texts(panel: SidePanel) -> list[str]:
    return [label.text() for label in panel.list.findChildren(QLabel)]


def settle(panel: SidePanel) -> None:
    panel.animation.setCurrentTime(panel.animation.duration())
    panel.animation.finished.emit()


def test_the_style_has_the_colors_of_the_theme() -> None:
    assert "#ffffff" in style(lambda color, text: color)


def test_the_cards_are_drawn_and_an_empty_list_says_so() -> None:
    panel = make_panel()
    panel.show_cards([card("one"), card("two")])
    assert "one" in texts(panel) and "two" in texts(panel)
    panel.show_cards([])  # the cards are replaced, not piled up
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
    assert texts(panel) == ["Nothing"]
    panel.restyle()


def test_it_slides_in_from_the_right_and_out_again() -> None:
    host = QWidget()
    panel = make_panel(host)
    host.show()
    closed: list[bool] = []
    panel.on_closed = lambda: closed.append(True)

    panel.close_panel()  # closed already: nothing happens
    assert closed == []

    panel.open_panel()
    assert panel.opened
    settle(panel)
    assert panel.pos() == QPoint(900 - WIDTH, 50)
    assert panel.height() == 550

    host.resize(1000, 700)  # the window is resized with the panel open
    assert panel.pos() == QPoint(1000 - WIDTH, 50)

    panel.close_panel()
    assert closed == [True] and not panel.opened
    settle(panel)
    assert panel.isHidden()
    assert panel.pos().x() == 1000

    host.resize(1100, 700)  # closed: it stays where it is
    assert panel.pos().x() == 1000


def test_the_close_button_and_esc_close_it_only_while_it_is_open() -> None:
    host = QWidget()
    panel = make_panel(host)
    closed: list[bool] = []
    panel.on_closed = lambda: closed.append(True)
    assert not panel._escape.isEnabled()  # closed: the key is the window's

    panel.open_panel()
    assert panel._escape.isEnabled()
    panel._escape.activated.emit()
    assert closed == [True] and not panel.opened
    assert not panel._escape.isEnabled()

    panel.open_panel()
    panel.close_button.click()
    assert closed == [True, True]


def mouse(panel: SidePanel, kind: QEvent.Type, x: float) -> None:
    event = QMouseEvent(
        kind,
        QPointF(2, 20),
        QPointF(x, 20),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    QApplication.sendEvent(panel.grip, event)


def test_it_is_dragged_by_its_left_edge_and_the_width_is_handed_on() -> None:
    host = QWidget()
    panel = make_panel(host)
    host.show()
    kept: list[int] = []
    panel.on_resized = kept.append
    panel.open_panel()
    settle(panel)

    mouse(panel, QEvent.Type.MouseMove, 500.0)  # no press yet: nothing moves
    assert panel.width() == WIDTH
    mouse(panel, QEvent.Type.MouseButtonPress, 600.0)
    mouse(panel, QEvent.Type.MouseMove, 520.0)  # 80 px to the left: 80 px wider
    assert panel.width() == WIDTH + 80
    assert panel.pos().x() == 900 - (WIDTH + 80)  # it stays at the right edge
    mouse(panel, QEvent.Type.MouseButtonRelease, 520.0)
    assert kept == [WIDTH + 80]
    mouse(panel, QEvent.Type.MouseButtonRelease, 520.0)  # one release only
    assert kept == [WIDTH + 80]


def test_the_width_stays_within_what_is_usable_and_what_the_window_allows() -> None:
    host = QWidget()
    panel = make_panel(host)

    panel.set_panel_width(10)
    assert panel.width() == MIN_WIDTH
    panel.set_panel_width(10**6)
    assert panel.width() == 900 - 40  # the window has room for 40 px of its own
    host.resize(380, 600)  # a window narrower than the panel
    panel.open_panel()
    assert panel.width() == 340
    assert panel.width() < MAX_WIDTH


def test_the_place_in_the_list_is_kept_when_it_is_drawn_again() -> None:
    host = QWidget()
    panel = make_panel(host)
    host.resize(900, 300)
    host.show()
    cards = [card(f"message {n}") for n in range(30)]
    panel.show_cards(cards)
    panel.open_panel()
    panel.animation.setCurrentTime(panel.animation.duration())
    QApplication.processEvents()
    bar = panel.scroller.verticalScrollBar()
    bar.setValue(bar.maximum() // 2)
    place = bar.value()
    assert place > 0

    panel.show_cards([card(f"message {n}") for n in range(30)])
    for _ in range(3):
        QApplication.processEvents()

    assert bar.value() == place
    panel._place = 10**6  # a place the list never grows back to
    panel._restore_place(0, 100)
    assert panel._place == 10**6  # kept until the moment is over
    panel._forget_place()
    assert panel._place is None


def press(widget: QWidget, position: QPoint, kind: QEvent.Type | None = None) -> None:
    event = QMouseEvent(
        kind or QEvent.Type.MouseButtonPress,
        QPointF(widget.mapFromGlobal(position)),
        QPointF(position),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    QApplication.sendEvent(widget, event)


def test_a_click_outside_closes_the_panel_but_not_one_inside_or_on_its_button() -> None:
    host = QWidget()
    host.resize(900, 600)
    other = QWidget(host)
    other.setGeometry(0, 0, 300, 600)
    bell = QPushButton(host)
    bell.setGeometry(800, 0, 40, 40)
    panel = make_panel(host)
    panel.is_inside = lambda position: bell.rect().contains(
        bell.mapFromGlobal(position)
    )
    closed: list[bool] = []
    panel.on_closed = lambda: closed.append(True)
    host.show()
    panel.open_panel()
    settle(panel)

    press(panel, panel.mapToGlobal(QPoint(20, 100)))  # on the panel
    press(bell, bell.mapToGlobal(QPoint(5, 5)))  # on its button: it closes itself
    press(other, other.mapToGlobal(QPoint(20, 100)), QEvent.Type.MouseButtonRelease)
    assert panel.opened and closed == []

    press(other, other.mapToGlobal(QPoint(20, 100)))  # on the rest of the window

    assert not panel.opened and closed == [True]
    press(other, other.mapToGlobal(QPoint(20, 100)))  # closed: nothing more to close
    assert closed == [True]


def test_a_click_of_another_window_is_not_a_click_outside() -> None:
    host = QWidget()
    host.resize(900, 600)
    panel = make_panel(host)
    elsewhere = QWidget()  # a window of its own
    host.show()
    elsewhere.show()
    panel.open_panel()

    press(elsewhere, elsewhere.mapToGlobal(QPoint(5, 5)))

    assert panel.opened
    panel.close_panel()
    elsewhere.close()


def release(widget: QWidget, point: QPointF, button: Qt.MouseButton) -> QMouseEvent:
    return QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        point,
        point,
        button,
        button,
        Qt.KeyboardModifier.NoModifier,
    )


def test_a_card_says_what_happened_and_a_click_reads_it() -> None:
    clicks: list[str] = []
    one = card("it broke", clicks=clicks)
    shown = [label.text() for label in one.findChildren(QLabel)]
    assert "Boom" in shown and "Error" in shown and "prod · Pod/api" in shown
    assert "it broke" in shown and "3m ago" in shown
    assert one.toolTip() == "Mark as read"
    assert one.property("read") == "false" and one.property("level") == "error"

    one.mouseReleaseEvent(release(one, QPointF(5, 5), Qt.MouseButton.LeftButton))
    assert clicks == ["it broke"]
    one.mouseReleaseEvent(release(one, QPointF(5, 5), Qt.MouseButton.RightButton))
    one.mouseReleaseEvent(release(one, QPointF(5000, 5), Qt.MouseButton.LeftButton))
    assert clicks == ["it broke"]  # only a left click inside it


def test_a_read_card_is_crossed_out_and_an_unread_one_is_not() -> None:
    def crossed(made: NoticeCard) -> list[bool]:
        return [
            label.font().strikeOut()
            for label in made.findChildren(QLabel)
            if label.objectName() in ("noticeReason", "noticeMessage")
        ]

    assert crossed(card(unread=True)) == [False, False]
    read = card(unread=False)
    assert crossed(read) == [True, True] and read.property("read") == "true"


def test_the_links_of_a_card_do_what_they_were_given() -> None:
    done: list[str] = []
    bare = card(about="")
    assert bare.buttons == []
    linked = card(actions=[("Go", lambda: done.append("go")), ("Off", lambda: None)])
    assert [button.text() for button in linked.buttons] == ["Go", "Off"]
    linked.buttons[0].click()
    assert done == ["go"]


def test_the_counter_button_counts_and_stops_at_99() -> None:
    from PySide6.QtGui import QIcon

    button = COMPONENTS.counter_button(QIcon(), "Notifications", "myBell")
    KEPT.append(button)
    button.resize(32, 32)
    assert button.badge_text() == "0"
    button.grab()  # nothing to paint over the icon
    button.set_unread(7)
    assert button.badge_text() == "7"
    button.grab()  # paints the badge
    button.set_unread(250)
    assert button.badge_text() == "99+"
    button.set_unread(-3)
    assert button.unread == 0
    assert button.objectName() == "myBell"


def test_the_counter_button_takes_the_colors_of_the_theme() -> None:
    from PySide6.QtGui import QIcon

    dark = {"#0d315d": "#222831", "#1f4f87": "#2f3640"}
    components = UiComponents(themed_text=lambda color, text: dark.get(color, color))
    button = components.counter_button(QIcon(), "Notifications")
    KEPT.append(button)
    sheet = button.styleSheet()
    assert "#222831" in sheet and "#2f3640" in sheet
    assert "#0d315d" not in sheet and "#1f4f87" not in sheet
    button.restyle(lambda color, text: "#abcdef")  # the theme changed
    assert button.styleSheet().count("#abcdef") == 2
