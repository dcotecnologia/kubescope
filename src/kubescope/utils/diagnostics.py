"""Application logging, and the debug mode that writes a log file to share.

The file is off by default. When it is on, it records what the app does
(which cluster requests and cloud CLI commands ran, how long they took,
how they ended) and never the content of Pod logs or resources. Common
secrets are scrubbed from every line, but the person should still read
the file before sending it.
"""

import faulthandler
import logging
import logging.handlers
import os
import platform
import re
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, cast

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QGuiApplication, QKeyEvent
from PySide6.QtWidgets import QApplication

import kubescope
from kubescope.settings import log_directory

LOG_FILE = "kubescope.log"
CRASH_FILE = "crash.log"
MAX_BYTES = 1_000_000
BACKUPS = 3
MAX_AGE_DAYS = 30
_FORMAT = "%(asctime)s %(levelname)-7s %(threadName)s %(name)s: %(message)s"

_SECRETS = (
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{8,}"), r"\1[redacted]"),
    (
        re.compile(
            r"(?i)((?:token|secret|password|passwd|authorization|access[_-]?key"
            r"|session[_-]?token|x-amz-[a-z-]*)[\"']?\s*[:=]\s*[\"']?)[^\s\"',;&]+"
        ),
        r"\1[redacted]",
    ),
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "[redacted-key-id]"),
    (re.compile(r"\bk8s-aws-v1\.[A-Za-z0-9_-]+"), "[redacted]"),
    (
        re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]*"),
        "[redacted]",
    ),
)

# Native libraries whose version and origin explain a crash that Python cannot
# show: the desktop ones a bundle may carry its own copy of, and Qt itself.
_NATIVE_LIBRARIES = (
    "libxkbcommon",
    "libfontconfig",
    "libfreetype",
    "libharfbuzz",
    "libglib-2.0",
    "libgio-2.0",
    "libdbus-1",
    "libX11",
    "libxcb.",
    "libwayland-client",
    "libEGL",
    "libGL.",
    "libQt6Core",
    "libQt6XcbQpa",
    "libQt6WaylandClient",
)

_logger = logging.getLogger("kubescope")
_file_handler: logging.Handler | None = None
_console_handler: logging.Handler | None = None
_crash_stream: IO[str] | None = None


def redact(text: str) -> str:
    """Hide tokens, keys and passwords that may appear in a line of text."""
    for pattern, replacement in _SECRETS:
        text = pattern.sub(replacement, text)
    return text


class _RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return redact(super().format(record))


def log_file() -> Path:
    return log_directory() / LOG_FILE


def purge_old_logs(
    max_age_days: int = MAX_AGE_DAYS,
    now: float | None = None,
    keep: tuple[str, ...] = (),
) -> None:
    """Delete the debug log, its backups and the crash log not written for
    longer than `max_age_days`; nothing else in the folder is touched.

    `keep` names files that are open for writing right now.
    """
    limit = (time.time() if now is None else now) - max_age_days * 86400
    for pattern in (f"{LOG_FILE}*", f"{CRASH_FILE}*"):
        for path in log_directory().glob(pattern):
            try:
                if (
                    path.name not in keep
                    and path.is_file()
                    and path.stat().st_mtime < limit
                ):
                    path.unlink(missing_ok=True)
            except OSError as error:
                logging.getLogger(__name__).warning(
                    "Could not delete %s: %s", path.name, error
                )


def commit() -> str:
    """The short git commit this build is from: written beside the code when a
    bundle is built, or asked of git in a source checkout; "unknown"
    otherwise."""
    recorded = Path(__file__).resolve().parent.parent / "_commit.txt"
    try:
        text = recorded.read_text(encoding="utf-8").strip()
        if text:
            return text
    except OSError:
        pass
    checkout = Path(__file__).resolve().parents[3]
    if (checkout / ".git").exists():
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=checkout,
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return "unknown"
        return result.stdout.strip() or "unknown"
    return "unknown"


def describe_environment() -> list[str]:
    """What a person reading a shared log needs to know about the machine."""
    from PySide6 import __version__ as pyside_version
    from PySide6.QtCore import qVersion

    return [
        f"KubeScope {kubescope.__version__} (commit {commit()})",
        f"Python {platform.python_version()} on {platform.platform()}",
        f"PySide6 {pyside_version}, Qt {qVersion()}",
        f"Frozen bundle: {bool(getattr(sys, 'frozen', False))}",
        *describe_desktop(),
    ]


def describe_desktop() -> list[str]:
    """The system and desktop session: a native crash often depends on them
    (the display server, the distro, the Qt variables in the environment)."""
    try:
        system = platform.freedesktop_os_release().get("PRETTY_NAME", "unknown")
    except OSError:
        system = "unknown"
    env = os.environ
    qt = sorted(
        f"{name}={value}" for name, value in env.items() if name.startswith("QT_")
    )
    return [
        f"System: {system}",
        f"Session: type={env.get('XDG_SESSION_TYPE', '-')}, "
        f"desktop={env.get('XDG_CURRENT_DESKTOP', '-')}, "
        f"DISPLAY={'set' if 'DISPLAY' in env else 'unset'}, "
        f"WAYLAND_DISPLAY={'set' if 'WAYLAND_DISPLAY' in env else 'unset'}",
        f"Qt environment: {'; '.join(qt) or 'none'}",
    ]


