"""Capture an unhandled error and keep it for the next start, with no network.

Two things run all the time, and both cost next to nothing: a handler
that keeps the last records in memory (appending to a bounded deque; the
text is only built when a report is written), and the hooks Python calls
when an exception escapes. When one does, a report with the build, the
machine, the trace and the recent records is written to the logs folder.
The next start offers it to the person, who reads it and decides whether
to open an issue. Nothing is sent by the app.
"""

import collections
import logging
import sys
import threading
import traceback
from datetime import UTC, datetime
from types import TracebackType
from urllib.parse import urlencode

from kubescope import PROJECT_URL, __version__
from kubescope.settings import log_directory
from kubescope.utils.diagnostics import describe_environment, redact

REPORT_FILE = "crash-report.txt"
RECENT_RECORDS = 200
ISSUE_CHARS = 3000
ISSUE_FORM = "bug_report.yml"

_logger = logging.getLogger("kubescope")
_hooks_installed = False


class RecentLog(logging.Handler):
    """Remember the latest INFO (and above) records of the app, in memory only.

    DEBUG detail is not kept: it is what the debug log is for, and keeping it
    would mean building every record.
    """

    def __init__(self) -> None:
        super().__init__(level=logging.INFO)
        self.recent: collections.deque[tuple[float, str, str, str]] = collections.deque(
            maxlen=RECENT_RECORDS
        )

    def emit(self, record: logging.LogRecord) -> None:
        self.recent.append(
            (record.created, record.levelname, record.name, record.getMessage())
        )
        # This handler stops Python from falling back to stderr for the
        # warnings nobody else handles; keep printing those
        if (
            record.levelno >= logging.WARNING
            and _logger.handlers == [self]
            and logging.lastResort is not None
        ):
            logging.lastResort.handle(record)


_recent = RecentLog()


def build_report(
    exc_type: type[BaseException],
    exc: BaseException,
    tb: TracebackType | None,
    thread: str = "MainThread",
) -> str:
    """The text a person reads and may share: only the first line of the
    message, since an error from the cluster can quote what it was reading."""
    message = (str(exc).splitlines() or [""])[0]
    recent = [
        f"{datetime.fromtimestamp(created, UTC):%H:%M:%S} {level:<7} {name}: {text}"
        for created, level, name, text in _recent.recent
    ]
    lines = [
        f"Unhandled {exc_type.__qualname__} in thread {thread}",
        "",
        *describe_environment(),
        "",
        "Traceback (most recent call last):",
        "".join(traceback.format_tb(tb)).rstrip(),
        f"{exc_type.__qualname__}: {message}".rstrip(": "),
        "",
        "Recent records (newest last):",
        *(recent or ["none"]),
    ]
    return redact("\n".join(lines)) + "\n"


def _record(
    exc_type: type[BaseException],
    exc: BaseException,
    tb: TracebackType | None,
    thread: str,
) -> None:
    """Write the report of this error; reporting must never raise."""
    try:
        directory = log_directory()
        directory.mkdir(parents=True, exist_ok=True)
        (directory / REPORT_FILE).write_text(
            build_report(exc_type, exc, tb, thread), encoding="utf-8"
        )
    except Exception:  # a failing report must not hide the error itself
        logging.getLogger(__name__).warning("Could not write the crash report")


def install() -> None:
    """Start remembering records and reporting unhandled errors; safe to call
    again."""
    global _hooks_installed
    if _recent not in _logger.handlers:
        _logger.addHandler(_recent)
    if _hooks_installed:
        return
    _hooks_installed = True
    previous = sys.excepthook
    previous_thread = threading.excepthook

    def on_error(exc_type, exc, tb) -> None:
        if not issubclass(exc_type, KeyboardInterrupt):
            _record(exc_type, exc, tb, threading.current_thread().name)
        previous(exc_type, exc, tb)

    def on_thread_error(args: threading.ExceptHookArgs) -> None:
        if args.exc_value is not None:
            name = args.thread.name if args.thread else "unknown"
            _record(args.exc_type, args.exc_value, args.exc_traceback, name)
        previous_thread(args)

    sys.excepthook = on_error
    threading.excepthook = on_thread_error


def pending_report() -> str | None:
    """The report left by an earlier run, if there is one."""
    try:
        text = (log_directory() / REPORT_FILE).read_text(encoding="utf-8")
    except OSError:
        return None
    return text or None


def discard_report() -> None:
    try:
        (log_directory() / REPORT_FILE).unlink(missing_ok=True)
    except OSError as error:
        logging.getLogger(__name__).warning("Could not delete the report: %s", error)


def issue_url(report: str) -> str:
    """The new-issue page of the project with the bug form filled in.

    The start of the report goes in the address (the rest is for the
    person to paste), so it stays short enough for GitHub.
    """
    cut = report[:ISSUE_CHARS]
    if len(report) > ISSUE_CHARS:
        cut += "\n[cut: paste the rest of the report here]"
    title = f"bug: {report.splitlines()[0].removeprefix('Unhandled ')}"
    query = urlencode(
        {
            "template": ISSUE_FORM,
            "title": title,
            "summary": "KubeScope reported an unhandled error "
            "(the report below was made by the app and read before sending).",
            "version": __version__,
            "logs": cut,
        }
    )
    return f"{PROJECT_URL}/issues/new?{query}"
