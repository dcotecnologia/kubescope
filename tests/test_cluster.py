import io
import json
import os
import sys
import threading
import time
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import SimpleNamespace

import pytest

from kubescope import cluster
from kubescope.models import PodInfo, Workload


def test_parse_deployment_workload() -> None:
    workload = cluster._parse_workload(
        {
            "kind": "Deployment",
            "metadata": {
                "name": "api",
                "namespace": "production",
                "creationTimestamp": "2025-01-01T00:00:00Z",
            },
            "spec": {"replicas": 3},
            "status": {"readyReplicas": 2},
        },
        datetime(2025, 1, 1, 0, 2, tzinfo=UTC),
    )

    assert workload is not None
    assert (workload.namespace, workload.kind, workload.name) == (
        "production",
        "Deployment",
        "api",
    )
    assert (workload.ready, workload.desired, workload.age, workload.status) == (
        2,
        3,
        "2m",
        "Degraded",
    )


def test_get_workloads_lists_namespaces_and_every_default_kind(monkeypatch) -> None:
    daemon_set = {
        "metadata": {"name": "agent", "namespace": "default"},
        "status": {"desiredNumberScheduled": 2, "numberReady": 2},
    }
    documents = {
        "/api/v1/namespaces": {"items": [{"metadata": {"name": "default"}}]},
        "/apis/apps/v1/deployments": {"items": []},
        "/apis/apps/v1/statefulsets": {"items": []},
        "/apis/apps/v1/daemonsets": {"items": [daemon_set]},
    }
    paths = []

    def fake_get_json(path: str, context: str, query=None) -> dict:
        paths.append((path, context, query))
        return documents[path]

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    namespaces, workloads = cluster.get_workloads("dev")

    assert namespaces == ["default"]
    assert [(w.kind, w.name) for w in workloads] == [("DaemonSet", "agent")]
    assert sorted(paths) == sorted((path, "dev", []) for path in documents)


def test_get_workload_pods_uses_workload_label_selector(monkeypatch) -> None:
    responses = iter(
        [
            {
                "spec": {
                    "selector": {
                        "matchLabels": {"app": "api"},
                        "matchExpressions": [
                            {
                                "key": "tier",
                                "operator": "In",
                                "values": ["backend", "worker"],
                            }
                        ],
                    }
                }
            },
            {
                "items": [
                    {
                        "kind": "Pod",
                        "metadata": {"name": "api-abc", "namespace": "production"},
                        "spec": {"containers": [{"name": "api"}]},
                        "status": {
                            "phase": "Running",
                            "containerStatuses": [{"ready": True}],
                        },
                    }
                ]
            },
        ]
    )
    commands = []

    def fake_get_json(path: str, context: str, query=None) -> dict:
        commands.append((path, context, query))
        return next(responses)

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)
    workload = cluster.Workload("production", "Deployment", "api", 1, 1, "1h")

    pods = cluster.get_workload_pods("dev", workload)

    assert [
        (pod.name, pod.phase, pod.ready, pod.total, pod.containers) for pod in pods
    ] == [("api-abc", "Running", 1, 1, ("api",))]
    assert commands == [
        ("/apis/apps/v1/namespaces/production/deployments/api", "dev", None),
        (
            "/api/v1/namespaces/production/pods",
            "dev",
            [("labelSelector", "app=api,tier in (backend,worker)")],
        ),
    ]


def test_get_resource_details_returns_json_document(monkeypatch) -> None:
    expected = {"kind": "Deployment", "metadata": {"name": "api"}}
    commands = []

    def fake_get_json(path: str, context: str, query=None) -> dict:
        commands.append((path, context))
        return expected

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    result = cluster.get_resource_details("dev", "Deployment", "production", "api")

    assert result == expected
    assert commands == [("/apis/apps/v1/namespaces/production/deployments/api", "dev")]


def test_get_pod_logs_selects_container_and_caps_lines(monkeypatch) -> None:
    requests = []

    def fake_request(path, context, query=None, accept="application/json"):
        requests.append((path, context, query, accept))
        return "2026-10-08T00:00:00Z started ✓".encode()

    monkeypatch.setattr(cluster, "_request", fake_request)

    logs = cluster.get_pod_logs("dev", "production", "api-abc", "api", tail_lines=900)

    assert logs == "2026-10-08T00:00:00Z started ✓"
    assert requests == [
        (
            "/api/v1/namespaces/production/pods/api-abc/log",
            "dev",
            [("container", "api"), ("tailLines", "500"), ("timestamps", "true")],
            "application/json, */*",
        )
    ]


def _node(name: str, ready: str = "True", role: str | None = None) -> dict:
    labels = {f"node-role.kubernetes.io/{role}": ""} if role else {}
    return {
        "metadata": {
            "name": name,
            "labels": labels,
            "creationTimestamp": "2025-01-01T00:00:00Z",
        },
        "status": {
            "conditions": [{"type": "Ready", "status": ready}],
            "allocatable": {"cpu": "3920m", "memory": "7Gi", "pods": "58"},
            "nodeInfo": {"kubeletVersion": "v1.30.0"},
        },
    }


def _pod(node: str, phase: str, cpu: str = "500m", memory: str = "1Gi") -> dict:
    return {
        "spec": {
            "nodeName": node,
            "containers": [{"resources": {"requests": {"cpu": cpu, "memory": memory}}}],
        },
        "status": {"phase": phase},
    }


def test_build_overview_aggregates_nodes_pods_and_usage() -> None:
    results = {
        "nodes": {"items": [_node("b", role="worker"), _node("a", "False")]},
        "pods": {
            "items": [
                _pod("a", "Running"),
                _pod("a", "Running", "250m", "512Mi"),
                _pod("b", "Pending"),
                _pod("b", "Succeeded"),
                _pod("b", "Failed"),
            ]
        },
        "namespaces": {"items": [{}, {}, {}]},
        "workloads": {
            "items": [
                {"kind": "Deployment"},
                {"kind": "Deployment"},
                {"kind": "DaemonSet"},
            ]
        },
        "metrics": {
            "items": [
                {
                    "metadata": {"name": "a"},
                    "usage": {"cpu": "1000000000n", "memory": "2Gi"},
                }
            ]
        },
    }

    overview = cluster._build_overview(
        results, {"x": "ignored"}, datetime(2025, 1, 2, tzinfo=UTC)
    )

    assert [node.name for node in overview.nodes] == ["a", "b"]
    assert (overview.nodes_ready, overview.pods_capacity) == (1, 116)
    assert overview.nodes[0].roles == "—" and overview.nodes[1].roles == "worker"
    assert overview.nodes[0].age == "1d"
    assert overview.nodes[0].pods_running == 2
    assert overview.nodes[0].cpu_requests == 0.75
    assert overview.nodes[1].pods_running == 1  # Succeeded/Failed pods are skipped
    assert (overview.pods_total, overview.pods_running) == (5, 2)
    assert (overview.pods_pending, overview.pods_failed) == (1, 1)
    assert (overview.namespaces, overview.deployments, overview.daemonsets) == (3, 2, 1)
    assert overview.statefulsets == 0
    assert overview.metrics_available is True
    assert overview.cpu_usage == 1.0
    assert overview.memory_usage == 2 * 2**30


def test_get_cluster_overview_reports_unreadable_sections(monkeypatch) -> None:
    def fake_get_json(path: str, context: str, query=None) -> dict:
        if path == "/api/v1/nodes":
            raise cluster.ClusterError("forbidden")
        if "metrics" in path:
            raise cluster.ClusterError("no metrics")
        return {"items": []}

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    overview = cluster.get_cluster_overview("ctx")

    assert overview.warnings == ("Nodes: forbidden",)
    assert overview.metrics_available is False
    assert overview.nodes == ()
    assert overview.pods_total == 0


def test_get_cluster_overview_fails_when_nothing_is_readable(monkeypatch) -> None:
    def fail(*_args: object, **_kwargs: object) -> dict:
        raise cluster.ClusterError("unreachable")

    monkeypatch.setattr(cluster, "_get_json", fail)

    try:
        cluster.get_cluster_overview("ctx")
    except cluster.ClusterError as error:
        assert "unreachable" in str(error)
    else:
        raise AssertionError("expected ClusterError")


def test_get_pods_and_usage_include_metrics_restarts_and_owner(monkeypatch) -> None:
    pod = {
        "metadata": {
            "name": "api-5f7d9c-abcde",
            "namespace": "default",
            "ownerReferences": [{"kind": "ReplicaSet", "name": "api-5f7d9c"}],
        },
        "spec": {"containers": [{"name": "app"}]},
        "status": {
            "phase": "Running",
            "containerStatuses": [{"ready": True, "restartCount": 3}],
        },
    }
    metrics = {
        "items": [
            {
                "metadata": {"name": "api-5f7d9c-abcde", "namespace": "default"},
                "containers": [{"usage": {"cpu": "250m", "memory": "128Mi"}}],
            }
        ]
    }

    def fake_get_json(path: str, context: str, query=None) -> dict:
        if "metrics" in path:
            return metrics
        return {"items": [pod]} if path.endswith("/pods") else {"items": []}

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    _, pods = cluster.get_pods("dev")
    assert (pods[0].restarts, pods[0].cpu, pods[0].memory) == (3, 0.25, 128 * 2**20)
    assert pods[0].owner == ("Deployment", "api")
    usage = cluster.get_usage("dev")
    assert usage[("default", "Deployment", "api")] == (3, 0.25, 128 * 2**20)

    def no_metrics(path: str, context: str, query=None) -> dict:
        if "metrics" in path:
            raise cluster.ClusterError("no metrics")
        return {"items": [pod]} if path.endswith("/pods") else {"items": []}

    monkeypatch.setattr(cluster, "_get_json", no_metrics)
    assert cluster.get_pods("dev")[1][0].cpu is None


class FakeCluster:
    """A local HTTP server standing in for a cluster, and a kubeconfig that
    points at it."""

    def __init__(self, monkeypatch, tmp_path) -> None:
        self.routes: dict[str, tuple[int, bytes]] = {}
        self.requests: list[tuple[str, str | None]] = []
        self.accept_token: str | None = None  # refuse any other token with a 401
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                outer.requests.append((self.path, self.headers.get("Authorization")))
                status, body = outer.routes.get(self.path, (404, b"{}"))
                token = self.headers.get("Authorization")
                if outer.accept_token and token != outer.accept_token:
                    status, body = 401, b'{"message": "Unauthorized"}'
                self.send_response(status)
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args: object) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        self.kubeconfig = tmp_path / "kubeconfig"
        self.write_kubeconfig()
        monkeypatch.setenv("KUBECONFIG", str(self.kubeconfig))
        monkeypatch.setenv("NO_PROXY", "127.0.0.1")

    def write_kubeconfig(self, server: str | None = None, user: dict | None = None):
        document = {
            "current-context": "dev",
            "contexts": [{"name": "dev", "context": {"cluster": "c", "user": "u"}}],
            "clusters": [{"name": "c", "cluster": {"server": server or self.url}}],
            "users": [{"name": "u", "user": user or {"token": "fake-token"}}],
        }
        self.kubeconfig.write_text(json.dumps(document))  # JSON is valid YAML

    def serve(self, path: str, body: dict | str, status: int = 200) -> None:
        raw = body if isinstance(body, str) else json.dumps(body)
        self.routes[path] = (status, raw.encode())


