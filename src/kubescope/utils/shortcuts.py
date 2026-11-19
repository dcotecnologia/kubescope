"""The keyboard shortcuts of the app and their defaults.

No Qt. A shortcut is the text Qt writes for a key, like `Ctrl+K`, or for
two keys one after the other, like `G, P` (go to Pods); an empty one is
off. The keys follow the ones of Headlamp.
"""

import re

# id -> default key. The text of each is in the Settings page.
DEFAULTS: dict[str, str] = {
    "refresh": "Ctrl+R",
    "refresh_alt": "F5",
    "search": "/",
    "search_alt": "Ctrl+K",
    "assistant": "Ctrl+G",
    "overview": "G, O",
    "pods": "G, P",
    "deployments": "G, D",
    "services": "G, S",
    "settings": "G, C",
    "filter": "Ctrl+Shift+F",
    "context": "Ctrl+Shift+L",
    "help": "?",
}


# named after the extension, so it has a dot: a typo of an action of the app has none
_ACTION = re.compile(r"[a-z0-9][a-z0-9_-]*(\.[a-z0-9][a-z0-9_-]*)+")
MAX_KEY = 60


def clean(stored: object) -> dict[str, str]:
    """The saved shortcuts with every known action, a missing or damaged one
    falling back to its default.

    What an extension added is kept as it was saved (the action is named
    after the extension), so that its key is still there when it is
    installed again.
    """
    given = stored if isinstance(stored, dict) else {}
    kept = {
        action: (
            given[action].strip() if isinstance(given.get(action), str) else default
        )
        for action, default in DEFAULTS.items()
    }
    kept.update(
        {
            action: key.strip()
            for action, key in given.items()
            if isinstance(action, str)
            and action not in DEFAULTS
            and _ACTION.fullmatch(action)
            and isinstance(key, str)
            and len(key.strip()) <= MAX_KEY
        }
    )
    return kept


def duplicate(shortcuts: dict[str, str]) -> str | None:
    """The first key that two actions share, None when each is its own."""
    seen: set[str] = set()
    for key in shortcuts.values():
        if key and key in seen:
            return key
        seen.add(key)
    return None
