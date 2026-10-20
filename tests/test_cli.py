import os
import sys
import time

import pytest

from kubescope import __version__, app, cli
from kubescope.settings import log_directory
from kubescope.utils.diagnostics import CRASH_FILE, LOG_FILE, MAX_AGE_DAYS
from kubescope.utils.selfupdate import Install, UpdateError
from kubescope.utils.updates import Release, UpdateCheck


def _logs(old: bool) -> tuple:
    folder = log_directory()
    folder.mkdir(parents=True)
    log, crash, other = folder / LOG_FILE, folder / CRASH_FILE, folder / "notes.txt"
    for path in (log, crash, other):
        path.write_text("x" * 2048, encoding="utf-8")
    if old:
        stamp = time.time() - (MAX_AGE_DAYS + 1) * 86400
        os.utime(log, (stamp, stamp))
    return log, crash, other


def test_arguments_that_are_not_commands_open_the_window() -> None:
    assert cli.run([]) is None
    assert cli.run(["-platform", "offscreen"]) is None  # Qt's own options


def test_the_version_is_printed_and_exits(capsys) -> None:
    with pytest.raises(SystemExit) as stop:
        cli.run(["--version"])

    assert stop.value.code == 0
    assert capsys.readouterr().out == f"KubeScope {__version__}\n"


def test_info_says_where_the_app_keeps_its_files(capsys) -> None:
    assert cli.run(["info"]) == 0

    out = capsys.readouterr().out
    assert out.startswith(f"KubeScope {__version__} (")
    assert str(log_directory()) in out
    assert "settings.json" in out


def test_cleanup_deletes_only_the_old_logs(capsys) -> None:
    log, crash, other = _logs(old=True)

    assert cli.run(["cleanup"]) == 0

    assert not log.exists()
    assert crash.exists() and other.exists()
    assert "1 files; Freed 2.0 KiB" in capsys.readouterr().out


def test_cleanup_all_deletes_every_log_but_nothing_else(capsys) -> None:
    log, crash, other = _logs(old=False)

    assert cli.run(["cleanup", "--all"]) == 0

    assert not log.exists() and not crash.exists()
    assert other.exists()


def test_a_dry_run_deletes_nothing(capsys) -> None:
    log, crash, _other = _logs(old=False)

    assert cli.run(["cleanup", "--all", "--dry-run"]) == 0

    assert log.exists() and crash.exists()
    out = capsys.readouterr().out
    assert "Would delete" in out
    assert "Would free 4.0 KiB" in out


def test_cleanup_with_nothing_to_delete_says_so(capsys) -> None:
    assert cli.run(["cleanup"]) == 0
    assert "0 files" in capsys.readouterr().out


def test_cleanup_reports_a_file_it_cannot_delete(monkeypatch, capsys) -> None:
    log, _crash, _other = _logs(old=False)

    def refuse(self, missing_ok=False):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(type(log), "unlink", refuse)

    assert cli.run(["cleanup", "--all"]) == 1
    assert "Permission denied" in capsys.readouterr().err


def test_a_file_that_vanishes_before_its_size_is_read_counts_as_empty() -> None:
    assert cli._size(log_directory() / "missing") == 0


@pytest.mark.parametrize(
    ("result", "code", "stream", "text"),
    [
        (UpdateCheck("current"), 0, "out", "up to date"),
        (
            UpdateCheck("available", Release("9.9.9", "https://x.test")),
            10,
            "out",
            "9.9.9",
        ),
        (UpdateCheck("failed"), 1, "err", "Could not check"),
    ],
)
def test_check_update_tells_by_exit_code(
    monkeypatch, capsys, result, code, stream, text
) -> None:
    monkeypatch.setattr(cli, "check_for_update", lambda: result)

    assert cli.run(["check-update"]) == code
    assert text in getattr(capsys.readouterr(), stream)


def test_main_runs_a_command_instead_of_opening_the_window(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["kubescope", "info"])

    assert app.main() == 0


NEWER = Release("9.9.9", "https://x.test")


def _updating(monkeypatch, kind="deb", release=NEWER):
    """An installation that can update itself, and the calls it makes."""
    calls = []
    monkeypatch.setattr(cli, "detect_install", lambda: Install(kind, cli.Path("/app")))
    monkeypatch.setattr(cli, "latest_release", lambda: release)
    monkeypatch.setattr(cli, "release_of", lambda version: release)
    monkeypatch.setattr(
        cli,
        "run_update",
        lambda install, rel, current, stage, progress: (
            stage("download"),
            stage("install"),
            progress(1, 2),
            calls.append(rel.version),
            "restart",
        )[-1],
    )
    monkeypatch.setattr(cli, "restart", lambda command: calls.append(command))
    return calls


def test_update_installs_the_latest_version(monkeypatch, capsys) -> None:
    calls = _updating(monkeypatch)

    assert cli.run(["update"]) == 0

    assert calls == ["9.9.9"]
    out = capsys.readouterr().out
    assert "Downloading..." in out and "Installing..." in out
    assert "KubeScope 9.9.9 is installed" in out


def test_update_installs_the_version_asked_for(monkeypatch, capsys) -> None:
    asked = []
    calls = _updating(monkeypatch, release=Release("0.5.0", "https://x.test"))
    monkeypatch.setattr(
        cli,
        "release_of",
        lambda version: asked.append(version) or Release("0.5.0", "u"),
    )

    assert cli.run(["update", "--version", "0.5.0"]) == 0

    assert asked == ["0.5.0"] and calls == ["0.5.0"]


def test_update_on_windows_starts_the_installer_after_quitting(monkeypatch) -> None:
    calls = _updating(monkeypatch, kind="windows")

    assert cli.run(["update"]) == 0

    assert calls == ["9.9.9", "restart"]


def test_update_says_when_the_version_is_already_installed(monkeypatch, capsys) -> None:
    calls = _updating(monkeypatch, release=Release(__version__, "https://x.test"))

    assert cli.run(["update"]) == 0

    assert calls == []
    assert "already installed" in capsys.readouterr().out


def test_update_refuses_where_the_app_cannot_update_itself(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "detect_install", lambda: None)

    assert cli.run(["update"]) == 1
    assert "cannot update itself" in capsys.readouterr().err


def test_update_reports_a_release_that_does_not_exist(monkeypatch, capsys) -> None:
    _updating(monkeypatch, release=None)

    assert cli.run(["update", "--version", "0.0.1"]) == 1
    assert "no release 0.0.1" in capsys.readouterr().err
    assert cli.run(["update"]) == 1
    assert "no release to install" in capsys.readouterr().err


def test_update_reports_a_failed_lookup_and_a_failed_install(
    monkeypatch, capsys
) -> None:
    _updating(monkeypatch)

    def offline(_version):
        raise OSError("offline")

    monkeypatch.setattr(cli, "release_of", offline)
    assert cli.run(["update", "--version", "1.0.0"]) == 1
    assert "Could not look for the release: offline" in capsys.readouterr().err

    def broken(*_args):
        raise UpdateError("The download does not match")

    monkeypatch.setattr(cli, "run_update", broken)
    assert cli.run(["update"]) == 1
    assert "does not match" in capsys.readouterr().err
