"""The coding assistants of the system the person can ask about the cluster."""

from kubescope.extensions.bundled.gabi.claude import CLAUDE
from kubescope.extensions.bundled.gabi.codex import CODEX
from kubescope.extensions.bundled.gabi.runner import Assistant, is_available

ASSISTANTS = {assistant.key: assistant for assistant in (CLAUDE, CODEX)}


def installed() -> list[Assistant]:
    """The assistants whose program the system has."""
    return [assistant for assistant in ASSISTANTS.values() if is_available(assistant)]
