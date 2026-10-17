"""Build the Flatpak from the manifest, as a bundle in dist/.

The manifest builds from public sources, like Flathub does. Here the app
itself comes from this working tree instead of its git tag, so a change
that is not committed yet can be tried. Needs flatpak-builder and the
runtimes the manifest names (`flatpak install flathub
org.kde.Platform//6.11 org.kde.Sdk//6.11 io.qt.PySide.BaseApp//6.11`).

FLATPAK_BUILDER_ARGS adds options to flatpak-builder, for example
`--user`.
"""

import os
import re
import shlex
import shutil
import subprocess
import sys

try:  # as a module (the tests) or as a script (tools/ is then the import path)
    from tools import sync_changelog
except ImportError:
    import sync_changelog  # type: ignore[no-redef]
from flathub import (
    APP_ID,
    MANIFEST,
    ROOT,
    project_version,
    render_icons,
    render_sources,
)

STAGING = ROOT / "build" / "flatpak"
# what a local build leaves out of the copy of the working tree
SKIP = (".git", ".venv", "build", "dist", "vendor", "coverage.xml", "__pycache__")
GIT_SOURCE = re.compile(
    r"      - type: git\n        url: https://github.com/dcotecnologia/kubescope.git\n"
    r"        tag: \S+\n        commit: \w+\n"
)


def use_working_tree(manifest: str) -> str:
    """Point the app's source at this checkout instead of its git tag."""
    skipped = "".join(f"          - {name}\n" for name in SKIP)
    local = f"      - type: dir\n        path: {ROOT}\n        skip:\n{skipped}"
    result, count = GIT_SOURCE.subn(local, manifest)
    if count != 1:
        raise SystemExit("The manifest has no git source for KubeScope to replace")
    return result


def main() -> int:
    if sys.platform != "linux" or not shutil.which("flatpak-builder"):
        raise SystemExit("Building a Flatpak needs Linux with flatpak-builder")
    version = project_version()

    if STAGING.exists():
        shutil.rmtree(STAGING)
    render_sources(STAGING, version)
    # the Flatpak is built from this tree, which must carry the current changelog
    sync_changelog.main()
    manifest = STAGING / MANIFEST
    manifest.write_text(
        use_working_tree(manifest.read_text(encoding="utf-8")), encoding="utf-8"
    )
    render_icons(STAGING)

    repository = STAGING / "repo"
    subprocess.run(
        [
            "flatpak-builder",
            "--force-clean",
            "--disable-rofiles-fuse",
            *shlex.split(os.environ.get("FLATPAK_BUILDER_ARGS", "")),
            f"--repo={repository}",
            str(STAGING / "build-dir"),
            str(manifest),
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