@pytest.fixture
def fake_cluster(monkeypatch, tmp_path):
    fake = FakeCluster(monkeypatch, tmp_path)
    yield fake
    fake.server.shutdown()
    fake.server.server_close()


def test_request_sends_the_token_and_returns_the_body(fake_cluster) -> None:
    fake_cluster.serve("/version", {"gitVersion": "v1.30.0"})
    fake_cluster.serve("/api/v1/namespaces/ops/pods?labelSelector=app%3Dapi", "ok")

    assert json.loads(cluster._request("/version", "dev")) == {"gitVersion": "v1.30.0"}
    body = cluster._request(
        "/api/v1/namespaces/ops/pods", "dev", [("labelSelector", "app=api")]
    )

    assert body == b"ok"
    assert fake_cluster.requests == [
        ("/version", "Bearer fake-token"),
        ("/api/v1/namespaces/ops/pods?labelSelector=app%3Dapi", "Bearer fake-token"),
    ]


def test_request_never_writes_the_kubeconfig_back(monkeypatch, fake_cluster) -> None:
    seen = {}
    real = cluster.config.new_client_from_config

    def spy(**kwargs):
        seen.update(kwargs)
        return real(**kwargs)

    monkeypatch.setattr(cluster.config, "new_client_from_config", spy)
    fake_cluster.serve("/version", {})
    before = fake_cluster.kubeconfig.read_bytes()

    cluster._request("/version", "dev")

    assert seen["persist_config"] is False and seen["context"] == "dev"
    assert fake_cluster.kubeconfig.read_bytes() == before


def test_request_explains_a_refusal_like_kubectl_does(fake_cluster) -> None:
    message = 'pods is forbidden: User "me" cannot list resource "pods"'
    fake_cluster.serve("/forbidden", {"kind": "Status", "message": message}, 403)
    fake_cluster.serve("/plain", "oops", 500)
    fake_cluster.serve("/list", [1], 502)

    with pytest.raises(cluster.ClusterError) as refused:
        cluster._request("/forbidden", "dev")
    assert str(refused.value) == message
    with pytest.raises(cluster.ClusterError, match="500 Internal Server Error"):
        cluster._request("/plain", "dev")
    with pytest.raises(cluster.ClusterError, match="502 Bad Gateway"):
        cluster._request("/list", "dev")
    with pytest.raises(cluster.ClusterError, match="404 Not Found"):
        cluster._request("/missing", "dev")


def test_request_reports_a_cluster_that_cannot_be_reached(fake_cluster) -> None:
    fake_cluster.server.shutdown()
    fake_cluster.server.server_close()

    with pytest.raises(cluster.ClusterError, match="(?i)refused|failed to establish"):
        cluster._request("/version", "dev")


def test_request_reports_a_failed_tls_handshake(fake_cluster) -> None:
    fake_cluster.write_kubeconfig(server=fake_cluster.url.replace("http", "https"))

    with pytest.raises(cluster.ClusterError, match="(?i)ssl|tls|certificate"):
        cluster._request("/version", "dev")


def test_request_reports_a_tls_error_raised_by_the_client(monkeypatch) -> None:
    def failing(_api, *_a, **_k):
        raise cluster.ApiException(status=0, reason="SSLError handshake")

    monkeypatch.setattr(cluster.client.ApiClient, "call_api", failing)
    monkeypatch.setattr(cluster, "_api_client", lambda _c: cluster.client.ApiClient())

    with pytest.raises(cluster.ClusterError, match="SSLError handshake"):
        cluster._request("/version", "dev")


def test_request_gives_up_when_the_cluster_does_not_answer(monkeypatch) -> None:
    release = threading.Event()
    monkeypatch.setattr(cluster, "REQUEST_TIMEOUT", 0.1)
    monkeypatch.setattr(cluster, "_fetch", lambda *_a: release.wait(5))

    with pytest.raises(cluster.ClusterError, match="timed out"):
        cluster._request("/version", "dev")
    release.set()


def test_cancel_running_stops_a_request_at_once(monkeypatch) -> None:
    started, release = threading.Event(), threading.Event()

    def slow(*_a):
        started.set()
        release.wait(5)
        return b"late"

    monkeypatch.setattr(cluster, "_fetch", slow)
    outcome: list[BaseException] = []

    def call() -> None:
        try:
            cluster._request("/version", "dev")
        except cluster.ClusterError as error:
            outcome.append(error)

    thread = threading.Thread(target=call)
    thread.start()
    assert started.wait(5)

    cluster.cancel_running()
    thread.join(5)
    release.set()  # the late answer is dropped without a trace

    assert [str(error) for error in outcome] == ["The request was cancelled"]
    assert not cluster._pending


