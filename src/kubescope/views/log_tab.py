import re
from datetime import datetime

from PySide6.QtWidgets import QPlainTextEdit, QWidget

from kubescope.models import PodInfo, safe_file_name
from kubescope.ui.ui_log_tab import Ui_LogTab
from kubescope.utils.fonts import code_font
from kubescope.utils.log_view import style_log_view

LOG_REFRESH_MS = 3000
# colors and cursor moves that coloredlogs and the like write: the editor would
# draw their escape character as a box
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


class LogTab(QWidget):
    """A Pod log viewer that keeps following the end of the log."""

    def __init__(
        self, context: str, pod: PodInfo, container: str, wrap: bool = False
    ) -> None:
        super().__init__()
        self.ui = Ui_LogTab()
        self.ui.setupUi(self)
        self.ui.logText.setFont(code_font())
        self.highlighter = style_log_view(self.ui.logText)
        self.save_name = safe_file_name(f"{pod.name}-{container}", ".log")
        self.context = context
        self.pod = pod
        self.container = container
        self.busy = False
        self.closed = False
        self.ui.logText.clear()
        self.ui.logStatus.setText("")
        self.set_wrap(wrap)

    def set_wrap(self, wrap: bool) -> None:
        """Break long lines to the width of the view, or let them run on."""
        self.ui.wrapCheck.blockSignals(True)
        self.ui.wrapCheck.setChecked(wrap)
        self.ui.wrapCheck.blockSignals(False)
        self.ui.logText.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.WidgetWidth
            if wrap
            else QPlainTextEdit.LineWrapMode.NoWrap
        )

    @property
    def auto_refresh(self) -> bool:
        return self.ui.autoCheck.isChecked()

    def set_logs(self, text: str) -> None:
        """Replace the text, keeping the view pinned to the end only if it
        was."""
        editor = self.ui.logText
        scrollbar = editor.verticalScrollBar()
        was_at_end = scrollbar.value() >= scrollbar.maximum() - 2
        previous = scrollbar.value()
        text = _ANSI.sub("", text) or self.tr("No log lines returned.")
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
