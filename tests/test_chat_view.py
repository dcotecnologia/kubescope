import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import time
from dataclasses import dataclass

from PySide6.QtCore import QMimeData, QPoint, QPointF, Qt, QUrl
from PySide6.QtGui import QColor, QImage, QPixmap, QWheelEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton, QWidget

from kubescope import theme
from kubescope.extensions import chat_view as module
from kubescope.extensions import testing
from kubescope.extensions.chat_view import (
    ChatInput,
    ChatView,
    ClickableFrame,
    MessageText,
)
from tests.qt import get_application

application = get_application()
KEPT: list[object] = []  # until the end: a widget that goes first crashes Qt


@dataclass
class File:
    name: str
    kind: str
    data: bytes

    @property
    def text(self) -> str:
        return self.data.decode("utf-8", "replace")


def chip_at(view: ChatView, index: int) -> QWidget:
    item = view.chips.itemAt(index)
    assert item is not None
    widget = item.widget()
    assert widget is not None
    return widget


def make(texts: dict[str, str] | None = None) -> ChatView:
    view = ChatView(texts or {})
    KEPT.append(view)
    return view


def test_the_chat_says_its_words_in_the_language_it_is_given() -> None:
    view = make({"welcome": "Olá", "placeholder": "Pergunte", "Send": "Enviar"})
    assert view.welcome.text() == "Olá"
    assert view.input.placeholderText() == "Pergunte"
    assert view.send_button.toolTip() == "Enviar"
    view.set_texts({"welcome": "Hi", "Stop": "Parar", "Attach": "Anexar"})
    assert view.welcome.text() == "Hi" and view.stop_button.toolTip() == "Parar"
    assert view.attach_button.toolTip() == "Anexar"
    assert view.send_button.toolTip() == "Send"  # not given: as written


def test_the_buttons_and_the_field_say_what_the_person_did() -> None:
    view = make()
    heard: list[str] = []
    view.submitted.connect(lambda: heard.append("submitted"))
    view.stop_requested.connect(lambda: heard.append("stop"))
    view.attach_requested.connect(lambda: heard.append("attach"))
    view.ring_clicked.connect(lambda: heard.append("ring"))
    view.send_button.click()
    view.stop_button.setEnabled(True)
    view.stop_button.click()
    view.attach_button.click()
    view.ring.clicked.emit()
    assert heard == ["submitted", "stop", "attach", "ring"]

    view.input.setPlainText("first line")
    view.input.moveCursor(view.input.textCursor().MoveOperation.End)
    QTest.keyClick(view.input, Qt.Key.Key_Return, Qt.KeyboardModifier.ShiftModifier)
    QTest.keyClicks(view.input, "second")
    assert view.input.toPlainText() == "first line\nsecond"
    heard.clear()
    QTest.keyClick(view.input, Qt.Key.Key_Enter)  # the one of the numeric pad too
    assert heard == ["submitted"]


def test_a_picture_a_file_and_a_long_text_pasted_into_the_field_are_told() -> None:
    view = make()
    pictures: list[bytes] = []
    files: list[object] = []
    texts: list[str] = []
    view.image_pasted.connect(pictures.append)
    view.files_pasted.connect(files.append)
    view.text_pasted.connect(texts.append)

    image = QImage(40, 30, QImage.Format.Format_RGB32)
    image.fill(QColor("blue"))
    picture = QMimeData()
    picture.setImageData(image)
    assert view.input.canInsertFromMimeData(picture)
    view.input.insertFromMimeData(picture)
    assert pictures and pictures[0].startswith(b"\x89PNG")

    some = QMimeData()
    some.setUrls([QUrl.fromLocalFile("/tmp/app.log")])
    assert view.input.canInsertFromMimeData(some)
    view.input.insertFromMimeData(some)
    assert [str(path) for path in files[0]] == ["/tmp/app.log"]  # type: ignore[attr-defined]

    long = QMimeData()
    long.setText("x" * module.LONG_PASTE)
    view.input.insertFromMimeData(long)
    assert texts == ["x" * module.LONG_PASTE]

    words = QMimeData()
    words.setText("pasted words")
    view.input.insertFromMimeData(words)
    assert view.input.toPlainText() == "pasted words"