def test_get_json_rejects_documents_that_are_not_objects(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_request", lambda *_a, **_k: b'{"a": 1}')
    assert cluster._get_json("/x", "c") == {"a": 1}

    monkeypatch.setattr(cluster, "_request", lambda *_a, **_k: b"[1]")
    with pytest.raises(cluster.ClusterError, match="unexpected JSON"):
        cluster._get_json("/x", "c")

    monkeypatch.setattr(cluster, "_request", lambda *_a, **_k: b"<html>")
    with pytest.raises(cluster.ClusterError, match="unexpected response"):
        cluster._get_json("/x", "c")


def test_list_adds_the_kind_the_cluster_leaves_out_of_a_list(monkeypatch) -> None:
    monkeypatch.setattr(
        cluster, "_get_json", lambda *_a: {"items": [{"metadata": {"name": "a"}}, {}]}
    )

    items = cluster._list("deployments", "dev")["items"]

    assert [item["kind"] for item in items] == ["Deployment", "Deployment"]
    monkeypatch.setattr(cluster, "_get_json", lambda *_a: {})  # a list without items
    assert cluster._list("pods", "dev") == {}


def test_resource_paths_encode_the_names_that_come_from_the_cluster() -> None:
    assert cluster._resource_path("nodes") == "/api/v1/nodes"
    assert (
        cluster._resource_path("deployments", "a/b", "x?y")
        == "/apis/apps/v1/namespaces/a%2Fb/deployments/x%3Fy"
    )


def test_a_context_that_is_not_in_the_kubeconfig_is_named(fake_cluster) -> None:
    with pytest.raises(cluster.ClusterError, match="context was not found.*nope"):
        cluster._request("/version", "nope")


def test_a_sign_in_program_that_is_not_installed_is_named(fake_cluster) -> None:
    exec_block = {
        "apiVersion": "client.authentication.k8s.io/v1",
        "command": "kubescope-no-such-login-tool",
    }
    fake_cluster.write_kubeconfig(user={"exec": exec_block})

    with pytest.raises(
        cluster.ClusterError, match="executable kubescope-no-such-login-tool not found"
    ):
        cluster._request("/version", "dev")


def test_a_sign_in_program_that_fails_reports_what_it_printed(
    fake_cluster, monkeypatch
) -> None:
    # the client lets an interactive sign-in print to the terminal; the pytest
    # option -s leaves stdout on a real terminal, so make it a plain stream
    monkeypatch.setattr(sys, "stdout", io.StringIO())
    exec_block = {
        "apiVersion": "client.authentication.k8s.io/v1",
        "command": sys.executable,
        "args": [
            "-c",
            "import sys; sys.stderr.write('Token has expired'); sys.exit(3)",
        ],
    }
    fake_cluster.write_kubeconfig(user={"exec": exec_block})

    with pytest.raises(cluster.ClusterError, match="returned 3.*Token has expired"):
        cluster._request("/version", "dev")


def test_sign_in_failures_are_worded_for_the_error_dialog() -> None:
    posix = "[Errno 2] No such file or directory: 'aws'"
    windows = "exec: process returned 1. 'aws' is not recognized as a command"

    assert cluster._sign_in_failure(posix) == "exec: executable aws not found"
    assert cluster._sign_in_failure(windows) == "exec: executable aws not found"
    terminal = cluster._sign_in_failure("'NoneType' object has no attribute 'strip'")
    assert "credentials may have expired" in terminal
    assert cluster.is_auth_error(terminal)
    assert cluster._sign_in_failure("exec: process returned 3.") == (
        "exec: process returned 3."
    )


def test_a_sign_in_that_returns_no_credentials_is_reported(fake_cluster) -> None:
    document = {"apiVersion": "v1", "kind": "X", "status": {}}
    script = f"print({json.dumps(document)!r})"
    exec_block = {"apiVersion": "v1", "command": sys.executable, "args": ["-c", script]}
    fake_cluster.write_kubeconfig(user={"exec": exec_block})

    with pytest.raises(cluster.ClusterError, match="missing token"):
        cluster._request("/version", "dev")


def test_a_kubeconfig_that_cannot_be_read_is_reported(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("KUBECONFIG", str(tmp_path))  # a folder, not a file

    with pytest.raises(cluster.ClusterError, match="Could not read the kubeconfig"):
        cluster._request("/version", "dev")
    with pytest.raises(cluster.ClusterError, match="Could not read the kubeconfig"):
        cluster.list_contexts()

    nameless = tmp_path / "nameless"
    nameless.write_text(json.dumps({"contexts": [{"context": {}}, {"name": "x"}]}))
    monkeypatch.setenv("KUBECONFIG", str(nameless))
    with pytest.raises(cluster.ClusterError, match="Could not read the kubeconfig"):
        cluster.list_contexts()

    empty = tmp_path / "empty"
    empty.write_text("")
    monkeypatch.setenv("KUBECONFIG", str(empty))
    with pytest.raises(cluster.ClusterError, match="empty"):
        cluster.list_contexts()
    with pytest.raises(cluster.ClusterError, match="empty"):
        cluster._request("/version", "dev")


def test_list_contexts_merges_the_kubeconfig_files(monkeypatch, tmp_path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    first.write_text(
        json.dumps(
            {
                "current-context": "b",
                "contexts": [{"name": "b", "context": {}}, {"name": "a"}],
            }
        )
    )
    second.write_text(json.dumps({"contexts": [{"name": "c"}, {"name": "b"}]}))
    monkeypatch.setenv("KUBECONFIG", f"{first}{os.pathsep}{second}")

    assert cluster.list_contexts() == (["a", "b", "c"], "b")

    first.write_text(json.dumps({"current-context": "gone", "contexts": []}))
    assert cluster.list_contexts() == (["c", "b"][::-1], None)


def test_list_contexts_without_a_kubeconfig_finds_nothing(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("KUBECONFIG", str(tmp_path / "missing"))
    assert cluster.list_contexts() == ([], None)

    monkeypatch.delenv("KUBECONFIG")
    assert cluster._kubeconfig_paths() == "~/.kube/config"


def test_parse_workload_skips_unknown_kinds_and_handles_daemon_sets() -> None:
    now = datetime(2025, 1, 1, tzinfo=UTC)

    assert (
        cluster._parse_workload({"kind": "Ingress", "metadata": {"name": "x"}}, now)
        is None
    )
    assert cluster._parse_workload({"kind": "Deployment", "metadata": {}}, now) is None
    daemon = cluster._parse_workload(
        {
            "kind": "DaemonSet",
            "metadata": {"name": "agent"},
            "status": {"desiredNumberScheduled": 4, "numberReady": 3},
        },
        now,
    )
    assert daemon is not None
    assert (daemon.ready, daemon.desired, daemon.age) == (3, 4, "unknown")


def test_parse_workload_reads_replication_controllers_like_replica_sets() -> None:
    now = datetime(2025, 1, 1, tzinfo=UTC)

    controller = cluster._parse_workload(
        {
            "kind": "ReplicationController",
            "metadata": {"name": "legacy", "namespace": "ns"},
            "spec": {"replicas": 3},
            "status": {"readyReplicas": 2},
        },
        now,
    )

    assert controller is not None
    assert (controller.kind, controller.ready, controller.desired) == (
        "ReplicationController",
        2,
        3,
    )
    assert cluster._RESOURCES["ReplicationController"] == "replicationcontrollers"


def test_label_selector_reads_a_replication_controllers_plain_map() -> None:
    resource = {"spec": {"selector": {"tier": "web", "app": "legacy"}}}

    assert cluster._label_selector(resource) == "app=legacy,tier=web"


def test_get_resource_details_rejects_unsupported_kinds() -> None:
    with pytest.raises(cluster.ClusterError, match="Unsupported resource kind"):
        cluster.get_resource_details("c", "CustomResourceDefinition", "ns", "x")


def test_label_selector_supports_every_expression_operator() -> None:
    resource = {
        "spec": {
            "selector": {
                "matchLabels": {"b": "2", "a": "1"},
                "matchExpressions": [
                    {"key": "tier", "operator": "In", "values": ["x", "y"]},
                    {"key": "env", "operator": "NotIn", "values": ["dev"]},
                    {"key": "canary", "operator": "Exists"},
                    {"key": "legacy", "operator": "DoesNotExist"},
                ],
            }
        }
    }

    assert cluster._label_selector(resource) == (
        "a=1,b=2,tier in (x,y),env notin (dev),canary,!legacy"
    )


@pytest.mark.parametrize(
    ("selector", "message"),
    [
        ({"matchExpressions": [{"operator": "Exists"}]}, "without a key"),
        (
            {"matchExpressions": [{"key": "k", "operator": "In", "values": []}]},
            "requires values",
        ),
        (
            {"matchExpressions": [{"key": "k", "operator": "Gt", "values": ["1"]}]},
            "Unsupported workload selector operator",
        ),
        ({}, "no label selector"),
    ],
)
def test_label_selector_rejects_unusable_selectors(selector, message) -> None:
    with pytest.raises(cluster.ClusterError, match=message):
        cluster._label_selector({"spec": {"selector": selector}})


def test_parse_pod_handles_missing_names_and_ages() -> None:
    now = datetime(2025, 1, 1, 1, tzinfo=UTC)

    assert cluster._parse_pod({"metadata": {}}, now) is None
    pod = cluster._parse_pod(
        {
            "metadata": {
                "name": "web",
                "creationTimestamp": "2025-01-01T00:00:00Z",
            },
            "spec": {"containers": [{"name": "app"}, {}]},
        },
        now,
    )
    assert pod is not None
    assert (pod.age, pod.containers, pod.phase, pod.namespace) == (
        "1h",
        ("app",),
        "Unknown",
        "default",
    )


def test_parse_pod_lists_init_containers() -> None:
    now = datetime(2025, 1, 1, 1, tzinfo=UTC)
    pod = cluster._parse_pod(
        {
            "metadata": {"name": "web"},
            "spec": {
                "initContainers": [{"name": "migrate"}, {}],
                "containers": [{"name": "app"}],
            },
        },
        now,
    )
    assert pod is not None
    assert (pod.init_containers, pod.containers, pod.total) == (
        ("migrate",),
        ("app",),
        1,
    )


def test_pod_owner_prefers_controllers_and_maps_replica_sets() -> None:
    owner = cluster._pod_owner
    assert owner({}) is None
    assert owner({"ownerReferences": [{"kind": "Node"}]}) is None
    assert owner(
        {
            "ownerReferences": [
                {"kind": "Job", "name": "j", "controller": False},
                {"kind": "ReplicaSet", "name": "api-7d9f"},
            ]
        }
    ) == ("Deployment", "api")
    assert owner({"ownerReferences": [{"kind": "StatefulSet", "name": "db"}]}) == (
        "StatefulSet",
        "db",
    )


def test_item_age_is_unknown_without_a_timestamp() -> None:
    now = datetime(2025, 1, 1, tzinfo=UTC)
    assert cluster._item_age({}, now) == "unknown"


def test_build_overview_ignores_pods_not_scheduled_on_a_node() -> None:
    now = datetime(2025, 1, 1, tzinfo=UTC)
    results = {
        "nodes": {"items": [_node("a")]},
        "pods": {"items": [{"status": {"phase": "Pending"}}, _pod("a", "Running")]},
    }

    overview = cluster._build_overview(results, {}, now)

    assert overview.nodes[0].pods_running == 1


def test_get_usage_skips_pods_without_a_controlling_workload(monkeypatch) -> None:
    owned = PodInfo(
        "ns",
        "api-1",
        "Running",
        1,
        1,
        "1h",
        ("c",),
        2,
        0.5,
        100.0,
        ("Deployment", "api"),
    )
    orphan = PodInfo("ns", "solo", "Running", 1, 1, "1h", ("c",))
    monkeypatch.setattr(cluster, "_pods_with_usage", lambda *_a: [owned, orphan])

    assert cluster.get_usage("ctx") == {
        ("ns", "Deployment", "api"): (2, 0.5, 100.0),
        ("ns", "ReplicaSet", "api"): (2, 0.5, 100.0),  # the ReplicaSet row too
    }


def test_get_usage_adds_up_a_replica_sets_pods_without_metrics(monkeypatch) -> None:
    pods = [
        PodInfo("ns", f"api-6d4cf-{n}", "Running", 1, 1, "1h", ("c",), 1, owner=owner)
        for n, owner in (("a", ("Deployment", "api")), ("b", ("Deployment", "api")))
    ]
    monkeypatch.setattr(cluster, "_pods_with_usage", lambda *_a: pods)

    usage = cluster.get_usage("ctx")

    assert usage[("ns", "ReplicaSet", "api-6d4cf")] == (2, None, None)


def _aws_kubeconfig(arguments=None, env=None, command="/usr/local/bin/aws") -> dict:
    exec_block = {"command": command, "args": arguments or [], "env": env}
    return {
        "contexts": [
            {"name": "other", "context": {"user": "nobody"}},
            {"name": "ctx", "context": {"user": "me"}},
        ],
        "users": [{"name": "me", "user": {"exec": exec_block}}],
    }


def test_run_command_returns_output_and_reports_failures(monkeypatch) -> None:
    def completed(returncode, stdout="", stderr=""):
        return lambda command, **_kw: cluster.subprocess.CompletedProcess(
            command, returncode, stdout, stderr
        )

    monkeypatch.setattr(cluster, "_run_process", completed(0, "out"))
    assert cluster._run_command(["aws", "x"], 5) == "out"

    for run, message in (
        (completed(1, "", "bad credentials"), "bad credentials"),
        (completed(1, "from stdout", ""), "from stdout"),
        (completed(2), "exited with 2"),
    ):
        monkeypatch.setattr(cluster, "_run_process", run)
        with pytest.raises(cluster.ClusterError, match=message):
            cluster._run_command(["aws", "x"], 5)

    def timeout(command, **_kwargs):
        raise cluster.subprocess.TimeoutExpired(command, 5)

    def missing(_command, **_kwargs):
        raise OSError("not found")

    monkeypatch.setattr(cluster, "_run_process", timeout)
    with pytest.raises(cluster.ClusterError, match="timed out"):
        cluster._run_command(["aws"], 5)
    monkeypatch.setattr(cluster, "_run_process", missing)
    with pytest.raises(cluster.ClusterError, match="Could not start aws"):
        cluster._run_command(["aws"], 5)


def test_aws_profile_is_read_from_the_kubeconfig_exec_entry(monkeypatch) -> None:
    def config(document):
        monkeypatch.setattr(cluster, "_kubeconfig", lambda: document)

    config(_aws_kubeconfig(["eks", "get-token", "--profile", "work"]))
    assert cluster._aws_profile("ctx") == (True, "work")

    config(_aws_kubeconfig(env=[{"name": "AWS_PROFILE", "value": "env-profile"}]))
    assert cluster._aws_profile("ctx") == (True, "env-profile")

    config(
        _aws_kubeconfig(["--profile", "arg"], [{"name": "AWS_PROFILE", "value": "x"}])
    )
    assert cluster._aws_profile("ctx") == (True, "arg")

    config(_aws_kubeconfig(["eks", "get-token"], [{"name": "OTHER", "value": "x"}]))
    assert cluster._aws_profile("ctx") == (True, None)

    config(_aws_kubeconfig(command="kubelogin"))
    assert cluster._aws_profile("ctx") == (False, None)
    config({})
    assert cluster._aws_profile("ctx") == (False, None)
    config({"contexts": [{"name": "ctx", "context": {}}]})  # no user
    assert cluster._aws_profile("ctx") == (False, None)


SSO = cluster.LoginAction(["aws", "sso", "login", "--profile", "work"], "work", False)
KEYS = cluster.LoginAction(["aws", "configure", "--profile", "work"], "work", True)


def test_login_action_picks_sso_or_access_keys_by_profile(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, "work"))
    monkeypatch.setattr(cluster, "_is_sso_profile", lambda _p: True)
    assert cluster.login_action("ctx") == SSO

    monkeypatch.setattr(cluster, "_is_sso_profile", lambda _p: False)
    assert cluster.login_action("ctx") == KEYS

    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, None))
    assert cluster.login_action("ctx") == cluster.LoginAction(
        ["aws", "configure"], None, True
    )

    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (False, None))
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {})
    assert cluster.login_action("ctx") is None


@pytest.mark.parametrize(
    ("program", "provider", "command"),
    [
        (
            "/usr/bin/gke-gcloud-auth-plugin",
            "Google Cloud",
            ["gcloud", "auth", "login"],
        ),
        ("gcloud", "Google Cloud", ["gcloud", "auth", "login"]),
        ("kubelogin", "Azure", ["az", "login"]),
        ("/opt/bin/kubelogin.exe", "Azure", ["az", "login"]),
        ("az", "Azure", ["az", "login"]),
    ],
)
def test_login_action_signs_in_to_google_cloud_and_azure(
    monkeypatch, program, provider, command
) -> None:
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {"command": program})

    assert cluster.login_action("ctx") == cluster.LoginAction(
        command, None, False, provider
    )


def test_login_action_ignores_sign_in_programs_it_does_not_know(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {"command": "okta"})
    assert cluster.login_action("ctx") is None


def test_programs_are_found_on_the_path_on_windows(monkeypatch) -> None:
    started = []

    class Fake:
        pid = 1
        returncode = 0

        def __init__(self, command, **_kwargs):
            started.append(command)

        def communicate(self, timeout=None):
            return "", ""

    monkeypatch.setattr(cluster.sys, "platform", "win32")
    monkeypatch.setattr(cluster.subprocess, "Popen", Fake)
    monkeypatch.setattr(
        cluster.shutil,
        "which",
        lambda name: "C:\\cli\\az.CMD" if name == "az" else None,
    )

    cluster._run_process(["az", "login"], 5)
    cluster._run_process(["other", "x"], 5)

    assert started == [["C:\\cli\\az.CMD", "login"], ["other", "x"]]


