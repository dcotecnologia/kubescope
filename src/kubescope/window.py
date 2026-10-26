import dataclasses
import datetime
import html
import logging
import math
import re
import tempfile
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import (
    QByteArray,
    QCoreApplication,
    QEasingCurve,
    QEvent,
    QMimeData,
    QObject,
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
    QCursor,
    QDesktopServices,
    QDrag,
    QIcon,
    QKeySequence,
    QMouseEvent,
    QPainter,
    QPen,
    QPixmap,
    QPolygonF,
    QShortcut,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QCompleter,
    QDialog,
    QFileDialog,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QSystemTrayIcon,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from kubescope import COMPANY_URL, LICENSE_URL, PROJECT_URL, SPONSOR_URL, __version__
from kubescope.cluster import (
    ClusterError,
    LoginAction,
    cancel_running,
    check_login,
    forget_clients,
    get_cluster_info,
    get_cluster_overview,
    get_pod_logs,
    get_pod_usage,
    get_pods,
    get_resource_details,
    get_resources,
    get_usage,
    get_workload_pods,
    get_workloads,
    get_workloads_overview,
    is_eks_context,
    list_contexts,
    parse_command,
    retry_sign_in,
    run_login,
)
from kubescope.cluster import (
    configure as configure_cluster,
)
from kubescope.dialogs.changelog_dialog import ChangelogDialog
from kubescope.dialogs.theme_editor import ThemeEditor
from kubescope.dialogs.update_dialog import UpdateDialog
from kubescope.i18n import apply_language, language_choices
from kubescope.models import (
    EKS_VIEWS,
    RESOURCE_VIEWS,
    WORKLOAD_VIEWS,
    ClusterInfo,
    ClusterOverview,
    ClusterResource,
    PodInfo,
    Workload,
    WorkloadsOverview,
    event_link,
    format_bytes,
    format_cores,
    format_cpu,
    format_memory,
    pod_highlight,
    pod_sort_key,
    resource_sort_key,
    workload_sort_key,
)
from kubescope.settings import Settings, log_directory
from kubescope.theme import (
    DEFAULT_THEME,
    Theme,
    active_theme,
    apply_theme,
    available_themes,
    can_delete_theme,
    delete_custom_theme,
    save_custom_theme,
    theme_tokens,
    themed,
    themed_stylesheet,
    themes_directory,
)
from kubescope.ui.ui_main_window import Ui_MainWindow
from kubescope.ui.ui_overview_page import Ui_OverviewPage
from kubescope.ui.ui_pods_dialog import Ui_PodsDialog
from kubescope.ui.ui_settings_page import Ui_SettingsPage
from kubescope.ui.ui_viewer_page import Ui_ViewerPage
from kubescope.ui.ui_workloads_overview_page import Ui_WorkloadsOverviewPage
from kubescope.utils.diagnostics import configure_logging, log_file
from kubescope.utils.errors import (
    ErrorInfo,
    describe_error,
    first_line,
    forbidden_action,
    is_auth_error,
    is_forbidden,
)
from kubescope.utils.fonts import code_font
from kubescope.utils.json_view import restyle
from kubescope.utils.selfupdate import detect_install, restart
from kubescope.utils.updates import Release, UpdateCheck, check_for_update
from kubescope.views.container_states import (
    LINK_ROLE,
    STATES_ROLE,
    TIPS_ROLE,
    ContainerStatesDelegate,
)
from kubescope.views.detail_tab import USAGE_REFRESH_MS, DetailTab
from kubescope.views.log_tab import LOG_REFRESH_MS, LogTab
from kubescope.views.search_bar import compile_query, switch_button
from kubescope.views.widgets import TabScrollArea
from kubescope.views.window_frame import WindowFrame
from kubescope.writes import (
    MAX_REPLICAS,
    delete_pod,
    evict_pod,
    forward_commands,
    restart_deployment,
    scale_deployment,
    service_ports,
    shell_commands,
)

# The buttons of the write mode that each list view shows.
WRITE_VIEWS = {
    "pods": ("shell", "evict", "delete"),
    "deployments": ("scale", "reload"),
    "services": ("forward",),
}

logger = logging.getLogger(__name__)

PIN_MIME = "application/x-kubescope-pin"  # what a dragged pinned tab carries
VIEWER_MIME = "application/x-kubescope-viewer"  # the same, for a Details/Logs tab
DESIGNED_COLUMNS = 6  # the columns the table has in main_window.ui
LIST_DEBOUNCE_MS = 150
LIST_REFRESH_MS = 5_000  # the list on screen is read again this often
LIST_REFRESH_MAX_MS = 60_000  # ... and this rarely while the cluster keeps failing
UPDATE_RECHECK_MS = 60 * 60 * 1000  # look for a new version again every hour
UPDATE_SEARCH_MS = 5000  # an update check shows as searching for at least this long
UPDATE_NOTICE_MS = 4000  # how long "Up to date" stays next to the icon

NOTICES_PATH = Path(__file__).resolve().parent / "assets" / "THIRD_PARTY_NOTICES.txt"
LOGO_PATH = Path(__file__).resolve().parent / "assets" / "icon.png"

# Overview rows that open a list when clicked, and the list each opens.
WORKLOAD_LINKS = {
    "pods": "pods",
    "deployments": "deployments",
    "statefulsets": "statefulsets",
    "daemonsets": "daemonsets",
    "replicasets": "replicasets",
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


def _gear_icon() -> QIcon:
    """A white gear for the top bar, which is dark in every theme."""
    scale, teeth = 3, 8  # drawn three times larger so the edges stay smooth
    pixmap = QPixmap(18 * scale, 18 * scale)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.translate(9 * scale, 9 * scale)
    painter.scale(scale, scale)
    outline = QPolygonF()
    step = 360 / teeth
    for tooth in range(teeth):
        # a tooth: wide at its root, narrower at its tip, then the rim to the next
        for offset, radius in (
            (-0.30, 6.6),
            (-0.17, 8.6),
            (0.17, 8.6),
            (0.30, 6.6),
            (0.5, 6.6),
        ):
            angle = math.radians((tooth + offset) * step - 90)
            outline.append(QPointF(radius * math.cos(angle), radius * math.sin(angle)))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(themed("#ffffff", text=True)))
    painter.drawPolygon(outline)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
    painter.drawEllipse(QPointF(0, 0), 2.7, 2.7)
    painter.end()
    pixmap.setDevicePixelRatio(scale)
    icon = QIcon()
    icon.addPixmap(pixmap, QIcon.Mode.Normal)
    icon.addPixmap(pixmap, QIcon.Mode.Disabled)
    return icon


def _pair(color: str) -> tuple[str, str]:
    return color, color


def _nav_icon(shape: str, colors: tuple[str, str] | None = None) -> QIcon:
    """A line icon in the theme's colors.

    By default it is muted at rest and the accent while its page is
    open, as in the side menu; `colors` gives the resting and the
    checked color for a button.
    """
    scale = 3  # drawn three times larger so the edges stay smooth
    icon = QIcon()
    off, on = colors or (themed("#4f5966"), themed("#3220a0"))
    for state, color in ((QIcon.State.Off, off), (QIcon.State.On, on)):
        pixmap = QPixmap(18 * scale, 18 * scale)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.scale(scale, scale)
        pen = QPen(QColor(color), 1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if shape == "overview":  # a screen on its stand
            painter.drawRoundedRect(QRectF(2.5, 3, 13, 9), 1.5, 1.5)
            painter.drawLine(QPointF(9, 12), QPointF(9, 15))
            painter.drawLine(QPointF(6, 15), QPointF(12, 15))
        elif shape == "workloads":  # four tiles
            for x, y in ((3, 3), (10, 3), (3, 10), (10, 10)):
                painter.drawRoundedRect(QRectF(x, y, 5, 5), 1.2, 1.2)
        elif shape == "details":  # an "i" in a circle
            painter.drawEllipse(QPointF(9, 9), 6.5, 6.5)
            painter.drawLine(QPointF(9, 8.3), QPointF(9, 12.3))
            painter.drawPoint(QPointF(9, 5.6))
        elif shape == "document":  # a page with lines of text
            painter.drawRoundedRect(QRectF(3.8, 2.5, 10.4, 13), 1.5, 1.5)
            for y in (6.3, 9, 11.7):
                painter.drawLine(QPointF(6.4, y), QPointF(11.6, y))
        elif shape == "pods":  # stacked layers
            painter.drawPolygon(
                QPolygonF(
                    [
                        QPointF(2.5, 6.5),
                        QPointF(9, 3),
                        QPointF(15.5, 6.5),
                        QPointF(9, 10),
                    ]
                )
            )
            painter.drawPolyline(
                QPolygonF([QPointF(2.5, 9.7), QPointF(9, 13.2), QPointF(15.5, 9.7)])
            )
            painter.drawPolyline(
                QPolygonF([QPointF(2.5, 12.9), QPointF(9, 16.4), QPointF(15.5, 12.9)])
            )
        elif shape == "reload":  # an arrow going round
            painter.drawArc(QRectF(3.5, 3.5, 11, 11), 40 * 16, 280 * 16)
            painter.drawPolyline(
                QPolygonF([QPointF(11.8, 3.1), QPointF(14.6, 5.2), QPointF(11.6, 7.2)])
            )
        elif shape == "save":  # an arrow down into a tray
            painter.drawPolyline(
                QPolygonF(
                    [
                        QPointF(3, 11.5),
                        QPointF(3, 15),
                        QPointF(15, 15),
                        QPointF(15, 11.5),
                    ]
                )
            )
            painter.drawLine(QPointF(9, 2.5), QPointF(9, 11))
            painter.drawPolyline(
                QPolygonF([QPointF(5.5, 7.5), QPointF(9, 11), QPointF(12.5, 7.5)])
            )
        elif shape == "nodegroups":  # two stacked servers
            painter.drawRoundedRect(QRectF(3, 3, 12, 5), 1.2, 1.2)
            painter.drawRoundedRect(QRectF(3, 10, 12, 5), 1.2, 1.2)
            painter.drawPoint(QPointF(5.8, 5.5))
            painter.drawPoint(QPointF(5.8, 12.5))
        elif shape == "config":  # two sliders
            painter.drawLine(QPointF(3, 6), QPointF(15, 6))
            painter.drawLine(QPointF(3, 12), QPointF(15, 12))
            painter.setBrush(QColor(color))
            painter.drawEllipse(QPointF(6.5, 6), 1.8, 1.8)
            painter.drawEllipse(QPointF(11.5, 12), 1.8, 1.8)
        elif shape == "shell":  # a terminal window with a prompt
            painter.drawRoundedRect(QRectF(2.5, 3.5, 13, 11), 1.5, 1.5)
            painter.drawPolyline(
                QPolygonF([QPointF(5.5, 7), QPointF(8, 9), QPointF(5.5, 11)])
            )
            painter.drawLine(QPointF(9.5, 11.2), QPointF(12.5, 11.2))
        elif shape == "evict":  # an arrow leaving a box
            painter.drawPolyline(
                QPolygonF([QPointF(8, 3.5), QPointF(3, 3.5), QPointF(3, 14.5)])
            )
            painter.drawPolyline(QPolygonF([QPointF(3, 14.5), QPointF(8, 14.5)]))
            painter.drawLine(QPointF(7, 9), QPointF(15, 9))
            painter.drawPolyline(
                QPolygonF([QPointF(12, 6), QPointF(15, 9), QPointF(12, 12)])
            )
        elif shape == "delete":  # a trash can
            painter.drawLine(QPointF(3, 5), QPointF(15, 5))
            painter.drawPolyline(
                QPolygonF(
                    [QPointF(7, 5), QPointF(7, 3), QPointF(11, 3), QPointF(11, 5)]
                )
            )
            painter.drawPolyline(
                QPolygonF(
                    [
                        QPointF(4.5, 5),
                        QPointF(5.3, 15),
                        QPointF(12.7, 15),
                        QPointF(13.5, 5),
                    ]
                )
            )
        elif shape == "forward":  # an arrow into a wall
            painter.drawLine(QPointF(3, 9), QPointF(12, 9))
            painter.drawPolyline(
                QPolygonF([QPointF(9, 6), QPointF(12, 9), QPointF(9, 12)])
            )
            painter.drawLine(QPointF(15, 4), QPointF(15, 14))
        elif shape == "scale":  # arrows growing apart
            painter.drawLine(QPointF(9, 3), QPointF(9, 15))
            painter.drawPolyline(
                QPolygonF([QPointF(6, 6), QPointF(9, 3), QPointF(12, 6)])
            )
            painter.drawPolyline(
                QPolygonF([QPointF(6, 12), QPointF(9, 15), QPointF(12, 12)])
            )
        else:  # network: three linked nodes
            top, left, right = QPointF(9, 3.5), QPointF(3.5, 14), QPointF(14.5, 14)
            painter.drawLine(top, left)
            painter.drawLine(top, right)
            painter.drawLine(left, right)
            painter.setBrush(QColor(color))
            for node in (top, left, right):
                painter.drawEllipse(node, 2, 2)
        painter.end()
        pixmap.setDevicePixelRatio(scale)
        icon.addPixmap(pixmap, QIcon.Mode.Normal, state)
        icon.addPixmap(pixmap, QIcon.Mode.Active, state)
    return icon


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


def _update_icon(state: str, opacity: float = 1.0) -> QIcon:
    """The footer icon of the update check: a circle with a check when up to
    date, an exclamation mark when the check failed, an arrow up in the accent
    color when there is a new version, and the reload arrow before any
    check."""
    muted = themed("#6b7380", text=True)
    if state == "idle":
        return _nav_icon("reload", (muted, muted))
    scale = 3  # drawn three times larger so the edges stay smooth
    pixmap = QPixmap(18 * scale, 18 * scale)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(scale, scale)
    color = QColor(themed("#3220a0") if state == "available" else muted)
    color.setAlphaF(opacity)
    pen = QPen(color, 1.6)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawEllipse(QPointF(9, 9), 6.5, 6.5)
    if state == "current":
        painter.drawPolyline(
            QPolygonF([QPointF(5.9, 9.2), QPointF(8, 11.3), QPointF(12.1, 6.9)])
        )
    elif state == "failed":
        painter.drawLine(QPointF(9, 5.6), QPointF(9, 9.8))
        painter.drawPoint(QPointF(9, 12.3))
    else:  # available
        painter.drawLine(QPointF(9, 12.2), QPointF(9, 6))
        painter.drawPolyline(
            QPolygonF([QPointF(6.2, 8.6), QPointF(9, 5.8), QPointF(11.8, 8.6)])
        )
    painter.end()
    pixmap.setDevicePixelRatio(scale)
    icon = QIcon()
    icon.addPixmap(pixmap, QIcon.Mode.Normal)
    icon.addPixmap(pixmap, QIcon.Mode.Active)
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
        self.key: tuple[str, str | None, str] | None = None

    def _usage(self, kind: str) -> dict:
        try:
            return (
                {}  # a CronJob's Pods belong to the Jobs it creates
                if kind == "CronJob"
                else get_usage(self.context, self.namespace)
            )
        except ClusterError as error:  # metrics-server is optional
            logger.debug("No Pod usage for %s: %s", self.context, error)
        except Exception:
            logger.exception("Could not load Pod usage for %s", self.context)
        return {}

    def run(self) -> None:
        try:
            if self.view == "pods":
                namespaces, items = get_pods(self.context, self.namespace)
            elif self.view in RESOURCE_VIEWS:
                namespaces, items = get_resources(
                    self.context, self.namespace, RESOURCE_VIEWS[self.view]
                )
            else:
                kind = WORKLOAD_VIEWS[self.view]
                with ThreadPoolExecutor(max_workers=1) as pool:
                    # the Pods are read while the workloads are
                    usage_call = pool.submit(self._usage, kind)
                    namespaces, items = get_workloads(
                        self.context, self.namespace, (kind,)
                    )
                    usage = usage_call.result()
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
        except ClusterError as error:  # expected: the window explains it
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
        except ClusterError as error:  # expected: the window explains it
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
        # the last overview of each context, shown at once when it is chosen again
        self._overviews: dict[str, ClusterOverview] = {}
        self._workloads_overviews: dict[str, WorkloadsOverview] = {}
        self._status_message: Callable[[], str] | None = None
        self._workers: dict[str, RefreshWorker] = {}  # one request per list
        self._retired: list[RefreshWorker] = []  # cancelled, still winding down
        # the last answer per (context, namespace, list), shown at once while the
        # list is requested again
        self._answers: dict[tuple[str, str | None, str], tuple[list, list]] = {}
        # clicking through the lists quickly asks for the last one only
        self._list_timer = QTimer(self)
        self._list_timer.setSingleShot(True)
        self._list_timer.setInterval(LIST_DEBOUNCE_MS)
        self._list_timer.timeout.connect(self.refresh)
        # the list on screen follows the cluster: Pods come and go on their own
        self._live_timer = QTimer(self)
        self._live_timer.setInterval(LIST_REFRESH_MS)
        self._live_timer.timeout.connect(self._refresh_live)
        self._live_timer.start()
        self._action_workers: list[ActionWorker] = []
        self._close_when_worker_stops = False
        self._workloads: list[Workload] = []
        self._pods: list[PodInfo] = []
        self._resources: list[ClusterResource] = []
        self._view = "deployments"  # which list the shared table shows
        self._update_state = "idle"  # idle, checking, current, available or failed
        self._cluster_info: ClusterInfo | None = None
        self._eks_context: str | None = None  # the open context, when it is EKS
        self._update_release: Release | None = None
        self._update_phase = 0  # frame of the icon animation
        self._update_timer = QTimer(self)
        self._update_timer.setInterval(60)
        self._update_timer.timeout.connect(self._tick_update)
        self._update_started = 0.0
        self._update_result = UpdateCheck("current")
        # a check shows as searching for a while, so it reads as a real look
        self._update_delay = QTimer(self)
        self._update_delay.setSingleShot(True)
        self._update_delay.timeout.connect(self._update_checked)
        self._update_recheck = QTimer(self)
        self._update_recheck.setInterval(UPDATE_RECHECK_MS)
        self._update_recheck.timeout.connect(self._recheck_updates)
        self._update_recheck.start()
        self._rechecking = False  # an hourly check says nothing when up to date
        self._update_notice_timer = QTimer(self)  # hides "Up to date" again
        self._update_notice_timer.setSingleShot(True)
        self._update_notice_timer.setInterval(UPDATE_NOTICE_MS)
        self._apply_cluster_settings()
        self._build_ui()
        self._restore_geometry()
        self._load_contexts()

    def _build_ui(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ui = self.ui
        self.context_combo = ui.contextCombo
        self.namespace_combo = ui.namespaceCombo
        self.search_input = ui.searchInput
        # the switches of the search: Aa matches the case, .* reads a regular expression
        self.search_case_button = switch_button("Aa", self.tr("Match case"))
        self.search_regex_button = switch_button(".*", self.tr("Regular expression"))
        filters = cast(QHBoxLayout, ui.filtersBar.layout())
        at = filters.indexOf(ui.searchInput) + 1
        for button in (self.search_regex_button, self.search_case_button):
            filters.insertWidget(at, button)
        self.refresh_button = ui.refreshButton
        self.summary_label = ui.summaryLabel
        self.pods_button = ui.podsButton
        self.details_button = ui.detailsButton
        self.logs_button = ui.logsButton
        # the write mode's buttons; each view shows its own, and only in that mode
        self.write_buttons: dict[str, QPushButton] = {}
        for shape in ("shell", "evict", "delete", "scale", "reload", "forward"):
            button = QPushButton()
            button.setProperty("variant", "secondary")
            button.setEnabled(False)
            button.clicked.connect(partial(self._write_button_clicked, shape))
            ui.summaryRow.addWidget(button)
            self.write_buttons[shape] = button
        self.table = ui.workloadTable
        states_delegate = ContainerStatesDelegate(self.table)
        # the containers of a Pod and the replicas of a workload, in READY
        self.table.setItemDelegateForColumn(3, states_delegate)
        self.status_label = ui.statusLabel
        self.login_button = ui.loginButton
        ui.topLogo.setPixmap(QPixmap(str(LOGO_PATH)))
        self._frame = WindowFrame(
            self,
            ui.topBar,
            ui.windowControls,
            ui.minimizeButton,
            ui.maximizeButton,
            ui.windowCloseButton,
        )
        self._frame.set_custom(not self.settings.system_title_bar)
        self.no_contexts_banner = ui.noContextsBanner
        self.permission_banner = ui.permissionBanner
        ui.permissionDismiss.clicked.connect(self._hide_permission_banner)
        self.pages = ui.pages
        self.nav_overview = ui.navOverview
        self.nav_workloads = ui.navWorkloads
        self.submenu = ui.workloadsSubmenu
        self.nav_workloads_overview = ui.navWorkloadsOverview
        self.nav_pods = ui.navPods
        self.nav_deployments = ui.navDeployments
        self.nav_statefulsets = ui.navStatefulSets
        self.nav_daemonsets = ui.navDaemonSets
        self.nav_replicasets = ui.navReplicaSets
        self.nav_replicationcontrollers = ui.navReplicationControllers
        self.nav_jobs = ui.navJobs
        self.nav_cronjobs = ui.navCronJobs
        self.nav_network = ui.navNetwork
        self.network_submenu = ui.networkSubmenu
        self.nav_config = ui.navConfig
        self._pinned_buttons: list[QPushButton] = []
        self._tray: QSystemTrayIcon | None = None
        self._quitting = False
        self._name_fitted: set[str] = set()  # the lists whose NAME column was fitted
        self._viewer_contexts: dict[QWidget | None, str] = {}  # the context of each tab
        # widget -> (what the gesture does, the list it is about)
        self._pin_gestures: dict[QObject, tuple[str, str]] = {}
        # every tab shown in the top bar, left to right, parallel to the buttons:
        # ("pin", the list) or ("viewer", the Details/Logs widget)
        self._bar_items: list[tuple[str, Any]] = []
        self._bar_order: list[tuple[str, Any]] = []  # the order the person chose
        self._drag_start: QPoint | None = None
        # more tabs than room: the bar scrolls instead of cutting the first ones
        self.pinned_scroll = TabScrollArea(ui.topBar)
        position = ui.topLayout.indexOf(ui.pinnedBar)
        ui.topLayout.removeWidget(ui.pinnedBar)
        self.pinned_scroll.setWidget(ui.pinnedBar)
        ui.topLayout.insertWidget(position, self.pinned_scroll)
        self.pinned_scroll.setVisible(False)
        ui.pinnedBar.setAcceptDrops(True)  # a pinned tab dropped here moves
        ui.pinnedBar.installEventFilter(self)
        self._drop_marker = QFrame(ui.pinnedBar)  # the line a dragged tab aims at
        self._drop_marker.setObjectName("dropMarker")
        self._drop_marker.hide()
        self.config_submenu = ui.configSubmenu
        # the two overview pages pin like a list does, by the page they show
        self._nav_pages = {
            "cluster-overview": (self.nav_overview, 0),
            "workloads-overview": (self.nav_workloads_overview, 4),
        }
        self._nav_views = {
            "pods": self.nav_pods,
            "deployments": self.nav_deployments,
            "statefulsets": self.nav_statefulsets,
            "daemonsets": self.nav_daemonsets,
            "replicasets": self.nav_replicasets,
            "replicationcontrollers": self.nav_replicationcontrollers,
            "jobs": self.nav_jobs,
            "cronjobs": self.nav_cronjobs,
            "services": ui.navServices,
            "endpointslices": ui.navEndpointSlices,
            "endpoints": ui.navEndpoints,
            "ingresses": ui.navIngresses,
            "ingressclasses": ui.navIngressClasses,
            "networkpolicies": ui.navNetworkPolicies,
            "configmaps": ui.navConfigMaps,
            "secrets": ui.navSecrets,
            "resourcequotas": ui.navResourceQuotas,
            "limitranges": ui.navLimitRanges,
            "horizontalpodautoscalers": ui.navHorizontalPodAutoscalers,
            "poddisruptionbudgets": ui.navPodDisruptionBudgets,
            "priorityclasses": ui.navPriorityClasses,
            "runtimeclasses": ui.navRuntimeClasses,
            "leases": ui.navLeases,
            "mutatingwebhooks": ui.navMutatingWebhooks,
            "validatingwebhooks": ui.navValidatingWebhooks,
            "nodegroups": ui.navNodeGroups,
            "addons": ui.navAddons,
        }

        self.overview_ui = Ui_OverviewPage()
        overview_content = QWidget()
        overview_content.setObjectName("overviewContent")
        self.overview_ui.setupUi(overview_content)
        overview_scroll = QScrollArea()  # the cards can be taller than the window
        overview_scroll.setWidgetResizable(True)
        overview_scroll.setFrameShape(QFrame.Shape.NoFrame)
        overview_scroll.viewport().setAutoFillBackground(False)
        overview_content.setAutoFillBackground(False)
        overview_scroll.setWidget(overview_content)
        overview_layout = QVBoxLayout(ui.overviewHost)
        overview_layout.setContentsMargins(0, 0, 0, 0)
        overview_layout.addWidget(overview_scroll)
        self.overview_refresh_button = ui.overviewRefreshButton
        self.nodes_table = ui.nodesTable
        self.nodes_heading = ui.nodesHeading
        self.workloads_ui = Ui_WorkloadsOverviewPage()
        self.workloads_ui.setupUi(ui.workloadsOverviewHost)
        self.workloads_refresh_button = ui.workloadsRefreshButton
        self.workloads_table = self.workloads_ui.eventsTable
        for linked in (self.table, self.nodes_table, self.workloads_table):
            self._enable_links(linked)
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
        self.save_button = self.viewer_ui.saveButton
        self.save_button.clicked.connect(self._save_viewer_tab)
        while self.viewer_tabs.count():  # drop the sample tab used in Designer
            sample = self.viewer_tabs.widget(0)
            assert sample is not None
            self.viewer_tabs.removeTab(0)
            sample.deleteLater()
        self.viewer_tabs.tabCloseRequested.connect(self._close_viewer_tab)
        self.viewer_tabs.tabBar().hide()  # the top bar shows them
        self.settings_ui = Ui_SettingsPage()
        self.settings_ui.setupUi(ui.settingsHost)
        self.settings_ui.contextsTable.setRowCount(0)
        self.settings_ui.saveButton.clicked.connect(self._save_preferences)
        self.settings_ui.openLogsButton.clicked.connect(self._open_log_folder)
        self.settings_ui.clearCacheButton.clicked.connect(self._clear_cache)
        self.settings_ui.kubeconfigAddButton.clicked.connect(self._add_kubeconfig_file)
        self.settings_ui.kubeconfigRemoveButton.clicked.connect(
            self._remove_kubeconfig_file
        )
        self.settings_ui.loginAddButton.clicked.connect(self._add_login_row)
        self.settings_ui.loginRemoveButton.clicked.connect(self._remove_login_row)
        self.settings_ui.newThemeButton.clicked.connect(self._new_theme)
        self.settings_ui.editThemeButton.clicked.connect(self._edit_theme)
        self.settings_ui.deleteThemeButton.clicked.connect(self._delete_theme)
        self.settings_ui.openThemesButton.clicked.connect(self._open_themes_folder)
        self.settings_ui.themeCombo.currentIndexChanged.connect(
            self._update_theme_buttons
        )
        self._overview_context: str | None = None
        self._overview_busy = False

        for button in (
            self.nav_overview,
            self.nav_workloads,
            self.nav_network,
            self.nav_config,
            self.nav_workloads_overview,
            *self._nav_views.values(),
            ui.settingsButton,
        ):
            button.setAutoExclusive(False)  # _show_page keeps the checked state
        self.nav_workloads.setCheckable(False)
        self.nav_network.setCheckable(False)
        self.nav_config.setCheckable(False)
        ui.navNodeGroups.setVisible(False)  # only EKS contexts have Node Groups
        for button in (self.refresh_button, self.workloads_refresh_button):
            button.setVisible(False)  # the Overview opens first
        self._render_pinned()
        self._submenus = {}
        for submenu in (self.submenu, self.network_submenu, self.config_submenu):
            animation = QPropertyAnimation(submenu, b"maximumHeight")
            animation.setDuration(180)
            animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self._submenus[submenu] = animation
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
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )  # the headers line up with the cells below them
        header.sectionClicked.connect(self._sort_rows)
        self.table.setShowGrid(False)  # the rows draw their own divider
        self._apply_view_columns()
        for column, width in (
            (0, 160),
            (1, 150),
            (2, 260),
            (3, 110),
            (4, 130),
            (5, 90),
            (6, 100),
            (7, 90),
        ):
            self.table.setColumnWidth(column, width)
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self._show_column_menu)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_row_menu)
        self._style_template = self.styleSheet()
        self._apply_style()
        self._sync_tray()
        self._show_version()
        self._show_access_note()
        self._update_notice_timer.timeout.connect(self.ui.updateNotice.hide)
        self.ui.updateLink.clicked.connect(self._update_app)
        self.ui.updateButton.clicked.connect(self._update_clicked)
        self.ui.updateButton.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.updateButton.customContextMenuRequested.connect(self._show_update_menu)
        self.ui.githubLink.clicked.connect(self._open_project)
        self.ui.licenseLink.clicked.connect(self._open_license)
        self.ui.footerVersion.clicked.connect(self._show_changelog)
        self.ui.companyLink.clicked.connect(self._open_company)

        self._spinner_angle = 0
        self._spinner_button: QPushButton | None = None
        self._spinner_saved: tuple[QIcon, str] | None = None
        self._spinner_timer = QTimer(self)
        self._spinner_timer.setInterval(70)
        self._spinner_timer.timeout.connect(self._tick_spinner)

        self._workloads_overview: WorkloadsOverview | None = None
        self._shown_key: tuple[str, str | None, str] | None = None  # what the table has
        # the rows the table was last filled with, so a read that changed a few
        # of them rewrites only those
        self._rendered: tuple[str, list] | None = None
        self._workloads_overview_context: str | None = None
        self._workloads_overview_busy = False
        self._login_action: LoginAction | None = None
        self._login_checking = False
        self.login_button.clicked.connect(self._sign_in)
        self.refresh_button.clicked.connect(self._refresh_or_cancel)
        self.pods_button.clicked.connect(self._view_workload_pods)
        self.details_button.clicked.connect(self._view_details)
        self.logs_button.clicked.connect(self._view_logs)
        self.table.itemSelectionChanged.connect(self._update_workload_actions)
        self.table.cellDoubleClicked.connect(lambda _row, _column: self._view_details())
        ui.settingsButton.setIcon(_gear_icon())
        ui.settingsButton.clicked.connect(lambda: self._show_page(2))
        for keys in ("Ctrl+R", "F5"):
            QShortcut(QKeySequence(keys), self).activated.connect(self._press_refresh)
        self.nav_overview.clicked.connect(lambda: self._show_page(0))
        self.nav_workloads.clicked.connect(lambda: self._toggle_submenu(self.submenu))
        self.nav_network.clicked.connect(
            lambda: self._toggle_submenu(self.network_submenu)
        )
        self.nav_config.clicked.connect(
            lambda: self._toggle_submenu(self.config_submenu)
        )
        for view, button in self._nav_views.items():
            button.clicked.connect(
                lambda _checked=False, view=view: self._open_list_view(view)
            )
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            button.customContextMenuRequested.connect(
                lambda position, view=view, button=button: self._show_pin_menu(
                    view, button.mapToGlobal(position)
                )
            )
            button.installEventFilter(self)
            self._pin_gestures[button] = ("pin", view)
        self.nav_workloads_overview.clicked.connect(lambda: self._show_page(4))
        for view, (button, _page) in self._nav_pages.items():
            button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            button.customContextMenuRequested.connect(
                lambda position, view=view, button=button: self._show_pin_menu(
                    view, button.mapToGlobal(position)
                )
            )
            button.installEventFilter(self)
            self._pin_gestures[button] = ("pin", view)
        self.workloads_refresh_button.clicked.connect(self.refresh_workloads_overview)
        # the overview names each kind; the ones that have a list link to it
        for key, view in WORKLOAD_LINKS.items():
            getattr(self.workloads_ui, f"{key}Link").clicked.connect(
                lambda _checked=False, view=view: self._open_list_view(view)
            )
        self.overview_refresh_button.clicked.connect(self.refresh_overview)
        self.context_combo.currentTextChanged.connect(self._context_changed)
        self.context_combo.currentTextChanged.connect(self.refresh)
        self.namespace_combo.currentIndexChanged.connect(self.refresh)
        self.search_input.textChanged.connect(self._filter_rows)
        self.search_case_button.toggled.connect(self._filter_rows)
        self.search_regex_button.toggled.connect(self._filter_rows)

    def _press_refresh(self) -> None:
        """Ctrl+R and F5: press the refresh button of the page on screen, if it
        has one and it can be pressed now."""
        page = self.pages.currentIndex()
        tab = self.viewer_tabs.currentWidget()
        button = {
            0: self.overview_refresh_button,
            1: self.refresh_button,
            3: tab.ui.refreshButton if isinstance(tab, LogTab) else None,
            4: self.workloads_refresh_button,
        }.get(page)
        if button is not None:
            button.click()

    def _load_contexts(self) -> None:
        """Read the kubeconfig contexts in a worker; reading them can take a
        while and must not freeze the window."""
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
        self._select_default_namespace()
        self.no_contexts_banner.setVisible(not contexts)
        if not contexts:
            self._set_status(lambda: self.tr("No contexts found in kubeconfig"))
            self.refresh_button.setEnabled(False)
            return
        self.refresh()
        self._ensure_overview()
        self._check_login()
        self._update_eks_entries()
        self._restore_screen()

    def _restore_screen(self) -> None:
        """Back to the page and list the app was left on, when it remembers the
        last context."""
        if not self.settings.remember_last_context:
            return
        page, view = self.settings.last_screen
        if page == 1 and view in self._nav_views:
            self._open_list_view(view)
        elif page in (0, 2, 4):
            self._show_page(page)

    def _remember_screen(self) -> None:
        """Keep the page and list on screen; a viewer tab keeps the last
        list."""
        page = self.pages.currentIndex()
        if self.settings.remember_last_context and page in (0, 1, 2, 4):
            view = self._view if page == 1 else self.settings.last_screen[1]
            self.settings.last_screen = (page, view)
            self._save_settings()

    def _update_eks_entries(self) -> None:
        """Node Groups belong to Amazon EKS: show the entry only for a context
        that is one."""
        context = self._context()
        if not context:
            self._show_eks_entries(context, False)
            return
        self._run_action(
            is_eks_context,
            lambda available: self._show_eks_entries(context, available),
            context,
            on_error=lambda _reason: self._show_eks_entries(context, False),
            quiet=True,
        )

    def _show_pin_menu(self, view: str, position: QPoint) -> None:
        """Right-click on a list's entry: pin it to the top of the menu, or
        take it back."""
        pinned = view in self.settings.pinned_views()
        menu = QMenu(self)
        action = menu.addAction(
            self.tr("Unpin from the top") if pinned else self.tr("Pin to the top")
        )
        action.triggered.connect(lambda: self._toggle_pin(view))
        menu.exec(position)

    def _tab_context_menu(self, button: QPushButton, close: Callable[[], None]) -> None:
        """Right-click on a tab of the top bar: close it, or close them all."""
        button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        button.customContextMenuRequested.connect(
            lambda position: self._show_tab_menu(close, button.mapToGlobal(position))
        )

    def _show_tab_menu(self, close: Callable[[], None], position: QPoint) -> None:
        menu = QMenu(self)
        menu.addAction(self.tr("Close")).triggered.connect(
            lambda _checked=False: close()
        )
        menu.addAction(self.tr("Close all")).triggered.connect(
            lambda _checked=False: self._close_all_tabs()
        )
        menu.exec(position)

    def _close_all_tabs(self) -> None:
        """Unpin every list and close every Details and Logs of this
        context."""
        context = self._context()
        self.settings.set_pinned_views([])
        self._save_settings()
        for index in reversed(range(self.viewer_tabs.count())):
            if self._viewer_contexts.get(self.viewer_tabs.widget(index)) == context:
                self._close_viewer_tab(index)
        self._render_pinned()

    def _toggle_pin(self, view: str) -> None:
        pinned = self.settings.pinned_views()
        if view in pinned:
            pinned.remove(view)
        else:
            pinned.append(view)
        self.settings.set_pinned_views(pinned)
        self._save_settings()
        self._render_pinned()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Two quick clicks on a list's entry pin it; the middle button on a
        pinned tab unpins it and on an open Details or Logs closes it; dragging
        any tab of the top bar moves it."""
        if watched is self.ui.pinnedBar and event.type() in (
            QEvent.Type.DragEnter,
            QEvent.Type.DragMove,
            QEvent.Type.DragLeave,
            QEvent.Type.Drop,
        ):
            return self._drag_over_pins(event)
        gesture, view = self._pin_gestures.get(watched, ("", ""))
        draggable = gesture in ("unpin", "viewer")
        mouse = cast(QMouseEvent, event)  # only read once `event.type()` says so
        if draggable and event.type() == QEvent.Type.MouseButtonPress:
            self._drag_start = (
                mouse.position().toPoint()
                if mouse.button() == Qt.MouseButton.LeftButton
                else None
            )
        elif draggable and event.type() == QEvent.Type.MouseButtonRelease:
            self._drag_start = None  # a click that ended is not a drag to come
        if (
            draggable
            and event.type() == QEvent.Type.MouseMove
            and mouse.buttons() & Qt.MouseButton.LeftButton
            and self._drag_start is not None
            and (mouse.position().toPoint() - self._drag_start).manhattanLength()
            >= QApplication.startDragDistance()
        ):
            self._drag_start = None
            self._drag_pin(view, watched, viewer=gesture == "viewer")
            return True
        if (
            gesture == "pin"
            and event.type() == QEvent.Type.MouseButtonDblClick
            and mouse.button() == Qt.MouseButton.LeftButton
        ):
            if view not in self.settings.pinned_views():
                self._toggle_pin(view)
        elif (
            draggable
            and event.type() == QEvent.Type.MouseButtonPress
            and mouse.button() == Qt.MouseButton.MiddleButton
        ):
            if gesture == "viewer":
                self._close_viewer_tab(int(view))
            else:
                self._toggle_pin(view)
            return True
        return super().eventFilter(watched, event)

    def _drag_pin(self, view: str, widget: QObject, viewer: bool = False) -> None:
        """Drag a tab of the top bar: its picture follows the cursor,
        translucent, while the tab stays behind faded.

        `view` is the pinned list, or the index of the Details or Logs
        when `viewer`.
        """
        tab = (
            widget
            if isinstance(widget, QFrame)
            else cast(QWidget, widget).parentWidget()
        )
        assert tab is not None
        picture = QPixmap(tab.size())
        picture.fill(Qt.GlobalColor.transparent)
        painter = QPainter(picture)
        painter.setOpacity(0.85)
        painter.drawPixmap(0, 0, tab.grab())
        painter.end()
        mime = QMimeData()
        mime.setData(VIEWER_MIME if viewer else PIN_MIME, view.encode())
        drag = QDrag(tab)
        drag.setMimeData(mime)
        drag.setPixmap(picture)
        drag.setHotSpot(tab.mapFromGlobal(QCursor.pos()))
        fade = QGraphicsOpacityEffect(tab)
        fade.setOpacity(0.35)
        tab.setGraphicsEffect(fade)
        drag.exec(Qt.DropAction.MoveAction)
        self._drop_marker.hide()
        if tab.graphicsEffect() is fade:  # the move may have redrawn the tabs
            tab.setGraphicsEffect(cast(Any, None))  # the stubs do not allow None

    def _pin_slot(self, item: tuple[str, Any], left: int) -> tuple[int, int]:
        """Where a tab dropped at `left` (a position in the top bar) would
        land: its place among the other tabs, and the x of the edge it goes
        against."""
        bar = self.ui.pinnedBar
        tabs = [
            tab
            for other, button in zip(self._bar_items, self._pinned_buttons, strict=True)
            if other != item and (tab := button.parentWidget()) is not None
        ]
        slot = sum(1 for tab in tabs if tab.mapTo(bar, tab.rect().center()).x() < left)
        if slot < len(tabs):
            return slot, tabs[slot].mapTo(bar, QPoint(0, 0)).x()
        return slot, tabs[-1].mapTo(bar, QPoint(tabs[-1].width(), 0)).x()

    def _dragged_item(self, mime: QMimeData) -> tuple[str, Any] | None:
        """The tab a drag carries, when it is one of the top bar's."""
        if mime.hasFormat(PIN_MIME):
            return "pin", bytes(mime.data(PIN_MIME).data()).decode()
        if mime.hasFormat(VIEWER_MIME):
            index = int(bytes(mime.data(VIEWER_MIME).data()).decode())
            widget = self.viewer_tabs.widget(index)
            return ("viewer", widget) if widget is not None else None
        return None

    def _drag_over_pins(self, event: Any) -> bool:
        """Show where a dragged tab would land, a line between the tabs;
        dropping it moves it there."""
        if event.type() == QEvent.Type.DragLeave:
            self._drop_marker.hide()
            return False
        item = self._dragged_item(event.mimeData())
        if item is None:
            return False
        event.acceptProposedAction()
        left = event.position().toPoint().x()
        if event.type() == QEvent.Type.Drop:
            self._drop_marker.hide()
            # after the drag ends: the tab it came from is redrawn by the move
            QTimer.singleShot(0, lambda: self._move_tab(item, left))
        elif any(other != item for other in self._bar_items):
            _slot, edge = self._pin_slot(item, left)
            bar = self.ui.pinnedBar
            self._drop_marker.setGeometry(max(edge - 1, 0), 6, 2, bar.height() - 12)
            self._drop_marker.show()
            self._drop_marker.raise_()
        return True

    def _move_tab(self, item: tuple[str, Any], left: int) -> None:
        """Put a tab where it was dropped: before the first other tab whose
        middle is right of `left`, or last.

        The pinned lists keep the order they now have among themselves.
        """
        others = [other for other in self._bar_items if other != item]
        if item not in self._bar_items or not others:
            return
        slot, _edge = self._pin_slot(item, left)
        order = others[:slot] + [item] + others[slot:]
        if order == self._bar_items:
            return
        self._bar_order = order
        shown = [name for kind, name in order if kind == "pin"]
        pinned = self.settings.pinned_views()
        ranked = iter(shown)  # the pinned lists out of sight keep their places
        reordered = [next(ranked) if name in shown else name for name in pinned]
        if reordered != pinned:
            self.settings.set_pinned_views(reordered)
            self._save_settings()
        self._render_pinned()

    def _render_pinned(self) -> None:
        """The pinned lists, as tabs in the top bar, each with a × to unpin.

        A list that is not available now (Node Groups outside Amazon
        EKS) stays out.
        """
        layout = self.ui.pinnedLayout
        for button in self._pinned_buttons:
            tab = button.parentWidget()
            assert tab is not None
            layout.removeWidget(tab)
            tab.deleteLater()
        self._pinned_buttons = []
        built: dict[tuple[str, Any], tuple[QFrame, QPushButton]] = {}
        self._pin_gestures = {
            widget: gesture
            for widget, gesture in self._pin_gestures.items()
            if gesture[0] == "pin"  # the tabs are gone; the menu entries stay
        }
        for view in self.settings.pinned_views():
            page = self._nav_pages.get(view)
            source = page[0] if page else self._nav_views.get(view)
            if source is None or source.isHidden():
                continue
            active = (
                self.pages.currentIndex() == page[1]
                if page
                else self.pages.currentIndex() == 1 and self._view == view
            )
            show = (
                (lambda _checked=False, index=page[1]: self._show_page(index))
                if page
                else (lambda _checked=False, view=view: self._open_list_view(view))
            )
            tab = QFrame()
            tab.setProperty("pinTab", "true")
            tab.setProperty("active", "true" if active else "false")
            row = QHBoxLayout(tab)
            row.setContentsMargins(10, 0, 4, 0)
            row.setSpacing(0)
            button = QPushButton(source.text())
            button.setCheckable(True)
            button.setChecked(active)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(show)
            self._tab_context_menu(button, lambda view=view: self._toggle_pin(view))
            close = QPushButton("×")
            close.setProperty("closeTab", "true")
            close.setToolTip(self.tr("Unpin from the top"))
            close.setCursor(Qt.CursorShape.PointingHandCursor)
            close.clicked.connect(
                lambda _checked=False, view=view: self._toggle_pin(view)
            )
            for widget in (tab, button, close):
                widget.installEventFilter(self)
                self._pin_gestures[widget] = ("unpin", view)
            row.addWidget(button)
            row.addWidget(close)
            built[("pin", view)] = (tab, button)
        for index in range(self.viewer_tabs.count()):
            widget = self.viewer_tabs.widget(index)
            if self._viewer_contexts.get(widget) != self._context():
                continue  # kept open, but shown only in its own context
            built[("viewer", widget)] = self._viewer_top_tab(index)
        # the order the person gave them, then the ones that came after
        self._bar_items = [item for item in self._bar_order if item in built]
        self._bar_items += [item for item in built if item not in self._bar_items]
        # the pinned lists keep the order of the settings among themselves
        pins = iter(("pin", view) for view in self.settings.pinned_views())
        pins = iter(item for item in pins if item in built)
        self._bar_items = [
            next(pins) if item[0] == "pin" else item for item in self._bar_items
        ]
        self._bar_order = list(self._bar_items)
        for item in self._bar_items:
            tab, button = built[item]
            layout.addWidget(tab)
            self._pinned_buttons.append(button)
        self.ui.pinnedBar.setVisible(bool(self._pinned_buttons))
        self.pinned_scroll.setVisible(bool(self._pinned_buttons))
        QTimer.singleShot(0, self._reveal_current_tab)

    def _reveal_current_tab(self) -> None:
        """Scroll the top bar to the tab that is open."""
        for button in self._pinned_buttons:
            if button.isChecked():
                self.pinned_scroll.ensureWidgetVisible(button.parentWidget() or button)
                return

    def _viewer_top_tab(self, index: int) -> tuple[QFrame, QPushButton]:
        """A tab of the top bar for an open Details or Logs, with a × to close
        it."""
        title = self.viewer_tabs.tabText(index)
        active = self.pages.currentIndex() == 3 and (
            self.viewer_tabs.currentIndex() == index
        )
        tab = QFrame()
        tab.setProperty("pinTab", "true")
        tab.setProperty("active", "true" if active else "false")
        row = QHBoxLayout(tab)
        row.setContentsMargins(10, 0, 4, 0)
        row.setSpacing(0)
        short = title if len(title) <= 32 else f"{title[:31]}…"
        button = QPushButton(short.replace("&", "&&"))
        button.setToolTip(title)
        button.setCheckable(True)
        button.setChecked(active)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda _checked=False, i=index: self._open_viewer_tab(i))
        self._tab_context_menu(button, lambda i=index: self._close_viewer_tab(i))
        close = QPushButton("×")
        close.setProperty("closeTab", "true")
        close.setToolTip(self.tr("Close"))
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.clicked.connect(lambda _checked=False, i=index: self._close_viewer_tab(i))
        for widget in (tab, button, close):
            widget.installEventFilter(self)
            self._pin_gestures[widget] = ("viewer", str(index))
        row.addWidget(button)
        row.addWidget(close)
        return tab, button

    def _open_viewer_tab(self, index: int) -> None:
        self.viewer_tabs.setCurrentIndex(index)
        self._show_page(3)

    def _load_cluster_info(self, context: str) -> None:
        """What AWS says about an EKS cluster, for the card on the overview;
        when it cannot be read the card stays hidden and the rest is
        unaffected."""
        self._run_action(
            get_cluster_info,
            lambda info: self._show_cluster_info(context, info),
            context,
            on_error=lambda reason: self._cluster_info_failed(context, reason),
            quiet=True,
        )

    def _cluster_info_failed(self, context: str, reason: str) -> None:
        logger.info("Cluster info unavailable: %s", first_line(reason))
        self._show_cluster_info(context, None)

    def _show_cluster_info(self, context: str, info: ClusterInfo | None) -> None:
        if context != self._context():
            return  # the answer of a context that is no longer open
        self._cluster_info = info
        self._render_cluster_info()

    def _render_cluster_info(self) -> None:
        info = self._cluster_info
        overview = self.overview_ui
        for card, grid in (
            (overview.clusterInfoCard, overview.clusterInfoGrid),
            (overview.networkingCard, overview.networkingGrid),
        ):
            card.setVisible(info is not None)
            while (item := grid.takeAt(0)) is not None:
                widget = item.widget()
                assert widget is not None
                widget.deleteLater()
        if info is None:
            return
        short = (
            (self.tr("Status"), self._aws_value(info.status)),
            (self.tr("Kubernetes version"), info.version),
            (self.tr("Platform version"), info.platform_version),
            (self.tr("Created"), info.created),
            (self.tr("Provider"), info.provider),
        )
        long = (
            (self.tr("API server endpoint"), info.endpoint),
            (self.tr("Cluster ARN"), info.arn),
            (self.tr("Cluster IAM role ARN"), info.role_arn),
            (self.tr("OpenID Connect provider URL"), info.oidc_issuer),
        )
        grid = overview.clusterInfoGrid
        for index, (title, value) in enumerate(short):
            grid.addWidget(self._info_cell(title, value), index // 4, index % 4)
        for index, (title, value) in enumerate(long):
            grid.addWidget(self._info_cell(title, value), 2 + index, 0, 1, 4)
        networking = (
            (self.tr("VPC"), info.vpc_id),
            (self.tr("Cluster security group"), info.security_group),
            (
                self.tr("Additional security groups"),
                ", ".join(info.additional_security_groups) or self.tr("None"),
            ),
            (
                self.tr("API server endpoint access"),
                self._aws_value(info.endpoint_access),
            ),
            (self.tr("Cluster IP address family"), info.ip_family),
            (self.tr("Service IPv4 range"), info.service_cidr),
            (
                self.tr("Public access source allowlist"),
                ", ".join(info.public_access_cidrs) or "—",
            ),
            (self.tr("Subnets"), "\n".join(info.subnets) or "—"),
        )
        grid = overview.networkingGrid
        for index, (title, value) in enumerate(networking):
            grid.addWidget(self._info_cell(title, value), index // 4, index % 4)

    def _aws_value(self, value: str) -> str:
        """A status or access mode as AWS words it, in the interface language;
        a word it does not know stays as it came."""
        known = {
            "ACTIVE": self.tr("Active"),
            "CREATING": self.tr("Creating"),
            "UPDATING": self.tr("Updating"),
            "DELETING": self.tr("Deleting"),
            "DEGRADED": self.tr("Degraded"),
            "FAILED": self.tr("Failed"),
            "CREATE_FAILED": self.tr("Creation failed"),
            "UPDATE_FAILED": self.tr("Update failed"),
            "DELETE_FAILED": self.tr("Deletion failed"),
            "PENDING": self.tr("Pending"),
            "DEPLOYED": self.tr("Deployed"),
            "SUPERSEDED": self.tr("Superseded"),
            "UNINSTALLED": self.tr("Uninstalled"),
            "UNINSTALLING": self.tr("Uninstalling"),
            "PENDING_INSTALL": self.tr("Pending install"),
            "PENDING_UPGRADE": self.tr("Pending upgrade"),
            "PENDING_ROLLBACK": self.tr("Pending rollback"),
            "PUBLIC": self.tr("Public"),
            "PRIVATE": self.tr("Private"),
            "PUBLIC_AND_PRIVATE": self.tr("Public and private"),
        }
        key = value.strip().upper().replace(" ", "_").replace("-", "_")
        return known.get(key, value)

    @staticmethod
    def _info_cell(title: str, value: str) -> QLabel:
        body = html.escape(value).replace("\n", "<br>")
        cell = QLabel(f"<b>{html.escape(title)}</b><br>{body}")
        cell.setTextFormat(Qt.TextFormat.RichText)
        cell.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        cell.setMinimumHeight(cell.sizeHint().height())  # never squeezed by the page
        return cell

    def _show_eks_entries(self, context: str, available: bool) -> None:
        if context != self._context():
            return  # the answer of a context that is no longer open
        self.ui.navNodeGroups.setVisible(available)
        self._eks_context = context if available else None
        self._render_pinned()
        if available:
            self._load_cluster_info(context)
        else:
            self._show_cluster_info(context, None)
        if not available and self._view in EKS_VIEWS:
            self._open_list_view("deployments")

    def _fill_contexts(self, selected: str | None) -> None:
        """Show contexts under their custom names while keeping the real
        name."""
        self.context_combo.blockSignals(True)
        self.context_combo.clear()
        for context in sorted(
            self._contexts,
            key=lambda name: (self.settings.display_name(name).casefold(), name),
        ):
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
        self.nav_workloads_overview.setChecked(index == 4)
        self._apply_page_titles()
        self._render_pinned()
        self._remember_screen()
        for page, button in (
            (0, self.overview_refresh_button),
            (1, self.refresh_button),
            (4, self.workloads_refresh_button),
        ):
            button.setVisible(index == page)  # the page's own, next to its title
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
                "daemonsets": (
                    self.tr("DaemonSets"),
                    self.tr("DaemonSets of the cluster"),
                ),
                "replicasets": (
                    self.tr("ReplicaSets"),
                    self.tr("ReplicaSets of the cluster"),
                ),
                "replicationcontrollers": (
                    self.tr("ReplicationControllers"),
                    self.tr("ReplicationControllers of the cluster"),
                ),
                "jobs": (self.tr("Jobs"), self.tr("Jobs of the cluster")),
                "cronjobs": (self.tr("CronJobs"), self.tr("CronJobs of the cluster")),
                "services": (self.tr("Services"), self.tr("Services of the cluster")),
                "endpointslices": (
                    self.tr("Endpoint Slices"),
                    self.tr("Endpoint Slices of the cluster"),
                ),
                "endpoints": (
                    self.tr("Endpoints"),
                    self.tr("Endpoints of the cluster"),
                ),
                "ingresses": (
                    self.tr("Ingresses"),
                    self.tr("Ingresses of the cluster"),
                ),
                "ingressclasses": (
                    self.tr("Ingress Classes"),
                    self.tr("Ingress Classes of the cluster"),
                ),
                "networkpolicies": (
                    self.tr("Network Policies"),
                    self.tr("Network Policies of the cluster"),
                ),
                "configmaps": (
                    self.tr("Config Maps"),
                    self.tr("Config Maps of the cluster"),
                ),
                "secrets": (
                    self.tr("Secrets"),
                    self.tr("Secrets of the cluster"),
                ),
                "resourcequotas": (
                    self.tr("Resource Quotas"),
                    self.tr("Resource Quotas of the cluster"),
                ),
                "limitranges": (
                    self.tr("Limit Ranges"),
                    self.tr("Limit Ranges of the cluster"),
                ),
                "horizontalpodautoscalers": (
                    self.tr("Horizontal Pod Autoscalers"),
                    self.tr("Horizontal Pod Autoscalers of the cluster"),
                ),
                "poddisruptionbudgets": (
                    self.tr("Pod Disruption Budgets"),
                    self.tr("Pod Disruption Budgets of the cluster"),
                ),
                "priorityclasses": (
                    self.tr("Priority Classes"),
                    self.tr("Priority Classes of the cluster"),
                ),
                "runtimeclasses": (
                    self.tr("Runtime Classes"),
                    self.tr("Runtime Classes of the cluster"),
                ),
                "leases": (
                    self.tr("Leases"),
                    self.tr("Leases of the cluster"),
                ),
                "mutatingwebhooks": (
                    self.tr("Mutating Webhook Configurations"),
                    self.tr("Mutating Webhook Configurations of the cluster"),
                ),
                "validatingwebhooks": (
                    self.tr("Validating Webhook Configurations"),
                    self.tr("Validating Webhook Configurations of the cluster"),
                ),
                "nodegroups": (
                    self.tr("Node Groups"),
                    self.tr("Node Groups of the cluster"),
                ),
                "addons": (
                    self.tr("Add-ons"),
                    self.tr("Add-ons of the cluster"),
                ),
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

    def start_update_check(self) -> None:
        """Look for a new version when the app starts, if Settings allow it."""
        if self.settings.check_updates:
            self.check_updates()

    def _recheck_updates(self) -> None:
        if self.settings.check_updates and self._update_state != "checking":
            self._rechecking = True
            self.check_updates()

    def check_updates(self) -> None:
        if self._update_state == "checking":
            return
        self._update_started = time.monotonic()
        self._set_update_state("checking")
        self._run_action(
            check_for_update,
            self._update_answered,
            quiet=True,
            on_error=lambda _message: self._update_answered(UpdateCheck("failed")),
        )

    def _update_answered(self, result: UpdateCheck) -> None:
        """Show the answer once the icon has searched for long enough."""
        self._update_result = result
        remaining = UPDATE_SEARCH_MS / 1000 - (time.monotonic() - self._update_started)
        if remaining > 0:
            self._update_delay.start(int(remaining * 1000))
        else:
            self._update_checked()

    def _update_checked(self) -> None:
        result = self._update_result
        self._update_release = result.release
        self._set_update_state(result.status)
        rechecking, self._rechecking = self._rechecking, False
        if result.release is not None:
            self._notify_update(result.release, daily=rechecking)
        notice = {
            "current": self.tr("Up to date"),
            "failed": self.tr("Could not check"),
        }.get(result.status)
        if notice is not None and not rechecking:
            self.ui.updateNotice.setText(notice)
            self.ui.updateNotice.show()
            self._update_notice_timer.start()

    def _notify_update(self, release: Release, daily: bool) -> None:
        """Tell the operating system about a new version through the tray icon:
        a check the person asked for always says so, the hourly one only once
        a day. Without a tray the icon in the footer is the notice."""
        if self._tray is None:
            return
        if daily:
            today = datetime.date.today().isoformat()
            if self.settings.last_update_notice == today:
                return
            self.settings.last_update_notice = today
            self._save_settings()
        self._tray.showMessage(
            self.tr("KubeScope update available"),
            self.tr("Version {version} is available").format(version=release.version),
            QSystemTrayIcon.MessageIcon.Information,
        )

    def _set_update_state(self, state: str) -> None:
        self._update_state = state
        self._update_phase = 0
        tips = {
            "idle": self.tr("Check for updates"),
            "checking": self.tr("Checking for updates..."),
            "current": self.tr("KubeScope is up to date. Click to check again."),
            "failed": self.tr("Could not check for updates. Click to try again."),
        }
        release = self._update_release
        available = state == "available" and release is not None
        if release is not None and available:
            tip = self.tr(
                "Update available: {version}. Click to update; "
                "right-click to check again."
            ).format(version=release.version)
        else:
            tip = tips.get(state, tips["idle"])
        self.ui.updateButton.setToolTip(tip)
        self.ui.updateLink.setVisible(available)
        if release is not None and available:
            self.ui.updateLink.setText(self.tr("Update available"))
            self.ui.updateLink.setToolTip(
                self.tr("Update KubeScope to {version}").format(version=release.version)
            )
        self.ui.updateNotice.hide()
        self._update_notice_timer.stop()
        if state in ("checking", "available"):
            self._update_timer.start()
        else:
            self._update_timer.stop()
        self._tick_update(advance=False)

    def _tick_update(self, advance: bool = True) -> None:
        """Draw the next frame of the footer icon: it spins while checking and
        pulses while an update waits."""
        self._update_phase += 1 if advance else 0
        state, phase = self._update_state, self._update_phase
        if state == "checking":
            icon = _spinner_icon(phase * 30 % 360, themed("#6b7380", text=True))
        elif state == "available":
            icon = _update_icon(state, 0.6 + 0.4 * math.sin(phase / 6) ** 2)
        else:
            icon = _update_icon(state)
        self.ui.updateButton.setIcon(icon)

    def _update_clicked(self) -> None:
        if self._update_state == "available":
            self._update_app()
        else:
            self.check_updates()

    def _update_app(self) -> None:
        """Confirm the update, install it as this app was installed, and start
        the new version."""
        release = self._update_release
        if release is None:
            return
        dialog = UpdateDialog(self, __version__, release, detect_install())
        if dialog.exec() != QDialog.DialogCode.Accepted or not dialog.restart_command:
            return
        restart(dialog.restart_command)
        self.close()
        QApplication.quit()

    def _show_update_menu(self, position: QPoint) -> None:
        menu = QMenu(self)
        menu.addAction(self.tr("Check for updates again"), self.check_updates)
        menu.exec(self.ui.updateButton.mapToGlobal(position))

    def _open_project(self) -> None:
        QDesktopServices.openUrl(QUrl(PROJECT_URL))

    def _open_company(self) -> None:
        QDesktopServices.openUrl(QUrl(COMPANY_URL))

    def _show_changelog(self) -> None:
        ChangelogDialog(self).exec()

    def _open_license(self) -> None:
        QDesktopServices.openUrl(QUrl(LICENSE_URL))

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
        self.nav_overview.setIcon(_nav_icon("overview"))
        self.nav_workloads.setIcon(_nav_icon("workloads"))
        self.ui.navNodeGroups.setIcon(_nav_icon("nodegroups"))
        self.nav_network.setIcon(_nav_icon("network"))
        self.nav_config.setIcon(_nav_icon("config"))
        self.save_button.setIcon(_nav_icon("save"))
        self._set_update_state(self._update_state)  # redraw its icon in this theme
        light = _pair(themed("#ffffff", text=True))  # on the filled buttons
        for button in (
            self.workloads_refresh_button,
            self.overview_refresh_button,
            self.refresh_button,
        ):
            button.setIcon(_nav_icon("reload", light))
        accent = _pair(themed("#3220a0"))
        self.pods_button.setIcon(_nav_icon("pods", accent))
        self.details_button.setIcon(_nav_icon("details", accent))
        self.logs_button.setIcon(_nav_icon("document", accent))
        for shape, button in self.write_buttons.items():
            button.setIcon(_nav_icon(shape, accent))

    def _apply_theme(self) -> None:
        """Switch to the theme in the settings and redraw what was drawn with
        the old colors."""
        apply_theme(cast(QApplication, QApplication.instance()), self.settings.theme)
        self._apply_style()
        accent = _pair(themed("#3220a0"))
        for index in range(self.viewer_tabs.count()):
            tab = self.viewer_tabs.widget(index)
            if isinstance(tab, LogTab):
                tab.ui.refreshButton.setIcon(_nav_icon("reload", accent))
                restyle(tab.ui.logText, tab.highlighter)
            else:
                assert isinstance(tab, DetailTab)
                restyle(tab.editor, tab.highlighter)
                tab.restyle()
        self._render_rows()
        if self._overview is not None:
            self._render_overview(self._overview)
        if self._workloads_overview is not None:
            self._render_workloads_overview(self._workloads_overview)

    def _toggle_submenu(self, submenu: QFrame) -> None:
        """Slide a menu's entries open or closed, whatever the other one
        does."""
        animation = self._submenus[submenu]
        expand = submenu.maximumHeight() == 0 or (
            animation.state() == QPropertyAnimation.State.Running
            and animation.endValue() == 0
        )
        animation.stop()
        animation.setStartValue(submenu.maximumHeight())
        animation.setEndValue(submenu.sizeHint().height() if expand else 0)
        animation.start()

    def _open_list_view(self, view: str) -> None:
        """Show a Pods or workload list; they all share one table."""
        changed = view != self._view
        if changed and view in WORKLOAD_VIEWS and self._view in WORKLOAD_VIEWS:
            self._workloads = []  # another kind: do not show these rows meanwhile
        if changed and view in RESOURCE_VIEWS and self._view in RESOURCE_VIEWS:
            self._resources = []  # other columns: do not show these rows meanwhile
        logger.debug("Opening the %s list", view)
        self._view = view
        if changed:
            self._sort = None
            header = self.table.horizontalHeader()
            header.setSortIndicatorShown(False)
            self._apply_view_columns()
            self._render_rows()
            key = (self._context(), self._list_namespace(view), view)
            known = self._answers.get(key)
            self._shown_key = key if known else None
            if known:  # the last answer, until the fresh one arrives
                self._show_answer(view, *known)
        self._show_page(1)
        if changed:
            self._set_status(lambda: self.tr("Loading resources..."))
            self._sync_loading()
            self._list_timer.start()

    def _resource_headers(self) -> list[str]:
        """The columns a network kind shows between its name and its age."""
        translate = QCoreApplication.translate
        return {
            "services": [
                translate("MainWindow", "TYPE"),
                translate("MainWindow", "CLUSTER IP"),
                translate("MainWindow", "EXTERNAL IP"),
                translate("MainWindow", "PORTS"),
            ],
            "endpointslices": [
                translate("MainWindow", "ADDRESS TYPE"),
                translate("MainWindow", "PORTS"),
                translate("MainWindow", "ENDPOINTS"),
            ],
            "endpoints": [translate("MainWindow", "ENDPOINTS")],
            "ingresses": [
                translate("MainWindow", "CLASS"),
                translate("MainWindow", "HOSTS"),
                translate("MainWindow", "ADDRESS"),
                translate("MainWindow", "PORTS"),
            ],
            "ingressclasses": [
                translate("MainWindow", "CONTROLLER"),
                translate("MainWindow", "PARAMETERS"),
            ],
            "networkpolicies": [
                translate("MainWindow", "POD SELECTOR"),
                translate("MainWindow", "POLICY TYPES"),
            ],
            "configmaps": [
                translate("MainWindow", "DATA"),
            ],
            "secrets": [
                translate("MainWindow", "TYPE"),
                translate("MainWindow", "DATA"),
            ],
            "resourcequotas": [
                translate("MainWindow", "USAGE"),
            ],
            "limitranges": [
                translate("MainWindow", "TYPES"),
            ],
            "horizontalpodautoscalers": [
                translate("MainWindow", "REFERENCE"),
                translate("MainWindow", "MIN PODS"),
                translate("MainWindow", "MAX PODS"),
                translate("MainWindow", "REPLICAS"),
            ],
            "poddisruptionbudgets": [
                translate("MainWindow", "MIN AVAILABLE"),
                translate("MainWindow", "MAX UNAVAILABLE"),
                translate("MainWindow", "ALLOWED DISRUPTIONS"),
            ],
            "priorityclasses": [
                translate("MainWindow", "VALUE"),
                translate("MainWindow", "GLOBAL DEFAULT"),
            ],
            "runtimeclasses": [
                translate("MainWindow", "HANDLER"),
            ],
            "leases": [
                translate("MainWindow", "HOLDER"),
            ],
            "mutatingwebhooks": [
                translate("MainWindow", "WEBHOOKS"),
            ],
            "validatingwebhooks": [
                translate("MainWindow", "WEBHOOKS"),
            ],
            "nodegroups": [
                translate("MainWindow", "STATUS"),
                translate("MainWindow", "INSTANCE TYPES"),
                translate("MainWindow", "NODES"),
                translate("MainWindow", "AMI TYPE"),
                translate("MainWindow", "AMI VERSION"),
            ],
            "addons": [
                translate("MainWindow", "STATUS"),
                translate("MainWindow", "VERSION"),
                translate("MainWindow", "SOURCE"),
            ],
        }[self._view]

    def _apply_view_columns(self) -> None:
        if self._view in RESOURCE_VIEWS:
            self._apply_resource_columns()
            return
        second = "CONTAINERS" if self._view == "pods" else "KIND"
        ready_header = {
            "jobs": QCoreApplication.translate("MainWindow", "COMPLETIONS"),
            "cronjobs": QCoreApplication.translate("MainWindow", "SCHEDULE"),
        }.get(self._view) or QCoreApplication.translate("MainWindow", "READY")
        context = "PodsDialog" if self._view == "pods" else "MainWindow"
        extra_columns = (
            [
                QCoreApplication.translate("MainWindow", "CONTROLLED BY"),
                QCoreApplication.translate("MainWindow", "NODE"),
                QCoreApplication.translate("MainWindow", "QOS"),
            ]
            if self._view == "pods"
            else [QCoreApplication.translate("MainWindow", "NODE SELECTOR")]
        )
        headers = [
            QCoreApplication.translate("MainWindow", "NAMESPACE"),
            QCoreApplication.translate(context, second),
            QCoreApplication.translate("MainWindow", "NAME"),
            ready_header,
            QCoreApplication.translate("MainWindow", "STATUS"),
            QCoreApplication.translate("MainWindow", "CPU"),
            QCoreApplication.translate("MainWindow", "MEMORY"),
            QCoreApplication.translate("MainWindow", "RESTARTS"),
            *extra_columns,
            QCoreApplication.translate("MainWindow", "AGE"),
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self._apply_view_buttons()

    def _apply_resource_columns(self) -> None:
        translate = QCoreApplication.translate
        headers = [
            translate("MainWindow", "NAMESPACE"),
            translate("MainWindow", "KIND"),
            translate("MainWindow", "NAME"),
            *self._resource_headers(),
            translate("MainWindow", "AGE"),
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self._apply_view_buttons()

    def _always_hidden(self) -> set[int]:
        """The namespace column, and the kind column of every list that has one
        (the count of containers, for Pods, which READY shows as squares):

        the page and the filter already say what the rows are.
        """
        return {0, 1}

    def _apply_view_buttons(self) -> None:
        """Pods and logs belong to workloads; a network resource has details
        only."""
        self.ui.filtersBar.setVisible(self._view not in EKS_VIEWS)  # nothing to filter
        for widget in (self.nodes_heading, self.nodes_table):
            widget.setVisible(self._view == "nodegroups")
        self.pods_button.setVisible(self._view in WORKLOAD_VIEWS)
        self.logs_button.setVisible(self._view not in RESOURCE_VIEWS)
        self._update_write_buttons()
        hidden = self.settings.hidden_columns(self._view) | self._always_hidden()
        for column in range(self.table.columnCount()):
            self.table.setColumnHidden(column, column in hidden)

    def _update_write_buttons(self) -> None:
        """The buttons of the write mode: the ones of this view, only while the
        mode is on."""
        names = {
            "shell": self.tr("Shell command"),
            "evict": self.tr("Evict"),
            "delete": self.tr("Delete"),
            "scale": self.tr("Scale"),
            "reload": self.tr("Restart"),
            "forward": self.tr("Forward"),
        }
        shown = WRITE_VIEWS.get(self._view, ()) if self.settings.write_mode else ()
        for shape, button in self.write_buttons.items():
            button.setText(names[shape])
            button.setVisible(shape in shown)
        self._update_workload_actions()

    def _write_button_clicked(self, shape: str) -> None:
        for entry_shape, _text, callback in self._write_entries():
            if entry_shape == shape:
                callback()

    def _show_row_menu(self, position: QPoint) -> None:
        """Row right-click: select the row and offer what the buttons above the
        table do for it."""
        row = self.table.rowAt(position.y())
        if row < 0:
            return
        self.table.selectRow(row)
        menu = QMenu(self)
        for button in (self.pods_button, self.details_button, self.logs_button):
            if not button.isHidden():
                action = menu.addAction(button.icon(), button.text())
                action.setEnabled(button.isEnabled())
                action.triggered.connect(button.click)
        entries = self._write_entries() if self.settings.write_mode else []
        if entries:
            menu.addSeparator()
            self._add_entries(menu, entries)
        menu.exec(self.table.viewport().mapToGlobal(position))

    def _show_column_menu(self, position: QPoint) -> None:
        """Header right-click: tick the columns to show; the choice is
        saved."""
        menu = QMenu(self)
        hidden = self.settings.hidden_columns(self._view)
        for column in range(self.table.columnCount()):
            if column in self._always_hidden():
                continue
            label = self._cell_text(self.table.horizontalHeaderItem(column))
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
        self._select_default_namespace()
        self._hide_permission_banner()
        self._overview_context = None
        self._workloads_overview_context = None
        self._show_cached_overviews()
        self._hide_login()
        self._check_login()
        self._show_eks_entries(self._context(), False)  # AWS data of the last context
        self._update_eks_entries()
        if self.pages.currentIndex() == 4:
            self._ensure_workloads_overview()
        if self.settings.remember_last_context and self._contexts:
            self.settings.last_context = self._context()
            self._save_settings()
        if self.pages.currentIndex() == 0:
            self._ensure_overview()
        self._leave_other_context_tab()
        self._render_pinned()

    def _leave_other_context_tab(self) -> None:
        """Move off a Details or Logs tab that belongs to the context just
        left; the tab stays open for when that context comes back."""
        current = self.viewer_tabs.currentWidget()
        if (
            self.pages.currentIndex() == 3
            and self._viewer_contexts.get(current) != self._context()
        ):
            for index in range(self.viewer_tabs.count()):
                if (
                    self._viewer_contexts.get(self.viewer_tabs.widget(index))
                    == self._context()
                ):
                    self.viewer_tabs.setCurrentIndex(index)
                    return
            self._show_page(1)

    def _hide_login(self) -> None:
        self._login_action = None
        self.login_button.setVisible(False)

    def _check_login(self) -> None:
        """Ask the cluster whether this context still needs a sign-in; the
        button appears only when it does and the kubeconfig names an AWS,
        Google Cloud or Azure sign-in."""
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
        provider = self._login_action.provider
        profile = self._login_action.profile or (
            "default" if provider == "AWS" else None
        )
        if self._login_action.interactive:
            self.login_button.setText(
                self.tr("Configure AWS credentials ({profile})").format(profile=profile)
            )
            self._set_status(
                lambda: self.tr(
                    "AWS credentials for profile {profile} are missing or invalid"
                ).format(profile=profile)
            )
        elif profile is None:
            self.login_button.setText(
                self.tr("Sign in to {provider}").format(provider=provider)
            )
            self._set_status(
                lambda: self.tr("Not signed in to {provider}").format(provider=provider)
            )
        else:
            self.login_button.setText(
                self.tr("Sign in to {provider} ({profile})").format(
                    provider=provider, profile=profile
                )
            )
            self._set_status(
                lambda: self.tr(
                    "Not signed in to {provider} (profile {profile})"
                ).format(provider=provider, profile=profile)
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
        self._update_eks_entries()  # the AWS data could not be read before

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
        self._workloads_overviews[context] = overview
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
                if column == 3 and (link := event_link(event)):
                    self._link_item(item, link)
                item.setForeground(
                    QColor(
                        themed("#985415")
                        if event.type == "Warning"
                        else themed("#242a33")
                    )
                )
                table.setItem(row, column, item)

    def _show_cached_overviews(self) -> None:
        """Another context was chosen: show what was last read from it, or
        nothing, never the numbers of the context left behind.

        The pages still load fresh data.
        """
        context = self._context()
        self._overview = self._overviews.get(context)
        if self._overview is not None:
            self._render_overview(self._overview)
        else:
            self._reset_overview()
        self._workloads_overview = self._workloads_overviews.get(context)
        self._render_workloads_overview(
            self._workloads_overview or WorkloadsOverview({})
        )

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
        self._overviews[context] = overview
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
        if self._eks_context == context and self._cluster_info is None:
            self._load_cluster_info(context)  # it failed before the sign-in

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

        notices = list(overview.warnings)
        if overview.nodes and not overview.metrics_available:
            notices.append(self.tr("Real usage unavailable: metrics-server not found."))
        page.noticeLabel.setTextFormat(Qt.TextFormat.PlainText)
        page.noticeLabel.setToolTip("")
        page.noticeLabel.setText("  ·  ".join(notices))

    def _load_nodes(self, context: str) -> None:
        """The Nodes shown under the Node Groups; when they cannot be read the
        table stays as it was."""
        self._run_action(
            get_cluster_overview,
            lambda overview: self._show_nodes(context, overview),
            context,
            on_error=lambda reason: logger.info(
                "Nodes unavailable: %s", first_line(reason)
            ),
            quiet=True,
        )

    def _show_nodes(self, context: str, overview: ClusterOverview) -> None:
        if context != self._context() or self._view != "nodegroups":
            return  # the answer of a list that is no longer open
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
                if column == 0:
                    self._link_item(item, ("Node", "", node.name))
                self.nodes_table.setItem(row, column, item)

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

    def _refresh_or_cancel(self) -> None:
        """The refresh button stops the list that is loading, and refreshes
        otherwise."""
        if self._loading(self._view):
            self._cancel_refreshes()
            self._set_status(lambda: self.tr("Loading cancelled"))
            self._sync_loading()
            return
        self.refresh()
        self._check_login()

    def _cancel_refreshes(self) -> None:
        """Give up on every list that is loading: the requests stop at once,
        and whatever they answer is ignored."""
        for view, worker in list(self._workers.items()):
            if worker.isRunning():
                self._retired.append(worker)
                del self._workers[view]
        cancel_running()

    def _refresh_running(self) -> bool:
        return any(worker.isRunning() for worker in self._retired) or any(
            self._loading(view) for view in self._workers
        )

    def _refresh_live(self) -> None:
        """Read the list on screen again, quietly, while the person is looking
        at it."""
        if (
            self.pages.currentIndex() == 1
            and self.isVisible()
            and not self.isMinimized()
            and not self._loading(self._view)
            and self._view not in EKS_VIEWS
        ):
            self.refresh(quiet=True)

    def refresh(self, *_args: object, quiet: bool = False) -> None:
        context = self._context()
        if not context:
            return
        namespace = self._list_namespace(self._view)
        key = (context, namespace, self._view)
        if self._loading(self._view):
            if self._workers[self._view].key == key:
                return
            self._cancel_refreshes()  # the person moved on: do not wait
        if key != self._shown_key:  # another context or namespace than on screen
            self._show_cached(key)
        logger.info(
            "Refreshing %s in %s (namespace %s)",
            self._view,
            context,
            namespace or "all",
        )
        view = self._view
        worker = RefreshWorker(context, namespace, view)
        worker.key = key
        self._workers[view] = worker
        # An answer for a list the person has left is kept, not shown: it appears
        # at once when they come back.
        worker.completed.connect(
            lambda namespaces, items: (
                self._answered(context, namespace, view, namespaces, items, quiet)
                if self._workers.get(view) is worker
                else None
            )
        )
        worker.failed.connect(
            lambda message: (
                self._failed(message, quiet)
                if view == self._view and self._workers.get(view) is worker
                else None
            )
        )
        worker.finished.connect(lambda: self._refresh_finished(worker))
        if not quiet:  # a background read leaves the status and the spinner be
            retry_sign_in()  # the person asked: they may have signed in elsewhere
            self._set_status(lambda: self.tr("Loading resources..."))
        worker.start()
        if not quiet:
            self._sync_loading()

    def _list_namespace(self, view: str) -> str | None:
        """The namespace a list is asked for.

        Add-ons span the cluster: the Helm releases of every namespace sit
        next to the cluster's EKS add-ons, so the default namespace must not
        hide them.
        """
        if view == "addons":
            return None
        return self.namespace_combo.currentData() or None

    def _loading(self, view: str) -> bool:
        worker = self._workers.get(view)
        return worker is not None and worker.isRunning()

    def _sync_loading(self) -> None:
        """Spin the refresh button while the list on screen loads; the context
        and namespace stay fixed while any list is loading."""
        loading = self._loading(self._view)
        self.refresh_button.setEnabled(True)
        if loading:  # the button stops the load
            self._begin_loading(self.refresh_button, self.tr("Cancel"))
        else:
            self._end_loading(self.refresh_button)

    def _show_cached(self, key: tuple[str, str | None, str]) -> None:
        """Put the last answer for this context, namespace and list on screen
        while the fresh one loads, or an empty table when there is none."""
        known = self._answers.get(key)
        if known:
            self._show_answer(key[2], *known)
        else:
            self._workloads, self._pods, self._resources = [], [], []
            self._render_rows()
        self._shown_key = key

    def _answered(
        self,
        context: str,
        namespace: str | None,
        view: str,
        namespaces: list,
        items: list,
        quiet: bool = False,
    ) -> None:
        key = (context, namespace, view)
        unchanged = self._answers.get(key) == (namespaces, items)
        self._answers[key] = (namespaces, items)
        if view == self._view:
            self._live_timer.setInterval(LIST_REFRESH_MS)  # the cluster answers
            self._hide_permission_banner()  # this list loaded: access is fine
            if quiet and unchanged and self._shown_key == key:
                return  # the table already shows exactly this: leave it be
            self._shown_key = key
            self._show_answer(view, namespaces, items)

    def _failed(self, message: str, quiet: bool) -> None:
        """A list could not be read; a background read that keeps failing is
        tried less and less often."""
        if quiet:
            self._live_timer.setInterval(
                min(self._live_timer.interval() * 2, LIST_REFRESH_MAX_MS)
            )
        self._show_error(message)

    def _show_answer(self, view: str, namespaces: list, items: list) -> None:
        selected = self._selected_identity()
        if view == "pods":
            self._show_pods(namespaces, items)
        elif view in RESOURCE_VIEWS:
            self._show_resources(namespaces, items)
        else:
            self._show_workloads(namespaces, items)
        self._reselect(selected)

    def _selected_identity(self) -> tuple[str, str, str] | None:
        """What the selected row is, to find it again when the rows change."""
        row = self._selected_row()
        if row is None:
            return None
        return (row.namespace, getattr(row, "kind", ""), row.name)

    def _reselect(self, identity: tuple[str, str, str] | None) -> None:
        """Select the row that was selected, wherever it is now; a Pod that is
        gone leaves nothing selected rather than its neighbour."""
        if identity is None:
            return
        rows = {"pods": self._pods}.get(
            self._view,
            self._resources if self._view in RESOURCE_VIEWS else self._workloads,
        )
        for index, row in enumerate(rows):
            if (row.namespace, getattr(row, "kind", ""), row.name) == identity:
                self.table.selectRow(index)
                return
        self.table.clearSelection()
        self.table.setCurrentCell(-1, -1)

    def _show_resources(self, namespaces: list, resources: list) -> None:
        logger.info(
            "Loaded %d network resource(s) in %d namespace(s)",
            len(resources),
            len(namespaces),
        )
        self._resources = resources
        self._apply_sort()
        if self._view not in EKS_VIEWS:  # not namespaced: keep the filter as it is
            self._fill_namespaces(namespaces)
        if self._view in RESOURCE_VIEWS:
            self._render_resources()
        if self._view == "nodegroups":
            self._load_nodes(self._context())

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

    def _fill_default_namespaces(self) -> None:
        """The saved default namespace, typed freely; the namespaces of the
        cluster on screen are offered as the person types."""
        edit = self.settings_ui.defaultNamespaceEdit
        edit.setText(self.settings.default_namespace)
        completer = QCompleter(sorted(self._namespaces), edit)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseSensitive)
        edit.setCompleter(completer)

    def _select_default_namespace(self) -> None:
        """Start on the namespace chosen in Settings; the list is still to be
        loaded, so it is added until the cluster names its own."""
        default = self.settings.default_namespace
        combo = self.namespace_combo
        combo.blockSignals(True)
        index = combo.findData(default) if default else 0
        if index < 0:
            combo.addItem(default, default)
            index = combo.count() - 1
        combo.setCurrentIndex(index)
        combo.blockSignals(False)

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
        if selected_namespace and index < 0:
            self._list_timer.start()  # this cluster has no such namespace: show all

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
        elif self._view in RESOURCE_VIEWS:
            self._resources.sort(
                key=lambda resource: resource_sort_key(resource, column),
                reverse=descending,
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
        if self._view == "pods":
            return self._pods
        return self._resources if self._view in RESOURCE_VIEWS else self._workloads

    @staticmethod
    def _cell_text(item: QTableWidgetItem | None) -> str:
        return item.text() if item is not None else ""

    def _selected_row(self) -> Workload | PodInfo | ClusterResource | None:
        if self._view == "pods":
            return self._selected_pod()
        if self._view in RESOURCE_VIEWS:
            return self._selected_resource()
        return self._selected_workload()

    def _kept_rows(self, rows: list) -> list:
        """The rows the table already shows for this list, to leave as they
        are; nothing when it was cleared or draws another list."""
        if self._rendered is None or self._rendered[0] != self._view:
            return []
        shown = self._rendered[1]
        return shown if self.table.rowCount() == len(shown) else []

    def _render_rows(self) -> None:
        self._rendered = None  # a full redraw: the theme, language or order changed
        # one repaint for the whole batch instead of one per cell and row
        self.table.setUpdatesEnabled(False)
        try:
            if self._view == "pods":
                self._render_pods()
                self._fit_states_column()
            elif self._view in RESOURCE_VIEWS:
                self._render_resources()
            else:
                self._render_workloads()
                self._fit_states_column()
        finally:
            self.table.setUpdatesEnabled(True)
        self._fit_name_column()

    def _fit_states_column(self) -> None:
        """READY grows to hold the squares and the count of its widest row; a
        width the person made larger is kept."""
        needed = self.table.sizeHintForColumn(3) + 2 * 8
        if needed > self.table.columnWidth(3):
            self.table.setColumnWidth(3, needed)

    def _fit_name_column(self) -> None:
        """Start each list with the whole of its names showing; after that the
        width is the person's to drag."""
        if self._view in self._name_fitted or self.table.rowCount() == 0:
            return
        self._name_fitted.add(self._view)
        self.table.resizeColumnToContents(2)
        self.table.setColumnWidth(2, min(max(self.table.columnWidth(2), 260), 700))

    def _render_resources(self) -> None:
        resources = self._resources
        kept = self._kept_rows(resources)
        self.table.setRowCount(len(resources))
        for row_index, resource in enumerate(resources):
            if row_index < len(kept) and kept[row_index] == resource:
                continue
            shown = resource.values
            if self._view in EKS_VIEWS | {"addons"}:  # the first value is a status
                shown = (self._aws_value(shown[0]), *shown[1:])
            values = (
                resource.namespace or "—",
                resource.kind,
                resource.name,
                *shown,
                resource.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor(themed("#242a33")))
                self.table.setItem(row_index, column, item)
        self._rendered = (self._view, list(resources))
        self._filter_rows()
        summaries = {
            "services": lambda: self.tr("{count} Services in {namespaces} namespaces"),
            "endpointslices": lambda: self.tr(
                "{count} Endpoint Slices in {namespaces} namespaces"
            ),
            "endpoints": lambda: self.tr(
                "{count} Endpoints in {namespaces} namespaces"
            ),
            "ingresses": lambda: self.tr(
                "{count} Ingresses in {namespaces} namespaces"
            ),
            "ingressclasses": lambda: self.tr("{count} Ingress Classes in the cluster"),
            "networkpolicies": lambda: self.tr(
                "{count} Network Policies in {namespaces} namespaces"
            ),
            "configmaps": lambda: self.tr(
                "{count} Config Maps in {namespaces} namespaces"
            ),
            "secrets": lambda: self.tr("{count} Secrets in {namespaces} namespaces"),
            "resourcequotas": lambda: self.tr(
                "{count} Resource Quotas in {namespaces} namespaces"
            ),
            "limitranges": lambda: self.tr(
                "{count} Limit Ranges in {namespaces} namespaces"
            ),
            "horizontalpodautoscalers": lambda: self.tr(
                "{count} Horizontal Pod Autoscalers in {namespaces} namespaces"
            ),
            "poddisruptionbudgets": lambda: self.tr(
                "{count} Pod Disruption Budgets in {namespaces} namespaces"
            ),
            "leases": lambda: self.tr("{count} Leases in {namespaces} namespaces"),
            "priorityclasses": lambda: self.tr(
                "{count} Priority Classes in the cluster"
            ),
            "runtimeclasses": lambda: self.tr("{count} Runtime Classes in the cluster"),
            "mutatingwebhooks": lambda: self.tr(
                "{count} Mutating Webhook Configurations in the cluster"
            ),
            "validatingwebhooks": lambda: self.tr(
                "{count} Validating Webhook Configurations in the cluster"
            ),
            "nodegroups": lambda: self.tr("{count} Node Groups in the cluster"),
            "addons": lambda: self.tr("{count} Add-ons in the cluster"),
        }
        summary = summaries[self._view]
        self._set_status(
            lambda: summary().format(
                count=len(resources), namespaces=len(self._namespaces)
            )
        )

    def _phase_label(self, phase: str) -> str:
        labels = {
            "Running": self.tr("Running"),
            "Pending": self.tr("Pending"),
            "Succeeded": self.tr("Succeeded"),
            "Failed": self.tr("Failed"),
            "Unknown": self.tr("Unknown"),
        }
        return labels.get(phase, phase)

    def _container_state_label(self, state: str) -> str:
        labels = {
            "running": self.tr("Running"),
            "pending": self.tr("Pending"),
            "error": self.tr("Error"),
            "terminated": self.tr("Terminated"),
        }
        return labels.get(state, state)

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
        kept = self._kept_rows(pods)
        self.table.setRowCount(len(pods))
        for row_index, pod in enumerate(pods):
            if row_index < len(kept) and kept[row_index] == pod:
                continue
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
                pod.owner[0] if pod.owner else "",
                pod.node,
                pod.qos,
                pod.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor(themed("#242a33")))
                if tint is not None:
                    item.setBackground(tint)
                if column == 8 and pod.owner:
                    self._link_item(item, (*pod.owner[:1], pod.namespace, pod.owner[1]))
                if column == 9 and pod.node:
                    self._link_item(item, ("Node", "", pod.node))
                if column == 3 and pod.container_states:
                    item.setData(STATES_ROLE, pod.container_states)
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    item.setData(
                        TIPS_ROLE,
                        tuple(
                            f"{name}: {self._container_state_label(state)}"
                            for name, state in zip(
                                pod.containers, pod.container_states, strict=True
                            )
                        ),
                    )
                if column == 4:
                    foreground, background = colors.get(
                        pod.phase, (themed("#a33d45"), themed("#fce9ea"))
                    )
                    item.setForeground(QColor(foreground))
                    item.setBackground(QColor(background))
                self.table.setItem(row_index, column, item)
        self._rendered = (self._view, list(pods))
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
        good = (themed("#176b58"), themed("#e5f4eb"))
        warning = (themed("#985415"), themed("#fff2de"))
        bad = (themed("#a33d45"), themed("#fce9ea"))
        muted = (themed("#505963"), themed("#eff1f3"))
        colors = {
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
        }
        kept = self._kept_rows(workloads)
        self.table.setRowCount(len(workloads))
        for row_index, workload in enumerate(workloads):
            if row_index < len(kept) and kept[row_index] == workload:
                continue
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
                workload.node_selector,
                workload.age,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setForeground(QColor(themed("#242a33")))
                if column == 3 and workload.kind != "CronJob":
                    item.setData(STATES_ROLE, workload.states)
                    item.setData(
                        TIPS_ROLE,
                        tuple(
                            self._container_state_label(state)
                            for state in workload.states
                        ),
                    )
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                if column == 4:
                    foreground, background = colors[workload.status]
                    item.setForeground(QColor(foreground))
                    item.setBackground(QColor(background))
                self.table.setItem(row_index, column, item)
        self._rendered = (self._view, list(workloads))
        self._filter_rows()
        summaries = {
            "deployments": lambda: self.tr(
                "{count} Deployments in {namespaces} namespaces"
            ),
            "statefulsets": lambda: self.tr(
                "{count} StatefulSets in {namespaces} namespaces"
            ),
            "daemonsets": lambda: self.tr(
                "{count} DaemonSets in {namespaces} namespaces"
            ),
            "replicasets": lambda: self.tr(
                "{count} ReplicaSets in {namespaces} namespaces"
            ),
            "replicationcontrollers": lambda: self.tr(
                "{count} ReplicationControllers in {namespaces} namespaces"
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
        pattern = None
        self.search_input.setToolTip("")
        if self._view not in EKS_VIEWS:
            text = self.search_input.text()
            try:
                pattern = compile_query(
                    text if self.search_regex_button.isChecked() else text.strip(),
                    self.search_case_button.isChecked(),
                    self.search_regex_button.isChecked(),
                )
            except re.error as error:  # every row stays until it compiles
                self.search_input.setToolTip(str(error))
        visible_rows = 0
        rows = self._current_rows()
        self.table.setUpdatesEnabled(False)  # hiding rows one by one relays out
        for row_index, row in enumerate(rows):
            kind = "Pod" if isinstance(row, PodInfo) else row.kind
            matches = (
                pattern is None
                or pattern.search(f"{row.namespace} {kind} {row.name}") is not None
            )
            self.table.setRowHidden(row_index, not matches)
            visible_rows += matches
        self.table.setUpdatesEnabled(True)
        self._update_workload_actions()
        template = {
            "pods": self.tr("{visible} of {total} Pods"),
            "deployments": self.tr("{visible} of {total} Deployments"),
            "statefulsets": self.tr("{visible} of {total} StatefulSets"),
            "daemonsets": self.tr("{visible} of {total} DaemonSets"),
            "replicasets": self.tr("{visible} of {total} ReplicaSets"),
            "replicationcontrollers": self.tr(
                "{visible} of {total} ReplicationControllers"
            ),
            "jobs": self.tr("{visible} of {total} Jobs"),
            "cronjobs": self.tr("{visible} of {total} CronJobs"),
            "services": self.tr("{visible} of {total} Services"),
            "endpointslices": self.tr("{visible} of {total} Endpoint Slices"),
            "endpoints": self.tr("{visible} of {total} Endpoints"),
            "ingresses": self.tr("{visible} of {total} Ingresses"),
            "ingressclasses": self.tr("{visible} of {total} Ingress Classes"),
            "networkpolicies": self.tr("{visible} of {total} Network Policies"),
            "configmaps": self.tr("{visible} of {total} Config Maps"),
            "secrets": self.tr("{visible} of {total} Secrets"),
            "resourcequotas": self.tr("{visible} of {total} Resource Quotas"),
            "limitranges": self.tr("{visible} of {total} Limit Ranges"),
            "horizontalpodautoscalers": self.tr(
                "{visible} of {total} Horizontal Pod Autoscalers"
            ),
            "poddisruptionbudgets": self.tr(
                "{visible} of {total} Pod Disruption Budgets"
            ),
            "priorityclasses": self.tr("{visible} of {total} Priority Classes"),
            "runtimeclasses": self.tr("{visible} of {total} Runtime Classes"),
            "leases": self.tr("{visible} of {total} Leases"),
            "mutatingwebhooks": self.tr(
                "{visible} of {total} Mutating Webhook Configurations"
            ),
            "validatingwebhooks": self.tr(
                "{visible} of {total} Validating Webhook Configurations"
            ),
            "nodegroups": self.tr("{visible} of {total} Node Groups"),
            "addons": self.tr("{visible} of {total} Add-ons"),
        }[self._view]
        self.summary_label.setText(
            template.format(visible=visible_rows, total=len(rows))
        )

    def _selected_workload(self) -> Workload | None:
        row = self.table.currentRow()
        if 0 <= row < len(self._workloads) and not self.table.isRowHidden(row):
            return self._workloads[row]
        return None

    def _selected_resource(self) -> ClusterResource | None:
        row = self.table.currentRow()
        if 0 <= row < len(self._resources) and not self.table.isRowHidden(row):
            return self._resources[row]
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
        for button in self.write_buttons.values():
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
        refresh_running = self._refresh_running()
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

    def _enable_links(self, table: QTableWidget) -> None:
        """Let the cells of a table that link to another resource be
        clicked."""
        table.setMouseTracking(True)
        table.cellEntered.connect(
            lambda row, column: self._hover_cell(table, row, column)
        )
        table.cellClicked.connect(
            lambda row, column: self._open_link(table, row, column)
        )

    @staticmethod
    def _hover_cell(table: QTableWidget, row: int, column: int) -> None:
        """A cell that links to another resource shows the hand."""
        item = table.item(row, column)
        linked = item is not None and item.data(LINK_ROLE) is not None
        table.viewport().setCursor(
            Qt.CursorShape.PointingHandCursor if linked else Qt.CursorShape.ArrowCursor
        )

    def _open_link(self, table: QTableWidget, row: int, column: int) -> None:
        """Open the details of the resource a cell points to."""
        item = table.item(row, column)
        link = item.data(LINK_ROLE) if item is not None else None
        if link is None:
            return
        self._open_resource(*link)

    def _open_resource(self, kind: str, namespace: str, name: str) -> None:
        self._run_action(
            get_resource_details,
            lambda result: self._show_json_dialog(f"{kind}: {name}", result),
            self._context(),
            kind,
            namespace,
            name,
        )

    def _link_item(self, item: QTableWidgetItem, link: tuple[str, str, str]) -> None:
        """Style a cell as a link to the resource `link` names."""
        font = item.font()
        font.setUnderline(True)
        item.setFont(font)
        item.setForeground(QColor(themed("#3220a0")))
        item.setData(LINK_ROLE, link)
        item.setToolTip(
            self.tr("Open {kind} {name}").format(kind=link[0], name=link[2])
        )

    def _view_details(self) -> None:
        pod = self._selected_pod() if self._view == "pods" else None
        if pod is None:
            self._view_workload_details()
            return
        self._run_action(
            get_resource_details,
            lambda result: self._show_json_dialog(
                self.tr("Pod: {name}").format(name=pod.name), result, pod
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
        workload = self._selected_row()
        if workload is None or isinstance(workload, PodInfo):
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
                    self.tr("Pod: {name}").format(name=pod.name), result, pod
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

        def show_pod_menu(position: QPoint) -> None:
            row = table.rowAt(position.y())
            if not self.settings.write_mode or row < 0:
                return
            table.selectRow(row)
            menu = QMenu(dialog)
            self._add_entries(
                menu,
                [
                    (shape, text, partial(self._after_closing, dialog, callback))
                    for shape, text, callback in self._pod_entries(pods[row])
                ],
            )
            menu.exec(table.viewport().mapToGlobal(position))

        table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        table.customContextMenuRequested.connect(show_pod_menu)
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

    def _pick_item(self, title: str, label: str, items: list[str]) -> tuple[str, bool]:
        """Ask the person to pick one of `items` in a select styled like the
        window's own filters, which a plain input dialog would not be."""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(420)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(QLabel(label))
        combo = QComboBox()
        combo.setProperty("variant", "filter")
        combo.addItems(items)
        layout.addWidget(combo)
        actions = QHBoxLayout()
        actions.addStretch()
        cancel_button = QPushButton(self.tr("Cancel"))
        cancel_button.setProperty("variant", "secondary")
        ok_button = QPushButton(self.tr("OK"))
        ok_button.setProperty("variant", "primary")
        ok_button.setDefault(True)
        cancel_button.clicked.connect(dialog.reject)
        ok_button.clicked.connect(dialog.accept)
        actions.addWidget(cancel_button)
        actions.addWidget(ok_button)
        layout.addLayout(actions)
        accepted = dialog.exec() == QDialog.DialogCode.Accepted
        return combo.currentText(), accepted

    def _choose_pod_for_logs(self, context: str, pods: list[PodInfo]) -> None:
        if not pods:
            self._show_message(
                QMessageBox.Icon.Information,
                self.tr("Logs"),
                self.tr("This workload has no Pods."),
            )
            return
        if len(pods) == 1:
            self._choose_container_for_logs(context, pods[0])
            return
        pod_names = [pod.name for pod in pods]
        pod_name, accepted = self._pick_item(
            self.tr("View logs"), self.tr("Select the Pod:"), pod_names
        )
        if accepted:
            pod = next(pod for pod in pods if pod.name == pod_name)
            self._choose_container_for_logs(context, pod)

    def _choose_container_for_logs(self, context: str, pod: PodInfo) -> None:
        # Init containers (migrations, setup) run and stop but keep their logs.
        choices = [*pod.init_containers, *pod.containers]
        if not choices:
            self._show_message(
                QMessageBox.Icon.Information,
                self.tr("Logs"),
                self.tr("Pod {name} has no containers.").format(name=pod.name),
            )
            return
        if len(choices) == 1:
            container, accepted = choices[0], True
        else:
            container, accepted = self._pick_item(
                self.tr("View logs"),
                self.tr("Select the container of {name}:").format(name=pod.name),
                choices,
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

    def _write_entries(self) -> list[tuple[str, str, Callable[[], None]]]:
        """The actions that change the cluster for the selected row; only
        offered in the write mode."""
        row = self._selected_row()
        if self._view == "pods" and isinstance(row, PodInfo):
            return self._pod_entries(row)
        if self._view == "deployments" and isinstance(row, Workload):
            return [
                ("scale", self.tr("Scale"), partial(self._scale_deployment, row)),
                ("reload", self.tr("Restart"), partial(self._restart_deployment, row)),
            ]
        if self._view == "services" and isinstance(row, ClusterResource):
            return [
                ("forward", self.tr("Forward"), partial(self._forward_service, row))
            ]
        return []

    def _pod_entries(self, pod: PodInfo) -> list[tuple[str, str, Callable[[], None]]]:
        return [
            ("shell", self.tr("Shell command"), partial(self._show_shell_command, pod)),
            ("evict", self.tr("Evict"), partial(self._evict_pod, pod)),
            ("delete", self.tr("Delete"), partial(self._delete_pod, pod)),
        ]

    @staticmethod
    def _add_entries(
        menu: QMenu, entries: list[tuple[str, str, Callable[[], None]]]
    ) -> None:
        """Add the entries to a menu like the buttons above the table: an icon
        in the accent color and the plain name."""
        accent = _pair(themed("#3220a0"))
        for shape, text, callback in entries:
            menu.addAction(_nav_icon(shape, accent), text, callback)

    @staticmethod
    def _after_closing(dialog: QDialog, callback: Callable[[], None]) -> None:
        dialog.accept()
        callback()

    def _style_box_buttons(self, box: QMessageBox) -> None:
        """Give a message box the window's own buttons: the accepting one
        filled, the others outlined, and none of the style's stock icons."""
        accepting = (QMessageBox.ButtonRole.AcceptRole, QMessageBox.ButtonRole.YesRole)
        for button in box.buttons():
            button.setIcon(QIcon())
            button.setProperty(
                "variant",
                "primary" if box.buttonRole(button) in accepting else "secondary",
            )
            # the box polished its buttons already, before the variant
            style = button.style()
            style.unpolish(button)
            style.polish(button)

    def _show_message(
        self,
        icon: QMessageBox.Icon,
        title: str,
        text: str,
        hint: str = "",
        details: str = "",
    ) -> None:
        """Tell the person something, in a box styled like the window."""
        box = QMessageBox(self)
        box.setIcon(icon)
        box.setWindowTitle(title)
        box.setText(text)
        if hint:
            box.setInformativeText(hint)
        if details:
            box.setDetailedText(details)
        ok = box.addButton(self.tr("OK"), QMessageBox.ButtonRole.AcceptRole)
        box.setDefaultButton(ok)
        self._style_box_buttons(box)
        box.exec()

    def _confirm(self, title: str, text: str, action: str) -> bool:
        """Ask before an action that changes the cluster; Cancel is the
        default."""
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle(title)
        box.setText(text)
        confirm = box.addButton(action, QMessageBox.ButtonRole.AcceptRole)
        cancel = box.addButton(self.tr("Cancel"), QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(cancel)
        self._style_box_buttons(box)
        box.exec()
        return box.clickedButton() is confirm

    def _run_write(
        self, operation: Callable[..., Any], done: str, *arguments: Any
    ) -> None:
        """Run an action that changes the cluster off the UI thread, then say
        so and refresh the list."""
        self._run_action(
            operation,
            lambda _result: self._write_done(done),
            *arguments,
            on_error=self._show_write_error,
        )

    def _write_done(self, message: str) -> None:
        logger.info(message)
        self._set_status(lambda: message)
        self.refresh()

    def _show_write_error(self, message: str) -> None:
        if self._close_when_worker_stops:
            return
        self._show_message(
            QMessageBox.Icon.Warning,
            self.tr("Action failed"),
            first_line(message),
            details=message,
        )

    def _delete_pod(self, pod: PodInfo) -> None:
        question = self.tr("Delete the Pod {name} in {namespace}?").format(
            name=pod.name, namespace=pod.namespace
        )
        if self._confirm(self.tr("Delete Pod"), question, self.tr("Delete")):
            self._run_write(
                delete_pod,
                self.tr("Deleted the Pod {name}").format(name=pod.name),
                self._context(),
                pod.namespace,
                pod.name,
            )

    def _evict_pod(self, pod: PodInfo) -> None:
        question = self.tr("Evict the Pod {name} in {namespace}?").format(
            name=pod.name, namespace=pod.namespace
        )
        if self._confirm(self.tr("Evict Pod"), question, self.tr("Evict")):
            self._run_write(
                evict_pod,
                self.tr("Evicted the Pod {name}").format(name=pod.name),
                self._context(),
                pod.namespace,
                pod.name,
            )

    def _show_shell_command(self, pod: PodInfo) -> None:
        """Show the kubectl command that opens a shell in the Pod, ready to
        paste in a terminal, for the container the person picks; the app runs
        nothing itself."""
        if not pod.containers:
            self._show_message(
                QMessageBox.Icon.Information,
                self.tr("Shell command"),
                self.tr("Pod {name} has no containers.").format(name=pod.name),
            )
            return
        context = self._context()
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Shell command"))
        dialog.setMinimumWidth(560)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(QLabel(self.tr("Container of {name}:").format(name=pod.name)))
        combo = QComboBox()
        combo.setProperty("variant", "filter")
        combo.addItems(pod.containers)
        layout.addWidget(combo)
        text = QLabel(self.tr("Run this in a terminal to open a shell:"))
        text.setWordWrap(True)
        layout.addWidget(text)
        refresh = self._add_command_views(
            dialog,
            layout,
            lambda: shell_commands(
                context, pod.namespace, pod.name, combo.currentText()
            ),
        )
        combo.currentIndexChanged.connect(refresh)
        dialog.exec()

    def _add_command_views(
        self,
        dialog: QDialog,
        layout: QVBoxLayout,
        build: Callable[[], list[tuple[str, str]]],
    ) -> Callable[[], None]:
        """Show the commands that `build` returns as (shell, command) pairs: a
        box for each, named by its shell when there is more than one
        (PowerShell and cmd on Windows), with its own Copy button, and a Close
        button at the foot.

        Returns the function that shows them again after a choice
        changed.
        """
        boxes = []
        for shell, _command in build():
            if shell:
                layout.addWidget(QLabel(shell))
            box = QPlainTextEdit()
            box.setReadOnly(True)
            box.setFont(code_font())
            box.setFixedHeight(96 if not shell else 64)
            layout.addWidget(box)
            copy_button = QPushButton(self.tr("Copy"))
            copy_button.setProperty("variant", "primary")
            copy_button.clicked.connect(
                lambda _checked=False, box=box: QApplication.clipboard().setText(
                    box.toPlainText()
                )
            )
            row = QHBoxLayout()
            row.addStretch()
            row.addWidget(copy_button)
            layout.addLayout(row)
            boxes.append(box)

        def refresh() -> None:
            for box, (_shell, command) in zip(boxes, build(), strict=True):
                box.setPlainText(command)

        close_button = QPushButton(self.tr("Close"))
        close_button.setProperty("variant", "secondary")
        close_button.clicked.connect(dialog.accept)
        footer = QHBoxLayout()
        footer.addStretch()
        footer.addWidget(close_button)
        layout.addLayout(footer)
        refresh()
        return refresh

    def _forward_service(self, service: ClusterResource) -> None:
        """Read the ports of the Service, then show the kubectl command that
        forwards one of them."""
        self._run_action(
            get_resource_details,
            lambda document: self._show_forward_command(service, document),
            self._context(),
            "Service",
            service.namespace,
            service.name,
        )

    def _show_forward_command(
        self, service: ClusterResource, document: dict[str, Any]
    ) -> None:
        """The kubectl port-forward command for a port of the Service and a
        local port the person picks, ready to paste in a terminal; the app runs
        nothing itself."""
        ports = service_ports(document)
        if not ports:
            self._show_message(
                QMessageBox.Icon.Information,
                self.tr("Forward"),
                self.tr("Service {name} has no TCP ports to forward.").format(
                    name=service.name
                ),
            )
            return
        context = self._context()
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("Forward"))
        dialog.setMinimumWidth(560)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(QLabel(self.tr("Port of {name}:").format(name=service.name)))
        combo = QComboBox()
        combo.setProperty("variant", "filter")
        for number, label in ports:
            combo.addItem(label, number)
        layout.addWidget(combo)
        layout.addWidget(QLabel(self.tr("Local port:")))
        local = QSpinBox()
        local.setProperty("variant", "filter")
        local.setRange(1, 65535)
        layout.addWidget(local)
        text = QLabel(
            self.tr("Run this in a terminal and keep it open while you use the port:")
        )
        text.setWordWrap(True)
        layout.addWidget(text)
        refresh = self._add_command_views(
            dialog,
            layout,
            lambda: forward_commands(
                context,
                service.namespace,
                service.name,
                combo.currentData(),
                local.value(),
            ),
        )

        def suggest_local_port() -> None:
            # a port below 1024 needs privileges: offer it shifted up instead
            remote = combo.currentData()
            local.setValue(remote if remote >= 1024 else remote + 8000)

        combo.currentIndexChanged.connect(suggest_local_port)
        combo.currentIndexChanged.connect(refresh)
        local.valueChanged.connect(refresh)
        suggest_local_port()
        dialog.exec()

    def _ask_replicas(self, title: str, label: str, current: int) -> tuple[int, bool]:
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumWidth(360)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setRange(0, MAX_REPLICAS)
        spin.setValue(current)
        layout.addWidget(spin)
        actions = QHBoxLayout()
        actions.addStretch()
        cancel_button = QPushButton(self.tr("Cancel"))
        cancel_button.setProperty("variant", "secondary")
        ok_button = QPushButton(self.tr("Scale"))
        ok_button.setProperty("variant", "primary")
        ok_button.setDefault(True)
        cancel_button.clicked.connect(dialog.reject)
        ok_button.clicked.connect(dialog.accept)
        actions.addWidget(cancel_button)
        actions.addWidget(ok_button)
        layout.addLayout(actions)
        accepted = dialog.exec() == QDialog.DialogCode.Accepted
        return spin.value(), accepted

    def _scale_deployment(self, workload: Workload) -> None:
        replicas, accepted = self._ask_replicas(
            self.tr("Scale Deployment"),
            self.tr("Replicas of {name} in {namespace}:").format(
                name=workload.name, namespace=workload.namespace
            ),
            workload.desired,
        )
        if accepted and replicas != workload.desired:
            self._run_write(
                scale_deployment,
                self.tr("Scaled {name} to {count} replicas").format(
                    name=workload.name, count=replicas
                ),
                self._context(),
                workload.namespace,
                workload.name,
                replicas,
            )

    def _restart_deployment(self, workload: Workload) -> None:
        question = self.tr(
            "Restart the Deployment {name} in {namespace}? Its Pods are replaced "
            "one after the other."
        ).format(name=workload.name, namespace=workload.namespace)
        if self._confirm(self.tr("Restart Deployment"), question, self.tr("Restart")):
            self._run_write(
                restart_deployment,
                self.tr("Restarting {name}").format(name=workload.name),
                self._context(),
                workload.namespace,
                workload.name,
            )

    def _save_viewer_tab(self) -> None:
        """Write the shown details or logs to a file the person picks.

        Nothing is written until they choose where.
        """
        tab = self.viewer_tabs.currentWidget()
        if tab is None:
            return
        if isinstance(tab, LogTab):
            editor = tab.ui.logText
        else:
            assert isinstance(tab, DetailTab)
            editor = tab.editor
        path, _filter = QFileDialog.getSaveFileName(
            self,
            self.tr("Save to a file"),
            str(Path.home() / tab.save_name),
        )
        if not path:
            return
        try:
            Path(path).write_text(editor.toPlainText(), encoding="utf-8")
        except OSError as error:
            logger.warning("Could not save the tab to a file: %s", error.strerror)
            self._show_message(
                QMessageBox.Icon.Warning,
                self.tr("Could not save"),
                self.tr("The file could not be written: {reason}").format(
                    reason=error.strerror or str(error)
                ),
            )
            return
        logger.info("Saved a tab to a file")

    def _add_viewer_tab(self, widget: QWidget, title: str) -> None:
        self._viewer_contexts[widget] = self._context()
        index = self.viewer_tabs.addTab(widget, title)
        self.viewer_tabs.setTabToolTip(index, title)
        self.viewer_tabs.setCurrentIndex(index)
        self._show_page(3)

    def _close_viewer_tab(self, index: int) -> None:
        editor = self.viewer_tabs.widget(index)
        self.viewer_tabs.removeTab(index)
        assert editor is not None
        self._viewer_contexts.pop(editor, None)
        if isinstance(editor, LogTab | DetailTab):
            editor.closed = True
        editor.deleteLater()
        if self.viewer_tabs.count() == 0 and self.pages.currentIndex() == 3:
            self._show_page(1)
        self._render_pinned()

    def _show_json_dialog(
        self, title: str, document: dict[str, Any], pod: PodInfo | None = None
    ) -> None:
        """Open the details of a resource in a tab; a Pod's also follow its
        live CPU and memory."""
        tab = DetailTab(title, document, live_usage=pod is not None)
        tab.link_clicked.connect(self._open_resource)
        if pod is not None:
            timer = QTimer(tab)
            timer.setInterval(USAGE_REFRESH_MS)
            timer.timeout.connect(lambda: self._refresh_usage(tab, pod))
            timer.start()
        self._add_viewer_tab(tab, title)
        if pod is not None:
            self._refresh_usage(tab, pod, True)

    def _refresh_usage(self, tab: DetailTab, pod: PodInfo, force: bool = False) -> None:
        """Take a usage sample quietly; skipped while the tab is not on
        screen."""
        if tab.closed or tab.busy:
            return
        if not force:
            on_screen = (
                self.pages.currentIndex() == 3
                and self.viewer_tabs.currentWidget() is tab
                and self.isVisible()
            )
            if not on_screen:
                return
        tab.busy = True

        def done(result: tuple[float, float] | None) -> None:
            tab.busy = False
            if not tab.closed:
                tab.add_usage(result)

        def failed(_message: str) -> None:
            tab.busy = False

        self._run_action(
            get_pod_usage,
            done,
            self._context(),
            pod.namespace,
            pod.name,
            on_error=failed,
            quiet=True,
        )

    def _show_logs_dialog(self, pod: PodInfo, container: str, logs: str) -> None:
        tab = LogTab(self._context(), pod, container, self.settings.wrap_log_lines)
        tab.ui.wrapCheck.toggled.connect(self._wrap_logs)
        tab.set_logs(logs)
        timer = QTimer(tab)
        timer.setInterval(LOG_REFRESH_MS)
        timer.timeout.connect(lambda: self._refresh_log(tab))
        timer.start()
        tab.ui.refreshButton.setIcon(_nav_icon("reload", _pair(themed("#3220a0"))))
        tab.ui.refreshButton.clicked.connect(lambda: self._refresh_log(tab, True))
        title = self.tr("Logs: {pod} / {container}").format(
            pod=pod.name, container=container
        )
        self._add_viewer_tab(tab, title)

    def _wrap_logs(self, wrap: bool) -> None:
        """Remember the choice and apply it to every open log."""
        self.settings.wrap_log_lines = wrap
        self._save_settings()
        for index in range(self.viewer_tabs.count()):
            widget = self.viewer_tabs.widget(index)
            if isinstance(widget, LogTab):
                widget.set_wrap(wrap)

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
        since = None if force else tab.last_time  # a button press reads it all again

        def done(result: str) -> None:
            tab.busy = False
            if tab.closed:
                return
            if since:
                tab.add_logs(result)
            else:
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
            *((500, since) if since else ()),
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
        for code, label in language_choices():
            form.languageCombo.addItem(label, code)
        form.languageCombo.setCurrentIndex(
            max(form.languageCombo.findData(self.settings.language), 0)
        )
        self._fill_theme_combo(self.settings.theme)
        self._fill_default_namespaces()
        form.rememberCheck.setChecked(self.settings.remember_last_context)
        form.debugCheck.setChecked(self.settings.debug_logging)
        form.updatesCheck.setChecked(self.settings.check_updates)
        form.writeModeCheck.setChecked(self.settings.write_mode)
        form.backgroundCheck.setChecked(self.settings.run_in_background)
        form.titleBarCheck.setChecked(self.settings.system_title_bar)
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
                    "Give your contexts friendlier names. "
                    "Leave a name empty to keep the original one.",
                )
            )
        else:
            form.contextsHint.setText(self.tr("No contexts were found in kubeconfig."))
        form.kubeconfigList.clear()
        form.kubeconfigList.addItems(self.settings.kubeconfig_files)
        form.loginTable.setRowCount(0)
        for program, command in self.settings.sign_in_commands.items():
            self._add_login_row(program, command)
        self._show_config_tables()
        form.noticeLabel.setText("")

    def _show_config_tables(self) -> None:
        """The kubeconfig list and the sign-in table (and their Remove buttons)
        only show while they have rows; the Add buttons are always there."""
        form = self.settings_ui
        has_files = form.kubeconfigList.count() > 0
        form.kubeconfigList.setVisible(has_files)
        form.kubeconfigRemoveButton.setVisible(has_files)
        has_commands = form.loginTable.rowCount() > 0
        form.loginTable.setVisible(has_commands)
        form.loginRemoveButton.setVisible(has_commands)

    def _apply_cluster_settings(self) -> None:
        """Tell the cluster layer which kubeconfig files to read and which
        commands sign in for programs the app does not know."""
        configure_cluster(
            self.settings.kubeconfig_files, self.settings.sign_in_commands
        )

    def _add_kubeconfig_file(self) -> None:
        path, _filter = QFileDialog.getOpenFileName(
            self, self.tr("Choose a kubeconfig file"), str(Path.home() / ".kube")
        )
        files = self.settings_ui.kubeconfigList
        if path and not files.findItems(path, Qt.MatchFlag.MatchExactly):
            files.addItem(path)
        self._show_config_tables()

    def _remove_kubeconfig_file(self) -> None:
        files = self.settings_ui.kubeconfigList
        for item in files.selectedItems():
            files.takeItem(files.row(item))
        self._show_config_tables()

    def _add_login_row(self, program: str = "", command: str = "") -> None:
        table = self.settings_ui.loginTable
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(program))
        table.setItem(row, 1, QTableWidgetItem(command))
        self._show_config_tables()

    def _remove_login_row(self) -> None:
        table = self.settings_ui.loginTable
        if table.currentRow() >= 0:
            table.removeRow(table.currentRow())
        self._show_config_tables()

    def _login_commands_from_form(self) -> dict[str, str] | None:
        """The sign-in commands in the table; None (with a notice) when one of
        them cannot be read.

        Empty rows are skipped.
        """
        table = self.settings_ui.loginTable
        commands: dict[str, str] = {}
        for row in range(table.rowCount()):
            program = self._cell_text(table.item(row, 0)).strip()
            command = self._cell_text(table.item(row, 1)).strip()
            if not program and not command:
                continue
            try:
                if not program:
                    raise ValueError("no program")
                parse_command(command)
            except ValueError:
                self.settings_ui.noticeLabel.setText(
                    self.tr("The sign-in command in row {row} is not valid.").format(
                        row=row + 1
                    )
                )
                return None
            commands[program] = command
        return commands

    def _fill_theme_combo(self, selected: str) -> None:
        """List the built-in and custom themes, choosing `selected`."""
        combo = self.settings_ui.themeCombo
        combo.blockSignals(True)
        combo.clear()
        names = {"light": self.tr("Light"), "dark": self.tr("Dark")}
        for theme in available_themes():
            combo.addItem(names.get(theme.id, theme.name), theme.id)
        index = combo.findData(selected)
        combo.setCurrentIndex(index if index >= 0 else combo.findData(DEFAULT_THEME))
        combo.blockSignals(False)
        self._update_theme_buttons()

    def _selected_theme(self) -> Theme:
        theme_id = self.settings_ui.themeCombo.currentData()
        return next(t for t in available_themes() if t.id == theme_id)

    def _update_theme_buttons(self) -> None:
        # the built-in themes are fixed; copy one with New theme to change it
        theme = self._selected_theme()
        self.settings_ui.editThemeButton.setEnabled(not theme.builtin)
        # the themes that come with the app can be edited, but they stay
        self.settings_ui.deleteThemeButton.setEnabled(can_delete_theme(theme.id))

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

    def _delete_theme(self) -> None:
        """Delete the selected custom theme after asking; if it was the one in
        use, go back to the default theme."""
        theme = self._selected_theme()
        if not can_delete_theme(theme.id):
            return
        question = self.tr("Delete the theme {name}?").format(name=theme.name)
        if not self._confirm(self.tr("Delete theme"), question, self.tr("Delete")):
            return
        try:
            delete_custom_theme(theme.id)
        except OSError as error:
            self._show_write_error(str(error))
            return
        logger.info("Deleted theme %s", theme.id)
        in_use = self.settings.theme == theme.id
        if in_use:
            self.settings.theme = DEFAULT_THEME
            self._save_settings()
        self._fill_theme_combo(self.settings.theme)
        if in_use:
            self._apply_theme()

    def _open_themes_folder(self) -> None:
        themes_directory().mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(themes_directory())))

    def _clear_cache(self) -> None:
        """Forget what was loaded and the sign-in of every cluster; pages load
        again, and the sign-in runs again, the next time they are needed."""
        logger.info("Clearing the cache")
        forget_clients()
        self._answers.clear()
        self._overviews.clear()
        self._workloads_overviews.clear()
        self._overview = None
        self._workloads_overview = None
        self._shown_key = None
        self._overview_context = None
        self._workloads_overview_context = None
        self.settings_ui.noticeLabel.setText(
            self.tr("Cache cleared. Everything loads again the next time it is needed.")
        )

    def _open_log_folder(self) -> None:
        directory = log_directory()
        directory.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(directory)))

    def _save_preferences(self) -> None:
        form = self.settings_ui
        commands = self._login_commands_from_form()
        if commands is None:
            return  # nothing is saved until every command is valid
        files = [
            form.kubeconfigList.item(row).text()
            for row in range(form.kubeconfigList.count())
        ]
        files_changed = files != self.settings.kubeconfig_files
        self.settings.kubeconfig_files = files
        self.settings.sign_in_commands = commands
        self._apply_cluster_settings()
        self.settings.default_namespace = form.defaultNamespaceEdit.text().strip()
        table = form.contextsTable
        aliases = self.settings.context_aliases
        if self._contexts:
            edited = {
                context: self._cell_text(table.item(row, 1))
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
        was_checking = self.settings.check_updates
        self.settings.check_updates = form.updatesCheck.isChecked()
        if self.settings.check_updates and not was_checking:
            self.check_updates()
        self.settings.run_in_background = form.backgroundCheck.isChecked()
        self._sync_tray()
        self.settings.system_title_bar = form.titleBarCheck.isChecked()
        self._frame.set_custom(not self.settings.system_title_bar)
        was_writing = self.settings.write_mode
        self.settings.write_mode = form.writeModeCheck.isChecked()
        if self.settings.write_mode != was_writing:
            logger.info("Write mode %s", "on" if self.settings.write_mode else "off")
            self._show_access_note()
            self._apply_view_buttons()
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
        if files_changed:
            self._load_contexts()  # the contexts come from other files now

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LanguageChange and hasattr(self, "ui"):
            self._retranslate()
        elif event.type() == QEvent.Type.WindowStateChange and hasattr(self, "_frame"):
            self._frame.refresh()
        super().changeEvent(event)

    def _show_access_note(self) -> None:
        """The note at the foot of the side menu: read-only, or the write
        mode."""
        if self.settings.write_mode:
            note = self.tr("WRITE MODE\nActions that change the cluster are on")
        else:
            note = QCoreApplication.translate(
                "MainWindow", "SECURE ACCESS\nResources in read-only mode"
            )
        self.ui.sidebarNote.setText(note)

    def _restore_designed_headers(self) -> None:
        """Give the table the columns and headers its layout has, which the
        generated retranslation sets one by one; a list with fewer columns, or
        none of its own headers, would make it fail.

        The columns of the list on screen are drawn again right after.
        """
        if self.table.columnCount() < DESIGNED_COLUMNS:
            self.table.setColumnCount(DESIGNED_COLUMNS)
        for column in range(DESIGNED_COLUMNS):
            if self.table.horizontalHeaderItem(column) is None:
                self.table.setHorizontalHeaderItem(column, QTableWidgetItem())

    def _retranslate(self) -> None:
        """Re-apply every visible text after the translator changed."""
        self._restore_designed_headers()
        self.ui.retranslateUi(self)
        self._show_access_note()
        self.search_case_button.setToolTip(self.tr("Match case"))
        self.search_regex_button.setToolTip(self.tr("Regular expression"))
        self.viewer_ui.retranslateUi(self.ui.viewerHost)
        self._show_version()
        self.overview_ui.retranslateUi(self.ui.overviewHost)
        self._render_cluster_info()
        self.settings_ui.retranslateUi(self.ui.settingsHost)
        self.workloads_ui.retranslateUi(self.ui.workloadsOverviewHost)
        if self._workloads_overview is not None:
            self._render_workloads_overview(self._workloads_overview)
        if self.pages.currentIndex() == 2:
            self._load_settings_form()
        self._apply_page_titles()
        self._render_pinned()
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

    def _show_permission_banner(self, message: str) -> None:
        action = forbidden_action(message)
        text = (
            self.tr(
                "Your user is not allowed to {action}. "
                "Ask your cluster admin for access."
            ).format(action=action)
            if action
            else self.tr(
                "Your user is not allowed to do this. "
                "Ask your cluster admin for access."
            )
        )
        self.ui.permissionLabel.setText(text)
        self.permission_banner.show()

    def _hide_permission_banner(self) -> None:
        self.permission_banner.hide()

    def show_welcome(self) -> None:
        """Greet the person on opening the app and invite them to contribute,
        unless they asked never to see this again."""
        if self.settings.welcome_dismissed:
            return
        box = QMessageBox(self)
        box.setIconPixmap(QPixmap(str(LOGO_PATH)).scaledToWidth(56))
        box.setWindowTitle(self.tr("Welcome to KubeScope"))
        box.setText(self.tr("Welcome to KubeScope"))
        box.setInformativeText(
            self.tr(
                "KubeScope is free and open source software. If it helps you, "
                "please consider contributing: star the project on GitHub, report "
                "a problem, suggest an idea, translate it into your language, send "
                "a pull request or become a sponsor."
            )
        )
        github = box.addButton(
            self.tr("Open on GitHub"), QMessageBox.ButtonRole.AcceptRole
        )
        sponsor = box.addButton(
            self.tr("Sponsor on GitHub"), QMessageBox.ButtonRole.AcceptRole
        )
        box.addButton(self.tr("Maybe later"), QMessageBox.ButtonRole.RejectRole)
        never = box.addButton(
            self.tr("Don't show again"), QMessageBox.ButtonRole.DestructiveRole
        )
        box.setDefaultButton(github)
        self._style_box_buttons(box)
        box.exec()
        if box.clickedButton() is github:
            QDesktopServices.openUrl(QUrl(PROJECT_URL))
        elif box.clickedButton() is sponsor:
            QDesktopServices.openUrl(QUrl(SPONSOR_URL))
        elif box.clickedButton() is never:
            self.settings.welcome_dismissed = True
            self._save_settings()

    def _show_action_error(self, message: str) -> None:
        if self._close_when_worker_stops:
            return  # the window is closing; the cancelled request is no news
        if is_forbidden(message):
            self._show_permission_banner(message)
            return
        info = describe_error(message)
        self._show_message(
            QMessageBox.Icon.Warning,
            self.tr("Query failed"),
            info.title,
            info.hint,
            info.details,
        )

    def _show_error(self, message: str) -> None:
        logger.info("Refresh failed: %s", first_line(message))
        if is_auth_error(message):
            self._check_login()
        if is_forbidden(message):
            self._show_permission_banner(message)
        self._workloads = []
        self._pods = []
        self._resources = []
        self._shown_key = None
        self._set_status(lambda: self._error_line(message))
        self.status_label.setToolTip(describe_error(message).details)
        self.table.setRowCount(0)
        self._filter_rows()

    def _refresh_finished(self, worker: RefreshWorker | None = None) -> None:
        if worker in self._retired:
            self._retired.remove(worker)
        self._sync_loading()
        self._finish_deferred_close()

    def _restore_geometry(self) -> None:
        """Open at the size and place the window had when it was last
        closed."""
        saved = self.settings.window_geometry
        if saved and not self.restoreGeometry(QByteArray.fromBase64(saved.encode())):
            logger.debug("The saved window geometry was not usable")

    def _remember_geometry(self) -> None:
        self.settings.window_geometry = bytes(
            self.saveGeometry().toBase64().data()
        ).decode()
        self._save_settings()

    def _sync_tray(self) -> None:
        """Show the tray icon while the setting is on and the desktop has a
        system tray; without one the window must still close for real."""
        wanted = (
            self.settings.run_in_background and QSystemTrayIcon.isSystemTrayAvailable()
        )
        if wanted and self._tray is None:
            tray = QSystemTrayIcon(self.windowIcon(), self)
            tray.setToolTip("KubeScope")
            menu = QMenu(self)
            menu.addAction(self.tr("Show KubeScope"), self.bring_to_front)
            menu.addSeparator()
            menu.addAction(self.tr("About KubeScope"), self._show_about)
            menu.addAction(self.tr("Preferences"), self._show_preferences)
            menu.addAction(self.tr("Check for updates"), self._check_updates_from_tray)
            menu.addSeparator()
            menu.addAction(self.tr("Quit"), self._quit)
            tray.setContextMenu(menu)
            tray.activated.connect(self._tray_activated)
            tray.messageClicked.connect(self.bring_to_front)
            tray.show()
            self._tray = tray
        elif not wanted and self._tray is not None:
            self._tray.hide()
            self._tray.deleteLater()
            self._tray = None
        QApplication.setQuitOnLastWindowClosed(self._tray is None)

    def _tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.bring_to_front()

    def bring_to_front(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _show_about(self) -> None:
        box = QMessageBox(self)
        box.setIconPixmap(QPixmap(str(LOGO_PATH)).scaledToWidth(56))
        box.setWindowTitle(self.tr("About KubeScope"))
        box.setText(f"KubeScope {__version__}")
        box.setInformativeText(
            "Copyright © 2026 DCO Tecnologia\n\n"
            + self.tr(
                "KubeScope is free and open source software, released under the "
                'MIT License. It is provided "as is", without warranty of any '
                "kind."
            )
            + "\n\n"
            + self.tr(
                "It is built with Qt for Python (PySide6) and Qt, under the "
                "LGPL-3.0. The licenses of the other libraries it uses are in the "
                "third-party notices."
            )
            + "\n\n"
            + self.tr(
                "Kubernetes is a registered trademark of The Linux Foundation. "
                "KubeScope is an independent project, not affiliated with or "
                "endorsed by it."
            )
        )
        github = box.addButton(
            self.tr("Open on GitHub"), QMessageBox.ButtonRole.AcceptRole
        )
        license_button = box.addButton(
            self.tr("License"), QMessageBox.ButtonRole.AcceptRole
        )
        notices = box.addButton(
            self.tr("Third-party notices"), QMessageBox.ButtonRole.AcceptRole
        )
        box.addButton(self.tr("Close"), QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(github)
        self._style_box_buttons(box)
        box.exec()
        if box.clickedButton() is github:
            QDesktopServices.openUrl(QUrl(PROJECT_URL))
        elif box.clickedButton() is license_button:
            self._open_license()
        elif box.clickedButton() is notices:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(NOTICES_PATH)))

    def _show_preferences(self) -> None:
        self.bring_to_front()
        self._show_page(2)

    def _check_updates_from_tray(self) -> None:
        self.bring_to_front()
        self.check_updates()

    def _quit(self) -> None:
        """Quit for real, which closing the window does not while it lives in
        the tray."""
        self._quitting = True
        QApplication.setQuitOnLastWindowClosed(True)
        self.close()

    def closeEvent(self, event: QCloseEvent) -> None:
        self._remember_geometry()
        if self._tray is not None and not self._quitting:
            logger.info("Closing to the system tray")
            self.hide()
            event.ignore()
            return
        refresh_running = self._refresh_running()
        actions_running = any(worker.isRunning() for worker in self._action_workers)
        if refresh_running or actions_running:
            logger.info("Closing while requests are running; stopping them")
            # Stop the cluster requests and the cloud CLIs so the workers return at
            # once, hide the window so closing feels instant, and quit when the
            # last one is done.
            self._close_when_worker_stops = True
            QApplication.setQuitOnLastWindowClosed(False)
            cancel_running()
            self.hide()
            event.ignore()
            return
        super().closeEvent(event)
