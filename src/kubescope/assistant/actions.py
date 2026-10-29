"""What the assistant may ask the app to do, and how it asks.

The assistant never runs anything. When it wants something done it
writes a block of JSON in its answer, and the app checks it against this
catalog, which is a closed list of what the app itself can do, with the
same code and the same permissions as its buttons. A block that names
another action, misses a field, has one more or a value of the wrong
kind is dropped. What each kind of action needs from the person is the
app's to decide: a `write` is never run without a confirmation and the
write mode, a `fetch` sends what it reads to the assistant. No Qt.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Any, Literal

from kubescope.models import EKS_VIEWS, RESOURCE_VIEWS, WORKLOAD_VIEWS
from kubescope.writes import _RESOURCE_OF_KIND, MAX_REPLICAS

FENCE = "kubescope-action"
_BLOCK = re.compile(rf"```{FENCE}[ \t]*\n(.*?)```[ \t]*\n?", re.DOTALL)

Kind = Literal["navigate", "fetch", "write"]
VIEWS = tuple(sorted({"pods", *WORKLOAD_VIEWS, *RESOURCE_VIEWS, *EKS_VIEWS}))
KINDS = tuple(sorted(_RESOURCE_OF_KIND))


@dataclass(frozen=True, slots=True)
class Param:
    name: str
    type: type  # str, int, bool or dict
    summary: str
    required: bool = True
    empty: bool = False  # a string may be empty (no namespace, no search)
    choices: tuple[str, ...] = ()
    low: int = 0  # the range of an int
    high: int = MAX_REPLICAS


@dataclass(frozen=True, slots=True)
class Action:
    name: str
    kind: Kind
    summary: str
    params: tuple[Param, ...] = ()


_NAMESPACE = Param(
    "namespace", str, "its namespace; empty when it has none", empty=True
)
_NAME = Param("name", str, "its name")
_KIND = Param("kind", str, "the Kubernetes kind", choices=KINDS)

ACTIONS = (
    Action(
        "open_view",
        "navigate",
        "show a list in the app",
        (Param("view", str, "the list", choices=VIEWS),),
    ),
    Action(
        "set_namespace",
        "navigate",
        "choose the namespace of the lists; empty is all namespaces",
        (Param("namespace", str, "the namespace", empty=True),),
    ),
    Action(
        "search",
        "navigate",
        "type in the search bar of the list, which looks through every column",
        (
            Param("text", str, "what to look for; empty clears it", empty=True),
            Param("regex", bool, "read it as a regular expression", required=False),
            Param("case", bool, "match the case", required=False),
        ),
    ),
    Action(
        "switch_context",
        "navigate",
        "change the cluster of the kubeconfig",
        (Param("context", str, "the name of the context"),),
    ),
    Action(
        "open_page",
        "navigate",
        "go to a page of the window that is not a list",
        (
            Param(
                "page",
                str,
                "the page",
                choices=("overview", "workloads_overview", "settings"),
            ),
        ),
    ),
    Action(
        "switch_tab",
        "navigate",
        "show a Details or Logs tab that is already open, found by its title",
        (Param("title", str, "a part of the title of the tab"),),
    ),
    Action(
        "show_logs",
        "navigate",
        "open the logs of a Pod for the person, in a tab",
        (
            Param("namespace", str, "the namespace of the Pod"),
            Param("pod", str, "the name of the Pod"),
            Param("container", str, "the container", required=False, empty=True),
        ),
    ),
    Action("refresh", "navigate", "read the list again"),
    Action(
        "show_details",
        "navigate",
        "open the details of a resource for the person",
        (_KIND, _NAMESPACE, _NAME),
    ),
    Action(
        "get_details",
        "fetch",
        "read the document of a resource and get it back as the next message",
        (_KIND, _NAMESPACE, _NAME),
    ),
    Action(
        "list",
        "fetch",
        "read a list of the cluster, as the app shows it, and get it back as the "
        "next message",
        (
            Param("view", str, "the list", choices=VIEWS),
            Param("namespace", str, "its namespace; empty is all", empty=True),
        ),
    ),
    Action(
        "get_events",
        "fetch",
        "read the events of a namespace, the youngest first, and get them back as "
        "the next message",
        (
            Param("namespace", str, "the namespace; empty is all", empty=True),
            Param(
                "name",
                str,
                "keep the events whose object has this in its name",
                required=False,
                empty=True,
            ),
        ),
    ),
    Action(
        "get_logs",
        "fetch",
        "read the last lines of a log and get them back as the next message",
        (
            Param("namespace", str, "the namespace of the Pod"),
            Param("pod", str, "the name of the Pod"),
            Param("container", str, "the container", required=False, empty=True),
            Param("lines", int, "how many lines", required=False, low=1, high=2000),
        ),
    ),
    Action(
        "scale",
        "write",
        "set the replicas of a Deployment",
        (
            Param("namespace", str, "its namespace"),
            _NAME,
            Param("replicas", int, "how many"),
        ),
    ),
    Action(
        "restart",
        "write",
        "restart the Pods of a Deployment, one by one",
        (Param("namespace", str, "its namespace"), _NAME),
    ),
    Action(
        "evict_pod",
        "write",
        "evict a Pod, respecting its disruption budget",
        (Param("namespace", str, "its namespace"), _NAME),
    ),
    Action("delete", "write", "delete a resource", (_KIND, _NAMESPACE, _NAME)),
    Action(
        "replace",
        "write",
        "replace a resource with the whole document, as kubectl replace does",
        (
            _KIND,
            _NAMESPACE,
            _NAME,
            Param("document", dict, "the whole new document of the resource"),
        ),
    ),
)
BY_NAME = {action.name: action for action in ACTIONS}


@dataclass(frozen=True, slots=True)
class Request:
    """An action the assistant asked for, checked."""

    action: Action
    args: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Invalid:
    """A block that was dropped, and why."""

    reason: str


def _check(param: Param, value: Any) -> str:
    """Why the value does not fit the field, or nothing when it does."""
    if param.type is int:
        if isinstance(value, bool) or not isinstance(value, int):
            return f"{param.name} must be a whole number"
        if not param.low <= value <= param.high:
            return f"{param.name} must be between {param.low} and {param.high}"
    elif not isinstance(value, param.type):
        return f"{param.name} must be a {param.type.__name__}"
    elif param.type is str:
        if not value.strip() and not param.empty:
            return f"{param.name} is empty"
        if param.choices and value not in param.choices:
            return f"{param.name} is not one of the known ones: {value}"
    return ""


def _parse_block(text: str) -> Request | Invalid:
    try:
        document = json.loads(text)
    except ValueError:
        return Invalid("the block is not JSON")
    if not isinstance(document, dict):
        return Invalid("the block is not an object")
    action = BY_NAME.get(str(document.get("action")))
    if action is None:
        return Invalid(f"there is no action {document.get('action')}")
    args = {key: value for key, value in document.items() if key != "action"}
    known = {param.name for param in action.params}
    if unknown := sorted(set(args) - known):
        return Invalid(f"{action.name} has no {', '.join(unknown)}")
    for param in action.params:
        if param.name not in args:
            if param.required:
                return Invalid(f"{action.name} needs {param.name}")
            continue
        if problem := _check(param, args[param.name]):
            return Invalid(f"{action.name}: {problem}")
    return Request(action, args)


def parse(text: str) -> list[Request | Invalid]:
    """The actions an answer asks for, in order; a block that does not fit the
    catalog comes back as `Invalid`."""
    return [_parse_block(block) for block in _BLOCK.findall(text)]


def strip(text: str) -> str:
    """The answer without its action blocks, to read."""
    return _BLOCK.sub("", text).strip()


def instructions(write_mode: bool = True) -> str:
    """What the assistant is told about the actions; with the write mode off,
    the ones that change a cluster are not among them, as if they did not
    exist."""
    lines = [
        "The client can act for the person. To ask for an action, put a fenced "
        f"block in your answer, tagged {FENCE}, with one JSON object and the name "
        'of the action in "action". Ask for one action per block. Say in plain '
        "words what it does and why before you ask. You cannot see the result of "
        "a navigate or write action, and the client asks the person before it "
        "changes anything, so never say it is done. A fetch action answers in the "
        "next message. Use only these actions and their fields:",
    ]
    for action in ACTIONS:
        if action.kind == "write" and not write_mode:
            continue
        fields = ", ".join(
            f"{param.name}{'' if param.required else '?'}: {param.type.__name__}"
            + (f" ({'|'.join(param.choices)})" if param.choices else "")
            for param in action.params
        )
        lines.append(f"- {action.name} [{action.kind}] {{{fields}}}: {action.summary}")
    return "\n".join(lines)


def describe(request: Request) -> str:
    """What the action does, in a line, for the person to confirm."""
    fields = ", ".join(
        f"{key}={json.dumps(value) if isinstance(value, dict) else value}"
        for key, value in request.args.items()
    )
    return f"{request.action.name}({fields})"