def test_sso_profiles_are_told_apart_from_access_key_profiles(monkeypatch) -> None:
    answers = {"sso_session": "", "sso_start_url": "https://example.awsapps.com/start"}

    def configure(command, _timeout):
        assert command[:3] == ["aws", "configure", "get"]
        assert command[4:] == ["--profile", "work"]
        value = answers[command[3]]
        if value is None:
            raise cluster.ClusterError("not set")
        return value + "\n"

    monkeypatch.setattr(cluster, "_run_command", configure)
    assert cluster._is_sso_profile("work") is True  # the legacy start URL

    answers.update(sso_session="main", sso_start_url=None)
    assert cluster._is_sso_profile("work") is True

    answers.update(sso_session=None, sso_start_url=None)
    assert cluster._is_sso_profile("work") is False

    monkeypatch.setattr(cluster, "_run_command", lambda _c, _t: "main")
    assert cluster._is_sso_profile(None) is True  # the default profile


def test_check_login_reports_signed_in_when_everything_answers(monkeypatch) -> None:
    calls = []
    monkeypatch.setattr(cluster, "_request", lambda *a, **_k: calls.append(a) or "")
    monkeypatch.setattr(cluster, "_run_command", lambda c, _t: calls.append(c) or "")

    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (False, None))
    assert cluster.check_login("ctx") == (False, None)

    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, "work"))
    assert cluster.check_login("ctx") == (False, None)
    assert ["aws", "sts", "get-caller-identity", "--profile", "work"] in calls


def test_check_login_detects_expired_sso_and_bad_access_keys(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "login_action", lambda _c: SSO)

    def request_fails(*_a, **_k):
        raise cluster.ClusterError("Error: the SSO session has expired")

    monkeypatch.setattr(cluster, "_request", request_fails)
    assert cluster.check_login("ctx") == (True, SSO)

    monkeypatch.setattr(cluster, "_request", lambda *_a, **_k: "")
    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, None))

    def sts_fails(*_a):
        raise cluster.ClusterError("InvalidClientTokenId: the token is invalid")

    monkeypatch.setattr(cluster, "_run_command", sts_fails)
    monkeypatch.setattr(cluster, "login_action", lambda _c: KEYS)
    assert cluster.check_login("ctx") == (True, KEYS)

    monkeypatch.setattr(cluster, "login_action", lambda _c: None)  # not AWS
    assert cluster.check_login("ctx") == (True, None)

    def unreadable(_context):
        raise cluster.ClusterError("config view failed")

    monkeypatch.setattr(cluster, "login_action", unreadable)
    assert cluster.check_login("ctx") == (True, None)


def test_check_login_ignores_failures_that_are_not_about_credentials(
    monkeypatch,
) -> None:
    def unreachable(*_a, **_k):
        raise cluster.ClusterError("Unable to connect: i/o timeout")

    monkeypatch.setattr(cluster, "_request", unreachable)
    assert cluster.check_login("ctx") == (False, None)

    monkeypatch.setattr(cluster, "_request", lambda *_a, **_k: "")
    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, None))

    def no_cli(*_a):
        raise cluster.ClusterError("Could not start aws: not found")

    monkeypatch.setattr(cluster, "_run_command", no_cli)
    assert cluster.check_login("ctx") == (False, None)

    def broken_json(*_a, **_k):
        raise cluster.ClusterError("expired token in a bad document")

    monkeypatch.setattr(cluster, "_aws_profile", broken_json)
    monkeypatch.setattr(cluster, "login_action", broken_json)
    assert cluster.check_login("ctx") == (True, None)


def test_run_login_waits_for_sso_and_opens_a_terminal_for_access_keys(
    monkeypatch,
) -> None:
    ran, opened = [], []
    monkeypatch.setattr(cluster, "_run_command", lambda c, t: ran.append((c, t)) or "")
    monkeypatch.setattr(cluster, "_open_terminal", opened.append)

    cluster.run_login(SSO)
    cluster.run_login(KEYS)

    assert ran == [(SSO.command, cluster.LOGIN_TIMEOUT)]
    assert opened == [KEYS.command]


def test_open_terminal_uses_the_first_terminal_found(monkeypatch) -> None:
    launched = []
    monkeypatch.setattr(cluster.sys, "platform", "linux")
    monkeypatch.setattr(cluster.subprocess, "Popen", lambda cmd: launched.append(cmd))
    monkeypatch.setattr(
        cluster.shutil,
        "which",
        lambda name: "/usr/bin/konsole" if name == "konsole" else None,
    )

    cluster._open_terminal(["aws", "configure"])
    assert launched == [["/usr/bin/konsole", "-e", "aws", "configure"]]

    monkeypatch.setattr(cluster.shutil, "which", lambda _name: None)
    with pytest.raises(cluster.ClusterError, match="aws configure"):
        cluster._open_terminal(["aws", "configure"])


def test_open_terminal_on_windows_and_when_it_cannot_start(monkeypatch) -> None:
    launched = []
    monkeypatch.setattr(cluster.sys, "platform", "win32")
    monkeypatch.setattr(cluster.subprocess, "Popen", lambda cmd: launched.append(cmd))

    cluster._open_terminal(["aws", "configure"])
    assert launched == [["cmd", "/c", "start", "", "cmd", "/k", "aws", "configure"]]

    def broken(_command):
        raise OSError("no cmd")

    monkeypatch.setattr(cluster.subprocess, "Popen", broken)
    with pytest.raises(cluster.ClusterError, match="Could not open a terminal"):
        cluster._open_terminal(["aws", "configure"])


def test_run_process_captures_output_and_the_exit_code() -> None:
    script = "import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)"

    result = cluster._run_process([sys.executable, "-c", script], timeout=20)

    assert (result.stdout.strip(), result.stderr.strip(), result.returncode) == (
        "out",
        "err",
        3,
    )
    assert not cluster._running


def test_run_process_stops_the_whole_process_group_on_timeout() -> None:
    started = time.monotonic()

    with pytest.raises(cluster.subprocess.TimeoutExpired):
        cluster._run_process(["sh", "-c", "sleep 30; true"], timeout=0.3)

    assert time.monotonic() - started < 10  # the grandchild did not hold it up
    assert not cluster._running


def test_cancel_running_stops_commands_that_are_in_flight() -> None:
    outcome = []

    def run() -> None:
        outcome.append(cluster._run_process(["sh", "-c", "sleep 30; true"], 60))

    worker = threading.Thread(target=run)
    started = time.monotonic()
    worker.start()
    deadline = time.monotonic() + 5
    while not cluster._running and time.monotonic() < deadline:
        time.sleep(0.01)

    cluster.cancel_running()
    worker.join(10)

    assert not worker.is_alive() and time.monotonic() - started < 10
    assert outcome[0].returncode != 0
    cluster.cancel_running()  # nothing left: harmless


def test_stop_handles_windows_and_already_finished_processes(monkeypatch) -> None:
    calls = []
    process = SimpleNamespace(pid=4242)

    monkeypatch.setattr(cluster.sys, "platform", "win32")
    monkeypatch.setattr(cluster.subprocess, "run", lambda cmd, **_kw: calls.append(cmd))
    cluster._stop(process)
    assert calls == [["taskkill", "/F", "/T", "/PID", "4242"]]

    def gone(_pid, _signal):
        raise ProcessLookupError

    monkeypatch.setattr(cluster.sys, "platform", "linux")
    monkeypatch.setattr(cluster.os, "killpg", gone)
    cluster._stop(process)  # must not raise


def test_commands_are_logged_with_their_outcome(caplog) -> None:
    caplog.set_level("DEBUG", logger="kubescope.cluster")

    cluster._run_process([sys.executable, "-c", "import sys; sys.exit(2)"], timeout=20)

    messages = [record.getMessage() for record in caplog.records]
    assert any(m.startswith("Run: ") and "-c" in m for m in messages)
    assert any(m.startswith("Exit 2 after ") for m in messages)
    assert any(m.startswith("stderr:") for m in messages)


def test_timeouts_and_cancellations_are_logged(caplog) -> None:
    caplog.set_level("INFO", logger="kubescope.cluster")

    with pytest.raises(cluster.subprocess.TimeoutExpired):
        cluster._run_process(["sh", "-c", "sleep 30; true"], timeout=0.2)
    assert "Timed out after 0.2s" in caplog.text

    thread = threading.Thread(
        target=lambda: cluster._run_process(["sh", "-c", "sleep 30; true"], 60)
    )
    thread.start()
    deadline = time.monotonic() + 5
    while not cluster._running and time.monotonic() < deadline:
        time.sleep(0.01)
    cluster.cancel_running()
    thread.join(10)
    assert "Stopping 1 running command(s)" in caplog.text


def test_login_steps_are_logged(monkeypatch, caplog) -> None:
    caplog.set_level("INFO", logger="kubescope.cluster")
    monkeypatch.setattr(cluster, "_request", lambda *_a, **_k: "")
    monkeypatch.setattr(cluster, "_run_command", lambda *_a: "")
    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, "work"))
    cluster.check_login("ctx")
    monkeypatch.setattr(cluster, "_is_sso_profile", lambda _p: True)
    cluster.login_action("ctx")
    monkeypatch.setattr(cluster, "_is_sso_profile", lambda _p: False)
    cluster.login_action("ctx")
    cluster.run_login(SSO)

    assert "Login check for ctx: signed in" in caplog.text
    assert "profile work signs in with SSO" in caplog.text
    assert "profile work uses access keys" in caplog.text
    assert "Starting sign-in: aws sso login --profile work" in caplog.text
    assert "Sign-in finished for profile work" in caplog.text

    caplog.clear()

    def fail(*_a, **_k):
        raise cluster.ClusterError("Unable to connect: i/o timeout")

    monkeypatch.setattr(cluster, "_request", fail)
    cluster.check_login("ctx")
    assert "not a credentials problem" in caplog.text


def _job(**status) -> dict:
    return {
        "kind": "Job",
        "metadata": {"name": "backup", "namespace": "ops"},
        "spec": status.pop("spec", {}),
        "status": status,
    }


def test_parse_job_reports_progress_and_state() -> None:
    now = datetime(2025, 1, 1, tzinfo=UTC)

    def parse(**status):
        workload = cluster._parse_workload(_job(**status), now)
        assert workload is not None
        return workload

    done = parse(
        succeeded=3,
        conditions=[{"type": "Complete", "status": "True"}],
        spec={"completions": 3},
    )
    assert (done.ready, done.desired, done.status) == (3, 3, "Complete")

    failed = parse(failed=2, conditions=[{"type": "Failed", "status": "True"}])
    assert (failed.status, failed.desired) == ("Failed", 1)  # completions default

    assert parse(active=1).status == "Running"
    assert parse().status == "Pending"
    assert parse(spec={"suspend": True}).status == "Suspended"
    # a condition that is not true says nothing
    assert parse(conditions=[{"type": "Failed", "status": "False"}]).status == "Pending"


def test_parse_cron_job_shows_schedule_and_activity() -> None:
    now = datetime(2025, 1, 1, tzinfo=UTC)

    def parse(spec, status=None):
        item = {
            "kind": "CronJob",
            "metadata": {"name": "nightly", "namespace": "ops"},
            "spec": spec,
            "status": status or {},
        }
        workload = cluster._parse_workload(item, now)
        assert workload is not None
        return workload

    idle = parse({"schedule": "0 3 * * *"})
    assert (idle.schedule, idle.status, idle.ready) == ("0 3 * * *", "Scheduled", 0)
    assert parse({"schedule": "* * * * *"}, {"active": [{}, {}]}).status == "Active"
    assert parse({"schedule": "* * * * *", "suspend": True}).status == "Suspended"


