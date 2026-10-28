import json
import shlex
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from kubescope import cluster, writes
from kubescope.cluster import ClusterError


class Recorder:
    """A local HTTP server standing in for a cluster that records every
    request."""

    def __init__(self, monkeypatch, tmp_path) -> None:
        self.requests: list[dict] = []
        self.status = 200
        self.reply = b"{}"
        self.accept_token: str | None = None
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def handle_any(self) -> None:
                size = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(size)
                token = self.headers.get("Authorization")
                outer.requests.append(
                    {
                        "method": self.command,
                        "path": self.path,
                        "type": self.headers.get("Content-Type"),
                        "body": json.loads(body) if body else None,
                        "token": token,
                    }
                )
                status, reply = outer.status, outer.reply
                if outer.accept_token and token != outer.accept_token:
                    status, reply = 401, b'{"message": "Unauthorized"}'
                self.send_response(status)
                self.end_headers()
                self.wfile.write(reply)

            do_DELETE = do_POST = do_PATCH = do_PUT = handle_any

            def log_message(self, format: str, *args: object) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        kubeconfig = tmp_path / "kubeconfig"
        kubeconfig.write_text(
            json.dumps(
                {
                    "current-context": "dev",
                    "contexts": [
                        {"name": "dev", "context": {"cluster": "c", "user": "u"}}
                    ],
                    "clusters": [
                        {
                            "name": "c",
                            "cluster": {
                                "server": f"http://127.0.0.1:{self.server.server_port}"
                            },
                        }
                    ],
                    "users": [{"name": "u", "user": {"token": "fake-token"}}],
                }
            )
        )
        monkeypatch.setenv("KUBECONFIG", str(kubeconfig))
        monkeypatch.setenv("NO_PROXY", "127.0.0.1")


@pytest.fixture
def server(monkeypatch, tmp_path):
    recorder = Recorder(monkeypatch, tmp_path)
    yield recorder
    recorder.server.shutdown()
    recorder.server.server_close()


def test_delete_pod_sends_a_delete(server) -> None:
    writes.delete_pod("dev", "ops", "api-1")

    assert server.requests == [
        {
            "method": "DELETE",
            "path": "/api/v1/namespaces/ops/pods/api-1",
            "type": "application/json",
            "body": None,
            "token": "Bearer fake-token",
        }
    ]


def test_delete_resource_sends_a_delete(server) -> None:
    writes.delete_resource("dev", "Deployment", "ops", "api")
    writes.delete_resource("dev", "PriorityClass", "", "high")

    assert [r["method"] + " " + r["path"] for r in server.requests] == [
        "DELETE /apis/apps/v1/namespaces/ops/deployments/api",
        "DELETE /apis/scheduling.k8s.io/v1/priorityclasses/high",
    ]


def test_replace_resource_puts_the_document(server) -> None:
    writes.replace_resource("dev", "Event", "ops", "e1", {"kind": "Event"})

    request = server.requests[0]
    assert request["method"] == "PUT"
    assert request["path"] == "/api/v1/namespaces/ops/events/e1"
    assert request["body"] == {"kind": "Event"}


def test_replace_resource_refuses_an_unknown_kind() -> None:
    with pytest.raises(ValueError, match="Cannot edit a Node"):
        writes.replace_resource("dev", "Node", "", "n1", {})


def test_delete_resource_refuses_an_unknown_kind() -> None:
    with pytest.raises(ValueError, match="Cannot delete a Node"):
        writes.delete_resource("dev", "Node", "", "n1")


def test_evict_pod_posts_an_eviction(server) -> None:
    writes.evict_pod("dev", "ops", "api-1")

    request = server.requests[0]
    assert request["method"] == "POST"
    assert request["path"] == "/api/v1/namespaces/ops/pods/api-1/eviction"
    assert request["body"] == {
        "apiVersion": "policy/v1",
        "kind": "Eviction",
        "metadata": {"name": "api-1", "namespace": "ops"},
    }


def test_scale_deployment_patches_the_scale(server) -> None:
    writes.scale_deployment("dev", "ops", "api", 5)

    request = server.requests[0]
    assert request["method"] == "PATCH"
    assert request["path"] == "/apis/apps/v1/namespaces/ops/deployments/api/scale"
    assert request["type"] == "application/merge-patch+json"
    assert request["body"] == {"spec": {"replicas": 5}}


