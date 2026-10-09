import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from kubescope import theme, widgets
from kubescope.theme import themed
from kubescope.widgets import StatusBar

application = QApplication.instance() or QApplication([])


def _colors(bar: StatusBar, *fractions: float) -> list[str]:
    image = bar.grab().toImage()
    y = image.height() // 2
    return [
        image.pixelColor(int(image.width() * fraction), y).name()
        for fraction in fractions
    ]


def _bar() -> StatusBar:
    bar = StatusBar()
    bar.resize(400, bar.HEIGHT)
    return bar


def test_status_bar_splits_the_width_by_health() -> None:
    bar = _bar()

    bar.set_summary(ok=2, warning=1, bad=1, total=4)

    assert _colors(bar, 0.25, 0.62, 0.87) == [widgets.OK, widgets.WARNING, widgets.BAD]


def test_idle_resources_and_empty_totals_leave_the_track_empty() -> None:
    bar = _bar()

    bar.set_summary(ok=1, warning=0, bad=0, total=4)  # three idle of four
    assert _colors(bar, 0.1, 0.6) == [widgets.OK, widgets.TRACK]

    bar.set_summary(ok=0, warning=0, bad=0, total=0)
    assert _colors(bar, 0.1, 0.9) == [widgets.TRACK, widgets.TRACK]


def test_status_bar_is_thin_and_stretches_sideways() -> None:
    bar = StatusBar()

    assert bar.height() == StatusBar.HEIGHT == bar.sizeHint().height()
    assert bar.sizeHint().width() > 0


def test_status_bar_follows_the_theme() -> None:
    bar = _bar()
    bar.set_summary(ok=1, warning=0, bad=0, total=2)

    theme.set_theme("dark")

    assert _colors(bar, 0.25, 0.75) == [themed(widgets.OK), themed(widgets.TRACK)]
    assert themed(widgets.OK) != widgets.OK
