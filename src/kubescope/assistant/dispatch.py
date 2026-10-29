"""Which function of the write mode runs each change the assistant may ask for.

The person confirmed it on a card of the chat first; the functions are
the ones the buttons of the write mode use, so the same limits hold. No
Qt.
"""

from collections.abc import Callable
from typing import Any

from kubescope import writes
from kubescope.assistant.actions import Request


def write_call(
    request: Request, context: str
) -> tuple[Callable[..., None], tuple[Any, ...]]:
    """The function and the arguments that run a `write` request."""
    args = request.args
    name = request.action.name
    if name == "scale":
        return writes.scale_deployment, (
            context,
            args["namespace"],
            args["name"],
            args["replicas"],
        )
    if name == "restart":
        return writes.restart_deployment, (context, args["namespace"], args["name"])
    if name == "evict_pod":
        return writes.evict_pod, (context, args["namespace"], args["name"])
    if name == "delete":
        if args["kind"] == "Pod":
            return writes.delete_pod, (context, args["namespace"], args["name"])
        return writes.delete_resource, (
            context,
            args["kind"],
            args["namespace"],
            args["name"],
        )
    if name == "replace":
        return writes.replace_resource, (
            context,
            args["kind"],
            args["namespace"],
            args["name"],
            args["document"],
        )
    raise ValueError(f"{name} does not change the cluster")
