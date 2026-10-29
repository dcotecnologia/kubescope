import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import time

import pytest
from PySide6.QtWidgets import QApplication

from kubescope.assistant import session as chat
from kubescope.assistant.runner import Assistant, AssistantError
from kubescope.assistant.session import ChatSession
from kubescope.views import assistant_tab
from kubescope.views.assistant_tab import AnswerWorker, AssistantTab, ReadWorker

application = QApplication.instance() or QApplication([])
FAKE = Assistant("fake", "Fake", "fake-ai", lambda m, s: [], lambda line: ("", ""))


def _block(document: str) -> str:
    return f"```kubescope-action\n{document}\n```\n"


def settle(tab: AssistantTab) -> None:
    deadline = time.monotonic() + 5
    while tab.busy and time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.005)
    application.processEvents()


@pytest.fixture
def replies(monkeypatch):
    """The program answers with the next of these (a list of pieces, or an
    error); the prompts it got are kept in `prompts`."""
    queue: list = []
    prompts: list[str] = []

    def ask(assistant, prompt, model, system, images=()):
        prompts.append(prompt)
        reply = queue.pop(0)
        if isinstance(reply, Exception):
            raise reply
        yield from reply

    monkeypatch.setattr(chat.runner, "ask", ask)
    return queue, prompts


def _tab(write_mode=True, fetch=None) -> AssistantTab:
    kwargs = {"fetch": fetch} if fetch else {}
    return AssistantTab(ChatSession(FAKE), "ctx", lambda: write_mode, **kwargs)


def _card(tab: AssistantTab):
    item = tab.cards.itemAt(0)
    assert item is not None
    card = item.widget()
    assert card is not None
    return card


def _say(tab: AssistantTab, text: str) -> None:
    tab.input.setPlainText(text)
    tab.send_button.click()
    settle(tab)


def test_the_question_is_sent_and_the_answer_is_shown_as_it_comes(replies) -> None:
    queue, prompts = replies
    queue.append(["It is ", "a Pod."])
    tab = _tab()

    _say(tab, "  what is x?  ")

    assert "what is x?" in prompts[0]
    assert "**You**\n\nwhat is x?" in tab.markdown()
    assert "**Assistant**\n\nIt is a Pod." in tab.markdown()
    assert tab.input.toPlainText() == "" and tab.status.text() == ""
    assert tab.send_button.isEnabled() and not tab.stop_button.isEnabled()
    assert [label.text() for label in tab._labels] == ["what is x?", "It is a Pod."]


def test_an_empty_question_or_one_while_busy_is_ignored(replies) -> None:
    queue, prompts = replies
    queue.append(["ok"])
    tab = _tab()

    _say(tab, "   ")
    assert prompts == []

    tab.input.setPlainText("first")
    tab.submit()
    tab.input.setPlainText("second")
    tab.submit()  # still answering the first
    settle(tab)

    assert len(prompts) == 1 and tab.input.toPlainText() == "second"


def test_a_failure_is_said_and_the_question_is_taken_back(replies) -> None:
    queue, _prompts = replies
    queue.append(AssistantError("Not logged in"))
    tab = _tab()

    _say(tab, "why?")

    assert "Not logged in" in tab.status.text()
    assert "why?" not in tab.markdown() and tab.session.messages == []
    assert tab.send_button.isEnabled()


def test_navigation_runs_at_once_and_the_blocks_are_not_shown(replies) -> None:
    queue, _prompts = replies
    queue.append(["Opening.\n", _block('{"action": "open_view", "view": "pods"}')])
    tab = _tab()
    seen: list = []
    tab.navigate.connect(seen.append)

    _say(tab, "show pods")

    assert [request.action.name for request in seen] == ["open_view"]
    assert "Opening." in tab.markdown() and "kubescope-action" not in tab.markdown()


def test_a_change_waits_for_the_person_and_can_be_run_or_cancelled(replies) -> None:
    queue, _prompts = replies
    scale = '{"action": "scale", "namespace": "ns", "name": "web", "replicas": 2}'
    queue.extend([[_block(scale)], [_block(scale)]])
    tab = _tab()
    confirmed: list = []
    tab.write.connect(confirmed.append)

    _say(tab, "scale web")
    assert tab.cards.count() == 1 and confirmed == []
    card = _card(tab)
    buttons = card.findChildren(assistant_tab.QPushButton)
    buttons[0].click()  # Run
    assert [request.action.name for request in confirmed] == ["scale"]
    assert tab.cards.count() == 0

    _say(tab, "again")
    card = _card(tab)
    card.findChildren(assistant_tab.QPushButton)[1].click()  # Cancel
    assert tab.cards.count() == 0 and len(confirmed) == 1


