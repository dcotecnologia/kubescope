import argparse
import json
import sys
from types import SimpleNamespace

import pytest

from kubescope import cli, cli_cluster, cluster, writes
from kubescope.cluster import ClusterError, LoginAction
from kubescope.models import ClusterResource, NodeInfo, PodInfo, Workload


class FakeSettings:
    write_mode = True
    kubeconfig_files: list[str] = []
    sign_in_commands: dict[str, str] = {}


@pytest.fixture(autouse=True)
def fakes(monkeypatch):
    monkeypatch.setattr(cli_cluster, "Settings", FakeSettings)
    monkeypatch.setattr(cluster, "configure", lambda *_: None)
    monkeypatch.setattr(cluster, "list_contexts", lambda: (["a", "b"], "b"))
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    FakeSettings.write_mode = True


def _tty(monkeypatch, *answers):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    given = iter(answers)
    monkeypatch.setattr(cli_cluster, "_ask", lambda _prompt: next(given))


POD = PodInfo("ns", "web", "Running", 1, 2, "3d", ("c",), restarts=4, node="n1")


def test_contexts_table_and_json(capsys):
    assert cli.run(["contexts"]) == 0
    assert "*" in capsys.readouterr().out
    assert cli.run(["contexts", "-o", "json"]) == 0
    assert json.loads(capsys.readouterr().out)[1] == {"name": "b", "current": True}


def test_pods_table(monkeypatch, capsys):
    seen = []
    monkeypatch.setattr(
        cluster, "get_pods", lambda ctx, ns: seen.append((ctx, ns)) or ([], [POD])
    )
    assert cli.run(["pods", "--context", "a", "-n", "ns"]) == 0
    out = capsys.readouterr().out
    assert seen == [("a", "ns")]
    assert "web" in out and "1/2" in out and "n1" in out


def test_pods_yaml_and_empty(monkeypatch, capsys):
    monkeypatch.setattr(cluster, "get_pods", lambda *_: ([], [POD]))
    assert cli.run(["pods", "--context", "a", "-o", "yaml"]) == 0
    assert "name: web" in capsys.readouterr().out
    monkeypatch.setattr(cluster, "get_pods", lambda *_: ([], []))
    assert cli.run(["pods", "--context", "a"]) == 0
    assert "No resources found" in capsys.readouterr().err


def test_workloads(monkeypatch, capsys):
    seen = []
    monkeypatch.setattr(
        cluster,
        "get_workloads",
        lambda ctx, ns, kinds: (
            seen.append(kinds)
            or ([], [Workload("ns", "Deployment", "api", 1, 2, "1d")])
        ),
    )
    assert cli.run(["workloads", "--context", "a"]) == 0
    assert "api" in capsys.readouterr().out
    assert cli.run(["workloads", "--context", "a", "--kind", "DaemonSet"]) == 0
    assert seen == [("Deployment", "StatefulSet", "DaemonSet"), ("DaemonSet",)]


def test_nodes_with_warnings(monkeypatch, capsys):
    node = NodeInfo("n1", True, "worker", "v1", "2d", 2.0, 4.0, 10, 3)
    overview = SimpleNamespace(nodes=(node,), warnings=("no metrics",))
    monkeypatch.setattr(cluster, "get_cluster_overview", lambda ctx: overview)
    assert cli.run(["nodes", "--context", "a"]) == 0
    captured = capsys.readouterr()
    assert "Ready" in captured.out and "3/10" in captured.out
    assert "no metrics" in captured.err
    overview.nodes = (NodeInfo("n2", False, "", "v1", "1d", 1.0, 1.0, 1),)
    assert cli.run(["nodes", "--context", "a"]) == 0
    assert "NotReady" in capsys.readouterr().out


def test_events(monkeypatch, capsys):
    event = ClusterResource(
        "ns", "Event", "e", ("Warning", "BackOff", "Pod/web", "boom", "2"), "1m"
    )
    monkeypatch.setattr(cluster, "get_resources", lambda *_: ([], [event]))
    assert cli.run(["events", "--context", "a"]) == 0
    assert "BackOff" in capsys.readouterr().out


def test_get_defaults_to_yaml_and_scopes_cluster_wide(monkeypatch, capsys):
    seen = []
    monkeypatch.setattr(
        cluster,
        "get_resource_details",
        lambda ctx, kind, ns, name: seen.append((kind, ns, name)) or {"kind": kind},
    )
    assert cli.run(["get", "pod", "web", "--context", "a"]) == 0
    assert "kind: Pod" in capsys.readouterr().out
    assert cli.run(["get", "Node", "n1", "--context", "a", "-o", "json"]) == 0
    assert json.loads(capsys.readouterr().out) == {"kind": "Node"}
    assert seen == [("Pod", "default", "web"), ("Node", "", "n1")]


def test_get_unknown_kind(capsys):
    assert cli.run(["get", "banana", "x", "--context", "a"]) == 1
    assert "Unknown kind" in capsys.readouterr().err


def test_logs_first_container_and_given(monkeypatch, capsys):
    monkeypatch.setattr(
        cluster,
        "get_resource_details",
        lambda *_: {"spec": {"containers": [{"name": "app"}]}},
    )
    monkeypatch.setattr(
        cluster, "get_pod_logs", lambda ctx, ns, pod, c, tail: f"{c}:{tail}\n"
    )
    assert cli.run(["logs", "web", "--context", "a"]) == 0
    assert capsys.readouterr().out == "app:100\n"
    assert cli.run(["logs", "web", "--context", "a", "-c", "x", "--tail", "5"]) == 0
    assert capsys.readouterr().out == "x:5\n"


