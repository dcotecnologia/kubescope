import json
import logging
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from PySide6.QtCore import (
    QCoreApplication,
    QEvent,
    QPointF,
    QRectF,
    QSize,
    Qt,
    QThread,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QCloseEvent,
    QColor,
    QFontDatabase,
    QIcon,
    QPainter,
    QPen,
    QPixmap,
    QPolygonF,
)
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHeaderView,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QStyle,
    QTableWidgetItem,
    QWidget,
)

from kubescope.cluster import (
    KubectlError,
    get_cluster_overview,
    get_pod_logs,
    get_resource_details,
    get_workload_pods,
    get_workloads,
    list_contexts,
)
from kubescope.i18n import apply_language
from kubescope.log_tab import LOG_REFRESH_MS, LogTab
from kubescope.models import (
    ClusterOverview,
    PodInfo,
    Workload,
    format_bytes,
    format_cores,
    workload_sort_key,
)
from kubescope.settings import Settings
from kubescope.ui.ui_main_window import Ui_MainWindow
from kubescope.ui.ui_overview_page import Ui_OverviewPage
from kubescope.ui.ui_pods_dialog import Ui_PodsDialog
from kubescope.ui.ui_settings_page import Ui_SettingsPage
from kubescope.ui.ui_viewer_page import Ui_ViewerPage

logger = logging.getLogger(__name__)


def _icon_path(name: str, draw: Callable[[QPainter], None], size: QSize) -> str:
    """Render a small PNG once; Qt style sheets cannot draw shapes themselves."""
    path = Path(tempfile.gettempdir()) / f"kubescope-{name}.png"
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    draw(painter)
    painter.end()
    pixmap.save(str(path), "PNG")
    return path.as_posix()


