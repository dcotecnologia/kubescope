import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kubectl_gui.models import PodInfo, Workload, format_age


class KubectlError(RuntimeError):
    """Raised when the bundled kubectl command fails."""


def kubectl_executable() -> Path:
    executable_name = "kubectl.exe" if os.name == "nt" else "kubectl"
    if getattr(sys, "frozen", False):
        bundle_directory = Path(getattr(sys, "_MEIPASS"))
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


def get_workloads(
    context: str,
    namespace: str | None = None,
) -> tuple[list[str], list[Workload]]:
    namespaces_document = _get_json("get", "namespaces", context=context)
    namespaces = sorted(
        item["metadata"]["name"]
        for item in namespaces_document.get("items", [])
        if item.get("metadata", {}).get("name")
    )
    arguments = ["get", "deployments,statefulsets,daemonsets"]
    arguments.extend(("-n", namespace) if namespace else ("-A",))
    workloads_document = _get_json(*arguments, context=context)
    now = datetime.now(timezone.utc)
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
    )


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
    now = datetime.now(timezone.utc)
    pods = [
        pod
        for item in document.get("items", [])
        if (pod := _parse_pod(item, now)) is not None
    ]
    return sorted(pods, key=lambda pod: pod.name)


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
