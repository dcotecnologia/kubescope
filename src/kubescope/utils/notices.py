"""The third-party notices of the installed version, which every package
carries: what KubeScope uses and each license, split to be read one at a
time."""

import re
from dataclasses import dataclass
from pathlib import Path

# next to the other assets of the package, also once the app is bundled
NOTICES = Path(__file__).resolve().parent.parent / "assets" / "THIRD_PARTY_NOTICES.txt"

_HEADING = re.compile(r"^={20,}\n([^\n]+)\n={20,}\n", re.MULTILINE)


@dataclass(frozen=True, slots=True)
class Notice:
    title: str  # "aiohttp 3.14.5", "Qt and Qt for Python (PySide6, Shiboken6)"
    text: str


def read_notices() -> str | None:
    """The text of the notices, or None when this installation does not have
    it."""
    try:
        return NOTICES.read_text(encoding="utf-8")
    except OSError:
        return None


def parse_notices(text: str) -> list[Notice]:
    """The notices one by one, in the order of the file: first the overview (what
    is used, and under which license), then a heading and a text for each."""
    headings = list(_HEADING.finditer(text))
    first = text.splitlines()[0].strip() if text.strip() else ""
    start = headings[0].start() if headings else len(text)
    notices = [Notice(first, text[:start].strip("\n"))] if first else []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        notices.append(
            Notice(heading.group(1).strip(), text[heading.end() : end].strip("\n"))
        )
    return notices
