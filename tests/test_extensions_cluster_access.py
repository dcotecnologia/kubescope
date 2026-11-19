import pytest

from kubescope import cluster, writes
from kubescope.extensions import cluster_access
from kubescope.extensions.cluster_access import ClusterBridge, WritesBridge
from kubescope.sdk import ClusterAccess, WriteModeOff, Writes


def names(protocol: type) -> set[str]:
    return {
        name
        for name in {*vars(protocol), *getattr(protocol, "__annotations__", {})}
        if not name.startswith("_")
    }


def test_the_bridges_offer_everything_the_sdk_describes_and_nothing_more() -> None:
    assert names(ClusterAccess) <= {
        n for n in dir(ClusterBridge) if not n.startswith("_")
    }
    assert names(Writes) == {n for n in dir(WritesBridge) if not n.startswith("_")}


def test_the_kinds_and_the_window_of_a_log_are_the_ones_of_the_app() -> None:
    assert ClusterBridge.KINDS == writes.RESOURCE_KINDS
    assert (
        tuple(sorted(ClusterBridge.KINDS)) == ClusterBridge.KINDS
        and ClusterBridge.KINDS
    )
    assert ClusterBridge.LOG_WINDOW_BYTES == cluster.LOG_WINDOW_BYTES


@pytest.mark.parametrize(
    ("method", "arguments", "target", "expected"),
    [
        ("get_pods", ("dev", "ns"), "get_pods", ("dev", "ns")),
        ("get_pods", ("dev",), "get_pods", ("dev", None)),
        (
            "get_pod_container_usage",
            ("dev", "ns", "p"),
            "get_pod_container_usage",
            ("dev", "ns", "p"),
        ),
        ("get_usage", ("dev", "ns"), "get_usage", ("dev", "ns")),
        ("get_usage", ("dev",), "get_usage", ("dev", None)),
        (
            "get_resources",
            ("dev", "ns", "Secret"),
            "get_resources",
            ("dev", "ns", "Secret"),
        ),
        (
            "get_resource_details",
            ("dev", "Pod", "ns", "p"),
            "get_resource_details",
            ("dev", "Pod", "ns", "p"),
        ),
        ("describe_kube", (), "describe_kube", ()),
    ],
)
def test_a_read_goes_to_the_function_of_the_app_that_does_it(
    monkeypatch, method, arguments, target, expected
) -> None:
    seen: list = []
    monkeypatch.setattr(cluster, target, lambda *a: seen.append(a) or "answer")

    assert getattr(ClusterBridge(), method)(*arguments) == "answer"

    assert seen == [expected]


def test_workloads_use_the_kinds_of_the_app_unless_some_are_asked_for(
    monkeypatch,
) -> None:
    seen: list = []
    monkeypatch.setattr(cluster, "get_workloads", lambda *a: seen.append(a) or "w")

    ClusterBridge().get_workloads("dev", "ns")
    ClusterBridge().get_workloads("dev", None, ("Deployment",))

    assert seen == [("dev", "ns"), ("dev", None, ("Deployment",))]


def test_the_log_of_a_pod_passes_every_option(monkeypatch) -> None:
    seen: list = []
    monkeypatch.setattr(cluster, "get_pod_logs", lambda *a: seen.append(a) or "log")

    result = ClusterBridge().get_pod_logs(
        "dev", "ns", "pod", "app", 10, "2026-01-01T00:00:00Z", 60, 1000
    )

    assert result == "log"
    assert seen == [("dev", "ns", "pod", "app", 10, "2026-01-01T00:00:00Z", 60, 1000)]
    ClusterBridge().get_pod_logs("dev", "ns", "pod", "app")
    assert seen[1] == ("dev", "ns", "pod", "app", 500, None, 0, 0)


CHANGES = [
    ("scale_deployment", ("dev", "ns", "web", 3)),
    ("restart_deployment", ("dev", "ns", "web")),
    ("evict_pod", ("dev", "ns", "p")),
    ("delete_pod", ("dev", "ns", "p")),
    ("delete_resource", ("dev", "Secret", "ns", "s")),
    ("replace_resource", ("dev", "Secret", "ns", "s", {"kind": "Secret"})),
]


@pytest.mark.parametrize(("method", "arguments"), CHANGES)
def test_a_change_is_made_only_with_the_write_mode_on(
    monkeypatch, method, arguments
) -> None:
    seen: list = []
    monkeypatch.setattr(writes, method, lambda *a: seen.append(a))

    with pytest.raises(WriteModeOff):
        getattr(WritesBridge(lambda: False), method)(*arguments)
    assert seen == []

    getattr(WritesBridge(lambda: True), method)(*arguments)
    assert seen == [arguments]


def test_the_module_keeps_to_the_cluster_and_the_writes_of_the_app() -> None:
    assert cluster_access.cluster is cluster and cluster_access.writes is writes
