import logging
import json
from typing import Any, Callable

from PySide6.QtCore import QThread, QSize, Signal, Qt
from PySide6.QtGui import QCloseEvent, QColor
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QMainWindow,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from kubectl_gui.cluster import (
    KubectlError,
    get_pod_logs,
    get_resource_details,
    get_workload_pods,
    get_workloads,
    list_contexts,
)
from kubectl_gui.models import PodInfo, Workload

logger = logging.getLogger(__name__)


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
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("KubeScope | Workloads")
        self.setMinimumSize(980, 640)
        self._worker: RefreshWorker | None = None
        self._action_workers: list[ActionWorker] = []
        self._close_when_worker_stops = False
        self._workloads: list[Workload] = []
        self._build_ui()
        self._load_contexts()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setObjectName("topBar")
        top_bar.setFixedHeight(46)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(18, 0, 22, 0)
        top_layout.setSpacing(12)
        brand = QLabel("KUBESCOPE")
        brand.setObjectName("topBrand")
        top_layout.addWidget(brand)
        top_layout.addStretch(1)
        context_label = QLabel("CONTEXTO")
        context_label.setObjectName("topCaption")
        top_layout.addWidget(context_label)
        self.context_combo = QComboBox()
        self.context_combo.setObjectName("contextCombo")
        self.context_combo.setMinimumWidth(220)
        self.context_combo.setToolTip("Kubernetes context from your kubeconfig")
        top_layout.addWidget(self.context_combo)
        access_label = QLabel("SOMENTE LEITURA")
        access_label.setObjectName("topAccess")
        top_layout.addWidget(access_label)
        root_layout.addWidget(top_bar)

        shell = QHBoxLayout()
        shell.setContentsMargins(0, 0, 0, 0)
        shell.setSpacing(0)
        root_layout.addLayout(shell, 1)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(252)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(24, 22, 18, 18)
        sidebar_layout.setSpacing(8)
        sidebar_brand = QLabel("KubeScope")
        sidebar_brand.setObjectName("sidebarBrand")
        sidebar_subtitle = QLabel("Kubernetes console")
        sidebar_subtitle.setObjectName("sidebarSubtitle")
        sidebar_layout.addWidget(sidebar_brand)
        sidebar_layout.addWidget(sidebar_subtitle)
        sidebar_layout.addSpacing(28)
        nav_section = QLabel("MONITORAMENTO")
        nav_section.setObjectName("navSection")
        sidebar_layout.addWidget(nav_section)
        workloads_nav = QPushButton("Workloads")
        workloads_nav.setObjectName("activeNav")
        workloads_nav.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        )
        workloads_nav.setIconSize(QSize(16, 16))
        workloads_nav.setMinimumHeight(42)
        workloads_nav.setEnabled(False)
        sidebar_layout.addWidget(workloads_nav)
        sidebar_layout.addStretch(1)
        sidebar_rule = QFrame()
        sidebar_rule.setObjectName("sidebarRule")
        sidebar_rule.setFrameShape(QFrame.Shape.HLine)
        sidebar_layout.addWidget(sidebar_rule)
        sidebar_note = QLabel("ACESSO SEGURO\nRecursos em modo somente leitura")
        sidebar_note.setObjectName("sidebarNote")
        sidebar_layout.addWidget(sidebar_note)
        shell.addWidget(sidebar)

        page = QWidget()
        page.setObjectName("page")
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        page_header = QWidget()
        page_header.setObjectName("pageHeader")
        page_header_layout = QHBoxLayout(page_header)
        page_header_layout.setContentsMargins(32, 12, 32, 12)
        title_block = QVBoxLayout()
        title_block.setSpacing(3)
        title = QLabel("Workloads")
        title.setObjectName("pageTitle")
        subtitle = QLabel("Deployments, StatefulSets e DaemonSets do cluster")
        subtitle.setObjectName("muted")
        title_block.addWidget(title)
        title_block.addWidget(subtitle)
        page_header_layout.addLayout(title_block)
        page_header_layout.addStretch(1)
        profile_label = QLabel("RO")
        profile_label.setObjectName("profileBadge")
        profile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_label.setFixedSize(36, 36)
        page_header_layout.addWidget(profile_label)
        page_layout.addWidget(page_header)

        work_area = QWidget()
        work_area.setObjectName("workArea")
        layout = QVBoxLayout(work_area)
        layout.setContentsMargins(32, 24, 32, 22)
        layout.setSpacing(14)

        filters = QHBoxLayout()
        filters.setSpacing(12)
        namespace_label = QLabel("NAMESPACE")
        namespace_label.setObjectName("filterLabel")
        filters.addWidget(namespace_label)
        self.namespace_combo = QComboBox()
        self.namespace_combo.setObjectName("filterControl")
        self.namespace_combo.setMinimumWidth(170)
        self.namespace_combo.addItem("All namespaces", "")
        filters.addWidget(self.namespace_combo)
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Buscar por nome ou namespace...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumWidth(240)
        self.search_input.setMaximumWidth(300)
        filters.addWidget(self.search_input)
        filters.addStretch(1)
        self.refresh_button = QPushButton("Atualizar")
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        )
        self.refresh_button.clicked.connect(self.refresh)
        filters.addWidget(self.refresh_button)
        layout.addLayout(filters)

        self.summary_label = QLabel("0 workloads")
        self.summary_label.setObjectName("summaryLabel")
        summary_row = QHBoxLayout()
        summary_row.addWidget(self.summary_label)
        summary_row.addStretch(1)
        self.pods_button = QPushButton("Pods")
        self.pods_button.setObjectName("secondaryButton")
        self.pods_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        )
        self.pods_button.setToolTip("Ver Pods do workload selecionado")
        self.pods_button.clicked.connect(self._view_workload_pods)
        self.details_button = QPushButton("Detalhes")
        self.details_button.setObjectName("secondaryButton")
        self.details_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        )
        self.details_button.setToolTip("Ver os detalhes JSON do workload selecionado")
        self.details_button.clicked.connect(self._view_workload_details)
        self.logs_button = QPushButton("Logs")
        self.logs_button.setObjectName("secondaryButton")
        self.logs_button.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView)
        )
        self.logs_button.setToolTip("Ver logs de um Pod do workload selecionado")
        self.logs_button.clicked.connect(self._view_workload_logs)
        for button in (self.pods_button, self.details_button, self.logs_button):
            button.setEnabled(False)
            summary_row.addWidget(button)
        layout.addLayout(summary_row)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["NAMESPACE", "TIPO", "NOME", "PRONTOS", "STATUS", "IDADE"]
        )
        self.table.setObjectName("workloadTable")
        self.table.setAlternatingRowColors(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self._update_workload_actions)
        self.table.cellDoubleClicked.connect(
            lambda _row, _column: self._view_workload_details()
        )
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(58)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        for column, width in ((0, 160), (1, 150), (3, 110), (4, 150), (5, 90)):
            self.table.setColumnWidth(column, width)
        layout.addWidget(self.table, 1)

        footer = QHBoxLayout()
        self.status_label = QLabel("Selecione um contexto para carregar os workloads")
        self.status_label.setObjectName("muted")
        footer.addWidget(self.status_label)
        footer.addStretch(1)
        footer_note = QLabel("Dados consultados via kubectl")
        footer_note.setObjectName("muted")
        footer.addWidget(footer_note)
        layout.addLayout(footer)
        page_layout.addWidget(work_area, 1)
        shell.addWidget(page, 1)
        self.setCentralWidget(root)

        self.context_combo.currentTextChanged.connect(self.refresh)
        self.namespace_combo.currentIndexChanged.connect(self.refresh)
        self.search_input.textChanged.connect(self._filter_rows)
        self.setStyleSheet(
            """
            QMainWindow, QWidget#page { background: #f7f7fa; color: #20232a; }
            QWidget#topBar { background: #06234a; }
            QLabel#topBrand {
                color: #ffffff; font-size: 13px; font-weight: 700;
                padding: 0 12px; background: #123764; min-height: 46px;
            }
            QLabel#topCaption { color: #b8c7dc; font-size: 9px; font-weight: 700; }
            QLabel#topAccess { color: #d2deec; font-size: 9px; font-weight: 700; }
            QComboBox#contextCombo {
                background: #0d315d; color: #ffffff; border: 1px solid #2d5077;
                border-radius: 4px; min-height: 30px; padding: 0 9px; font-size: 11px;
            }
            QWidget#sidebar { background: #ffffff; border-right: 1px solid #e1e3e9; }
            QLabel#sidebarBrand { color: #16375f; font-size: 19px; font-weight: 700; }
            QLabel#sidebarSubtitle { color: #4f5966; font-size: 11px; }
            QLabel#navSection, QLabel#filterLabel {
                color: #535d69; font-size: 9px; font-weight: 700;
            }
            QPushButton#activeNav {
                text-align: left; color: #3220a0; background: #f3f1f9;
                border: 0; border-right: 3px solid #3220a0; border-radius: 0;
                padding: 0 12px; font-size: 12px; font-weight: 700;
            }
            QPushButton#activeNav:disabled { color: #3220a0; }
            QFrame#sidebarRule { color: #e6e7ed; }
            QLabel#sidebarNote { color: #4d5866; font-size: 10px; line-height: 1.4; }
            QWidget#pageHeader { background: #ffffff; border-bottom: 1px solid #e4e5eb; }
            QLabel#pageTitle { color: #17191e; font-size: 22px; font-weight: 700; }
            QLabel#muted { color: #4f5966; font-size: 11px; }
            QLabel#profileBadge {
                color: #4d35a8; background: #eee9f7; border-radius: 5px;
                font-size: 12px; font-weight: 700;
            }
            QComboBox#filterControl, QLineEdit#searchInput, QPushButton#refreshButton {
                background: #ffffff; border: 1px solid #d9dce4; border-radius: 5px;
                min-height: 36px; padding: 0 10px; font-size: 11px;
            }
            QComboBox#filterControl:hover, QLineEdit#searchInput:focus {
                border-color: #6252b5;
            }
            QComboBox#filterControl:disabled { color: #414852; background: #ffffff; }
            QComboBox#contextCombo:disabled { color: #ffffff; }
            QPushButton#refreshButton {
                background: #3020a5; color: #ffffff; border: 0;
                font-weight: 700; padding: 0 16px;
            }
            QPushButton#refreshButton:hover { background: #4030b8; }
            QPushButton#secondaryButton {
                background: #ffffff; color: #3220a0; border: 1px solid #d9dce4;
                border-radius: 5px; min-height: 32px; padding: 0 10px;
                font-size: 11px; font-weight: 600;
            }
            QPushButton#secondaryButton:hover:enabled {
                background: #f3f1f9; border-color: #a9a0d6;
            }
            QPushButton#secondaryButton:disabled { color: #7b8089; }
            QLabel#summaryLabel { color: #4f5966; font-size: 11px; font-weight: 600; }
            QTableWidget#workloadTable {
                background: #ffffff; color: #242a33;
                border: 1px solid #dfe2e9; border-radius: 5px;
                gridline-color: #e8e9ee; selection-background-color: #f0edfa;
                selection-color: #28213f;
            }
            QHeaderView::section {
                background: #fbfbfc; color: #3c4149; border: 0;
                border-bottom: 1px solid #dfe2e9; padding: 10px 8px;
                font-size: 9px; font-weight: 700;
            }
            QTableWidget#workloadTable::item {
                color: #242a33; padding: 6px 8px; border-bottom: 1px solid #e8e9ee;
            }
            """
        )

    def _load_contexts(self) -> None:
        try:
            contexts, active_context = list_contexts()
        except KubectlError as error:
            self.status_label.setText(f"Could not load kubeconfig: {error}")
            self.context_combo.setEnabled(False)
            self.namespace_combo.setEnabled(False)
            self.refresh_button.setEnabled(False)
            return

        self.context_combo.addItems(contexts)
        if active_context in contexts:
            self.context_combo.setCurrentText(active_context)
        if not contexts:
            self.status_label.setText("No contexts found in kubeconfig")
            self.refresh_button.setEnabled(False)
            return
        self.refresh()

    def refresh(self, *_args: object) -> None:
        context = self.context_combo.currentText()
        if not context or (self._worker is not None and self._worker.isRunning()):
            return
        namespace = self.namespace_combo.currentData() or None
        self.refresh_button.setEnabled(False)
        self.context_combo.setEnabled(False)
        self.namespace_combo.setEnabled(False)
        self.status_label.setText("Loading resources...")
        self._worker = RefreshWorker(context, namespace)
        self._worker.completed.connect(self._show_workloads)
        self._worker.failed.connect(self._show_error)
        self._worker.finished.connect(self._refresh_finished)
        self._worker.start()

    def _show_workloads(self, namespaces: list, workloads: list) -> None:
        self._workloads = workloads
        selected_namespace = self.namespace_combo.currentData()
        self.namespace_combo.blockSignals(True)
        self.namespace_combo.clear()
        self.namespace_combo.addItem("All namespaces", "")
        for namespace in namespaces:
            self.namespace_combo.addItem(namespace, namespace)
        index = self.namespace_combo.findData(selected_namespace)
        self.namespace_combo.setCurrentIndex(max(index, 0))
        self.namespace_combo.blockSignals(False)

        self.table.setRowCount(len(workloads))
        for row_index, workload in enumerate(workloads):
            values = (
                workload.namespace,
                workload.kind,
                workload.name,
                f"{workload.ready}/{workload.desired}",
                {
                    "Healthy": "Saudável",
                    "Degraded": "Degradado",
                    "Unavailable": "Indisponível",
                    "Scaled to zero": "Zero réplicas",
                }[workload.status],
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
        self.status_label.setText(
            f"{len(workloads)} workloads em {len(namespaces)} namespaces"
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
            f"{visible_rows} de {len(self._workloads)} workloads"
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
    ) -> None:
        if self._close_when_worker_stops:
            return
        worker = ActionWorker(operation, arguments)
        self._action_workers.append(worker)
        worker.completed.connect(on_success)
        worker.failed.connect(self._show_action_error)
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
        context = self.context_combo.currentText()
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
            self.context_combo.currentText(),
            workload.kind,
            workload.namespace,
            workload.name,
        )

    def _view_workload_logs(self) -> None:
        workload = self._selected_workload()
        if workload is None:
            return
        context = self.context_combo.currentText()
        self._run_action(
            get_workload_pods,
            lambda result: self._choose_pod_for_logs(context, result),
            context,
            workload,
        )

    def _show_pods_dialog(self, workload: Workload, pods: list[PodInfo]) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Pods de {workload.name}")
        dialog.setMinimumSize(760, 420)
        layout = QVBoxLayout(dialog)
        heading = QLabel(f"{len(pods)} Pods em {workload.namespace} / {workload.name}")
        heading.setObjectName("summaryLabel")
        layout.addWidget(heading)

        table = QTableWidget(len(pods), 5)
        table.setHorizontalHeaderLabels(
            ["NOME", "PRONTOS", "FASE", "CONTAINERS", "IDADE"]
        )
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
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
        layout.addWidget(table, 1)

        actions = QHBoxLayout()
        details_button = QPushButton("Detalhes do Pod")
        logs_button = QPushButton("Ver logs")
        close_button = QPushButton("Fechar")
        details_button.setEnabled(False)
        logs_button.setEnabled(False)
        actions.addWidget(details_button)
        actions.addWidget(logs_button)
        actions.addStretch(1)
        actions.addWidget(close_button)
        layout.addLayout(actions)

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
            self._run_action(
                get_resource_details,
                lambda result: self._show_json_dialog(f"Pod: {pod.name}", result),
                self.context_combo.currentText(),
                "Pod",
                pod.namespace,
                pod.name,
            )

        def show_pod_logs() -> None:
            pod = selected_pod()
            if pod is not None:
                self._choose_container_for_logs(self.context_combo.currentText(), pod)

        table.itemSelectionChanged.connect(update_pod_actions)
        table.cellDoubleClicked.connect(lambda _row, _column: show_pod_details())
        details_button.clicked.connect(show_pod_details)
        logs_button.clicked.connect(show_pod_logs)
        close_button.clicked.connect(dialog.accept)
        if not pods:
            heading.setText("Nenhum Pod associado a este workload")
        dialog.exec()

    def _choose_pod_for_logs(self, context: str, pods: list[PodInfo]) -> None:
        if not pods:
            QMessageBox.information(self, "Logs", "Este workload não possui Pods.")
            return
        pod_names = [pod.name for pod in pods]
        pod_name, accepted = QInputDialog.getItem(
            self, "Ver logs", "Selecione o Pod:", pod_names, 0, False
        )
        if accepted:
            pod = next(pod for pod in pods if pod.name == pod_name)
            self._choose_container_for_logs(context, pod)

    def _choose_container_for_logs(self, context: str, pod: PodInfo) -> None:
        if not pod.containers:
            QMessageBox.information(
                self, "Logs", f"O Pod {pod.name} não possui containers."
            )
            return
        container, accepted = QInputDialog.getItem(
            self,
            "Ver logs",
            f"Selecione o container de {pod.name}:",
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

    def _show_json_dialog(self, title: str, document: dict[str, Any]) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setMinimumSize(760, 540)
        layout = QVBoxLayout(dialog)
        content = QPlainTextEdit()
        content.setReadOnly(True)
        content.setPlainText(json.dumps(document, ensure_ascii=False, indent=2))
        layout.addWidget(content, 1)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()

    def _show_logs_dialog(self, pod: PodInfo, container: str, logs: str) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Logs: {pod.name} / {container}")
        dialog.setMinimumSize(800, 540)
        layout = QVBoxLayout(dialog)
        content = QPlainTextEdit()
        content.setReadOnly(True)
        content.setPlainText(logs or "Nenhuma linha de log retornada.")
        layout.addWidget(content, 1)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()

    def _show_action_error(self, message: str) -> None:
        QMessageBox.warning(self, "Falha na consulta", message)

    def _show_error(self, message: str) -> None:
        self._workloads = []
        self.status_label.setText(f"Could not load workloads: {message}")
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
            self.status_label.setText("Finishing the current cluster request...")
            self._update_workload_actions()
            event.ignore()
            return
        super().closeEvent(event)
