import contextlib
import json
import logging
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from concurrent.futures import Future, InvalidStateError, ThreadPoolExecutor
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from functools import partial
from pathlib import Path
from typing import Any
from urllib.parse import quote

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubernetes.config.config_exception import ConfigException
from kubernetes.config.kube_config import ConfigNode, KubeConfigMerger
from urllib3.exceptions import HTTPError

from kubescope.errors import first_line, is_auth_error
from kubescope.models import (
    BAD_STATUSES,
    OK_STATUSES,
    WARNING_STATUSES,
    ClusterInfo,
    ClusterOverview,
    ClusterResource,
    EventInfo,
    KindSummary,
    NodeInfo,
    PodInfo,
    Workload,
    WorkloadsOverview,
    format_age,
    parse_cpu,
    parse_memory,
)

logger = logging.getLogger(__name__)


class ClusterError(RuntimeError):
    """Raised when a request to the cluster or an AWS CLI command fails."""


REQUEST_TIMEOUT = 45  # seconds a cluster request may take
_running: set[subprocess.Popen] = set()
_pending: set[Future] = set()
_running_lock = threading.Lock()


def _describe(command: list[str]) -> str:
    """A command line for the log: the program name, then its arguments."""
    return " ".join([Path(command[0]).name, *command[1:]])


def _stop(process: subprocess.Popen) -> None:
    """Stop a command and everything it started: the AWS CLI can start more
    processes, all holding the output open."""
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(process.pid)],
            capture_output=True,
            check=False,
        )
    else:
        with contextlib.suppress(ProcessLookupError):  # it may already be gone
            os.killpg(process.pid, signal.SIGTERM)


def _run_process(command: list[str], timeout: float) -> subprocess.CompletedProcess:
    """Run a command and capture its output, keeping it listed while it runs so
    closing the app can stop it."""
    label = _describe(command)
    logger.debug("Run: %s", label)
    started = time.monotonic()
    if sys.platform == "win32":  # az and gcloud are .cmd files there
        command = [shutil.which(command[0]) or command[0], *command[1:]]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=sys.platform != "win32",  # its own group, to stop it whole
    )
    with _running_lock:
        _running.add(process)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.warning("Timed out after %ss: %s", timeout, label)
        _stop(process)
        process.communicate()
        raise
    finally:
        with _running_lock:
            _running.discard(process)
    logger.debug(
        "Exit %s after %.2fs: %s", process.returncode, time.monotonic() - started, label
    )
    if process.returncode != 0:
        logger.debug("stderr: %s", first_line(stderr))
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)


def cancel_running() -> None:
    """Stop every AWS CLI process and cluster request in flight; their callers
    see a failure and return at once."""
    with _running_lock:
        if _running or _pending:
            logger.info("Stopping %d running command(s)", len(_running) + len(_pending))
        for process in _running:
            _stop(process)
        for outcome in _pending:
            with contextlib.suppress(InvalidStateError):  # it may have just ended
                outcome.set_exception(ClusterError("The request was cancelled"))


def _in_background[T](call: Callable[[], T], timeout: float) -> T:
    """Run a blocking call in a daemon thread and wait for it, so that
    `cancel_running` and the timeout can give up on it at once; the thread ends
    on its own, and never keeps the app from quitting."""
    outcome: Future = Future()

    def work() -> None:
        with contextlib.suppress(InvalidStateError):  # nobody is waiting anymore
            try:
                outcome.set_result(call())
            except Exception as error:
                outcome.set_exception(error)

    with _running_lock:
        _pending.add(outcome)
    threading.Thread(target=work, daemon=True).start()
    try:
        return outcome.result(timeout=timeout)
    finally:
        with _running_lock:
            _pending.discard(outcome)


_kubeconfig_files: list[str] = []
_custom_logins: dict[str, str] = {}


def configure(
    kubeconfig_files: list[str] | None = None,
    sign_in_commands: dict[str, str] | None = None,
) -> None:
    """Apply the preferences that change how clusters are reached: the
    kubeconfig files to read (none means KUBECONFIG, or ~/.kube/config) and the
    commands that sign in for sign-in programs the app does not know."""
    global _kubeconfig_files, _custom_logins
    _kubeconfig_files = list(kubeconfig_files or [])
    _custom_logins = dict(sign_in_commands or {})
    forget_clients()  # they were made from the previous files


def parse_command(text: str) -> list[str]:
    """A command line as a list of arguments; raises ValueError when it is
    empty or has an unclosed quote.

    It is never run through a shell.
    """
    arguments = shlex.split(text, posix=sys.platform != "win32")
    arguments = [argument.strip('"') for argument in arguments]
    if not arguments:
        raise ValueError("The command is empty")
    return arguments


def _kubeconfig_paths() -> str:
    if _kubeconfig_files:
        return os.pathsep.join(_kubeconfig_files)
    return os.environ.get("KUBECONFIG") or "~/.kube/config"


def _plain(node: Any) -> Any:
    return node.value if isinstance(node, ConfigNode) else node


def _kubeconfig() -> dict[str, Any]:
    """The kubeconfig files merged into one document; empty when there are
    none."""
    try:
        merged = KubeConfigMerger(_kubeconfig_paths()).config
    except (ConfigException, OSError, KeyError) as error:  # KeyError: no name
        raise ClusterError(f"Could not read the kubeconfig: {error}") from error
    return _plain(merged) or {}


def _named(entries: list[Any] | None, name: str | None) -> dict[str, Any]:
    """The kubeconfig entry (context, user...) with that name."""
    return next(
        (entry for entry in map(_plain, entries or []) if entry.get("name") == name),
        {},
    )


class _SignInErrors(logging.Handler):
    """Collects what the kubernetes library logs, on the thread that created
    it, when the sign-in program of a kubeconfig fails: the library logs that
    failure and goes on without credentials, which would only show later as a
    vague "Unauthorized"."""

    def __init__(self) -> None:
        super().__init__(logging.ERROR)
        self.thread = threading.get_ident()
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        if record.thread == self.thread and record.module == "kube_config":
            self.messages.append(record.getMessage())


_MISSING_PROGRAM = re.compile(
    r"No such file or directory: '([^']+)'|'([^']+)' is not recognized"
)


def _sign_in_failure(message: str) -> str:
    """The failure of a sign-in program, worded for `describe_error`."""
    if "has no attribute 'strip'" in message:
        # started from a terminal, the library shows the program's error there
        # and then fails to read it
        return (
            "exec: the sign-in command failed, and its error went to the "
            "terminal; your credentials may have expired"
        )
    missing = _MISSING_PROGRAM.search(message)
    if missing:
        return f"exec: executable {missing.group(1) or missing.group(2)} not found"
    return message


def _api_client(context: str) -> client.ApiClient:
    """A client for one context.

    The kubeconfig is only read: refreshed
    credentials are never written back to it.
    """
    errors = _SignInErrors()
    logging.getLogger().addHandler(errors)
    try:
        api = config.new_client_from_config(
            config_file=_kubeconfig_paths(), context=context, persist_config=False
        )
    except ConfigException as error:
        if "Expected object with name" in str(error):
            raise ClusterError(
                f"context was not found for specified context: {context}"
            ) from error
        raise ClusterError(str(error)) from error
    except OSError as error:
        raise ClusterError(f"Could not read the kubeconfig: {error}") from error
    finally:
        logging.getLogger().removeHandler(errors)
    if errors.messages:
        api.close()
        raise ClusterError(_sign_in_failure(errors.messages[0]))
    return api


_clients: dict[str, client.ApiClient] = {}
_client_locks: dict[str, threading.Lock] = {}


def _cached_client(context: str, fresh: bool = False) -> client.ApiClient:
    """The client of a context, made once and then reused, with its token and
    its open connections: the sign-in program of the kubeconfig runs again only
    when there is no client yet, or `fresh` asks for a new one because the
    cluster refused the token. Calls for the same context wait for the first
    one instead of each running the sign-in."""
    with _running_lock:
        lock = _client_locks.setdefault(context, threading.Lock())
    with lock:
        if fresh and (old := _clients.pop(context, None)) is not None:
            old.close()
        if context not in _clients:
            _clients[context] = _api_client(context)
        return _clients[context]


