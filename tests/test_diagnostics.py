import logging
import logging.handlers
import os

import pytest

import kubescope
from kubescope.settings import log_directory
from kubescope.utils import diagnostics


@pytest.fixture(autouse=True)
def reset_logging():
    yield
    diagnostics.configure_logging()  # always leave the outputs off


def _fake(*parts: str) -> str:
    """Join a made-up secret from pieces, so no literal in this file looks like
    a real one to the secret scanner."""
    return "".join(parts)


@pytest.mark.parametrize(
    ("template", "hidden"),
    [
        ("Authorization: Bearer {}", _fake("abcdef12", "34567890")),
        ("token={}", _fake("not-a-", "real-value-", "12345")),
        ("aws_secret_access_key = {}", _fake("FAKE", "SECRETVALUE", "1234567")),
        ("key {} in use", _fake("AK", "IA", "ABCDEFGHIJKLMNOP")),
        ("exec token {}", _fake("k8s-aws-", "v1.", "ZmFrZS1wcmVzaWduZWQ")),
        (
            "jwt {}",
            _fake("ey", "JhbGciOiJIUzI1NiJ9.", "eyJzdWIiOiIxMjM0", ".c2ln-fake"),
        ),
        ('{{"password": "{}"}}', _fake("fake-", "pass-", "value-1")),
    ],
)
def test_redact_hides_secrets(template: str, hidden: str) -> None:
    text = template.format(hidden)

    assert hidden not in diagnostics.redact(text)
    assert "redacted" in diagnostics.redact(text)


def test_redact_keeps_ordinary_text() -> None:
    line = "Exit 0 after 0.31s: kubectl --context prod get pods -n default"
    assert diagnostics.redact(line) == line


def test_the_debug_file_records_the_run_without_secrets() -> None:
    diagnostics.configure_logging(to_file=True)
    logging.getLogger("kubescope.test").debug(
        "calling with token=%s", _fake("fake-", "tok-", "99887766")
    )
    logging.getLogger("kubescope.test").info("a milestone")

    for handler in logging.getLogger("kubescope").handlers:
        handler.flush()
    text = diagnostics.log_file().read_text(encoding="utf-8")

    assert diagnostics.log_file().parent == log_directory()
    assert "KubeScope " in text and "PySide6" in text  # the environment header
    assert "a milestone" in text and "calling with" in text
    assert _fake("fake-", "tok-", "99887766") not in text
    assert (log_directory() / diagnostics.CRASH_FILE).exists()


def test_the_log_file_rotates_to_stay_small() -> None:
    diagnostics.configure_logging(to_file=True)

    (handler,) = logging.getLogger("kubescope").handlers

    assert isinstance(handler, logging.handlers.RotatingFileHandler)
    assert handler.maxBytes == diagnostics.MAX_BYTES
    assert handler.backupCount == diagnostics.BACKUPS


def test_turning_debug_off_removes_every_output() -> None:
    package = logging.getLogger("kubescope")
    diagnostics.configure_logging(to_file=True, to_console=True)
    assert len(package.handlers) == 2 and package.level == logging.DEBUG

    diagnostics.configure_logging()

    assert package.handlers == [] and package.level == logging.INFO


def test_an_unwritable_log_folder_is_reported_not_fatal(
    monkeypatch, tmp_path, caplog
) -> None:
    blocker = tmp_path / "blocker"
    blocker.write_text("a file where a folder is needed")
    monkeypatch.setattr(diagnostics, "log_directory", lambda: blocker / "logs")

    with caplog.at_level(logging.WARNING):
        diagnostics.configure_logging(to_file=True)

    assert "Could not write the log file" in caplog.text
    assert logging.getLogger("kubescope").handlers == []
    assert logging.getLogger("kubescope").level == logging.INFO


def test_the_environment_description_starts_with_the_app_version() -> None:
    import kubescope

    assert diagnostics.describe_environment()[0].startswith(
        f"KubeScope {kubescope.__version__} (commit "
    )


