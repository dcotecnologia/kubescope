from PySide6.QtWidgets import QApplication, QDialog, QPlainTextEdit

from kubescope.dialogs import crash_dialog
from kubescope.dialogs.crash_dialog import CrashReportDialog, show_pending_crash_report
from kubescope.settings import log_directory
from kubescope.utils import crashreport

REPORT = "Unhandled ValueError in thread MainThread\ntrace\n"


def _application() -> None:
    QApplication.instance() or QApplication([])


def _leave_report() -> None:
    log_directory().mkdir(parents=True, exist_ok=True)
    (log_directory() / crashreport.REPORT_FILE).write_text(REPORT, encoding="utf-8")


def test_the_dialog_shows_the_report_for_reading() -> None:
    _application()
    dialog = CrashReportDialog(REPORT)

    text = dialog.findChild(QPlainTextEdit)
    assert text.toPlainText() == REPORT and text.isReadOnly()
    assert dialog.open_issue.isDefault()


def test_open_issue_opens_the_prefilled_page_and_closes(monkeypatch) -> None:
    _application()
    opened = []
    monkeypatch.setattr(
        crash_dialog.QDesktopServices, "openUrl", lambda url: opened.append(url)
    )
    dialog = CrashReportDialog(REPORT)

    dialog.open_issue.click()

    assert opened[0].toString() == crashreport.issue_url(REPORT)
    assert dialog.result() == QDialog.DialogCode.Accepted


def test_copy_puts_the_whole_report_on_the_clipboard() -> None:
    _application()
    dialog = CrashReportDialog(REPORT)

    dialog.copy.click()

    assert crash_dialog.QGuiApplication.clipboard().text() == REPORT
    assert dialog.result() != QDialog.DialogCode.Accepted  # still open to choose


def test_discard_closes_the_dialog() -> None:
    _application()
    dialog = CrashReportDialog(REPORT)

    dialog.discard.click()

    assert dialog.result() == QDialog.DialogCode.Accepted


def test_nothing_is_shown_when_no_report_was_left() -> None:
    _application()

    show_pending_crash_report()  # the suite refuses any real modal dialog


def test_the_report_is_shown_once_and_deleted(monkeypatch) -> None:
    _application()
    _leave_report()
    shown = []
    monkeypatch.setattr(QDialog, "exec", lambda self: shown.append(self.report))

    show_pending_crash_report()
    show_pending_crash_report()

    assert shown == [REPORT]
    assert crashreport.pending_report() is None