def test_get_workloads_lists_only_the_requested_kinds(monkeypatch) -> None:
    calls = []

    def fake_get_json(path, context, query=None):
        calls.append(path)
        if path == "/api/v1/namespaces":
            return {"items": [{"metadata": {"name": "ops"}}]}
        return {"items": [_job(succeeded=1)] if path.endswith("/jobs") else []}

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    namespaces, workloads = cluster.get_workloads("ctx", "ops", ("Job", "CronJob"))

    assert namespaces == ["ops"] and [w.name for w in workloads] == ["backup"]
    assert "/apis/batch/v1/namespaces/ops/jobs" in calls
    assert "/apis/batch/v1/namespaces/ops/cronjobs" in calls
    calls.clear()
    cluster.get_workloads("ctx")
    assert "/apis/apps/v1/deployments" in calls


@pytest.mark.parametrize(
    ("kind", "path"),
    [
        ("Job", "/apis/batch/v1/namespaces/ns/jobs/x"),
        ("CronJob", "/apis/batch/v1/namespaces/ns/cronjobs/x"),
        ("StatefulSet", "/apis/apps/v1/namespaces/ns/statefulsets/x"),
        ("Pod", "/api/v1/namespaces/ns/pods/x"),
    ],
)
def test_get_resource_details_knows_every_listed_kind(monkeypatch, kind, path) -> None:
    seen = []
    monkeypatch.setattr(cluster, "_get_json", lambda *a: seen.append(a[0]) or {})

    cluster.get_resource_details("ctx", kind, "ns", "x")

    assert seen == [path]


def test_get_resource_details_rejects_unknown_kinds() -> None:
    with pytest.raises(cluster.ClusterError, match="Unsupported resource kind: Gizmo"):
        cluster.get_resource_details("ctx", "Gizmo", "ns", "x")


def test_cron_job_pods_come_from_the_jobs_it_created(monkeypatch) -> None:
    cron = Workload("ops", "CronJob", "nightly", 0, 0, "1d", state="Scheduled")
    owned = {
        "metadata": {
            "name": "nightly-1",
            "ownerReferences": [{"kind": "CronJob", "name": "nightly"}],
        }
    }
    other = {
        "metadata": {
            "name": "other-1",
            "ownerReferences": [{"kind": "CronJob", "name": "other"}],
        }
    }
    standalone = {"metadata": {"name": "manual"}}
    pod = {"metadata": {"name": "nightly-1-abc", "namespace": "ops"}, "status": {}}
    seen = []

    def fake_get_json(path, context, query=None):
        seen.append((path, query))
        if path.endswith("/jobs"):
            return {"items": [owned, other, standalone]}
        return {"items": [pod]}

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    pods = cluster.get_workload_pods("ctx", cron)

    assert [p.name for p in pods] == ["nightly-1-abc"]
    assert seen[-1] == (
        "/api/v1/namespaces/ops/pods",
        [("labelSelector", "job-name in (nightly-1)")],
    )

    monkeypatch.setattr(
        cluster, "_get_json", lambda *_a: {"items": [other, standalone]}
    )
    assert cluster.get_workload_pods("ctx", cron) == []  # no Jobs, no Pods


NOW = datetime(2025, 1, 2, 12, 0, tzinfo=UTC)


def _item(kind, name="x", spec=None, status=None) -> dict:
    return {
        "kind": kind,
        "metadata": {"name": name, "namespace": "ns"},
        "spec": spec or {},
        "status": status or {},
    }


def test_workloads_are_counted_by_health() -> None:
    items = [
        _item("Deployment", spec={"replicas": 2}, status={"readyReplicas": 2}),  # ok
        _item(
            "Deployment", spec={"replicas": 2}, status={"readyReplicas": 1}
        ),  # warning
        _item("Deployment", spec={"replicas": 2}),  # bad
        _item("Deployment", spec={"replicas": 0}),  # idle: scaled to zero
        {"kind": "Deployment", "metadata": {}},  # unnamed: not counted
    ]

    summary = cluster._summarize_workloads(items, NOW)

    assert (summary.total, summary.ok, summary.warning, summary.bad) == (4, 1, 1, 1)


def test_pods_are_counted_by_phase_and_readiness() -> None:
    def pod(phase, ready, total=1):
        return {
            "metadata": {"name": "p"},
            "spec": {"containers": [{"name": f"c{i}"} for i in range(total)]},
            "status": {
                "phase": phase,
                "containerStatuses": [{"ready": i < ready} for i in range(total)],
            },
        }

    items = [
        pod("Running", 1),  # ok
        pod("Succeeded", 0),  # ok
        pod("Running", 1, 2),  # running but not ready: warning
        pod("Pending", 0),  # warning
        pod("Failed", 0),  # bad
        pod("Unknown", 0),  # bad
        {"metadata": {}},  # unnamed
    ]

    summary = cluster._summarize_pods(items, NOW)

    assert (summary.total, summary.ok, summary.warning, summary.bad) == (6, 2, 2, 2)


def test_events_use_whichever_timestamp_the_cluster_provides() -> None:
    created = "2025-01-02T03:00:00Z"
    base = {
        "metadata": {"namespace": "ns", "creationTimestamp": created},
        "message": "hi",
    }

    classic = cluster._parse_event(
        {
            **base,
            "type": "Warning",
            "lastTimestamp": "2025-01-02T11:00:00Z",
            "count": 7,
            "source": {"component": "kubelet"},
            "involvedObject": {"kind": "Pod", "name": "api-1"},
        },
        NOW,
    )
    assert classic is not None
    seen, event = classic
    assert seen == 3600 and event.type == "Warning" and event.count == 7
    assert (event.source, event.namespace, event.involved) == (
        "kubelet",
        "ns",
        "Pod: api-1",
    )
    assert (event.age, event.last_seen) == ("9h", "1h")

    modern = cluster._parse_event(
        {
            **base,
            "series": {"lastObservedTime": "2025-01-02T11:30:00Z", "count": 3},
            "reportingComponent": "secret-store",
            "involvedObject": {"namespace": "other"},
        },
        NOW,
    )
    assert modern is not None
    assert modern[1].count == 3 and modern[1].source == "secret-store"
    assert modern[1].involved == "?: ?" and modern[1].type == "Normal"

    only_event_time = cluster._parse_event(
        {
            "message": "hi",
            "eventTime": "2025-01-02T11:59:00Z",
            "involvedObject": {"namespace": "o"},
            "metadata": {},
        },
        NOW,
    )
    assert only_event_time is not None and only_event_time[1].namespace == "o"
    assert only_event_time[1].age == "unknown" and only_event_time[1].source == ""

    undated = cluster._parse_event({"message": "hi", "metadata": {}}, NOW)
    assert undated is not None and undated[0] == float("inf")
    assert undated[1].last_seen == "unknown"
    assert cluster._parse_event({"metadata": {}}, NOW) is None  # nothing to say


def _overview_documents(extra_events=0):
    events = [
        {
            "message": f"event {i}",
            "metadata": {
                "namespace": "ns",
                "creationTimestamp": "2025-01-01T00:00:00Z",
            },
            "lastTimestamp": f"2025-01-02T{i % 24:02d}:00:00Z",
            "involvedObject": {"kind": "Pod", "name": "p"},
        }
        for i in range(2 + extra_events)
    ]
    return {
        "pods": {"items": []},
        "deployments": {
            "items": [
                _item("Deployment", spec={"replicas": 1}, status={"readyReplicas": 1})
            ]
        },
        "daemonsets": {"items": []},
        "statefulsets": {"items": []},
        "replicasets": {"items": [_item("ReplicaSet", spec={"replicas": 0})]},
        "jobs": {
            "items": [
                _item(
                    "Job",
                    status={
                        "succeeded": 1,
                        "conditions": [{"type": "Complete", "status": "True"}],
                    },
                )
            ]
        },
        "cronjobs": {"items": []},
        "events": {"items": events},
    }


def test_workloads_overview_counts_every_kind_and_lists_recent_events(
    monkeypatch,
) -> None:
    documents = _overview_documents()
    monkeypatch.setattr(
        cluster,
        "_get_json",
        lambda path, _c, _q=None: documents[path.rsplit("/", 1)[1]],
    )

    overview = cluster.get_workloads_overview("ctx")

    assert set(overview.kinds) == set(cluster.OVERVIEW_KINDS)
    assert (
        overview.kinds["Deployment"].ok == 1 and overview.kinds["ReplicaSet"].total == 1
    )
    assert overview.kinds["ReplicaSet"].ok == 0  # scaled to zero: idle
    assert overview.kinds["Job"].ok == 1
    assert [e.message for e in overview.events] == [
        "event 1",
        "event 0",
    ]  # newest first
    assert overview.unreadable == ()


def test_workloads_overview_reports_unreadable_sections_and_caps_events(
    monkeypatch,
) -> None:
    documents = _overview_documents(extra_events=cluster.EVENT_LIMIT + 10)

    def fake(path, context, query=None):
        resource = path.rsplit("/", 1)[1]
        if resource in {"daemonsets", "replicasets"}:
            raise cluster.ClusterError("forbidden: cannot list")
        return documents[resource]

    monkeypatch.setattr(cluster, "_get_json", fake)

    overview = cluster.get_workloads_overview("ctx")

    assert "DaemonSet" not in overview.kinds and "ReplicaSet" not in overview.kinds
    assert set(overview.unreadable) == {"DaemonSet", "ReplicaSet"}
    assert len(overview.events) == cluster.EVENT_LIMIT


def test_workloads_overview_fails_when_nothing_is_readable(monkeypatch) -> None:
    def forbidden(*_a):
        raise cluster.ClusterError("Unable to connect to the server")

    monkeypatch.setattr(cluster, "_get_json", forbidden)

    with pytest.raises(cluster.ClusterError, match="Unable to connect"):
        cluster.get_workloads_overview("ctx")


def test_together_runs_calls_at_the_same_time_and_raises_the_first_failure() -> None:
    barrier = threading.Barrier(2, timeout=5)  # both must be running to pass

    def meet(value: str) -> str:
        barrier.wait()
        return value

    assert cluster._together(lambda: meet("a"), lambda: meet("b")) == ["a", "b"]

    def fail() -> None:
        raise cluster.ClusterError("first")

    def fail_later() -> None:
        raise cluster.ClusterError("second")

    with pytest.raises(cluster.ClusterError, match="first"):
        cluster._together(fail, fail_later)


NETWORK_NOW = datetime(2025, 1, 10, tzinfo=UTC)
CREATED = {"creationTimestamp": "2025-01-08T00:00:00Z"}


def _network(kind: str, item: dict) -> cluster.ClusterResource:
    metadata = {**CREATED, "name": "x", **item.get("metadata", {})}
    resource = cluster._parse_resource(
        kind, {**item, "metadata": metadata}, NETWORK_NOW
    )
    assert resource is not None
    return resource


def test_parse_network_reads_a_service() -> None:
    resource = _network(
        "Service",
        {
            "metadata": {"name": "web", "namespace": "shop"},
            "spec": {
                "type": "LoadBalancer",
                "clusterIP": "10.0.0.1",
                "ports": [
                    {"port": 80, "nodePort": 30080, "protocol": "TCP"},
                    {"port": 53, "protocol": "UDP"},
                ],
            },
            "status": {"loadBalancer": {"ingress": [{"hostname": "lb.example"}]}},
        },
    )

    assert (resource.namespace, resource.kind, resource.name) == (
        "shop",
        "Service",
        "web",
    )
    assert resource.values == (
        "LoadBalancer",
        "10.0.0.1",
        "lb.example",
        "80:30080/TCP, 53/UDP",
    )
    assert resource.age == "2d"