def test_logs_pod_without_container(monkeypatch, capsys):
    monkeypatch.setattr(cluster, "get_resource_details", lambda *_: {})
    assert cli.run(["logs", "web", "--context", "a"]) == 1
    assert "no container" in capsys.readouterr().err


def test_context_asked_by_number_name_and_default(monkeypatch):
    for answer, expected in (("1", "a"), ("b", "b"), ("", "b")):
        _tty(monkeypatch, answer)
        assert cli_cluster._context(None) == expected
    assert cli_cluster._context("given") == "given"


def test_context_asked_invalid(monkeypatch, capsys):
    _tty(monkeypatch, "9")
    monkeypatch.setattr(cluster, "get_pods", lambda *_: ([], []))
    assert cli.run(["pods"]) == 1
    assert "no context '9'" in capsys.readouterr().err


def test_context_not_asked_without_terminal(capsys):
    assert cli.run(["pods"]) == 1
    assert "Pass --context" in capsys.readouterr().err


def test_context_without_any(monkeypatch, capsys):
    monkeypatch.setattr(cluster, "list_contexts", lambda: ([], None))
    assert cli.run(["pods"]) == 1
    assert "no context" in capsys.readouterr().err


def test_context_asked_without_current(monkeypatch):
    monkeypatch.setattr(cluster, "list_contexts", lambda: (["a"], None))
    _tty(monkeypatch, "a")
    assert cli_cluster._context(None) == "a"


def test_cluster_error_hints_the_login(monkeypatch, capsys):
    def fail(*_):
        raise ClusterError("Unauthorized (401)")

    monkeypatch.setattr(cluster, "get_pods", fail)
    assert cli.run(["pods", "--context", "a"]) == 1
    err = capsys.readouterr().err
    assert "kubescope login --context a" in err
    monkeypatch.setattr(cluster, "get_pods", lambda *_: 1 / 0)
    with pytest.raises(ZeroDivisionError):
        cli.run(["pods", "--context", "a"])


def test_interrupt(monkeypatch, capsys):
    def stop(*_):
        raise KeyboardInterrupt

    monkeypatch.setattr(cluster, "get_pods", stop)
    assert cli.run(["pods", "--context", "a"]) == 130


def test_hint_without_context(monkeypatch, capsys):
    namespace = argparse.Namespace(command="contexts", output="table")
    monkeypatch.setattr(
        cli_cluster,
        "_dispatch",
        lambda _n: (_ for _ in ()).throw(ClusterError("token expired")),
    )
    assert cli_cluster.run(namespace) == 1
    assert "<name>" in capsys.readouterr().err


def test_login(monkeypatch, capsys):
    ran = []
    action = LoginAction(["aws", "sso", "login"], "p", False)
    monkeypatch.setattr(cluster, "login_action", lambda ctx: action)
    monkeypatch.setattr(cluster, "run_login_here", ran.append)
    assert cli.run(["login", "--context", "a"]) == 0
    assert cli.run(["auth", "--context", "a"]) == 0
    assert ran == [action, action]
    assert "Signed in to a" in capsys.readouterr().out


def test_login_unknown_program(monkeypatch, capsys):
    monkeypatch.setattr(cluster, "login_action", lambda ctx: None)
    assert cli.run(["login", "--context", "a"]) == 1
    assert "does not know how to sign in" in capsys.readouterr().err


def test_write_needs_write_mode(capsys):
    FakeSettings.write_mode = False
    assert cli.run(["evict", "web", "-n", "ns", "--context", "a", "-y"]) == 1
    assert "write mode is off" in capsys.readouterr().err


def test_write_needs_namespace():
    with pytest.raises(SystemExit):
        cli.run(["evict", "web", "--context", "a"])


def test_writes_with_yes(monkeypatch, capsys):
    calls = []
    for name in ("delete_pod", "delete_resource", "evict_pod", "restart_deployment"):
        monkeypatch.setattr(
            writes, name, lambda *args, name=name: calls.append((name, *args))
        )
    monkeypatch.setattr(
        writes, "scale_deployment", lambda *args: calls.append(("scale", *args))
    )
    base = ["--context", "a", "-n", "ns", "-y"]
    assert cli.run(["delete", "pod", "web", *base]) == 0
    assert cli.run(["delete", "deployment", "api", *base]) == 0
    assert cli.run(["delete", "namespace", "ns", *base]) == 0
    assert cli.run(["evict", "web", *base]) == 0
    assert cli.run(["scale", "api", "--replicas", "3", *base]) == 0
    assert cli.run(["restart", "api", *base]) == 0
    assert calls == [
        ("delete_pod", "a", "ns", "web"),
        ("delete_resource", "a", "Deployment", "ns", "api"),
        ("delete_resource", "a", "Namespace", "", "ns"),
        ("evict_pod", "a", "ns", "web"),
        ("scale", "a", "ns", "api", 3),
        ("restart_deployment", "a", "ns", "api"),
    ]
    assert "scaled to 3" in capsys.readouterr().out


def test_write_confirmation(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(writes, "evict_pod", lambda *args: calls.append(args))
    base = ["evict", "web", "--context", "a", "-n", "ns"]
    assert cli.run(base) == 1  # no terminal, no --yes
    assert "Pass --yes" in capsys.readouterr().err
    _tty(monkeypatch, "n")
    assert cli.run(base) == 1
    assert "Cancelled" in capsys.readouterr().err
    assert calls == []
    _tty(monkeypatch, "y")
    assert cli.run(base) == 0
    assert calls == [("a", "ns", "web")]


def test_delete_cluster_wide_kind_has_no_namespace_in_question(monkeypatch, capsys):
    _tty(monkeypatch, "n")
    assert cli.run(["delete", "node", "n1", "--context", "a", "-n", "ns"]) == 1
    assert "in ns" not in capsys.readouterr().err
