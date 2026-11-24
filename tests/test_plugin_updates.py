import subprocess

import pytest

from kubescope import cluster, plugin_updates
from kubescope.cluster import ClusterError


def test_run_update_gives_the_keys_and_reports_failures(
    monkeypatch,
) -> None:
    seen = {}

    def run(program, environment):
        seen.update(program=program, environment=environment)
        return subprocess.CompletedProcess(program, 0, " done \n", "")

    monkeypatch.setattr(plugin_updates, "_run", run)
    monkeypatch.setattr(cluster, "context_environment", lambda _c: {"K": "v"})
    monkeypatch.setattr(cluster, "_kubeconfig_files", ["/a", "/b"])
    assert plugin_updates.run_update("ctx", ["helm", "upgrade"]) == "done"
    assert seen["environment"]["K"] == "v" and "KUBECONFIG" in seen["environment"]
    plugin_updates.run_update("ctx", ["aws", "eks"])
    assert "KUBECONFIG" not in seen["environment"]

    monkeypatch.setattr(
        plugin_updates,
        "_run",
        lambda *_a: subprocess.CompletedProcess([], 1, "", "denied"),
    )
    with pytest.raises(ClusterError, match="denied"):
        plugin_updates.run_update("ctx", ["helm", "upgrade"])

    def missing(*_a):
        raise OSError("no helm")

    monkeypatch.setattr(plugin_updates, "_run", missing)
    with pytest.raises(ClusterError, match="no helm"):
        plugin_updates.run_update("ctx", ["helm", "upgrade"])

    def slow(*_a):
        raise subprocess.TimeoutExpired("helm", 1)

    monkeypatch.setattr(plugin_updates, "_run", slow)
    with pytest.raises(ClusterError, match="timed out"):
        plugin_updates.run_update("ctx", ["helm", "upgrade"])
