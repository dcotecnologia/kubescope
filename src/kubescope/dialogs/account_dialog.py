import logging
from collections.abc import Mapping
from functools import partial

from PySide6.QtCore import QCoreApplication, QThread, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope import integrations
from kubescope.integrations import Account, Found, IntegrationError

logger = logging.getLogger(__name__)
translate = QCoreApplication.translate

# The labels of the fields, written out so that they can be translated.
LABELS = {
    "AWS profile (instead of keys)": lambda: translate(
        "AccountDialog", "AWS profile (instead of keys)"
    ),
    "Access key ID": lambda: translate("AccountDialog", "Access key ID"),
    "Secret access key": lambda: translate("AccountDialog", "Secret access key"),
    "Session token": lambda: translate("AccountDialog", "Session token"),
    "Regions (comma separated)": lambda: translate(
        "AccountDialog", "Regions (comma separated)"
    ),
    "Tenant ID": lambda: translate("AccountDialog", "Tenant ID"),
    "Client ID": lambda: translate("AccountDialog", "Client ID"),
    "Client secret": lambda: translate("AccountDialog", "Client secret"),
    "Subscription ID": lambda: translate("AccountDialog", "Subscription ID"),
    "Project ID": lambda: translate("AccountDialog", "Project ID"),
    "Service account key (JSON file)": lambda: translate(
        "AccountDialog", "Service account key (JSON file)"
    ),
}


def label_of(text: str) -> str:
    return LABELS[text]() if text in LABELS else text


class DiscoverWorker(QThread):
    """Asks the cloud for its clusters off the UI thread."""

    done = Signal(list)
    failed = Signal(str)

    def __init__(self, account: Account, values: Mapping[str, str]) -> None:
        super().__init__()
        self.account = account
        self.values = dict(values)

    def run(self) -> None:
        try:
            self.done.emit(integrations.discover(self.account, self.values))
        except IntegrationError as error:
            self.failed.emit(str(error))
        except Exception:
            logger.exception("Looking for the clusters of %s failed", self.account.id)
            self.failed.emit(translate("AccountDialog", "Something went wrong."))


