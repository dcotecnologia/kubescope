import json
import sys
import threading
import time
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from kubescope import cluster
from kubescope.models import PodInfo


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


def test_get_workloads_uses_kubectl_json(monkeypatch) -> None:
    responses = iter(
        [
            {"items": [{"metadata": {"name": "default"}}]},
            {
                "items": [
                    {
                        "kind": "DaemonSet",
                        "metadata": {"name": "agent", "namespace": "default"},
                        "status": {
                            "desiredNumberScheduled": 2,
                            "numberReady": 2,
                        },
                    }
                ]
            },
        ]
    )
    commands = []

    def fake_get_json(*arguments: str, context: str) -> dict:
        commands.append((arguments, context))
        return next(responses)

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    namespaces, workloads = cluster.get_workloads("dev")

    assert namespaces == ["default"]
    assert [workload.name for workload in workloads] == ["agent"]
    assert commands == [
        (("get", "namespaces"), "dev"),
        (("get", "deployments,statefulsets,daemonsets", "-A"), "dev"),
    ]


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

    def fake_get_json(*arguments: str, context: str) -> dict:
        commands.append((arguments, context))
        return next(responses)

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)
    workload = cluster.Workload("production", "Deployment", "api", 1, 1, "1h")

    pods = cluster.get_workload_pods("dev", workload)

    assert [
        (pod.name, pod.phase, pod.ready, pod.total, pod.containers) for pod in pods
    ] == [("api-abc", "Running", 1, 1, ("api",))]
    assert commands == [
        (("get", "deployment", "api", "-n", "production"), "dev"),
        (
            (
                "get",
                "pods",
                "-n",
                "production",
                "-l",
                "app=api,tier in (backend,worker)",
            ),
            "dev",
        ),
    ]


def test_get_resource_details_returns_json_document(monkeypatch) -> None:
    expected = {"kind": "Deployment", "metadata": {"name": "api"}}
    commands = []

    def fake_get_json(*arguments: str, context: str) -> dict:
        commands.append((arguments, context))
        return expected

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)

    result = cluster.get_resource_details("dev", "Deployment", "production", "api")

    assert result == expected
    assert commands == [(("get", "deployment", "api", "-n", "production"), "dev")]


def test_get_pod_logs_selects_container_and_caps_lines(monkeypatch) -> None:
    commands = []

    def fake_run_kubectl(*arguments: str, context: str | None = None) -> str:
        commands.append((arguments, context))
        return "2026-10-08T00:00:00Z started"

    monkeypatch.setattr(cluster, "_run_kubectl", fake_run_kubectl)

    logs = cluster.get_pod_logs("dev", "production", "api-abc", "api")

    assert logs == "2026-10-08T00:00:00Z started"
    assert commands == [
        (
            (
                "logs",
                "api-abc",
                "-n",
                "production",
                "-c",
                "api",
                "--tail=500",
                "--timestamps",
            ),
            "dev",
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
    def fake_get_json(*arguments: str, context: str) -> dict:
        if arguments[1] == "nodes":
            raise cluster.KubectlError("forbidden")
        return {"items": []}

    def no_metrics(*_args: object, **_kwargs: object) -> str:
        raise cluster.KubectlError("no metrics")

    monkeypatch.setattr(cluster, "_get_json", fake_get_json)
    monkeypatch.setattr(cluster, "_run_kubectl", no_metrics)

    overview = cluster.get_cluster_overview("ctx")

    assert overview.warnings == ("Nodes: forbidden",)
    assert overview.metrics_available is False
    assert overview.nodes == ()
    assert overview.pods_total == 0


def test_get_cluster_overview_fails_when_nothing_is_readable(monkeypatch) -> None:
    def fail(*_args: object, **_kwargs: object) -> dict:
        raise cluster.KubectlError("unreachable")

    monkeypatch.setattr(cluster, "_get_json", fail)
    monkeypatch.setattr(cluster, "_run_kubectl", fail)

    try:
        cluster.get_cluster_overview("ctx")
    except cluster.KubectlError as error:
        assert "unreachable" in str(error)
    else:
        raise AssertionError("expected KubectlError")


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
    monkeypatch.setattr(
        cluster,
        "_get_json",
        lambda *a, context: {"items": [pod]} if "pods" in a else {"items": []},
    )
    monkeypatch.setattr(
        cluster, "_run_kubectl", lambda *a, context: json.dumps(metrics)
    )

    _, pods = cluster.get_pods("dev")
    assert (pods[0].restarts, pods[0].cpu, pods[0].memory) == (3, 0.25, 128 * 2**20)
    assert pods[0].owner == ("Deployment", "api")
    usage = cluster.get_usage("dev")
    assert usage[("default", "Deployment", "api")] == (3, 0.25, 128 * 2**20)

    def no_metrics(*_a, context):
        raise cluster.KubectlError("no metrics")

    monkeypatch.setattr(cluster, "_run_kubectl", no_metrics)
    assert cluster.get_pods("dev")[1][0].cpu is None


def test_kubectl_executable_in_the_source_tree_and_in_a_bundle(
    monkeypatch, tmp_path
) -> None:
    source = cluster.kubectl_executable()
    assert source.parts[-3:] == ("vendor", "kubectl", "kubectl")

    monkeypatch.setattr(cluster, "os", SimpleNamespace(name="nt"))
    monkeypatch.setattr(cluster.sys, "frozen", True, raising=False)
    monkeypatch.setattr(cluster.sys, "_MEIPASS", str(tmp_path), raising=False)
    assert cluster.kubectl_executable() == tmp_path / "kubectl" / "kubectl.exe"


def _fake_kubectl(monkeypatch, tmp_path, run):
    executable = tmp_path / "kubectl"
    executable.write_text("")
    monkeypatch.setattr(cluster, "kubectl_executable", lambda: executable)
    monkeypatch.setattr(cluster, "_run_process", run)
    return executable


def test_run_kubectl_builds_the_command_and_returns_stdout(
    monkeypatch, tmp_path
) -> None:
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs))
        return cluster.subprocess.CompletedProcess(command, 0, "out\n", "")

    executable = _fake_kubectl(monkeypatch, tmp_path, run)

    assert cluster._run_kubectl("get", "pods", context="prod") == "out\n"
    assert calls[0][0] == [str(executable), "--context", "prod", "get", "pods"]
    assert calls[0][1]["timeout"] == 45
    cluster._run_kubectl("version")
    assert calls[1][0] == [str(executable), "version"]


