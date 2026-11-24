"""What the Plugins list as installed on the clusters of Azure and Google
Cloud.

An AKS cluster lists its managed extensions (`az k8s-extension`), which
have a version and can be updated; a GKE cluster lists its add-ons
(`addonsConfig`), which are only on or off. The cluster is found the way
each cloud names it: AKS from the address of its API server, GKE from
the name of the context (`gke_<project>_<location>_<cluster>`). Every
call reads, except `aks_update_arguments`, which only builds the command
the update dialog shows and runs. No Qt.
"""

import json
import logging
import re
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

from kubescope.sdk.models import ClusterResource

from kubescope import cluster
from kubescope.cluster import ClusterError

logger = logging.getLogger(__name__)

AKS_KIND = "AksExtension"
GKE_KIND = "GkeAddon"
TIMEOUT = 60  # seconds the az and gcloud programs may take
NO_VALUE = "—"
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}")
_VERSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,99}")
GKE_CONTEXT = re.compile(r"gke_([^_]+)_([^_]+)_([^_]+)")


def is_aks_context(context: str) -> bool:
    """Whether the context signs in with kubelogin, as the AKS ones do."""
    command = str(cluster._sign_in_program(context).get("command") or "")
    return command.rsplit("/", 1)[-1].removesuffix(".exe") == "kubelogin"


def gke_target(context: str) -> tuple[str, str, str]:
    """The project, the location and the name of a GKE cluster, from its
    context."""
    found = GKE_CONTEXT.fullmatch(context)
    if not found:
        raise ClusterError("This list is only available for GKE, AKS and EKS contexts")
    return found.group(1), found.group(2), found.group(3)


def _server_host(context: str) -> str:
    document = cluster._kubeconfig()
    name = (cluster._named(document.get("contexts"), context).get("context") or {}).get(
        "cluster"
    )
    server = (cluster._named(document.get("clusters"), name).get("cluster") or {}).get(
        "server"
    )
    return (urlparse(str(server or "")).hostname or "").lower()


def _run_json(command: list[str], context: str) -> Any:
    output = cluster._run_command(command, TIMEOUT, cluster._context_env(context))
    try:
        return json.loads(output or "null")
    except ValueError as error:
        raise ClusterError(
            f"{command[0]} answered with something unexpected"
        ) from error


def aks_cluster(context: str) -> tuple[str, str]:
    """The name and the resource group of the AKS cluster of a context, found
    by the address of its API server among the clusters `az aks list` shows."""
    host = _server_host(context)
    if not host:
        raise ClusterError("The kubeconfig does not say where this cluster is")
    clusters = _run_json(["az", "aks", "list", "--output", "json"], context)
    for item in clusters if isinstance(clusters, list) else []:
        addresses = {
            str(item.get(key) or "").lower()
            for key in ("fqdn", "privateFqdn", "azurePortalFqdn")
        }
        if host in addresses and item.get("name") and item.get("resourceGroup"):
            return str(item["name"]), str(item["resourceGroup"])
    raise ClusterError("This cluster is not among the AKS clusters of the account")


def _extension_target(name: str, group: str) -> list[str]:
    if not _NAME.fullmatch(name) or not _NAME.fullmatch(group):
        raise ClusterError("That is not the name of a cluster")
    return [
        "--cluster-name",
        name,
        "--resource-group",
        group,
        "--cluster-type",
        "managedClusters",
    ]


def aks_extensions(context: str, now: datetime) -> list[ClusterResource]:
    """The managed extensions of the AKS cluster of a context."""
    name, group = aks_cluster(context)
    items = _run_json(
        ["az", "k8s-extension", "list", *_extension_target(name, group), "-o", "json"],
        context,
    )
    rows = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict) or not item.get("name"):
            continue
        rows.append(
            ClusterResource(
                namespace="",
                kind=AKS_KIND,
                name=str(item["name"]),
                values=(
                    str(item.get("provisioningState") or NO_VALUE),
                    str(item.get("version") or NO_VALUE),
                    "AKS",
                    _age((item.get("systemData") or {}).get("lastModifiedAt"), now),
                ),
                age=_age(
                    ((item.get("systemData") or {}).get("createdAt")),
                    now,
                ),
            )
        )
    return rows


def aks_extension_details(context: str, name: str) -> dict[str, Any]:
    cluster_name, group = aks_cluster(context)
    if not _NAME.fullmatch(name):
        raise ClusterError("That is not the name of an extension")
    document = _run_json(
        [
            "az",
            "k8s-extension",
            "show",
            "--name",
            name,
            *_extension_target(cluster_name, group),
            "-o",
            "json",
        ],
        context,
    )
    return document if isinstance(document, dict) else {}


def aks_update_arguments(
    cluster_name: str, group: str, extension: str, version: str
) -> list[str]:
    """The `az k8s-extension update` command that moves an extension to a
    version; a version that is asked for turns the automatic minor upgrades
    off, as the command requires."""
    if not _NAME.fullmatch(extension):
        raise ClusterError("That is not the name of an extension")
    if not _VERSION.fullmatch(version):
        raise ClusterError("Give the version to update to")
    return [
        "az",
        "k8s-extension",
        "update",
        "--name",
        extension,
        *_extension_target(cluster_name, group),
        "--version",
        version,
        "--auto-upgrade-minor-version",
        "false",
        "--yes",
        "--output",
        "json",
    ]


def _gke_description(context: str) -> dict[str, Any]:
    project, location, name = gke_target(context)
    document = _run_json(
        [
            "gcloud",
            "container",
            "clusters",
            "describe",
            name,
            "--location",
            location,
            "--project",
            project,
            "--format",
            "json",
        ],
        context,
    )
    return document if isinstance(document, dict) else {}


def gke_addons(context: str) -> list[ClusterResource]:
    """The add-ons of the GKE cluster of a context, each on or off."""
    config = _gke_description(context).get("addonsConfig") or {}
    return [
        ClusterResource(
            namespace="",
            kind=GKE_KIND,
            name=name,
            values=(_state(value), NO_VALUE, "GKE", NO_VALUE),
            age=NO_VALUE,
        )
        for name, value in sorted(config.items())
        if isinstance(value, dict)
    ]


def _state(value: dict[str, Any]) -> str:
    return "Disabled" if value.get("disabled") else "Enabled"


def gke_addon_details(context: str, name: str) -> dict[str, Any]:
    value = (_gke_description(context).get("addonsConfig") or {}).get(name)
    if not isinstance(value, dict):
        raise ClusterError(f"The add-on {name} was not found")
    return {name: value}


def _age(created: object, now: datetime) -> str:
    try:
        started = datetime.fromisoformat(str(created).replace("Z", "+00:00"))
    except ValueError:
        return NO_VALUE
    if started.tzinfo is None:
        started = started.replace(tzinfo=UTC)
    return cluster.format_age((now - started).total_seconds())
