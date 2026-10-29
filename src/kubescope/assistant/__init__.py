"""The coding assistants of the system the person can ask about the cluster."""

from kubescope.assistant.claude import CLAUDE
from kubescope.assistant.runner import Assistant, is_available

ASSISTANTS = {assistant.key: assistant for assistant in (CLAUDE,)}


def installed() -> list[Assistant]:
    """The assistants whose program the system has."""
    return [assistant for assistant in ASSISTANTS.values() if is_available(assistant)]