@pytest.mark.parametrize("replicas", [-1, writes.MAX_REPLICAS + 1])
def test_scale_deployment_refuses_an_impossible_count(server, replicas) -> None:
    with pytest.raises(ValueError, match="between"):
        writes.scale_deployment("dev", "ops", "api", replicas)

    assert server.requests == []


def test_restart_deployment_stamps_the_pod_template(server) -> None:
    writes.restart_deployment("dev", "ops", "api")

    request = server.requests[0]
    assert request["path"] == "/apis/apps/v1/namespaces/ops/deployments/api"
    assert request["type"] == "application/strategic-merge-patch+json"
    stamp = request["body"]["spec"]["template"]["metadata"]["annotations"][
        writes.RESTARTED_AT
    ]
    assert stamp.endswith("Z") and "T" in stamp


def test_names_are_encoded_in_the_path(server) -> None:
    writes.delete_pod("dev", "ops", "a/b")

    assert server.requests[0]["path"] == "/api/v1/namespaces/ops/pods/a%2Fb"


def test_a_refusal_is_explained_like_kubectl_does(server) -> None:
    server.status = 403
    server.reply = b'{"kind": "Status", "message": "pods is forbidden: cannot delete"}'

    with pytest.raises(ClusterError, match="forbidden: cannot delete"):
        writes.delete_pod("dev", "ops", "api-1")


def test_a_refused_token_signs_in_again_once(server) -> None:
    server.accept_token = "Bearer other"

    with pytest.raises(ClusterError, match="Unauthorized"):
        writes.delete_pod("dev", "ops", "api-1")

    assert len(server.requests) == 2  # the retry with a fresh client


def test_a_cluster_that_cannot_be_reached_is_reported(server) -> None:
    server.server.shutdown()
    server.server.server_close()

    with pytest.raises(ClusterError, match="(?i)refused|failed to establish"):
        writes.delete_pod("dev", "ops", "api-1")


def test_a_tls_error_of_the_client_is_reported(monkeypatch) -> None:
    def failing(_api, *_a, **_k):
        raise cluster.ApiException(status=0, reason="SSLError handshake")

    monkeypatch.setattr(cluster.client.ApiClient, "call_api", failing)
    monkeypatch.setattr(cluster, "_api_client", lambda _c: cluster.client.ApiClient())

    with pytest.raises(ClusterError, match="SSLError handshake"):
        writes.delete_pod("dev", "ops", "api-1")


def test_a_request_that_never_answers_times_out(monkeypatch) -> None:
    release = threading.Event()
    monkeypatch.setattr(cluster, "REQUEST_TIMEOUT", 0.1)
    monkeypatch.setattr(writes, "_send", lambda *_a: release.wait(5))

    with pytest.raises(ClusterError, match="timed out"):
        writes.delete_pod("dev", "ops", "api-1")
    release.set()


def _on(monkeypatch, platform: str) -> None:
    monkeypatch.setattr(writes.sys, "platform", platform)


def test_the_shell_command_is_complete_and_ready_to_paste(monkeypatch) -> None:
    for platform in ("linux", "darwin"):
        _on(monkeypatch, platform)

        [(shell, command)] = writes.shell_commands("dev", "ops", "api-1", "app")

        assert shell == ""  # one shell: no name
        assert command.startswith(
            "kubectl --context dev --namespace ops exec -it api-1 -c app -- sh -c "
        )
        assert shlex.split(command)[-1] == writes._SHELL  # quoted as one argument


def test_the_shell_command_quotes_names_with_odd_characters(monkeypatch) -> None:
    _on(monkeypatch, "linux")

    [(_, command)] = writes.shell_commands(
        "arn:aws:eks:r:1:cluster/my cl", "ops", "p", "c"
    )

    assert shlex.split(command)[2] == "arn:aws:eks:r:1:cluster/my cl"