def forget_clients() -> None:
    """Drop every client, so the next request signs in again."""
    with _running_lock:
        stale = list(_clients.values())
        _clients.clear()
    for api in stale:
        api.close()


def _status_message(status: int, reason: str | None, body: bytes) -> str:
    """The cluster's own explanation of a refused request, as kubectl shows
    it."""
    try:
        message = json.loads(body).get("message")
    except (ValueError, AttributeError):  # not a Status document
        message = None
    return message or f"{status} {reason or 'Error'}"


def _fetch(path: str, context: str, query: list[tuple[str, str]], accept: str) -> bytes:
    started = time.monotonic()
    for attempt in (1, 2):
        api = _cached_client(context, fresh=attempt == 2)
        try:
            method, url, headers, body, _form = api.param_serialize(
                "GET",
                path,
                query_params=query,
                header_params={"Accept": accept},
                auth_settings=["BearerToken"],
            )
            response = api.call_api(
                method, url, headers, body, _request_timeout=REQUEST_TIMEOUT
            )
            data = response.read()
        except ApiException as error:  # the TLS handshake failed
            raise ClusterError(str(error.reason or error)) from error
        except HTTPError as error:  # unreachable, timed out, connection reset
            raise ClusterError(str(getattr(error, "reason", None) or error)) from error
        if response.status != 401 or attempt == 2:
            break
        logger.debug("The cluster refused the token; signing in again")
    logger.debug(
        "GET %s: %s after %.2fs", path, response.status, time.monotonic() - started
    )
    if not 200 <= response.status < 300:
        message = _status_message(response.status, response.reason, data)
        logger.debug("error: %s", first_line(message))
        raise ClusterError(message)
    return data


def _request(
    path: str,
    context: str,
    query: list[tuple[str, str]] | None = None,
    accept: str = "application/json",
) -> bytes:
    """GET a path of the cluster's API and return the body."""
    try:
        return _in_background(
            partial(_fetch, path, context, query or [], accept), REQUEST_TIMEOUT
        )
    except TimeoutError as error:
        logger.warning("Timed out after %ss: GET %s", REQUEST_TIMEOUT, path)
        raise ClusterError(
            "The request timed out while contacting the cluster"
        ) from error


def _get_json(
    path: str,
    context: str,
    query: list[tuple[str, str]] | None = None,
    accept: str = "application/json",
) -> dict[str, Any]:
    try:
        payload = json.loads(_request(path, context, query, accept))
    except ValueError as error:
        raise ClusterError("The cluster returned an unexpected response") from error
    if not isinstance(payload, dict):
        raise ClusterError("The cluster returned an unexpected JSON document")
    return payload


# The API group each resource lives in; the core group is "/api/v1".
_API_PATHS = {
    "pods": "/api/v1",
    "nodes": "/api/v1",
    "namespaces": "/api/v1",
    "events": "/api/v1",
    "services": "/api/v1",
    "endpoints": "/api/v1",
    "replicationcontrollers": "/api/v1",
    "configmaps": "/api/v1",
    "secrets": "/api/v1",
    "resourcequotas": "/api/v1",
    "limitranges": "/api/v1",
    "deployments": "/apis/apps/v1",
    "statefulsets": "/apis/apps/v1",
    "daemonsets": "/apis/apps/v1",
    "replicasets": "/apis/apps/v1",
    "jobs": "/apis/batch/v1",
    "cronjobs": "/apis/batch/v1",
    "endpointslices": "/apis/discovery.k8s.io/v1",
    "ingresses": "/apis/networking.k8s.io/v1",
    "ingressclasses": "/apis/networking.k8s.io/v1",
    "networkpolicies": "/apis/networking.k8s.io/v1",
    "horizontalpodautoscalers": "/apis/autoscaling/v2",
    "poddisruptionbudgets": "/apis/policy/v1",
    "priorityclasses": "/apis/scheduling.k8s.io/v1",
    "runtimeclasses": "/apis/node.k8s.io/v1",
    "leases": "/apis/coordination.k8s.io/v1",
    "mutatingwebhookconfigurations": "/apis/admissionregistration.k8s.io/v1",
    "validatingwebhookconfigurations": "/apis/admissionregistration.k8s.io/v1",
}
_METRICS_PATH = "/apis/metrics.k8s.io/v1beta1"


def _resource_path(
    resource: str, namespace: str | None = None, name: str | None = None
) -> str:
    """The API path of a resource type, or of one object.

    Names come from the cluster, so they are encoded.
    """
    parts = [_API_PATHS[resource]]
    if namespace:
        parts += ["namespaces", quote(namespace, safe="")]
    parts.append(resource)
    if name:
        parts.append(quote(name, safe=""))
    return "/".join(parts)


def _list(
    resource: str,
    context: str,
    namespace: str | None = None,
    selector: str | None = None,
) -> dict[str, Any]:
    """Every object of a type, in a namespace or in all of them.

    A list does not name the kind of its items, so each gets it.
    """
    query = [("labelSelector", selector)] if selector else []
    document = _get_json(_resource_path(resource, namespace), context, query)
    kind = _KINDS[resource]
    for item in document.get("items") or []:
        item.setdefault("kind", kind)
    return document


def _list_kinds(
    kinds: tuple[str, ...], context: str, namespace: str | None
) -> dict[str, Any]:
    """The objects of several kinds, listed at the same time, in one
    document."""
    documents = _together(
        *(partial(_list, _RESOURCES[kind], context, namespace) for kind in kinds)
    )
    return {
        "items": [
            item for document in documents for item in document.get("items") or []
        ]
    }


def list_contexts() -> tuple[list[str], str | None]:
    document = _kubeconfig()
    contexts = sorted(
        name
        for entry in document.get("contexts") or []
        if (name := _plain(entry).get("name"))
    )
    current = document.get("current-context")
    logger.info("Found %d kubeconfig context(s)", len(contexts))
    return contexts, current if current in contexts else None


LOGIN_TIMEOUT = 300  # seconds; the sign-in waits for the person in the browser
AWS_TIMEOUT = 30


