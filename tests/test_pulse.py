import os
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget

from kubescope.views import motion
from kubescope.views.pulse import DURATION_MS, _Ring, pulse
from tests.qt import get_application

application = get_application()
KEPT: list[QWidget] = []  # until the end: a widget that goes first crashes Qt


def _host() -> tuple[QWidget, QWidget]:
    host = QWidget()
    host.resize(300, 100)
    child = QWidget(host)
    child.setGeometry(40, 30, 120, 30)
    KEPT.append(host)
    host.show()
    return host, child


def test_a_ring_spreads_around_the_widget_and_goes_away(monkeypatch) -> None:
    monkeypatch.setattr(motion, "ENABLED", True)  # the tests run without motion
    host, child = _host()

    pulse(child, "#9b8cff")

    (ring,) = host.findChildren(_Ring)
    assert ring.geometry().contains(child.geometry())  # it surrounds it
    ring.setProperty("progress", 0.5)
    assert not ring.grab().isNull()  # painted half way
    end = time.monotonic() + DURATION_MS / 1000 + 2
    while host.findChildren(_Ring) and time.monotonic() < end:
        QCoreApplication.processEvents()
        QCoreApplication.sendPostedEvents(None, 16)  # DeferredDelete
    assert host.findChildren(_Ring) == []


def test_nothing_is_drawn_when_the_animations_are_off_or_it_is_hidden(
    monkeypatch,
) -> None:
    host, child = _host()

    monkeypatch.setattr(motion, "ENABLED", False)
    pulse(child, "#fff")
    monkeypatch.setattr(motion, "ENABLED", True)
    child.hide()
    pulse(child, "#fff")
    pulse(QWidget(), "#fff")  # no parent

    assert host.findChildren(_Ring) == []