def test_on_windows_there_is_a_version_for_powershell_and_one_for_cmd(
    monkeypatch,
) -> None:
    _on(monkeypatch, "win32")

    versions = dict(writes.shell_commands("dev", "ops", "api-1", "app"))

    assert list(versions) == ["PowerShell", "cmd"]
    assert versions["PowerShell"] == (
        "kubectl --context dev --namespace ops exec -it api-1 -c app -- sh -c "
        "'command -v bash >/dev/null 2>&1 && exec bash || exec sh'"
    )
    assert versions["cmd"] == (
        "kubectl --context dev --namespace ops exec -it api-1 -c app -- sh -c "
        '"command -v bash >/dev/null 2>&1 && exec bash || exec sh"'
    )


def test_powershell_quotes_what_is_not_plain() -> None:
    assert writes._powershell_quote("dev-1.x:80") == "dev-1.x:80"
    assert writes._powershell_quote("my cluster") == "'my cluster'"
    assert writes._powershell_quote("it's") == "'it''s'"
    assert writes._powershell_quote("") == "''"


def test_one_kubeconfig_file_goes_in_the_flag_on_every_system(monkeypatch) -> None:
    cluster.configure(kubeconfig_files=["/a/my config"])

    for platform in ("linux", "darwin"):
        _on(monkeypatch, platform)
        [(_, command)] = writes.shell_commands("dev", "ops", "api-1", "app")
        assert shlex.split(command)[:3] == ["kubectl", "--kubeconfig", "/a/my config"]

    _on(monkeypatch, "win32")
    cluster.configure(kubeconfig_files=["C:\\my k\\config"])
    versions = dict(writes.forward_commands("dev", "ops", "api", 80, 8080))
    assert versions["PowerShell"].startswith(
        "kubectl --kubeconfig 'C:\\my k\\config' --context dev"
    )
    assert versions["cmd"].startswith(
        'kubectl --kubeconfig "C:\\my k\\config" --context dev'
    )


def test_several_kubeconfig_files_are_set_the_way_each_shell_does(monkeypatch) -> None:
    cluster.configure(kubeconfig_files=["/a/config", "/b/my config"])
    joined = "/a/config" + cluster.os.pathsep + "/b/my config"

    for platform in ("linux", "darwin"):
        _on(monkeypatch, platform)
        [(_, command)] = writes.shell_commands("dev", "ops", "api-1", "app")
        assert shlex.split(command)[:2] == [f"KUBECONFIG={joined}", "kubectl"]

    _on(monkeypatch, "win32")
    versions = dict(writes.shell_commands("dev", "ops", "api-1", "app"))
    assert versions["PowerShell"].startswith(
        f"$env:KUBECONFIG = '{joined}'; kubectl --context dev"
    )
    assert versions["cmd"].startswith(
        f'set "KUBECONFIG={joined}" && kubectl --context dev'
    )


def test_service_ports_keeps_the_tcp_ones_with_their_names() -> None:
    document = {
        "spec": {
            "ports": [
                {"port": 80, "name": "http", "protocol": "TCP"},
                {"port": 443},  # TCP when it says nothing
                {"port": 53, "protocol": "UDP"},  # cannot be forwarded
                {"port": "web"},  # not a number
            ]
        }
    }

    assert writes.service_ports(document) == [(80, "80 (http)"), (443, "443")]
    assert writes.service_ports({}) == []


def test_container_ports_reads_a_pod_or_a_pod_template() -> None:
    containers = [
        {
            "ports": [
                {"containerPort": 80, "name": "http"},
                {"containerPort": 53, "protocol": "UDP"},
            ]
        },
        {"ports": [{"containerPort": 80}, {"containerPort": 9090}]},
        {},
    ]

    expected = [(80, "80 (http)"), (9090, "9090")]
    assert writes.container_ports({"spec": {"containers": containers}}) == expected
    template = {"spec": {"template": {"spec": {"containers": containers}}}}
    assert writes.container_ports(template) == expected
    assert writes.container_ports({}) == []


