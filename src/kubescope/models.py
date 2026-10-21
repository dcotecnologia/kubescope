import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

MAX_REPLICA_SQUARES = 5


@dataclass(frozen=True, slots=True)
class Workload:
    namespace: str
    kind: str
    name: str
    ready: int
    desired: int
    age: str
    restarts: int = 0
    cpu: float | None = None  # cores in use, None without metrics-server
    memory: float | None = None  # bytes in use
    state: str | None = None  # Jobs and CronJobs name their own state
    schedule: str | None = None  # CronJobs only

    @property
    def status(self) -> str:
        if self.state:
            return self.state
        if self.desired == 0:
            return "Scaled to zero"
        if self.ready == self.desired:
            return "Healthy"
        if self.ready > 0:
            return "Degraded"
        return "Unavailable"

    @property
    def states(self) -> tuple[str, ...]:
        """One state for each replica, as the colored squares of the list
        show them: running, pending, error or terminated. A Job or CronJob
        has one, for its own state."""
        if self.state:
            own = {
                "Running": "running",
                "Active": "running",
                "Pending": "pending",
                "Failed": "error",
            }
            return (own.get(self.state, "terminated"),)
        if self.desired == 0:
            return ("terminated",)
        shown = min(self.desired, MAX_REPLICA_SQUARES)
        running = min(self.ready, self.desired) * shown // self.desired
        if self.ready and not running:
            running = 1  # some replicas are up, however many there are
        missing = "pending" if self.ready else "error"
        return ("running",) * running + (missing,) * (shown - running)


@dataclass(frozen=True, slots=True)
class ClusterResource:
    namespace: str  # empty for the kinds that belong to the whole cluster
    kind: str
    name: str
    values: tuple[str, ...]  # what the kind shows between its name and its age
    age: str


@dataclass(frozen=True, slots=True)
class ClusterInfo:
    """What the cloud provider says about the cluster itself."""

    status: str
    version: str
    platform_version: str
    created: str
    provider: str
    endpoint: str
    arn: str
    role_arn: str
    oidc_issuer: str
    vpc_id: str = "—"
    subnets: tuple[str, ...] = ()
    security_group: str = "—"
    additional_security_groups: tuple[str, ...] = ()
    ip_family: str = "—"
    service_cidr: str = "—"
    endpoint_access: str = "—"
    public_access_cidrs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PodInfo:
    namespace: str
    name: str
    phase: str
    ready: int
    total: int
    age: str
    containers: tuple[str, ...]
    restarts: int = 0
    cpu: float | None = None
    memory: float | None = None
    owner: tuple[str, str] | None = None  # (kind, name) of the controlling workload
    init_containers: tuple[str, ...] = ()  # run to completion before `containers`
    # one per container: running, pending, error or terminated
    container_states: tuple[str, ...] = ()


def safe_file_name(title: str, suffix: str) -> str:
    """A file name for a tab title: letters, digits, dots and dashes only."""
    stem = re.sub(r"[^\w.-]+", "-", title).strip("-.")
    return f"{stem or 'kubescope'}{suffix}"


def format_age(seconds: float) -> str:
    if seconds < 60:
        return "<1m"
    if seconds < 3600:
        return f"{int(seconds // 60)}m"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h"
    return f"{int(seconds // 86400)}d"


_BINARY_UNITS = {"Ki": 2**10, "Mi": 2**20, "Gi": 2**30, "Ti": 2**40, "Pi": 2**50}
_DECIMAL_UNITS = {"k": 1e3, "K": 1e3, "M": 1e6, "G": 1e9, "T": 1e12, "P": 1e15}
_CPU_UNITS = {"n": 1e-9, "u": 1e-6, "m": 1e-3, "": 1.0}


def _split_quantity(value: str) -> tuple[float, str]:
    text = value.strip()
    index = len(text)
    while index > 0 and text[index - 1].isalpha() and text[index - 1] not in "eE":
        index -= 1
    return float(text[:index]), text[index:]


def parse_cpu(value: str | None) -> float:
    """Convert a Kubernetes CPU quantity ("250m", "2") to cores."""
    if not value:
        return 0.0
    number, unit = _split_quantity(str(value))
    return number * _CPU_UNITS.get(unit, 1.0)


def parse_memory(value: str | None) -> float:
    """Convert a Kubernetes memory quantity ("512Mi", "2G") to bytes."""
    if not value:
        return 0.0
    number, unit = _split_quantity(str(value))
    if unit in _BINARY_UNITS:
        return number * _BINARY_UNITS[unit]
    if unit in _DECIMAL_UNITS:
        return number * _DECIMAL_UNITS[unit]
    if unit == "m":
        return number / 1000
    return number