def native_libraries(maps: str = "/proc/self/maps") -> list[str]:
    """Where each native library of interest was loaded from, and whether that
    is the bundle or the system; empty where /proc is not available."""
    try:
        text = Path(maps).read_text(encoding="utf-8")
    except OSError:
        return []
    bundle = getattr(sys, "_MEIPASS", None)

    def origin(path: str) -> str:
        return "bundle" if bundle and path.startswith(bundle) else "system"

    found: dict[str, str] = {}
    for line in text.splitlines():
        fields = line.split(maxsplit=5)
        if len(fields) == 6 and fields[5].startswith("/"):
            found.setdefault(Path(fields[5]).name, fields[5])
    return [
        f"  {name} <- {path} ({origin(path)})"
        for name, path in sorted(found.items())
        if name.startswith(_NATIVE_LIBRARIES)
    ]


def describe_runtime() -> list[str]:
    """What only exists once the application does: the platform plugin and
    style Qt picked, and the native libraries it loaded.

    A key press that crashes inside xkbcommon is explained by these
    lines.
    """
    return [
        f"Qt platform: {QGuiApplication.platformName()}, "
        f"style: {QApplication.style().objectName()}",
        "Native libraries:",
        *native_libraries(),
    ]


def record_runtime() -> None:
    """Put the runtime description in the log and in the crash log, beside the
    header of this session."""
    lines = describe_runtime()
    if _crash_stream is not None:
        _crash_stream.writelines(f"{line}\n" for line in lines)
        _crash_stream.flush()
    for line in lines:
        _logger.info(line)


class InputTrail(QObject):
    """Log the keys that are not text (Ctrl, Shift, arrows, shortcuts) and the
    widget that got them, so the last line of the log before a crash says what
    the person had just done.

    Typed characters are never recorded.
    """

    _EVENTS = {QEvent.Type.KeyPress: "pressed", QEvent.Type.KeyRelease: "released"}

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        action = self._EVENTS.get(event.type())
        key_event = cast(QKeyEvent, event)  # read only when it is a key event
        text = key_event.text() if action else ""
        if action and not (text and text.isprintable()):
            _logger.debug(
                "Key %s %s on %s",
                Qt.Key(key_event.key()).name,
                action,
                type(watched).__name__,
            )
        return False


def trace_input(application: QObject) -> None:
    application.installEventFilter(InputTrail(application))


def _write_crash_header(stream: IO[str]) -> None:
    """Say which build and machine the crashes after this line come from:
    faulthandler appends bare tracebacks to the same file, session after
    session."""
    started = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    stream.write(f"\n=== KubeScope session started {started} ===\n")
    stream.writelines(f"{line}\n" for line in describe_environment())
    stream.flush()


def _remove(handler: logging.Handler | None) -> None:
    if handler is not None:
        _logger.removeHandler(handler)
        handler.close()


def configure_logging(*, to_file: bool = False, to_console: bool = False) -> None:
    """Turn the debug outputs on or off; safe to call again when a setting
    changes.

    Without either output, nothing is written; warnings still reach
    stderr and the latest INFO records are remembered in memory for the
    crash report.
    """
    global _file_handler, _console_handler, _crash_stream
    _remove(_file_handler)
    _remove(_console_handler)
    _file_handler = _console_handler = None
    faulthandler.disable()
    if _crash_stream is not None:
        _crash_stream.close()
        _crash_stream = None

    formatter = _RedactingFormatter(_FORMAT)
    if to_file:
        directory = log_directory()
        try:
            directory.mkdir(parents=True, exist_ok=True)
            _file_handler = logging.handlers.RotatingFileHandler(
                log_file(), maxBytes=MAX_BYTES, backupCount=BACKUPS, encoding="utf-8"
            )
            _crash_stream = (directory / CRASH_FILE).open("a", encoding="utf-8")
            _write_crash_header(_crash_stream)
            faulthandler.enable(file=_crash_stream)
        except OSError as error:
            to_file = False
            logging.getLogger(__name__).warning(
                "Could not write the log file: %s", error
            )
    if to_console:
        _console_handler = logging.StreamHandler()
        faulthandler.enable()
    for handler in (_file_handler, _console_handler):
        if handler is not None:
            handler.setFormatter(formatter)
            _logger.addHandler(handler)
    # INFO even with the outputs off: the crash report keeps the latest records
    # in memory (utils/crashreport.py); DEBUG stays off, so its calls cost nothing
    _logger.setLevel(logging.DEBUG if to_file or to_console else logging.INFO)
    if _file_handler is not None:
        for line in describe_environment():
            _logger.info(line)
