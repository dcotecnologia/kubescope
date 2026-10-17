import logging

from PySide6.QtCore import QThread, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from kubescope.utils.selfupdate import Install, UpdateError, find_asset, run_update
from kubescope.utils.updates import Release

logger = logging.getLogger(__name__)


class UpdateWorker(QThread):
    """Downloads and installs a release off the UI thread."""

    stage = Signal(str)  # "download" or "install"
    progress = Signal(int, int)  # bytes done, bytes in all (0 when unknown)
    done = Signal(object)  # the command that restarts the app
    failed = Signal(str)

    def __init__(self, install: Install, release: Release, current: str) -> None:
        super().__init__()
        self.install = install
        self.release = release
        self.current = current

    def run(self) -> None:
        try:
            command = run_update(
                self.install,
                self.release,
                self.current,
                self.stage.emit,
                self.progress.emit,
            )
        except UpdateError as error:  # expected: the dialog explains it
            logger.warning("Update failed: %s", error)
            self.failed.emit(str(error))
            return
        except Exception as error:
            logger.exception("Update failed")
            self.failed.emit(str(error))
            return
        self.done.emit(command)


class UpdateDialog(QDialog):
    """Confirms an update: from which version to which, what changed, and then
    installs it the way this KubeScope was installed.

    It is accepted when the new version is in place; `restart_command`
    then starts it.
    """

    def __init__(
        self,
        parent: QWidget | None,
        current: str,
        release: Release,
        install: Install | None,
    ) -> None:
        super().__init__(parent)
        self.current = current
        self.release = release
        self.install = install
        self.restart_command: list[str] | str | None = None
        self.worker: UpdateWorker | None = None
        # a file GitHub published no sha256 for cannot be checked, so it is not used
        self.can_update = install is not None and find_asset(install, release)
        self.setWindowTitle(self.tr("Update KubeScope"))
        self.setMinimumSize(560, 460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        heading = QLabel(
            self.tr("Update KubeScope from version {current} to {new}?").format(
                current=current, new=release.version
            )
        )
        heading.setWordWrap(True)
        layout.addWidget(heading)
        layout.addWidget(QLabel(self.tr("What is new")))
        self.notes = QTextBrowser()
        self.notes.setOpenLinks(False)
        if release.notes:
            self.notes.setMarkdown(release.notes)
        else:
            self.notes.setPlainText(self.tr("No release notes were published."))
        layout.addWidget(self.notes, 1)

        self.message = QLabel()
        self.message.setWordWrap(True)
        self.message.setVisible(False)
        layout.addWidget(self.message)
        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setVisible(False)
        layout.addWidget(self.bar)

        actions = QHBoxLayout()
        actions.addStretch()
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.cancel_button.setProperty("variant", "secondary")
        self.cancel_button.clicked.connect(self.reject)
        self.start_button = QPushButton()
        self.start_button.setProperty("variant", "primary")
        self.start_button.setDefault(True)
        self.start_button.clicked.connect(self._start)
        actions.addWidget(self.cancel_button)
        actions.addWidget(self.start_button)
        layout.addLayout(actions)

        if self.can_update:
            self.start_button.setText(self.tr("Update and restart"))
        else:
            self.start_button.setText(self.tr("Open release page"))
            self._say(
                self.tr(
                    "This installation cannot update itself. Open the release "
                    "page to download the new version."
                )
            )

    def _say(self, text: str) -> None:
        self.message.setText(text)
        self.message.setVisible(bool(text))

    def _start(self) -> None:
        if not self.can_update:
            QDesktopServices.openUrl(QUrl(self.release.url))
            return
        assert self.install is not None
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.bar.setRange(0, 0)  # busy until the size is known
        self.bar.setVisible(True)
        self._say(self.tr("Downloading..."))
        worker = UpdateWorker(self.install, self.release, self.current)
        worker.stage.connect(self._stage)
        worker.progress.connect(self._progress)
        worker.done.connect(self._done)
        worker.failed.connect(self._failed)
        self.worker = worker
        worker.start()

    def _stage(self, stage: str) -> None:
        if stage == "install":
            self.bar.setRange(0, 0)
            self._say(self.tr("Installing..."))

    def _progress(self, done: int, total: int) -> None:
        if total > 0:
            self.bar.setRange(0, total)
            self.bar.setValue(done)

    def _done(self, command: object) -> None:
        self.restart_command = command  # type: ignore[assignment]
        self._say(self.tr("Updated. Restarting..."))
        self.accept()

    def _failed(self, message: str) -> None:
        self.bar.setVisible(False)
        self._say(self.tr("The update failed: {error}").format(error=message))
        self.start_button.setText(self.tr("Try again"))
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(True)

    def reject(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            return  # a half-done install must not be abandoned
        super().reject()

    def done_with_worker(self) -> None:
        """Wait for the worker thread; used when the dialog is closed."""
        if self.worker is not None:
            self.worker.wait()
