"""The command line: a few commands that answer on the terminal and exit,
without opening the window."""

import argparse
import platform
import sys
from collections.abc import Sequence
from pathlib import Path

from kubescope import __version__
from kubescope.settings import Settings, config_directory, log_directory
from kubescope.utils.diagnostics import MAX_AGE_DAYS, commit, log_files
from kubescope.utils.selfupdate import UpdateError, detect_install, restart, run_update
from kubescope.utils.updates import check_for_update, latest_release, release_of

COMMANDS = ("info", "cleanup", "check-update", "update")
FLAGS = ("--version", "-V", "--help", "-h")


def _size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def _info() -> int:
    settings = Settings()
    print(f"KubeScope {__version__} ({commit()})")
    print(f"Python {platform.python_version()} on {platform.platform()}")
    print(f"Settings: {settings.path}")
    print(f"Logs: {log_directory()}")
    print(f"Configuration folder: {config_directory()}")
    return 0


def _cleanup(everything: bool, dry_run: bool) -> int:
    """Delete the debug log, its backups and the crash log: the ones older than
    the app's own limit, or all of them with --all."""
    found = log_files(None if everything else MAX_AGE_DAYS)
    freed = 0
    for path in found:
        freed += _size(path)
        if dry_run:
            print(f"Would delete {path}")
            continue
        try:
            path.unlink(missing_ok=True)
        except OSError as error:
            print(f"Could not delete {path}: {error.strerror}", file=sys.stderr)
            return 1
        print(f"Deleted {path}")
    verb = "Would free" if dry_run else "Freed"
    print(f"{len(found)} files; {verb} {freed / 1024:.1f} KiB")
    return 0


def _check_update() -> int:
    """Exit 0 when up to date, 10 when a newer version exists, 1 when the check
    failed."""
    result = check_for_update()
    if result.status == "available" and result.release is not None:
        print(f"KubeScope {result.release.version} is available: {result.release.url}")
        return 10
    if result.status == "current":
        print(f"KubeScope {__version__} is up to date")
        return 0
    print("Could not check for updates", file=sys.stderr)
    return 1


def _update(version: str | None) -> int:
    """Install the given version, or the latest one, the way the window does:

    the file is checked against the sha256 GitHub published.
    """
    install = detect_install()
    if install is None:
        print(
            "This installation cannot update itself (a Flatpak is updated by "
            "Flathub, a source tree with git or pip).",
            file=sys.stderr,
        )
        return 1
    try:
        release = release_of(version) if version else latest_release()
    except (OSError, ValueError) as error:
        print(f"Could not look for the release: {error}", file=sys.stderr)
        return 1
    if release is None:
        print(f"There is no release {version or 'to install'}.", file=sys.stderr)
        return 1
    if release.version == __version__:
        print(f"KubeScope {__version__} is already installed")
        return 0

    def stage(name: str) -> None:
        print("Downloading..." if name == "download" else "Installing...")

    try:
        command = run_update(
            install, release, __version__, stage, lambda _done, _total: None
        )
    except UpdateError as error:
        print(str(error), file=sys.stderr)
        return 1
    if install.kind == "windows":
        restart(command)  # the installer runs after this process has quit
    print(f"KubeScope {release.version} is installed")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kubescope",
        description="Without a command, KubeScope opens its window.",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"KubeScope {__version__}"
    )
    commands = parser.add_subparsers(dest="command", metavar="command")
    commands.add_parser("info", help="show the version and where the app keeps files")
    cleanup = commands.add_parser(
        "cleanup",
        help=f"delete the debug and crash logs older than {MAX_AGE_DAYS} days",
    )
    cleanup.add_argument("--all", action="store_true", help="delete all of them")
    cleanup.add_argument(
        "-n", "--dry-run", action="store_true", help="only list what would go"
    )
    commands.add_parser(
        "check-update",
        help="look for a newer version (exit code 10 when there is one)",
    )
    update = commands.add_parser(
        "update", help="install the latest version, or the one given"
    )
    update.add_argument(
        "--version", metavar="X.Y.Z", help="the version to install (default: latest)"
    )
    return parser


def run(arguments: Sequence[str]) -> int | None:
    """Run a command line command and return its exit code, or None when the
    arguments are not one, so the window opens (Qt's own options pass through
    to it)."""
    if not arguments or arguments[0] not in (*COMMANDS, *FLAGS):
        return None
    namespace = _parser().parse_args(arguments)
    if namespace.command == "info":
        return _info()
    if namespace.command == "cleanup":
        return _cleanup(namespace.all, namespace.dry_run)
    if namespace.command == "update":
        return _update(namespace.version)
    return _check_update()
