import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import time

import pytest
from PySide6.QtCore import QEvent, QPoint
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QWidget

from kubescope.views import motion

application = QApplication.instance() or QApplication([])


@pytest.fixture(autouse=True)
def moving(monkeypatch):
    monkeypatch.setattr(motion, "ENABLED", True)
    monkeypatch.setattr(motion, "DURATION_MS", 80)


def _wait(condition, seconds: float = 3.0) -> None:
    deadline = time.monotonic() + seconds
    while not condition() and time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.005)
    assert condition()


def test_a_widget_rises_into_its_place_and_is_left_as_it_was() -> None:
    widget = QLabel("list")
    widget.resize(200, 100)
    widget.show()

    motion.slide_up(widget)

    effect = widget.graphicsEffect()
    assert (
        isinstance(effect, motion.SlideUpEffect) and effect.property("progress") == 0.0
    )
    motion.slide_up(widget)  # already rising: left alone
    assert widget.graphicsEffect() is effect
    _wait(lambda: widget.graphicsEffect() is None)
    widget.close()


def test_the_effect_draws_the_widget_lower_and_fainter_until_it_arrives() -> None:
    widget = QLabel("list")
    widget.resize(120, 60)
    widget.show()
    effect = motion.SlideUpEffect(widget)
    widget.setGraphicsEffect(effect)

    assert effect.boundingRectFor(widget.rect().toRectF()).height() == (
        60 + motion.DISTANCE
    )
    for progress in (0.0, 0.5, 1.0):
        effect.setProperty("progress", progress)
        canvas = QPixmap(160, 120)
        canvas.fill()
        painter = QPainter(canvas)
        widget.render(painter, QPoint(0, 0))
        painter.end()
        assert not canvas.isNull()
    widget.close()


def test_nothing_moves_when_the_animations_are_off(monkeypatch) -> None:
    widget = QWidget()
    monkeypatch.setattr(motion, "ENABLED", False)
    motion.slide_up(widget)
    assert widget.graphicsEffect() is None

    monkeypatch.setattr(motion, "ENABLED", True)
    monkeypatch.setattr(motion, "DURATION_MS", 0)
    motion.slide_up(widget)
    assert widget.graphicsEffect() is None


def test_a_dialog_rises_when_it_opens_and_other_widgets_do_not() -> None:
    watcher = motion.DialogSlide()
    dialog, plain = QDialog(), QWidget()

    assert watcher.eventFilter(dialog, QEvent(QEvent.Type.Show)) is False
    assert isinstance(dialog.graphicsEffect(), motion.SlideUpEffect)
    watcher.eventFilter(plain, QEvent(QEvent.Type.Show))
    watcher.eventFilter(dialog, QEvent(QEvent.Type.Hide))
    assert plain.graphicsEffect() is None
    _wait(lambda: dialog.graphicsEffect() is None)
