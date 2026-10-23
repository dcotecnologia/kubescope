"""Package dist/KubeScope (from `make build`) as a Snap.

Run it as `python tools/build_snap.py` to build dist/dco-
kubescope_<version>_amd64.snap, or with `--stage` to only lay out
build/snap, for snapcraft to pack.

The snap carries the PyInstaller bundle, like the .deb and the AppImage,
and is classic: it runs the tools of the system (aws, gcloud, az,
kubelogin, oci...) that the kubeconfig names to sign in, so it works
with every cloud.

snapcraft runs in LXD by default; SNAPCRAFT_BUILD_ARGS adds options to
it, for example `--destructive-mode` on an Ubuntu 24.04 machine.
"""

import os
import re
import shlex
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

try:  # as a module (the tests) or as a script (tools/ is then the import path)
    from tools import sync_changelog
except ImportError:
    import sync_changelog  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "dist" / "KubeScope"
ICON = ROOT / "src" / "kubescope" / "assets" / "icon.png"
PACKAGING = ROOT / "packaging" / "snap"
STAGING = ROOT / "build" / "snap"

# The Snap Store reserves "kubescope", so the snap is registered as this name.
SNAP_NAME = "dco-kubescope"

PLACEHOLDER = re.compile(r"@[A-Z0-9_]+@")


def project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["version"]


def render_snapcraft(version: str) -> str:
    """snapcraft.yaml with the version of the app."""
    text = (PACKAGING / "snapcraft.yaml").read_text(encoding="utf-8")
    text = text.replace("@VERSION@", version)
    leftover = PLACEHOLDER.search(text)
    if leftover:
        raise SystemExit(f"snapcraft.yaml has an unfilled value: {leftover.group(0)}")
    return text


def stage(version: str) -> Path:
    """Lay out what snapcraft packs: the bundle and snap/."""
    if STAGING.exists():
        shutil.rmtree(STAGING)
    shutil.copytree(BUNDLE, STAGING / "bundle", symlinks=True)
    gui = STAGING / "snap" / "gui"
    gui.mkdir(parents=True)
    shutil.copy(PACKAGING / "dco-kubescope.desktop", gui / "dco-kubescope.desktop")
    shutil.copy(ICON, gui / "dco-kubescope.png")
    (STAGING / "snap" / "snapcraft.yaml").write_text(
        render_snapcraft(version), encoding="utf-8"
    )
    return STAGING


def main(argv: list[str]) -> int:
    if sys.platform != "linux":
        raise SystemExit("A snap can only be built on Linux")
    if not (BUNDLE / "KubeScope").is_file():
        raise SystemExit("Run `make build` before packaging the snap")
    sync_changelog.check_bundle(BUNDLE)  # no bundle from before the last change
    stage_only = "--stage" in argv
    if not stage_only and not shutil.which("snapcraft"):
        raise SystemExit(
            "Building a snap needs snapcraft (`sudo snap install snapcraft --classic`)"
        )
    version = project_version()
    staging = stage(version)
    if stage_only:
        print(f"Staged {staging}")
        return 0
    output = ROOT / "dist" / f"{SNAP_NAME}_{version}_amd64.snap"
    output.parent.mkdir(exist_ok=True)
    arguments = shlex.split(os.environ.get("SNAPCRAFT_BUILD_ARGS", ""))
    subprocess.run(
        ["snapcraft", "pack", "--output", str(output), *arguments],
        cwd=staging,
        check=True,
    )
    print(f"Created {output} ({output.stat().st_size / 2**20:.0f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