def format_cores(cores: float) -> str:
    return f"{cores:.1f}"


def format_cpu(cores: float | None) -> str:
    if cores is None:
        return "—"
    if cores < 1:
        return f"{cores * 1000:.0f}m"
    return f"{cores:.2f}"


def format_memory(size: float | None) -> str:
    return "—" if size is None else format_bytes(size)


def format_bytes(size: float) -> str:
    gibibytes = size / 2**30
    if gibibytes >= 1:
        return f"{gibibytes:.1f} GiB"
    return f"{size / 2**20:.0f} MiB"


@dataclass(frozen=True, slots=True)
class NodeInfo:
    name: str
    ready: bool
    roles: str
    version: str
    age: str
    cpu_allocatable: float
    memory_allocatable: float
    pods_allocatable: int
    pods_running: int = 0
    cpu_requests: float = 0.0
    memory_requests: float = 0.0
    cpu_usage: float | None = None
    memory_usage: float | None = None


@dataclass(frozen=True, slots=True)
class ClusterOverview:
    nodes: tuple[NodeInfo, ...] = ()
    namespaces: int | None = None
    deployments: int | None = None
    statefulsets: int | None = None
    daemonsets: int | None = None
    pods_total: int | None = None
    pods_running: int | None = None
    pods_pending: int | None = None
    pods_failed: int | None = None
    metrics_available: bool = False
    warnings: tuple[str, ...] = ()

    @property
    def nodes_ready(self) -> int:
        return sum(1 for node in self.nodes if node.ready)

    @property
    def cpu_allocatable(self) -> float:
        return sum(node.cpu_allocatable for node in self.nodes)

    @property
    def cpu_requests(self) -> float:
        return sum(node.cpu_requests for node in self.nodes)

    @property
    def cpu_usage(self) -> float | None:
        if not self.metrics_available:
            return None
        return sum(node.cpu_usage or 0.0 for node in self.nodes)

    @property
    def memory_allocatable(self) -> float:
        return sum(node.memory_allocatable for node in self.nodes)

    @property
    def memory_requests(self) -> float:
        return sum(node.memory_requests for node in self.nodes)

    @property
    def memory_usage(self) -> float | None:
        if not self.metrics_available:
            return None
        return sum(node.memory_usage or 0.0 for node in self.nodes)

    @property
    def pods_capacity(self) -> int:
        return sum(node.pods_allocatable for node in self.nodes)


_AGE_UNITS = {"m": 60, "h": 3600, "d": 86400}


@dataclass(frozen=True, slots=True)
class KindSummary:
    """How many resources of one kind there are, and how many are healthy (ok),
    still coming up or degraded (warning), or failing (bad).

    The rest are idle on purpose, such as a Deployment scaled to zero.
    """

    total: int = 0
    ok: int = 0
    warning: int = 0
    bad: int = 0


@dataclass(frozen=True, slots=True)
class EventInfo:
    type: str
    source: str
    namespace: str
    involved: str  # "Kind: name"
    message: str
    count: int
    age: str
    last_seen: str


@dataclass(frozen=True, slots=True)
class WorkloadsOverview:
    kinds: dict[str, KindSummary]  # by Kubernetes kind
    events: tuple[EventInfo, ...] = ()
    unreadable: tuple[str, ...] = ()  # sections this user cannot read


# How a workload status counts in a KindSummary; anything else is idle.
OK_STATUSES = frozenset({"Healthy", "Complete", "Running", "Active", "Scheduled"})
WARNING_STATUSES = frozenset({"Degraded", "Pending"})
BAD_STATUSES = frozenset({"Unavailable", "Failed"})

