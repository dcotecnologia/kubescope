"""Update what the Plugins list as installed, with the program that put it
there.

An Amazon EKS add-on is updated with `aws eks update-addon`, a Helm
release with `helm upgrade`. Each takes its own inputs, so each has its
own function that builds the command from them, and `run_update` runs
it. Nothing here runs unless the person turned on the write mode and
confirmed the dialog: the window guards that, as for the other writes.
No Qt.
"""

import logging
import re
import shlex
import subprocess
from typing import Any

from kubescope import cluster
from kubescope.cluster import ClusterError
from kubescope.utils.flatpak import in_flatpak
from kubescope.utils.programs import find_program
from kubescope.writes import _with_kubeconfig

logger = logging.getLogger(__name__)

UPDATE_TIMEOUT = 600  # seconds a helm upgrade may wait for the release
CONFLICTS = ("NONE", "OVERWRITE", "PRESERVE")  # what EKS does with changed fields
_VERSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,99}")
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/:-]{0,199}")
_REPO = re.compile(r"https://[^\s]{1,300}")
_PATH = re.compile(r"[^\s\0-\x1f]{1,500}")


def eks_addon_versions(context: str, addon: str) -> list[str]:
    """The versions EKS offers for an add-on, as `aws eks describe-addon-
    versions` lists them, the newest first.

    Reads only.
    """
    if not _NAME.fullmatch(addon):
        raise ClusterError("That is not the name of an add-on")
    # the region and the profile of the cluster, without the cluster's own name
    scope = cluster._eks_target(context)[2:]
    document = cluster._eks_json(
        "describe-addon-versions",
        ["--addon-name", addon, *scope],
        env=cluster._context_env(context),
    )
    versions: list[str] = []
    for item in document.get("addons") or []:
        for entry in item.get("addonVersions") or []:
            version = entry.get("addonVersion")
            if isinstance(version, str) and version not in versions:
                versions.append(version)
    return versions


def eks_update_arguments(
    context: str, addon: str, version: str, conflicts: str = "NONE"
) -> list[str]:
    """The AWS CLI command that moves an add-on of the context's EKS cluster to
    a version."""
    if not _NAME.fullmatch(addon):
        raise ClusterError("That is not the name of an add-on")
    if not _VERSION.fullmatch(version):
        raise ClusterError("Give the version to update to")
    if conflicts not in CONFLICTS:
        raise ClusterError("Choose what to do with the fields that differ")
    return [
        "aws",
        "eks",
        "update-addon",
        *cluster._eks_target(context),
        "--addon-name",
        addon,
        "--addon-version",
        version,
        "--resolve-conflicts",
        conflicts,
        "--output",
        "json",
    ]


def helm_upgrade_arguments(
    context: str,
    namespace: str,
    release: str,
    chart: str,
    version: str = "",
    repository: str = "",
    reuse_values: bool = True,
    values_file: str = "",
) -> list[str]:
    """The `helm upgrade` command for a release.

    `chart` is a reference as Helm takes it (`repo/name`, `oci://...`, a
    path), or the bare name of a chart when `repository` gives the
    address to read it from. By default the values the release already
    has are kept.
    """
    if not _NAME.fullmatch(release) or not _NAME.fullmatch(namespace):
        raise ClusterError("That is not the name of a release")
    if not _NAME.fullmatch(chart):
        raise ClusterError("Give the chart to upgrade the release with")
    if version and not _VERSION.fullmatch(version):
        raise ClusterError("That is not a chart version")
    if repository and not _REPO.fullmatch(repository):
        raise ClusterError("The repository must be an https address")
    if values_file and not _PATH.fullmatch(values_file):
        raise ClusterError("That is not the path of a values file")
    return [
        "helm",
        "--kube-context",
        context,
        "upgrade",
        release,
        chart,
        "--namespace",
        namespace,
        *(["--repo", repository] if repository else []),
        *(["--version", version] if version else []),
        "--reuse-values" if reuse_values else "--reset-values",
        *(["--values", values_file] if values_file else []),
        "--wait",
        "--timeout",
        "5m",
    ]


def program_missing(program: str) -> bool:
    """Whether the program that runs an update is not installed.

    In a Flatpak the programs are the host's, which the sandbox cannot
    look at, so it is taken as there.
    """
    return not in_flatpak() and find_program(program) is None


def commands(arguments: list[str]) -> str:
    """The command as the person would type it, to show before it runs."""
    return shlex.join(arguments)


def run_update(context: str, arguments: list[str]) -> str:
    """Run an update command with the keys of the context's account and the
    kubeconfigs the app reads; returns what the program printed."""
    environment, program = cluster.context_environment(context), arguments
    if arguments[0] == "helm":
        program, extra = _with_kubeconfig(arguments)
        environment = {**environment, **extra}
    logger.info("Updating with %s %s", arguments[0], arguments[1])
    try:
        result = _run(program, environment)
    except subprocess.TimeoutExpired as error:
        raise ClusterError(f"{arguments[0]} timed out") from error
    except OSError as error:
        raise ClusterError(f"Could not start {arguments[0]}: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ClusterError(detail or f"{arguments[0]} exited with {result.returncode}")
    return (result.stdout or "").strip()


def _run(program: list[str], environment: dict[str, str]) -> Any:
    return cluster._run_process(program, timeout=UPDATE_TIMEOUT, env=environment)