def test_a_change_cannot_be_run_while_the_write_mode_is_off(replies) -> None:
    queue, _prompts = replies
    queue.append([_block('{"action": "restart", "namespace": "ns", "name": "web"}')])
    tab = _tab(write_mode=False)

    _say(tab, "restart web")

    card = _card(tab)
    run = card.findChildren(assistant_tab.QPushButton)[0]
    assert not run.isEnabled()
    assert "write mode is off" in card.findChildren(assistant_tab.QLabel)[0].text()


def test_a_block_that_does_not_fit_the_catalog_is_noted(replies) -> None:
    queue, _prompts = replies
    queue.append([_block('{"action": "rm_rf"}')])
    tab = _tab()

    _say(tab, "do it")

    assert "Ignored an action: there is no action rm_rf" in tab.markdown()


def test_a_read_goes_back_to_the_assistant_as_the_next_message(replies) -> None:
    queue, prompts = replies
    details = '{"action": "get_details", "kind": "Pod", "namespace": "ns", "name": "p"}'
    queue.extend([[_block(details)], ["It is healthy."]])
    reads: list = []

    def fetch(request, context):
        reads.append((request.action.name, context))
        return "DATA OF THE POD"

    tab = _tab(fetch=fetch)

    _say(tab, "check p")

    assert reads == [("get_details", "ctx")]
    assert "DATA OF THE POD" in prompts[1]
    assert "DATA OF THE POD" not in tab.markdown()  # the person sees what was read
    assert "(read) get_details(kind=Pod, namespace=ns, name=p)" in tab.markdown()
    assert "It is healthy." in tab.markdown()
    assert tab.send_button.isEnabled()


def test_the_assistant_cannot_keep_reading_forever(replies) -> None:
    queue, prompts = replies
    again = _block('{"action": "get_logs", "namespace": "ns", "pod": "p"}')
    queue.extend([[again]] * (assistant_tab.MAX_FOLLOW_UPS + 1))
    tab = _tab(fetch=lambda request, context: "log")

    _say(tab, "look")

    assert len(prompts) == assistant_tab.MAX_FOLLOW_UPS + 1
    assert "too many reads" in tab.markdown()
    assert tab.send_button.isEnabled()


def test_a_worker_that_was_stopped_sends_nothing_and_closes_the_answer(
    replies,
) -> None:
    queue, _prompts = replies
    queue.append(["one", "two"])
    worker = AnswerWorker(ChatSession(FAKE), "why?")
    pieces: list[str] = []
    worker.piece.connect(pieces.append)
    worker.stopped = True

    worker.run()

    assert pieces == []
    _tab().stop()  # nothing running: nothing to stop


def test_the_chat_goes_to_the_newest_message_and_keeps_the_sides(replies) -> None:
    tab = _tab()
    tab.resize(400, 300)
    tab.show()
    for number in range(40):
        tab.note(f"line {number}")
    for _ in range(10):  # the layout settles over a few turns of the loop
        application.processEvents()
        time.sleep(0.02)
    bar = tab.thread_scroll.verticalScrollBar()
    assert bar.value() == bar.maximum() > 0

    bar.setValue(0)  # the person scrolls up to read: the view stays there
    tab.note("a new one")
    for _ in range(5):
        application.processEvents()
        time.sleep(0.02)
    assert bar.value() == 0
    bar.setValue(bar.maximum())

    first = tab._bubbles[0]
    assert first.maximumWidth() <= int(tab.thread_scroll.viewport().width() * 0.82) + 1
    tab.resize(700, 300)
    application.processEvents()
    assert tab._bubbles[0].maximumWidth() > first.maximumWidth() - 1
    tab.close()


def test_closing_the_tab_stops_what_is_running(replies) -> None:
    queue, _prompts = replies
    queue.append(["slow"])
    tab = _tab()

    tab.input.setPlainText("go")
    tab.submit()
    tab.shutdown()
    assert tab.closed
    settle(tab)

    reader = ReadWorker(lambda: "x")
    tab._reader = reader
    reader.start()
    tab.shutdown()
    tab._reader = None
    _tab().shutdown()  # nothing running


def test_stop_cuts_the_answer_short_and_keeps_what_came(replies) -> None:
    queue, _prompts = replies

    def slow():
        yield "first "
        time.sleep(0.3)
        yield "second"

    queue.append(slow())
    tab = _tab()

    tab.input.setPlainText("go")
    tab.submit()
    deadline = time.monotonic() + 5
    while tab._stream is None and time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.005)
    assert "first" in tab.markdown()  # the answer is there as it comes
    tab.stop_button.click()
    settle(tab)

    assert "first" in tab.markdown() and "second" not in tab.markdown()
    assert tab.send_button.isEnabled()


