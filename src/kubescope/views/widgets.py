"""Small custom widgets used by the Designer layouts."""

from collections.abc import Callable
from datetime import datetime

from PySide6.QtCore import QEvent, QObject, QPointF, QRect, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QPolygonF,
    QResizeEvent,
    QWheelEvent,
)
from PySide6.QtWidgets import QPlainTextEdit, QScrollArea, QSizePolicy, QWidget

from kubescope.theme import themed
from kubescope.utils.json_view import current_palette

TRACK = "#e8eaee"
OK = "#3d9a6d"
WARNING = "#e0a030"
BAD = "#d05560"


class TabScrollArea(QScrollArea):
    """Holds the tabs of the top bar: as wide as they are when there is room,
    and scrolled sideways, by the wheel, when there is not."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("pinnedScroll")
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setStyleSheet(
            "QScrollArea#pinnedScroll, QScrollArea#pinnedScroll > QWidget > QWidget"
            " { background: transparent; }"
        )

    def setWidget(self, widget: QWidget) -> None:
        super().setWidget(widget)
        widget.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """The tabs are laid out after they are added, and then they know how
        wide they are: ask the bar for that room."""
        if watched is self.widget() and event.type() == QEvent.Type.LayoutRequest:
            QTimer.singleShot(0, self.updateGeometry)  # once the tabs are polished
        return super().eventFilter(watched, event)

    def sizeHint(self) -> QSize:
        content = self.widget()
        return content.sizeHint() if content is not None else super().sizeHint()

    def minimumSizeHint(self) -> QSize:
        return QSize(120, self.sizeHint().height())

    def wheelEvent(self, event: QWheelEvent) -> None:
        bar = self.horizontalScrollBar()
        delta = event.angleDelta().y() or event.angleDelta().x()
        bar.setValue(bar.value() - delta)
        event.accept()


class StatusBar(QWidget):
    """A thin bar split into healthy, warning and failing parts of a total;
    what is left over (idle resources) stays as the empty track."""

    HEIGHT = 8

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._parts = (0, 0, 0)
        self._total = 0
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self.HEIGHT)

    def sizeHint(self) -> QSize:
        return QSize(200, self.HEIGHT)

    def set_summary(self, ok: int, warning: int, bad: int, total: int) -> None:
        self._parts = (ok, warning, bad)
        self._total = total
        self.update()

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        radius = self.HEIGHT / 2
        painter.setBrush(QColor(themed(TRACK)))
        painter.drawRoundedRect(QRectF(self.rect()), radius, radius)
        if self._total <= 0:
            return
        x = 0.0
        for count, color in zip(self._parts, (OK, WARNING, BAD), strict=True):
            width = self.width() * count / self._total
            if width > 0:
                painter.setBrush(QColor(themed(color)))
                painter.drawRoundedRect(
                    QRectF(x, 0, width, self.height()), radius, radius
                )
            x += width


class UsageChart(QWidget):
    """A small live chart: the last samples of one number as a filled line,
    with its title and latest value on top, value marks on the right and the
    time of every minute below."""

    HEIGHT = 150
    MAX_SAMPLES = 60
    GRID_LINES = 3
    LABEL_WIDTH = 64

    def __init__(
        self, title: str, formatter: Callable[[float], str], parent=None
    ) -> None:
        super().__init__(parent)
        self._title = title
        self._formatter = formatter
        self._samples: list[float] = []
        self._times: list[datetime] = []
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(self.HEIGHT)
        self.setMouseTracking(True)
        self._hover: int | None = None

    @property
    def samples(self) -> list[float]:
        return list(self._samples)

    def add_sample(self, value: float, when: datetime | None = None) -> None:
        self._samples = [*self._samples, value][-self.MAX_SAMPLES :]
        self._times = [*self._times, when or datetime.now()][-self.MAX_SAMPLES :]
        self.update()

    def _plot(self) -> tuple[QRectF, float, float]:
        """The plot area, the x of the first sample and the width of a step."""
        area = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        plot = area.adjusted(10, 30, -self.LABEL_WIDTH, -24)
        step = plot.width() / (self.MAX_SAMPLES - 1)
        return plot, plot.right() - step * (len(self._samples) - 1), step

    def sample_at(self, x: float) -> int | None:
        """The sample nearest to a horizontal position, None before the first
        one or without a line to point at."""
        if len(self._samples) < 2:
            return None
        _plot, left, step = self._plot()
        index = round((x - left) / step)
        return index if 0 <= index < len(self._samples) else None

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._hover = self.sample_at(event.position().x())
        self.update()

    def leaveEvent(self, _event: QEvent) -> None:
        self._hover = None
        self.update()

    def minute_marks(self) -> list[int]:
        """The samples that start a new minute: where a time mark goes."""
        return [
            index
            for index, time in enumerate(self._times)
            if index == 0 or time.minute != self._times[index - 1].minute
        ]

    def paintEvent(self, _event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        area = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        painter.setPen(QColor(themed("#e1e3e9")))
        painter.setBrush(QColor(themed("#f3f4f7")))
        painter.drawRoundedRect(area, 5, 5)
        header = area.adjusted(10, 6, -10, 0)
        painter.setPen(QColor(themed("#4f5966", text=True)))
        painter.drawText(
            header, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, self._title
        )
        painter.setPen(QColor(themed("#20232a", text=True)))
        latest = self._formatter(self._samples[-1]) if self._samples else "-"
        painter.drawText(
            header, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, latest
        )
        if len(self._samples) < 2:
            return
        plot, left, step = self._plot()
        top = max(max(self._samples), 1e-9)
        grid = QColor(themed("#e1e3e9"))
        muted = QColor(themed("#6b7380", text=True))
        for line in range(self.GRID_LINES + 1):
            y = plot.bottom() - plot.height() * line / self.GRID_LINES
            painter.setPen(QPen(grid, 1))
            painter.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))
            painter.setPen(muted)
            painter.drawText(
                QRectF(plot.right() + 6, y - 8, self.LABEL_WIDTH - 12, 16),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                self._formatter(top * line / self.GRID_LINES),
            )
        for index in self.minute_marks():
            x = left + index * step
            painter.setPen(QPen(grid, 1, Qt.PenStyle.DotLine))
            painter.drawLine(QPointF(x, plot.top()), QPointF(x, plot.bottom()))
            text = f"{self._times[index]:%H:%M}"
            width = painter.fontMetrics().horizontalAdvance(text)
            painter.setPen(muted)
            painter.drawText(
                QPointF(
                    min(max(x - width / 2, plot.left()), plot.right() - width),
                    area.bottom() - 6,
                ),
                text,
            )
        points = [
            QPointF(left + index * step, plot.bottom() - plot.height() * v / top)
            for index, v in enumerate(self._samples)
        ]
        accent = QColor(themed("#3220a0"))
        faded = QColor(accent)
        faded.setAlpha(50)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(faded)
        painter.drawPolygon(
            QPolygonF(
                [QPointF(points[0].x(), plot.bottom()), *points]
                + [QPointF(points[-1].x(), plot.bottom())]
            )
        )
        painter.setPen(QPen(accent, 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPolyline(QPolygonF(points))
        if self._hover is not None:
            self._paint_hover(painter, area, points[self._hover], self._hover, plot)

    def _paint_hover(
        self, painter: QPainter, area: QRectF, point: QPointF, index: int, plot: QRectF
    ) -> None:
        """A cursor line on the sample under the mouse, with its time and value
        in a box."""
        accent = QColor(themed("#3220a0"))
        painter.setPen(QPen(accent, 1))
        painter.drawLine(
            QPointF(point.x(), plot.top()), QPointF(point.x(), plot.bottom())
        )
        painter.setBrush(accent)
        painter.drawEllipse(point, 3.5, 3.5)
        text = (
            f"{self._times[index]:%H:%M:%S}   {self._formatter(self._samples[index])}"
        )
        metrics = painter.fontMetrics()
        box = QRectF(0, 0, metrics.horizontalAdvance(text) + 16, metrics.height() + 8)
        box.moveTo(
            min(
                max(point.x() - box.width() / 2, area.left() + 4),
                area.right() - box.width() - 4,
            ),
            plot.top() + 2,
        )
        painter.setPen(QColor(themed("#e1e3e9")))
        painter.setBrush(QColor(themed("#ffffff")))
        painter.drawRoundedRect(box, 4, 4)
        painter.setPen(QColor(themed("#20232a", text=True)))
        painter.drawText(box, Qt.AlignmentFlag.AlignCenter, text)


class _LineNumbers(QWidget):
    def __init__(self, editor: "LineNumberEditor") -> None:
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self._editor.gutter_width(), 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        self._editor.paint_gutter(event)


class LineNumberEditor(QPlainTextEdit):
    """A plain text editor with the line numbers of VS Code in a gutter."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._gutter = _LineNumbers(self)
        self.blockCountChanged.connect(self._update_margin)
        self.updateRequest.connect(self._scroll_gutter)
        self._update_margin()

    def gutter_width(self) -> int:
        digits = len(str(max(1, self.blockCount())))
        return 20 + self.fontMetrics().horizontalAdvance("9") * max(digits, 2)

    def _update_margin(self, _count: int = 0) -> None:
        self.setViewportMargins(self.gutter_width(), 0, 0, 0)

    def _scroll_gutter(self, rect: QRect, dy: int) -> None:
        if dy:
            self._gutter.scroll(0, dy)
        else:
            self._gutter.update(0, rect.y(), self._gutter.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_margin()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        area = self.contentsRect()
        self._gutter.setGeometry(
            QRect(area.left(), area.top(), self.gutter_width(), area.height())
        )

    def paint_gutter(self, event: QPaintEvent) -> None:
        palette = current_palette()
        painter = QPainter(self._gutter)
        painter.fillRect(event.rect(), QColor(palette.background))
        dimmed = QColor(palette.text)
        dimmed.setAlpha(120)
        painter.setPen(dimmed)
        block = self.firstVisibleBlock()
        top = round(
            self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        )
        while block.isValid() and top <= event.rect().bottom():
            height = round(self.blockBoundingRect(block).height())
            if block.isVisible() and top + height >= event.rect().top():
                painter.drawText(
                    0,
                    top,
                    self._gutter.width() - 10,
                    height,
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                    str(block.blockNumber() + 1),
                )
            block = block.next()
            top += height
