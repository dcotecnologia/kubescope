"""Check the Flatpak files and gather what a Flathub submission needs.

Flathub has no deploy command: an app is added by a pull request to
github.com/flathub/flathub, reviewers read it, and Flathub builds it.
This tool does what can be done here, and sends nothing anywhere:

python tools/flathub.py lint      validate the metainfo, desktop file
and manifest python tools/flathub.py package   write dist/flathub/<app
id>/ and print the steps
"""

import re
import shutil
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "packaging" / "flatpak"
APP_ID = "com.dcotecnologia.KubeScope"
MANIFEST = f"{APP_ID}.yml"
METAINFO = f"{APP_ID}.metainfo.xml"
DESKTOP = f"{APP_ID}.desktop"
ICON = ROOT / "src" / "kubescope" / "assets" / "icon.png"


SUBMISSION_STEPS = """
Read Flathub's Generative AI policy first (the requirements page of
https://docs.flathub.org/docs/for-app-authors/requirements): a manifest must not
contain AI-generated or AI-assisted content, an AI tool must not open the pull
request or write its text, and AI-generated code or packaging in the app must be
disclosed. The files here are a starting point to check and to rewrite by hand,
not text to send.

To submit it (nothing is sent from here):
  1. Fork https://github.com/flathub/flathub with "Copy the master branch only"
     unchecked, and clone your fork on its `new-pr` branch:
     git clone --branch=new-pr git@github.com:<you>/flathub.git
  2. Create a branch from `new-pr` and add your manifest and its files at the root
     of the repository.
  3. Open a pull request against the `new-pr` base branch of flathub/flathub, titled
     "Add com.dcotecnologia.KubeScope", and keep its template. Reviewers answer on
     the pull request. When it is accepted, Flathub creates the repository
     github.com/flathub/com.dcotecnologia.KubeScope; later updates are changes to it.
  See https://docs.flathub.org/docs/for-app-authors/submission for the rules.
"""


def project_version() -> str:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["version"]


def render_sources(destination: Path, version: str) -> None:
    """Copy the packaging files, filling in the version and today's date."""
    destination.mkdir(parents=True, exist_ok=True)
    for path in SOURCE.iterdir():
        text = path.read_text(encoding="utf-8")
        text = text.replace("@VERSION@", version).replace("@DATE@", str(date.today()))
        (destination / path.name).write_text(text, encoding="utf-8")


def render_icons(destination: Path) -> None:
    """The two icon sizes the manifest installs."""
    source = QImage(str(ICON))
    for size in (256, 512):
        source.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        ).save(str(destination / f"icon-{size}.png"), "PNG")


def blockers(manifest: str) -> list[str]:
    """What Flathub reviewers will not accept in this manifest as it is: it
    must build from public sources, not from files that only exist on this
    machine."""
    found = []
    if re.search(r"type:\s*dir\b", manifest):
        found.append(
            "a `type: dir` source: the app is built from a local PyInstaller bundle "
            "(`make build`); Flathub builds from a public source (a git tag or an "
            "archive with its sha256), through Python modules, not a prebuilt bundle"
        )
    if "awscli.amazonaws.com" in manifest:
        found.append(
            "the AWS CLI is downloaded already built; Flathub asks for open source "
            "software to be built from its source, or the dependency to be left out"
        )
    if "--filesystem=~/.aws" in manifest:
        found.append(
            "`--filesystem=~/.aws` is a broad permission; be ready to justify it, "
            "or narrow it, in the review"
        )
    if "--talk-name=org.freedesktop.Flatpak" in manifest:
        found.append(
            "`--talk-name=org.freedesktop.Flatpak` lets the app run programs on the "
            "host (`flatpak-spawn --host`); Flathub reviews it case by case, so be "
            "ready to explain that GKE, AKS and OCI sign-ins need the tools of the "
            "system"
        )
    return found


def check_tag(manifest: str) -> bool:
    """The git source must name a tag that exists and the commit it points at,
    or Flathub cannot build what the manifest says."""
    found = re.search(r"type: git\s+url: (\S+)\s+tag: (\S+)\s+commit: (\w+)", manifest)
    if not found:
        print("No git source with a tag and a commit in the manifest")
        return False
    url, tag, commit = found.groups()
    result = subprocess.run(
        ["git", "ls-remote", url, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    commits = {line.split()[0] for line in result.stdout.splitlines()}
    if commit in commits:
        print(f"The tag {tag} of {url} points at {commit[:7]}")
        return True
    print(
        f"The tag {tag} of {url} is not at {commit[:7]}: {sorted(commits) or 'no tag'}"
    )
    return False


def run(command: list[str], label: str) -> bool:
    print(f"$ {' '.join(command)}", flush=True)
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(f"  -> {label} found problems", file=sys.stderr)
    return result.returncode == 0


def builder_lint() -> list[str] | None:
    """The command for flatpak-builder-lint, installed or through Flatpak."""
    if shutil.which("flatpak-builder-lint"):
        return ["flatpak-builder-lint"]
    if (
        shutil.which("flatpak")
        and subprocess.run(
            ["flatpak", "info", "org.flatpak.Builder"],
            capture_output=True,
            check=False,
        ).returncode
        == 0
    ):
        return [
            "flatpak",
            "run",
            "--command=flatpak-builder-lint",
            "org.flatpak.Builder",
        ]
    return None


def lint() -> int:
    staging = ROOT / "build" / "flatpak-lint"
    shutil.rmtree(staging, ignore_errors=True)
    render_sources(staging, project_version())
    ok = True
    if shutil.which("appstreamcli"):
        ok &= run(
            ["appstreamcli", "validate", "--no-net", str(staging / METAINFO)],
            "the metainfo",
        )
    else:
        print("appstreamcli is missing: install appstream to validate the metainfo")
    if shutil.which("desktop-file-validate"):
        ok &= run(["desktop-file-validate", str(staging / DESKTOP)], "the desktop file")
    else:
        print("desktop-file-validate is missing: install desktop-file-utils")
    linter = builder_lint()
    if linter is None:
        print(
            "flatpak-builder-lint is missing, and it is what Flathub runs. Install it "
            "with `flatpak install flathub org.flatpak.Builder`."
        )
    else:
        ok &= run([*linter, "manifest", str(staging / MANIFEST)], "the manifest")
        ok &= run([*linter, "appstream", str(staging / METAINFO)], "the metainfo")
    manifest = (staging / MANIFEST).read_text(encoding="utf-8")
    ok &= check_tag(manifest)
    for item in blockers(manifest):
        print(f"Flathub will not accept as it is: {item}")
    return 0 if ok else 1


def package() -> int:
    output = ROOT / "dist" / "flathub" / APP_ID
    shutil.rmtree(output, ignore_errors=True)
    render_sources(output, project_version())
    render_icons(output)
    manifest = (output / MANIFEST).read_text(encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}/")
    print(SUBMISSION_STEPS)
    found = blockers(manifest)
    if found:
        print("\nBefore it can be accepted, the manifest needs work:")
        for item in found:
            print(f"  - {item}")
    return 0


def main() -> int:
    commands = {"lint": lint, "package": package}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        raise SystemExit(__doc__)
    return commands[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
