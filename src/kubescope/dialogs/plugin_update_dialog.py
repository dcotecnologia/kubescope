from collections.abc import Callable

from kubescope.sdk.models import ClusterResource
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope import cloud_addons, plugin_updates
from kubescope.cluster import ClusterError


class PluginUpdateDialog(QDialog):
    """Asks for what an update needs and shows the exact command it will run.

    An EKS add-on takes a version (from the ones EKS offers) and what to
    do with the fields that were changed by hand; a Helm release takes
    the chart, where to read it from, a version and its values.
    Accepting it leaves the command in `arguments`; the window runs it.
    """

    def __init__(
        self,
        parent: QWidget | None,
        context: str,
        row: ClusterResource,
        versions: list[str],
        repository: str = "",
        target: tuple[str, str] = ("", ""),
    ) -> None:
        super().__init__(parent)
        self.context = context
        self.row = row
        self.arguments: list[str] = []
        self.is_eks = row.kind == "Addon"
        self.is_aks = row.kind == cloud_addons.AKS_KIND
        self.target = target  # the name and resource group of an AKS cluster
        self.setWindowTitle(self.tr("Update {name}").format(name=row.name))
        self.setMinimumWidth(640)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)
        current = row.values[1] if len(row.values) > 1 else ""
        form.addRow(self.tr("Installed"), QLabel(current))
        self._builder: Callable[[], list[str]]
        if self.is_eks or self.is_aks:
            self.eks_version = QComboBox()
            self.eks_version.setEditable(True)
            self.eks_version.setProperty("variant", "filter")
            latest = row.values[2] if len(row.values) > 2 else ""
            self.eks_version.addItems(versions)
            if latest in versions:
                self.eks_version.setCurrentIndex(versions.index(latest))
            self.conflicts = QComboBox()
            self.conflicts.setProperty("variant", "filter")
            for option, text in (
                ("NONE", self.tr("Stop if a field was changed by hand")),
                ("OVERWRITE", self.tr("Overwrite the fields changed by hand")),
                ("PRESERVE", self.tr("Keep the fields changed by hand")),
            ):
                self.conflicts.addItem(text, option)
            form.addRow(self.tr("Update to version"), self.eks_version)
            if self.is_eks:  # only EKS decides what to do with the fields changed
                form.addRow(self.tr("If a field was changed"), self.conflicts)
            self.eks_version.currentTextChanged.connect(self._preview)
            self.conflicts.currentIndexChanged.connect(self._preview)
            self._builder = self._eks_arguments
        else:
            self.chart = QLineEdit(row.name)
            self.repository = QLineEdit()
            self.repository.setPlaceholderText(self.tr("https://charts.example.com"))
            self.helm_version = QComboBox()
            self.helm_version.setEditable(True)
            self.helm_version.addItems(versions)
            self.helm_version.setCurrentIndex(0 if versions else -1)
            self.repository.setText(repository)
            self.values_file = QLineEdit()
            self.values_file.setPlaceholderText(self.tr("none"))
            self.helm_version.setProperty("variant", "filter")
            for edit in (self.chart, self.repository, self.values_file):
                edit.setProperty("variant", "filter")
            self.reuse = QCheckBox(self.tr("Keep the values the release has"))
            self.reuse.setChecked(True)
            form.addRow(self.tr("Chart"), self.chart)
            form.addRow(self.tr("Repository"), self.repository)
            form.addRow(self.tr("Chart version"), self.helm_version)
            form.addRow(self.tr("Values file"), self.values_file)
            form.addRow("", self.reuse)
            for edit in (self.chart, self.repository, self.values_file):
                edit.textChanged.connect(self._preview)
            self.helm_version.currentTextChanged.connect(self._preview)
            self.reuse.toggled.connect(self._preview)
            self._builder = self._helm_arguments
            note = QLabel(
                self.tr(
                    "Helm does not keep where a chart came from: give the chart as "
                    "repo/name or oci://..., or its name with the repository address."
                )
            )
            note.setWordWrap(True)
            layout.addWidget(note)
        self.command = QPlainTextEdit()
        self.command.setReadOnly(True)
        self.command.setMaximumHeight(90)
        layout.addWidget(QLabel(self.tr("This command will run:")))
        layout.addWidget(self.command)
        self.problem = QLabel()
        self.problem.setProperty("variant", "muted")
        self.problem.setWordWrap(True)
        layout.addWidget(self.problem)
        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self.update_button = QPushButton(self.tr("Update"))
        self.update_button.setProperty("variant", "primary")
        self.update_button.clicked.connect(self.accept)
        cancel = QPushButton(self.tr("Cancel"))
        cancel.setProperty("variant", "secondary")
        cancel.setDefault(True)
        cancel.clicked.connect(self.reject)
        buttons.addWidget(cancel)
        buttons.addWidget(self.update_button)
        layout.addLayout(buttons)
        self._preview()

    def _eks_arguments(self) -> list[str]:
        if self.is_aks:
            return cloud_addons.aks_update_arguments(
                *self.target, self.row.name, self.eks_version.currentText().strip()
            )
        return plugin_updates.eks_update_arguments(
            self.context,
            self.row.name,
            self.eks_version.currentText().strip(),
            self.conflicts.currentData(),
        )

    def _helm_arguments(self) -> list[str]:
        return plugin_updates.helm_upgrade_arguments(
            self.context,
            self.row.namespace,
            self.row.name,
            self.chart.text().strip(),
            self.helm_version.currentText().strip(),
            self.repository.text().strip(),
            self.reuse.isChecked(),
            self.values_file.text().strip(),
        )

    def _preview(self, *_args: object) -> None:
        try:
            arguments = self._builder()
        except ClusterError as error:
            self.arguments = []
            self.command.setPlainText("")
            self.problem.setText(str(error))
            self.update_button.setEnabled(False)
            return
        self.command.setPlainText(plugin_updates.commands(arguments))
        program = arguments[0]
        if plugin_updates.program_missing(program):  # shown, but it cannot run here
            self.arguments = []
            self.problem.setText(
                self.tr(
                    "{program} is not installed, so KubeScope cannot run this. "
                    "Install it, or copy the command and run it where it is."
                ).format(program=program)
            )
            self.update_button.setEnabled(False)
            return
        self.arguments = arguments
        self.problem.setText("")
        self.update_button.setEnabled(True)