def test_parse_network_shows_a_pending_load_balancer_and_plain_services() -> None:
    pending = _network(
        "Service", {"metadata": {"name": "a"}, "spec": {"type": "LoadBalancer"}}
    )
    plain = _network(
        "Service",
        {"metadata": {"name": "b"}, "spec": {"externalIPs": ["1.2.3.4"]}},
    )

    assert pending.values == ("LoadBalancer", "—", "pending", "—")
    assert plain.values == ("ClusterIP", "—", "1.2.3.4", "—")
    assert plain.namespace == "default"


def test_parse_network_reads_endpoints_and_slices() -> None:
    endpoints = _network(
        "Endpoints",
        {
            "metadata": {"name": "web"},
            "subsets": [
                {
                    "addresses": [{"ip": "10.0.0.1"}, {"ip": "10.0.0.2"}],
                    "ports": [{"port": 80}, {"port": 443}],
                },
                {"addresses": [{"ip": "10.0.0.3"}]},
            ],
        },
    )
    empty = _network("Endpoints", {"metadata": {"name": "none"}})
    slice_ = _network(
        "EndpointSlice",
        {
            "metadata": {"name": "web-abc"},
            "addressType": "IPv4",
            "ports": [{"port": 80, "protocol": "TCP"}, {"name": "x"}],
            "endpoints": [{"addresses": ["10.0.0.1", "10.0.0.9"]}, {"addresses": []}],
        },
    )

    assert endpoints.values == ("10.0.0.1:80, 10.0.0.1:443, 10.0.0.2:80 +2 more",)
    assert empty.values == ("—",)
    assert slice_.values == ("IPv4", "80/TCP", "10.0.0.1")


def test_parse_network_reads_ingresses_and_ingress_classes() -> None:
    ingress = _network(
        "Ingress",
        {
            "metadata": {"name": "site"},
            "spec": {
                "ingressClassName": "nginx",
                "rules": [{"host": "a.example"}, {}],
                "tls": [{}],
            },
            "status": {"loadBalancer": {"ingress": [{"ip": "5.6.7.8"}]}},
        },
    )
    annotated = _network(
        "Ingress",
        {
            "metadata": {
                "name": "old",
                "annotations": {"kubernetes.io/ingress.class": "alb"},
            }
        },
    )
    bare = _network("Ingress", {"metadata": {"name": "bare"}})
    ingress_class = _network(
        "IngressClass",
        {
            "metadata": {"name": "nginx", "namespace": "ignored"},
            "spec": {
                "controller": "k8s.io/ingress-nginx",
                "parameters": {"kind": "IngressParameters", "name": "p"},
            },
        },
    )
    plain_class = _network("IngressClass", {"metadata": {"name": "x"}})

    assert ingress.values == ("nginx", "a.example, *", "5.6.7.8", "80, 443")
    assert annotated.values[0] == "alb"
    assert bare.values == ("—", "—", "—", "80")
    assert ingress_class.namespace == ""  # it belongs to the whole cluster
    assert ingress_class.values == ("k8s.io/ingress-nginx", "IngressParameters/p")
    assert plain_class.values == ("—", "—")


def test_parse_network_reads_network_policies() -> None:
    selected = _network(
        "NetworkPolicy",
        {
            "metadata": {"name": "db"},
            "spec": {
                "podSelector": {
                    "matchLabels": {"tier": "db", "app": "x"},
                    "matchExpressions": [{"key": "env", "operator": "In"}],
                },
                "policyTypes": ["Ingress"],
            },
        },
    )
    everything = _network(
        "NetworkPolicy", {"metadata": {"name": "all"}, "spec": {"egress": [{}]}}
    )
    default = _network("NetworkPolicy", {"metadata": {"name": "d"}})

    assert selected.values == ("app=x,tier=db,env in", "Ingress")
    assert everything.values == ("*", "Ingress, Egress")
    assert default.values == ("*", "Ingress")
    assert cluster._parse_resource("Service", {"metadata": {}}, NETWORK_NOW) is None


def test_get_network_lists_by_namespace_or_for_the_whole_cluster(monkeypatch) -> None:
    calls = []

    def fake_get_json(path: str, context: str, query=None) -> dict:
        calls.append(path)
        if path == "/api/v1/namespaces":
            return {"items": [{"metadata": {"name": "ops"}}]}
        return {
            "items": [
                {"metadata": {**CREATED, "name": "b", "namespace": "ops"}},
                {"metadata": {**CREATED, "name": "a", "namespace": "ops"}},
            ]
        }

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    namespaces, services = cluster.get_resources("ctx", "ops", "Service")
    assert namespaces == ["ops"] and [s.name for s in services] == ["a", "b"]
    assert "/api/v1/namespaces/ops/services" in calls
    cluster.get_resources("ctx", None, "Ingress")
    assert "/apis/networking.k8s.io/v1/ingresses" in calls
    cluster.get_resources("ctx", "ops", "IngressClass")  # not namespaced
    assert "/apis/networking.k8s.io/v1/ingressclasses" in calls


@pytest.mark.parametrize(
    ("kind", "namespace", "path"),
    [
        ("Service", "ns", "/api/v1/namespaces/ns/services/x"),
        ("Endpoints", "ns", "/api/v1/namespaces/ns/endpoints/x"),
        (
            "NetworkPolicy",
            "ns",
            "/apis/networking.k8s.io/v1/namespaces/ns/networkpolicies/x",
        ),
        ("IngressClass", "", "/apis/networking.k8s.io/v1/ingressclasses/x"),
    ],
)
def test_get_resource_details_knows_the_network_kinds(
    monkeypatch, kind, namespace, path
) -> None:
    seen = []
    monkeypatch.setattr(cluster, "_get_json", lambda *a: seen.append(a[0]) or {})

    cluster.get_resource_details("ctx", kind, namespace, "x")

    assert seen == [path]


def test_configured_kubeconfig_files_replace_the_environment(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("KUBECONFIG", "/from/the/environment")
    assert cluster._kubeconfig_paths() == "/from/the/environment"

    first, second = tmp_path / "first", tmp_path / "second"
    first.write_text(json.dumps({"contexts": [{"name": "a"}]}))
    second.write_text(json.dumps({"contexts": [{"name": "b"}]}))
    cluster.configure([str(first), str(second)])

    assert cluster._kubeconfig_paths() == f"{first}{os.pathsep}{second}"
    assert cluster.list_contexts() == (["a", "b"], None)
    cluster.configure()
    assert cluster._kubeconfig_paths() == "/from/the/environment"


@pytest.mark.parametrize(
    ("text", "arguments"),
    [
        ("oci session authenticate", ["oci", "session", "authenticate"]),
        (
            'doctl auth init --label "my team"',
            ["doctl", "auth", "init", "--label", "my team"],
        ),
    ],
)
def test_parse_command_splits_without_a_shell(text, arguments) -> None:
    assert cluster.parse_command(text) == arguments


@pytest.mark.parametrize("text", ["", "   ", 'oci "unclosed'])
def test_parse_command_rejects_what_cannot_run(text) -> None:
    with pytest.raises(ValueError):
        cluster.parse_command(text)


def test_parse_command_follows_windows_quoting(monkeypatch) -> None:
    monkeypatch.setattr(cluster.sys, "platform", "win32")

    assert cluster.parse_command('"C:\\Tools\\oci.exe" session authenticate') == [
        "C:\\Tools\\oci.exe",
        "session",
        "authenticate",
    ]


def test_login_action_uses_the_command_set_for_the_program(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {"command": "/bin/oci"})
    cluster.configure(sign_in_commands={"oci": "oci session authenticate"})

    assert cluster.login_action("ctx") == cluster.LoginAction(
        ["oci", "session", "authenticate"], None, False, "oci"
    )

    cluster.configure(sign_in_commands={"oci": 'oci "broken'})
    assert cluster.login_action("ctx") is None  # an unreadable command is no sign-in

    cluster.configure(sign_in_commands={"other": "other login"})
    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (False, None))
    assert cluster.login_action("ctx") is None  # not the program of this context


def test_a_failing_custom_sign_in_program_offers_the_sign_in(monkeypatch) -> None:
    login = cluster.LoginAction(["oci", "session", "authenticate"], None, False, "oci")
    monkeypatch.setattr(cluster, "login_action", lambda _c: login)
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {"command": "oci"})

    def fails(*_a, **_k):
        raise cluster.ClusterError("exec: process returned 1. something odd")

    monkeypatch.setattr(cluster, "_request", fails)
    assert cluster.check_login("ctx") == (False, None)  # no command set: not a login

    cluster.configure(sign_in_commands={"oci": "oci session authenticate"})
    assert cluster.check_login("ctx") == (True, login)


def test_only_a_sign_in_program_with_a_command_counts_as_a_login_problem(
    monkeypatch,
) -> None:
    exec_error = cluster.ClusterError("exec: process returned 1")
    cluster.configure(sign_in_commands={"oci": "oci login"})
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {"command": "oci"})

    assert cluster._custom_sign_in_failed(exec_error, "ctx") is True
    assert cluster._custom_sign_in_failed(cluster.ClusterError("503"), "ctx") is False

    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {"command": "doctl"})
    assert cluster._custom_sign_in_failed(exec_error, "ctx") is False

    def unreadable(_context):
        raise cluster.ClusterError("kubeconfig is damaged")

    monkeypatch.setattr(cluster, "_sign_in_program", unreadable)
    assert cluster._custom_sign_in_failed(exec_error, "ctx") is False


def _counting_sign_in(tmp_path, tokens: list[str]) -> dict:
    """A sign-in program that counts how often it runs and hands out `tokens`
    one after the other."""
    counter = tmp_path / "runs"
    script = tmp_path / "login.py"
    script.write_text(
        "import json, pathlib\n"
        f"counter = pathlib.Path({str(counter)!r})\n"
        "runs = int(counter.read_text()) if counter.exists() else 0\n"
        "counter.write_text(str(runs + 1))\n"
        f"tokens = {tokens!r}\n"
        "print(json.dumps({'apiVersion': 'v1', 'kind': 'ExecCredential',"
        " 'status': {'token': tokens[min(runs, len(tokens) - 1)]}}))\n"
    )
    return {
        "apiVersion": "v1",
        "command": sys.executable,
        "args": [str(script)],
        "counter": counter,
    }


def _sign_in_runs(exec_block: dict) -> int:
    counter = exec_block["counter"]
    return int(counter.read_text()) if counter.exists() else 0


def _use_sign_in(fake_cluster, exec_block: dict) -> None:
    program = {key: value for key, value in exec_block.items() if key != "counter"}
    fake_cluster.write_kubeconfig(user={"exec": program})


def test_the_sign_in_runs_once_however_many_requests_follow(
    fake_cluster, tmp_path
) -> None:
    block = _counting_sign_in(tmp_path, ["t1"])
    _use_sign_in(fake_cluster, block)
    fake_cluster.serve("/version", {})

    for _ in range(3):
        cluster._request("/version", "dev")
    cluster._together(*[lambda: cluster._request("/version", "dev")] * 4)

    assert _sign_in_runs(block) == 1
    assert {token for _path, token in fake_cluster.requests} == {"Bearer t1"}


