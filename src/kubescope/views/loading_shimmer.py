"""What a table shows while it has no rows: grey bars where the rows will be,
with a band of light that crosses them, while it loads, as a loading that makes
progress; and a line of text in the middle when it tried to load and stayed
empty.

It is a transparent widget over the viewport of the table, so nothing
else has to know. As soon as a row shows it draws nothing, and with the
animations off the bars stand still.
"""

from collections.abc import Callable

from PySide6.QtCore import QEvent, QObject, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPaintEvent,
)
from PySide6.QtWidgets import QTableWidget, QWidget

INTERVAL_MS = 33  # about thirty frames a second
CYCLE_MS = 1400  # the time the band takes to cross
BAND = 0.30  # the width of the band, as a part of the width of the table
BAR_HEIGHT = 12
BAR_ALPHA = 46
BAND_ALPHA = 120
MAX_ROWS = 10
SHARE = (0.78, 0.55, 0.86, 0.46, 0.68)  # how much of a column each bar fills
PADDING = 10


class LoadingShimmer(QWidget):
    def __init__(
        self,
        table: QTableWidget,
        accent: Callable[[], str],
        animated: Callable[[], bool] = lambda: True,
        bars: Callable[[], str] = lambda: "#8a919c",
        text: Callable[[], str] = lambda: "#7b8089",
    ) -> None:
        super().__init__(table.viewport())
        self._table = table
        self._accent = accent
        self._bars = bars
        self._text = text
        self._message = ""
        self._animated = animated
        self._elapsed = 0
        self._active = False
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self._timer = QTimer(self)
        self._timer.setInterval(INTERVAL_MS)
        self._timer.timeout.connect(self._tick)
        self._follow = _Follow(self)
        table.viewport().installEventFilter(self._follow)
        self.setGeometry(table.viewport().rect())
        self.hide()

    def set_active(self, active: bool) -> None:
        """Show the bars while the table loads, or take them away."""
        if active == self._active:
            return
        self._active = active
        if active:
            self._message = ""
            self._elapsed = 0
            if self._animated():
                self._timer.start()
        else:
            self._timer.stop()
        self._sync()

    def set_message(self, message: str) -> None:
        """Say in the middle of the table why it is empty; an empty text takes
        it away."""
        if self._active:
            return  # it is loading: the bars say it
        self._message = message
        self._sync()

    def _sync(self) -> None:
        if self._active or self._message:
            self.setGeometry(self.parentWidget().rect())  # type: ignore[union-attr]
            self.raise_()
            self.show()
            self.update()
        else:
            self.hide()

    def _shown_rows(self) -> int:
        table = self._table
        return sum(not table.isRowHidden(row) for row in range(table.rowCount()))

    def _tick(self) -> None:
        self._elapsed = (self._elapsed + INTERVAL_MS) % CYCLE_MS
        self.update()

    def _bar_paths(self) -> QPainterPath:
        """The grey bars, a few to a row, in the columns of the table."""
        table = self._table
        header = table.horizontalHeader()
        height = max(table.verticalHeader().defaultSectionSize(), BAR_HEIGHT + 8)
        rows = min(MAX_ROWS, max(self.height() // height, 1))
        path = QPainterPath()
        for row in range(rows):
            top = row * height + (height - BAR_HEIGHT) / 2
            for column in range(table.columnCount()):
                if table.isColumnHidden(column):
                    continue
                left = header.sectionViewportPosition(column) + PADDING
                room = header.sectionSize(column) - 2 * PADDING
                if room <= 0 or left > self.width():
                    continue
                width = room * SHARE[(row * 3 + column) % len(SHARE)]
                path.addRoundedRect(QRectF(left, top, width, BAR_HEIGHT), 6, 6)
        return path

    def paintEvent(self, event: QPaintEvent) -> None:
        if not self._active:
            if self._message and self._shown_rows() == 0:
                self._paint_message()
            return
        if self._table.rowCount() > 0:
            return  # the rows are here: nothing to wait for
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bars = self._bar_paths()
        grey = QColor(self._bars())
        grey.setAlpha(BAR_ALPHA)
        painter.fillPath(bars, grey)
        if not self._animated():
            return
        width = float(self.width())
        band = width * BAND
        head = -band + (width + band) * self._elapsed / CYCLE_MS
        accent = QColor(self._accent())
        clear, strong = QColor(accent), QColor(accent)
        clear.setAlpha(0)
        strong.setAlpha(BAND_ALPHA)
        gradient = QLinearGradient(head, 0, head + band, 0)
        gradient.setColorAt(0.0, clear)
        gradient.setColorAt(0.5, strong)
        gradient.setColorAt(1.0, clear)
        painter.setClipPath(bars)  # the light only shows on the bars
        painter.fillRect(QRectF(head, 0, band, self.height()), gradient)

    def _paint_message(self) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        font = QFont(painter.font())
        font.setPointSizeF(font.pointSizeF() + 1)
        painter.setFont(font)
        painter.setPen(QColor(self._text()))
        margin = 24
        area = QRectF(margin, 0, max(self.width() - 2 * margin, 1), self.height())
        painter.drawText(
            area,
            int(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap),
            self._message,
        )


class _Follow(QObject):
    """Keeps the bars the size of the viewport they cover."""

    def __init__(self, shimmer: LoadingShimmer) -> None:
        super().__init__(shimmer)
        self._shimmer = shimmer

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Resize and isinstance(watched, QWidget):
            self._shimmer.setGeometry(watched.rect())
        return False
