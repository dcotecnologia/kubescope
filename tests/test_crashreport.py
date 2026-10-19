import logging
import sys
import threading
from urllib.parse import parse_qs, urlparse

import pytest

from kubescope import PROJECT_URL, __version__
from kubescope.settings import log_directory
from kubescope.utils import crashreport


@pytest.fixture(autouse=True)
def isolated_hooks(monkeypatch):
    """The hooks and the handler are process-wide; leave them as they were."""
    monkeypatch.setattr(sys, "excepthook", sys.excepthook)
    monkeypatch.setattr(threading, "excepthook", threading.excepthook)
    monkeypatch.setattr(crashreport, "_hooks_installed", False)
    crashreport._recent.recent.clear()
    yield
    logging.getLogger("kubescope").removeHandler(crashreport._recent)


def _error() -> tuple:
    message = "\n".join(("first line", "second line with a Pod's content"))
    try:
        raise ValueError(message)
    except ValueError:
        return sys.exc_info()


def _log_to_the_buffer(*messages: str) -> None:
    logger = logging.getLogger("kubescope.tests")
    logger.addHandler(crashreport._recent)
    logger.setLevel(logging.INFO)
    try:
        for message in messages:
            logger.info(message)
    finally:
        logger.removeHandler(crashreport._recent)


def test_the_report_keeps_the_first_line_of_the_message_only() -> None:
    report = crashreport.build_report(*_error())

    assert report.startswith("Unhandled ValueError in thread MainThread")
    assert f"KubeScope {__version__}" in report
    assert "ValueError: first line" in report
    assert "second line" not in report
    assert "Recent records (newest last):\nnone" in report


def test_the_report_has_the_recent_records_without_secrets() -> None:
    secret = "".join(("abcdefgh", "12345678"))
    _log_to_the_buffer(f"Context dev opened with token={secret}")
    logging.getLogger("kubescope.tests").debug("not kept")

    report = crashreport.build_report(*_error())

    assert "INFO    kubescope.tests: Context dev opened" in report
    assert secret not in report
    assert "not kept" not in report


def test_an_error_without_a_message_is_reported_by_its_type() -> None:
    report = crashreport.build_report(KeyError, KeyError(), None, "worker")

    assert "in thread worker" in report
    assert "\nKeyError\n" in report


def test_the_buffer_is_bounded() -> None:
    count = crashreport.RECENT_RECORDS + 50

    _log_to_the_buffer(*(f"line {number}" for number in range(count)))

    recent = crashreport._recent.recent
    assert len(recent) == crashreport.RECENT_RECORDS
    assert recent[-1][3] == f"line {count - 1}"


def test_unhandled_warnings_still_reach_stderr(capsys) -> None:
    crashreport.install()
    package = logging.getLogger("kubescope")
    package.setLevel(logging.INFO)

    package.info("quiet")
    package.warning("loud")

    err = capsys.readouterr().err
    assert "loud" in err and "quiet" not in err


def test_warnings_are_not_printed_twice_when_a_log_handler_exists(capsys) -> None:
    crashreport.install()
    package = logging.getLogger("kubescope")
    extra = logging.NullHandler()
    package.addHandler(extra)
    try:
        package.warning("handled elsewhere")
    finally:
        package.removeHandler(extra)

    assert "handled elsewhere" not in capsys.readouterr().err


def test_an_unhandled_error_writes_the_report_and_still_reaches_the_old_hook(
    monkeypatch,
) -> None:
    seen = []
    monkeypatch.setattr(sys, "excepthook", lambda *args: seen.append(args[0]))

    crashreport.install()
    crashreport.install()  # a second call changes nothing
    sys.excepthook(*_error())

    assert seen == [ValueError]
    report = crashreport.pending_report()
    assert report is not None and "ValueError: first line" in report
    assert logging.getLogger("kubescope").handlers.count(crashreport._recent) == 1


