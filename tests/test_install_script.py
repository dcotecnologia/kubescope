"""install.sh against a local server that stands in for the GitHub API.

The server serves a release in the shape GitHub gives, with the sha256
of each file, so the script's choices, its checks and its changes can be
tried without the network and without installing anything on this
machine.
"""

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "install.sh"
REPO = "owner/kubescope"
pytestmark = pytest.mark.skipif(
    sys.platform != "linux", reason="install.sh installs on Linux"
)


def release(version: str, files: dict[str, bytes], base: str, digests=True) -> dict:
    """A release as GitHub gives it: one key per line, the sha256 in
    `digest`."""
    assets = []
    for name, content in files.items():
        asset = {
            "url": f"{base}/api/assets/{name}",
            "name": name,
            "label": "",
            "uploader": {"login": "github-actions[bot]"},
            "content_type": "application/octet-stream",
            "state": "uploaded",
            "size": len(content),
        }
        if digests:
            asset["digest"] = "sha256:" + hashlib.sha256(content).hexdigest()
        asset["download_count"] = 0
        asset["browser_download_url"] = f"{base}/download/v{version}/{name}"
        assets.append(asset)
    return {"tag_name": f"v{version}", "name": f"v{version}", "assets": assets}


def package_files(version: str) -> dict[str, bytes]:
    return {
        f"kubescope_{version}_amd64.deb": f"deb {version}".encode(),
        f"KubeScope-{version}-x86_64.AppImage": f"appimage {version}".encode(),
    }


class Server:
    """Serves releases by version and the bytes of their files."""

    def __init__(self) -> None:
        self.versions = ["1.1.0", "1.2.0"]  # the last one is the latest
        self.digests = True
        self.corrupt: set[str] = set()  # files whose bytes differ from their digest
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args) -> None:
                pass

            def reply(self, body: bytes, status: int = 200) -> None:
                self.send_response(status)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:
                base = f"http://127.0.0.1:{outer.port}"
                path = self.path
                latest = outer.versions[-1]
                if path == f"/repos/{REPO}/releases/latest":
                    version = latest
                elif path.startswith(f"/repos/{REPO}/releases/tags/v"):
                    version = path.rsplit("/v", 1)[1]
                elif path.startswith("/download/v"):
                    _, _, version, name = path.split("/", 3)
                    content = package_files(version[1:])[name]
                    if name in outer.corrupt:
                        content = b"not what was published"
                    return self.reply(content)
                else:
                    return self.reply(b"{}", 404)
                if version not in outer.versions:
                    return self.reply(b'{"message": "Not Found"}', 404)
                document = release(
                    version, package_files(version), base, digests=outer.digests
                )
                self.reply(json.dumps(document, indent=2).encode())

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()


@pytest.fixture
def server():
    instance = Server()
    yield instance
    instance.close()


@pytest.fixture
def home(tmp_path):
    folder = tmp_path / "home"
    folder.mkdir()
    return folder


ESSENTIALS = (
    "sh", "sed", "awk", "head", "tail", "cut", "sort", "uname", "id", "mktemp", "rm",
    "cp", "chmod", "ln", "mkdir", "sha256sum", "printf", "dirname",
)  # fmt: skip


def only_these_tools(folder: Path, *names: str) -> Path:
    """A folder of links to just the tools the script needs, so that nothing
    else on this machine (a real apt, a real sudo) can answer for it."""
    folder.mkdir()
    for name in (*ESSENTIALS, *names):
        found = shutil.which(name)
        if found:
            (folder / name).symlink_to(found)
    return folder