class AccountDialog(QDialog):
    """Add a cloud account, or type its keys again: the fields of the cloud,
    the clusters it lists and the ones to add."""

    def __init__(
        self,
        provider: str,
        account: Account | None = None,
        parent: QWidget | None = None,
        profile: str = "",
    ) -> None:
        super().__init__(parent)
        self.provider = integrations.PROVIDERS[provider]
        self.account = account or Account(
            integrations.new_account_id(provider), provider, ""
        )
        self.editing = account is not None
        self.found: list[Found] = []
        self._worker: DiscoverWorker | None = None
        self._edits: dict[str, QLineEdit] = {}
        self.setWindowTitle(self.provider.name)
        self.setModal(True)
        self.resize(520, 560)
        saved = integrations.values_of(self.account)
        if profile and account is None:  # an AWS profile the person picked
            saved = {**saved, "profile": profile}

        self.name_edit = QLineEdit(self.account.name or profile or self.provider.name)
        self.name_edit.setProperty("variant", "filter")
        self.name_edit.setEnabled(not self.editing)
        self.mode = QComboBox()
        self.mode.setProperty("variant", "filter")
        self.form = QFormLayout()
        self.form.addRow(translate("AccountDialog", "Name"), self.name_edit)
        if provider == "aws":
            self.mode.addItem(translate("AccountDialog", "AWS profile"), "profile")
            self.mode.addItem(translate("AccountDialog", "Access keys"), "keys")
            self.mode.setCurrentIndex(0 if saved.get("profile") or not saved else 1)
            self.form.addRow(translate("AccountDialog", "Sign in with"), self.mode)
        for item in self.provider.fields:
            self._add_field(item, saved)
        self.mode.currentIndexChanged.connect(self._show_mode)

        self.find_button = QPushButton(translate("AccountDialog", "Find clusters"))
        self.find_button.setProperty("variant", "secondary")
        self.find_button.clicked.connect(self._find)
        self.status = QLabel()
        self.status.setProperty("variant", "muted")
        self.status.setWordWrap(True)
        self.clusters = QListWidget()
        self.clusters.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.add_button = QPushButton(translate("AccountDialog", "Add clusters"))
        self.add_button.setProperty("variant", "primary")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.accept)
        cancel = QPushButton(translate("AccountDialog", "Cancel"))
        cancel.setProperty("variant", "secondary")
        cancel.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addWidget(self.find_button)
        buttons.addStretch(1)
        buttons.addWidget(cancel)
        buttons.addWidget(self.add_button)
        layout = QVBoxLayout(self)
        layout.addLayout(self.form)
        layout.addWidget(self.status)
        layout.addWidget(self.clusters, 1)
        layout.addLayout(buttons)
        self._show_mode()

    def _add_field(self, item: integrations.Field, saved: Mapping[str, str]) -> None:
        edit = QLineEdit(saved.get(item.key, item.default))
        edit.setProperty("variant", "filter")
        if item.secret:
            edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._edits[item.key] = edit
        label = label_of(item.label)
        if item.key == "profile":
            profiles = QComboBox()
            profiles.setProperty("variant", "filter")
            profiles.setEditable(True)
            for name, account in integrations.aws_profiles():
                profiles.addItem(f"{name}  ({account})" if account else name, name)
            profiles.setCurrentIndex(max(profiles.findData(edit.text()), 0))
            self._profiles = profiles
            self.form.addRow(label, profiles)
        elif item.file:
            row = QWidget()
            box = QHBoxLayout(row)
            box.setContentsMargins(0, 0, 0, 0)
            browse = QPushButton(translate("AccountDialog", "Browse"))
            browse.setProperty("variant", "secondary")
            browse.clicked.connect(partial(self._browse, edit))
            box.addWidget(edit)
            box.addWidget(browse)
            self.form.addRow(label, row)
        else:
            self.form.addRow(label, edit)

    def _browse(self, edit: QLineEdit) -> None:
        path, _filter = QFileDialog.getOpenFileName(
            self, translate("AccountDialog", "Choose the key file"), "", "JSON (*.json)"
        )
        if path:
            edit.setText(path)

    def _show_mode(self) -> None:
        """The profile or the keys, by how the AWS account signs in."""
        if self.provider.id != "aws":
            self.mode.setVisible(False)
            return
        profile = self.mode.currentData() == "profile"
        for key, edit in self._edits.items():
            if key in ("access_key_id", "secret_access_key", "session_token"):
                self._row_visible(edit, not profile)
        self._row_visible(self._profiles, profile)

    def _row_visible(self, widget: QWidget, visible: bool) -> None:
        self.form.setRowVisible(widget, visible)

    def values(self) -> dict[str, str]:
        """What is typed; an AWS account has either a profile or keys."""
        typed = {key: edit.text().strip() for key, edit in self._edits.items()}
        if self.provider.id == "aws":
            if self.mode.currentData() == "profile":
                typed = {**typed, "access_key_id": "", "secret_access_key": ""}
                typed["session_token"] = ""
                typed["profile"] = str(self._profiles.currentData() or "")
                if not typed["profile"]:
                    typed["profile"] = self._profiles.currentText().strip()
            else:
                typed["profile"] = ""
        return typed

    def name(self) -> str:
        return self.name_edit.text().strip() or self.provider.name

    def chosen(self) -> list[Found]:
        return [
            self.found[self.clusters.row(item)]
            for item in self.clusters.selectedItems()
        ]

    def _find(self) -> None:
        values = self.values()
        problem = integrations.missing(self.provider.id, values)
        if problem is not None:
            self.status.setText(
                translate("AccountDialog", "{field} is required.").format(
                    field=label_of(problem)
                )
            )
            return
        self.find_button.setEnabled(False)
        self.status.setText(translate("AccountDialog", "Looking for clusters..."))
        account = Account(
            self.account.id, self.provider.id, self.name(), self._public(values)
        )
        self._worker = DiscoverWorker(account, values)
        self._worker.done.connect(self._found)
        self._worker.failed.connect(self._failed)
        self._worker.start()

    def _public(self, values: Mapping[str, str]) -> dict[str, str]:
        return {
            item.key: values.get(item.key, "")
            for item in self.provider.fields
            if not item.secret
        }

    def _found(self, hits: list[Found]) -> None:
        self.find_button.setEnabled(True)
        self.found = hits
        self.clusters.clear()
        for hit in hits:
            self.clusters.addItem(f"{hit.name}  ({hit.place})")
        self.clusters.selectAll()
        self.add_button.setEnabled(bool(hits))
        self.status.setText(
            translate("AccountDialog", "{count} clusters found.").format(
                count=len(hits)
            )
            if hits
            else translate("AccountDialog", "No clusters found.")
        )

    def _failed(self, message: str) -> None:
        self.find_button.setEnabled(True)
        self.status.setText(message)

    def done_working(self) -> None:
        """Wait for a search that is still running, so closing the dialog does
        not leave a thread behind."""
        if self._worker is not None:
            self._worker.wait()

    def closeEvent(self, event) -> None:
        self.done_working()
        super().closeEvent(event)

    def done(self, result: int) -> None:
        self.done_working()
        super().done(result)