# The list views that show workloads, and the Kubernetes kind each one lists.
WORKLOAD_VIEWS = {
    "deployments": "Deployment",
    "statefulsets": "StatefulSet",
    "daemonsets": "DaemonSet",
    "replicasets": "ReplicaSet",
    "replicationcontrollers": "ReplicationController",
    "jobs": "Job",
    "cronjobs": "CronJob",
}
# The list views that show network resources, and the Kubernetes kind each lists.
NETWORK_VIEWS = {
    "services": "Service",
    "endpointslices": "EndpointSlice",
    "endpoints": "Endpoints",
    "ingresses": "Ingress",
    "ingressclasses": "IngressClass",
    "networkpolicies": "NetworkPolicy",
}
# The list views that show configuration resources, and the kind each lists.
CONFIG_VIEWS = {
    "configmaps": "ConfigMap",
    "secrets": "Secret",
    "resourcequotas": "ResourceQuota",
    "limitranges": "LimitRange",
    "horizontalpodautoscalers": "HorizontalPodAutoscaler",
    "poddisruptionbudgets": "PodDisruptionBudget",
    "priorityclasses": "PriorityClass",
    "runtimeclasses": "RuntimeClass",
    "leases": "Lease",
    "mutatingwebhooks": "MutatingWebhookConfiguration",
    "validatingwebhooks": "ValidatingWebhookConfiguration",
    "nodegroups": "NodeGroup",
    "addons": "Addon",
}
# The views that list Amazon EKS objects: not namespaced, so the namespace and
# the filters do not apply.
EKS_VIEWS = frozenset({"nodegroups"})
# Every view that lists plain resources in the shared table.
RESOURCE_VIEWS = {**NETWORK_VIEWS, **CONFIG_VIEWS}
STATUS_SEVERITY = {
    "Failed": 0,
    "Unavailable": 0,
    "Degraded": 1,
    "Pending": 1,
    "Suspended": 2,
    "Scaled to zero": 2,
    "Running": 3,
    "Active": 3,
    "Scheduled": 3,
    "Complete": 3,
    "Healthy": 3,
}
SORT_COLUMNS = (
    "namespace",
    "kind",
    "name",
    "ready",
    "status",
    "cpu",
    "memory",
    "restarts",
    "age",
)


def age_seconds(age: str) -> float:
    """Inverse of format_age(): "12d" -> seconds, unknown ages sort last."""
    text = age.strip()
    if text == "<1m":
        return 0.0
    if text[:-1].isdigit() and text[-1:] in _AGE_UNITS:
        return int(text[:-1]) * _AGE_UNITS[text[-1]]
    return float("inf")


def workload_sort_key(workload: Workload, column: int) -> tuple:
    """Sort key for a workloads table column; status ranks worst first."""
    by_name = (
        workload.namespace.casefold(),
        workload.kind,
        workload.name.casefold(),
    )
    field = SORT_COLUMNS[column]
    if field == "ready":
        fraction = workload.ready / workload.desired if workload.desired else 1.0
        primary: tuple = (fraction, workload.desired)
    elif field == "status":
        primary = (STATUS_SEVERITY[workload.status],)
    elif field in {"cpu", "memory", "restarts"}:
        value = getattr(workload, field)
        primary = (-1.0 if value is None else value,)
    elif field == "age":
        primary = (age_seconds(workload.age),)
    elif field == "kind":
        primary = (workload.kind,)
    elif field == "name":
        primary = (workload.name.casefold(),)
    else:
        primary = ()
    return (*primary, *by_name)


def resource_sort_key(resource: ClusterResource, column: int) -> tuple:
    """Sort key for a network table column: namespace, kind, name, the values
    of the kind, then age."""
    by_name = (resource.namespace.casefold(), resource.kind, resource.name.casefold())
    if column == len(resource.values) + 3:
        return (age_seconds(resource.age), *by_name)
    texts = (resource.namespace, resource.kind, resource.name, *resource.values)
    return (texts[column].casefold(), *by_name)


def pod_highlight(pod: PodInfo) -> str | None:
    """Classify a Pod as "problem", "young" (under an hour old) or neither."""
    not_ready = pod.phase == "Running" and pod.ready < pod.total
    if pod.restarts > 0 or pod.phase in {"Failed", "Unknown"} or not_ready:
        return "problem"
    if age_seconds(pod.age) < 3600:
        return "young"
    return None


POD_SORT_COLUMNS = (
    "namespace",
    "containers",
    "name",
    "ready",
    "status",
    "cpu",
    "memory",
    "restarts",
    "age",
)
_PHASE_SEVERITY = {"Failed": 0, "Unknown": 1, "Pending": 2, "Running": 3}


def pod_sort_key(pod: PodInfo, column: int) -> tuple:
    """Sort key for a Pods table column; phase ranks worst first."""
    by_name = (pod.namespace.casefold(), pod.name.casefold())
    field = POD_SORT_COLUMNS[column]
    if field == "containers":
        primary: tuple = (pod.total,)
    elif field == "ready":
        primary = (pod.ready / pod.total if pod.total else 1.0, pod.total)
    elif field == "status":
        primary = (_PHASE_SEVERITY.get(pod.phase, 4),)
    elif field in {"cpu", "memory", "restarts"}:
        value = getattr(pod, field)
        primary = (-1.0 if value is None else value,)
    elif field == "age":
        primary = (age_seconds(pod.age),)
    elif field == "name":
        primary = (pod.name.casefold(),)
    else:
        primary = ()
    return (*primary, *by_name)


