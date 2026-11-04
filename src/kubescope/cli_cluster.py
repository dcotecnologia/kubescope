"""The cluster commands of the command line: what the window shows (contexts,
Pods, workloads, nodes, events, one object, a log) answered on the terminal,
and, with the write mode on, the actions that change a cluster."""

import argparse
import dataclasses
import json
import sys
from collections.abc import Callable, Sequence
from typing import Any

import yaml

from kubescope import cluster, writes
from kubescope.cluster import ClusterError
from kubescope.settings import Settings
from kubescope.utils import ansi
from kubescope.utils.errors import is_auth_error

CLUSTER_COMMANDS = (
    "contexts",
    "pods",
    "workloads",
    "nodes",
    "events",
    "get",
    "logs",
    "login",
    "auth",
    "delete",
    "evict",
    "scale",
    "restart",
)
WRITE_COMMANDS = ("delete", "evict", "scale", "restart")
DEFAULT_NAMESPACE = "default"
_WORKLOAD_KINDS = ("Deployment", "StatefulSet", "DaemonSet")


def _kinds() -> dict[str, str]:
    """The kinds `get` knows, by their lower case name."""
    names = {
        "Pod",
        "Node",
        "Namespace",
        *cluster._RESOURCES,
        *cluster._LISTED_RESOURCES,
    }
    return {name.lower(): name for name in names}


def _table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    widths = [
        max(len(line[column]) for line in (headers, *rows))
        for column in range(len(headers))
    ]
    return "\n".join(
        "   ".join(
            cell.ljust(width) for cell, width in zip(line, widths, strict=True)
        ).rstrip()
        for line in (headers, *rows)
    )


def _emit(
    output: str,
    document: Any,
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
) -> None:
    if output == "json":
        print(json.dumps(document, ensure_ascii=False, indent=2, default=str))
    elif output == "yaml":
        print(
            yaml.safe_dump(
                json.loads(json.dumps(document, default=str)),
                allow_unicode=True,
                sort_keys=False,
                default_flow_style=False,
            ),
            end="",
        )
    elif rows:
        print(_table(headers, rows))
    else:
        print("No resources found", file=sys.stderr)


def _rows_of(items: Sequence[Any]) -> list[dict[str, Any]]:
    return [dataclasses.asdict(item) for item in items]


def _ask(prompt: str) -> str:
    return input(prompt).strip()


def _confirm(question: str, yes: bool) -> bool:
    if yes:
        return True
    if not sys.stdin.isatty():
        raise ClusterError("Pass --yes to confirm without a terminal")
    return _ask(f"{question} [y/N] ").lower() in ("y", "yes")


def _context(given: str | None) -> str:
    """The context asked for; without one, ask which, on a terminal."""
    if given:
        return given
    contexts, current = cluster.list_contexts()
    if not contexts:
        raise ClusterError("There is no context in the kubeconfig")
    if not sys.stdin.isatty():
        raise ClusterError("Pass --context (the choice is asked on a terminal only)")
    on = ansi.enabled(sys.stdout)
    for number, name in enumerate(contexts, 1):
        mark = "  " + ansi.paint("(current)", "green", on=on) if name == current else ""
        print(f"{ansi.paint(f'{number:>3})', 'cyan', on=on)} {name}{mark}")
    answer = _ask("Context (number or name)" + (f" [{current}]: " if current else ": "))
    if not answer and current:
        return current
    if answer in contexts:
        return answer
    if answer.isdigit() and 1 <= int(answer) <= len(contexts):
        return contexts[int(answer) - 1]
    raise ClusterError(f"There is no context {answer!r}")


def _contexts(output: str) -> int:
    names, current = cluster.list_contexts()
    document = [{"name": name, "current": name == current} for name in names]
    rows = [("*" if name == current else "", name) for name in names]
    _emit(output, document, ("CURRENT", "NAME"), rows)
    return 0


def _pods(context: str, namespace: str | None, output: str) -> int:
    _, pods = cluster.get_pods(context, namespace)
    rows = [
        (
            pod.namespace,
            pod.name,
            f"{pod.ready}/{pod.total}",
            pod.phase,
            str(pod.restarts),
            pod.node,
            pod.age,
        )
        for pod in pods
    ]
    _emit(
        output,
        _rows_of(pods),
        ("NAMESPACE", "NAME", "READY", "STATUS", "RESTARTS", "NODE", "AGE"),
        rows,
    )
    return 0


