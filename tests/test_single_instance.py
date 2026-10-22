import os
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from kubescope.utils import single_instance
from kubescope.utils.single_instance import SingleInstance, server_name


def _wait(condition) -> None:
    deadline = time.monotonic() + 3
    while not condition() and time.monotonic() < deadline:
        QApplication.processEvents()


def test_the_name_is_the_persons_own(monkeypatch) -> None:
    monkeypatch.setattr(single_instance.getpass, "getuser", lambda: "ana")

    assert server_name() == "kubescope-ana"
    assert SingleInstance().name == "kubescope-ana"


def test_a_second_start_finds_the_first_and_asks_it_to_come_forward() -> None:
    QApplication.instance() or QApplication([])
    name = f"kubescope-test-{os.getpid()}"
    first = SingleInstance(name)
    asked = []
    first.activated.connect(lambda: asked.append(True))

    assert first.notify_running() is False  # nobody is there yet
    assert first.listen() is True

    second = SingleInstance(name)
    assert second.notify_running() is True
    _wait(lambda: asked)
    assert asked == [True]
    first.server.close()


def test_a_name_left_behind_is_taken_over() -> None:
    QApplication.instance() or QApplication([])
    name = f"kubescope-stale-{os.getpid()}"
    stale = SingleInstance(name)
    stale.listen()
    stale.server.close()

    assert SingleInstance(name).listen() is True
