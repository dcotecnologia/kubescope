"""Package dist/KubeScope (from `make build`) as a Flatpak bundle.

Needs flatpak-builder and the org.freedesktop.Platform and Sdk 25.08
runtimes (`flatpak install flathub org.freedesktop.Platform//25.08
org.freedesktop.Sdk//25.08`).
"""

import shutil
import subprocess
import sys
from pathlib import Path

from flathub import project_version, render_icons, render_sources

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "dist" / "KubeScope"
STAGING = ROOT / "build" / "flatpak"
APP_ID = "com.dcotecnologia.KubeScope"
MANIFEST = f"{APP_ID}.yml"


def main() -> int:
    if sys.platform != "linux" or not shutil.which("flatpak-builder"):
        raise SystemExit("Building a Flatpak needs Linux with flatpak-builder")
    if not (BUNDLE / "KubeScope").is_file():
        raise SystemExit("Run `make build` before packaging the Flatpak")
    version = project_version()

    if STAGING.exists():
        shutil.rmtree(STAGING)
    render_sources(STAGING, version)
    (STAGING / "bundle").symlink_to(BUNDLE)

    render_icons(STAGING)

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
