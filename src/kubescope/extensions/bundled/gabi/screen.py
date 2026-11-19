"""What the person sees in the window, as text for the assistant.

It goes with each question, so the assistant answers about the list, the
row and the log in front of the person without being told. It passes
through the same redaction of tokens and keys as every read. No Qt.
"""

from dataclasses import dataclass, field

from kubescope.models import (
    ClusterOverview,
    WorkloadsOverview,
    format_cpu,
    format_memory,
)
from kubescope.utils.diagnostics import redact

ROW_LIMIT = 60  # rows of the list that are described
VIEWER_LIMIT = 6000  # characters of the open Details or Logs
EVENT_ROWS = 40  # events of the Workloads overview that are described
_PAGES = {0: "Cluster overview", 2: "Settings", 4: "Workloads overview"}


@dataclass(frozen=True, slots=True)
class Screen:
    context: str
    page: int  # the index of the page of the window
    view: str = ""  # the list, on the page of the lists
    namespace: str = ""
    search: str = ""
    regex: bool = False
    case: bool = False
    headers: tuple[str, ...] = ()
    rows: tuple[tuple[str, ...], ...] = ()  # the rows the list shows
    selected: tuple[str, ...] = ()
    viewer_title: str = ""
    viewer_text: str = ""
    extra: tuple[str, ...] = field(default=())


def _line(cells: tuple[str, ...]) -> str:
    return " | ".join(cell.strip() for cell in cells)


def describe(screen: Screen) -> str:
    """The screen in words."""
    lines = [f"Context: {screen.context}"]
    if screen.page == 1:
        lines.append(f"Page: the {screen.view} list")
        lines.append(f"Namespace filter: {screen.namespace or 'all namespaces'}")
        if screen.search:
            how = [
                text
                for text, on in (
                    ("regular expression", screen.regex),
                    ("match case", screen.case),
                )
                if on
            ]
            suffix = f" ({', '.join(how)})" if how else ""
            lines.append(f'Search: "{screen.search}"{suffix}')
        if screen.selected:
            lines.append(f"Selected row: {_line(screen.selected)}")
        shown = screen.rows[:ROW_LIMIT]
        lines.append(f"Rows shown: {len(screen.rows)}")
        if screen.headers:
            lines.append(_line(screen.headers))
        lines.extend(_line(row) for row in shown)
        if len(screen.rows) > ROW_LIMIT:
            lines.append(f"[{len(screen.rows) - ROW_LIMIT} more rows left out]")
    elif screen.page == 3:
        lines.append(f"Page: an open tab, {screen.viewer_title}")
        text = screen.viewer_text
        if len(text) > VIEWER_LIMIT:
            text = f"[earlier text left out]\n{text[-VIEWER_LIMIT:]}"
        lines.append(text)
    else:
        lines.append(f"Page: {_PAGES.get(screen.page, 'the window')}")
    lines.extend(screen.extra)
    return redact("\n".join(lines))


def describe_cluster_overview(overview: ClusterOverview | None) -> tuple[str, ...]:
    """The numbers and the nodes of the Cluster overview page."""
    if overview is None:
        return ("The overview has not loaded yet.",)

    def count(value: int | None) -> str:
        return "unknown" if value is None else str(value)

    lines = [
        f"Nodes: {len(overview.nodes)} ({overview.nodes_ready} ready)",
        f"Namespaces: {count(overview.namespaces)}",
        f"Deployments: {count(overview.deployments)}, StatefulSets: "
        f"{count(overview.statefulsets)}, DaemonSets: {count(overview.daemonsets)}",
        f"Pods: {count(overview.pods_total)} total, {count(overview.pods_running)} "
        f"running, {count(overview.pods_pending)} pending, "
        f"{count(overview.pods_failed)} failed",
        f"CPU: {format_cpu(overview.cpu_requests)} requested of "
        f"{format_cpu(overview.cpu_allocatable)} allocatable, usage "
        f"{format_cpu(overview.cpu_usage)}",
        f"Memory: {format_memory(overview.memory_requests)} requested of "
        f"{format_memory(overview.memory_allocatable)} allocatable, usage "
        f"{format_memory(overview.memory_usage)}",
    ]
    lines.extend(
        f"Node {node.name}: {'Ready' if node.ready else 'NotReady'}, {node.roles}, "
        f"{node.version}, pods {node.pods_running}/{node.pods_allocatable}, CPU "
        f"{format_cpu(node.cpu_requests)}/{format_cpu(node.cpu_allocatable)}, memory "
        f"{format_memory(node.memory_requests)}/"
        f"{format_memory(node.memory_allocatable)}"
        for node in overview.nodes
    )
    lines.extend(f"Warning: {warning}" for warning in overview.warnings)
    return tuple(lines)


def describe_workloads_overview(
    overview: WorkloadsOverview | None,
) -> tuple[str, ...]:
    """The health of each kind and the events of the Workloads overview
    page."""
    if overview is None:
        return ("The overview has not loaded yet.",)
    lines = [
        f"{kind}: {summary.total} in all, {summary.ok} healthy, "
        f"{summary.warning} degraded or coming up, {summary.bad} failing"
        for kind, summary in overview.kinds.items()
    ]
    if overview.unreadable:
        lines.append(f"Not readable by this user: {', '.join(overview.unreadable)}")
    lines.append(f"Events, the youngest first ({len(overview.events)}):")
    lines.extend(
        f"{event.type} {event.involved} in {event.namespace or '-'}: {event.message} "
        f"(x{event.count}, age {event.age}, last seen {event.last_seen})"
        for event in overview.events[:EVENT_ROWS]
    )
    if len(overview.events) > EVENT_ROWS:
        lines.append(f"[{len(overview.events) - EVENT_ROWS} more events left out]")
    return tuple(lines)
