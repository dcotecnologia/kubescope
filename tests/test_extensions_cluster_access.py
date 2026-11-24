import pytest
from kubescope.sdk import ClusterAccess, WriteModeOff, Writes
from kubescope.sdk.models import RESOURCE_KINDS

from kubescope import cluster, writes
from kubescope.extensions import cluster_access
from kubescope.extensions.cluster_access import ClusterBridge, WritesBridge


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


def test_the_window_of_a_log_is_the_one_of_the_app() -> None:
    assert ClusterBridge.LOG_WINDOW_BYTES == cluster.LOG_WINDOW_BYTES


def test_the_kinds_of_the_sdk_are_the_ones_the_app_reads_and_changes() -> None:
    """The SDK lists them so that an extension has them when it is imported;
    this is what tells that the app and the list went apart."""
    assert tuple(sorted(writes._RESOURCE_OF_KIND)) == RESOURCE_KINDS


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
        ("get_events", ("dev", ("Warning",)), "get_events", ("dev", ("Warning",))),
        (
            "get_custom_resources",
            ("dev", "a.io", "v1", "things", "ns"),
            "get_custom_resources",
            ("dev", "a.io", "v1", "things", "ns"),
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
    ("patch_custom_resource", ("dev", "a.io", "v1", "things", "ns", "x", {"a": 1})),
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


def test_the_contexts_are_the_names_of_the_kubeconfig(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "list_contexts", lambda: (["a", "b"], "a"))

    assert ClusterBridge().list_contexts() == ["a", "b"]


def test_a_context_the_person_disconnected_is_not_listed(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "list_contexts", lambda: (["a", "b", "c"], "a"))
    off = {"b"}
    bridge = ClusterBridge(lambda: off)

    assert bridge.list_contexts() == ["a", "c"]
    off.clear()  # connected again: it is asked each time
    assert bridge.list_contexts() == ["a", "b", "c"]


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        (["aws", "eks", "update-addon", "--addon-name", "x"], True),
        (["helm", "--kube-context", "c", "upgrade", "r", "chart"], True),
        (["az", "k8s-extension", "update", "--name", "x"], True),
        (["aws", "eks", "delete-cluster", "--name", "x"], False),
        (["helm", "--kube-context", "c", "uninstall", "r"], False),
        (["az", "k8s-extension", "delete", "--name", "x"], False),
        (["kubectl", "delete", "pod", "x"], False),
        ([], False),
    ],
)
def test_only_the_commands_that_update_a_plugin_are_run(
    arguments, expected, monkeypatch
) -> None:
    ran = []
    monkeypatch.setattr(
        cluster_access.plugin_updates,
        "run_update",
        lambda context, command: ran.append(command) or "ok",
    )
    bridge = WritesBridge(lambda: True)
    if expected:
        assert bridge.run_update("ctx", arguments) == "ok" and ran == [arguments]
    else:
        with pytest.raises(cluster.ClusterError):
            bridge.run_update("ctx", arguments)
        assert ran == []


def test_a_plugin_is_updated_only_with_the_write_mode_on() -> None:
    with pytest.raises(WriteModeOff):
        WritesBridge(lambda: False).run_update(
            "ctx", ["aws", "eks", "update-addon", "--addon-name", "x"]
        )


def test_the_environment_and_the_chart_of_a_release_are_the_ones_of_the_app(
    monkeypatch,
) -> None:
    monkeypatch.setattr(cluster, "context_environment", lambda context: {"A": context})
    monkeypatch.setattr(cluster, "helm_chart_name", lambda *args: "-".join(args))
    assert ClusterBridge().environment("ctx") == {"A": "ctx"}
    assert ClusterBridge().helm_chart_name("c", "n", "r") == "c-n-r"
