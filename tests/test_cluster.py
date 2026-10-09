import json
from datetime import UTC, datetime

from kubescope import cluster


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