def test_ctrl_c_is_not_an_error_to_report(monkeypatch) -> None:
    monkeypatch.setattr(sys, "excepthook", lambda *_args: None)
    crashreport.install()

    sys.excepthook(KeyboardInterrupt, KeyboardInterrupt(), None)

    assert crashreport.pending_report() is None


def test_an_error_in_a_thread_is_reported_with_the_thread_name(monkeypatch) -> None:
    seen = []
    monkeypatch.setattr(threading, "excepthook", lambda args: seen.append(args))
    crashreport.install()

    def fail() -> None:
        raise RuntimeError("worker failed")

    thread = threading.Thread(target=fail, name="refresh-worker")
    thread.start()
    thread.join()

    assert len(seen) == 1
    report = crashreport.pending_report()
    assert report is not None
    assert "in thread refresh-worker" in report and "RuntimeError" in report


def test_a_thread_hook_call_without_an_error_is_ignored(monkeypatch) -> None:
    monkeypatch.setattr(threading, "excepthook", lambda _args: None)
    crashreport.install()

    threading.excepthook(threading.ExceptHookArgs((SystemExit, None, None, None)))

    assert crashreport.pending_report() is None


def test_a_thread_error_without_its_thread_is_still_reported(monkeypatch) -> None:
    monkeypatch.setattr(threading, "excepthook", lambda _args: None)
    crashreport.install()

    exc_type, exc, tb = _error()
    threading.excepthook(threading.ExceptHookArgs((exc_type, exc, tb, None)))

    report = crashreport.pending_report()
    assert report is not None and "in thread unknown" in report


def test_a_report_that_cannot_be_written_never_hides_the_error(
    monkeypatch, tmp_path, caplog
) -> None:
    blocker = tmp_path / "blocker"
    blocker.write_text("a file where a folder is needed")
    monkeypatch.setattr(crashreport, "log_directory", lambda: blocker / "logs")

    with caplog.at_level(logging.WARNING):
        crashreport._record(*_error(), "MainThread")

    assert "Could not write the crash report" in caplog.text


def test_there_is_no_pending_report_by_default_and_discard_removes_it() -> None:
    assert crashreport.pending_report() is None

    log_directory().mkdir(parents=True)
    (log_directory() / crashreport.REPORT_FILE).write_text("", encoding="utf-8")
    assert crashreport.pending_report() is None  # an empty file says nothing

    (log_directory() / crashreport.REPORT_FILE).write_text("text", encoding="utf-8")
    assert crashreport.pending_report() == "text"
    crashreport.discard_report()
    assert crashreport.pending_report() is None


def test_discard_reports_a_file_it_cannot_remove(monkeypatch, caplog) -> None:
    def refuse(*_args, **_kwargs):
        raise PermissionError("denied")

    monkeypatch.setattr("pathlib.Path.unlink", refuse)

    with caplog.at_level(logging.WARNING):
        crashreport.discard_report()

    assert "Could not delete the report" in caplog.text


def test_the_issue_link_fills_the_bug_form_and_stays_short() -> None:
    report = "Unhandled ValueError in thread MainThread\n" + "x" * 9000

    url = crashreport.issue_url(report)

    assert url.startswith(f"{PROJECT_URL}/issues/new?")
    fields = parse_qs(urlparse(url).query)
    assert fields["template"] == [crashreport.ISSUE_FORM]
    assert fields["title"] == ["bug: ValueError in thread MainThread"]
    assert fields["version"] == [__version__]
    assert fields["logs"][0].startswith("Unhandled ValueError")
    assert "[cut:" in fields["logs"][0]
    assert len(url) < 8000


def test_a_short_report_goes_into_the_issue_link_whole() -> None:
    report = "Unhandled KeyError in thread MainThread\ntrace\n"

    fields = parse_qs(urlparse(crashreport.issue_url(report)).query)

    assert fields["logs"] == [report]