def fake_command(folder: Path, name: str, body: str) -> None:
    path = folder / name
    path.write_text(f"#!/bin/sh\n{body}\n", encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def run(server, home, *arguments, path="", env=None):
    environment = {
        "PATH": f"{path}:{os.environ['PATH']}" if path else os.environ["PATH"],
        "HOME": str(home),
        "KUBESCOPE_REPO": REPO,
        "KUBESCOPE_API": f"http://127.0.0.1:{server.port}",
        **(env or {}),
    }
    return subprocess.run(
        ["sh", str(SCRIPT), *arguments],
        capture_output=True,
        text=True,
        env=environment,
        check=False,
        timeout=60,
    )


def data_dir(home: Path) -> Path:
    return home / ".local" / "share" / "kubescope"


def test_help_and_bad_options(server, home) -> None:
    helped = run(server, home, "--help")
    assert helped.returncode == 0 and "Usage: install.sh" in helped.stdout

    for arguments, message in (
        (("--nope",), "unknown option"),
        (("--method", "rpm"), "deb or appimage"),
        (("--version",), "needs a value"),
    ):
        failed = run(server, home, *arguments)
        assert failed.returncode == 1 and message in failed.stderr


def test_a_dry_run_names_the_file_and_changes_nothing(server, home) -> None:
    result = run(server, home, "--dry-run", "--method", "appimage")

    assert result.returncode == 0, result.stderr
    assert "Installing KubeScope 1.2.0 (appimage)" in result.stdout
    assert "KubeScope-1.2.0-x86_64.AppImage" in result.stdout
    expected = hashlib.sha256(b"appimage 1.2.0").hexdigest()
    assert expected in result.stdout
    assert "Dry run" in result.stdout
    assert not data_dir(home).exists()


def test_the_appimage_is_installed_and_linked(server, home) -> None:
    result = run(server, home, "--method", "appimage")

    assert result.returncode == 0, result.stderr
    installed = data_dir(home) / "KubeScope-1.2.0-x86_64.AppImage"
    assert installed.read_bytes() == b"appimage 1.2.0"
    assert os.access(installed, os.X_OK)
    link = home / ".local" / "bin" / "kubescope"
    assert link.is_symlink() and link.resolve() == installed.resolve()
    assert "Checked the sha256" in result.stdout
    assert "not in your PATH" in result.stdout  # the test PATH lacks ~/.local/bin


def test_running_it_again_finds_nothing_to_do_until_forced(server, home) -> None:
    run(server, home, "--method", "appimage")

    again = run(server, home, "--method", "appimage")
    assert "already installed and up to date" in again.stdout
    assert "Downloading" not in again.stdout

    forced = run(server, home, "--method", "appimage", "--force")
    assert "Downloading" in forced.stdout and forced.returncode == 0


def test_an_older_version_is_updated_and_the_old_file_goes(server, home) -> None:
    run(server, home, "--method", "appimage", "--version", "1.1.0")
    old = data_dir(home) / "KubeScope-1.1.0-x86_64.AppImage"
    assert old.exists()

    result = run(server, home, "--method", "appimage")

    assert "Updating KubeScope 1.1.0 -> 1.2.0" in result.stdout
    assert not old.exists()
    link = home / ".local" / "bin" / "kubescope"
    assert link.resolve().name == "KubeScope-1.2.0-x86_64.AppImage"


def test_a_newer_install_is_left_alone_unless_a_version_is_asked(server, home) -> None:
    newer = data_dir(home) / "KubeScope-2.0.0-x86_64.AppImage"
    newer.parent.mkdir(parents=True)
    newer.write_text("future")

    result = run(server, home, "--method", "appimage")
    assert "newer than the latest release" in result.stdout and newer.exists()

    asked = run(server, home, "--method", "appimage", "--version", "1.1.0")
    assert "Updating KubeScope 2.0.0 -> 1.1.0" in asked.stdout
    assert (data_dir(home) / "KubeScope-1.1.0-x86_64.AppImage").exists()
    assert not newer.exists()


def test_a_download_that_does_not_match_its_sha256_installs_nothing(
    server, home
) -> None:
    server.corrupt.add("KubeScope-1.2.0-x86_64.AppImage")

    result = run(server, home, "--method", "appimage")

    assert result.returncode == 1
    assert "does not match" in result.stderr
    assert not (home / ".local" / "bin" / "kubescope").exists()
    assert not list(data_dir(home).glob("*")) if data_dir(home).exists() else True


def test_without_a_published_sha256_it_stops_unless_told_to_go_on(server, home) -> None:
    server.digests = False

    refused = run(server, home, "--method", "appimage")
    assert refused.returncode == 1 and "no sha256" in refused.stderr
    assert not data_dir(home).exists()

    allowed = run(
        server, home, "--method", "appimage", env={"KUBESCOPE_ALLOW_UNVERIFIED": "1"}
    )
    assert allowed.returncode == 0, allowed.stderr
    assert "not published" in allowed.stdout
    assert (data_dir(home) / "KubeScope-1.2.0-x86_64.AppImage").exists()


def test_a_version_that_does_not_exist_is_reported(server, home) -> None:
    result = run(server, home, "--method", "appimage", "--version", "9.9.9")

    assert result.returncode == 1
    assert "could not read the release" in result.stderr


def test_other_systems_get_a_clear_answer(server, home, tmp_path) -> None:
    fakes = tmp_path / "fakes"
    fakes.mkdir()
    for system, machine, message in (
        ("Darwin", "arm64", "no macOS package"),
        ("MINGW64_NT-10.0", "x86_64", "install.ps1"),
        ("FreeBSD", "amd64", "unsupported system"),
        ("Linux", "aarch64", "only x86_64"),
    ):
        fake_command(
            fakes,
            "uname",
            f'if [ "$1" = -m ]; then echo {machine}; else echo {system}; fi',
        )
        result = run(server, home, path=str(fakes))
        assert result.returncode == 1 and message in result.stderr, (
            system,
            result.stderr,
        )


def test_an_insecure_api_is_refused(server, home) -> None:
    result = run(server, home, env={"KUBESCOPE_API": "http://example.com"})

    assert result.returncode == 1 and "https URL" in result.stderr


def test_the_deb_is_installed_through_apt_with_sudo(server, home, tmp_path) -> None:
    fakes = tmp_path / "fakes"
    fakes.mkdir()
    log = tmp_path / "sudo.log"
    fake_command(fakes, "sudo", f'echo "$@" >> {log}')
    fake_command(fakes, "dpkg", "exit 0")
    fake_command(fakes, "apt-get", "exit 0")
    fake_command(fakes, "dpkg-query", "exit 1")  # nothing installed yet

    result = run(server, home, path=str(fakes))

    assert result.returncode == 0, result.stderr
    assert "Installing KubeScope 1.2.0 (deb)" in result.stdout
    called = log.read_text(encoding="utf-8").split()
    assert called[:3] == ["apt-get", "install", "-y"]
    assert called[3].endswith("kubescope_1.2.0_amd64.deb")


def test_an_installed_deb_is_updated_but_a_removed_one_counts_as_absent(
    server, home, tmp_path
) -> None:
    fakes = tmp_path / "fakes"
    fakes.mkdir()
    fake_command(fakes, "sudo", "exit 0")
    fake_command(fakes, "dpkg", "exit 0")
    fake_command(fakes, "apt-get", "exit 0")

    fake_command(fakes, "dpkg-query", "echo 'ii |1.1.0'")
    updated = run(server, home, "--dry-run", path=str(fakes))
    assert "Updating KubeScope 1.1.0 -> 1.2.0 (deb)" in updated.stdout

    fake_command(fakes, "dpkg-query", "echo 'rc |1.2.0'")  # removed, settings kept
    removed = run(server, home, "--dry-run", path=str(fakes))
    assert "Installing KubeScope 1.2.0 (deb)" in removed.stdout


def test_without_apt_or_sudo_the_default_is_the_appimage(
    server, home, tmp_path
) -> None:
    tools = only_these_tools(tmp_path / "tools", "curl")
    fake_command(tools, "dpkg", "exit 0")  # dpkg alone is not enough: no apt-get

    result = run(server, home, "--dry-run", env={"PATH": str(tools)})

    assert "(appimage)" in result.stdout


def test_wget_is_used_when_curl_is_missing(server, home, tmp_path) -> None:
    wget = shutil.which("wget")
    if wget is None:
        pytest.skip("wget is not installed here")
    tools = only_these_tools(tmp_path / "tools", "wget")
    environment = {
        "PATH": str(tools),
        "HOME": str(home),
        "KUBESCOPE_REPO": REPO,
        "KUBESCOPE_API": f"http://127.0.0.1:{server.port}",
    }

    result = subprocess.run(
        [str(tools / "sh"), str(SCRIPT), "--method", "appimage"],
        capture_output=True,
        text=True,
        env=environment,
        check=False,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert (data_dir(home) / "KubeScope-1.2.0-x86_64.AppImage").exists()


def test_the_powershell_script_parses_and_refuses_other_systems() -> None:
    pwsh = shutil.which("pwsh")
    if pwsh is None:
        pytest.skip("PowerShell is not installed here")
    script = SCRIPT.with_name("install.ps1")
    parse = (
        "$e = $null; $t = $null; "
        f"[void][System.Management.Automation.Language.Parser]::ParseFile('{script}', "
        "[ref]$t, [ref]$e); if ($e.Count) { $e | % { $_.Message }; exit 1 }"
    )

    parsed = subprocess.run(
        [pwsh, "-NoProfile", "-Command", parse],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert parsed.returncode == 0, parsed.stdout

    ran = subprocess.run(
        [pwsh, "-NoProfile", "-File", str(script), "-DryRun"],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert ran.returncode != 0 and "for Windows" in ran.stdout + ran.stderr
