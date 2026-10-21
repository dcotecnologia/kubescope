import hashlib
import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

from kubescope.utils import selfupdate
from kubescope.utils.selfupdate import Install, UpdateError
from kubescope.utils.updates import Asset, Release

URL = "https://github.com/dcotecnologia/kubescope/releases/download/v0.7.0/"
DATA = b"payload" * 100


def release(kind: str = "deb", data: bytes = DATA) -> Release:
    name = selfupdate.asset_name(kind, "0.7.0")
    asset = Asset(name, URL + name, hashlib.sha256(data).hexdigest())
    return Release("0.7.0", "https://example.test/tag", "notes", (asset,))


class FakeResponse(io.BytesIO):
    def __init__(self, data: bytes, url: str = URL, length: bool = True) -> None:
        super().__init__(data)
        self.url = url
        self.headers = {"Content-Length": str(len(data))} if length else {}

    def geturl(self) -> str:
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False


def serve(monkeypatch, response: FakeResponse | Exception) -> None:
    def urlopen(_request, timeout):
        if isinstance(response, Exception):
            raise response
        return response

    monkeypatch.setattr(selfupdate.urllib.request, "urlopen", urlopen)


def test_detect_install_reads_how_the_app_was_installed(monkeypatch, tmp_path) -> None:
    appimage = tmp_path / "KubeScope.AppImage"
    appimage.write_bytes(b"x")
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setenv("APPIMAGE", str(appimage))
    assert selfupdate.detect_install() == Install("appimage", appimage)

    monkeypatch.delenv("APPIMAGE")
    assert selfupdate.detect_install() is None  # a source tree or a Flatpak

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(selfupdate.DEB_EXECUTABLE))
    monkeypatch.setattr(Path, "resolve", lambda self: self)
    assert selfupdate.detect_install() == Install("deb", selfupdate.DEB_EXECUTABLE)

    monkeypatch.setattr(sys, "executable", "/somewhere/else/KubeScope")
    assert selfupdate.detect_install() is None  # a bundle nothing installed

    monkeypatch.setattr(sys, "platform", "win32")
    assert selfupdate.detect_install() == Install(
        "windows", Path("/somewhere/else/KubeScope")
    )
    monkeypatch.delattr(sys, "frozen")
    assert selfupdate.detect_install() is None


def test_find_asset_picks_the_file_for_the_installation() -> None:
    wanted = release("deb")
    assert selfupdate.find_asset(Install("deb", Path("x")), wanted) is wanted.assets[0]
    assert selfupdate.find_asset(Install("appimage", Path("x")), wanted) is None


def test_download_saves_and_checks_the_file(monkeypatch, tmp_path) -> None:
    serve(monkeypatch, FakeResponse(DATA))
    seen = []

    file = selfupdate.download(
        release().assets[0], tmp_path, lambda done, total: seen.append((done, total))
    )

    assert file.read_bytes() == DATA
    assert seen == [(len(DATA), len(DATA))]


def test_download_refuses_a_file_that_does_not_match_its_sha256(
    monkeypatch, tmp_path
) -> None:
    serve(monkeypatch, FakeResponse(b"tampered"))

    with pytest.raises(UpdateError, match="sha256"):
        selfupdate.download(release().assets[0], tmp_path, lambda *_a: None)

    assert list(tmp_path.iterdir()) == []


def test_download_refuses_a_link_outside_the_releases(tmp_path) -> None:
    asset = Asset("x", "https://evil.test/x", "0" * 64)

    with pytest.raises(UpdateError, match="releases"):
        selfupdate.download(asset, tmp_path, lambda *_a: None)


def test_download_refuses_a_redirect_away_from_https(monkeypatch, tmp_path) -> None:
    serve(monkeypatch, FakeResponse(DATA, url="http://mirror.test/x"))

    with pytest.raises(UpdateError, match="HTTPS"):
        selfupdate.download(release().assets[0], tmp_path, lambda *_a: None)


def test_download_reports_network_failures(monkeypatch, tmp_path) -> None:
    serve(monkeypatch, OSError("offline"))

    with pytest.raises(UpdateError, match="offline"):
        selfupdate.download(release().assets[0], tmp_path, lambda *_a: None)