def _chevron_icon_path(color: str = "#6b7380", name: str = "chevron-down") -> str:
    def draw(painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        painter.drawPolygon(QPolygonF([QPointF(0, 0), QPointF(10, 0), QPointF(5, 6)]))

    return _icon_path(name, draw, QSize(10, 6))


def _sort_icon_path(up: bool) -> str:
    def draw(painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#3220a0"))
        points = [QPointF(0, 6), QPointF(9, 6), QPointF(4.5, 0)]
        if not up:
            points = [QPointF(0, 0), QPointF(9, 0), QPointF(4.5, 6)]
        painter.drawPolygon(QPolygonF(points))

    return _icon_path("sort-up" if up else "sort-down", draw, QSize(9, 6))


def _close_icon_path(color: str, name: str) -> str:
    def draw(painter: QPainter) -> None:
        pen = QPen(QColor(color), 1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(QPointF(1.5, 1.5), QPointF(8.5, 8.5))
        painter.drawLine(QPointF(8.5, 1.5), QPointF(1.5, 8.5))

    return _icon_path(name, draw, QSize(10, 10))


def _spinner_icon(angle: int, color: str) -> QIcon:
    """Draw one frame of the loading spinner; the disabled state keeps its color."""
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color), 2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.drawArc(QRectF(2, 2, 12, 12), -angle * 16, 270 * 16)
    painter.end()
    icon = QIcon()
    icon.addPixmap(pixmap, QIcon.Mode.Normal)
    icon.addPixmap(pixmap, QIcon.Mode.Disabled)
    return icon


class RefreshWorker(QThread):
    completed = Signal(list, list)
    failed = Signal(str)

    def __init__(self, context: str, namespace: str | None) -> None:
        super().__init__()
        self.context = context
        self.namespace = namespace

    def run(self) -> None:
        try:
            namespaces, workloads = get_workloads(self.context, self.namespace)
        except Exception as error:
            logger.exception("Could not load workloads from context %s", self.context)
            self.failed.emit(str(error))
            return
        self.completed.emit(namespaces, workloads)


class ActionWorker(QThread):
    completed = Signal(object)
    failed = Signal(str)

    def __init__(
        self,
        operation: Callable[..., Any],
        arguments: tuple[Any, ...],
    ) -> None:
        super().__init__()
        self.operation = operation
        self.arguments = arguments

    def run(self) -> None:
        try:
            result = self.operation(*self.arguments)
        except Exception as error:
            logger.exception("Kubernetes detail action failed")
            self.failed.emit(str(error))
            return
        self.completed.emit(result)


class WorkloadWindow(QMainWindow):
    def __init__(self, settings: Settings | None = None) -> None:
        super().__init__()
        self.settings = settings or Settings()
        self.setMinimumSize(980, 640)
        self._contexts: list[str] = []
        self._namespaces: list[str] = []
        self._sort: tuple[int, Qt.SortOrder] | None = None
        self._overview: ClusterOverview | None = None
        self._status_message: Callable[[], str] | None = None
        self._worker: RefreshWorker | None = None
        self._action_workers: list[ActionWorker] = []
        self._close_when_worker_stops = False
        self._workloads: list[Workload] = []
        self._build_ui()
        self._load_contexts()

    def _build_ui(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ui = self.ui
        self.context_combo = ui.contextCombo
        self.namespace_combo = ui.namespaceCombo
        self.search_input = ui.searchInput
        self.refresh_button = ui.refreshButton
        self.summary_label = ui.summaryLabel
        self.pods_button = ui.podsButton
        self.details_button = ui.detailsButton
        self.logs_button = ui.logsButton
        self.table = ui.workloadTable
        self.status_label = ui.statusLabel
        self.pages = ui.pages
        self.nav_overview = ui.navOverview
        self.nav_workloads = ui.navWorkloads

        self.overview_ui = Ui_OverviewPage()
        self.overview_ui.setupUi(ui.overviewHost)
        self.overview_refresh_button = self.overview_ui.overviewRefreshButton
        self.nodes_table = self.overview_ui.nodesTable
        self.viewer_ui = Ui_ViewerPage()
        self.viewer_ui.setupUi(ui.viewerHost)
        self.viewer_tabs = self.viewer_ui.viewerTabs
        while self.viewer_tabs.count():  # drop the sample tab used in Designer
            sample = self.viewer_tabs.widget(0)
            self.viewer_tabs.removeTab(0)
            sample.deleteLater()
        self.viewer_tabs.tabCloseRequested.connect(self._close_viewer_tab)
        self.nav_viewer = ui.navViewer
        self.settings_ui = Ui_SettingsPage()
        self.settings_ui.setupUi(ui.settingsHost)
        self.settings_ui.contextsTable.setRowCount(0)
        self.settings_ui.saveButton.clicked.connect(self._save_preferences)
        self._overview_context: str | None = None
        self._overview_busy = False

        style = self.style()
        self.nav_overview.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        self.nav_workloads.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        )
        self.overview_refresh_button.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        )
        self.refresh_button.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        )
        self.pods_button.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        )
        self.details_button.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        )
        self.logs_button.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )
        # The .ui files carry sample data for Qt Designer; the app starts empty.
        self.context_combo.clear()
        self.namespace_combo.clear()
        self.table.setRowCount(0)
        self.summary_label.setText(self.tr("0 workloads"))
        self.nodes_table.setRowCount(0)
        self._reset_overview()
        self.nodes_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        for column, width in (
            (1, 100),
            (2, 80),
            (3, 105),
            (4, 90),
            (5, 140),
            (6, 70),
            (7, 60),
        ):
            self.nodes_table.setColumnWidth(column, width)
        self.namespace_combo.addItem(self.tr("All namespaces"), "")
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self._sort_workloads)
        for column, width in ((0, 160), (1, 150), (3, 110), (4, 150), (5, 90)):
            self.table.setColumnWidth(column, width)
        self.setStyleSheet(
            self.styleSheet()
            .replace("SORT_UP", _sort_icon_path(up=True))
            .replace("SORT_DOWN", _sort_icon_path(up=False))
            .replace("CHEVRON_LIGHT", _chevron_icon_path("#b8c7dc", "chevron-light"))
            .replace("CHEVRON", _chevron_icon_path())
            .replace("CLOSE_ICON_HOVER", _close_icon_path("#3220a0", "close-hover"))
            .replace("CLOSE_ICON", _close_icon_path("#6b7380", "close"))
        )

        self._loading = 0
        self._spinner_angle = 0
        self._spinner_button: QPushButton | None = None
        self._spinner_saved: tuple[QIcon, str] | None = None
        self._spinner_timer = QTimer(self)
        self._spinner_timer.setInterval(70)
        self._spinner_timer.timeout.connect(self._tick_spinner)

        self.refresh_button.clicked.connect(self.refresh)
        self.pods_button.clicked.connect(self._view_workload_pods)
        self.details_button.clicked.connect(self._view_workload_details)
        self.logs_button.clicked.connect(self._view_workload_logs)
        self.table.itemSelectionChanged.connect(self._update_workload_actions)
        self.table.cellDoubleClicked.connect(
            lambda _row, _column: self._view_workload_details()
        )
        self.nav_viewer.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        )
        self.nav_viewer.clicked.connect(lambda: self._show_page(3))
        ui.settingsButton.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )
        ui.settingsButton.clicked.connect(lambda: self._show_page(2))
        self.nav_overview.clicked.connect(lambda: self._show_page(0))
        self.nav_workloads.clicked.connect(lambda: self._show_page(1))
        self.overview_refresh_button.clicked.connect(self.refresh_overview)
        self.context_combo.currentTextChanged.connect(self._context_changed)
        self.context_combo.currentTextChanged.connect(self.refresh)
        self.namespace_combo.currentIndexChanged.connect(self.refresh)
        self.search_input.textChanged.connect(self._filter_rows)

    def _load_contexts(self) -> None:
        try:
            contexts, active_context = list_contexts()
        except KubectlError as error:
            reason = str(error)
            self._set_status(
                lambda: self.tr("Could not load kubeconfig: {error}").format(
                    error=reason
                )
            )
            self.context_combo.setEnabled(False)
            self.namespace_combo.setEnabled(False)
            self.refresh_button.setEnabled(False)
            return

        self._contexts = contexts
        remembered = self.settings.last_context
        if self.settings.remember_last_context and remembered in contexts:
            selected = remembered
        else:
            selected = active_context
        self._fill_contexts(selected)
        if not contexts:
            self._set_status(lambda: self.tr("No contexts found in kubeconfig"))
            self.refresh_button.setEnabled(False)
            return
        self.refresh()
        self._ensure_overview()

    def _fill_contexts(self, selected: str | None) -> None:
        """Show contexts under their custom names while keeping the real name."""
        self.context_combo.blockSignals(True)
        self.context_combo.clear()
        for context in self._contexts:
            self.context_combo.addItem(self.settings.display_name(context), context)
            if self.settings.display_name(context) != context:
                self.context_combo.setItemData(
                    self.context_combo.count() - 1,
                    context,
                    Qt.ItemDataRole.ToolTipRole,
                )
        index = self.context_combo.findData(selected)
        self.context_combo.setCurrentIndex(max(index, 0))
        self.context_combo.blockSignals(False)
        # the closed box is narrow, but the list must show whole names
        metrics = self.context_combo.fontMetrics()
        widest = (
            max(
                (metrics.horizontalAdvance(self.context_combo.itemText(i)) + 48)
                for i in range(self.context_combo.count())
            )
            if self.context_combo.count()
            else 0
        )
        self.context_combo.view().setMinimumWidth(widest)

    def _context(self) -> str:
        """Real kubeconfig context name, whatever the combo displays."""
        return self.context_combo.currentData() or self.context_combo.currentText()

    def _set_status(self, message: Callable[[], str]) -> None:
        self._status_message = message
        self.status_label.setText(message())

    def _show_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        self.nav_overview.setChecked(index == 0)
        self.nav_workloads.setChecked(index == 1)
        self.ui.settingsButton.setChecked(index == 2)
        self.nav_viewer.setChecked(index == 3)
        self._apply_page_titles()
        if index == 0:
            self._ensure_overview()
        elif index == 2:
            self._load_settings_form()

    def _apply_page_titles(self) -> None:
        if self.pages.currentIndex() == 0:
            self.ui.pageTitle.setText(self.tr("Overview"))
            self.ui.pageSubtitle.setText(self.tr("Cluster resources and capacity"))
        elif self.pages.currentIndex() == 3:
            self.ui.pageTitle.setText(self.tr("Details & Logs"))
            self.ui.pageSubtitle.setText(
                self.tr("Resource details and Pod logs, one tab each")
            )
        elif self.pages.currentIndex() == 2:
            self.ui.pageTitle.setText(self.tr("Settings"))
            self.ui.pageSubtitle.setText(self.tr("Preferences and context names"))
        else:
            self.ui.pageTitle.setText(self.tr("Workloads"))
            self.ui.pageSubtitle.setText(
                self.tr("Deployments, StatefulSets and DaemonSets of the cluster")
            )

    def _context_changed(self, *_args: object) -> None:
        self._overview_context = None
        if self.settings.remember_last_context and self._contexts:
            self.settings.last_context = self._context()
            self._save_settings()
        if self.pages.currentIndex() == 0:
            self._ensure_overview()

    def _ensure_overview(self) -> None:
        context = self._context()
        if context and context != self._overview_context:
            self.refresh_overview()

    def refresh_overview(self, *_args: object) -> None:
        context = self._context()
        if not context or self._overview_busy:
            return
        self._overview_busy = True
        self.overview_ui.noticeLabel.setText(self.tr("Loading cluster data..."))
        self._run_action(
            get_cluster_overview,
            lambda result: self._show_overview(context, result),
            context,
            on_error=self._show_overview_error,
        )

    def _show_overview_error(self, message: str) -> None:
        self._overview_busy = False
        self.overview_ui.noticeLabel.setText(
            self.tr("Could not load the overview: {message}").format(message=message)
        )

    def _reset_overview(self) -> None:
        overview = self.overview_ui
        for name in ("nodes", "pods", "cpu", "mem"):
            getattr(overview, f"{name}Value").setText("—")
            getattr(overview, f"{name}Caption").setText("")
        for name in ("namespaces", "deployments", "statefulsets", "daemonsets"):
            getattr(overview, f"{name}Value").setText("—")
            getattr(overview, f"{name}Caption").setText("")
        for bar in (overview.podsBar, overview.cpuBar, overview.memBar):
            self._set_bar(bar, 0)
        overview.noticeLabel.setText("")

    @staticmethod
    def _set_bar(bar: QProgressBar, percent: float) -> None:
        percent = max(0, min(100, round(percent)))
        bar.setValue(percent)
        level = "high" if percent >= 90 else "warn" if percent >= 75 else ""
        bar.setProperty("level", level)
        bar.style().unpolish(bar)
        bar.style().polish(bar)

    @staticmethod
    def _ratio(part: float, whole: float) -> float:
        return part / whole * 100 if whole else 0

    def _show_overview(self, context: str, overview: ClusterOverview) -> None:
        self._overview_busy = False
        if context != self._context():
            self._overview_context = None
            self.refresh_overview()
            return
        self._overview_context = context
        self._overview = overview
        self._render_overview(overview)

    def _render_overview(self, overview: ClusterOverview) -> None:
        translate = QCoreApplication.translate
        page = self.overview_ui
        page.nodesValue.setText(f"{overview.nodes_ready} / {len(overview.nodes)}")
        page.nodesCaption.setText(translate("OverviewPage", "nodes ready"))
        if overview.pods_total is None:
            page.podsValue.setText("—")
            page.podsCaption.setText("")
        else:
            page.podsValue.setText(
                f"{overview.pods_running} / {overview.pods_capacity}"
            )
            page.podsCaption.setText(
                self.tr("running · {pending} pending · {failed} failed").format(
                    pending=overview.pods_pending, failed=overview.pods_failed
                )
            )
        running = overview.pods_running or 0
        self._set_bar(page.podsBar, self._ratio(running, overview.pods_capacity))

        cpu_text = translate("OverviewPage", "cores requested / allocatable")
        if overview.cpu_usage is not None:
            cpu_text += self.tr(" · usage {value}").format(
                value=format_cores(overview.cpu_usage)
            )
        page.cpuValue.setText(
            f"{format_cores(overview.cpu_requests)} / "
            f"{format_cores(overview.cpu_allocatable)}"
        )
        page.cpuCaption.setText(cpu_text)
        self._set_bar(
            page.cpuBar, self._ratio(overview.cpu_requests, overview.cpu_allocatable)
        )

        memory_text = translate("OverviewPage", "requested / allocatable")
        if overview.memory_usage is not None:
            memory_text += self.tr(" · usage {value}").format(
                value=format_bytes(overview.memory_usage)
            )
        page.memValue.setText(
            f"{format_bytes(overview.memory_requests)} / "
            f"{format_bytes(overview.memory_allocatable)}"
        )
        page.memCaption.setText(memory_text)
        self._set_bar(
            page.memBar,
            self._ratio(overview.memory_requests, overview.memory_allocatable),
        )

        for name in ("namespaces", "deployments", "statefulsets", "daemonsets"):
            value = getattr(overview, name)
            getattr(page, f"{name}Value").setText("—" if value is None else str(value))
            getattr(page, f"{name}Caption").setText(
                translate("OverviewPage", "in the cluster")
                if name == "namespaces"
                else translate("OverviewPage", "workloads")
            )

        self.nodes_table.setRowCount(len(overview.nodes))
        for row, node in enumerate(overview.nodes):
            values = (
                node.name,
                self.tr("Ready") if node.ready else self.tr("Not ready"),
                node.roles,
                node.version,
                f"{format_cores(node.cpu_requests)} / "
                f"{format_cores(node.cpu_allocatable)}",
                f"{format_bytes(node.memory_requests)} / "
                f"{format_bytes(node.memory_allocatable)}",
                f"{node.pods_running} / {node.pods_allocatable}",
                node.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor("#242a33"))
                if column == 1:
                    text_color, background = (
                        ("#176b58", "#e5f4eb") if node.ready else ("#a33d45", "#fce9ea")
                    )
                    item.setForeground(QColor(text_color))
                    item.setBackground(QColor(background))
                self.nodes_table.setItem(row, column, item)

        notices = list(overview.warnings)
        if overview.nodes and not overview.metrics_available:
            notices.append(self.tr("Real usage unavailable: metrics-server not found."))
        page.noticeLabel.setText("  ·  ".join(notices))

    def _begin_loading(self, button: QPushButton | None, label: str) -> Callable:
        """Show a busy cursor and button spinner; return a one-shot finisher."""
        self._loading += 1
        if self._loading == 1:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if button is not None and self._spinner_button is None:
            self._spinner_button = button
            self._spinner_saved = (button.icon(), button.text())
            button.setText(label)
            self._spinner_timer.start()
            self._tick_spinner()
        finished = False

        def end(*_args: object) -> None:
            nonlocal finished
            if not finished:
                finished = True
                self._end_loading(button)

        return end

    def _end_loading(self, button: QPushButton | None) -> None:
        self._loading = max(0, self._loading - 1)
        if button is not None and button is self._spinner_button:
            self._spinner_timer.stop()
            if self._spinner_saved is not None:
                button.setIcon(self._spinner_saved[0])
                button.setText(self._spinner_saved[1])
            self._spinner_button = None
            self._spinner_saved = None
        if self._loading == 0:
            QApplication.restoreOverrideCursor()

    def _tick_spinner(self) -> None:
        if self._spinner_button is None:
            return
        self._spinner_angle = (self._spinner_angle + 30) % 360
        primary = (self.refresh_button, self.overview_refresh_button)
        color = "#ffffff" if self._spinner_button in primary else "#3220a0"
        self._spinner_button.setIcon(_spinner_icon(self._spinner_angle, color))

    def refresh(self, *_args: object) -> None:
        context = self._context()
        if not context or (self._worker is not None and self._worker.isRunning()):
            return
        namespace = self.namespace_combo.currentData() or None
        self.refresh_button.setEnabled(False)
        self.context_combo.setEnabled(False)
        self.namespace_combo.setEnabled(False)
        self._set_status(lambda: self.tr("Loading resources..."))
        self._worker = RefreshWorker(context, namespace)
        end_loading = self._begin_loading(self.refresh_button, self.tr("Refreshing..."))
        self._worker.completed.connect(end_loading)
        self._worker.failed.connect(end_loading)
        self._worker.finished.connect(end_loading)
        self._worker.completed.connect(self._show_workloads)
        self._worker.failed.connect(self._show_error)
        self._worker.finished.connect(self._refresh_finished)
        self._worker.start()

    def _show_workloads(self, namespaces: list, workloads: list) -> None:
        self._workloads = workloads
        self._apply_sort()
        self._namespaces = namespaces
        selected_namespace = self.namespace_combo.currentData()
        self.namespace_combo.blockSignals(True)
        self.namespace_combo.clear()
        self.namespace_combo.addItem(self.tr("All namespaces"), "")
        for namespace in namespaces:
            self.namespace_combo.addItem(namespace, namespace)
        index = self.namespace_combo.findData(selected_namespace)
        self.namespace_combo.setCurrentIndex(max(index, 0))
        self.namespace_combo.blockSignals(False)

        self._render_workloads()

    def _apply_sort(self) -> None:
        """Order self._workloads by the chosen header; no-op until one is clicked."""
        if self._sort is None:
            return
        column, order = self._sort
        self._workloads.sort(
            key=lambda workload: workload_sort_key(workload, column),
            reverse=order == Qt.SortOrder.DescendingOrder,
        )

    def _sort_workloads(self, column: int) -> None:
        """Header click: sort ascending, click again to reverse."""
        if self._sort is not None and self._sort[0] == column:
            flipped = self._sort[1] == Qt.SortOrder.AscendingOrder
            order = (
                Qt.SortOrder.DescendingOrder if flipped else Qt.SortOrder.AscendingOrder
            )
        else:
            order = Qt.SortOrder.AscendingOrder
        self._sort = (column, order)
        selected = self._selected_workload()
        self._apply_sort()
        header = self.table.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(column, order)
        self._render_workloads()
        if selected in self._workloads:
            self.table.selectRow(self._workloads.index(selected))
        self._update_workload_actions()

    def _render_workloads(self) -> None:
        workloads = self._workloads
        statuses = {
            "Healthy": self.tr("Healthy"),
            "Degraded": self.tr("Degraded"),
            "Unavailable": self.tr("Unavailable"),
            "Scaled to zero": self.tr("Scaled to zero"),
        }
        self.table.setRowCount(len(workloads))
        for row_index, workload in enumerate(workloads):
            values = (
                workload.namespace,
                workload.kind,
                workload.name,
                f"{workload.ready}/{workload.desired}",
                statuses[workload.status],
                workload.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor("#242a33"))
                if column == 4:
                    color = {
                        "Healthy": ("#176b58", "#e5f4eb"),
                        "Degraded": ("#985415", "#fff2de"),
                        "Unavailable": ("#a33d45", "#fce9ea"),
                        "Scaled to zero": ("#505963", "#eff1f3"),
                    }[workload.status]
                    item.setForeground(QColor(color[0]))
                    item.setBackground(QColor(color[1]))
                self.table.setItem(row_index, column, item)
        self._filter_rows()
        self._set_status(
            lambda: self.tr("{count} workloads in {namespaces} namespaces").format(
                count=len(workloads), namespaces=len(self._namespaces)
            )
        )

    def _filter_rows(self, *_args: object) -> None:
        query = self.search_input.text().strip().casefold()
        visible_rows = 0
        for row_index, workload in enumerate(self._workloads):
            searchable_text = f"{workload.namespace} {workload.kind} {workload.name}"
            matches = query in searchable_text.casefold()
            self.table.setRowHidden(row_index, not matches)
            visible_rows += matches
        self._update_workload_actions()
        self.summary_label.setText(
            self.tr("{visible} of {total} workloads").format(
                visible=visible_rows, total=len(self._workloads)
            )
        )

    def _selected_workload(self) -> Workload | None:
        row = self.table.currentRow()
        if 0 <= row < len(self._workloads) and not self.table.isRowHidden(row):
            return self._workloads[row]
        return None

    def _update_workload_actions(self) -> None:
        enabled = self._selected_workload() is not None
        for button in (self.pods_button, self.details_button, self.logs_button):
            button.setEnabled(enabled and not self._close_when_worker_stops)

    def _run_action(
        self,
        operation: Callable[..., Any],
        on_success: Callable[[Any], None],
        *arguments: Any,
        on_error: Callable[[str], None] | None = None,
        quiet: bool = False,
    ) -> None:
        if self._close_when_worker_stops:
            return
        worker = ActionWorker(operation, arguments)
        self._action_workers.append(worker)
        if not quiet:  # background refreshes must not flash the busy cursor
            sender = self.sender()
            end_loading = self._begin_loading(
                sender if isinstance(sender, QPushButton) else None,
                self.tr("Loading..."),
            )
            worker.completed.connect(end_loading)
            worker.failed.connect(end_loading)
            worker.finished.connect(end_loading)
        worker.completed.connect(on_success)
        worker.failed.connect(on_error or self._show_action_error)
        worker.finished.connect(lambda: self._action_worker_finished(worker))
        worker.start()

    def _action_worker_finished(self, worker: ActionWorker) -> None:
        if worker in self._action_workers:
            self._action_workers.remove(worker)
        self._finish_deferred_close()

    def _finish_deferred_close(self) -> None:
        refresh_running = self._worker is not None and self._worker.isRunning()
        actions_running = any(worker.isRunning() for worker in self._action_workers)
        if (
            self._close_when_worker_stops
            and not refresh_running
            and not actions_running
        ):
            self.close()

    def _view_workload_pods(self) -> None:
        workload = self._selected_workload()
        if workload is None:
            return
        context = self._context()
        self._run_action(
            get_workload_pods,
            lambda result: self._show_pods_dialog(workload, result),
            context,
            workload,
        )

    def _view_workload_details(self) -> None:
        workload = self._selected_workload()
        if workload is None:
            return
        self._run_action(
            get_resource_details,
            lambda result: self._show_json_dialog(
                f"{workload.kind}: {workload.name}", result
            ),
            self._context(),
            workload.kind,
            workload.namespace,
            workload.name,
        )

    def _view_workload_logs(self) -> None:
        workload = self._selected_workload()
        if workload is None:
            return
        context = self._context()
        self._run_action(
            get_workload_pods,
            lambda result: self._choose_pod_for_logs(context, result),
            context,
            workload,
        )

    def _show_pods_dialog(self, workload: Workload, pods: list[PodInfo]) -> None:
        dialog = QDialog(self)
        form = Ui_PodsDialog()
        form.setupUi(dialog)
        dialog.setWindowTitle(self.tr("Pods of {name}").format(name=workload.name))
        form.summaryLabel.setText(
            self.tr("{count} Pods in {namespace} / {name}").format(
                count=len(pods), namespace=workload.namespace, name=workload.name
            )
        )
        table = form.podsTable
        details_button = form.detailsButton
        logs_button = form.logsButton
        table.setRowCount(0)
        table.setRowCount(len(pods))
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for column, width in ((1, 90), (2, 120), (3, 110), (4, 90)):
            table.setColumnWidth(column, width)
        for row, pod in enumerate(pods):
            values = (
                pod.name,
                f"{pod.ready}/{pod.total}",
                pod.phase,
                str(len(pod.containers)),
                pod.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor("#242a33"))
                table.setItem(row, column, item)

        def selected_pod() -> PodInfo | None:
            row = table.currentRow()
            if 0 <= row < len(pods):
                return pods[row]
            return None

        def update_pod_actions() -> None:
            has_selection = selected_pod() is not None
            details_button.setEnabled(has_selection)
            logs_button.setEnabled(has_selection)

        def show_pod_details() -> None:
            pod = selected_pod()
            if pod is None:
                return
            dialog.accept()  # the result opens as a tab behind this dialog
            self._run_action(
                get_resource_details,
                lambda result: self._show_json_dialog(
                    self.tr("Pod: {name}").format(name=pod.name), result
                ),
                self._context(),
                "Pod",
                pod.namespace,
                pod.name,
            )

        def show_pod_logs() -> None:
            pod = selected_pod()
            if pod is not None:
                dialog.accept()
                self._choose_container_for_logs(self._context(), pod)

        table.itemSelectionChanged.connect(update_pod_actions)
        table.cellDoubleClicked.connect(lambda _row, _column: show_pod_details())
        details_button.clicked.connect(show_pod_details)
        logs_button.clicked.connect(show_pod_logs)
        form.closeButton.clicked.connect(dialog.accept)
        if not pods:
            form.summaryLabel.setText(
                self.tr("No Pods are associated with this workload")
            )
        dialog.exec()

    def _choose_pod_for_logs(self, context: str, pods: list[PodInfo]) -> None:
        if not pods:
            QMessageBox.information(
                self, self.tr("Logs"), self.tr("This workload has no Pods.")
            )
            return
        if len(pods) == 1:
            self._choose_container_for_logs(context, pods[0])
            return
        pod_names = [pod.name for pod in pods]
        pod_name, accepted = QInputDialog.getItem(
            self,
            self.tr("View logs"),
            self.tr("Select the Pod:"),
            pod_names,
            0,
            False,
        )
        if accepted:
            pod = next(pod for pod in pods if pod.name == pod_name)
            self._choose_container_for_logs(context, pod)

    def _choose_container_for_logs(self, context: str, pod: PodInfo) -> None:
        if not pod.containers:
            QMessageBox.information(
                self,
                self.tr("Logs"),
                self.tr("Pod {name} has no containers.").format(name=pod.name),
            )
            return
        if len(pod.containers) == 1:
            container, accepted = pod.containers[0], True
        else:
            container, accepted = QInputDialog.getItem(
                self,
                self.tr("View logs"),
                self.tr("Select the container of {name}:").format(name=pod.name),
                list(pod.containers),
                0,
                False,
            )
        if accepted:
            self._run_action(
                get_pod_logs,
                lambda result: self._show_logs_dialog(pod, container, result),
                context,
                pod.namespace,
                pod.name,
                container,
            )

    def _open_text_tab(self, title: str, text: str) -> None:
        """Show read-only text in a new closable tab of the viewer page."""
        editor = QPlainTextEdit()
        editor.setReadOnly(True)
        editor.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
        editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        editor.setPlainText(text)
        self._add_viewer_tab(editor, title)

    def _add_viewer_tab(self, widget: QWidget, title: str) -> None:
        index = self.viewer_tabs.addTab(widget, title)
        self.viewer_tabs.setTabToolTip(index, title)
        self.viewer_tabs.setCurrentIndex(index)
        self.nav_viewer.show()
        self._show_page(3)

    def _close_viewer_tab(self, index: int) -> None:
        editor = self.viewer_tabs.widget(index)
        self.viewer_tabs.removeTab(index)
        if isinstance(editor, LogTab):
            editor.closed = True
        editor.deleteLater()
        if self.viewer_tabs.count() == 0:
            self.nav_viewer.hide()
            if self.pages.currentIndex() == 3:
                self._show_page(1)

    def _show_json_dialog(self, title: str, document: dict[str, Any]) -> None:
        self._open_text_tab(title, json.dumps(document, ensure_ascii=False, indent=2))

    def _show_logs_dialog(self, pod: PodInfo, container: str, logs: str) -> None:
        tab = LogTab(self._context(), pod, container)
        tab.set_logs(logs)
        timer = QTimer(tab)
        timer.setInterval(LOG_REFRESH_MS)
        timer.timeout.connect(lambda: self._refresh_log(tab))
        timer.start()
        tab.ui.refreshButton.clicked.connect(lambda: self._refresh_log(tab, True))
        title = self.tr("Logs: {pod} / {container}").format(
            pod=pod.name, container=container
        )
        self._add_viewer_tab(tab, title)

    def _refresh_log(self, tab: LogTab, force: bool = False) -> None:
        """Fetch newer lines quietly; skipped while paused or not on screen."""
        if tab.closed or tab.busy:
            return
        if not force:
            on_screen = (
                self.pages.currentIndex() == 3
                and self.viewer_tabs.currentWidget() is tab
                and self.isVisible()
            )
            if not (tab.auto_refresh and on_screen):
                return
        tab.busy = True

        def done(result: str) -> None:
            tab.busy = False
            if not tab.closed:
                tab.set_logs(result)

        def failed(message: str) -> None:
            tab.busy = False
            if not tab.closed:
                tab.set_error(message)

        self._run_action(
            get_pod_logs,
            done,
            tab.context,
            tab.pod.namespace,
            tab.pod.name,
            tab.container,
            on_error=failed,
            quiet=True,
        )

    def _save_settings(self) -> None:
        try:
            self.settings.save()
        except OSError as error:
            logger.warning("Could not save settings: %s", error)

    def _load_settings_form(self) -> None:
        """Fill the settings page from the saved preferences."""
        form = self.settings_ui
        form.languageCombo.clear()
        for code, label in (
            ("auto", self.tr("Automatic")),
            ("en", "English"),
            ("pt", "Português"),
        ):
            form.languageCombo.addItem(label, code)
        form.languageCombo.setCurrentIndex(
            max(form.languageCombo.findData(self.settings.language), 0)
        )
        form.rememberCheck.setChecked(self.settings.remember_last_context)

        aliases = self.settings.context_aliases
        table = form.contextsTable
        table.setRowCount(len(self._contexts))
        # Real context names (often long ARNs) must stay readable: size the first
        # column to its content and let the editable name take the rest.
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        for row, context in enumerate(self._contexts):
            name_item = QTableWidgetItem(context)
            name_item.setToolTip(context)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 0, name_item)
            table.setItem(row, 1, QTableWidgetItem(aliases.get(context, "")))
        if self._contexts:
            form.contextsHint.setText(
                QCoreApplication.translate(
                    "SettingsPage",
                    "Give your contexts friendlier names. Leave a name empty to keep the original one.",  # noqa: E501
                )
            )
        else:
            form.contextsHint.setText(self.tr("No contexts were found in kubeconfig."))
        form.noticeLabel.setText("")

    def _save_preferences(self) -> None:
        form = self.settings_ui
        table = form.contextsTable
        aliases = self.settings.context_aliases
        if self._contexts:
            edited = {
                context: table.item(row, 1).text()
                for row, context in enumerate(self._contexts)
            }
            kept = {c: a for c, a in aliases.items() if c not in edited}
            self.settings.set_context_aliases({**kept, **edited})
        previous_language = self.settings.language
        self.settings.language = form.languageCombo.currentData()
        self.settings.remember_last_context = form.rememberCheck.isChecked()
        if self.settings.remember_last_context:
            self.settings.last_context = self._context()
        self._save_settings()
        self._fill_contexts(self._context())
        if self.settings.language != previous_language:
            apply_language(self.settings.language)
        form.noticeLabel.setText(self.tr("Settings saved."))

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange and hasattr(self, "ui"):
            self._retranslate()
        super().changeEvent(event)

    def _retranslate(self) -> None:
        """Re-apply every visible text after the translator changed."""
        self.ui.retranslateUi(self)
        self.overview_ui.retranslateUi(self.ui.overviewHost)
        self.settings_ui.retranslateUi(self.ui.settingsHost)
        if self.pages.currentIndex() == 2:
            self._load_settings_form()
        self._apply_page_titles()
        if self.namespace_combo.count():
            self.namespace_combo.setItemText(0, self.tr("All namespaces"))
        self._render_workloads()
        if self._overview is not None:
            self._render_overview(self._overview)
        else:
            self._reset_overview()
        if self._status_message is not None:
            self.status_label.setText(self._status_message())

    def _show_action_error(self, message: str) -> None:
        QMessageBox.warning(self, self.tr("Query failed"), message)

    def _show_error(self, message: str) -> None:
        self._workloads = []
        self._set_status(
            lambda: self.tr("Could not load workloads: {message}").format(
                message=message
            )
        )
        self.table.setRowCount(0)
        self._filter_rows()

    def _refresh_finished(self) -> None:
        self.refresh_button.setEnabled(True)
        self.context_combo.setEnabled(True)
        self.namespace_combo.setEnabled(True)
        self._finish_deferred_close()

    def closeEvent(self, event: QCloseEvent) -> None:
        refresh_running = self._worker is not None and self._worker.isRunning()
        actions_running = any(worker.isRunning() for worker in self._action_workers)
        if refresh_running or actions_running:
            self._close_when_worker_stops = True
            self._set_status(
                lambda: self.tr("Finishing the current cluster request...")
            )
            self._update_workload_actions()
            event.ignore()
            return
        super().closeEvent(event)
