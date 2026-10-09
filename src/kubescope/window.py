import dataclasses
import html
import json
import logging
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from PySide6.QtCore import (
    QCoreApplication,
    QEasingCurve,
    QEvent,
    QPoint,
    QPointF,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
    QThread,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QColor,
    QDesktopServices,
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
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QStyle,
    QTableWidgetItem,
    QWidget,
)

from kubescope import PROJECT_URL, __version__
from kubescope.cluster import (
    KubectlError,
    LoginAction,
    cancel_running,
    check_login,
    get_cluster_overview,
    get_pod_logs,
    get_pods,
    get_resource_details,
    get_usage,
    get_workload_pods,
    get_workloads,
    get_workloads_overview,
    list_contexts,
    run_login,
)
from kubescope.diagnostics import configure_logging, log_file
from kubescope.errors import ErrorInfo, describe_error, first_line, is_auth_error
from kubescope.i18n import apply_language
from kubescope.log_tab import LOG_REFRESH_MS, LogTab
from kubescope.models import (
    WORKLOAD_VIEWS,
    ClusterOverview,
    PodInfo,
    Workload,
    WorkloadsOverview,
    format_bytes,
    format_cores,
    format_cpu,
    format_memory,
    pod_highlight,
    pod_sort_key,
    workload_sort_key,
)
from kubescope.settings import LANGUAGES, Settings, log_directory
from kubescope.theme import (
    Theme,
    active_theme,
    apply_theme,
    available_themes,
    save_custom_theme,
    theme_tokens,
    themed,
    themed_stylesheet,
    themes_directory,
)
from kubescope.theme_editor import ThemeEditor
from kubescope.ui.ui_main_window import Ui_MainWindow
from kubescope.ui.ui_overview_page import Ui_OverviewPage
from kubescope.ui.ui_pods_dialog import Ui_PodsDialog
from kubescope.ui.ui_settings_page import Ui_SettingsPage
from kubescope.ui.ui_viewer_page import Ui_ViewerPage
from kubescope.ui.ui_workloads_overview_page import Ui_WorkloadsOverviewPage

logger = logging.getLogger(__name__)

# Overview rows that open a list when clicked, and the list each opens.
WORKLOAD_LINKS = {
    "pods": "pods",
    "deployments": "deployments",
    "statefulsets": "statefulsets",
    "jobs": "jobs",
    "cronjobs": "cronjobs",
}


def _icon_path(name: str, draw: Callable[[QPainter], None], size: QSize) -> str:
    """Render a small PNG once; Qt style sheets cannot draw shapes
    themselves."""
    path = Path(tempfile.gettempdir()) / f"kubescope-{active_theme()}-{name}.png"
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
        painter.setBrush(QColor(themed(color)))
        painter.drawPolygon(QPolygonF([QPointF(0, 0), QPointF(10, 0), QPointF(5, 6)]))

    return _icon_path(name, draw, QSize(10, 6))


def _sort_icon_path(up: bool) -> str:
    def draw(painter: QPainter) -> None:
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(themed("#3220a0")))
        points = [QPointF(0, 6), QPointF(9, 6), QPointF(4.5, 0)]
        if not up:
            points = [QPointF(0, 0), QPointF(9, 0), QPointF(4.5, 6)]
        painter.drawPolygon(QPolygonF(points))

    return _icon_path("sort-up" if up else "sort-down", draw, QSize(9, 6))


