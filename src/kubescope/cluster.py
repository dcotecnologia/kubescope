import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from kubescope.errors import is_auth_error
from kubescope.models import (
    ClusterOverview,
    NodeInfo,
    PodInfo,
    Workload,
    format_age,
    parse_cpu,
    parse_memory,
)


class KubectlError(RuntimeError):
    """Raised when the bundled kubectl command fails."""


def kubectl_executable() -> Path:
    executable_name = "kubectl.exe" if os.name == "nt" else "kubectl"
    if getattr(sys, "frozen", False):
        bundle_directory = Path(sys._MEIPASS)
        return bundle_directory / "kubectl" / executable_name
    project_directory = Path(__file__).resolve().parents[2]
    return project_directory / "vendor" / "kubectl" / executable_name


def _run_kubectl(*arguments: str, context: str | None = None) -> str:
    executable = kubectl_executable()
    if not executable.is_file():
        raise KubectlError(
            "Bundled kubectl is missing. Run `python tools/fetch_kubectl.py` "
            "before starting the app."
        )
    command = [str(executable)]
    if context:
        command.extend(("--context", context))
    command.extend(arguments)
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=45,
        )
    except subprocess.TimeoutExpired as error:
        raise KubectlError("kubectl timed out while contacting the cluster") from error
    except OSError as error:
        raise KubectlError(f"Could not start bundled kubectl: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise KubectlError(detail or f"kubectl exited with {result.returncode}")
    return result.stdout


def _get_json(*arguments: str, context: str) -> dict[str, Any]:
    output = _run_kubectl(*arguments, "-o", "json", context=context)
    payload = json.loads(output)
    if not isinstance(payload, dict):
        raise KubectlError("kubectl returned an unexpected JSON document")
    return payload


def list_contexts() -> tuple[list[str], str | None]:
    output = _run_kubectl("config", "get-contexts", "-o", "name")
    contexts = [line.strip() for line in output.splitlines() if line.strip()]
    active_context = None
    if contexts:
        active_context = _run_kubectl("config", "current-context").strip() or None
    return contexts, active_context


LOGIN_TIMEOUT = 300  # seconds; the sign-in waits for the person in the browser
AWS_TIMEOUT = 30


def _run_command(command: list[str], timeout: float) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        raise KubectlError(f"{command[0]} timed out") from error
    except OSError as error:
        raise KubectlError(f"Could not start {command[0]}: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise KubectlError(detail or f"{command[0]} exited with {result.returncode}")
    return result.stdout


def _aws_profile(context: str) -> tuple[bool, str | None]:
    """Whether the context signs in through the AWS CLI, and with which
    profile.

    Read from the kubeconfig entry; secrets stay redacted because
    `config view` runs without --raw.
    """
    users = _get_json("config", "view", "--minify", context=context).get("users")
    login = ((users or [{}])[0].get("user") or {}).get("exec") or {}
    if Path(login.get("command") or "").stem != "aws":
        return False, None
    arguments = login.get("args") or []
    profile = next(
        (
            arguments[index + 1]
            for index, argument in enumerate(arguments[:-1])
            if argument == "--profile"
        ),
        None,
    )
    for variable in login.get("env") or []:
        if variable.get("name") == "AWS_PROFILE":
            profile = profile or variable.get("value")
    return True, profile


def _profile_arguments(profile: str | None) -> list[str]:
    return ["--profile", profile] if profile else []


def _is_sso_profile(profile: str | None) -> bool:
    """SSO profiles sign in through the browser; the others use access keys."""
    for key in ("sso_session", "sso_start_url"):
        try:
            value = _run_command(
                ["aws", "configure", "get", key, *_profile_arguments(profile)],
                AWS_TIMEOUT,
            )
        except KubectlError:
            continue
        if value.strip():
            return True
    return False


@dataclass(frozen=True, slots=True)
class LoginAction:
    """How to sign in to a context's AWS profile."""

    command: list[str]
    profile: str | None
    interactive: bool  # access keys are typed in a terminal; SSO uses the browser


def login_action(context: str) -> LoginAction | None:
    """The sign-in for a context: "aws sso login" for an AWS SSO profile, and
    "aws configure" in a terminal for an access-key profile.

    Other login tools are not supported and return None.
    """
    uses_aws, profile = _aws_profile(context)
    if not uses_aws:
        return None
    arguments = _profile_arguments(profile)
    if _is_sso_profile(profile):
        return LoginAction(["aws", "sso", "login", *arguments], profile, False)
    return LoginAction(["aws", "configure", *arguments], profile, True)


def check_login(context: str) -> tuple[bool, LoginAction | None]:
    """Whether the context needs a sign-in, and how to do it.

    kubectl catches an expired SSO session. Access keys that were
    rotated or revoked only fail at the cluster, because `aws eks get-
    token` signs locally, so AWS contexts are also checked with STS.
    Other failures (an unreachable cluster, denied access) are not a
    login problem and report as signed in.
    """
    try:
        _run_kubectl("get", "--raw", "/version", context=context)
        uses_aws, profile = _aws_profile(context)
        if uses_aws:
            _run_command(
                ["aws", "sts", "get-caller-identity", *_profile_arguments(profile)],
                AWS_TIMEOUT,
            )
    except (KubectlError, ValueError) as error:
        if not is_auth_error(str(error)):
            return False, None
        try:
            return True, login_action(context)
        except (KubectlError, ValueError):
            return True, None
    return False, None


_TERMINALS = (
    ("x-terminal-emulator", "-e"),
    ("gnome-terminal", "--"),
    ("konsole", "-e"),
    ("xfce4-terminal", "-x"),
    ("xterm", "-e"),
)


def _open_terminal(command: list[str]) -> None:
    """Run a command in a new terminal window and return without waiting."""
    if sys.platform == "win32":
        launcher = ["cmd", "/c", "start", "", "cmd", "/k", *command]
    else:
        launcher = next(
            (
                [path, flag, *command]
                for name, flag in _TERMINALS
                if (path := shutil.which(name))
            ),
            None,
        )
        if launcher is None:
            raise KubectlError(
                "No terminal found. Run this in a terminal: " + " ".join(command)
            )
    try:
        subprocess.Popen(launcher)
    except OSError as error:
        raise KubectlError(f"Could not open a terminal: {error}") from error


def run_login(action: LoginAction) -> None:
    """Start the sign-in.

    SSO opens the browser and is waited for; access keys open a terminal
    where the person types them, so the app never sees them.
    """
    if action.interactive:
        _open_terminal(action.command)
    else:
        _run_command(action.command, LOGIN_TIMEOUT)


def _parse_workload(item: dict[str, Any], now: datetime) -> Workload | None:
    metadata = item.get("metadata") or {}
    spec = item.get("spec") or {}
    status = item.get("status") or {}
    kind = item.get("kind")
    name = metadata.get("name")
    if kind not in {"Deployment", "StatefulSet", "DaemonSet"} or not name:
        return None

    if kind == "DaemonSet":
        desired = status.get("desiredNumberScheduled") or 0
        ready = status.get("numberReady") or 0
    else:
        desired = spec.get("replicas") or 0
        ready = status.get("readyReplicas") or 0

    age = "unknown"
    creation_timestamp = metadata.get("creationTimestamp")
    if creation_timestamp:
        created = datetime.fromisoformat(creation_timestamp.replace("Z", "+00:00"))
        age = format_age((now - created).total_seconds())
    return Workload(
        namespace=metadata.get("namespace") or "default",
        kind=kind,
        name=name,
        ready=ready,
        desired=desired,
        age=age,
    )


def _get_namespaces(context: str) -> list[str]:
    document = _get_json("get", "namespaces", context=context)
    return sorted(
        item["metadata"]["name"]
        for item in document.get("items", [])
        if item.get("metadata", {}).get("name")
    )


def get_workloads(
    context: str,
    namespace: str | None = None,
) -> tuple[list[str], list[Workload]]:
    namespaces = _get_namespaces(context)
    arguments = ["get", "deployments,statefulsets,daemonsets"]
    arguments.extend(("-n", namespace) if namespace else ("-A",))
    workloads_document = _get_json(*arguments, context=context)
    now = datetime.now(UTC)
    workloads = [
        workload
        for item in workloads_document.get("items", [])
        if (workload := _parse_workload(item, now)) is not None
    ]
    workloads.sort(key=lambda row: (row.namespace, row.kind, row.name))
    return namespaces, workloads


def get_resource_details(
    context: str,
    kind: str,
    namespace: str,
    name: str,
) -> dict[str, Any]:
    resource_name = {
        "Deployment": "deployment",
        "StatefulSet": "statefulset",
        "DaemonSet": "daemonset",
        "Pod": "pod",
    }.get(kind)
    if resource_name is None:
        raise KubectlError(f"Unsupported resource kind: {kind}")
    return _get_json("get", resource_name, name, "-n", namespace, context=context)


def _label_selector(resource: dict[str, Any]) -> str:
    selector = (resource.get("spec") or {}).get("selector") or {}
    terms = [
        f"{key}={value}"
        for key, value in sorted((selector.get("matchLabels") or {}).items())
    ]
    for expression in selector.get("matchExpressions") or []:
        key = expression.get("key")
        operator = expression.get("operator")
        values = expression.get("values") or []
        if not key:
            raise KubectlError("Workload selector has an expression without a key")
        if operator in {"In", "NotIn"}:
            if not values:
                raise KubectlError(f"Workload selector {operator} requires values")
            joined_values = ",".join(values)
            terms.append(f"{key} {operator.lower()} ({joined_values})")
        elif operator == "Exists":
            terms.append(key)
        elif operator == "DoesNotExist":
            terms.append(f"!{key}")
        else:
            raise KubectlError(f"Unsupported workload selector operator: {operator}")
    if not terms:
        raise KubectlError("Workload has no label selector for its Pods")
    return ",".join(terms)


def _parse_pod(item: dict[str, Any], now: datetime) -> PodInfo | None:
    metadata = item.get("metadata") or {}
    spec = item.get("spec") or {}
    status = item.get("status") or {}
    name = metadata.get("name")
    if not name:
        return None
    containers = tuple(
        container["name"]
        for container in spec.get("containers") or []
        if container.get("name")
    )
    container_statuses = status.get("containerStatuses") or []
    age = "unknown"
    creation_timestamp = metadata.get("creationTimestamp")
    if creation_timestamp:
        created = datetime.fromisoformat(creation_timestamp.replace("Z", "+00:00"))
        age = format_age((now - created).total_seconds())
    return PodInfo(
        namespace=metadata.get("namespace") or "default",
        name=name,
        phase=status.get("phase") or "Unknown",
        ready=sum(bool(container.get("ready")) for container in container_statuses),
        total=len(containers),
        age=age,
        containers=containers,
        restarts=sum(
            container.get("restartCount") or 0 for container in container_statuses
        ),
        owner=_pod_owner(metadata),
    )


def _pod_owner(metadata: dict[str, Any]) -> tuple[str, str] | None:
    """The workload that controls a Pod; ReplicaSets map back to their
    Deployment."""
    for reference in metadata.get("ownerReferences") or []:
        kind, name = reference.get("kind"), reference.get("name")
        if not kind or not name or not reference.get("controller", True):
            continue
        if kind == "ReplicaSet" and "-" in name:
            return "Deployment", name.rsplit("-", 1)[0]
        return kind, name
    return None


def _pod_metrics(
    context: str, namespace: str | None
) -> dict[tuple[str, str], tuple[float, float]] | None:
    """Live (cores, bytes) per Pod; None when metrics-server is unavailable."""
    scope = f"namespaces/{namespace}/" if namespace else ""
    try:
        document = json.loads(
            _run_kubectl(
                "get",
                "--raw",
                f"/apis/metrics.k8s.io/v1beta1/{scope}pods",
                context=context,
            )
        )
    except (KubectlError, ValueError):
        return None
    usage: dict[tuple[str, str], tuple[float, float]] = {}
    for item in document.get("items", []):
        metadata = item.get("metadata") or {}
        cpu = memory = 0.0
        for container in item.get("containers") or []:
            container_usage = container.get("usage") or {}
            cpu += parse_cpu(container_usage.get("cpu"))
            memory += parse_memory(container_usage.get("memory"))
        usage[(metadata.get("namespace") or "default", metadata.get("name", ""))] = (
            cpu,
            memory,
        )
    return usage


def _pods_with_usage(context: str, namespace: str | None) -> list[PodInfo]:
    arguments = ["get", "pods"]
    arguments.extend(("-n", namespace) if namespace else ("-A",))
    document = _get_json(*arguments, context=context)
    now = datetime.now(UTC)
    pods = [
        pod
        for item in document.get("items", [])
        if (pod := _parse_pod(item, now)) is not None
    ]
    metrics = _pod_metrics(context, namespace)
    if metrics is not None:
        pods = [
            replace(pod, cpu=cpu, memory=memory)
            for pod in pods
            for cpu, memory in [metrics.get((pod.namespace, pod.name), (None, None))]
        ]
    return pods


def get_usage(
    context: str, namespace: str | None = None
) -> dict[tuple[str, str, str], tuple[int, float | None, float | None]]:
    """Restarts, CPU and memory per (namespace, kind, name) workload, from its
    Pods."""
    totals: dict[tuple[str, str, str], tuple[int, float | None, float | None]] = {}
    for pod in _pods_with_usage(context, namespace):
        if pod.owner is None:
            continue
        key = (pod.namespace, *pod.owner)
        restarts, cpu, memory = totals.get(key, (0, None, None))
        if pod.cpu is not None and pod.memory is not None:
            cpu = (cpu or 0.0) + pod.cpu
            memory = (memory or 0.0) + pod.memory
        totals[key] = (restarts + pod.restarts, cpu, memory)
    return totals


def get_workload_pods(context: str, workload: Workload) -> list[PodInfo]:
    resource = get_resource_details(
        context, workload.kind, workload.namespace, workload.name
    )
    selector = _label_selector(resource)
    document = _get_json(
        "get",
        "pods",
        "-n",
        workload.namespace,
        "-l",
        selector,
        context=context,
    )
    now = datetime.now(UTC)
    pods = [
        pod
        for item in document.get("items", [])
        if (pod := _parse_pod(item, now)) is not None
    ]
    return sorted(pods, key=lambda pod: pod.name)


def get_pods(
    context: str,
    namespace: str | None = None,
) -> tuple[list[str], list[PodInfo]]:
    namespaces = _get_namespaces(context)
    pods = _pods_with_usage(context, namespace)
    pods.sort(key=lambda pod: (pod.namespace, pod.name))
    return namespaces, pods


def get_pod_logs(
    context: str,
    namespace: str,
    pod_name: str,
    container: str,
    tail_lines: int = 500,
) -> str:
    tail = min(max(tail_lines, 1), 500)
    return _run_kubectl(
        "logs",
        pod_name,
        "-n",
        namespace,
        "-c",
        container,
        f"--tail={tail}",
        "--timestamps",
        context=context,
    )


_OVERVIEW_SECTIONS = {
    "nodes": "Nodes",
    "pods": "Pods",
    "namespaces": "Namespaces",
    "workloads": "Workloads",
}


def _item_age(item: dict[str, Any], now: datetime) -> str:
    created = (item.get("metadata") or {}).get("creationTimestamp")
    if not created:
        return "unknown"
    started = datetime.fromisoformat(created.replace("Z", "+00:00"))
    return format_age((now - started).total_seconds())


def _node_roles(labels: dict[str, str]) -> str:
    prefix = "node-role.kubernetes.io/"
    roles = sorted(key[len(prefix) :] for key in labels if key.startswith(prefix))
    return ", ".join(roles) or "—"


def _pod_requests(pod: dict[str, Any]) -> tuple[float, float]:
    cpu = memory = 0.0
    for container in (pod.get("spec") or {}).get("containers") or []:
        requests = (container.get("resources") or {}).get("requests") or {}
        cpu += parse_cpu(requests.get("cpu"))
        memory += parse_memory(requests.get("memory"))
    return cpu, memory


def _build_overview(
    results: dict[str, Any], errors: dict[str, str], now: datetime
) -> ClusterOverview:
    usage: dict[str, tuple[float, float]] = {}
    for item in (results.get("metrics") or {}).get("items", []):
        node_usage = item.get("usage") or {}
        usage[(item.get("metadata") or {}).get("name", "")] = (
            parse_cpu(node_usage.get("cpu")),
            parse_memory(node_usage.get("memory")),
        )

    running_on: dict[str, int] = {}
    requests_on: dict[str, tuple[float, float]] = {}
    phases = {"Running": 0, "Pending": 0, "Failed": 0}
    pod_items = (results.get("pods") or {}).get("items", [])
    for pod in pod_items:
        phase = (pod.get("status") or {}).get("phase")
        if phase in phases:
            phases[phase] += 1
        if phase in {"Succeeded", "Failed"}:
            continue
        node_name = (pod.get("spec") or {}).get("nodeName")
        if not node_name:
            continue
        running_on[node_name] = running_on.get(node_name, 0) + 1
        cpu, memory = _pod_requests(pod)
        old_cpu, old_memory = requests_on.get(node_name, (0.0, 0.0))
        requests_on[node_name] = (old_cpu + cpu, old_memory + memory)

    nodes = []
    for item in (results.get("nodes") or {}).get("items", []):
        metadata = item.get("metadata") or {}
        status = item.get("status") or {}
        name = metadata.get("name") or ""
        allocatable = status.get("allocatable") or {}
        ready = any(
            condition.get("type") == "Ready" and condition.get("status") == "True"
            for condition in status.get("conditions") or []
        )
        node_cpu, node_memory = usage.get(name, (None, None))
        requested_cpu, requested_memory = requests_on.get(name, (0.0, 0.0))
        nodes.append(
            NodeInfo(
                name=name,
                ready=ready,
                roles=_node_roles(metadata.get("labels") or {}),
                version=(status.get("nodeInfo") or {}).get("kubeletVersion", ""),
                age=_item_age(item, now),
                cpu_allocatable=parse_cpu(allocatable.get("cpu")),
                memory_allocatable=parse_memory(allocatable.get("memory")),
                pods_allocatable=int(allocatable.get("pods") or 0),
                pods_running=running_on.get(name, 0),
                cpu_requests=requested_cpu,
                memory_requests=requested_memory,
                cpu_usage=node_cpu,
                memory_usage=node_memory,
            )
        )
    nodes.sort(key=lambda node: node.name)

    kinds = {"Deployment": 0, "StatefulSet": 0, "DaemonSet": 0}
    for item in (results.get("workloads") or {}).get("items", []):
        if item.get("kind") in kinds:
            kinds[item["kind"]] += 1
    have_workloads = "workloads" in results
    have_pods = "pods" in results
    return ClusterOverview(
        nodes=tuple(nodes),
        namespaces=(
            len((results["namespaces"]).get("items", []))
            if "namespaces" in results
            else None
        ),
        deployments=kinds["Deployment"] if have_workloads else None,
        statefulsets=kinds["StatefulSet"] if have_workloads else None,
        daemonsets=kinds["DaemonSet"] if have_workloads else None,
        pods_total=len(pod_items) if have_pods else None,
        pods_running=phases["Running"] if have_pods else None,
        pods_pending=phases["Pending"] if have_pods else None,
        pods_failed=phases["Failed"] if have_pods else None,
        metrics_available="metrics" in results,
        warnings=tuple(
            f"{label}: {errors[key]}"
            for key, label in _OVERVIEW_SECTIONS.items()
            if key in errors
        ),
    )


def get_cluster_overview(context: str) -> ClusterOverview:
    """Collect cluster-wide totals; sections the user cannot read become
    warnings."""
    tasks = {
        "nodes": lambda: _get_json("get", "nodes", context=context),
        "pods": lambda: _get_json("get", "pods", "-A", context=context),
        "namespaces": lambda: _get_json("get", "namespaces", context=context),
        "workloads": lambda: _get_json(
            "get", "deployments,statefulsets,daemonsets", "-A", context=context
        ),
        "metrics": lambda: json.loads(
            _run_kubectl(
                "get", "--raw", "/apis/metrics.k8s.io/v1beta1/nodes", context=context
            )
        ),
    }
    results: dict[str, Any] = {}
    errors: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = {name: pool.submit(task) for name, task in tasks.items()}
        for name, future in futures.items():
            try:
                results[name] = future.result()
            except (KubectlError, ValueError) as error:
                errors[name] = str(error)
    if not any(key in results for key in _OVERVIEW_SECTIONS):
        raise KubectlError(next(iter(errors.values()), "No data returned"))
    errors.pop("metrics", None)
    return _build_overview(results, errors, datetime.now(UTC))
