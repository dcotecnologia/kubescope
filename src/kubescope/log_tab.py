from datetime import datetime

from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QWidget

from kubescope.models import PodInfo
from kubescope.ui.ui_log_tab import Ui_LogTab

LOG_REFRESH_MS = 3000


class LogTab(QWidget):
    """A Pod log viewer that keeps following the end of the log."""

    def __init__(self, context: str, pod: PodInfo, container: str) -> None:
        super().__init__()
        self.ui = Ui_LogTab()
        self.ui.setupUi(self)
        self.ui.logText.setFont(
            QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        )
        self.context = context
        self.pod = pod
        self.container = container
        self.busy = False
        self.closed = False
        self.ui.logText.clear()
        self.ui.logStatus.setText("")

    @property
    def auto_refresh(self) -> bool:
        return self.ui.autoCheck.isChecked()

    def set_logs(self, text: str) -> None:
        """Replace the text, keeping the view pinned to the end only if it was."""
        editor = self.ui.logText
        scrollbar = editor.verticalScrollBar()
        was_at_end = scrollbar.value() >= scrollbar.maximum() - 2
        previous = scrollbar.value()
        text = text or self.tr("No log lines returned.")
        if text != editor.toPlainText():
            editor.setPlainText(text)
            scrollbar.setValue(scrollbar.maximum() if was_at_end else previous)
        self.ui.logStatus.setText(
            self.tr("Updated at {time}").format(
                time=datetime.now().strftime("%H:%M:%S")
            )
        )

    def set_error(self, message: str) -> None:
        self.ui.logStatus.setText(
            self.tr("Could not refresh logs: {message}").format(message=message)
        )