def _close_icon_path(color: str, name: str) -> str:
    def draw(painter: QPainter) -> None:
        pen = QPen(QColor(themed(color)), 1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(QPointF(1.5, 1.5), QPointF(8.5, 8.5))
        painter.drawLine(QPointF(8.5, 1.5), QPointF(1.5, 8.5))

    return _icon_path(name, draw, QSize(10, 10))


def _spinner_icon(angle: int, color: str) -> QIcon:
    """Draw one frame of the loading spinner; the disabled state keeps its
    color."""
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

    def __init__(
        self, context: str, namespace: str | None, view: str = "deployments"
    ) -> None:
        super().__init__()
        self.context = context
        self.namespace = namespace
        self.view = view

    def run(self) -> None:
        try:
            if self.view == "pods":
                namespaces, items = get_pods(self.context, self.namespace)
            else:
                kind = WORKLOAD_VIEWS[self.view]
                namespaces, items = get_workloads(self.context, self.namespace, (kind,))
                try:
                    usage = (
                        {}  # a CronJob's Pods belong to the Jobs it creates
                        if kind == "CronJob"
                        else get_usage(self.context, self.namespace)
                    )
                except KubectlError as error:  # metrics-server is optional
                    logger.debug("No Pod usage for %s: %s", self.context, error)
                    usage = {}
                except Exception:
                    logger.exception("Could not load Pod usage for %s", self.context)
                    usage = {}
                items = [
                    dataclasses.replace(
                        item,
                        restarts=restarts,
                        cpu=cpu,
                        memory=memory,
                    )
                    for item in items
                    for restarts, cpu, memory in [
                        usage.get((item.namespace, item.kind, item.name))
                        or (0, None, None)
                    ]
                ]
        except KubectlError as error:  # expected: the window explains it
            logger.debug(
                "Could not load %s from %s: %s", self.view, self.context, error
            )
            self.failed.emit(str(error))
            return
        except Exception as error:
            logger.exception(
                "Could not load %s from context %s", self.view, self.context
            )
            self.failed.emit(str(error))
            return
        self.completed.emit(namespaces, items)


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
        except KubectlError as error:  # expected: the window explains it
            logger.debug("Kubernetes action failed: %s", error)
            self.failed.emit(str(error))
            return
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
        self._pods: list[PodInfo] = []
        self._view = "deployments"  # which list the shared table shows
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
        self.login_button = ui.loginButton
        self.pages = ui.pages
        self.nav_overview = ui.navOverview
        self.nav_workloads = ui.navWorkloads
        self.submenu = ui.workloadsSubmenu
        self.nav_workloads_overview = ui.navWorkloadsOverview
        self.nav_pods = ui.navPods
        self.nav_deployments = ui.navDeployments
        self.nav_statefulsets = ui.navStatefulSets
        self.nav_jobs = ui.navJobs
        self.nav_cronjobs = ui.navCronJobs
        self._nav_views = {
            "pods": self.nav_pods,
            "deployments": self.nav_deployments,
            "statefulsets": self.nav_statefulsets,
            "jobs": self.nav_jobs,
            "cronjobs": self.nav_cronjobs,
        }

        self.overview_ui = Ui_OverviewPage()
        self.overview_ui.setupUi(ui.overviewHost)
        self.overview_refresh_button = self.overview_ui.overviewRefreshButton
        self.nodes_table = self.overview_ui.nodesTable
        self.workloads_ui = Ui_WorkloadsOverviewPage()
        self.workloads_ui.setupUi(ui.workloadsOverviewHost)
        self.workloads_refresh_button = self.workloads_ui.workloadsRefreshButton
        self.workloads_table = self.workloads_ui.eventsTable
        events_header = self.workloads_table.horizontalHeader()
        for column in range(self.workloads_table.columnCount()):
            events_header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.Stretch
                if column == 4  # the message takes what the others leave
                else QHeaderView.ResizeMode.ResizeToContents,
            )
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
        self.settings_ui.openLogsButton.clicked.connect(self._open_log_folder)
        self.settings_ui.newThemeButton.clicked.connect(self._new_theme)
        self.settings_ui.editThemeButton.clicked.connect(self._edit_theme)
        self.settings_ui.openThemesButton.clicked.connect(self._open_themes_folder)
        self.settings_ui.themeCombo.currentIndexChanged.connect(
            self._update_theme_buttons
        )
        self._overview_context: str | None = None
        self._overview_busy = False

        style = self.style()
        self.nav_overview.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
        )
        for button in (
            self.nav_overview,
            self.nav_workloads,
            self.nav_workloads_overview,
            *self._nav_views.values(),
            ui.navViewer,
            ui.settingsButton,
        ):
            button.setAutoExclusive(False)  # _show_page keeps the checked state
        self.nav_workloads.setCheckable(False)
        self._submenu_animation = QPropertyAnimation(self.submenu, b"maximumHeight")
        self._submenu_animation.setDuration(180)
        self._submenu_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.nav_workloads.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        )
        self.workloads_refresh_button.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
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
        self.summary_label.setText(self.tr("0 Deployments"))
        self.nodes_table.setRowCount(0)
        self._reset_overview()
        # every column stays user-resizable; the last one takes the spare room
        self.nodes_table.horizontalHeader().setStretchLastSection(True)
        for column, width in (
            (0, 220),
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
        header.setStretchLastSection(True)
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self._sort_rows)
        self._apply_view_columns()
        for column, width in (
            (0, 160),
            (1, 150),
            (2, 320),
            (3, 110),
            (4, 150),
            (5, 90),
            (6, 100),
            (7, 90),
        ):
            self.table.setColumnWidth(column, width)
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self._show_column_menu)
        self._style_template = self.styleSheet()
        self._apply_style()
        self._show_version()
        self.ui.githubLink.clicked.connect(self._open_project)

        self._spinner_angle = 0
        self._spinner_button: QPushButton | None = None
        self._spinner_saved: tuple[QIcon, str] | None = None
        self._spinner_timer = QTimer(self)
        self._spinner_timer.setInterval(70)
        self._spinner_timer.timeout.connect(self._tick_spinner)

        self._workloads_overview: WorkloadsOverview | None = None
        self._workloads_overview_context: str | None = None
        self._workloads_overview_busy = False
        self._login_action: LoginAction | None = None
        self._login_checking = False
        self.login_button.clicked.connect(self._sign_in)
        self.refresh_button.clicked.connect(self.refresh)
        self.refresh_button.clicked.connect(lambda: self._check_login())
        self.pods_button.clicked.connect(self._view_workload_pods)
        self.details_button.clicked.connect(self._view_details)
        self.logs_button.clicked.connect(self._view_logs)
        self.table.itemSelectionChanged.connect(self._update_workload_actions)
        self.table.cellDoubleClicked.connect(lambda _row, _column: self._view_details())
        self.nav_viewer.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        )
        self.nav_viewer.clicked.connect(lambda: self._show_page(3))
        ui.settingsButton.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )
        ui.settingsButton.clicked.connect(lambda: self._show_page(2))
        self.nav_overview.clicked.connect(lambda: self._show_page(0))
        self.nav_workloads.clicked.connect(self._toggle_submenu)
        for view, button in self._nav_views.items():
            button.clicked.connect(
                lambda _checked=False, view=view: self._open_list_view(view)
            )
        self.nav_workloads_overview.clicked.connect(lambda: self._show_page(4))
        self.workloads_refresh_button.clicked.connect(self.refresh_workloads_overview)
        # the overview names each kind; the ones that have a list link to it
        for key, view in WORKLOAD_LINKS.items():
            getattr(self.workloads_ui, f"{key}Link").clicked.connect(
                lambda _checked=False, view=view: self._open_list_view(view)
            )
        for key in ("daemonsets", "replicasets"):  # counted, but no list of their own
            getattr(self.workloads_ui, f"{key}Link").setEnabled(False)
        self.overview_refresh_button.clicked.connect(self.refresh_overview)
        self.context_combo.currentTextChanged.connect(self._context_changed)
        self.context_combo.currentTextChanged.connect(self.refresh)
        self.namespace_combo.currentIndexChanged.connect(self.refresh)
        self.search_input.textChanged.connect(self._filter_rows)

    def _load_contexts(self) -> None:
        """Read the kubeconfig contexts in a worker; kubectl can take a while
        and must not freeze the window."""
        self._set_status(lambda: self.tr("Loading contexts..."))
        self.refresh_button.setEnabled(False)
        self._run_action(
            list_contexts, self._contexts_loaded, on_error=self._contexts_failed
        )

    def _contexts_failed(self, reason: str) -> None:
        logger.warning("Could not load kubeconfig: %s", first_line(reason))
        self._set_status(
            lambda: self.tr("Could not load kubeconfig: {error}").format(
                error=self._error_line(reason)
            )
        )
        self.status_label.setToolTip(describe_error(reason).details)
        self.context_combo.setEnabled(False)
        self.namespace_combo.setEnabled(False)
        self.refresh_button.setEnabled(False)

    def _contexts_loaded(self, result: tuple[list[str], str | None]) -> None:
        contexts, active_context = result
        self._contexts = contexts
        remembered = self.settings.last_context
        if self.settings.remember_last_context and remembered in contexts:
            selected = remembered
        else:
            selected = active_context
        logger.info("Loaded %d context(s); selected %s", len(contexts), selected)
        self._fill_contexts(selected)
        if not contexts:
            self._set_status(lambda: self.tr("No contexts found in kubeconfig"))
            self.refresh_button.setEnabled(False)
            return
        self.refresh()
        self._ensure_overview()
        self._check_login()

    def _fill_contexts(self, selected: str | None) -> None:
        """Show contexts under their custom names while keeping the real
        name."""
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

    @staticmethod
    def _error_line(message: str) -> str:
        info = describe_error(message)
        return f"{info.title}. {info.hint}" if info.hint else info.title

    def _set_status(self, message: Callable[[], str]) -> None:
        self.status_label.setToolTip("")
        self._status_message = message
        self.status_label.setText(message())

    def _show_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        self.nav_overview.setChecked(index == 0)
        for view, button in self._nav_views.items():
            button.setChecked(index == 1 and self._view == view)
        self.ui.settingsButton.setChecked(index == 2)
        self.nav_viewer.setChecked(index == 3)
        self.nav_workloads_overview.setChecked(index == 4)
        self._apply_page_titles()
        if index == 0:
            self._ensure_overview()
        elif index == 4:
            self._ensure_workloads_overview()
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
        elif self.pages.currentIndex() == 4:
            self.ui.pageTitle.setText(self.tr("Workloads overview"))
            self.ui.pageSubtitle.setText(
                self.tr("Health of every workload kind and the latest events")
            )
        else:
            title, subtitle = {
                "pods": (self.tr("Pods"), self.tr("Pods of the cluster")),
                "deployments": (
                    self.tr("Deployments"),
                    self.tr("Deployments of the cluster"),
                ),
                "statefulsets": (
                    self.tr("StatefulSets"),
                    self.tr("StatefulSets of the cluster"),
                ),
                "jobs": (self.tr("Jobs"), self.tr("Jobs of the cluster")),
                "cronjobs": (self.tr("CronJobs"), self.tr("CronJobs of the cluster")),
            }[self._view]
            self.ui.pageTitle.setText(title)
            self.ui.pageSubtitle.setText(subtitle)

    def _show_version(self) -> None:
        """The version in the footer's corner; the link opens the project."""
        self.ui.footerVersion.setText(
            self.tr("Version {version}").format(version=__version__)
        )
        self.ui.githubLink.setToolTip(
            self.tr("Open the project on GitHub") + f"\n{PROJECT_URL}"
        )

    def _open_project(self) -> None:
        QDesktopServices.openUrl(QUrl(PROJECT_URL))

    def _apply_style(self) -> None:
        """Style the window for the active theme; the icons Qt style sheets
        cannot draw are rendered in the theme's colors."""
        self.setStyleSheet(
            themed_stylesheet(self._style_template)
            .replace("SORT_UP", _sort_icon_path(up=True))
            .replace("SORT_DOWN", _sort_icon_path(up=False))
            .replace("CHEVRON_LIGHT", _chevron_icon_path("#b8c7dc", "chevron-light"))
            .replace("CHEVRON", _chevron_icon_path())
            .replace("CLOSE_ICON_HOVER", _close_icon_path("#3220a0", "close-hover"))
            .replace("CLOSE_ICON", _close_icon_path("#6b7380", "close"))
        )

    def _apply_theme(self) -> None:
        """Switch to the theme in the settings and redraw what was drawn with
        the old colors."""
        apply_theme(QApplication.instance(), self.settings.theme)
        self._apply_style()
        self._render_rows()
        if self._overview is not None:
            self._render_overview(self._overview)
        if self._workloads_overview is not None:
            self._render_workloads_overview(self._workloads_overview)

    def _toggle_submenu(self) -> None:
        """Slide the Pods, Deployments, StatefulSets, Jobs and CronJobs entries
        open or closed."""
        animation = self._submenu_animation
        expand = self.submenu.maximumHeight() == 0 or (
            animation.state() == QPropertyAnimation.State.Running
            and animation.endValue() == 0
        )
        animation.stop()
        animation.setStartValue(self.submenu.maximumHeight())
        animation.setEndValue(self.submenu.sizeHint().height() if expand else 0)
        animation.start()

    def _open_list_view(self, view: str) -> None:
        """Show a Pods or workload list; they all share one table."""
        changed = view != self._view
        if changed and view in WORKLOAD_VIEWS and self._view in WORKLOAD_VIEWS:
            self._workloads = []  # another kind: do not show these rows meanwhile
        logger.debug("Opening the %s list", view)
        self._view = view
        if changed:
            self._sort = None
            header = self.table.horizontalHeader()
            header.setSortIndicatorShown(False)
            self._apply_view_columns()
            self._render_rows()
        self._show_page(1)
        if changed:
            self.refresh()

    def _apply_view_columns(self) -> None:
        second = "CONTAINERS" if self._view == "pods" else "KIND"
        ready_header = {
            "jobs": QCoreApplication.translate("MainWindow", "COMPLETIONS"),
            "cronjobs": QCoreApplication.translate("MainWindow", "SCHEDULE"),
        }.get(self._view) or QCoreApplication.translate("MainWindow", "READY")
        context = "PodsDialog" if self._view == "pods" else "MainWindow"
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            [
                QCoreApplication.translate("MainWindow", "NAMESPACE"),
                QCoreApplication.translate(context, second),
                QCoreApplication.translate("MainWindow", "NAME"),
                ready_header,
                QCoreApplication.translate("MainWindow", "STATUS"),
                QCoreApplication.translate("MainWindow", "CPU"),
                QCoreApplication.translate("MainWindow", "MEMORY"),
                QCoreApplication.translate("MainWindow", "RESTARTS"),
                QCoreApplication.translate("MainWindow", "AGE"),
            ]
        )
        self.pods_button.setVisible(self._view in WORKLOAD_VIEWS)
        hidden = self.settings.hidden_columns(self._view)
        for column in range(self.table.columnCount()):
            self.table.setColumnHidden(column, column in hidden)

    def _show_column_menu(self, position: QPoint) -> None:
        """Header right-click: tick the columns to show; the choice is
        saved."""
        menu = QMenu(self)
        hidden = self.settings.hidden_columns(self._view)
        for column in range(self.table.columnCount()):
            label = self.table.horizontalHeaderItem(column).text()
            action = QAction(label, menu, checkable=True)
            action.setChecked(column not in hidden)
            action.setEnabled(column != 2)  # the name stays, rows need an identity
            action.toggled.connect(
                lambda visible, column=column: self._set_column_visible(column, visible)
            )
            menu.addAction(action)
        menu.exec(self.table.horizontalHeader().mapToGlobal(position))

    def _set_column_visible(self, column: int, visible: bool) -> None:
        hidden = self.settings.hidden_columns(self._view)
        hidden.discard(column) if visible else hidden.add(column)
        self.settings.set_hidden_columns(self._view, hidden)
        self._save_settings()
        self.table.setColumnHidden(column, not visible)

    def _context_changed(self, *_args: object) -> None:
        logger.info("Context changed to %s", self._context())
        self._overview_context = None
        self._workloads_overview_context = None
        self._hide_login()
        self._check_login()
        if self.pages.currentIndex() == 4:
            self._ensure_workloads_overview()
        if self.settings.remember_last_context and self._contexts:
            self.settings.last_context = self._context()
            self._save_settings()
        if self.pages.currentIndex() == 0:
            self._ensure_overview()

    def _hide_login(self) -> None:
        self._login_action = None
        self.login_button.setVisible(False)

    def _check_login(self) -> None:
        """Ask the cluster whether this context still needs a sign-in; the
        button appears only when it does and the kubeconfig names an AWS
        profile."""
        context = self._context()
        if not context or self._login_checking:
            return
        self._login_checking = True

        def finished(_result: object = None) -> None:
            self._login_checking = False

        def show(result: tuple[bool, LoginAction | None]) -> None:
            finished()
            self._show_login(context, result)

        self._run_action(check_login, show, context, on_error=finished, quiet=True)

    def _show_login(
        self, context: str, result: tuple[bool, LoginAction | None]
    ) -> None:
        needs_login, action = result
        if context != self._context():
            return  # the person switched contexts while this was running
        self._login_action = action if needs_login else None
        self.login_button.setVisible(self._login_action is not None)
        if self._login_action is None:
            return
        profile = self._login_action.profile or "default"
        if self._login_action.interactive:
            self.login_button.setText(
                self.tr("Configure AWS credentials ({profile})").format(profile=profile)
            )
            self._set_status(
                lambda: self.tr(
                    "AWS credentials for profile {profile} are missing or invalid"
                ).format(profile=profile)
            )
        else:
            self.login_button.setText(
                self.tr("Sign in to AWS ({profile})").format(profile=profile)
            )
            self._set_status(
                lambda: self.tr("Not signed in to AWS (profile {profile})").format(
                    profile=profile
                )
            )

    def _sign_in(self) -> None:
        action = self._login_action
        if action is None:
            return
        logger.info("Sign-in requested for profile %s", action.profile or "default")
        self._run_action(
            run_login,
            lambda _result: self._signed_in(action),
            action,
            on_error=self._show_action_error,
        )

    def _signed_in(self, action: LoginAction) -> None:
        if action.interactive:
            # the keys are typed in the terminal that opened; nothing to wait for
            self._set_status(
                lambda: self.tr(
                    "Finish in the terminal that opened, then press Refresh."
                )
            )
            return
        self._hide_login()
        self.refresh()
        self._overview_context = None
        self._ensure_overview()

    def _ensure_workloads_overview(self) -> None:
        context = self._context()
        if context and context != self._workloads_overview_context:
            self.refresh_workloads_overview()

    def refresh_workloads_overview(self, *_args: object) -> None:
        context = self._context()
        if not context or self._workloads_overview_busy:
            return
        self._workloads_overview_busy = True
        self.workloads_ui.noticeLabel.setText(self.tr("Loading workloads..."))
        self._run_action(
            get_workloads_overview,
            lambda result: self._show_workloads_overview(context, result),
            context,
            on_error=self._show_workloads_overview_error,
        )

    def _show_workloads_overview_error(self, message: str) -> None:
        logger.info("Workloads overview failed: %s", first_line(message))
        self._workloads_overview_busy = False
        if is_auth_error(message):
            self._check_login()
        info = describe_error(message)
        label = self.workloads_ui.noticeLabel
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setText(self._error_html(info))
        label.setToolTip(info.details)

    def _show_workloads_overview(
        self, context: str, overview: WorkloadsOverview
    ) -> None:
        self._workloads_overview_busy = False
        if context != self._context():
            self._workloads_overview_context = None
            self.refresh_workloads_overview()
            return
        self._workloads_overview_context = context
        self._workloads_overview = overview
        logger.info(
            "Workloads overview loaded: %d kind(s), %d event(s)",
            len(overview.kinds),
            len(overview.events),
        )
        self._render_workloads_overview(overview)

    def _render_workloads_overview(self, overview: WorkloadsOverview) -> None:
        page = self.workloads_ui
        labels = {
            "pods": ("Pod", self.tr("Pods")),
            "deployments": ("Deployment", self.tr("Deployments")),
            "daemonsets": ("DaemonSet", self.tr("DaemonSets")),
            "statefulsets": ("StatefulSet", self.tr("StatefulSets")),
            "replicasets": ("ReplicaSet", self.tr("ReplicaSets")),
            "jobs": ("Job", self.tr("Jobs")),
            "cronjobs": ("CronJob", self.tr("CronJobs")),
        }
        for key, (kind, label) in labels.items():
            summary = overview.kinds.get(kind)
            link, bar = getattr(page, f"{key}Link"), getattr(page, f"{key}Bar")
            if summary is None:  # this user cannot read it
                link.setText(f"{label} (—)")
                bar.set_summary(0, 0, 0, 0)
            else:
                link.setText(f"{label} ({summary.total})")
                bar.set_summary(summary.ok, summary.warning, summary.bad, summary.total)
        self._render_events(overview)
        page.noticeLabel.setTextFormat(Qt.TextFormat.PlainText)
        page.noticeLabel.setToolTip("")
        page.noticeLabel.setText(
            self.tr("Could not read: {names}").format(
                names=", ".join(overview.unreadable)
            )
            if overview.unreadable
            else ""
        )

    def _render_events(self, overview: WorkloadsOverview) -> None:
        table = self.workloads_table
        table.setRowCount(len(overview.events))
        for row, event in enumerate(overview.events):
            values = (
                event.type,
                event.source,
                event.namespace,
                event.involved,
                event.message,
                str(event.count),
                event.age,
                event.last_seen,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setToolTip(event.message)
                item.setForeground(
                    QColor(
                        themed("#985415")
                        if event.type == "Warning"
                        else themed("#242a33")
                    )
                )
                table.setItem(row, column, item)

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

    @staticmethod
    def _error_html(info: ErrorInfo) -> str:
        color = themed("#a33d45")
        return (
            f'<span style="color:{color}"><b>{html.escape(info.title)}</b></span>'
            f"<br>{html.escape(info.hint)}"
        )

    def _show_overview_error(self, message: str) -> None:
        logger.info("Overview failed: %s", first_line(message))
        self._overview_busy = False
        if is_auth_error(message):
            self._check_login()
        info = describe_error(message)
        label = self.overview_ui.noticeLabel
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setText(self._error_html(info))
        label.setToolTip(info.details)

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
        logger.info(
            "Overview loaded: %d node(s), %s Pod(s)",
            len(overview.nodes),
            overview.pods_total,
        )
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
                item.setForeground(QColor(themed("#242a33")))
                if column == 1:
                    text_color, background = (
                        (themed("#176b58"), themed("#e5f4eb"))
                        if node.ready
                        else (themed("#a33d45"), themed("#fce9ea"))
                    )
                    item.setForeground(QColor(text_color))
                    item.setBackground(QColor(background))
                self.nodes_table.setItem(row, column, item)

        notices = list(overview.warnings)
        if overview.nodes and not overview.metrics_available:
            notices.append(self.tr("Real usage unavailable: metrics-server not found."))
        page.noticeLabel.setTextFormat(Qt.TextFormat.PlainText)
        page.noticeLabel.setToolTip("")
        page.noticeLabel.setText("  ·  ".join(notices))

    def _begin_loading(self, button: QPushButton | None, label: str) -> Callable:
        """Spin the button while work runs in the background; return a one-shot
        finisher.

        The cursor is left alone so the window never looks frozen.
        """
        if button is not None and self._spinner_button is None:
            self._spinner_button = button
            self._spinner_saved = (button.icon(), button.text())
            if button.text():  # icon-only buttons just spin
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
        if button is not None and button is self._spinner_button:
            self._spinner_timer.stop()
            if self._spinner_saved is not None:
                button.setIcon(self._spinner_saved[0])
                button.setText(self._spinner_saved[1])
            self._spinner_button = None
            self._spinner_saved = None

    def _tick_spinner(self) -> None:
        if self._spinner_button is None:
            return
        self._spinner_angle = (self._spinner_angle + 30) % 360
        primary = (
            self.refresh_button,
            self.overview_refresh_button,
            self.workloads_refresh_button,
        )
        color = "#ffffff" if self._spinner_button in primary else themed("#3220a0")
        self._spinner_button.setIcon(_spinner_icon(self._spinner_angle, color))

    def refresh(self, *_args: object) -> None:
        context = self._context()
        if not context or (self._worker is not None and self._worker.isRunning()):
            return
        namespace = self.namespace_combo.currentData() or None
        logger.info(
            "Refreshing %s in %s (namespace %s)",
            self._view,
            context,
            namespace or "all",
        )
        self.refresh_button.setEnabled(False)
        self.context_combo.setEnabled(False)
        self.namespace_combo.setEnabled(False)
        self._set_status(lambda: self.tr("Loading resources..."))
        view = self._view
        self._worker = RefreshWorker(context, namespace, view)
        end_loading = self._begin_loading(self.refresh_button, self.tr("Refreshing..."))
        self._worker.completed.connect(end_loading)
        self._worker.failed.connect(end_loading)
        self._worker.finished.connect(end_loading)
        show = self._show_pods if view == "pods" else self._show_workloads
        # an answer for a view the person has left is dropped; the list is
        # requested again for the new one when this request finishes
        self._worker.completed.connect(
            lambda namespaces, items: (
                show(namespaces, items) if view == self._view else None
            )
        )
        self._worker.failed.connect(self._show_error)
        self._worker.finished.connect(self._refresh_finished)
        self._worker.start()

    def _show_workloads(self, namespaces: list, workloads: list) -> None:
        logger.info(
            "Loaded %d workload(s) in %d namespace(s)", len(workloads), len(namespaces)
        )
        self._workloads = workloads
        self._apply_sort()
        self._fill_namespaces(namespaces)
        if self._view in WORKLOAD_VIEWS:
            self._render_workloads()

    def _show_pods(self, namespaces: list, pods: list) -> None:
        logger.info("Loaded %d Pod(s) in %d namespace(s)", len(pods), len(namespaces))
        self._pods = pods
        self._apply_sort()
        self._fill_namespaces(namespaces)
        if self._view == "pods":
            self._render_pods()

    def _fill_namespaces(self, namespaces: list) -> None:
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

    def _apply_sort(self) -> None:
        """Order self._workloads by the chosen header; no-op until one is
        clicked."""
        if self._sort is None:
            return
        column, order = self._sort
        descending = order == Qt.SortOrder.DescendingOrder
        if self._view == "pods":
            self._pods.sort(
                key=lambda pod: pod_sort_key(pod, column), reverse=descending
            )
        else:
            self._workloads.sort(
                key=lambda workload: workload_sort_key(workload, column),
                reverse=descending,
            )

    def _sort_rows(self, column: int) -> None:
        """Header click: sort ascending, click again to reverse."""
        if self._sort is not None and self._sort[0] == column:
            flipped = self._sort[1] == Qt.SortOrder.AscendingOrder
            order = (
                Qt.SortOrder.DescendingOrder if flipped else Qt.SortOrder.AscendingOrder
            )
        else:
            order = Qt.SortOrder.AscendingOrder
        self._sort = (column, order)
        selected = self._selected_row()
        self._apply_sort()
        header = self.table.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(column, order)
        self._render_rows()
        rows = self._current_rows()
        if selected in rows:
            self.table.selectRow(rows.index(selected))
        self._update_workload_actions()

    def _current_rows(self) -> list:
        return self._pods if self._view == "pods" else self._workloads

    def _selected_row(self) -> Workload | PodInfo | None:
        return (
            self._selected_pod() if self._view == "pods" else self._selected_workload()
        )

    def _render_rows(self) -> None:
        if self._view == "pods":
            self._render_pods()
        else:
            self._render_workloads()

    def _phase_label(self, phase: str) -> str:
        labels = {
            "Running": self.tr("Running"),
            "Pending": self.tr("Pending"),
            "Succeeded": self.tr("Succeeded"),
            "Failed": self.tr("Failed"),
            "Unknown": self.tr("Unknown"),
        }
        return labels.get(phase, phase)

    def _render_pods(self) -> None:
        pods = self._pods
        colors = {
            "Running": (themed("#176b58"), themed("#e5f4eb")),
            "Pending": (themed("#985415"), themed("#fff2de")),
            "Succeeded": (themed("#505963"), themed("#eff1f3")),
            "Failed": (themed("#a33d45"), themed("#fce9ea")),
        }
        tints = {
            "problem": QColor(themed("#fbe4e4")),
            "young": QColor(themed("#e2f5e8")),
        }
        self.table.setRowCount(len(pods))
        for row_index, pod in enumerate(pods):
            tint = tints.get(pod_highlight(pod) or "")
            values = (
                pod.namespace,
                str(len(pod.containers)),
                pod.name,
                f"{pod.ready}/{pod.total}",
                self._phase_label(pod.phase),
                format_cpu(pod.cpu),
                format_memory(pod.memory),
                str(pod.restarts),
                pod.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor(themed("#242a33")))
                if tint is not None:
                    item.setBackground(tint)
                if column == 4:
                    foreground, background = colors.get(
                        pod.phase, (themed("#a33d45"), themed("#fce9ea"))
                    )
                    item.setForeground(QColor(foreground))
                    item.setBackground(QColor(background))
                self.table.setItem(row_index, column, item)
        self._filter_rows()
        self._set_status(
            lambda: self.tr("{count} Pods in {namespaces} namespaces").format(
                count=len(pods), namespaces=len(self._namespaces)
            )
        )

    def _render_workloads(self) -> None:
        workloads = self._workloads
        statuses = {
            "Healthy": self.tr("Healthy"),
            "Degraded": self.tr("Degraded"),
            "Unavailable": self.tr("Unavailable"),
            "Scaled to zero": self.tr("Scaled to zero"),
            "Complete": self.tr("Complete"),
            "Failed": self.tr("Failed"),
            "Pending": self.tr("Pending"),
            "Suspended": self.tr("Suspended"),
            "Active": self.tr("Active"),
            "Scheduled": self.tr("Scheduled"),
            "Running": self.tr("Running"),
        }
        self.table.setRowCount(len(workloads))
        for row_index, workload in enumerate(workloads):
            values = (
                workload.namespace,
                workload.kind,
                workload.name,
                workload.schedule or ""
                if workload.kind == "CronJob"
                else f"{workload.ready}/{workload.desired}",
                statuses[workload.status],
                format_cpu(workload.cpu),
                format_memory(workload.memory),
                str(workload.restarts),
                workload.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor(themed("#242a33")))
                if column == 4:
                    good = (themed("#176b58"), themed("#e5f4eb"))
                    warning = (themed("#985415"), themed("#fff2de"))
                    bad = (themed("#a33d45"), themed("#fce9ea"))
                    muted = (themed("#505963"), themed("#eff1f3"))
                    color = {
                        "Healthy": good,
                        "Complete": good,
                        "Running": good,
                        "Active": good,
                        "Degraded": warning,
                        "Pending": warning,
                        "Unavailable": bad,
                        "Failed": bad,
                        "Scaled to zero": muted,
                        "Suspended": muted,
                        "Scheduled": muted,
                    }[workload.status]
                    item.setForeground(QColor(color[0]))
                    item.setBackground(QColor(color[1]))
                self.table.setItem(row_index, column, item)
        self._filter_rows()
        summaries = {
            "deployments": lambda: self.tr(
                "{count} Deployments in {namespaces} namespaces"
            ),
            "statefulsets": lambda: self.tr(
                "{count} StatefulSets in {namespaces} namespaces"
            ),
            "jobs": lambda: self.tr("{count} Jobs in {namespaces} namespaces"),
            "cronjobs": lambda: self.tr("{count} CronJobs in {namespaces} namespaces"),
        }
        summary = summaries[self._view]
        self._set_status(
            lambda: summary().format(
                count=len(workloads), namespaces=len(self._namespaces)
            )
        )

    def _filter_rows(self, *_args: object) -> None:
        query = self.search_input.text().strip().casefold()
        visible_rows = 0
        rows = self._current_rows()
        for row_index, row in enumerate(rows):
            kind = row.kind if isinstance(row, Workload) else "Pod"
            matches = query in f"{row.namespace} {kind} {row.name}".casefold()
            self.table.setRowHidden(row_index, not matches)
            visible_rows += matches
        self._update_workload_actions()
        template = {
            "pods": self.tr("{visible} of {total} Pods"),
            "deployments": self.tr("{visible} of {total} Deployments"),
            "statefulsets": self.tr("{visible} of {total} StatefulSets"),
            "jobs": self.tr("{visible} of {total} Jobs"),
            "cronjobs": self.tr("{visible} of {total} CronJobs"),
        }[self._view]
        self.summary_label.setText(
            template.format(visible=visible_rows, total=len(rows))
        )

    def _selected_workload(self) -> Workload | None:
        row = self.table.currentRow()
        if 0 <= row < len(self._workloads) and not self.table.isRowHidden(row):
            return self._workloads[row]
        return None

    def _selected_pod(self) -> PodInfo | None:
        row = self.table.currentRow()
        if 0 <= row < len(self._pods) and not self.table.isRowHidden(row):
            return self._pods[row]
        return None

    def _update_workload_actions(self) -> None:
        enabled = self._selected_row() is not None
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
        logger.debug("Action: %s", getattr(operation, "__name__", operation))
        worker = ActionWorker(operation, arguments)
        self._action_workers.append(worker)
        if not quiet:  # background refreshes must not flash a spinner
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
            QApplication.quit()

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

    def _view_details(self) -> None:
        pod = self._selected_pod() if self._view == "pods" else None
        if pod is None:
            self._view_workload_details()
            return
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

    def _view_logs(self) -> None:
        pod = self._selected_pod() if self._view == "pods" else None
        if pod is None:
            self._view_workload_logs()
        else:
            self._choose_container_for_logs(self._context(), pod)

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
        table.horizontalHeader().setStretchLastSection(True)
        for column, width in ((0, 320), (1, 90), (2, 120), (3, 110)):
            table.setColumnWidth(column, width)
        for row, pod in enumerate(pods):
            values = (
                pod.name,
                f"{pod.ready}/{pod.total}",
                self._phase_label(pod.phase),
                str(len(pod.containers)),
                pod.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor(themed("#242a33")))
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
        tab.ui.refreshButton.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        )
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
        form.languageCombo.addItem(self.tr("Automatic"), "auto")
        for code, name in LANGUAGES.items():
            form.languageCombo.addItem(name, code)
        form.languageCombo.setCurrentIndex(
            max(form.languageCombo.findData(self.settings.language), 0)
        )
        self._fill_theme_combo(self.settings.theme)
        form.rememberCheck.setChecked(self.settings.remember_last_context)
        form.debugCheck.setChecked(self.settings.debug_logging)
        form.debugHint.setText(
            self.tr(
                "Off by default. When on, KubeScope writes what it does, "
                "never Pod logs or resource contents, to {path}. Read it before "
                "sharing: it includes context names."
            ).format(path=log_file())
        )

        aliases = self.settings.context_aliases
        table = form.contextsTable
        table.setRowCount(len(self._contexts))
        # Real context names (often long ARNs) must stay readable: size the first
        # column to its content and let the editable name take the rest.
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        for row, context in enumerate(self._contexts):
            name_item = QTableWidgetItem(context)
            name_item.setToolTip(context)
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(row, 0, name_item)
            table.setItem(row, 1, QTableWidgetItem(aliases.get(context, "")))
        table.resizeColumnToContents(0)  # a starting width; the user can drag it
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

    def _fill_theme_combo(self, selected: str) -> None:
        """List the built-in and custom themes, choosing `selected`."""
        combo = self.settings_ui.themeCombo
        combo.blockSignals(True)
        combo.clear()
        names = {"light": self.tr("Light"), "dark": self.tr("Dark")}
        for theme in available_themes():
            combo.addItem(names.get(theme.id, theme.name), theme.id)
        combo.setCurrentIndex(max(combo.findData(selected), 0))
        combo.blockSignals(False)
        self._update_theme_buttons()

    def _selected_theme(self) -> Theme:
        theme_id = self.settings_ui.themeCombo.currentData()
        return next(t for t in available_themes() if t.id == theme_id)

    def _update_theme_buttons(self) -> None:
        # the built-in themes are fixed; copy one with New theme to change it
        self.settings_ui.editThemeButton.setEnabled(not self._selected_theme().builtin)

    def _edit_theme_dialog(self, theme: Theme, *, new: bool) -> Theme | None:
        editor = ThemeEditor(
            self,
            name=self.tr("My theme") if new else theme.name,
            base=theme.base,
            tokens=theme_tokens(theme),
            new=new,
        )
        if editor.exec() != QDialog.DialogCode.Accepted:
            return None
        name, base, tokens = editor.values()
        return save_custom_theme(name, base, tokens, None if new else theme.id)

    def _new_theme(self) -> None:
        """Start a new theme from the selected one."""
        saved = self._edit_theme_dialog(self._selected_theme(), new=True)
        if saved is not None:
            logger.info("Created theme %s", saved.id)
            self._fill_theme_combo(saved.id)

    def _edit_theme(self) -> None:
        theme = self._selected_theme()
        saved = self._edit_theme_dialog(theme, new=False)
        if saved is not None:
            logger.info("Edited theme %s", saved.id)
            self._fill_theme_combo(saved.id)
            if self.settings.theme == saved.id:
                self._apply_theme()  # the theme in use changed: show it now

    def _open_themes_folder(self) -> None:
        themes_directory().mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(themes_directory())))

    def _open_log_folder(self) -> None:
        directory = log_directory()
        directory.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(directory)))

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
        previous_theme = self.settings.theme
        self.settings.language = form.languageCombo.currentData()
        self.settings.theme = form.themeCombo.currentData()
        self.settings.remember_last_context = form.rememberCheck.isChecked()
        if self.settings.remember_last_context:
            self.settings.last_context = self._context()
        was_debugging = self.settings.debug_logging
        self.settings.debug_logging = form.debugCheck.isChecked()
        self._save_settings()
        if self.settings.debug_logging != was_debugging:
            configure_logging(to_file=self.settings.debug_logging)
            logger.info("Debug mode %s", "on" if self.settings.debug_logging else "off")
        logger.info("Settings saved")
        self._fill_contexts(self._context())
        if self.settings.language != previous_language:
            apply_language(self.settings.language)
        if self.settings.theme != previous_theme:
            logger.info("Theme changed to %s", self.settings.theme)
            self._apply_theme()
        form.noticeLabel.setText(self.tr("Settings saved."))

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange and hasattr(self, "ui"):
            self._retranslate()
        super().changeEvent(event)

    def _retranslate(self) -> None:
        """Re-apply every visible text after the translator changed."""
        self.ui.retranslateUi(self)
        self._show_version()
        self.overview_ui.retranslateUi(self.ui.overviewHost)
        self.settings_ui.retranslateUi(self.ui.settingsHost)
        self.workloads_ui.retranslateUi(self.ui.workloadsOverviewHost)
        if self._workloads_overview is not None:
            self._render_workloads_overview(self._workloads_overview)
        if self.pages.currentIndex() == 2:
            self._load_settings_form()
        self._apply_page_titles()
        if self.namespace_combo.count():
            self.namespace_combo.setItemText(0, self.tr("All namespaces"))
        self._apply_view_columns()
        self._render_rows()
        if self._overview is not None:
            self._render_overview(self._overview)
        else:
            self._reset_overview()
        if self._status_message is not None:
            self.status_label.setText(self._status_message())

    def _show_action_error(self, message: str) -> None:
        if self._close_when_worker_stops:
            return  # the window is closing; the cancelled request is no news
        info = describe_error(message)
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(self.tr("Query failed"))
        box.setText(info.title)
        box.setInformativeText(info.hint)
        box.setDetailedText(info.details)
        box.exec()

    def _show_error(self, message: str) -> None:
        logger.info("Refresh failed: %s", first_line(message))
        if is_auth_error(message):
            self._check_login()
        self._workloads = []
        self._pods = []
        self._set_status(lambda: self._error_line(message))
        self.status_label.setToolTip(describe_error(message).details)
        self.table.setRowCount(0)
        self._filter_rows()

    def _refresh_finished(self) -> None:
        self.refresh_button.setEnabled(True)
        self.context_combo.setEnabled(True)
        self.namespace_combo.setEnabled(True)
        self._finish_deferred_close()
        if self._worker is not None and self._worker.view != self._view:
            QTimer.singleShot(0, self.refresh)  # the view changed mid-request

    def closeEvent(self, event: QCloseEvent) -> None:
        refresh_running = self._worker is not None and self._worker.isRunning()
        actions_running = any(worker.isRunning() for worker in self._action_workers)
        if refresh_running or actions_running:
            logger.info("Closing while requests are running; stopping them")
            # Stop kubectl and the AWS CLI so the workers return at once, hide the
            # window so closing feels instant, and quit when the last one is done.
            self._close_when_worker_stops = True
            QApplication.setQuitOnLastWindowClosed(False)
            cancel_running()
            self.hide()
            event.ignore()
            return
        super().closeEvent(event)
