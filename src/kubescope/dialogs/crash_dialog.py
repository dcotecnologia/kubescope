from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kubescope.utils.crashreport import discard_report, issue_url, pending_report


class CrashReportDialog(QDialog):
    """Show the report of an earlier error so the person reads it before
    deciding: nothing leaves the machine unless they open the issue page (and
    submit it there) or copy the text themselves."""

    def __init__(self, report: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.report = report
        self.setWindowTitle(self.tr("KubeScope found an error"))
        self.resize(720, 520)
        intro = QLabel(
            self.tr(
                "KubeScope hit an unexpected error the last time it ran. This "
                "report stayed on your computer and was not sent anywhere. Read "
                "it, since it can include context names and paths, then choose "
                "what to do."
            )
        )
        intro.setWordWrap(True)
        text = QPlainTextEdit(report)
        text.setReadOnly(True)
        self.open_issue = QPushButton(self.tr("Open an issue on GitHub"))
        self.copy = QPushButton(self.tr("Copy report"))
        self.discard = QPushButton(self.tr("Discard"))
        self.open_issue.setDefault(True)
        self.open_issue.clicked.connect(self._open_issue)
        self.copy.clicked.connect(self._copy)
        self.discard.clicked.connect(self.accept)
        buttons = QHBoxLayout()
        buttons.addStretch()
        for button in (self.copy, self.discard, self.open_issue):
            buttons.addWidget(button)
        layout = QVBoxLayout(self)
        layout.addWidget(intro)
        layout.addWidget(text)
        layout.addLayout(buttons)

    def _open_issue(self) -> None:
        QDesktopServices.openUrl(QUrl(issue_url(self.report)))
        self.accept()

    def _copy(self) -> None:
        QGuiApplication.clipboard().setText(self.report)


def show_pending_crash_report(parent: QWidget | None = None) -> None:
    """Offer the report an earlier run left, once: it is deleted whatever the
    person chooses."""
    report = pending_report()
    if report is None:
        return
    CrashReportDialog(report, parent).exec()
    discard_report()