def _run_command(command: list[str], timeout: float) -> str:
    try:
        result = _run_process(command, timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise ClusterError(f"{command[0]} timed out") from error
    except OSError as error:
        raise ClusterError(f"Could not start {command[0]}: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ClusterError(detail or f"{command[0]} exited with {result.returncode}")
    return result.stdout


def _sign_in_program(context: str) -> dict[str, Any]:
    """The sign-in program (the `exec` entry) of the context's user.

    Only that entry is read from the kubeconfig; its credentials are not
    touched.
    """
    document = _kubeconfig()
    user = (_named(document.get("contexts"), context).get("context") or {}).get("user")
    return (_named(document.get("users"), user).get("user") or {}).get("exec") or {}


def _flag(arguments: list[str], flag: str) -> str | None:
    """The value after a command-line flag, if the flag is there."""
    return next(
        (
            arguments[index + 1]
            for index, argument in enumerate(arguments[:-1])
            if argument == flag
        ),
        None,
    )


def _aws_profile(context: str) -> tuple[bool, str | None]:
    """Whether the context signs in through the AWS CLI, and with which
    profile."""
    login = _sign_in_program(context)
    if Path(login.get("command") or "").stem != "aws":
        return False, None
    profile = _flag(login.get("args") or [], "--profile")
    for variable in login.get("env") or []:
        if variable.get("name") == "AWS_PROFILE":
            profile = profile or variable.get("value")
    return True, profile


def _profile_arguments(profile: str | None) -> list[str]:
    return ["--profile", profile] if profile else []


def _eks_target(context: str, name_flag: str = "--cluster-name") -> list[str]:
    """The AWS CLI arguments that name the EKS cluster of a context: its name
    and region come from the sign-in command, as `aws eks update-kubeconfig`
    writes them."""
    uses_aws, profile = _aws_profile(context)
    arguments = _sign_in_program(context).get("args") or []
    name, region = _flag(arguments, "--cluster-name"), _flag(arguments, "--region")
    if not uses_aws or not name:
        raise ClusterError("This list is only available for Amazon EKS contexts")
    return [
        name_flag,
        name,
        *(["--region", region] if region else []),
        *_profile_arguments(profile),
    ]


def get_cluster_info(context: str) -> ClusterInfo:
    """What `aws eks describe-cluster` says about the context's EKS cluster."""
    cluster = _eks_json("describe-cluster", _eks_target(context, "--name")).get(
        "cluster"
    )
    cluster = cluster or {}
    try:
        created = datetime.fromisoformat(str(cluster.get("createdAt")))
        created_text = created.astimezone().strftime("%Y-%m-%d %H:%M")
    except ValueError:
        created_text = _NO_VALUE
    oidc = (cluster.get("identity") or {}).get("oidc") or {}
    vpc = cluster.get("resourcesVpcConfig") or {}
    network = cluster.get("kubernetesNetworkConfig") or {}
    public, private = vpc.get("endpointPublicAccess"), vpc.get("endpointPrivateAccess")
    access = {(True, False): "Public", (False, True): "Private"}.get(
        (public, private), "Public and private" if public and private else _NO_VALUE
    )
    return ClusterInfo(
        status=str(cluster.get("status") or _NO_VALUE).capitalize(),
        version=cluster.get("version") or _NO_VALUE,
        platform_version=cluster.get("platformVersion") or _NO_VALUE,
        created=created_text,
        provider="EKS",
        endpoint=cluster.get("endpoint") or _NO_VALUE,
        arn=cluster.get("arn") or _NO_VALUE,
        role_arn=cluster.get("roleArn") or _NO_VALUE,
        oidc_issuer=oidc.get("issuer") or _NO_VALUE,
        vpc_id=vpc.get("vpcId") or _NO_VALUE,
        subnets=tuple(vpc.get("subnetIds") or ()),
        security_group=vpc.get("clusterSecurityGroupId") or _NO_VALUE,
        additional_security_groups=tuple(vpc.get("securityGroupIds") or ()),
        ip_family=str(network.get("ipFamily") or _NO_VALUE).replace("ipv", "IPv"),
        service_cidr=network.get("serviceIpv4Cidr") or _NO_VALUE,
        endpoint_access=access,
        public_access_cidrs=tuple(vpc.get("publicAccessCidrs") or ()),
    )


def is_eks_context(context: str) -> bool:
    """Whether the context is an Amazon EKS cluster, the only kind with Node
    Groups."""
    try:
        _eks_target(context)
    except ClusterError:
        return False
    return True


def _eks_json(subcommand: str, target: list[str], *extra: str) -> dict[str, Any]:
    output = _run_command(
        ["aws", "eks", subcommand, *target, *extra, "--output", "json"], AWS_TIMEOUT
    )
    try:
        document = json.loads(output)
    except ValueError as error:
        raise ClusterError("The AWS CLI answered with something unexpected") from error
    if not isinstance(document, dict):
        raise ClusterError("The AWS CLI answered with something unexpected")
    return document


# EKS kind -> what the AWS CLI calls one (`describe-<one>`, `--<one>-name`), the
# plural (`list-<many>`) and the key that holds its name.
_EKS_KINDS = {
    "NodeGroup": ("nodegroup", "nodegroups", "nodegroupName"),
    "Addon": ("addon", "addons", "addonName"),
}


def _describe_eks(kind: str, target: list[str], name: str) -> dict[str, Any]:
    one = _EKS_KINDS[kind][0]
    return _eks_json(f"describe-{one}", target, f"--{one}-name", name).get(one) or {}


def _list_eks(kind: str, context: str) -> list[dict[str, Any]]:
    """Every Node Group or Add-on of the context's EKS cluster, described at
    the same time."""
    target = _eks_target(context)
    many = _EKS_KINDS[kind][1]
    names = _eks_json(f"list-{many}", target).get(many) or []
    if not names:
        return []
    return _together(*(partial(_describe_eks, kind, target, name) for name in names))


def _eks_age(item: dict[str, Any], now: datetime) -> str:
    try:
        created = datetime.fromisoformat(str(item.get("createdAt")))
    except ValueError:
        return "unknown"
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    return format_age((now - created).total_seconds())


def _nodegroup_values(group: dict[str, Any]) -> tuple[str, ...]:
    scaling = group.get("scalingConfig") or {}
    nodes = (
        f"{scaling['desiredSize']} ({scaling.get('minSize', 0)}–"
        f"{scaling.get('maxSize', scaling['desiredSize'])})"
        if scaling.get("desiredSize") is not None
        else _NO_VALUE
    )
    return (
        group.get("status") or _NO_VALUE,
        _listed(group.get("instanceTypes") or []),
        nodes,
        group.get("amiType") or _NO_VALUE,
        group.get("releaseVersion") or _NO_VALUE,
    )


def _addon_values(addon: dict[str, Any]) -> tuple[str, ...]:
    return (
        addon.get("status") or _NO_VALUE,
        addon.get("addonVersion") or _NO_VALUE,
        "EKS",
    )


_EKS_VALUES = {"NodeGroup": _nodegroup_values, "Addon": _addon_values}


def _parse_eks(
    kind: str, item: dict[str, Any], now: datetime
) -> ClusterResource | None:
    name = item.get(_EKS_KINDS[kind][2])
    if not name:
        return None
    return ClusterResource(
        namespace="",
        kind=kind,
        name=name,
        values=_EKS_VALUES[kind](item),
        age=_eks_age(item, now),
    )


def _is_sso_profile(profile: str | None) -> bool:
    """SSO profiles sign in through the browser; the others use access keys."""
    for key in ("sso_session", "sso_start_url"):
        try:
            value = _run_command(
                ["aws", "configure", "get", key, *_profile_arguments(profile)],
                AWS_TIMEOUT,
            )
        except ClusterError:
            continue
        if value.strip():
            return True
    return False


@dataclass(frozen=True, slots=True)
class LoginAction:
    """How to sign in to a context's AWS profile."""

    command: list[str]
    profile: str | None
    interactive: bool  # access keys are typed in a terminal; SSO uses the browser
    provider: str = "AWS"


# sign-in program of the kubeconfig -> the cloud, and the command that signs in
_CLOUD_LOGINS = {
    "gke-gcloud-auth-plugin": ("Google Cloud", ["gcloud", "auth", "login"]),
    "gcloud": ("Google Cloud", ["gcloud", "auth", "login"]),
    "kubelogin": ("Azure", ["az", "login"]),
    "az": ("Azure", ["az", "login"]),
}


def login_action(context: str) -> LoginAction | None:
    """The sign-in for a context: "aws sso login" for an AWS SSO profile, "aws
    configure" in a terminal for an access-key profile, "gcloud auth login" for
    Google Cloud and "az login" for Azure.

    Other login tools are not supported and return None.
    """
    if _custom_logins:
        program = Path(_sign_in_program(context).get("command") or "").stem
        if program in _custom_logins:
            try:
                command = parse_command(_custom_logins[program])
            except ValueError:
                return None
            logger.info(
                "Context %s signs in with the command set for %s", context, program
            )
            return LoginAction(command, None, False, program)
    uses_aws, profile = _aws_profile(context)
    if not uses_aws:
        program = Path(_sign_in_program(context).get("command") or "").stem
        cloud = _CLOUD_LOGINS.get(program)
        if cloud is None:
            return None
        logger.info("Context %s signs in with %s", context, cloud[0])
        return LoginAction(cloud[1], None, False, cloud[0])
    arguments = _profile_arguments(profile)
    if _is_sso_profile(profile):
        logger.info("AWS profile %s signs in with SSO", profile or "default")
        return LoginAction(["aws", "sso", "login", *arguments], profile, False)
    logger.info("AWS profile %s uses access keys", profile or "default")
    return LoginAction(["aws", "configure", *arguments], profile, True)


def _custom_sign_in_failed(error: ClusterError, context: str) -> bool:
    """Whether the sign-in program of the context failed and the person set a
    command to sign in with it: its error text is not for the app to guess."""
    if not (_custom_logins and str(error).startswith("exec:")):
        return False
    try:
        program = Path(_sign_in_program(context).get("command") or "").stem
    except ClusterError:
        return False
    return program in _custom_logins


def check_login(context: str) -> tuple[bool, LoginAction | None]:
    """Whether the context needs a sign-in, and how to do it.

    The cluster request catches an expired SSO session. Access keys that
    were rotated or revoked only fail at the cluster, because `aws eks
    get- token` signs locally, so AWS contexts are also checked with
    STS. Other failures (an unreachable cluster, denied access) are not
    a login problem and report as signed in.
    """
    try:
        _request("/version", context)
        uses_aws, profile = _aws_profile(context)
        if uses_aws:
            _run_command(
                ["aws", "sts", "get-caller-identity", *_profile_arguments(profile)],
                AWS_TIMEOUT,
            )
    except ClusterError as error:
        if not (is_auth_error(str(error)) or _custom_sign_in_failed(error, context)):
            logger.info("Login check for %s: not a credentials problem", context)
            logger.debug("Login check detail: %s", first_line(str(error)))
            return False, None
        logger.info("Login check for %s: sign-in needed", context)
        logger.debug("Login check detail: %s", first_line(str(error)))
        try:
            return True, login_action(context)
        except ClusterError:
            return True, None
    logger.info("Login check for %s: signed in", context)
    return False, None


_TERMINALS = (
    ("x-terminal-emulator", "-e"),
    ("gnome-terminal", "--"),
    ("konsole", "-e"),
    ("xfce4-terminal", "-x"),
    ("xterm", "-e"),
)


def _open_terminal(command: list[str]) -> None:
    """Run a command in a new terminal window and return without waiting."""
    if sys.platform == "win32":
        launcher = ["cmd", "/c", "start", "", "cmd", "/k", *command]
    else:
        launcher = next(
            (
                [path, flag, *command]
                for name, flag in _TERMINALS
                if (path := shutil.which(name))
            ),
            None,
        )
        if launcher is None:
            raise ClusterError(
                "No terminal found. Run this in a terminal: " + " ".join(command)
            )
    try:
        subprocess.Popen(launcher)
    except OSError as error:
        raise ClusterError(f"Could not open a terminal: {error}") from error


def run_login(action: LoginAction) -> None:
    """Start the sign-in.

    SSO opens the browser and is waited for; access keys open a terminal
    where the person types them, so the app never sees them.
    """
    logger.info("Starting sign-in: %s", _describe(action.command))
    if action.interactive:
        _open_terminal(action.command)
    else:
        _run_command(action.command, LOGIN_TIMEOUT)
        forget_clients()  # the new credentials are picked up by the next request
        logger.info("Sign-in finished for profile %s", action.profile or "default")


# Kubernetes kind -> the plural name of its resource.
_RESOURCES = {
    "Deployment": "deployments",
    "StatefulSet": "statefulsets",
    "DaemonSet": "daemonsets",
    "ReplicaSet": "replicasets",
    "ReplicationController": "replicationcontrollers",
    "Job": "jobs",
    "CronJob": "cronjobs",
}
_REPLICATED_KINDS = ("Deployment", "StatefulSet", "DaemonSet")


# Network kind -> the plural name of its resource.
_NETWORK_RESOURCES = {
    "Service": "services",
    "EndpointSlice": "endpointslices",
    "Endpoints": "endpoints",
    "Ingress": "ingresses",
    "IngressClass": "ingressclasses",
    "NetworkPolicy": "networkpolicies",
}
# Config kind -> the plural name of its resource.
_CONFIG_RESOURCES = {
    "ConfigMap": "configmaps",
    "Secret": "secrets",
    "ResourceQuota": "resourcequotas",
    "LimitRange": "limitranges",
    "HorizontalPodAutoscaler": "horizontalpodautoscalers",
    "PodDisruptionBudget": "poddisruptionbudgets",
    "PriorityClass": "priorityclasses",
    "RuntimeClass": "runtimeclasses",
    "Lease": "leases",
    "MutatingWebhookConfiguration": "mutatingwebhookconfigurations",
    "ValidatingWebhookConfiguration": "validatingwebhookconfigurations",
}
_LISTED_RESOURCES = {**_NETWORK_RESOURCES, **_CONFIG_RESOURCES}
_CLUSTER_WIDE = frozenset(
    {
        "IngressClass",
        "PriorityClass",
        "RuntimeClass",
        "MutatingWebhookConfiguration",
        "ValidatingWebhookConfiguration",
    }
)
_KINDS = {
    resource: kind
    for kind, resource in {
        **_RESOURCES,
        **_LISTED_RESOURCES,
        "Pod": "pods",
        "Node": "nodes",
        "Namespace": "namespaces",
        "Event": "events",
    }.items()
}
_NO_VALUE = "—"
_LISTED_VALUES = 3  # a long list of addresses shows its first ones and a count


def _job_state(spec: dict[str, Any], status: dict[str, Any]) -> str:
    conditions = {
        condition.get("type")
        for condition in status.get("conditions") or []
        if condition.get("status") == "True"
    }
    if "Failed" in conditions:
        return "Failed"
    if "Complete" in conditions:
        return "Complete"
    if spec.get("suspend"):
        return "Suspended"
    return "Running" if status.get("active") else "Pending"


def _parse_workload(item: dict[str, Any], now: datetime) -> Workload | None:
    metadata = item.get("metadata") or {}
    spec = item.get("spec") or {}
    status = item.get("status") or {}
    kind = item.get("kind")
    name = metadata.get("name")
    if kind not in _RESOURCES or not name:
        return None

    state = schedule = None
    if kind == "DaemonSet":
        desired = status.get("desiredNumberScheduled") or 0
        ready = status.get("numberReady") or 0
    elif kind == "Job":
        desired = spec.get("completions") or 1
        ready = status.get("succeeded") or 0
        state = _job_state(spec, status)
    elif kind == "CronJob":
        active = len(status.get("active") or [])
        desired, ready = 0, active
        schedule = spec.get("schedule")
        state = (
            "Suspended" if spec.get("suspend") else "Active" if active else "Scheduled"
        )
    else:
        desired = spec.get("replicas") or 0
        ready = status.get("readyReplicas") or 0

    age = "unknown"
    creation_timestamp = metadata.get("creationTimestamp")
    if creation_timestamp:
        created = datetime.fromisoformat(creation_timestamp.replace("Z", "+00:00"))
        age = format_age((now - created).total_seconds())
    return Workload(
        namespace=metadata.get("namespace") or "default",
        kind=kind,
        name=name,
        ready=ready,
        desired=desired,
        age=age,
        state=state,
        schedule=schedule,
    )


def _together(*calls: Any) -> list[Any]:
    """Run independent cluster calls at the same time, so a list waits for the
    slowest one instead of the sum; the first failure, in order, is raised."""
    with ThreadPoolExecutor(max_workers=len(calls)) as pool:
        futures = [pool.submit(call) for call in calls]
        return [future.result() for future in futures]


def _get_namespaces(context: str) -> list[str]:
    document = _list("namespaces", context)
    return sorted(
        item["metadata"]["name"]
        for item in document.get("items", [])
        if item.get("metadata", {}).get("name")
    )


def get_workloads(
    context: str,
    namespace: str | None = None,
    kinds: tuple[str, ...] = _REPLICATED_KINDS,
) -> tuple[list[str], list[Workload]]:
    namespaces, workloads_document = _together(
        partial(_get_namespaces, context),
        partial(_list_kinds, kinds, context, namespace),
    )
    now = datetime.now(UTC)
    workloads = [
        workload
        for item in workloads_document.get("items", [])
        if (workload := _parse_workload(item, now)) is not None
    ]
    workloads.sort(key=lambda row: (row.namespace, row.kind, row.name))
    return namespaces, workloads


def get_resource_details(
    context: str,
    kind: str,
    namespace: str,
    name: str,
) -> dict[str, Any]:
    if kind == "HelmRelease":
        return _helm_release_details(context, namespace, name)
    if kind in _EKS_KINDS:
        return _describe_eks(kind, _eks_target(context), name)
    resource = {**_RESOURCES, **_LISTED_RESOURCES, "Pod": "pods"}.get(kind)
    if resource is None:
        raise ClusterError(f"Unsupported resource kind: {kind}")
    document = _get_json(_resource_path(resource, namespace, name), context)
    return _redact_secret(document) if kind == "Secret" else document


_REDACTED = "<redacted>"
_LAST_APPLIED = "kubectl.kubernetes.io/last-applied-configuration"


def _redact_secret(document: dict[str, Any]) -> dict[str, Any]:
    """A Secret without its values: the keys stay, so you can see what it
    holds.

    The last-applied annotation is dropped too, as it repeats the
    values.
    """
    for field in ("data", "stringData"):
        if isinstance(document.get(field), dict):
            document[field] = dict.fromkeys(document[field], _REDACTED)
    annotations = (document.get("metadata") or {}).get("annotations")
    if isinstance(annotations, dict):
        annotations.pop(_LAST_APPLIED, None)
    return document


def _label_selector(resource: dict[str, Any]) -> str:
    selector = (resource.get("spec") or {}).get("selector") or {}
    if "matchLabels" not in selector and "matchExpressions" not in selector:
        selector = {"matchLabels": selector}  # a ReplicationController's plain map
    terms = [
        f"{key}={value}"
        for key, value in sorted((selector.get("matchLabels") or {}).items())
    ]
    for expression in selector.get("matchExpressions") or []:
        key = expression.get("key")
        operator = expression.get("operator")
        values = expression.get("values") or []
        if not key:
            raise ClusterError("Workload selector has an expression without a key")
        if operator in {"In", "NotIn"}:
            if not values:
                raise ClusterError(f"Workload selector {operator} requires values")
            joined_values = ",".join(values)
            terms.append(f"{key} {operator.lower()} ({joined_values})")
        elif operator == "Exists":
            terms.append(key)
        elif operator == "DoesNotExist":
            terms.append(f"!{key}")
        else:
            raise ClusterError(f"Unsupported workload selector operator: {operator}")
    if not terms:
        raise ClusterError("Workload has no label selector for its Pods")
    return ",".join(terms)


def _parse_pod(item: dict[str, Any], now: datetime) -> PodInfo | None:
    metadata = item.get("metadata") or {}
    spec = item.get("spec") or {}
    status = item.get("status") or {}
    name = metadata.get("name")
    if not name:
        return None
    containers = tuple(
        container["name"]
        for container in spec.get("containers") or []
        if container.get("name")
    )
    container_statuses = status.get("containerStatuses") or []
    age = "unknown"
    creation_timestamp = metadata.get("creationTimestamp")
    if creation_timestamp:
        created = datetime.fromisoformat(creation_timestamp.replace("Z", "+00:00"))
        age = format_age((now - created).total_seconds())
    return PodInfo(
        namespace=metadata.get("namespace") or "default",
        name=name,
        phase=status.get("phase") or "Unknown",
        ready=sum(bool(container.get("ready")) for container in container_statuses),
        total=len(containers),
        age=age,
        containers=containers,
        restarts=sum(
            container.get("restartCount") or 0 for container in container_statuses
        ),
        owner=_pod_owner(metadata),
    )


def _pod_owner(metadata: dict[str, Any]) -> tuple[str, str] | None:
    """The workload that controls a Pod; ReplicaSets map back to their
    Deployment."""
    for reference in metadata.get("ownerReferences") or []:
        kind, name = reference.get("kind"), reference.get("name")
        if not kind or not name or not reference.get("controller", True):
            continue
        if kind == "ReplicaSet" and "-" in name:
            return "Deployment", name.rsplit("-", 1)[0]
        return kind, name
    return None


def _pod_metrics(
    context: str, namespace: str | None
) -> dict[tuple[str, str], tuple[float, float]] | None:
    """Live (cores, bytes) per Pod; None when metrics-server is unavailable."""
    scope = f"/namespaces/{quote(namespace, safe='')}" if namespace else ""
    try:
        document = _get_json(f"{_METRICS_PATH}{scope}/pods", context)
    except ClusterError:
        return None
    usage: dict[tuple[str, str], tuple[float, float]] = {}
    for item in document.get("items", []):
        metadata = item.get("metadata") or {}
        cpu = memory = 0.0
        for container in item.get("containers") or []:
            container_usage = container.get("usage") or {}
            cpu += parse_cpu(container_usage.get("cpu"))
            memory += parse_memory(container_usage.get("memory"))
        usage[(metadata.get("namespace") or "default", metadata.get("name", ""))] = (
            cpu,
            memory,
        )
    return usage


def _pods_with_usage(context: str, namespace: str | None) -> list[PodInfo]:
    document, metrics = _together(
        partial(_list, "pods", context, namespace),
        partial(_pod_metrics, context, namespace),
    )
    now = datetime.now(UTC)
    pods = [
        pod
        for item in document.get("items", [])
        if (pod := _parse_pod(item, now)) is not None
    ]
    if metrics is not None:
        pods = [
            replace(pod, cpu=cpu, memory=memory)
            for pod in pods
            for cpu, memory in [metrics.get((pod.namespace, pod.name), (None, None))]
        ]
    return pods


def get_usage(
    context: str, namespace: str | None = None
) -> dict[tuple[str, str, str], tuple[int, float | None, float | None]]:
    """Restarts, CPU and memory per (namespace, kind, name) workload, from its
    Pods."""
    totals: dict[tuple[str, str, str], tuple[int, float | None, float | None]] = {}
    for pod in _pods_with_usage(context, namespace):
        if pod.owner is None:
            continue
        key = (pod.namespace, *pod.owner)
        restarts, cpu, memory = totals.get(key, (0, None, None))
        if pod.cpu is not None and pod.memory is not None:
            cpu = (cpu or 0.0) + pod.cpu
            memory = (memory or 0.0) + pod.memory
        totals[key] = (restarts + pod.restarts, cpu, memory)
        if pod.owner[0] == "Deployment":  # the ReplicaSet in between has its own row
            key = (pod.namespace, "ReplicaSet", pod.name.rsplit("-", 1)[0])
            restarts, cpu, memory = totals.get(key, (0, None, None))
            if pod.cpu is not None and pod.memory is not None:
                cpu = (cpu or 0.0) + pod.cpu
                memory = (memory or 0.0) + pod.memory
            totals[key] = (restarts + pod.restarts, cpu, memory)
    return totals


def _cronjob_pod_selector(context: str, workload: Workload) -> str | None:
    """A CronJob has no selector of its own: its Pods belong to the Jobs it
    created, which carry the job-name label."""
    document = _list("jobs", context, workload.namespace)
    names = [
        job["metadata"]["name"]
        for job in document.get("items", [])
        if any(
            owner.get("kind") == "CronJob" and owner.get("name") == workload.name
            for owner in job["metadata"].get("ownerReferences") or []
        )
    ]
    return f"job-name in ({','.join(names)})" if names else None


def get_workload_pods(context: str, workload: Workload) -> list[PodInfo]:
    if workload.kind == "CronJob":
        selector = _cronjob_pod_selector(context, workload)
        if selector is None:
            return []
    else:
        resource = get_resource_details(
            context, workload.kind, workload.namespace, workload.name
        )
        selector = _label_selector(resource)
    document = _list("pods", context, workload.namespace, selector)
    now = datetime.now(UTC)
    pods = [
        pod
        for item in document.get("items", [])
        if (pod := _parse_pod(item, now)) is not None
    ]
    return sorted(pods, key=lambda pod: pod.name)


def _listed(values: list[str]) -> str:
    """The first few values, then how many more there are."""
    if not values:
        return _NO_VALUE
    shown = ", ".join(values[:_LISTED_VALUES])
    hidden = len(values) - _LISTED_VALUES
    return f"{shown} +{hidden} more" if hidden > 0 else shown


def _port_names(ports: list[dict[str, Any]]) -> list[str]:
    return [
        f"{port.get('port')}/{port.get('protocol') or 'TCP'}"
        for port in ports
        if port.get("port") is not None
    ]


def _load_balancer_addresses(status: dict[str, Any]) -> list[str]:
    ingress = (status.get("loadBalancer") or {}).get("ingress") or []
    return [entry.get("hostname") or entry.get("ip") for entry in ingress if entry]


def _label_terms(selector: dict[str, Any]) -> str:
    labels = selector.get("matchLabels") or {}
    terms = [f"{key}={value}" for key, value in sorted(labels.items())]
    terms += [
        f"{expression.get('key')} {str(expression.get('operator')).lower()}"
        for expression in selector.get("matchExpressions") or []
    ]
    return ",".join(terms) or "*"  # an empty selector picks everything


def _service_values(item: dict[str, Any]) -> tuple[str, ...]:
    spec, status = item.get("spec") or {}, item.get("status") or {}
    service_type = spec.get("type") or "ClusterIP"
    external = _load_balancer_addresses(status) + (spec.get("externalIPs") or [])
    if not external and service_type == "LoadBalancer":
        external = ["pending"]
    ports = [
        f"{port['port']}:{port['nodePort']}/{port.get('protocol') or 'TCP'}"
        if port.get("nodePort")
        else f"{port['port']}/{port.get('protocol') or 'TCP'}"
        for port in spec.get("ports") or []
        if port.get("port") is not None
    ]
    return (
        service_type,
        spec.get("clusterIP") or _NO_VALUE,
        _listed(external),
        _listed(ports),
    )


def _endpoints_values(item: dict[str, Any]) -> tuple[str, ...]:
    addresses = []
    for subset in item.get("subsets") or []:
        ports = [port.get("port") for port in subset.get("ports") or []]
        for address in subset.get("addresses") or []:
            ip = address.get("ip")
            addresses += [f"{ip}:{port}" for port in ports] if ports else [ip]
    return (_listed(addresses),)


def _endpoint_slice_values(item: dict[str, Any]) -> tuple[str, ...]:
    addresses = [
        address
        for endpoint in item.get("endpoints") or []
        for address in (endpoint.get("addresses") or [])[:1]
    ]
    return (
        item.get("addressType") or _NO_VALUE,
        _listed(_port_names(item.get("ports") or [])),
        _listed(addresses),
    )


def _ingress_values(item: dict[str, Any]) -> tuple[str, ...]:
    metadata = item.get("metadata") or {}
    spec, status = item.get("spec") or {}, item.get("status") or {}
    ingress_class = spec.get("ingressClassName") or (
        metadata.get("annotations") or {}
    ).get("kubernetes.io/ingress.class")
    hosts = [rule.get("host") or "*" for rule in spec.get("rules") or []]
    ports = ["80", "443"] if spec.get("tls") else ["80"]
    return (
        ingress_class or _NO_VALUE,
        _listed(hosts),
        _listed(_load_balancer_addresses(status)),
        ", ".join(ports),
    )


def _ingress_class_values(item: dict[str, Any]) -> tuple[str, ...]:
    spec = item.get("spec") or {}
    parameters = spec.get("parameters") or {}
    reference = (
        f"{parameters['kind']}/{parameters['name']}"
        if parameters.get("kind") and parameters.get("name")
        else _NO_VALUE
    )
    return (spec.get("controller") or _NO_VALUE, reference)


def _network_policy_values(item: dict[str, Any]) -> tuple[str, ...]:
    spec = item.get("spec") or {}
    types = spec.get("policyTypes") or (
        ["Ingress", "Egress"] if spec.get("egress") else ["Ingress"]
    )
    return (_label_terms(spec.get("podSelector") or {}), ", ".join(types))


def _data_values(item: dict[str, Any]) -> tuple[str, ...]:
    return (str(len(item.get("data") or {}) + len(item.get("binaryData") or {})),)


def _secret_values(item: dict[str, Any]) -> tuple[str, ...]:
    return (item.get("type") or _NO_VALUE, *_data_values(item))


def _quantities(hard: dict[str, Any], used: dict[str, Any]) -> list[str]:
    return [f"{name}: {used.get(name, 0)}/{limit}" for name, limit in hard.items()]


def _resource_quota_values(item: dict[str, Any]) -> tuple[str, ...]:
    status = item.get("status") or {}
    hard = status.get("hard") or (item.get("spec") or {}).get("hard") or {}
    return (_listed(_quantities(hard, status.get("used") or {})),)


def _limit_range_values(item: dict[str, Any]) -> tuple[str, ...]:
    limits = (item.get("spec") or {}).get("limits") or []
    return (_listed([limit["type"] for limit in limits if limit.get("type")]),)


def _optional(value: Any) -> str:
    return _NO_VALUE if value is None else str(value)


def _autoscaler_values(item: dict[str, Any]) -> tuple[str, ...]:
    spec, status = item.get("spec") or {}, item.get("status") or {}
    target = spec.get("scaleTargetRef") or {}
    reference = (
        f"{target['kind']}/{target['name']}"
        if target.get("kind") and target.get("name")
        else _NO_VALUE
    )
    return (
        reference,
        str(spec.get("minReplicas") or 1),
        _optional(spec.get("maxReplicas")),
        _optional(status.get("currentReplicas")),
    )


def _disruption_budget_values(item: dict[str, Any]) -> tuple[str, ...]:
    spec, status = item.get("spec") or {}, item.get("status") or {}
    return (
        _optional(spec.get("minAvailable")),
        _optional(spec.get("maxUnavailable")),
        _optional(status.get("disruptionsAllowed")),
    )


def _priority_class_values(item: dict[str, Any]) -> tuple[str, ...]:
    return (
        _optional(item.get("value")),
        "true" if item.get("globalDefault") else "false",
    )


def _runtime_class_values(item: dict[str, Any]) -> tuple[str, ...]:
    return (item.get("handler") or _NO_VALUE,)


def _lease_values(item: dict[str, Any]) -> tuple[str, ...]:
    return ((item.get("spec") or {}).get("holderIdentity") or _NO_VALUE,)


def _webhook_values(item: dict[str, Any]) -> tuple[str, ...]:
    return (str(len(item.get("webhooks") or [])),)


_RESOURCE_VALUES = {
    "ConfigMap": _data_values,
    "Secret": _secret_values,
    "ResourceQuota": _resource_quota_values,
    "LimitRange": _limit_range_values,
    "HorizontalPodAutoscaler": _autoscaler_values,
    "PodDisruptionBudget": _disruption_budget_values,
    "PriorityClass": _priority_class_values,
    "RuntimeClass": _runtime_class_values,
    "Lease": _lease_values,
    "MutatingWebhookConfiguration": _webhook_values,
    "ValidatingWebhookConfiguration": _webhook_values,
    "Service": _service_values,
    "EndpointSlice": _endpoint_slice_values,
    "Endpoints": _endpoints_values,
    "Ingress": _ingress_values,
    "IngressClass": _ingress_class_values,
    "NetworkPolicy": _network_policy_values,
}


def _parse_resource(
    kind: str, item: dict[str, Any], now: datetime
) -> ClusterResource | None:
    metadata = item.get("metadata") or {}
    name = metadata.get("name")
    if not name:
        return None
    return ClusterResource(
        namespace=""
        if kind in _CLUSTER_WIDE
        else metadata.get("namespace") or "default",
        kind=kind,
        name=name,
        values=_RESOURCE_VALUES[kind](item),
        age=_item_age(item, now),
    )


# Ask for the metadata of a list only: the answer has the labels and nothing of
# the data of the objects.
_METADATA_ONLY = "application/json;as=PartialObjectMetadataList;g=meta.k8s.io;v=v1"
_HELM_SELECTOR = "owner=helm"


def _helm_revisions(
    context: str, namespace: str | None, name: str | None = None
) -> list[dict[str, Any]]:
    """The revisions of Helm releases, from the labels of the Secrets where
    Helm keeps them.

    Their contents are neither asked for nor read.
    """
    selector = _HELM_SELECTOR + (f",name={name}" if name else "")
    document = _get_json(
        _resource_path("secrets", namespace),
        context,
        [("labelSelector", selector)],
        _METADATA_ONLY,
    )
    revisions = []
    for item in document.get("items") or []:
        metadata = item.get("metadata") or {}
        labels = metadata.get("labels") or {}
        revision = str(labels.get("version") or "")
        if labels.get("name") and revision.isdigit():
            revisions.append(
                {
                    "name": labels["name"],
                    "namespace": metadata.get("namespace") or "default",
                    "revision": int(revision),
                    "status": labels.get("status") or _NO_VALUE,
                    "created": metadata.get("creationTimestamp"),
                }
            )
    return revisions


def _helm_releases(
    context: str, namespace: str | None, now: datetime
) -> list[ClusterResource]:
    """Each Helm release once, as its latest revision says."""
    releases: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for revision in _helm_revisions(context, namespace):
        releases.setdefault((revision["namespace"], revision["name"]), []).append(
            revision
        )
    rows = []
    for (release_namespace, name), revisions in releases.items():
        latest = max(revisions, key=lambda revision: revision["revision"])
        first = min(revisions, key=lambda revision: revision["revision"])
        rows.append(
            ClusterResource(
                namespace=release_namespace,
                kind="HelmRelease",
                name=name,
                values=(latest["status"], f"rev {latest['revision']}", "Helm"),
                age=_item_age(
                    {"metadata": {"creationTimestamp": first["created"]}}, now
                ),
            )
        )
    return rows


def _helm_release_details(context: str, namespace: str, name: str) -> dict[str, Any]:
    revisions = sorted(
        _helm_revisions(context, namespace, name), key=lambda r: r["revision"]
    )
    if not revisions:
        raise ClusterError(f"Helm release {name} was not found in {namespace}")
    latest = revisions[-1]
    return {
        "name": name,
        "namespace": namespace,
        "status": latest["status"],
        "revision": latest["revision"],
        "revisions": [
            {"revision": r["revision"], "status": r["status"], "created": r["created"]}
            for r in revisions
        ],
    }


def _eks_addons(context: str, now: datetime) -> list[ClusterResource]:
    if not is_eks_context(context):
        return []
    return [
        resource
        for item in _list_eks("Addon", context)
        if (resource := _parse_eks("Addon", item, now))
    ]


def _attempt(call: Any) -> tuple[list[ClusterResource], ClusterError | None]:
    try:
        return call(), None
    except ClusterError as error:
        return [], error


def _get_addons(
    context: str, namespace: str | None
) -> tuple[list[str], list[ClusterResource]]:
    """The add-ons of EKS and the Helm releases, in one list.

    One source failing does not hide the other; its error shows only
    when nothing else is listed.
    """
    now = datetime.now(UTC)
    namespaces, (eks, eks_error), (helm, helm_error) = _together(
        partial(_get_namespaces, context),
        partial(_attempt, partial(_eks_addons, context, now)),
        partial(_attempt, partial(_helm_releases, context, namespace, now)),
    )
    resources = [*eks, *helm]
    if not resources and (error := helm_error or eks_error):
        raise error
    resources.sort(key=lambda row: (row.name.casefold(), row.namespace))
    return namespaces, resources


def _get_eks(context: str, kind: str) -> tuple[list[str], list[ClusterResource]]:
    """Node Groups and Add-ons are not namespaced, so the answer has no
    namespaces."""
    now = datetime.now(UTC)
    resources = [
        resource
        for item in _list_eks(kind, context)
        if (resource := _parse_eks(kind, item, now))
    ]
    resources.sort(key=lambda row: row.name)
    return [], resources


def get_resources(
    context: str, namespace: str | None, kind: str
) -> tuple[list[str], list[ClusterResource]]:
    if kind == "Addon":
        return _get_addons(context, namespace)
    if kind in _EKS_KINDS:
        return _get_eks(context, kind)
    scope = None if kind in _CLUSTER_WIDE else namespace
    namespaces, document = _together(
        partial(_get_namespaces, context),
        partial(_list, _LISTED_RESOURCES[kind], context, scope),
    )
    now = datetime.now(UTC)
    resources = [
        resource
        for item in document.get("items", [])
        if (resource := _parse_resource(kind, item, now)) is not None
    ]
    resources.sort(key=lambda row: (row.namespace, row.name))
    return namespaces, resources


def get_pods(
    context: str,
    namespace: str | None = None,
) -> tuple[list[str], list[PodInfo]]:
    namespaces, pods = _together(
        partial(_get_namespaces, context),
        partial(_pods_with_usage, context, namespace),
    )
    pods.sort(key=lambda pod: (pod.namespace, pod.name))
    return namespaces, pods


def get_pod_logs(
    context: str,
    namespace: str,
    pod_name: str,
    container: str,
    tail_lines: int = 500,
) -> str:
    tail = min(max(tail_lines, 1), 500)
    path = f"{_resource_path('pods', namespace, pod_name)}/log"
    query = [("container", container), ("tailLines", str(tail)), ("timestamps", "true")]
    return _request(path, context, query, accept="application/json, */*").decode(
        errors="replace"
    )


_OVERVIEW_SECTIONS = {
    "nodes": "Nodes",
    "pods": "Pods",
    "namespaces": "Namespaces",
    "workloads": "Workloads",
}


def _item_age(item: dict[str, Any], now: datetime) -> str:
    created = (item.get("metadata") or {}).get("creationTimestamp")
    if not created:
        return "unknown"
    started = datetime.fromisoformat(created.replace("Z", "+00:00"))
    return format_age((now - started).total_seconds())


def _node_roles(labels: dict[str, str]) -> str:
    prefix = "node-role.kubernetes.io/"
    roles = sorted(key[len(prefix) :] for key in labels if key.startswith(prefix))
    return ", ".join(roles) or "—"


def _pod_requests(pod: dict[str, Any]) -> tuple[float, float]:
    cpu = memory = 0.0
    for container in (pod.get("spec") or {}).get("containers") or []:
        requests = (container.get("resources") or {}).get("requests") or {}
        cpu += parse_cpu(requests.get("cpu"))
        memory += parse_memory(requests.get("memory"))
    return cpu, memory


def _build_overview(
    results: dict[str, Any], errors: dict[str, str], now: datetime
) -> ClusterOverview:
    usage: dict[str, tuple[float, float]] = {}
    for item in (results.get("metrics") or {}).get("items", []):
        node_usage = item.get("usage") or {}
        usage[(item.get("metadata") or {}).get("name", "")] = (
            parse_cpu(node_usage.get("cpu")),
            parse_memory(node_usage.get("memory")),
        )

    running_on: dict[str, int] = {}
    requests_on: dict[str, tuple[float, float]] = {}
    phases = {"Running": 0, "Pending": 0, "Failed": 0}
    pod_items = (results.get("pods") or {}).get("items", [])
    for pod in pod_items:
        phase = (pod.get("status") or {}).get("phase")
        if phase in phases:
            phases[phase] += 1
        if phase in {"Succeeded", "Failed"}:
            continue
        node_name = (pod.get("spec") or {}).get("nodeName")
        if not node_name:
            continue
        running_on[node_name] = running_on.get(node_name, 0) + 1
        cpu, memory = _pod_requests(pod)
        old_cpu, old_memory = requests_on.get(node_name, (0.0, 0.0))
        requests_on[node_name] = (old_cpu + cpu, old_memory + memory)

    nodes = []
    for item in (results.get("nodes") or {}).get("items", []):
        metadata = item.get("metadata") or {}
        status = item.get("status") or {}
        name = metadata.get("name") or ""
        allocatable = status.get("allocatable") or {}
        ready = any(
            condition.get("type") == "Ready" and condition.get("status") == "True"
            for condition in status.get("conditions") or []
        )
        node_cpu, node_memory = usage.get(name, (None, None))
        requested_cpu, requested_memory = requests_on.get(name, (0.0, 0.0))
        nodes.append(
            NodeInfo(
                name=name,
                ready=ready,
                roles=_node_roles(metadata.get("labels") or {}),
                version=(status.get("nodeInfo") or {}).get("kubeletVersion", ""),
                age=_item_age(item, now),
                cpu_allocatable=parse_cpu(allocatable.get("cpu")),
                memory_allocatable=parse_memory(allocatable.get("memory")),
                pods_allocatable=int(allocatable.get("pods") or 0),
                pods_running=running_on.get(name, 0),
                cpu_requests=requested_cpu,
                memory_requests=requested_memory,
                cpu_usage=node_cpu,
                memory_usage=node_memory,
            )
        )
    nodes.sort(key=lambda node: node.name)

    kinds = {"Deployment": 0, "StatefulSet": 0, "DaemonSet": 0}
    for item in (results.get("workloads") or {}).get("items", []):
        if item.get("kind") in kinds:
            kinds[item["kind"]] += 1
    have_workloads = "workloads" in results
    have_pods = "pods" in results
    return ClusterOverview(
        nodes=tuple(nodes),
        namespaces=(
            len((results["namespaces"]).get("items", []))
            if "namespaces" in results
            else None
        ),
        deployments=kinds["Deployment"] if have_workloads else None,
        statefulsets=kinds["StatefulSet"] if have_workloads else None,
        daemonsets=kinds["DaemonSet"] if have_workloads else None,
        pods_total=len(pod_items) if have_pods else None,
        pods_running=phases["Running"] if have_pods else None,
        pods_pending=phases["Pending"] if have_pods else None,
        pods_failed=phases["Failed"] if have_pods else None,
        metrics_available="metrics" in results,
        warnings=tuple(
            f"{label}: {errors[key]}"
            for key, label in _OVERVIEW_SECTIONS.items()
            if key in errors
        ),
    )


def get_cluster_overview(context: str) -> ClusterOverview:
    """Collect cluster-wide totals; sections the user cannot read become
    warnings."""
    tasks = {
        "nodes": partial(_list, "nodes", context),
        "pods": partial(_list, "pods", context),
        "namespaces": partial(_list, "namespaces", context),
        "workloads": partial(_list_kinds, _REPLICATED_KINDS, context, None),
        "metrics": partial(_get_json, f"{_METRICS_PATH}/nodes", context),
    }
    results: dict[str, Any] = {}
    errors: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = {name: pool.submit(task) for name, task in tasks.items()}
        for name, future in futures.items():
            try:
                results[name] = future.result()
            except ClusterError as error:
                errors[name] = str(error)
    if not any(key in results for key in _OVERVIEW_SECTIONS):
        raise ClusterError(next(iter(errors.values()), "No data returned"))
    for name, reason in errors.items():
        logger.info("Overview section %s unavailable: %s", name, first_line(reason))
    errors.pop("metrics", None)
    return _build_overview(results, errors, datetime.now(UTC))


OVERVIEW_KINDS = (
    "Pod",
    "Deployment",
    "DaemonSet",
    "StatefulSet",
    "ReplicaSet",
    "Job",
    "CronJob",
)
EVENT_LIMIT = 200  # the most recent events are the useful ones


def _summarize_workloads(items: list[dict[str, Any]], now: datetime) -> KindSummary:
    counts = {"ok": 0, "warning": 0, "bad": 0}
    total = 0
    for item in items:
        workload = _parse_workload(item, now)
        if workload is None:
            continue
        total += 1
        if workload.status in OK_STATUSES:
            counts["ok"] += 1
        elif workload.status in WARNING_STATUSES:
            counts["warning"] += 1
        elif workload.status in BAD_STATUSES:
            counts["bad"] += 1
    return KindSummary(total, **counts)


def _summarize_pods(items: list[dict[str, Any]], now: datetime) -> KindSummary:
    counts = {"ok": 0, "warning": 0, "bad": 0}
    total = 0
    for item in items:
        pod = _parse_pod(item, now)
        if pod is None:
            continue
        total += 1
        if pod.phase == "Succeeded" or (
            pod.phase == "Running" and pod.ready >= pod.total
        ):
            counts["ok"] += 1
        elif pod.phase in {"Pending", "Running"}:
            counts["warning"] += 1
        else:
            counts["bad"] += 1
    return KindSummary(total, **counts)


def _seconds_since(timestamp: str | None, now: datetime) -> float | None:
    if not timestamp:
        return None
    return (
        now - datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    ).total_seconds()


def _parse_event(item: dict[str, Any], now: datetime) -> tuple[float, EventInfo] | None:
    """An event and how long ago it was last seen, for ordering."""
    metadata = item.get("metadata") or {}
    involved = item.get("involvedObject") or {}
    message = item.get("message")
    if not message:
        return None
    series = item.get("series") or {}
    last_seen = _seconds_since(
        item.get("lastTimestamp")
        or series.get("lastObservedTime")
        or item.get("eventTime")
        or metadata.get("creationTimestamp"),
        now,
    )
    created = _seconds_since(metadata.get("creationTimestamp"), now)
    source = (item.get("source") or {}).get("component") or item.get(
        "reportingComponent"
    )
    return (
        last_seen if last_seen is not None else float("inf"),
        EventInfo(
            type=item.get("type") or "Normal",
            source=source or "",
            namespace=metadata.get("namespace") or involved.get("namespace") or "",
            involved=f"{involved.get('kind') or '?'}: {involved.get('name') or '?'}",
            message=message,
            count=item.get("count") or series.get("count") or 1,
            age=format_age(created) if created is not None else "unknown",
            last_seen=format_age(last_seen) if last_seen is not None else "unknown",
        ),
    )


def get_workloads_overview(context: str) -> WorkloadsOverview:
    """Count every workload kind by health and list the latest events.

    A section the user cannot read is reported instead of failing the
    page.
    """
    tasks = {
        kind: partial(_list, _RESOURCES.get(kind, "pods"), context)
        for kind in OVERVIEW_KINDS
    }
    tasks["Event"] = partial(_list, "events", context)
    results: dict[str, Any] = {}
    errors: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
        futures = {name: pool.submit(task) for name, task in tasks.items()}
        for name, future in futures.items():
            try:
                results[name] = future.result()
            except ClusterError as error:
                errors[name] = str(error)
    if not results:
        raise ClusterError(next(iter(errors.values()), "No data returned"))
    for name, reason in errors.items():
        logger.info("Workloads overview: %s unavailable: %s", name, first_line(reason))

    now = datetime.now(UTC)
    kinds = {
        kind: (_summarize_pods if kind == "Pod" else _summarize_workloads)(
            results[kind].get("items") or [], now
        )
        for kind in OVERVIEW_KINDS
        if kind in results
    }
    events = sorted(
        (
            parsed
            for item in (results.get("Event") or {}).get("items") or []
            if (parsed := _parse_event(item, now)) is not None
        ),
        key=lambda pair: pair[0],
    )[:EVENT_LIMIT]
    return WorkloadsOverview(
        kinds=kinds,
        events=tuple(event for _seen, event in events),
        unreadable=tuple(errors),
    )
