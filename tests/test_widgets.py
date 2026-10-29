import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from kubescope import theme
from kubescope.theme import themed
from kubescope.views import widgets
from kubescope.views.widgets import StatusBar, UsageChart

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
    track = themed(widgets.TRACK)  # the track of the theme in use, which may be gray
    assert _colors(bar, 0.1, 0.6) == [widgets.OK, track]

    bar.set_summary(ok=0, warning=0, bad=0, total=0)
    assert _colors(bar, 0.1, 0.9) == [track, track]


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


def test_usage_chart_keeps_the_last_samples_and_draws_them() -> None:
    chart = UsageChart("CPU", lambda value: f"{value:.1f}")
    chart.resize(300, chart.HEIGHT)
    empty = chart.grab().toImage()

    chart.add_sample(1.0)  # one point is no line yet
    for value in range(chart.MAX_SAMPLES + 5):
        chart.add_sample(float(value))

    assert len(chart.samples) == chart.MAX_SAMPLES
    assert chart.samples[-1] == chart.MAX_SAMPLES + 4
    assert chart.grab().toImage() != empty


def test_usage_chart_marks_the_samples_that_start_a_minute() -> None:
    from datetime import datetime

    chart = UsageChart("CPU", str)
    for second in (50, 55, 0, 5):
        chart.add_sample(1.0, datetime(2026, 10, 19, 18, 40 + (second < 10), second))

    assert chart.minute_marks() == [0, 2]


def test_usage_chart_shows_the_time_and_value_under_the_mouse() -> None:
    from PySide6.QtCore import QEvent, QPoint
    from PySide6.QtTest import QTest

    chart = UsageChart("CPU", str)
    chart.resize(400, chart.HEIGHT)
    chart.show()  # a hidden widget gets no mouse events
    assert chart.sample_at(300) is None  # nothing to point at yet
    for value in range(10):
        chart.add_sample(float(value))
    plot, _left, _step = chart._plot()
    assert chart.sample_at(plot.right()) == 9
    assert chart.sample_at(plot.left()) is None  # before the first sample

    def move(x: float) -> None:
        QTest.mouseMove(chart, QPoint(int(x), 60))

    plain = chart.grab().toImage()
    move(plot.right())
    assert chart._hover == 9
    assert chart.grab().toImage() != plain  # the cursor and its box
    move(plot.left())
    assert chart._hover is None
    move(plot.right())
    chart.leaveEvent(QEvent(QEvent.Type.Leave))
    assert chart._hover is None
    chart.close()


def test_line_number_editor_grows_its_gutter_and_paints_the_numbers() -> None:
    from kubescope.views.widgets import LineNumberEditor

    editor = LineNumberEditor()
    editor.resize(300, 120)
    editor.show()
    narrow = editor.gutter_width()
    editor.setPlainText("\n".join(f"line {n}" for n in range(1, 1200)))
    assert editor.gutter_width() > narrow  # four digits now
    assert editor._gutter.sizeHint().width() == editor.gutter_width()
    assert editor.viewportMargins().left() == editor.gutter_width()

    plain = editor._gutter.grab().toImage()
    editor.verticalScrollBar().setValue(500)  # scrolls the gutter with the text
    QApplication.processEvents()
    assert editor._gutter.grab().toImage() != plain
    editor.document().findBlockByNumber(502).setVisible(False)  # a hidden block
    editor.viewport().update()
    editor._gutter.repaint()

    theme.set_theme("light")
    editor._gutter.repaint()
    theme.set_theme("dark")
    editor.close()