def test_run_kubectl_reports_every_failure(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(cluster, "kubectl_executable", lambda: tmp_path / "missing")
    with pytest.raises(cluster.KubectlError, match="missing"):
        cluster._run_kubectl("get")

    def failing(returncode, stdout, stderr):
        def run(command, **_kwargs):
            return cluster.subprocess.CompletedProcess(
                command, returncode, stdout, stderr
            )

        return run

    for run, message in (
        (failing(1, "", " denied \n"), "denied"),
        (failing(1, "from stdout", ""), "from stdout"),
        (failing(3, "", ""), "exited with 3"),
    ):
        _fake_kubectl(monkeypatch, tmp_path, run)
        with pytest.raises(cluster.KubectlError, match=message):
            cluster._run_kubectl("get")

    def timeout(command, **_kwargs):
        raise cluster.subprocess.TimeoutExpired(command, 45)

    def broken(_command, **_kwargs):
        raise OSError("exec format error")

    _fake_kubectl(monkeypatch, tmp_path, timeout)
    with pytest.raises(cluster.KubectlError, match="timed out"):
        cluster._run_kubectl("get")
    _fake_kubectl(monkeypatch, tmp_path, broken)
    with pytest.raises(cluster.KubectlError, match="Could not start"):
        cluster._run_kubectl("get")


def test_get_json_rejects_documents_that_are_not_objects(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_run_kubectl", lambda *_a, **_k: '{"a": 1}')
    assert cluster._get_json("get", "x", context="c") == {"a": 1}

    monkeypatch.setattr(cluster, "_run_kubectl", lambda *_a, **_k: "[1]")
    with pytest.raises(cluster.KubectlError, match="unexpected JSON"):
        cluster._get_json("get", "x", context="c")


def test_list_contexts_returns_names_and_the_active_one(monkeypatch) -> None:
    outputs = {"get-contexts": "a\n\n b \n", "current-context": " b \n"}
    monkeypatch.setattr(
        cluster, "_run_kubectl", lambda *arguments, **_k: outputs[arguments[1]]
    )
    assert cluster.list_contexts() == (["a", "b"], "b")

    monkeypatch.setattr(cluster, "_run_kubectl", lambda *_a, **_k: "\n")
    assert cluster.list_contexts() == ([], None)

    monkeypatch.setattr(
        cluster,
        "_run_kubectl",
        lambda *arguments, **_k: "a\n" if arguments[1] == "get-contexts" else "\n",
    )
    assert cluster.list_contexts() == (["a"], None)


def test_parse_workload_skips_unknown_kinds_and_handles_daemon_sets() -> None:
    now = datetime(2025, 1, 1, tzinfo=UTC)

    assert (
        cluster._parse_workload({"kind": "Job", "metadata": {"name": "x"}}, now) is None
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


def test_get_resource_details_rejects_unsupported_kinds() -> None:
    with pytest.raises(cluster.KubectlError, match="Unsupported resource kind"):
        cluster.get_resource_details("c", "Job", "ns", "x")


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
    with pytest.raises(cluster.KubectlError, match=message):
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

    assert cluster.get_usage("ctx") == {("ns", "Deployment", "api"): (2, 0.5, 100.0)}


def _aws_kubeconfig(arguments=None, env=None, command="/usr/local/bin/aws") -> dict:
    exec_block = {"command": command, "args": arguments or [], "env": env}
    return {"users": [{"user": {"exec": exec_block}}]}


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
        with pytest.raises(cluster.KubectlError, match=message):
            cluster._run_command(["aws", "x"], 5)

    def timeout(command, **_kwargs):
        raise cluster.subprocess.TimeoutExpired(command, 5)

    def missing(_command, **_kwargs):
        raise OSError("not found")

    monkeypatch.setattr(cluster, "_run_process", timeout)
    with pytest.raises(cluster.KubectlError, match="timed out"):
        cluster._run_command(["aws"], 5)
    monkeypatch.setattr(cluster, "_run_process", missing)
    with pytest.raises(cluster.KubectlError, match="Could not start aws"):
        cluster._run_command(["aws"], 5)


def test_aws_profile_is_read_from_the_kubeconfig_exec_entry(monkeypatch) -> None:
    def config(document):
        monkeypatch.setattr(cluster, "_get_json", lambda *_a, **_k: document)

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
    assert cluster.login_action("ctx") is None


def test_sso_profiles_are_told_apart_from_access_key_profiles(monkeypatch) -> None:
    answers = {"sso_session": "", "sso_start_url": "https://example.awsapps.com/start"}

    def configure(command, _timeout):
        assert command[:3] == ["aws", "configure", "get"]
        assert command[4:] == ["--profile", "work"]
        value = answers[command[3]]
        if value is None:
            raise cluster.KubectlError("not set")
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
    monkeypatch.setattr(cluster, "_run_kubectl", lambda *a, **_k: calls.append(a) or "")
    monkeypatch.setattr(cluster, "_run_command", lambda c, _t: calls.append(c) or "")

    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (False, None))
    assert cluster.check_login("ctx") == (False, None)

    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, "work"))
    assert cluster.check_login("ctx") == (False, None)
    assert ["aws", "sts", "get-caller-identity", "--profile", "work"] in calls