def test_crash_log_starts_each_session_with_the_build_and_the_machine() -> None:
    diagnostics.configure_logging(to_file=True)
    diagnostics.configure_logging(to_file=True)  # a second session, same file

    text = (log_directory() / diagnostics.CRASH_FILE).read_text(encoding="utf-8")

    assert text.count("=== KubeScope session started ") == 2
    assert text.count(f"KubeScope {kubescope.__version__} (commit ") == 2
    assert "Python " in text and "PySide6 " in text and "Frozen bundle: " in text


def test_commit_comes_from_the_bundle_file_or_from_git(monkeypatch, tmp_path) -> None:
    recorded = tmp_path / "_commit.txt"
    monkeypatch.setattr(
        diagnostics, "__file__", str(tmp_path / "utils" / "diagnostics.py")
    )

    recorded.write_text("abc1234\n", encoding="utf-8")
    assert diagnostics.commit() == "abc1234"

    recorded.write_text("\n", encoding="utf-8")  # empty: ask git (not a checkout here)
    assert diagnostics.commit() == "unknown"


def test_commit_asks_git_in_a_source_checkout(monkeypatch, tmp_path) -> None:
    package = tmp_path / "src" / "kubescope" / "utils"
    package.mkdir(parents=True)
    (tmp_path / ".git").mkdir()
    monkeypatch.setattr(diagnostics, "__file__", str(package / "diagnostics.py"))
    asked = []

    def run(command, **kwargs):
        asked.append((command, kwargs["cwd"]))
        return diagnostics.subprocess.CompletedProcess(command, 0, "9f8e7d6\n", "")

    monkeypatch.setattr(diagnostics.subprocess, "run", run)
    assert diagnostics.commit() == "9f8e7d6"
    assert asked == [(["git", "rev-parse", "--short", "HEAD"], tmp_path.resolve())]

    monkeypatch.setattr(
        diagnostics.subprocess,
        "run",
        lambda command, **_k: diagnostics.subprocess.CompletedProcess(
            command, 128, "", "x"
        ),
    )
    assert diagnostics.commit() == "unknown"  # git said nothing

    def missing(*_a, **_k):
        raise FileNotFoundError("git")

    monkeypatch.setattr(diagnostics.subprocess, "run", missing)
    assert diagnostics.commit() == "unknown"


def test_logs_older_than_thirty_days_are_deleted(tmp_path, monkeypatch) -> None:
    import os
    import time

    directory = log_directory()
    directory.mkdir(parents=True)
    old = time.time() - 31 * 86400
    names = ("kubescope.log", "kubescope.log.1", "crash.log", "other.txt")
    for name in names:
        (directory / name).write_text("x")
        os.utime(directory / name, (old, old))
    (directory / "kubescope.log.2").write_text("x")  # recent
    (directory / "crash.log.old").mkdir()  # a folder is left alone
    os.utime(directory / "crash.log.old", (old, old))

    diagnostics.purge_old_logs(keep=("crash.log",))

    assert sorted(path.name for path in directory.iterdir()) == [
        "crash.log",
        "crash.log.old",
        "kubescope.log.2",
        "other.txt",
    ]


def test_a_log_that_cannot_be_deleted_is_reported(monkeypatch, caplog) -> None:
    from pathlib import Path

    directory = log_directory()
    directory.mkdir(parents=True)
    (directory / "kubescope.log").write_text("x")

    def refuse(self, **_kwargs):
        raise OSError("busy")

    monkeypatch.setattr(Path, "unlink", refuse)

    with caplog.at_level(logging.WARNING):
        diagnostics.purge_old_logs(max_age_days=-1)

    assert "Could not delete kubescope.log" in caplog.text


def test_the_desktop_description_names_the_system_session_and_qt_variables(
    monkeypatch,
) -> None:
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")
    monkeypatch.setenv("QT_QPA_PLATFORM", "xcb")
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)
    monkeypatch.setattr(
        diagnostics.platform,
        "freedesktop_os_release",
        lambda: {"PRETTY_NAME": "Ubuntu"},
    )

    text = "\n".join(diagnostics.describe_desktop())

    assert "System: Ubuntu" in text
    assert "type=x11" in text and "WAYLAND_DISPLAY=unset" in text
    assert "QT_QPA_PLATFORM=xcb" in text