def test_download_without_a_known_size_still_works(monkeypatch, tmp_path) -> None:
    serve(monkeypatch, FakeResponse(DATA, length=False))

    file = selfupdate.download(release().assets[0], tmp_path, lambda *_a: None)

    assert file.read_bytes() == DATA


def test_the_environment_of_children_drops_the_appimage_and_bundle(
    monkeypatch,
) -> None:
    for name in ("APPIMAGE", "APPDIR", "_PYI_ARCHIVE_FILE"):
        monkeypatch.setenv(name, "x")
    monkeypatch.setenv("LD_LIBRARY_PATH", "/bundle")

    assert "APPIMAGE" not in selfupdate.clean_environment()
    assert "_PYI_ARCHIVE_FILE" not in selfupdate.clean_environment()
    assert "LD_LIBRARY_PATH" not in selfupdate.clean_environment()

    monkeypatch.setenv("LD_LIBRARY_PATH_ORIG", "/system")
    env = selfupdate.clean_environment()
    assert env["LD_LIBRARY_PATH"] == "/system" and "LD_LIBRARY_PATH_ORIG" not in env


def test_an_appimage_replaces_itself_and_its_link(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    data = tmp_path / "data"
    data.mkdir()
    old = data / "KubeScope-0.6.2-x86_64.AppImage"
    old.write_bytes(b"old")
    link = tmp_path / ".local" / "bin" / "kubescope"
    link.parent.mkdir(parents=True)
    link.symlink_to(old)
    download = tmp_path / "new.AppImage"
    download.write_bytes(b"new")

    command = selfupdate.install_download(
        Install("appimage", old), download, "0.6.2", release("appimage")
    )

    new = data / "KubeScope-0.7.0-x86_64.AppImage"
    assert new.read_bytes() == b"new" and os.access(new, os.X_OK)
    assert not old.exists() and link.resolve() == new.resolve()
    assert command == ["sh", "-c", 'sleep 1; exec "$0"', str(new)]


def test_an_appimage_with_another_name_is_replaced_in_place(tmp_path) -> None:
    old = tmp_path / "KubeScope.AppImage"
    old.write_bytes(b"old")
    download = tmp_path / "new"
    download.write_bytes(b"new")

    selfupdate.install_download(
        Install("appimage", old), download, "0.6.2", release("appimage")
    )

    assert old.read_bytes() == b"new"


def test_an_appimage_that_cannot_be_written_reports_it(tmp_path) -> None:
    old = tmp_path / "KubeScope-0.6.2-x86_64.AppImage"
    old.write_bytes(b"old")

    with pytest.raises(UpdateError, match="AppImage"):
        selfupdate.install_download(
            Install("appimage", old), tmp_path / "missing", "0.6.2", release("appimage")
        )


def test_a_link_to_something_else_is_left_alone(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    other = tmp_path / "other"
    other.write_bytes(b"x")
    link = tmp_path / ".local" / "bin" / "kubescope"
    link.parent.mkdir(parents=True)
    link.symlink_to(other)

    selfupdate._relink(tmp_path / "old", tmp_path / "new")

    assert link.resolve() == other.resolve()


def test_a_deb_is_installed_with_apt_through_pkexec(monkeypatch, tmp_path) -> None:
    file = tmp_path / "kubescope_0.7.0_amd64.deb"
    file.write_bytes(b"deb")
    ran = []
    monkeypatch.setattr(selfupdate.shutil, "which", lambda _name: "/usr/bin/pkexec")

    def run(command, **_kwargs):
        ran.append(command)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(selfupdate.subprocess, "run", run)

    command = selfupdate.install_download(
        Install("deb", selfupdate.DEB_EXECUTABLE), file, "0.6.2", release()
    )

    assert ran[0][:2] == ["pkexec", "env"] and ran[0][-4:] == [
        "install",
        "-y",
        "--allow-downgrades",
        str(file),
    ]
    assert command[-1] == str(selfupdate.DEB_EXECUTABLE)
    assert file.stat().st_mode & 0o777 == 0o644


def test_a_deb_without_pkexec_says_what_to_run(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(selfupdate.shutil, "which", lambda _name: None)

    with pytest.raises(UpdateError, match="sudo apt-get install"):
        selfupdate._install_deb(tmp_path / "x.deb")


def test_a_deb_that_apt_refuses_reports_why(monkeypatch, tmp_path) -> None:
    file = tmp_path / "x.deb"
    file.write_bytes(b"deb")
    monkeypatch.setattr(selfupdate.shutil, "which", lambda _name: "/usr/bin/pkexec")
    monkeypatch.setattr(
        selfupdate.subprocess,
        "run",
        lambda command, **_k: subprocess.CompletedProcess(
            command, 126, "", "Error: Request dismissed\nmore"
        ),
    )

    with pytest.raises(UpdateError, match="Request dismissed"):
        selfupdate._install_deb(file)


def test_the_windows_installer_runs_silently_after_the_app_quits(tmp_path) -> None:
    setup = tmp_path / "setup.exe"

    command = selfupdate.install_download(
        Install("windows", Path("C:/KubeScope/KubeScope.exe")),
        setup,
        "0.6.2",
        release("windows"),
    )

    assert isinstance(command, str) and command.startswith("cmd /c ")
    assert "/VERYSILENT" in command and "KubeScope.exe" in command
    assert str(tmp_path) in command  # removes its download


def test_run_update_downloads_checks_and_installs(monkeypatch, tmp_path) -> None:
    serve(monkeypatch, FakeResponse(DATA))
    monkeypatch.setattr(selfupdate.tempfile, "tempdir", str(tmp_path))
    stages = []
    installed = []
    monkeypatch.setattr(
        selfupdate,
        "install_download",
        lambda install, file, current, rel: (
            installed.append(file.read_bytes()) or ["go"]
        ),
    )

    command = selfupdate.run_update(
        Install("deb", selfupdate.DEB_EXECUTABLE),
        release(),
        "0.6.2",
        stages.append,
        lambda *_a: None,
    )

    assert command == ["go"] and installed == [DATA]
    assert stages == ["download", "install"]
    assert list(tmp_path.iterdir()) == []  # the download is removed


def test_run_update_keeps_the_windows_download_for_the_installer(
    monkeypatch, tmp_path
) -> None:
    serve(monkeypatch, FakeResponse(DATA))
    monkeypatch.setattr(selfupdate.tempfile, "tempdir", str(tmp_path))
    monkeypatch.setattr(selfupdate, "install_download", lambda *_a: "cmd")

    selfupdate.run_update(
        Install("windows", Path("x.exe")),
        release("windows"),
        "0.6.2",
        lambda _s: None,
        lambda *_a: None,
    )

    assert len(list(tmp_path.iterdir())) == 1


def test_run_update_cleans_up_when_it_fails(monkeypatch, tmp_path) -> None:
    serve(monkeypatch, FakeResponse(b"tampered"))
    monkeypatch.setattr(selfupdate.tempfile, "tempdir", str(tmp_path))

    with pytest.raises(UpdateError):
        selfupdate.run_update(
            Install("deb", selfupdate.DEB_EXECUTABLE),
            release(),
            "0.6.2",
            lambda _s: None,
            lambda *_a: None,
        )

    assert list(tmp_path.iterdir()) == []


def test_run_update_needs_a_verified_file() -> None:
    with pytest.raises(UpdateError, match="verified"):
        selfupdate.run_update(
            Install("deb", Path("x")),
            Release("0.7.0", "u"),
            "0.6.2",
            lambda _s: None,
            lambda *_a: None,
        )


def test_restart_starts_the_command_detached(monkeypatch) -> None:
    started = []
    monkeypatch.setattr(
        selfupdate.subprocess,
        "Popen",
        lambda command, **options: started.append((command, options)),
    )

    selfupdate.restart(["kubescope"])
    monkeypatch.setattr(sys, "platform", "win32")
    selfupdate.restart("cmd /c x")

    assert started[0][0] == ["kubescope"]
    assert started[0][1]["start_new_session"] is True
    assert started[1][0] == "cmd /c x" and "creationflags" in started[1][1]
