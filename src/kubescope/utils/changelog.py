"""The changelog of the installed version, which every package carries."""

import html
import re
from dataclasses import dataclass, field
from pathlib import Path

# next to the other assets of the package, also once the app is bundled
CHANGELOG = Path(__file__).resolve().parent.parent / "assets" / "CHANGELOG.md"


@dataclass(frozen=True, slots=True)
class Version:
    name: str  # "0.6.2" or "Unreleased"
    date: str = ""
    sections: list[tuple[str, list[str]]] = field(default_factory=list)


def read_changelog() -> str | None:
    """The text of the changelog in Markdown, or None when this installation
    does not have it."""
    try:
        return CHANGELOG.read_text(encoding="utf-8")
    except OSError:
        return None


_VERSION = re.compile(r"^## \[([^\]]+)\](?: - (\S+))?\s*$")


def parse_changelog(text: str) -> list[Version]:
    """The versions of a Keep a Changelog file, newest first, each with its
    sections (Added, Changed, Fixed...) and their items.

    The introduction and the link references at the end are left out.
    """
    versions: list[Version] = []
    for line in text.splitlines():
        if line.startswith("[") and re.match(r"^\[[^\]]+\]: ", line):
            break  # the link references that close the file
        found = _VERSION.match(line)
        if found:
            versions.append(Version(found.group(1), found.group(2) or ""))
        elif not versions:
            continue  # the introduction
        elif line.startswith("### "):
            versions[-1].sections.append((line[4:].strip(), []))
        elif line.startswith("- ") and versions[-1].sections:
            versions[-1].sections[-1][1].append(line[2:].strip())
        elif line.startswith("  ") and line.strip() and versions[-1].sections:
            items = versions[-1].sections[-1][1]
            if items:  # a wrapped line belongs to the item before it
                items[-1] += " " + line.strip()
    return versions


def inline_html(text: str, muted: str, code: str) -> str:
    """The inline Markdown of an item (bold, code, links and the author at the
    end) as rich text.

    Everything else is escaped.
    """
    escaped = html.escape(text, quote=False)
    escaped = re.sub(
        r"`([^`]+)`",
        rf'<span style="font-family: monospace; color: {code};">\1</span>',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', escaped
    )
    return re.sub(
        r"\s+by (@[\w-]+)$", rf' <span style="color: {muted};">by \1</span>', escaped
    )