def _workloads(
    context: str, namespace: str | None, kind: str | None, output: str
) -> int:
    kinds = (kind,) if kind else _WORKLOAD_KINDS
    _, workloads = cluster.get_workloads(context, namespace, kinds)
    rows = [
        (
            item.namespace,
            item.kind,
            item.name,
            f"{item.ready}/{item.desired}",
            item.age,
        )
        for item in workloads
    ]
    _emit(
        output,
        _rows_of(workloads),
        ("NAMESPACE", "KIND", "NAME", "READY", "AGE"),
        rows,
    )
    return 0


def _nodes(context: str, output: str) -> int:
    overview = cluster.get_cluster_overview(context)
    rows = [
        (
            node.name,
            "Ready" if node.ready else "NotReady",
            node.roles,
            node.version,
            f"{node.pods_running}/{node.pods_allocatable}",
            node.age,
        )
        for node in overview.nodes
    ]
    _emit(
        output,
        _rows_of(overview.nodes),
        ("NAME", "STATUS", "ROLES", "VERSION", "PODS", "AGE"),
        rows,
    )
    for warning in overview.warnings:
        print(warning, file=sys.stderr)
    return 0


def _events(context: str, namespace: str | None, output: str) -> int:
    _, events = cluster.get_resources(context, namespace, "Event")
    rows = [(*event.values[:4], event.age) for event in events]
    _emit(
        output,
        _rows_of(events),
        ("TYPE", "REASON", "OBJECT", "MESSAGE", "AGE"),
        rows,
    )
    return 0


def _kind(name: str) -> str:
    kind = _kinds().get(name.lower())
    if kind is None:
        raise ClusterError(f"Unknown kind {name!r}")
    return kind


def _scope(kind: str, namespace: str) -> str:
    """The namespace to ask for: empty for a kind of the whole cluster."""
    cluster_wide = kind in ("Node", "Namespace") or kind in cluster._CLUSTER_WIDE
    return "" if cluster_wide else namespace


def _get(context: str, kind: str, name: str, namespace: str, output: str) -> int:
    kind = _kind(kind)
    document = cluster.get_resource_details(
        context, kind, _scope(kind, namespace), name
    )
    print_as = "yaml" if output == "table" else output
    _emit(print_as, document, (), ())
    return 0


def _logs(
    context: str, pod: str, namespace: str, container: str | None, tail: int
) -> int:
    if container is None:
        document = cluster.get_resource_details(context, "Pod", namespace, pod)
        containers = (document.get("spec") or {}).get("containers") or []
        if not containers:
            raise ClusterError(f"The Pod {pod} has no container")
        container = str(containers[0]["name"])
    print(
        cluster.get_pod_logs(context, namespace, pod, container, tail),
        end="",
    )
    return 0


def _login(context: str) -> int:
    action = cluster.login_action(context)
    if action is None:
        raise ClusterError(
            f"KubeScope does not know how to sign in to {context}; set a sign-in "
            "command for its program in Settings"
        )
    print(f"Signing in to {context} with: {' '.join(action.command)}", file=sys.stderr)
    cluster.run_login_here(action)
    print(f"Signed in to {context}")
    return 0


def _change(description: str, yes: bool, action: Callable[[], None], done: str) -> int:
    if not _confirm(description, yes):
        print("Cancelled", file=sys.stderr)
        return 1
    action()
    print(done)
    return 0


def _delete(context: str, kind: str, name: str, namespace: str, yes: bool) -> int:
    kind = _kind(kind)
    scope = _scope(kind, namespace)

    def action() -> None:
        if kind == "Pod":
            writes.delete_pod(context, scope, name)
        else:
            writes.delete_resource(context, kind, scope, name)

    where = f" in {scope}" if scope else ""
    return _change(
        f"Delete {kind} {name}{where} on {context}?",
        yes,
        action,
        f"{kind} {name} deleted",
    )


def _run_write(namespace: argparse.Namespace, context: str) -> int:
    command, name, scope, yes = (
        namespace.command,
        namespace.name,
        namespace.namespace,
        namespace.yes,
    )
    where = f"{name} in {scope} on {context}"
    if command == "delete":
        return _delete(context, namespace.kind, name, scope, yes)
    if command == "evict":
        return _change(
            f"Evict Pod {where}?",
            yes,
            lambda: writes.evict_pod(context, scope, name),
            f"Pod {name} evicted",
        )
    if command == "scale":
        return _change(
            f"Scale Deployment {where} to {namespace.replicas}?",
            yes,
            lambda: writes.scale_deployment(context, scope, name, namespace.replicas),
            f"Deployment {name} scaled to {namespace.replicas}",
        )
    return _change(
        f"Restart Deployment {where}?",
        yes,
        lambda: writes.restart_deployment(context, scope, name),
        f"Deployment {name} restarting",
    )