def test_container_ports_adds_the_ports_the_services_send_to_the_pod() -> None:
    pod = {
        "metadata": {"labels": {"app": "api", "tier": "web"}},
        "spec": {"containers": [{"ports": [{"containerPort": 8080, "name": "http"}]}]},
    }
    services = [
        {  # selects the Pod: a number, a name of the Pod, an unknown name, UDP
            "metadata": {"name": "api"},
            "spec": {
                "selector": {"app": "api"},
                "ports": [
                    {"port": 80, "targetPort": 3000},
                    {"port": 81, "targetPort": "http"},
                    {"port": 82, "targetPort": "nope"},
                    {"port": 83, "targetPort": 9000, "protocol": "UDP"},
                    {"port": 5432},
                ],
            },
        },
        {  # another app
            "metadata": {"name": "other"},
            "spec": {
                "selector": {"app": "web"},
                "ports": [{"port": 1, "targetPort": 1}],
            },
        },
        {"metadata": {"name": "any"}, "spec": {"ports": [{"port": 2}]}},  # no selector
    ]

    assert writes.container_ports(pod, services) == [
        (8080, "8080 (http)"),
        (3000, "3000 (Service api)"),
        (5432, "5432 (Service api)"),
    ]
    template = {
        "spec": {"template": {"metadata": pod["metadata"], "spec": pod["spec"]}}
    }
    assert writes.container_ports(template, services) == writes.container_ports(
        pod, services
    )


def test_the_forward_command_names_the_kind_it_forwards_to(monkeypatch) -> None:
    _on(monkeypatch, "linux")

    [(_, command)] = writes.forward_commands("d", "ops", "db-0", 5432, 5432, "pod")

    assert command.endswith("port-forward pod/db-0 5432:5432")


def test_the_forward_command_is_complete_and_ready_to_paste(monkeypatch) -> None:
    _on(monkeypatch, "linux")

    [(_, command)] = writes.forward_commands("dev", "ops", "api", 80, 8080)

    assert command == (
        "kubectl --context dev --namespace ops port-forward service/api 8080:80"
    )

    _on(monkeypatch, "win32")
    versions = dict(writes.forward_commands("dev", "ops", "api", 80, 8080))
    expected = "kubectl --context dev --namespace ops port-forward service/api 8080:80"
    assert versions == {"PowerShell": expected, "cmd": expected}


def _review(allowed) -> bytes:
    return json.dumps({"status": {"allowed": allowed}}).encode()


def test_allowed_actions_asks_one_access_review_for_each_button(monkeypatch) -> None:
    sent = []

    def write(method, path, context, body, content_type=""):
        sent.append((method, path, context, body["spec"]["resourceAttributes"]))
        attributes = body["spec"]["resourceAttributes"]
        return _review(attributes.get("subresource") != "eviction")

    monkeypatch.setattr(writes, "_write", write)

    allowed = writes.allowed_actions("prod", "ops")

    assert allowed == {"shell", "delete", "scale", "reload", "forward", "edit"}
    assert {s[:3] for s in sent} == {
        ("POST", "/apis/authorization.k8s.io/v1/selfsubjectaccessreviews", "prod")
    }
    assert sent[0][3] == {
        "namespace": "ops",
        "verb": "create",
        "group": "",
        "resource": "pods",
        "subresource": "exec",
    }
    assert sent[3][3]["group"] == "apps"
    assert "subresource" not in sent[2][3]  # deleting a Pod


def test_a_review_that_fails_leaves_its_button_in(monkeypatch) -> None:
    answers = iter(
        [
            ClusterError("forbidden"),
            b"not json",
            b"{}",
            _review(False),
            _review(None),
            _review(True),
            _review(True),
        ]
    )

    def write(*_args, **_kwargs):
        answer = next(answers)
        if isinstance(answer, Exception):
            raise answer
        return answer

    monkeypatch.setattr(writes, "_write", write)

    # shell, evict and delete could not be told, scale is refused
    assert writes.allowed_actions("prod", "ops") == {
        "shell",
        "evict",
        "delete",
        "reload",
        "forward",
        "edit",
    }


def test_the_review_goes_through_the_write_path(monkeypatch) -> None:
    calls = []

    def background(call, _timeout):
        calls.append(call)
        return b"{}"

    monkeypatch.setattr(writes.cluster, "_in_background", background)

    assert writes._write("POST", "/p", "dev", {}) == b"{}"
    assert len(calls) == 1
