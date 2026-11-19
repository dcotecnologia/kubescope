"""What the extensions are lent of the cluster, by name (`kubescope.sdk`).

Each method calls the function of the app that does the work, looked up
when the call is made. Nothing else of `kubescope.cluster` or
`kubescope.writes` is reachable from here, so what an extension can do
to a cluster is this list. No Qt.
"""

from collections.abc import Callable
from typing import Any

from kubescope.sdk.models import ClusterResource, PodInfo, SearchHit, Workload

from kubescope import cluster, writes
from kubescope.sdk import WriteModeOff


class ClusterBridge:
    LOG_WINDOW_BYTES: int = cluster.LOG_WINDOW_BYTES

    def get_workloads(
        self,
        context: str,
        namespace: str | None = None,
        kinds: tuple[str, ...] | None = None,
    ) -> tuple[list[str], list[Workload]]:
        if kinds is None:
            return cluster.get_workloads(context, namespace)
        return cluster.get_workloads(context, namespace, kinds)

    def get_pods(
        self, context: str, namespace: str | None = None
    ) -> tuple[list[str], list[PodInfo]]:
        return cluster.get_pods(context, namespace)

    def get_pod_logs(
        self,
        context: str,
        namespace: str,
        pod_name: str,
        container: str,
        tail_lines: int = 500,
        since_time: str | None = None,
        since_seconds: int = 0,
        limit_bytes: int = 0,
    ) -> str:
        return cluster.get_pod_logs(
            context,
            namespace,
            pod_name,
            container,
            tail_lines,
            since_time,
            since_seconds,
            limit_bytes,
        )

    def get_pod_container_usage(
        self, context: str, namespace: str, pod_name: str
    ) -> dict[str, tuple[float, float]] | None:
        return cluster.get_pod_container_usage(context, namespace, pod_name)

    def get_usage(
        self, context: str, namespace: str | None = None
    ) -> dict[tuple[str, str, str], tuple[int, float | None, float | None]]:
        return cluster.get_usage(context, namespace)

    def get_resources(
        self, context: str, namespace: str | None, kind: str
    ) -> tuple[list[str], list[ClusterResource]]:
        return cluster.get_resources(context, namespace, kind)

    def get_resource_details(
        self, context: str, kind: str, namespace: str, name: str
    ) -> dict[str, Any]:
        return cluster.get_resource_details(context, kind, namespace, name)

    def search_resources(self, context: str) -> list[SearchHit]:
        return cluster.search_resources(context)

    def describe_kube(self) -> str:
        return cluster.describe_kube()


class WritesBridge:
    """The changes to a cluster, which refuse unless the write mode is on."""

    def __init__(self, write_mode: Callable[[], bool]) -> None:
        self._write_mode = write_mode

    def _allowed(self) -> None:
        if not self._write_mode():
            raise WriteModeOff("turn on the write mode to change the cluster")

    def scale_deployment(
        self, context: str, namespace: str, name: str, replicas: int
    ) -> None:
        self._allowed()
        writes.scale_deployment(context, namespace, name, replicas)

    def restart_deployment(self, context: str, namespace: str, name: str) -> None:
        self._allowed()
        writes.restart_deployment(context, namespace, name)

    def evict_pod(self, context: str, namespace: str, name: str) -> None:
        self._allowed()
        writes.evict_pod(context, namespace, name)

    def delete_pod(self, context: str, namespace: str, name: str) -> None:
        self._allowed()
        writes.delete_pod(context, namespace, name)

    def delete_resource(
        self, context: str, kind: str, namespace: str, name: str
    ) -> None:
        self._allowed()
        writes.delete_resource(context, kind, namespace, name)

    def replace_resource(
        self,
        context: str,
        kind: str,
        namespace: str,
        name: str,
        document: dict[str, Any],
    ) -> None:
        self._allowed()
        writes.replace_resource(context, kind, namespace, name, document)
