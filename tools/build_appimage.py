"""Package dist/KubeScope (from `make build`) as a single-file AppImage."""

import hashlib
import os
import shutil
import stat
import subprocess
import sys
import tomllib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "dist" / "KubeScope"
ICON = ROOT / "src" / "kubescope" / "assets" / "icon.png"
APPDIR = ROOT / "build" / "KubeScope.AppDir"
TOOL_DIR = ROOT / "vendor" / "appimagetool"

# Pinned release; GitHub publishes the SHA-256 of every asset.
TOOL_VERSION = "1.9.1"
TOOL_SHA256 = "ed4ce84f0d9caff66f50bcca6ff6f35aae54ce8135408b3fa33abfc3cb384eb0"
TOOL_URL = (
    "https://github.com/AppImage/appimagetool/releases/download/"
    f"{TOOL_VERSION}/appimagetool-x86_64.AppImage"
)

APP_RUN = """#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/lib/kubescope/KubeScope" "$@"
"""

DESKTOP_ENTRY = """[Desktop Entry]
Type=Application
Name=KubeScope
Comment=Desktop viewer for Kubernetes and Amazon EKS workloads
Exec=KubeScope
Icon=kubescope
Terminal=false
Categories=Development;System;
StartupWMClass=KubeScope
"""


def fetch_appimagetool() -> Path:
    tool = TOOL_DIR / f"appimagetool-{TOOL_VERSION}-x86_64.AppImage"
    if not tool.is_file():
        print(f"Downloading appimagetool {TOOL_VERSION}...")
        TOOL_DIR.mkdir(parents=True, exist_ok=True)
        partial = tool.with_suffix(".part")
        with urllib.request.urlopen(TOOL_URL, timeout=60) as response:
            partial.write_bytes(response.read())
        digest = hashlib.sha256(partial.read_bytes()).hexdigest()
        if digest != TOOL_SHA256:
            partial.unlink()
            raise SystemExit(f"appimagetool checksum mismatch: {digest}")
        partial.replace(tool)
    tool.chmod(tool.stat().st_mode | stat.S_IXUSR)
    return tool


def project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["version"]


def build_appdir() -> None:
    if APPDIR.exists():
        shutil.rmtree(APPDIR)
    shutil.copytree(BUNDLE, APPDIR / "usr" / "lib" / "kubescope", symlinks=True)
    icon_dir = APPDIR / "usr" / "share" / "icons" / "hicolor" / "512x512" / "apps"
    icon_dir.mkdir(parents=True)
    shutil.copy(ICON, icon_dir / "kubescope.png")
    shutil.copy(ICON, APPDIR / "kubescope.png")
    shutil.copy(ICON, APPDIR / ".DirIcon")
    (APPDIR / "kubescope.desktop").write_text(DESKTOP_ENTRY, encoding="utf-8")
    app_run = APPDIR / "AppRun"
    app_run.write_text(APP_RUN, encoding="utf-8")
    app_run.chmod(0o755)


def main() -> int:
    if sys.platform != "linux":
        raise SystemExit("AppImage can only be built on Linux")
    if not (BUNDLE / "KubeScope").is_file():
        raise SystemExit("Run `make build` before packaging the AppImage")
    tool = fetch_appimagetool()
    build_appdir()
    output = ROOT / "dist" / f"KubeScope-{project_version()}-x86_64.AppImage"
    # extract-and-run lets appimagetool work on machines without FUSE
    environment = {**os.environ, "ARCH": "x86_64", "APPIMAGE_EXTRACT_AND_RUN": "1"}
    subprocess.run([str(tool), str(APPDIR), str(output)], check=True, env=environment)
    print(f"Created {output} ({output.stat().st_size / 2**20:.0f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
