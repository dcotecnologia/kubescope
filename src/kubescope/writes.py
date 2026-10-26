"""The actions that change a cluster, apart from the read paths of `cluster`.

Nothing here runs unless the person turned on the write mode in the
settings and confirmed the action. Each function sends one request with
the client and the credentials of the chosen context (see `cluster`),
except the shell, which only builds the command for the person's own
terminal. No Qt.
"""

import logging
import os
import re
import shlex
import subprocess
import sys
from datetime import UTC, datetime
from functools import partial
from typing import Any

from kubescope import cluster
from kubescope.cluster import ClusterError

logger = logging.getLogger(__name__)

MAX_REPLICAS = 10000
RESTARTED_AT = "kubectl.kubernetes.io/restartedAt"
_MERGE_PATCH = "application/merge-patch+json"
_STRATEGIC_PATCH = "application/strategic-merge-patch+json"
# bash where the image has it, the plain shell where it does not
_SHELL = "command -v bash >/dev/null 2>&1 && exec bash || exec sh"


def _send(
    method: str,
    path: str,
    context: str,
    body: dict[str, Any] | None,
    content_type: str,
) -> None:
    from kubernetes.client.exceptions import ApiException
    from urllib3.exceptions import HTTPError

    attempt = 0
    while True:
        attempt += 1
        api = cluster._cached_client(context, fresh=attempt == 2)
        try:
            verb, url, headers, payload, _form = api.param_serialize(
                method,
                path,
                header_params={
                    "Accept": "application/json",
                    "Content-Type": content_type,
                },
                body=body,
                auth_settings=["BearerToken"],
            )
            response = api.call_api(
                verb, url, headers, payload, _request_timeout=cluster.REQUEST_TIMEOUT
            )
            data = response.read()
        except ApiException as error:  # the TLS handshake failed
            raise ClusterError(str(error.reason or error)) from error
        except HTTPError as error:  # unreachable, timed out, connection reset
            raise ClusterError(str(getattr(error, "reason", None) or error)) from error
        if response.status != 401 or attempt == 2:
            break
        logger.debug("The cluster refused the token; signing in again")
    logger.info("%s %s: %s", method, path, response.status)
    if not 200 <= response.status < 300:
        raise ClusterError(
            cluster._status_message(response.status, response.reason, data)
        )


def _write(
    method: str,
    path: str,
    context: str,
    body: dict[str, Any] | None = None,
    content_type: str = "application/json",
) -> None:
    try:
        cluster._in_background(
            partial(_send, method, path, context, body, content_type),
            cluster.REQUEST_TIMEOUT,
        )
    except TimeoutError as error:
        logger.warning("Timed out: %s %s", method, path)
        raise ClusterError(
            "The request timed out while contacting the cluster"
        ) from error


def delete_pod(context: str, namespace: str, name: str) -> None:
    """Delete a Pod; a controller that owns it makes a new one."""
    _write("DELETE", cluster._resource_path("pods", namespace, name), context)


def evict_pod(context: str, namespace: str, name: str) -> None:
    """Ask the cluster to evict a Pod, which respects its disruption budget
    (and is refused when that budget would be broken)."""
    _write(
        "POST",
        cluster._resource_path("pods", namespace, name) + "/eviction",
        context,
        {
            "apiVersion": "policy/v1",
            "kind": "Eviction",
            "metadata": {"name": name, "namespace": namespace},
        },
    )


def scale_deployment(context: str, namespace: str, name: str, replicas: int) -> None:
    if not 0 <= replicas <= MAX_REPLICAS:
        raise ValueError(f"The replicas must be between 0 and {MAX_REPLICAS}")
    _write(
        "PATCH",
        cluster._resource_path("deployments", namespace, name) + "/scale",
        context,
        {"spec": {"replicas": replicas}},
        _MERGE_PATCH,
    )


def restart_deployment(context: str, namespace: str, name: str) -> None:
    """A rolling restart, the way `kubectl rollout restart` does it: stamp the
    Pod template so the Deployment rolls its Pods."""
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write(
        "PATCH",
        cluster._resource_path("deployments", namespace, name),
        context,
        {"spec": {"template": {"metadata": {"annotations": {RESTARTED_AT: stamp}}}}},
        _STRATEGIC_PATCH,
    )


_POWERSHELL_SAFE = re.compile(r"[A-Za-z0-9_./:=@%+,-]+")


def _powershell_quote(argument: str) -> str:
    """One argument for PowerShell: as it is when plain, otherwise in single
    quotes, where nothing expands and a quote is doubled."""
    if _POWERSHELL_SAFE.fullmatch(argument):
        return argument
    return "'" + argument.replace("'", "''") + "'"


