from datetime import datetime, timezone

from kubectl_gui import cluster


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
        datetime(2025, 1, 1, 0, 2, tzinfo=timezone.utc),
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