@dataclass(frozen=True, slots=True)
class DetailRow:
    """One line of the details: a label and its value(s), or a small table."""

    label: str
    values: tuple[str, ...] = ()  # one badge each
    headers: tuple[str, ...] = ()  # a table, when the rows of a list are flat
    table: tuple[tuple[str, ...], ...] = ()


@dataclass(frozen=True, slots=True)
class DetailSection:
    title: str
    rows: tuple[DetailRow, ...]
    level: int = 1  # 2 for a part of the section above, such as one container


_DETAIL_SKIPPED = frozenset({"apiVersion", "kind", "metadata"})
_MAX_VALUE = 160


def _detail_text(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = "" if value is None else str(value)
    return text if len(text) <= _MAX_VALUE else f"{text[:_MAX_VALUE]}..."


def _is_scalar(value: Any) -> bool:
    return not isinstance(value, dict | list)


def _detail_rows(
    value: Any, path: str, sections: list[DetailSection], depth: int = 1
) -> list[DetailRow]:
    """Flatten a document into rows labelled by their path.

    A list of flat mappings becomes a table; a list of larger ones, such
    as the containers, becomes one subsection for each item, added to
    `sections`.
    """
    if isinstance(value, dict):
        rows: list[DetailRow] = []
        for key, item in value.items():
            rows.extend(
                _detail_rows(
                    item, f"{path}.{key}" if path else str(key), sections, depth
                )
            )
        return rows
    if isinstance(value, list):
        if not value:
            return []
        if all(_is_scalar(item) for item in value):
            return [DetailRow(path, tuple(_detail_text(item) for item in value))]
        if all(
            isinstance(item, dict) and all(_is_scalar(v) for v in item.values())
            for item in value
        ):
            headers = tuple(dict.fromkeys(key for item in value for key in item))
            table = tuple(
                tuple(_detail_text(item.get(key)) for key in headers) for item in value
            )
            return [DetailRow(path, headers=headers, table=table)]
        for index, item in enumerate(value):
            name = item.get("name") if isinstance(item, dict) else None
            children: list[DetailSection] = []
            rows = _detail_rows(item, "", children, depth + 1)
            title = f"{path}: {name or index}"
            if rows:
                sections.append(DetailSection(title, tuple(rows), depth + 1))
            sections.extend(
                DetailSection(f"{title} / {child.title}", child.rows, child.level)
                for child in children
            )
        return []
    return [DetailRow(path, (_detail_text(value),))]


def _created_text(timestamp: str, now: float) -> str:
    try:
        created = datetime.fromisoformat(timestamp)
    except ValueError:
        return timestamp
    if created.tzinfo is None:
        return timestamp
    age = format_age(max(now - created.timestamp(), 0))
    return f"{age} ago ({created.astimezone():%b %d, %Y, %H:%M:%S %Z})"


def _properties(document: dict[str, Any], now: float) -> list[DetailRow]:
    metadata = document.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    rows = []
    if document.get("kind"):
        rows.append(DetailRow("Kind", (_detail_text(document["kind"]),)))
    if created := metadata.get("creationTimestamp"):
        rows.append(DetailRow("Created", (_created_text(str(created), now),)))
    for label, key in (("Name", "name"), ("Namespace", "namespace")):
        if metadata.get(key):
            rows.append(DetailRow(label, (_detail_text(metadata[key]),)))
    for label, key in (("Labels", "labels"), ("Annotations", "annotations")):
        pairs = metadata.get(key)
        if isinstance(pairs, dict) and pairs:
            values = tuple(f"{k}={_detail_text(v)}" for k, v in pairs.items())
            rows.append(DetailRow(label, values))
    owners = metadata.get("ownerReferences")
    if isinstance(owners, list) and owners:
        values = tuple(
            f"{owner.get('kind', '')}/{owner.get('name', '')}"
            for owner in owners
            if isinstance(owner, dict)
        )
        rows.append(DetailRow("Controlled by", values))
    return rows


def detail_sections(
    document: dict[str, Any], now: float | None = None
) -> list[DetailSection]:
    """The details of a resource laid out for reading: its properties, then one
    section for each other top-level field (spec, status, data...)."""
    now = time.time() if now is None else now
    sections = []
    if properties := _properties(document, now):
        sections.append(DetailSection("Properties", tuple(properties)))
    for key, value in document.items():
        if key in _DETAIL_SKIPPED:
            continue
        subsections: list[DetailSection] = []
        rows = _detail_rows(
            value, "" if isinstance(value, dict) else str(key), subsections
        )
        if rows:
            sections.append(DetailSection(str(key).capitalize(), tuple(rows)))
        sections.extend(subsections)
    return sections