def test_a_refused_token_signs_in_again_once(fake_cluster, tmp_path) -> None:
    block = _counting_sign_in(tmp_path, ["old", "new"])
    _use_sign_in(fake_cluster, block)
    fake_cluster.accept_token = "Bearer new"
    fake_cluster.serve("/version", {"ok": True})

    assert json.loads(cluster._request("/version", "dev")) == {"ok": True}
    assert _sign_in_runs(block) == 2
    cluster._request("/version", "dev")  # the new token is kept
    assert _sign_in_runs(block) == 2


def test_a_token_that_stays_refused_is_reported_after_one_retry(
    fake_cluster, tmp_path
) -> None:
    block = _counting_sign_in(tmp_path, ["bad"])
    _use_sign_in(fake_cluster, block)
    fake_cluster.accept_token = "Bearer never"
    fake_cluster.serve("/version", {})

    with pytest.raises(cluster.ClusterError, match="Unauthorized"):
        cluster._request("/version", "dev")

    assert _sign_in_runs(block) == 2  # not a loop


def test_each_context_has_its_own_client_and_new_files_reset_them(
    fake_cluster,
) -> None:
    first = cluster._cached_client("dev")
    assert cluster._cached_client("dev") is first
    assert cluster._cached_client("dev", fresh=True) is not first

    cluster.configure(["/another/file"])  # other files: other credentials
    assert cluster._clients == {}


def test_a_finished_sign_in_makes_the_next_request_use_its_credentials(
    monkeypatch, fake_cluster
) -> None:
    first = cluster._cached_client("dev")
    monkeypatch.setattr(cluster, "_run_command", lambda *_a: "")

    cluster.run_login(cluster.LoginAction(["aws", "sso", "login"], None, False))

    assert cluster._clients == {}
    assert cluster._cached_client("dev") is not first


def test_parse_config_reads_config_maps_and_secrets() -> None:
    config_map = _network(
        "ConfigMap",
        {
            "metadata": {"name": "c"},
            "data": {"a": "1", "b": "2"},
            "binaryData": {"c": ""},
        },
    )
    empty = _network("ConfigMap", {"metadata": {"name": "e"}})
    secret = _network(
        "Secret", {"metadata": {"name": "s"}, "type": "Opaque", "data": {"k": "dg=="}}
    )
    untyped = _network("Secret", {"metadata": {"name": "u"}})

    assert config_map.values == ("3",) and empty.values == ("0",)
    assert secret.values == ("Opaque", "1") and untyped.values == ("—", "0")


def test_parse_config_reads_quotas_and_limit_ranges() -> None:
    quota = _network(
        "ResourceQuota",
        {"status": {"hard": {"pods": "10", "cpu": "4"}, "used": {"pods": "3"}}},
    )
    declared = _network("ResourceQuota", {"spec": {"hard": {"pods": "5"}}})
    bare = _network("ResourceQuota", {"metadata": {"name": "n"}})
    ranges = _network(
        "LimitRange", {"spec": {"limits": [{"type": "Container"}, {"type": "Pod"}, {}]}}
    )
    no_limits = _network("LimitRange", {"metadata": {"name": "n"}})

    assert quota.values == ("pods: 3/10, cpu: 0/4",)
    assert declared.values == ("pods: 0/5",) and bare.values == ("—",)
    assert ranges.values == ("Container, Pod",) and no_limits.values == ("—",)


def test_parse_config_reads_autoscalers_and_disruption_budgets() -> None:
    autoscaler = _network(
        "HorizontalPodAutoscaler",
        {
            "spec": {
                "scaleTargetRef": {"kind": "Deployment", "name": "web"},
                "minReplicas": 2,
                "maxReplicas": 8,
            },
            "status": {"currentReplicas": 3},
        },
    )
    bare = _network("HorizontalPodAutoscaler", {"metadata": {"name": "n"}})
    budget = _network(
        "PodDisruptionBudget",
        {"spec": {"minAvailable": "50%"}, "status": {"disruptionsAllowed": 0}},
    )
    unbounded = _network("PodDisruptionBudget", {"spec": {"maxUnavailable": 1}})

    assert autoscaler.values == ("Deployment/web", "2", "8", "3")
    assert bare.values == ("—", "1", "—", "—")
    assert budget.values == ("50%", "—", "0")
    assert unbounded.values == ("—", "1", "—")


def test_parse_config_reads_cluster_scoped_kinds_and_leases() -> None:
    priority = _network("PriorityClass", {"value": 1000, "globalDefault": True})
    plain = _network("PriorityClass", {"metadata": {"name": "n"}})
    runtime = _network("RuntimeClass", {"handler": "runc"})
    no_handler = _network("RuntimeClass", {"metadata": {"name": "n"}})
    lease = _network("Lease", {"spec": {"holderIdentity": "node-a"}})
    free = _network("Lease", {"metadata": {"name": "n"}})
    webhooks = _network("MutatingWebhookConfiguration", {"webhooks": [{}, {}]})
    none = _network("ValidatingWebhookConfiguration", {"metadata": {"name": "n"}})

    assert priority.values == ("1000", "true") and plain.values == ("—", "false")
    assert runtime.values == ("runc",) and no_handler.values == ("—",)
    assert lease.values == ("node-a",) and free.values == ("—",)
    assert webhooks.values == ("2",) and none.values == ("0",)
    assert priority.namespace == "" and runtime.namespace == ""
    assert webhooks.namespace == "" and lease.namespace == "default"


@pytest.mark.parametrize(
    ("kind", "path"),
    [
        ("ConfigMap", "/api/v1/namespaces/ns/configmaps/x"),
        ("Secret", "/api/v1/namespaces/ns/secrets/x"),
        ("ResourceQuota", "/api/v1/namespaces/ns/resourcequotas/x"),
        ("LimitRange", "/api/v1/namespaces/ns/limitranges/x"),
        (
            "HorizontalPodAutoscaler",
            "/apis/autoscaling/v2/namespaces/ns/horizontalpodautoscalers/x",
        ),
        (
            "PodDisruptionBudget",
            "/apis/policy/v1/namespaces/ns/poddisruptionbudgets/x",
        ),
        ("Lease", "/apis/coordination.k8s.io/v1/namespaces/ns/leases/x"),
        ("PriorityClass", "/apis/scheduling.k8s.io/v1/priorityclasses/x"),
        ("RuntimeClass", "/apis/node.k8s.io/v1/runtimeclasses/x"),
        (
            "MutatingWebhookConfiguration",
            "/apis/admissionregistration.k8s.io/v1/mutatingwebhookconfigurations/x",
        ),
        (
            "ValidatingWebhookConfiguration",
            "/apis/admissionregistration.k8s.io/v1/validatingwebhookconfigurations/x",
        ),
    ],
)
def test_config_kinds_are_listed_and_described_at_their_paths(
    monkeypatch, kind, path
) -> None:
    seen = []
    monkeypatch.setattr(cluster, "_get_json", lambda *a: seen.append(a[0]) or {})

    namespace = "" if kind in cluster._CLUSTER_WIDE else "ns"
    cluster.get_resource_details("ctx", kind, namespace, "x")
    cluster.get_resources("ctx", "ns", kind)

    assert seen[0] == path
    assert path.rsplit("/", 1)[0] in seen  # the list, in its namespace or not


def test_secret_details_keep_the_keys_but_never_the_values(monkeypatch) -> None:
    document = {
        "kind": "Secret",
        "metadata": {
            "name": "s",
            "annotations": {cluster._LAST_APPLIED: '{"data":{"k":"dg=="}}', "a": "b"},
        },
        "data": {"password": "aHVudGVyMg==", "user": "YWRtaW4="},
        "stringData": {"token": "plain"},
    }
    monkeypatch.setattr(cluster, "_get_json", lambda *a: document)

    result = cluster.get_resource_details("ctx", "Secret", "ns", "s")

    assert result["data"] == {"password": "<redacted>", "user": "<redacted>"}
    assert result["stringData"] == {"token": "<redacted>"}
    assert result["metadata"]["annotations"] == {"a": "b"}
    assert "aHVudGVyMg" not in json.dumps(result)


def test_secret_details_tolerate_a_secret_without_data(monkeypatch) -> None:
    for document in ({"kind": "Secret"}, {"metadata": {"name": "s"}, "data": None}):
        monkeypatch.setattr(cluster, "_get_json", lambda *a, d=document: dict(d))
        assert cluster.get_resource_details("ctx", "Secret", "ns", "s") == document


def _eks(monkeypatch, arguments=None, **kwargs) -> None:
    document = _aws_kubeconfig(
        arguments
        or ["eks", "get-token", "--cluster-name", "main", "--region", "us-east-1"],
        **kwargs,
    )
    monkeypatch.setattr(cluster, "_kubeconfig", lambda: document)


def test_eks_target_names_the_cluster_region_and_profile(monkeypatch) -> None:
    _eks(monkeypatch, ["eks", "get-token", "--cluster-name", "main", "--profile", "w"])
    assert cluster._eks_target("ctx") == ["--cluster-name", "main", "--profile", "w"]

    _eks(monkeypatch)
    assert cluster._eks_target("ctx") == [
        "--cluster-name",
        "main",
        "--region",
        "us-east-1",
    ]
    assert cluster.is_eks_context("ctx")