def test_the_question_goes_with_what_the_window_shows_now(replies) -> None:
    queue, prompts = replies
    queue.append(["ok"])
    tab = AssistantTab(
        ChatSession(FAKE),
        "ctx",
        lambda: True,
        screen=lambda: "Context: prod\nPage: pods",
    )

    _say(tab, "what is wrong?")

    assert "[What the person sees in KubeScope right now]\nContext: prod" in prompts[0]
    assert "Page: pods" not in tab.markdown()  # the person is not shown it again


def test_what_the_person_writes_is_on_the_right_and_the_rest_on_the_left(
    replies,
) -> None:
    queue, _prompts = replies
    queue.append(["**bold** answer"])
    tab = _tab()
    tab.resize(500, 400)
    tab.show()

    _say(tab, "hello")
    tab.note("noted")
    application.processEvents()

    def side(bubble) -> str:
        row = bubble.geometry().center().x() > tab.thread_view.width() / 2
        return "right" if row else "left"

    mine, answer, noted = tab._bubbles
    assert [side(b) for b in (mine, answer, noted)] == ["right", "left", "left"]
    assert tab._labels[0].textFormat() == assistant_tab.Qt.TextFormat.PlainText
    assert tab._labels[1].textFormat() == assistant_tab.Qt.TextFormat.MarkdownText
    tab.close()


def test_the_conversation_comes_back_from_the_history_and_goes_to_it(replies) -> None:
    queue, prompts = replies
    queue.append(["Sure."])
    saved: list = []
    kept = [
        ("user", "earlier question"),
        ("assistant", "earlier answer"),
        ("app", "Done: scale()"),
    ]
    tab = AssistantTab(ChatSession(FAKE), "ctx", lambda: True, history=kept)
    tab.changed.connect(lambda: saved.append(tab.entries()))

    assert [label.text() for label in tab._labels] == [text for _role, text in kept]
    assert [m.role for m in tab.session.messages] == ["user", "assistant"]

    _say(tab, "and now?")

    assert "earlier question" in prompts[0] and "earlier answer" in prompts[0]
    assert "Done: scale()" not in prompts[0]  # a note of the app is not a message
    assert saved[-1][-2:] == [("user", "and now?"), ("assistant", "Sure.")]
    assert tab.entries()[:3] == kept


def test_a_failure_after_half_an_answer_takes_both_bubbles_back(replies) -> None:
    queue, _prompts = replies

    def half():
        yield "half an ans"
        raise AssistantError("cut off")

    queue.append(half())
    tab = _tab()

    _say(tab, "why?")

    assert "cut off" in tab.status.text()
    assert tab._bubbles == [] and tab._labels == [] and tab.entries() == []
    assert tab.send_button.isEnabled()


def test_the_chat_takes_its_colors_from_the_theme_and_follows_a_change(
    replies, monkeypatch
) -> None:
    from kubescope import theme

    tab = _tab()
    tab.note("noted")
    tab._add_entry("user", "hello")
    tab._add_entry("assistant", "hi")
    light = [bubble.styleSheet() for bubble in tab._bubbles]
    wall = tab.thread_view.color.name()

    monkeypatch.setattr(theme, "_active", theme.DARK_THEME)
    tab.restyle()

    dark = [bubble.styleSheet() for bubble in tab._bubbles]
    assert dark != light and tab.thread_view.color.name() != wall
    assert theme.themed("#e5f4eb") in dark[1]  # the bubble of the person
    assert theme.themed("#ffffff") in dark[2]  # the bubble of the others
    stamp = tab._bubble_info[1][1]
    assert stamp is not None and theme.themed("#176b58") in stamp.text()
    assert theme.themed("#3020a5") in tab.send_button.styleSheet()  # as Save changes
    monkeypatch.setattr(theme, "_active", theme.LIGHT_THEME)


def _picture(path, color="red") -> None:
    from PySide6.QtGui import QColor, QImage

    image = QImage(300, 200, QImage.Format.Format_RGB32)
    image.fill(QColor(color))
    assert image.save(str(path))


