"""The events the app tells the extensions about.

No Qt. An extension subscribes with `on` and gets the payload as keyword
arguments. The app never lets a handler that raises stop the others.
"""

from collections.abc import Callable
from typing import Protocol

CONTEXT_CHANGED = "context_changed"  # context: str | None
THEME_CHANGED = "theme_changed"
LANGUAGE_CHANGED = "language_changed"
SHUTDOWN = "shutdown"

EVENTS = (CONTEXT_CHANGED, THEME_CHANGED, LANGUAGE_CHANGED, SHUTDOWN)


class Events(Protocol):
    def on(self, event: str, handler: Callable[..., None]) -> Callable[[], None]:
        """Call `handler` on every `event`; returns the function that stops
        it."""
        ...
