import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import time

from kubescope.extensions.components import UiComponents
from tests.qt import get_application

application = get_application()


def wait(worker) -> None:
    worker.wait(3000)
    for _ in range(5):
        application.processEvents()
        time.sleep(0.005)


def test_a_function_gives_one_answer_off_the_ui_thread() -> None:
    got: list = []
    finished: list = []
    worker = UiComponents().background(
        lambda: 6 * 7, on_done=got.append, on_finished=lambda: finished.append(1)
    )
    wait(worker)
    assert got == [42] and finished == [1]


def test_a_failure_is_told_with_its_message() -> None:
    told: list[str] = []

    def boom() -> int:
        raise RuntimeError("it broke")

    worker = UiComponents().background(boom, on_error=told.append)
    wait(worker)
    assert told == ["it broke"]


def test_a_generator_hands_over_its_pieces_and_is_closed() -> None:
    pieces: list = []
    closed: list[int] = []

    def produce():
        try:
            yield from ("a", "b", "c")
        finally:
            closed.append(1)

    worker = UiComponents().background(produce, on_piece=pieces.append, stream=True)
    wait(worker)
    assert pieces == ["a", "b", "c"] and closed == [1]


def test_a_stopped_stream_hands_over_no_more_and_closes_the_generator() -> None:
    pieces: list = []
    closed: list[int] = []

    def produce():
        try:
            for number in range(1000):
                time.sleep(0.002)
                yield number
        finally:
            closed.append(1)

    worker = UiComponents().background(produce, on_piece=pieces.append, stream=True)
    worker.stopped = True
    wait(worker)
    assert len(pieces) < 1000 and closed == [1]


def test_a_stream_that_fails_tells_it_and_closes() -> None:
    told: list[str] = []

    def produce():
        yield "a"
        raise ValueError("cut")

    worker = UiComponents().background(
        produce, on_piece=lambda _p: None, on_error=told.append, stream=True
    )
    wait(worker)
    assert told == ["cut"]