def test_only_eks_contexts_have_node_groups(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_kubeconfig", lambda: _aws_kubeconfig(["eks"]))
    assert not cluster.is_eks_context("ctx")  # aws, but no cluster name
    monkeypatch.setattr(
        cluster, "_kubeconfig", lambda: _aws_kubeconfig(command="kubelogin")
    )
    assert not cluster.is_eks_context("ctx")
    with pytest.raises(cluster.ClusterError, match="only available for Amazon EKS"):
        cluster.get_resource_details("ctx", "NodeGroup", "", "ng")


def _fake_aws(monkeypatch, answers: dict[str, str]) -> list[list[str]]:
    commands = []

    def run(command: list[str], timeout: float) -> str:
        commands.append(command)
        return answers[command[2]]

    monkeypatch.setattr(cluster, "_run_command", run)
    return commands


def test_get_resources_lists_the_node_groups_of_the_cluster(monkeypatch) -> None:
    _eks(monkeypatch)
    group = {
        "nodegroupName": "b",
        "status": "ACTIVE",
        "instanceTypes": ["m5.large"],
        "scalingConfig": {"minSize": 1, "maxSize": 4, "desiredSize": 2},
        "amiType": "AL2023_x86_64_STANDARD",
        "releaseVersion": "1.29.3-20240531",
        "createdAt": "2020-01-01T00:00:00+00:00",
    }
    commands = _fake_aws(
        monkeypatch,
        {
            "list-nodegroups": json.dumps({"nodegroups": ["b", "a"]}),
            "describe-nodegroup": json.dumps({"nodegroup": group}),
        },
    )

    namespaces, groups = cluster.get_resources("ctx", "ops", "NodeGroup")

    assert namespaces == []  # not namespaced, and no cluster request for them
    assert groups[0].values == (
        "ACTIVE",
        "m5.large",
        "2 (1–4)",
        "AL2023_x86_64_STANDARD",
        "1.29.3-20240531",
    )
    assert groups[0].namespace == "" and groups[0].kind == "NodeGroup"
    assert commands[0][:3] == ["aws", "eks", "list-nodegroups"]
    assert "--region" in commands[0] and commands[0][-2:] == ["--output", "json"]


def test_parse_nodegroup_tolerates_missing_fields() -> None:
    now = datetime(2025, 1, 10, tzinfo=UTC)
    bare = cluster._parse_eks("NodeGroup", {"nodegroupName": "x"}, now)
    naive = cluster._parse_eks(
        "NodeGroup", {"nodegroupName": "y", "createdAt": "2025-01-08T00:00:00"}, now
    )
    no_max = cluster._parse_eks(
        "NodeGroup", {"nodegroupName": "z", "scalingConfig": {"desiredSize": 3}}, now
    )

    assert bare.values == ("—",) * 5 and bare.age == "unknown"
    assert naive.age == "2d"
    assert no_max.values[2] == "3 (0–3)"
    assert cluster._parse_eks("NodeGroup", {}, now) is None


def test_node_groups_without_any_group_and_details(monkeypatch) -> None:
    _eks(monkeypatch)
    _fake_aws(
        monkeypatch,
        {
            "list-nodegroups": json.dumps({}),
            "describe-nodegroup": json.dumps({"nodegroup": {"nodegroupName": "ng"}}),
        },
    )
    assert cluster.get_resources("ctx", None, "NodeGroup") == ([], [])
    assert cluster.get_resource_details("ctx", "NodeGroup", "", "ng") == {
        "nodegroupName": "ng"
    }


@pytest.mark.parametrize("output", ["not json", "[1]"])
def test_unexpected_aws_answers_are_reported(monkeypatch, output) -> None:
    _eks(monkeypatch)
    monkeypatch.setattr(cluster, "_run_command", lambda *a: output)

    with pytest.raises(cluster.ClusterError, match="something unexpected"):
        cluster.get_resources("ctx", None, "NodeGroup")


def _helm_secret(
    name, revision, status, namespace="ops", created="2020-01-01T00:00:00Z"
):
    return {
        "metadata": {
            "name": f"sh.helm.release.v1.{name}.v{revision}",
            "namespace": namespace,
            "creationTimestamp": created,
            "labels": {
                "owner": "helm",
                "name": name,
                "status": status,
                "version": str(revision),
            },
        }
    }


def _fake_cluster_api(monkeypatch, secrets, calls=None):
    def fake_get_json(path, context, query=None, accept="application/json"):
        if calls is not None:
            calls.append((path, query, accept))
        if path == "/api/v1/namespaces":
            return {"items": [{"metadata": {"name": "ops"}}]}
        return {"items": secrets}

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)


def test_get_resources_lists_the_add_ons_of_eks_and_the_helm_releases(
    monkeypatch,
) -> None:
    _eks(monkeypatch)
    commands = _fake_aws(
        monkeypatch,
        {
            "list-addons": json.dumps({"addons": ["vpc-cni"]}),
            "describe-addon": json.dumps(
                {
                    "addon": {
                        "addonName": "vpc-cni",
                        "status": "ACTIVE",
                        "addonVersion": "v1.18.1-eksbuild.3",
                        "createdAt": "2020-01-01T00:00:00+00:00",
                    }
                }
            ),
        },
    )
    calls = []
    _fake_cluster_api(
        monkeypatch,
        [
            _helm_secret("web", 1, "superseded", created="2020-01-01T00:00:00Z"),
            _helm_secret("web", 2, "deployed", created="2020-02-01T00:00:00Z"),
            _helm_secret("agent", 1, "failed", namespace="monitoring"),
            {"metadata": {"labels": {"owner": "helm", "name": "odd"}}},  # no revision
        ],
        calls,
    )

    namespaces, addons = cluster.get_resources("ctx", None, "Addon")

    assert namespaces == ["ops"]
    assert [(a.kind, a.name, a.namespace) for a in addons] == [
        ("HelmRelease", "agent", "monitoring"),
        ("Addon", "vpc-cni", ""),
        ("HelmRelease", "web", "ops"),
    ]
    assert addons[0].values == ("failed", "—", "Helm")
    assert addons[1].values == ("ACTIVE", "v1.18.1-eksbuild.3", "EKS")
    assert addons[2].values == ("deployed", "—", "Helm")  # the latest revision
    secrets = next(call for call in calls if call[0].endswith("/secrets"))
    assert secrets[1] == [("labelSelector", "owner=helm")]
    assert "PartialObjectMetadataList" in secrets[2]  # never the data of a Secret
    assert commands[1][:3] == ["aws", "eks", "describe-addon"]
    assert "--addon-name" in commands[1]
    bare = cluster._parse_eks("Addon", {"addonName": "x"}, NETWORK_NOW)
    assert bare.values == ("—", "—", "EKS")
    assert cluster.get_resource_details("ctx", "Addon", "", "vpc-cni")["addonName"]


def test_helm_releases_show_the_chart_and_app_version_of_their_workloads(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        cluster, "_kubeconfig", lambda: _aws_kubeconfig(command="kubelogin")
    )
    calls = []
    workload = {
        "metadata": {
            "namespace": "ops",
            "annotations": {
                "meta.helm.sh/release-name": "web",
                "meta.helm.sh/release-namespace": "ops",
            },
            "labels": {
                "helm.sh/chart": "cert-manager-v1.14.0",
                "app.kubernetes.io/version": "v1.14.0",
            },
        }
    }

    def fake_get_json(path, context, query=None, accept="application/json"):
        calls.append((path, accept))
        if path == "/api/v1/namespaces":
            return {"items": []}
        if path.endswith("/deployments"):
            return {"items": [workload]}
        if path.endswith("/statefulsets"):
            raise cluster.ClusterError("forbidden")
        if path.endswith("/secrets"):
            return {
                "items": [
                    _helm_secret("web", 2, "deployed"),
                    _helm_secret("bare", 1, "deployed"),
                ]
            }
        return {"items": []}

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    _, addons = cluster.get_resources("ctx", None, "Addon")

    assert {a.name: a.values[1] for a in addons} == {
        "web": "chart v1.14.0 · app v1.14.0",
        "bare": "—",
    }
    assert all("PartialObjectMetadataList" in accept for _, accept in calls[1:])


def test_outside_eks_the_add_ons_are_the_helm_releases(monkeypatch) -> None:
    monkeypatch.setattr(
        cluster, "_kubeconfig", lambda: _aws_kubeconfig(command="kubelogin")
    )
    _fake_cluster_api(monkeypatch, [_helm_secret("web", 3, "deployed")])

    _, addons = cluster.get_resources("ctx", "ops", "Addon")

    assert [(a.kind, a.values) for a in addons] == [
        ("HelmRelease", ("deployed", "—", "Helm"))
    ]


def test_add_ons_report_an_error_only_when_nothing_can_be_listed(monkeypatch) -> None:
    monkeypatch.setattr(
        cluster, "_kubeconfig", lambda: _aws_kubeconfig(command="kubelogin")
    )

    def forbidden(path, context, query=None, accept="application/json"):
        if path == "/api/v1/namespaces":
            return {"items": []}
        raise cluster.ClusterError("secrets is forbidden: cannot list resource")

    monkeypatch.setattr(cluster, "_get_json", forbidden)
    with pytest.raises(cluster.ClusterError, match="forbidden"):
        cluster.get_resources("ctx", None, "Addon")

    _eks(monkeypatch)  # EKS still lists its own when Helm cannot be read
    _fake_aws(
        monkeypatch,
        {
            "list-addons": json.dumps({"addons": ["a"]}),
            "describe-addon": json.dumps({"addon": {"addonName": "a"}}),
        },
    )
    _, addons = cluster.get_resources("ctx", None, "Addon")
    assert [a.name for a in addons] == ["a"]


def test_a_helm_release_shows_its_revisions_without_any_secret_data(
    monkeypatch,
) -> None:
    calls = []
    _fake_cluster_api(
        monkeypatch,
        [_helm_secret("web", 2, "deployed"), _helm_secret("web", 1, "superseded")],
        calls,
    )

    details = cluster.get_resource_details("ctx", "HelmRelease", "ops", "web")

    assert details["status"] == "deployed" and details["revision"] == 2
    assert [r["revision"] for r in details["revisions"]] == [1, 2]
    assert calls[0][1] == [("labelSelector", "owner=helm,name=web")]
    assert "PartialObjectMetadataList" in calls[0][2]
    _fake_cluster_api(monkeypatch, [])
    with pytest.raises(cluster.ClusterError, match="not found"):
        cluster.get_resource_details("ctx", "HelmRelease", "ops", "gone")


def test_get_cluster_info_reads_the_describe_cluster_answer(monkeypatch) -> None:
    _eks(monkeypatch)
    answer = {
        "cluster": {
            "status": "ACTIVE",
            "version": "1.37",
            "platformVersion": "eks.4",
            "createdAt": "2026-02-11T13:16:00-03:00",
            "endpoint": "https://api.example",
            "arn": "arn:aws:eks:region:000000000000:cluster/main",
            "roleArn": "arn:aws:iam::000000000000:role/main",
            "identity": {"oidc": {"issuer": "https://oidc.example/id/1"}},
            "resourcesVpcConfig": {
                "vpcId": "vpc-1",
                "subnetIds": ["subnet-a", "subnet-b"],
                "clusterSecurityGroupId": "sg-1",
                "securityGroupIds": ["sg-2"],
                "endpointPublicAccess": True,
                "endpointPrivateAccess": False,
                "publicAccessCidrs": ["0.0.0.0/0"],
            },
            "kubernetesNetworkConfig": {
                "ipFamily": "ipv4",
                "serviceIpv4Cidr": "172.20.0.0/16",
            },
        }
    }
    commands = _fake_aws(monkeypatch, {"describe-cluster": json.dumps(answer)})

    info = cluster.get_cluster_info("ctx")

    assert commands[0][:5] == ["aws", "eks", "describe-cluster", "--name", "main"]
    assert (info.status, info.version, info.platform_version) == (
        "Active",
        "1.37",
        "eks.4",
    )
    assert info.created.startswith("2026-02-1") and info.provider == "EKS"
    assert info.endpoint == "https://api.example"
    assert info.arn.endswith("cluster/main") and info.role_arn.endswith("role/main")
    assert info.oidc_issuer == "https://oidc.example/id/1"
    assert (info.vpc_id, info.subnets) == ("vpc-1", ("subnet-a", "subnet-b"))
    assert (info.security_group, info.additional_security_groups) == ("sg-1", ("sg-2",))
    assert (info.ip_family, info.service_cidr) == ("IPv4", "172.20.0.0/16")
    assert info.endpoint_access == "Public"
    assert info.public_access_cidrs == ("0.0.0.0/0",)


@pytest.mark.parametrize(
    ("public", "private", "expected"),
    [(False, True, "Private"), (True, True, "Public and private"), (None, None, "—")],
)
def test_cluster_info_names_the_endpoint_access(monkeypatch, public, private, expected):
    _eks(monkeypatch)
    vpc = {"endpointPublicAccess": public, "endpointPrivateAccess": private}
    answer = {"cluster": {"resourcesVpcConfig": vpc}}
    _fake_aws(monkeypatch, {"describe-cluster": json.dumps(answer)})

    assert cluster.get_cluster_info("ctx").endpoint_access == expected


def test_get_cluster_info_tolerates_a_bare_answer(monkeypatch) -> None:
    _eks(monkeypatch)
    _fake_aws(monkeypatch, {"describe-cluster": json.dumps({})})

    info = cluster.get_cluster_info("ctx")

    assert (info.status, info.version, info.created, info.oidc_issuer) == ("—",) * 4
