from dataclasses import dataclass


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
# The list views that show workloads, and the Kubernetes kind each one lists.
WORKLOAD_VIEWS = {
    "deployments": "Deployment",
    "statefulsets": "StatefulSet",
    "jobs": "Job",
    "cronjobs": "CronJob",
}
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