def test_the_desktop_description_survives_a_system_without_os_release(
    monkeypatch,
) -> None:
    def missing():
        raise OSError

    monkeypatch.setattr(diagnostics.platform, "freedesktop_os_release", missing)
    monkeypatch.setenv("DISPLAY", ":0")
    for name in [n for n in os.environ if n.startswith("QT_")]:
        monkeypatch.delenv(name)

    text = "\n".join(diagnostics.describe_desktop())

    assert "System: unknown" in text
    assert "DISPLAY=set" in text and "Qt environment: none" in text


def test_the_environment_description_includes_the_desktop() -> None:
    assert any(
        line.startswith("System: ") for line in diagnostics.describe_environment()
    )


def test_native_libraries_say_where_each_was_loaded_from(monkeypatch, tmp_path) -> None:
    maps = tmp_path / "maps"
    maps.write_text(
        "7f00-7f10 r-xp 00000000 08:01 1 /opt/app/libxkbcommon.so.0\n"
        "7f10-7f20 r-xp 00000000 08:01 1 /opt/app/libxkbcommon.so.0\n"
        "7f20-7f30 r-xp 00000000 08:01 2 /lib/x86_64-linux-gnu/libfreetype.so.6\n"
        "7f30-7f40 r-xp 00000000 08:01 3 /lib/x86_64-linux-gnu/libother.so.1\n"
        "7f40-7f50 rw-p 00000000 00:00 0\n"
        "7f50-7f60 rw-p 00000000 00:00 0 [heap]\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(diagnostics.sys, "_MEIPASS", "/opt/app", raising=False)

    assert diagnostics.native_libraries(str(maps)) == [
        "  libfreetype.so.6 <- /lib/x86_64-linux-gnu/libfreetype.so.6 (system)",
        "  libxkbcommon.so.0 <- /opt/app/libxkbcommon.so.0 (bundle)",
    ]


def test_native_libraries_are_empty_without_proc(tmp_path) -> None:
    assert diagnostics.native_libraries(str(tmp_path / "missing")) == []


def test_the_runtime_goes_to_the_log_and_the_crash_log(caplog) -> None:
    from PySide6.QtWidgets import QApplication

    QApplication.instance() or QApplication([])
    diagnostics.configure_logging(to_file=True)

    diagnostics.record_runtime()

    crash = (log_directory() / diagnostics.CRASH_FILE).read_text(encoding="utf-8")
    assert "Qt platform: " in crash and "Native libraries:" in crash
    diagnostics.configure_logging()
    diagnostics.record_runtime()  # no crash file open: only the logger


def test_the_input_trail_logs_keys_that_are_not_text_and_never_typed_text(
    caplog,
) -> None:
    from PySide6.QtCore import QEvent, QObject, Qt
    from PySide6.QtGui import QKeyEvent

    def key(kind, code, text=""):
        return QKeyEvent(kind, code, Qt.KeyboardModifier.NoModifier, text)

    trail = diagnostics.InputTrail()
    target = QObject()
    with caplog.at_level(logging.DEBUG, logger="kubescope"):
        trail.eventFilter(target, key(QEvent.Type.KeyPress, Qt.Key.Key_Control))
        trail.eventFilter(target, key(QEvent.Type.KeyRelease, Qt.Key.Key_Control))
        trail.eventFilter(target, key(QEvent.Type.KeyPress, Qt.Key.Key_A, "a"))
        trail.eventFilter(target, key(QEvent.Type.KeyPress, 0x1234567))
        assert not trail.eventFilter(target, QEvent(QEvent.Type.Show))

    assert "Key Key_Control pressed on QObject" in caplog.text
    assert "Key Key_Control released on QObject" in caplog.text
    assert "Key 19088743 pressed" in caplog.text
    assert "'a'" not in caplog.text and "Key A" not in caplog.text


def test_tracing_input_installs_the_trail_on_the_application(monkeypatch) -> None:
    installed = []

    class FakeApplication:
        def installEventFilter(self, filter_) -> None:
            installed.append(filter_)

    monkeypatch.setattr(diagnostics.InputTrail, "__init__", lambda self, parent: None)
    diagnostics.trace_input(FakeApplication())

    assert len(installed) == 1
