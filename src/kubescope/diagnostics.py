"""Application logging, and the debug mode that writes a log file to share.

The file is off by default. When it is on, it records what the app does
(which kubectl and AWS CLI commands ran, how long they took, how they
ended) and never the content of Pod logs or resources. Common secrets
are scrubbed from every line, but the person should still read the file
before sending it.
"""

import faulthandler
import logging
import logging.handlers
import platform
import re
import sys
from importlib import metadata
from pathlib import Path
from typing import IO

from kubescope.settings import log_directory

LOG_FILE = "kubescope.log"
CRASH_FILE = "crash.log"
MAX_BYTES = 1_000_000
BACKUPS = 3
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


def _version() -> str:
    try:
        return metadata.version("kubescope")
    except metadata.PackageNotFoundError:  # running from a source checkout
        return "unknown"


def describe_environment() -> list[str]:
    """What a person reading a shared log needs to know about the machine."""
    from PySide6 import __version__ as pyside_version
    from PySide6.QtCore import qVersion

    return [
        f"KubeScope {_version()}",
        f"Python {platform.python_version()} on {platform.platform()}",
        f"PySide6 {pyside_version}, Qt {qVersion()}",
        f"Frozen bundle: {bool(getattr(sys, 'frozen', False))}",
    ]


def _remove(handler: logging.Handler | None) -> None:
    if handler is not None:
        _logger.removeHandler(handler)
        handler.close()


def configure_logging(*, to_file: bool = False, to_console: bool = False) -> None:
    """Turn the debug outputs on or off; safe to call again when a setting
    changes.

    Without either output, only warnings and errors are shown.
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
    _logger.setLevel(logging.DEBUG if to_file or to_console else logging.WARNING)
    if _file_handler is not None:
        for line in describe_environment():
            _logger.info(line)
