"""A soft band over the row of a table that the cursor is on.

One filter for the whole application, so the tables of the extensions
have it too. The band is a child of the table's viewport that lets every
click through, so the table, its selection and its delegates are not
touched.
"""

from PySide6.QtCore import QEvent, QObject, QPoint, Qt
from PySide6.QtGui import QColor, QMouseEvent, QPainter
from PySide6.QtWidgets import QApplication, QTableView, QWidget

from kubescope.theme import themed

ALPHA = 28  # of 255: a hint of the accent over the row


class _Band(QWidget):
    def __init__(self, viewport: QWidget) -> None:
        super().__init__(viewport)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()

    def paintEvent(self, _event: object) -> None:
        color = QColor(themed("#3220a0"))
        color.setAlpha(ALPHA)
        QPainter(self).fillRect(self.rect(), color)


class RowHover(QObject):
    """Follows the cursor over the tables and puts the band on its row."""

    def __init__(self) -> None:
        super().__init__()
        self._bands: dict[QWidget, _Band] = {}

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        kind = event.type()
        if kind == QEvent.Type.Show and isinstance(watched, QTableView):
            self._attach(watched)
        elif isinstance(watched, QWidget) and (band := self._bands.get(watched)):
            table = watched.parentWidget()
            if kind == QEvent.Type.MouseMove and isinstance(table, QTableView):
                assert isinstance(event, QMouseEvent)
                self._follow(table, band, event.position().toPoint())
            elif kind in (QEvent.Type.Leave, QEvent.Type.Hide):
                band.hide()
        return False

    def _attach(self, table: QTableView) -> None:
        viewport = table.viewport()
        if viewport is None or viewport in self._bands:
            return
        band = _Band(viewport)
        self._bands[viewport] = band
        viewport.setMouseTracking(True)
        viewport.installEventFilter(self)
        viewport.destroyed.connect(
            lambda _=None, key=viewport: self._bands.pop(key, None)
        )
        table.verticalScrollBar().valueChanged.connect(lambda _value: band.hide())

    @staticmethod
    def _follow(table: QTableView, band: _Band, at: QPoint) -> None:
        row = table.rowAt(at.y())
        if row < 0:
            band.hide()
            return
        band.setGeometry(
            0,
            table.rowViewportPosition(row),
            table.viewport().width(),
            table.rowHeight(row),
        )
        band.show()
        band.raise_()


_hover: list[RowHover] = []  # kept as long as the application lives


def install_row_hover(application: QApplication) -> None:
    hover = RowHover()
    _hover.append(hover)
    application.installEventFilter(hover)
