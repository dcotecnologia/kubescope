import re
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QPlainTextEdit, QWidget

from kubescope.models import PodInfo, safe_file_name
from kubescope.ui.ui_log_tab import Ui_LogTab
from kubescope.utils.fonts import code_font
from kubescope.utils.log_view import style_log_view
from kubescope.views.search_bar import SearchBar

LOG_REFRESH_MS = 3000
LOG_MAX_LINES = 5000  # what a log that keeps growing holds before the oldest go
# colors and cursor moves that coloredlogs and the like write: the editor would
# draw their escape character as a box
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
# the cluster puts the time of each line first (`timestamps=true`)
_LINE_TIME = re.compile(r"^\d{4}-\d\d-\d\dT[\d:.]+(?:Z|[+-]\d\d:\d\d)$")


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
        self.search = SearchBar(self.ui.logText)
        self.ui.logLayout.insertWidget(1, self.search)
        find = QShortcut(QKeySequence(QKeySequence.StandardKey.Find), self)
        find.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        find.activated.connect(self.search.focus)
        self.save_name = safe_file_name(f"{pod.name}-{container}", ".log")
        self.context = context
        self.pod = pod
        self.container = container
        self.busy = False
        self.closed = False
        # the last line shown and its time: the next read asks only for what follows
        self.last_line: str | None = None
        self.last_time: str | None = None
        self._empty = True
        self.ui.logText.setMaximumBlockCount(LOG_MAX_LINES)
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
        self._remember_end(text.splitlines())
        shown = _ANSI.sub("", text)
        self._empty = not shown
        shown = shown or self.tr("No log lines returned.")
        if shown != editor.toPlainText():
            editor.setPlainText(shown)
            scrollbar.setValue(scrollbar.maximum() if was_at_end else previous)
            self.search.refresh()
        self._show_updated()

    def add_logs(self, text: str) -> None:
        """Add the lines that came after the ones shown, keeping the view
        pinned to the end only if it was."""
        lines = [line for line in text.splitlines() if line.strip()]
        if self.last_line in lines:  # the cluster repeats the line it was given
            lines = lines[lines.index(self.last_line) + 1 :]
        if lines:
            editor = self.ui.logText
            scrollbar = editor.verticalScrollBar()
            was_at_end = scrollbar.value() >= scrollbar.maximum() - 2
            previous = scrollbar.value()
            added = _ANSI.sub("", "\n".join(lines))
            if self._empty:  # the notice of an empty log gives way
                editor.setPlainText(added)
            else:
                editor.appendPlainText(added)
            self._empty = False
            self._remember_end(lines)
            scrollbar.setValue(scrollbar.maximum() if was_at_end else previous)
            self.search.refresh()
        self._show_updated()

    def _remember_end(self, lines: list[str]) -> None:
        """Note the last line and its time, to ask only for what follows."""
        last = next((line for line in reversed(lines) if line.strip()), None)
        if last is None:
            self.last_line = self.last_time = None
            return
        self.last_line = last
        stamp = last.split(" ", 1)[0]
        self.last_time = stamp if _LINE_TIME.match(stamp) else None

    def _show_updated(self) -> None:
        self.ui.logStatus.setText(
            self.tr("Updated at {time}").format(
                time=datetime.now().strftime("%H:%M:%S")
            )
        )

    def set_error(self, message: str) -> None:
        self.ui.logStatus.setText(
            self.tr("Could not refresh logs: {message}").format(message=message)
        )
