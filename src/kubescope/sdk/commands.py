"""The named commands the window offers and the extensions can call.

No Qt. The window registers what a person can do by hand (choose a
context, open a tab, show the logs of a Pod) under a name; an extension
calls it by name with `Context.invoke` and never reaches into the window
itself.
"""

__all__ = ["CommandError"]


class CommandError(Exception):
    """The command does not exist, or is registered twice."""
