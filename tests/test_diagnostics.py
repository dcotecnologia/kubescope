import logging
import logging.handlers

import pytest

from kubescope import diagnostics
from kubescope.settings import log_directory


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

    assert package.handlers == [] and package.level == logging.WARNING


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
    assert logging.getLogger("kubescope").level == logging.WARNING


def test_the_environment_description_starts_with_the_app_version() -> None:
    import kubescope

    assert diagnostics.describe_environment()[0] == f"KubeScope {kubescope.__version__}"