def test_the_text_of_a_message_keeps_its_format_and_is_selectable() -> None:
    markdown, plain = MessageText(markdown=True), MessageText(markdown=False)
    KEPT.extend([markdown, plain])
    markdown.setText("**bold** and `code`")
    plain.setText("**not bold**")
    assert markdown.textFormat() == Qt.TextFormat.MarkdownText
    assert plain.textFormat() == Qt.TextFormat.PlainText
    assert markdown.text() == "**bold** and `code`"
    assert "**" not in markdown.toPlainText()
    assert plain.toPlainText() == "**not bold**"
    markdown.selectAll()
    assert markdown.textCursor().selectedText() == "bold and code"
    assert markdown.sizeHint().width() > 0 and markdown.sizeHint().height() > 0


def test_the_wheel_over_a_message_scrolls_the_conversation_not_the_message() -> None:
    text = MessageText(markdown=False)
    KEPT.append(text)
    event = QWheelEvent(
        QPointF(5, 5),
        QPointF(5, 5),
        QPoint(0, 0),
        QPoint(0, -120),
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.ControlModifier,  # which would zoom it
        Qt.ScrollPhase.NoScrollPhase,
        False,
    )
    text.wheelEvent(event)
    assert not event.isAccepted()


def test_a_frame_is_clicked_only_by_the_left_button_inside_it() -> None:
    card = ClickableFrame()
    KEPT.append(card)
    card.resize(40, 40)
    clicked: list[int] = []
    card.clicked.connect(lambda: clicked.append(1))
    QTest.mouseClick(card, Qt.MouseButton.LeftButton, pos=QPoint(5, 5))
    QTest.mouseRelease(card, Qt.MouseButton.LeftButton, pos=QPoint(500, 500))
    QTest.mouseClick(card, Qt.MouseButton.RightButton, pos=QPoint(5, 5))
    assert clicked == [1]


def test_the_ring_fills_with_the_conversation_and_asks_for_its_menu() -> None:
    view = make()
    ring = view.ring
    ring.show()
    for fraction in (0, 0.5, 0.75, 1, 2, -1):
        ring.set_fraction(fraction)
        ring.render(QPixmap(ring.size()))
    assert ring.fraction == 0
    clicked: list[bool] = []
    ring.clicked.connect(lambda: clicked.append(True))
    QTest.mouseClick(ring, Qt.MouseButton.LeftButton)
    assert clicked == [True]


def test_the_usage_is_shown_and_the_cache_timer_follows_it() -> None:
    view = make()
    expired: list[int] = []
    view.usage_expired.connect(lambda: expired.append(1))
    view.set_usage("", "tip", 0.5, "Context: 50% full", 90_000)
    assert view.usage_label.isHidden() and view.ring.isHidden()
    assert view._cache_timer.isActive() and view.ring.toolTip() == "Context: 50% full"
    view.set_usage("tokens", "tip", 1.0, "full", 0)
    assert not view.usage_label.isHidden() and not view.ring.isHidden()
    assert not view._cache_timer.isActive()
    view._cache_timer.timeout.emit()
    assert expired == [1]


def test_the_menu_of_the_ring_compacts_now_or_turns_it_off_by_itself() -> None:
    view = make()
    view.show()
    done: list = []
    menu = view.show_ring_menu(
        ["Context: 10% full", ""],
        "Compact now",
        True,
        lambda: done.append("now"),
        "Compact automatically",
        True,
        done.append,
    )
    labels = [action.text() for action in menu.actions() if action.text()]
    assert labels == ["Context: 10% full", "Compact now", "Compact automatically"]
    now = next(a for a in menu.actions() if a.text() == "Compact now")
    auto = next(a for a in menu.actions() if a.text() == "Compact automatically")
    assert now.isEnabled() and auto.isChecked()
    now.trigger()
    auto.setChecked(False)
    assert done == ["now", False]
    menu.close()


