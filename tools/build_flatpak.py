"""Package dist/KubeScope (from `make build`) as a Flatpak bundle.

Needs flatpak-builder and the org.freedesktop.Platform and Sdk 25.08
runtimes (`flatpak install flathub org.freedesktop.Platform//25.08
org.freedesktop.Sdk//25.08`).
"""

import shutil
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "dist" / "KubeScope"
ICON = ROOT / "src" / "kubescope" / "assets" / "icon.png"
SOURCE = ROOT / "packaging" / "flatpak"
STAGING = ROOT / "build" / "flatpak"
APP_ID = "com.dcotecnologia.KubeScope"
MANIFEST = f"{APP_ID}.yml"


def main() -> int:
    if sys.platform != "linux" or not shutil.which("flatpak-builder"):
        raise SystemExit("Building a Flatpak needs Linux with flatpak-builder")
    if not (BUNDLE / "KubeScope").is_file():
        raise SystemExit("Run `make build` before packaging the Flatpak")
    with (ROOT / "pyproject.toml").open("rb") as handle:
        version = tomllib.load(handle)["project"]["version"]

    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)
    for path in SOURCE.iterdir():
        text = path.read_text(encoding="utf-8")
        text = text.replace("@VERSION@", version).replace("@DATE@", str(date.today()))
        (STAGING / path.name).write_text(text, encoding="utf-8")
    (STAGING / "bundle").symlink_to(BUNDLE)

    source = QImage(str(ICON))
    for size in (256, 512):
        source.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        ).save(str(STAGING / f"icon-{size}.png"), "PNG")

    repository = STAGING / "repo"
    subprocess.run(
        [
            "flatpak-builder",
            "--force-clean",
            "--disable-rofiles-fuse",
            f"--repo={repository}",
            str(STAGING / "build-dir"),
            str(STAGING / MANIFEST),
        ],
        check=True,
        cwd=STAGING,
    )
    output = ROOT / "dist" / f"KubeScope-{version}.flatpak"
    subprocess.run(
        ["flatpak", "build-bundle", str(repository), str(output), APP_ID],
        check=True,
    )
    print(f"Created {output} ({output.stat().st_size / 2**20:.0f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
