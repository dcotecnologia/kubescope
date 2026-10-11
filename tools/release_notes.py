"""Print the release notes of a version: its section of CHANGELOG.md.

python tools/release_notes.py v0.2.0

The release workflow publishes this text as the body of the GitHub
release, so the notes people read are the ones written in the changelog.
The link to the comparison with the previous version is added at the
end.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def release_notes(changelog: str, version: str) -> str:
    """The section of `version` (like "0.2.0"), without its heading, followed
    by the link that compares it with the previous release."""
    heading = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n", changelog, re.M)
    if heading is None:
        raise ValueError(f"CHANGELOG.md has no section for {version}")
    following = re.search(r"^## \[|^\[[^\]]+\]: ", changelog[heading.end() :], re.M)
    end = heading.end() + following.start() if following else len(changelog)
    notes = changelog[heading.end() : end].strip()
    link = re.search(rf"^\[{re.escape(version)}\]: (\S+)", changelog, re.M)
    if link:
        notes += f"\n\n**Full changelog**: {link.group(1)}"
    return notes + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/release_notes.py <tag, like v0.2.0>")
    version = sys.argv[1].removeprefix("v")
    try:
        text = release_notes(
            (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), version
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