def test_the_bubbles_stand_on_their_sides_and_the_welcome_gives_way() -> None:
    view = make()
    view.resize(500, 400)
    view.show()
    assert view.welcome.isVisible()
    view.add_bubble("user", "hello", "10:00")
    view.add_bubble("assistant", "**bold** answer", "10:01")
    view.add_bubble("app", "noted", "10:02")
    application.processEvents()
    assert not view.welcome.isVisible()

    def side(bubble) -> str:
        return (
            "right"
            if bubble.geometry().center().x() > view.thread_view.width() / 2
            else "left"
        )

    assert [side(b) for b in view._bubbles] == ["right", "left", "left"]
    assert view._labels[0].textFormat() == Qt.TextFormat.PlainText
    assert view._labels[1].textFormat() == Qt.TextFormat.MarkdownText
    stamps = [info[1] for info in view._bubble_info]
    assert stamps[2] is None and stamps[0] is not None
    assert "10:00" in stamps[0].text()

    view.drop_last_bubble()
    view.drop_last_bubble()
    view.drop_last_bubble()
    view.drop_last_bubble()  # nothing left to drop
    assert view.welcome.isVisible() and view._bubbles == []


def test_the_chat_goes_to_the_newest_message_and_keeps_the_sides() -> None:
    view = make()
    view.resize(400, 300)
    view.show()
    for number in range(40):
        view.add_bubble("app", f"line {number}", "10:00")
    for _ in range(10):  # the layout settles over a few turns of the loop
        application.processEvents()
        time.sleep(0.02)
    bar = view.thread_scroll.verticalScrollBar()
    assert bar.value() == bar.maximum() > 0

    bar.setValue(0)  # the person scrolls up to read: the view stays there
    view.add_bubble("app", "a new one", "10:01")
    for _ in range(5):
        application.processEvents()
        time.sleep(0.02)
    assert bar.value() == 0
    bar.setValue(bar.maximum())

    first = view._bubbles[0]
    assert first.maximumWidth() <= int(view.thread_scroll.viewport().width() * 0.82) + 1
    view.resize(700, 300)
    application.processEvents()
    assert view._bubbles[0].maximumWidth() > first.maximumWidth() - 1


def test_the_chat_takes_its_colors_from_the_theme_and_follows_a_change(
    monkeypatch,
) -> None:
    view = make()
    chip = File("a.log", "text", b"x")
    view.show_chips([chip], lambda _i: None, lambda _i: None)
    view.add_bubble("app", "noted", "10:00")
    view.add_bubble("user", "hello", "10:01")
    view.add_bubble("assistant", "hi", "10:02")
    light = [bubble.styleSheet() for bubble in view._bubbles]
    wall = view.thread_view.color.name()
    light_chip = chip_at(view, 0).styleSheet()

    monkeypatch.setattr(theme, "_active", theme.DARK_THEME)
    view.restyle()

    dark = [bubble.styleSheet() for bubble in view._bubbles]
    assert dark != light and view.thread_view.color.name() != wall
    assert theme.themed("#e5f4eb") in dark[1]  # the bubble of the person
    assert theme.themed("#ffffff") in dark[2]  # the bubble of the others
    stamp = view._bubble_info[1][1]
    assert stamp is not None and theme.themed("#176b58") in stamp.text()
    assert theme.themed("#3020a5") in view.send_button.styleSheet()
    assert chip_at(view, 0).styleSheet() != light_chip
    monkeypatch.setattr(theme, "_active", theme.LIGHT_THEME)


