"""The keyboard shortcuts of the app and their defaults.

No Qt. A shortcut is the text Qt writes for a key, like `Ctrl+K`, or for
two keys one after the other, like `G, P` (go to Pods); an empty one is
off. The keys follow the ones of Headlamp.
"""

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


def clean(stored: object) -> dict[str, str]:
    """The saved shortcuts with every known action, a missing or damaged one
    falling back to its default."""
    given = stored if isinstance(stored, dict) else {}
    return {
        action: (
            given[action].strip() if isinstance(given.get(action), str) else default
        )
        for action, default in DEFAULTS.items()
    }


def duplicate(shortcuts: dict[str, str]) -> str | None:
    """The first key that two actions share, None when each is its own."""
    seen: set[str] = set()
    for key in shortcuts.values():
        if key and key in seen:
            return key
        seen.add(key)
    return None