def _command_lines(arguments: list[str]) -> list[tuple[str, str]]:
    """A kubectl command for the person's terminal as (shell, command) pairs,
    quoted for their system: one for a POSIX shell on Linux and macOS (no shell
    name), and on Windows one for PowerShell and one for cmd.

    The kubeconfig files the app was set to read go along when they are not the
    default. One file goes in `--kubeconfig`, which every shell understands.
    Several can only be given in the KUBECONFIG variable, which each shell sets
    in its own way.
    """
    files = cluster._kubeconfig_files
    if len(files) == 1:
        arguments = [arguments[0], "--kubeconfig", files[0], *arguments[1:]]
    paths = os.pathsep.join(files)
    if sys.platform != "win32":
        line = shlex.join(arguments)
        return [
            ("", f"KUBECONFIG={shlex.quote(paths)} {line}" if len(files) > 1 else line)
        ]
    powershell = " ".join(_powershell_quote(argument) for argument in arguments)
    cmd = subprocess.list2cmdline(arguments)
    if len(files) > 1:
        powershell = f"$env:KUBECONFIG = {_powershell_quote(paths)}; {powershell}"
        cmd = f'set "KUBECONFIG={paths}" && {cmd}'
    return [("PowerShell", powershell), ("cmd", cmd)]


def shell_commands(
    context: str, namespace: str, pod: str, container: str
) -> list[tuple[str, str]]:
    """The complete kubectl commands that open a shell in a container, for the
    person to run in their own terminal.

    They name the context, the namespace and the container. Nothing is
    run here.
    """
    return _command_lines(
        [
            "kubectl",
            "--context",
            context,
            "--namespace",
            namespace,
            "exec",
            "-it",
            pod,
            "-c",
            container,
            "--",
            "sh",
            "-c",
            _SHELL,
        ]
    )


def service_ports(document: dict[str, Any]) -> list[tuple[int, str]]:
    """The ports of a Service that can be forwarded, as (number, label): only
    TCP ones, which is all `kubectl port-forward` does."""
    ports = []
    for port in (document.get("spec") or {}).get("ports") or []:
        number = port.get("port")
        if not isinstance(number, int) or (port.get("protocol") or "TCP") != "TCP":
            continue
        name = port.get("name")
        ports.append((number, f"{number} ({name})" if name else str(number)))
    return ports


def container_ports(
    document: dict[str, Any], services: list[dict[str, Any]] | tuple = ()
) -> list[tuple[int, str]]:
    """The TCP ports a Pod, or the Pod template of a workload, can be reached
    on, as (number, label) without repeats: the ones its containers declare,
    then the ones the Services that select it send to (their target port)."""
    spec = document.get("spec") or {}
    template = spec.get("template") or {}
    spec, meta = (
        template.get("spec") or spec,
        template.get("metadata") or document.get("metadata"),
    )
    labels = (meta or {}).get("labels") or {}
    ports: dict[int, str] = {}
    names: dict[str, int] = {}
    for container in spec.get("containers") or []:
        for port in container.get("ports") or []:
            number = port.get("containerPort")
            if not isinstance(number, int) or (port.get("protocol") or "TCP") != "TCP":
                continue
            name = port.get("name")
            if name:
                names[name] = number
            ports.setdefault(number, f"{number} ({name})" if name else str(number))
    for service in services:
        selector = (service.get("spec") or {}).get("selector") or {}
        if not selector or any(
            labels.get(key) != value for key, value in selector.items()
        ):
            continue
        for port in service["spec"].get("ports") or []:
            target = port.get("targetPort", port.get("port"))
            number = names.get(target) if isinstance(target, str) else target
            if not isinstance(number, int) or (port.get("protocol") or "TCP") != "TCP":
                continue
            via = (service.get("metadata") or {}).get("name", "")
            ports.setdefault(number, f"{number} (Service {via})")
    return list(ports.items())


def forward_commands(
    context: str,
    namespace: str,
    service: str,
    remote: int,
    local: int,
    kind: str = "service",
) -> list[tuple[str, str]]:
    """The complete kubectl commands that forward a local port to a port of a
    Service, a Pod or a StatefulSet (named by `kind`), for the person to run in
    their own terminal.

    Nothing is run here.
    """
    return _command_lines(
        [
            "kubectl",
            "--context",
            context,
            "--namespace",
            namespace,
            "port-forward",
            f"{kind}/{service}",
            f"{local}:{remote}",
        ]
    )
