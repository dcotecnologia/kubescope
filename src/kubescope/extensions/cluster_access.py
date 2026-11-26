"""What the extensions are lent of the cluster, by name (`kubescope.sdk`).

Each method calls the function of the app that does the work, looked up
when the call is made. Nothing else of `kubescope.cluster` or
`kubescope.writes` is reachable from here, so what an extension can do
to a cluster is this list. No Qt.
"""

from collections.abc import Callable
from typing import Any

from kubescope.sdk import WriteModeOff
from kubescope.sdk.models import (
    ClusterEvent,
    ClusterResource,
    PodInfo,
    SearchHit,
    Workload,
)

from kubescope import cloud_addons, cluster, plugin_updates, writes


def is_plugin_update(arguments: list[str]) -> bool:
    """Whether a command is one that Plugins updates with: `aws eks update-
    addon`, `helm --kube-context <context> upgrade` or `az k8s-extension
    update`, and nothing else."""
    head = arguments[:4]
    return (
        head[:3] == ["aws", "eks", "update-addon"]
        or (head[:2] == ["helm", "--kube-context"] and head[3:4] == ["upgrade"])
        or head[:3] == ["az", "k8s-extension", "update"]
    )


def is_plugin_removal(arguments: list[str]) -> bool:
    """Whether a command is one that Plugins removes with: `aws eks delete-
    addon`, `helm --kube-context <context> uninstall` or `az k8s-extension
    delete`, and nothing else."""
    head = arguments[:4]
    return (
        head[:3] == ["aws", "eks", "delete-addon"]
        or (head[:2] == ["helm", "--kube-context"] and head[3:4] == ["uninstall"])
        or head[:3] == ["az", "k8s-extension", "delete"]
    )


class ClusterBridge:
    LOG_WINDOW_BYTES: int = cluster.LOG_WINDOW_BYTES

    def __init__(self, disconnected: Callable[[], set[str]] = set) -> None:
        # the contexts the person disconnected, asked when they are listed
        self._disconnected = disconnected

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

    def list_contexts(self) -> list[str]:
        """The contexts of the kubeconfig that are connected: one the person
        disconnected is left out, as it is from the selector, so that an
        extension does not read it."""
        off = self._disconnected()
        return [name for name in cluster.list_contexts()[0] if name not in off]

    def get_events(
        self, context: str, types: tuple[str, ...] = ("Warning",)
    ) -> list[ClusterEvent]:
        return cluster.get_events(context, types)

    def get_custom_resources(
        self,
        context: str,
        group: str,
        version: str,
        plural: str,
        namespace: str | None = None,
    ) -> dict[str, Any]:
        return cluster.get_custom_resources(context, group, version, plural, namespace)

    def environment(self, context: str) -> dict[str, str]:
        return cluster.context_environment(context)

    def helm_chart_name(self, context: str, namespace: str, release: str) -> str:
        return cluster.helm_chart_name(context, namespace, release)

    def helm_chart_repository(self, context: str, namespace: str, release: str) -> str:
        return cluster.helm_chart_repository(context, namespace, release)

    def eks_target(self, context: str) -> list[str]:
        return cluster._eks_target(context)

    def aks_cluster(self, context: str) -> tuple[str, str]:
        return cloud_addons.aks_cluster(context)

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

    def patch_custom_resource(
        self,
        context: str,
        group: str,
        version: str,
        plural: str,
        namespace: str,
        name: str,
        patch: dict[str, Any],
    ) -> None:
        self._allowed()
        writes.patch_custom_resource(
            context, group, version, plural, namespace, name, patch
        )

    def run_update(self, context: str, arguments: list[str]) -> str:
        self._allowed()
        if not is_plugin_update(arguments):
            raise cluster.ClusterError("That is not a command that updates a plugin")
        return plugin_updates.run_update(context, arguments)

    def run_remove(self, context: str, arguments: list[str]) -> str:
        self._allowed()
        if not is_plugin_removal(arguments):
            raise cluster.ClusterError("That is not a command that removes a plugin")
        return plugin_updates.run_update(context, arguments)