def test_check_login_detects_expired_sso_and_bad_access_keys(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "login_action", lambda _c: SSO)

    def kubectl_fails(*_a, **_k):
        raise cluster.KubectlError("Error: the SSO session has expired")

    monkeypatch.setattr(cluster, "_run_kubectl", kubectl_fails)
    assert cluster.check_login("ctx") == (True, SSO)

    monkeypatch.setattr(cluster, "_run_kubectl", lambda *_a, **_k: "")
    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, None))

    def sts_fails(*_a):
        raise cluster.KubectlError("InvalidClientTokenId: the token is invalid")

    monkeypatch.setattr(cluster, "_run_command", sts_fails)
    monkeypatch.setattr(cluster, "login_action", lambda _c: KEYS)
    assert cluster.check_login("ctx") == (True, KEYS)

    monkeypatch.setattr(cluster, "login_action", lambda _c: None)  # not AWS
    assert cluster.check_login("ctx") == (True, None)

    def unreadable(_context):
        raise cluster.KubectlError("config view failed")

    monkeypatch.setattr(cluster, "login_action", unreadable)
    assert cluster.check_login("ctx") == (True, None)


def test_check_login_ignores_failures_that_are_not_about_credentials(
    monkeypatch,
) -> None:
    def unreachable(*_a, **_k):
        raise cluster.KubectlError("Unable to connect: i/o timeout")

    monkeypatch.setattr(cluster, "_run_kubectl", unreachable)
    assert cluster.check_login("ctx") == (False, None)

    monkeypatch.setattr(cluster, "_run_kubectl", lambda *_a, **_k: "")
    monkeypatch.setattr(cluster, "_aws_profile", lambda _c: (True, None))

    def no_cli(*_a):
        raise cluster.KubectlError("Could not start aws: not found")

    monkeypatch.setattr(cluster, "_run_command", no_cli)
    assert cluster.check_login("ctx") == (False, None)

    def broken_json(*_a, **_k):
        raise ValueError("expired token in a bad document")

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
    with pytest.raises(cluster.KubectlError, match="aws configure"):
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
    with pytest.raises(cluster.KubectlError, match="Could not open a terminal"):
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
    monkeypatch.setattr(cluster, "_run_kubectl", lambda *_a, **_k: "")
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
        raise cluster.KubectlError("Unable to connect: i/o timeout")

    monkeypatch.setattr(cluster, "_run_kubectl", fail)
    cluster.check_login("ctx")
    assert "not a credentials problem" in caplog.text
