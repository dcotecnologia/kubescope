"""Install a newer KubeScope the way this one was installed.

The person confirms first (see `update_dialog`). Then the file of the
release is downloaded over HTTPS from this project's GitHub releases,
checked against the sha256 GitHub published for it, and installed:

- an AppImage replaces itself (and the link that points at it);
- the .deb is installed with `apt-get` through `pkexec`, which asks for
  the password in the system's own dialog;
- the Windows installer runs silently for the user once the app has quit.

A Flatpak or a source tree cannot update itself, so `detect_install`
finds nothing there. No Qt in this module.
"""

import hashlib
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from kubescope import PROJECT_URL
from kubescope.utils.errors import first_line
from kubescope.utils.updates import Asset, Release

logger = logging.getLogger(__name__)

DEB_EXECUTABLE = Path("/opt/kubescope/KubeScope")
TIMEOUT = 30  # seconds without an answer from the server
CHUNK = 256 * 1024
DOWNLOADS = f"{PROJECT_URL}/releases/download/"
_APPIMAGE_VARIABLES = ("APPIMAGE", "APPDIR", "ARGV0", "OWD")


class UpdateError(Exception):
    """The update could not be done; the message says why, for the person."""


@dataclass(frozen=True, slots=True)
class Install:
    kind: str  # "appimage", "deb" or "windows"
    path: Path  # the AppImage, or the executable that is running


def detect_install() -> Install | None:
    """How this KubeScope was installed, or None when it cannot update itself
    (a Flatpak, which Flathub updates, or a source tree)."""
    if sys.platform == "win32":
        return Install("windows", Path(sys.executable)) if _frozen() else None
    appimage = os.environ.get("APPIMAGE")
    if appimage and Path(appimage).is_file():
        return Install("appimage", Path(appimage))
    if _frozen() and Path(sys.executable).resolve() == DEB_EXECUTABLE:
        return Install("deb", DEB_EXECUTABLE)
    return None


def _frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def asset_name(kind: str, version: str) -> str:
    """The file of a release that installs on this kind of installation."""
    return {
        "appimage": f"KubeScope-{version}-x86_64.AppImage",
        "deb": f"kubescope_{version}_amd64.deb",
        "windows": f"KubeScope-{version}-windows-x64-setup.exe",
    }[kind]


def find_asset(install: Install, release: Release) -> Asset | None:
    wanted = asset_name(install.kind, release.version)
    return next((asset for asset in release.assets if asset.name == wanted), None)


def download(
    asset: Asset, directory: Path, progress: Callable[[int, int], None]
) -> Path:
    """Save the asset in `directory`, reporting (bytes, total), and fail unless
    its sha256 is the one GitHub published."""
    if not asset.url.startswith(DOWNLOADS):
        raise UpdateError("The download is not from the KubeScope releases.")
    target = directory / asset.name
    digest = hashlib.sha256()
    request = urllib.request.Request(asset.url)
    try:
        with (
            urllib.request.urlopen(request, timeout=TIMEOUT) as response,
            target.open("wb") as out,
        ):
            if not response.geturl().startswith("https://"):
                raise UpdateError("The download was redirected away from HTTPS.")
            total = int(response.headers.get("Content-Length") or 0)
            done = 0
            while chunk := response.read(CHUNK):
                out.write(chunk)
                digest.update(chunk)
                done += len(chunk)
                progress(done, total)
    except OSError as error:
        raise UpdateError(f"Could not download the update: {error}") from error
    if digest.hexdigest() != asset.sha256:
        target.unlink(missing_ok=True)
        raise UpdateError("The download does not match the sha256 GitHub published.")
    return target


def clean_environment() -> dict[str, str]:
    """The environment for a program started from here: without the variables
    of the AppImage or the bundle, which point at files that go away."""
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in _APPIMAGE_VARIABLES and not key.startswith("_PYI")
    }
    original = env.pop("LD_LIBRARY_PATH_ORIG", None)
    if original is None:
        env.pop("LD_LIBRARY_PATH", None)
    else:
        env["LD_LIBRARY_PATH"] = original
    return env


