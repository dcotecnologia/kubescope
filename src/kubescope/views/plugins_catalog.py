"""The Catalog of the Plugins menu: the Helm charts of Artifact Hub as cards.

Each card names the chart, its version and repository, and has Learn
More (its page on Artifact Hub) and Install. Install runs nothing: as
with a Forward, it shows the `helm` commands for you to copy and run
yourself.
"""

import logging

from PySide6.QtCore import QEvent, QObject, Qt, QThread, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope.ui.ui_plugins_page import Ui_PluginsPage
from kubescope.utils.artifacthub import (
    CatalogError,
    Chart,
    Results,
    fetch_logo,
    search_charts,
)

logger = logging.getLogger(__name__)

COLUMNS = 3  # until the page has a width
CARD_WIDTH = 300  # pixels a card needs at least
GAP = 14
LOGO = 56  # pixels of a logo


class SearchWorker(QThread):
    """Asks Artifact Hub off the UI thread."""

    found = Signal(str, int, object)  # the text searched, the offset, the results
    failed = Signal(str, str)

    def __init__(
        self, query: str, offset: int = 0, parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self.query = query
        self.offset = offset

    def run(self) -> None:
        try:
            results = search_charts(self.query, self.offset)
        except CatalogError as error:
            self.failed.emit(self.query, str(error))
        except Exception as error:  # never let a thread die silently
            logger.exception("Catalog search failed")
            self.failed.emit(self.query, str(error))
        else:
            self.found.emit(self.query, self.offset, results)


class LogoWorker(QThread):
    """Reads the logos of the charts shown, one by one, off the UI thread."""

    logo = Signal(str, bytes)  # the id of the logo, its image

    def __init__(self, ids: list[str], parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.ids = ids

    def run(self) -> None:
        for logo_id in self.ids:
            if self.isInterruptionRequested():
                return
            data = fetch_logo(logo_id)
            if data:
                self.logo.emit(logo_id, data)


class InstallDialog(QDialog):
    """The commands that install a chart, to copy and run in your terminal."""

    def __init__(self, parent: QWidget | None, chart: Chart) -> None:
        super().__init__(parent)
        self.setWindowTitle(self.tr("Install {name}").format(name=chart.name))
        self.setMinimumWidth(620)
        layout = QVBoxLayout(self)
        note = QLabel(
            self.tr(
                "KubeScope does not install charts. Copy these commands and run "
                "them in your terminal, with the context you want."
            )
        )
        note.setWordWrap(True)
        layout.addWidget(note)
        box = QPlainTextEdit(chart.command)
        box.setReadOnly(True)
        box.setMinimumHeight(110)
        layout.addWidget(box)
        row = QHBoxLayout()
        row.addStretch(1)
        copy = QPushButton(self.tr("Copy"))
        copy.clicked.connect(lambda: QApplication.clipboard().setText(chart.command))
        copy.setProperty("variant", "primary")
        close = QPushButton(self.tr("Close"))
        close.setProperty("variant", "secondary")
        close.clicked.connect(self.accept)
        row.addWidget(copy)
        row.addWidget(close)
        layout.addLayout(row)


class PluginsCatalog(QObject):
    """Drives the catalog page: searches, draws the cards, opens their
    links."""

    def __init__(self, ui: Ui_PluginsPage, host: QWidget) -> None:
        super().__init__(host)
        self.ui = ui
        self.host = host
        self.charts: list[Chart] | None = None
        self._worker: SearchWorker | None = None
        self._asked = ""
        self.total = 0
        self._columns = COLUMNS
        self._logos: LogoWorker | None = None
        self._logo_labels: dict[str, list[QLabel]] = {}
        self._pixmaps: dict[str, QPixmap] = {}  # kept, so a redraw keeps the logos
        ui.searchButton.clicked.connect(self.search)
        ui.searchInput.returnPressed.connect(self.search)
        ui.cardsScroll.viewport().installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """More cards side by side when the window gives room for them."""
        if event.type() == QEvent.Type.Resize and self.charts:
            columns = self._fit_columns()
            if columns != self._columns:
                self.render()
        return False

    def _fit_columns(self) -> int:
        width = self.ui.cardsScroll.viewport().width()
        return max(1, (width + GAP) // (CARD_WIDTH + GAP))

    def ensure(self) -> None:
        """Load the first page the first time the catalog opens."""
        if self.charts is None and self._worker is None:
            self.search()

    def search(self) -> None:
        self._asked = self.ui.searchInput.text().strip()
        self.total = 0
        self.charts = None
        self._ask(0)

    def load_more(self) -> None:
        self._ask(len(self.charts or []))

    def _ask(self, offset: int) -> None:
        self.ui.statusLabel.setText(self.tr("Searching Artifact Hub..."))
        worker = SearchWorker(self._asked, offset, self)
        worker.found.connect(self._found)
        worker.failed.connect(self._failed)
        worker.finished.connect(lambda worker=worker: self._finished(worker))
        self._worker = worker
        worker.start()

    def _finished(self, worker: SearchWorker) -> None:
        if self._worker is worker:
            self._worker = None

    def _found(self, query: str, offset: int, results: Results) -> None:
        if query != self._asked:  # the person searched for something else since
            return
        if offset == 0:
            self.charts = []
        elif offset != len(self.charts or []):  # an answer to an earlier ask
            return
        self.charts = [*(self.charts or []), *results.charts]
        self.total = results.total
        self.ui.statusLabel.setText(
            self.tr("{shown} of {total} charts").format(
                shown=len(self.charts), total=self.total
            )
            if self.charts
            else self.tr("No chart matches that search")
        )
        self.render()
        self._load_logos()

    def _load_logos(self) -> None:
        if self._logos is not None:  # the logos of the earlier search are not wanted
            self._logos.requestInterruption()
            self._logos.logo.disconnect()
            self._logos = None
        ids = [
            chart.logo_id
            for chart in self.charts or []
            if chart.logo_id and chart.logo_id not in self._pixmaps
        ]
        worker = LogoWorker(list(dict.fromkeys(ids)), self)
        worker.logo.connect(self._logo)
        worker.finished.connect(lambda worker=worker: self._logos_done(worker))
        self._logos = worker
        worker.start()

    def _logos_done(self, worker: LogoWorker) -> None:
        if self._logos is worker:
            self._logos = None

    def _logo(self, logo_id: str, data: bytes) -> None:
        pixmap = QPixmap()
        if not pixmap.loadFromData(data):  # a format Qt cannot draw: no logo
            return
        pixmap = pixmap.scaled(
            LOGO,
            LOGO,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._pixmaps[logo_id] = pixmap
        for label in self._logo_labels.get(logo_id, []):
            label.setPixmap(pixmap)

    def _failed(self, query: str, message: str) -> None:
        if query != self._asked:
            return
        self.ui.statusLabel.setText(
            self.tr("Could not reach Artifact Hub: {error}").format(error=message)
        )

    def render(self) -> None:
        grid = self.ui.cardsGrid
        self._logo_labels = {}
        while (item := grid.takeAt(0)) is not None:
            if widget := item.widget():
                widget.deleteLater()
        columns = self._columns = self._fit_columns()
        charts = self.charts or []
        for index, chart in enumerate(charts):
            grid.addWidget(self._card(chart), index // columns, index % columns)
        for column in range(columns):
            grid.setColumnStretch(column, 1)
        rows = (len(charts) + columns - 1) // columns
        if charts and len(charts) < self.total:
            more = QPushButton(self.tr("Load more"))
            more.setProperty("variant", "secondary")
            more.clicked.connect(self.load_more)
            grid.addWidget(more, rows, 0, 1, columns, Qt.AlignmentFlag.AlignCenter)
            rows += 1
        grid.setRowStretch(rows, 1)

    def _card(self, chart: Chart) -> QFrame:
        card = QFrame()
        card.setObjectName("pluginCard")
        card.setProperty("card", "true")  # the look of the app's other cards
        card.setMinimumHeight(190)
        layout = QVBoxLayout(card)
        top = QHBoxLayout()
        logo = QLabel()
        logo.setFixedSize(LOGO, LOGO)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if chart.logo_id:
            self._logo_labels.setdefault(chart.logo_id, []).append(logo)
            if chart.logo_id in self._pixmaps:
                logo.setPixmap(self._pixmaps[chart.logo_id])
        top.addWidget(logo)
        top.addStretch(1)
        for mark, text in (
            (chart.cncf, self.tr("CNCF")),
            (chart.official, self.tr("Official")),
            (chart.verified, self.tr("Verified publisher")),
        ):
            if mark:
                badge = QLabel("\u2605" if text == self.tr("Official") else "\u2713")
                badge.setToolTip(text)
                badge.setStyleSheet("font-weight: 700;")
                if text == self.tr("CNCF"):
                    badge.setText("CNCF")
                top.addWidget(badge)
        layout.addLayout(top)
        title = QLabel(chart.name)
        title.setObjectName("pluginCardTitle")
        title.setStyleSheet("font-size: 16px; font-weight: 700;")
        title.setWordWrap(True)
        layout.addWidget(title)
        meta = QHBoxLayout()
        meta.addWidget(QLabel(f"v{chart.version}" if chart.version else ""))
        meta.addStretch(1)
        repository = QLabel(chart.repository)
        repository.setAlignment(Qt.AlignmentFlag.AlignRight)
        meta.addWidget(repository)
        layout.addLayout(meta)
        description = QLabel(chart.description)
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(description, 1)
        buttons = QHBoxLayout()
        install = QPushButton(self.tr("Install"))
        install.clicked.connect(lambda _c=False, chart=chart: self.install(chart))
        learn = QPushButton(self.tr("Learn More"))
        install.setProperty("variant", "primary")
        learn.setProperty("variant", "link")
        learn.setCursor(Qt.CursorShape.PointingHandCursor)
        learn.clicked.connect(lambda _c=False, chart=chart: self.learn_more(chart))
        buttons.addWidget(install)
        buttons.addStretch(1)
        buttons.addWidget(learn)
        layout.addLayout(buttons)
        return card

    def install(self, chart: Chart) -> None:
        InstallDialog(self.host, chart).exec()

    @staticmethod
    def learn_more(chart: Chart) -> None:
        QDesktopServices.openUrl(QUrl(chart.link))