def test_the_plus_picks_files_that_wait_as_chips_until_the_question_goes(
    replies, monkeypatch, tmp_path
) -> None:
    queue, prompts = replies
    queue.append(["I see."])
    seen: list = []
    monkeypatch.setattr(
        assistant_tab.ChatInput, "canInsertFromMimeData", lambda *_a: True
    )
    log = tmp_path / "app.log"
    log.write_text("boom\n", encoding="utf-8")
    shot = tmp_path / "shot.png"
    _picture(shot)
    monkeypatch.setattr(
        assistant_tab.QFileDialog,
        "getOpenFileNames",
        lambda *_a: ([str(log), str(shot)], ""),
    )
    tab = _tab()
    tab.show()

    tab.attach_button.click()

    assert [item.name for item in tab._pending] == ["app.log", "shot.png"]
    assert tab.chip_bar.isVisible() and tab.chips.count() == 3  # two chips, a stretch

    tab.input.setPlainText("what is this?")
    tab.send_button.click()
    settle(tab)

    assert "Attached file app.log" in prompts[0] and "boom" in prompts[0]
    assert tab._pending == [] and not tab.chip_bar.isVisible()
    # the bubble shows the picture and the question; the history holds only names
    first = tab._bubbles[0]
    assert any(
        label.pixmap() is not None and not label.pixmap().isNull()
        for label in first.findChildren(assistant_tab.QLabel)
    )
    assert tab.entries()[0] == (
        "user",
        "what is this?\n(attached: app.log, shot.png)",
    )
    del seen
    tab.close()


def test_a_chip_can_be_taken_off_and_a_question_can_be_only_the_files(
    replies, tmp_path
) -> None:
    queue, prompts = replies
    queue.append(["ok"])
    a, b = tmp_path / "a.log", tmp_path / "b.log"
    a.write_text("A", encoding="utf-8")
    b.write_text("B", encoding="utf-8")
    tab = _tab()
    tab.attach(a)
    tab.attach(b)

    tab._detach(tab._pending[0])
    assert [item.name for item in tab._pending] == ["b.log"]

    tab.send_button.click()  # no text, one file
    settle(tab)

    assert "See what is attached." in prompts[0] and "B" in prompts[0]
    assert tab.entries()[0] == ("user", "(attached: b.log)")
    assert tab._labels[0].isHidden()  # no text to show, only the file


def test_a_file_that_cannot_be_attached_says_why_and_is_left_out(tmp_path) -> None:
    tab = _tab()
    (tmp_path / "tool.exe").write_bytes(b"MZ")

    tab.attach(tmp_path / "tool.exe")

    assert "not an image or a text file" in tab.status.text()
    assert tab._pending == [] and not tab.chip_bar.isVisible()


def test_no_more_than_four_files_go_with_a_question(tmp_path) -> None:
    tab = _tab()
    for number in range(5):
        path = tmp_path / f"f{number}.log"
        path.write_text("x", encoding="utf-8")
        tab.attach(path)

    assert len(tab._pending) == 4
    assert "At most 4 files" in tab.status.text()


def test_an_assistant_that_takes_text_only_refuses_images(tmp_path) -> None:
    tab = AssistantTab(ChatSession(FAKE), "ctx", lambda: True, takes_images=False)
    shot = tmp_path / "shot.png"
    _picture(shot)
    note = tmp_path / "n.txt"
    note.write_text("hello", encoding="utf-8")

    tab.attach(shot)
    assert tab._pending == [] and "takes text files only" in tab.status.text()
    tab.attach(note)
    assert [item.name for item in tab._pending] == ["n.txt"]
    assert tab.status.isHidden()  # the notice went away with a good attachment


def test_a_picture_pasted_into_the_field_is_attached_and_text_is_pasted_as_text(
    monkeypatch,
) -> None:
    from PySide6.QtCore import QMimeData
    from PySide6.QtGui import QColor, QImage

    tab = _tab()
    image = QImage(40, 30, QImage.Format.Format_RGB32)
    image.fill(QColor("blue"))
    picture = QMimeData()
    picture.setImageData(image)

    assert tab.input.canInsertFromMimeData(picture)
    tab.input.insertFromMimeData(picture)
    tab.input.insertFromMimeData(picture)
    words = QMimeData()
    words.setText("pasted words")
    tab.input.insertFromMimeData(words)

    assert [item.name for item in tab._pending] == ["pasted-1.png", "pasted-2.png"]
    assert tab._pending[0].data.startswith(b"\x89PNG")
    assert tab.input.toPlainText() == "pasted words"

    monkeypatch.setattr(assistant_tab.attachments, "MAX_IMAGE_BYTES", 10)
    tab.attach_image(image)
    assert "The picture is too large." in tab.status.text()
    assert len(tab._pending) == 2


def _chip(tab: AssistantTab):
    item = tab.chips.itemAt(0)
    assert item is not None
    widget = item.widget()
    assert widget is not None
    return widget


def test_the_chips_take_the_colors_of_the_theme(monkeypatch, tmp_path) -> None:
    from kubescope import theme

    tab = _tab()
    path = tmp_path / "a.log"
    path.write_text("x", encoding="utf-8")
    tab.attach(path)
    light = _chip(tab).styleSheet()

    monkeypatch.setattr(theme, "_active", theme.DARK_THEME)
    tab.restyle()

    assert _chip(tab).styleSheet() != light
    monkeypatch.setattr(theme, "_active", theme.LIGHT_THEME)
