"""Colors for the terminal, only when the terminal can show them, and the bit
of Markdown the assistant writes (bold, code, headings, lists, code blocks)."""

import os
import re
import sys
from typing import TextIO

RESET = "\x1b[0m"
STYLES = {
    "bold": "1",
    "dim": "2",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
}


def enabled(stream: TextIO | None = None) -> bool:
    """Whether the stream is a terminal that takes colors: NO_COLOR and a dumb
    terminal turn them off, FORCE_COLOR turns them on."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    stream = stream or sys.stdout
    if os.environ.get("TERM") == "dumb" or stream is None or not stream.isatty():
        return False
    return sys.platform != "win32" or "WT_SESSION" in os.environ


def paint(text: str, *styles: str, on: bool = True) -> str:
    """The text in the styles (names of STYLES), or as it is when off."""
    if not on or not text or not styles:
        return text
    codes = ";".join(STYLES[style] for style in styles)
    return f"\x1b[{codes}m{text}{RESET}"


_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+)`")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_BULLET = re.compile(r"^(\s*)[-*]\s+(.*)$")


class Markdown:
    """Paints the answer one line at a time, remembering whether a code block
    is open."""

    def __init__(self, on: bool = True) -> None:
        self.on = on
        self.in_code = False

    def line(self, text: str) -> str:
        if not self.on:
            return text
        stripped = text.strip()
        if stripped.startswith("```"):
            if self.in_code:
                self.in_code = False
                return paint("└" + "─" * 20, "dim")
            self.in_code = True
            language = stripped[3:].strip()
            return paint("┌─ " + language if language else "┌" + "─" * 20, "dim")
        if self.in_code:
            return paint("│ ", "dim") + paint(text, "green")
        if heading := _HEADING.match(text):
            return paint(heading.group(2), "bold", "magenta")
        if bullet := _BULLET.match(text):
            text = f"{bullet.group(1)}{paint('•', 'cyan')} {bullet.group(2)}"
        text = _BOLD.sub(lambda found: paint(found.group(1), "bold"), text)
        return _CODE.sub(lambda found: paint(found.group(1), "cyan"), text)
