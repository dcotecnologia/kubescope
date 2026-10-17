"""Copy CHANGELOG.md into the package, where the app shows it.

python tools/sync_changelog.py

python tools/sync_changelog.py --check

The first rewrites assets/CHANGELOG.md; the second fails if it differs
from the CHANGELOG.md of the repository. The copy lives inside the
package so every channel (the bundle, pip, the Flatpak) carries the
changelog of its version.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "CHANGELOG.md"
OUTPUT = ROOT / "src" / "kubescope" / "assets" / "CHANGELOG.md"


def check_bundle(bundle: Path) -> None:
    """Refuse a PyInstaller bundle whose changelog is not the current one: it
    was built before the changelog changed, and the app would show old news."""
    shipped = bundle / "_internal" / "kubescope" / "assets" / "CHANGELOG.md"
    if not shipped.is_file() or shipped.read_bytes() != SOURCE.read_bytes():
        raise SystemExit(
            "The bundle carries an old changelog; run `make build` before packaging"
        )


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    if "--check" in sys.argv:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != text:
            print("assets/CHANGELOG.md is out of date; run this script.")
            return 1
        return 0
    OUTPUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
