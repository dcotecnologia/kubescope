"""Run the command that updates what the Plugins extension lists as installed.

The extension builds the command (`aws eks update-addon`, `helm upgrade`
or `az k8s-extension update`), shows it and asks; the app runs it here,
with the keys of the context's account and the kubeconfigs it reads, and
only through `Writes.run_update`, which refuses everything but those
three and answers only in the write mode. No Qt.
"""

import logging
import subprocess
from typing import Any

from kubescope import cluster
from kubescope.cluster import ClusterError
from kubescope.writes import _with_kubeconfig

logger = logging.getLogger(__name__)

UPDATE_TIMEOUT = 600  # seconds a helm upgrade may wait for the release


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