def install_download(
    install: Install, file: Path, current: str, release: Release
) -> list[str] | str:
    """Install the downloaded file and return the command that starts the new
    version once this process has quit."""
    if install.kind == "appimage":
        target = _replace_appimage(install.path, file, current, release.version)
        return _delayed([str(target)])
    if install.kind == "deb":
        _install_deb(file)
        return _delayed([str(install.path)])
    return _windows_command(file, install.path)


def _delayed(command: list[str]) -> list[str]:
    """Start `command` a moment later, when this process has quit and saved its
    settings."""
    return ["sh", "-c", 'sleep 1; exec "$0"', *command]


def _replace_appimage(path: Path, file: Path, current: str, version: str) -> Path:
    name = path.name.replace(current, version) if current in path.name else path.name
    target = path.with_name(name)
    staged = target.with_name(target.name + ".new")
    try:
        shutil.copyfile(file, staged)
        staged.chmod(0o755)
        os.replace(staged, target)
        if target != path:
            _relink(path, target)
            path.unlink(missing_ok=True)
    except OSError as error:
        staged.unlink(missing_ok=True)
        raise UpdateError(f"Could not replace the AppImage: {error}") from error
    return target


def _relink(old: Path, new: Path) -> None:
    """Point the `kubescope` link that install.sh makes at the new file."""
    link = Path.home() / ".local" / "bin" / "kubescope"
    if link.is_symlink() and link.resolve() == old.resolve():
        link.unlink()
        link.symlink_to(new)


def _install_deb(file: Path) -> None:
    if shutil.which("pkexec") is None:
        raise UpdateError(
            "Updating the .deb needs pkexec. Install it, or run: "
            f"sudo apt-get install {file}"
        )
    # apt downloads as the _apt user, which must be able to read the file
    file.parent.chmod(0o755)
    file.chmod(0o644)
    result = subprocess.run(
        [
            "pkexec",
            "env",
            "DEBIAN_FRONTEND=noninteractive",
            "apt-get",
            "install",
            "-y",
            str(file),
        ],
        capture_output=True,
        text=True,
        env=clean_environment(),
        check=False,
    )
    if result.returncode != 0:
        detail = first_line(result.stderr or result.stdout)
        logger.error("apt-get failed: %s", result.stderr)
        raise UpdateError(f"The package could not be installed: {detail}")


def _windows_command(setup: Path, executable: Path) -> str:
    """Run the installer silently, start the app and remove the download, from
    a shell of its own so it can replace the files of this process once it has
    quit.

    A string, not a list: cmd does not read the quotes Python adds.
    """
    return (
        f'cmd /c ""{setup}" /VERYSILENT /SUPPRESSMSGBOXES /NORESTART'
        f' & start "" "{executable}" & rmdir /s /q "{setup.parent}""'
    )


def run_update(
    install: Install,
    release: Release,
    current: str,
    stage: Callable[[str], None],
    progress: Callable[[int, int], None],
) -> list[str] | str:
    """Download, check and install the release; returns the restart command.

    The Windows installer runs after this process has quit, so its
    download stays on disk and the command removes it.
    """
    asset = find_asset(install, release)
    if asset is None:
        raise UpdateError("This release has no verified file for this installation.")
    directory = Path(tempfile.mkdtemp(prefix="kubescope-update-"))
    try:
        stage("download")
        file = download(asset, directory, progress)
        stage("install")
        command = install_download(install, file, current, release)
    except BaseException:
        shutil.rmtree(directory, ignore_errors=True)
        raise
    if install.kind != "windows":
        shutil.rmtree(directory, ignore_errors=True)
    return command


def restart(command: list[str] | str) -> None:
    """Start the command detached from this process."""
    options: dict = {"start_new_session": True}
    if sys.platform == "win32":
        options = {"creationflags": 0x00000008 | 0x00000200}  # detached, new group
    subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=clean_environment(),
        **options,
    )