def test_the_files_are_chosen_and_shown_as_chips_and_pills(
    monkeypatch, tmp_path
) -> None:
    view = make()
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileNames",
        lambda *_a: ([str(tmp_path / "a.log")], ""),
    )
    assert view.choose_files("Attach", "*.log") == [tmp_path / "a.log"]

    log = File("app.log", "text", b"one\ntwo\n")
    shot = File("shot.png", "image", testing.png_bytes(30, 20))
    opened: list[str] = []
    detached: list[str] = []
    view.show_chips(
        [log, shot], lambda i: opened.append(i.name), lambda i: detached.append(i.name)
    )
    view.show()
    assert view.chip_bar.isVisible() and view.chips.count() == 3  # two cards, a stretch
    first = chip_at(view, 0)
    QTest.mouseClick(first, Qt.MouseButton.LeftButton, pos=QPoint(5, 20))
    assert opened == ["app.log"]
    next(b for b in first.findChildren(QPushButton) if b.text() == "×").click()
    assert detached == ["app.log"]
    pictured = chip_at(view, 1)
    assert any(
        label.pixmap() is not None and not label.pixmap().isNull()
        for label in pictured.findChildren(QLabel)
    )

    view.show_chips([], lambda _i: None, lambda _i: None)
    assert not view.chip_bar.isVisible()

    view.add_bubble(
        "user", "look", "10:00", [log, shot], lambda i: opened.append("pill " + i.name)
    )
    pills = [frame for frame in view._bubbles[0].findChildren(ClickableFrame)]
    assert len(pills) == 2
    QTest.mouseClick(pills[0], Qt.MouseButton.LeftButton, pos=QPoint(5, 5))
    assert opened[-1] == "pill app.log"
    details = [label.text() for label in pills[1].findChildren(QLabel)]
    assert "30×20" in details


def test_an_attachment_is_opened_from_a_copy_and_a_failed_copy_is_told(
    monkeypatch,
) -> None:
    view = make()
    opened: list[str] = []
    monkeypatch.setattr(
        module.QDesktopServices, "openUrl", lambda url: opened.append(url.toLocalFile())
    )
    item = File("a.log", "text", b"x")
    assert view.open_attachment(item) == ""
    assert opened[-1].endswith("a.log")

    def broken(_self, _data):
        raise OSError(13, "Permission denied")

    monkeypatch.setattr(module.Path, "write_bytes", broken)
    assert "Permission denied" in view.open_attachment(item)
    assert len(opened) == 1


def test_the_status_the_busy_buttons_and_the_action_cards() -> None:
    view = make()
    view.show()
    view.show_status("Thinking...")
    assert view.status.isVisible() and view.status.text() == "Thinking..."
    view.show_status("")
    assert not view.status.isVisible()

    view.set_busy(True)
    assert view.stop_button.isVisible() and not view.send_button.isVisible()
    view.set_busy(False)
    assert view.send_button.isVisible() and not view.stop_button.isVisible()

    ran: list[str] = []
    card = view.add_action_card(
        "scale web",
        "Run",
        "Cancel",
        lambda: ran.append("run"),
        lambda: ran.append("cancel"),
    )
    assert view.cards.count() == 1
    buttons = card.findChildren(QPushButton)
    buttons[0].click()
    buttons[1].click()
    assert ran == ["run", "cancel"]
    view.remove_card(card)
    assert view.cards.count() == 0


def test_the_components_make_the_chat_and_the_picture_is_a_png() -> None:
    from kubescope.extensions.components import UiComponents

    view = UiComponents().chat_view({"welcome": "Hi"})
    KEPT.append(view)
    assert view.welcome.text() == "Hi"
    image = QImage(10, 10, QImage.Format.Format_RGB32)
    got: list[bytes] = []
    view.image_pasted.connect(got.append)
    view._image_pasted(image)
    assert got[0].startswith(b"\x89PNG")
    QApplication.processEvents()
    assert ChatInput is not None
