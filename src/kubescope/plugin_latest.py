"""The latest version of what Plugins → Installed lists.

An EKS add-on's latest version is the newest one EKS offers for the
cluster's Kubernetes version. A Helm release's is the version of the
chart of the same name at Artifact Hub, the one of an official or
verified publisher first: Helm does not keep where a chart came from, so
this is the best match, not a certainty. Nothing here raises: a version
that cannot be found is a dash. No Qt.
"""

import logging
import re
import time
from functools import partial
from typing import Any

from kubescope import cluster
from kubescope.cluster import ClusterError
from kubescope.utils import artifacthub

logger = logging.getLogger(__name__)

NONE = "—"
HELM_TTL = 600.0  # seconds a chart's latest version is kept
_helm_cache: dict[str, tuple[float, str]] = {}
_CHART_IN_VERSION = re.compile(r"chart (\S+)")


def eks_latest(context: str, addon: str, cluster_version: str) -> str:
    """The newest version of an EKS add-on that the cluster's Kubernetes
    version can run, from `aws eks describe-addon-versions`."""
    try:
        target = cluster._eks_target(context)[2:]
        document = cluster._eks_json(
            "describe-addon-versions",
            ["--addon-name", addon, *target],
            env=cluster._context_env(context),
        )
    except ClusterError as error:
        logger.info("Latest version of %s not read: %s", addon, error)
        return NONE
    versions: list[dict[str, Any]] = [
        entry
        for item in document.get("addons") or []
        for entry in item.get("addonVersions") or []
    ]
    for entry in versions:  # the newest first
        version = entry.get("addonVersion")
        fits = any(
            isinstance(found, dict) and found.get("clusterVersion") == cluster_version
            for found in entry.get("compatibilities") or []
        )
        if isinstance(version, str) and (fits or not cluster_version):
            return version
    return NONE


def _ranked(name: str) -> list[artifacthub.Chart]:
    """The charts of that name at Artifact Hub: an official publisher first,
    then a verified one, then a CNCF project, then the order of relevance."""
    found = artifacthub.search_charts(name, 0, 20).charts
    same = [c for c in found if c.name.casefold() == name.casefold() and c.version]
    return sorted(same, key=lambda c: (not c.official, not c.verified, not c.cncf))


def helm_match(name: str, installed: str = "") -> tuple[str, list[str]]:
    """Where a release's chart most likely comes from: the address of the
    repository and the versions it has, the newest first.

    Charts of one name are not one chart (many are called `prometheus`),
    so the first one that has the installed version among its own is
    taken; with none of them having it, the best publisher's. Raises
    CatalogError.
    """
    candidates = _ranked(name)[:5]
    first: tuple[str, list[str]] | None = None
    for chart in candidates:
        versions = artifacthub.package_versions(chart.repository, chart.name)
        found = (chart.repository_url, versions or [chart.version])
        first = first or found
        if installed and any(_bare(v) == _bare(installed) for v in versions):
            return found
    return first or ("", [])


def helm_latest(chart: str, installed: str = "") -> str:
    """The latest version of the chart of that name at Artifact Hub."""
    key = f"{chart}@{installed}"
    cached = _helm_cache.get(key)
    if cached and time.monotonic() - cached[0] < HELM_TTL:
        return cached[1]
    try:
        _url, versions = helm_match(chart, installed)
    except artifacthub.CatalogError as error:
        logger.info("Latest version of %s not read: %s", chart, error)
        return NONE
    latest = versions[0] if versions else NONE
    _helm_cache[key] = (time.monotonic(), latest)
    return latest


def installed_chart(version_text: str) -> str:
    """The chart version of a Helm row's VERSION ("chart 3.6.2 · app v2")."""
    found = _CHART_IN_VERSION.match(version_text)
    return found.group(1) if found else ""


def _bare(version: str) -> str:
    return version.strip().removeprefix("v")


def update_available(kind: str, installed: str, latest: str) -> bool:
    """Whether the latest version differs from the installed one: for a Helm
    release only its chart version is compared, not the app's."""
    if latest in ("", NONE):
        return False
    if kind == "HelmRelease":
        installed = installed_chart(installed)
    return bool(installed) and installed != NONE and _bare(installed) != _bare(latest)


def _latest_call(context: str, row: Any, cluster_version: str) -> Any:
    """How to find a row's latest version: EKS and Helm have one to find; an
    AKS extension or a GKE add-on does not say."""
    if row.kind == "Addon":
        return partial(eks_latest, context, row.name, cluster_version)
    if row.kind == "HelmRelease":
        return partial(helm_latest, row.name, installed_chart(row.values[1]))
    return lambda: NONE


def latest_versions(context: str, rows: list[Any]) -> dict[tuple[str, str], str]:
    """The latest version of each row, by (kind, name), asked at the same
    time."""
    wanted = [(row.kind, row.name) for row in rows]
    cluster_version = ""
    if any(kind == "Addon" for kind, _name in wanted):
        try:
            cluster_version = cluster.get_cluster_info(context).version
        except ClusterError:
            cluster_version = ""
    calls = [_latest_call(context, row, cluster_version) for row in rows]
    if not calls:
        return {}
    return dict(zip(wanted, cluster._together(*calls), strict=True))