def add_commands(commands: Any) -> None:
    """Add the cluster commands to the sub-parsers of the command line."""

    def common(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--context", metavar="NAME", help="the kubeconfig context (asked if absent)"
        )

    def listing(name: str, help_text: str) -> argparse.ArgumentParser:
        parser = commands.add_parser(name, help=help_text)
        common(parser)
        parser.add_argument(
            "-o",
            "--output",
            choices=("table", "json", "yaml"),
            default="table",
            help="how to print it (default: table)",
        )
        return parser

    def namespaced(parser: argparse.ArgumentParser, required: bool) -> None:
        parser.add_argument(
            "-n",
            "--namespace",
            metavar="NAME",
            required=required,
            default=None if required else DEFAULT_NAMESPACE,
            help="the namespace"
            + ("" if required else f" (default: {DEFAULT_NAMESPACE})"),
        )

    def scoped(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-n", "--namespace", metavar="NAME", help="only this namespace"
        )

    commands.add_parser("contexts", help="list the kubeconfig contexts").add_argument(
        "-o", "--output", choices=("table", "json", "yaml"), default="table"
    )
    scoped(listing("pods", "list the Pods"))
    workloads = listing("workloads", "list Deployments, StatefulSets and DaemonSets")
    scoped(workloads)
    workloads.add_argument(
        "--kind", choices=_WORKLOAD_KINDS, help="only this kind of workload"
    )
    listing("nodes", "list the nodes")
    scoped(listing("events", "list the events, the newest first"))
    get = listing("get", "print one object as YAML (or -o json)")
    get.add_argument("kind", help="Pod, Deployment, Service, Node, ConfigMap...")
    get.add_argument("name")
    namespaced(get, required=False)
    logs = commands.add_parser("logs", help="print the end of a Pod's log")
    common(logs)
    logs.add_argument("name", metavar="POD")
    namespaced(logs, required=False)
    logs.add_argument("-c", "--container", help="default: the first container")
    logs.add_argument(
        "--tail", type=int, default=100, help="how many lines (500 at most)"
    )
    login = commands.add_parser(
        "login",
        aliases=["auth"],
        help="sign in to the cloud of a context (SSO, gcloud, az...); also `auth`",
    )
    common(login)
    for name, help_text in (
        ("delete", "delete an object (needs the write mode)"),
        ("evict", "evict a Pod (needs the write mode)"),
        ("scale", "scale a Deployment (needs the write mode)"),
        ("restart", "restart a Deployment (needs the write mode)"),
    ):
        parser = commands.add_parser(name, help=help_text)
        common(parser)
        if name == "delete":
            parser.add_argument("kind", help="Pod, Deployment, Service...")
        parser.add_argument("name")
        namespaced(parser, required=True)
        if name == "scale":
            parser.add_argument("--replicas", type=int, required=True)
        parser.add_argument(
            "-y", "--yes", action="store_true", help="do not ask for confirmation"
        )


def run(namespace: argparse.Namespace) -> int:
    """Run a cluster command; a failure of the cluster is printed, exit 1."""
    try:
        return _dispatch(namespace)
    except (ClusterError, ValueError) as error:
        print(str(error), file=sys.stderr)
        if is_auth_error(str(error)):
            print(
                "It looks like a sign-in is needed: run `kubescope login --context "
                f"{getattr(namespace, 'context', None) or '<name>'}`",
                file=sys.stderr,
            )
        return 1
    except KeyboardInterrupt, EOFError:
        print(file=sys.stderr)
        return 130


def _dispatch(namespace: argparse.Namespace) -> int:
    command = namespace.command
    settings = Settings()
    cluster.configure(settings.kubeconfig_files, settings.sign_in_commands)
    if command == "contexts":
        return _contexts(namespace.output)
    if command in WRITE_COMMANDS and not settings.write_mode:
        raise ClusterError(
            "The write mode is off; turn it on in Settings to change a cluster"
        )
    context = _context(namespace.context)
    if command in ("login", "auth"):
        return _login(context)
    if command in WRITE_COMMANDS:
        return _run_write(namespace, context)
    if command == "pods":
        return _pods(context, namespace.namespace, namespace.output)
    if command == "workloads":
        return _workloads(
            context, namespace.namespace, namespace.kind, namespace.output
        )
    if command == "nodes":
        return _nodes(context, namespace.output)
    if command == "events":
        return _events(context, namespace.namespace, namespace.output)
    if command == "get":
        return _get(
            context,
            namespace.kind,
            namespace.name,
            namespace.namespace,
            namespace.output,
        )
    return _logs(
        context,
        namespace.name,
        namespace.namespace,
        namespace.container,
        namespace.tail,
    )
