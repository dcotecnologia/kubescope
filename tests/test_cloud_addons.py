import json
from datetime import UTC, datetime

import pytest

from kubescope import cloud_addons, cluster, plugin_latest
from kubescope.cluster import ClusterError
from kubescope.models import ClusterResource

NOW = datetime(2026, 1, 11, tzinfo=UTC)
AKS_LIST = [
    {"name": "other", "resourceGroup": "rg0", "fqdn": "other.hcp.azmk8s.io"},
    {
        "name": "prod",
        "resourceGroup": "rg1",
        "fqdn": "PROD-dns.hcp.eastus.azmk8s.io",
        "privateFqdn": None,
    },
]
EXTENSIONS = [
    {
        "name": "flux",
        "version": "1.2.3",
        "provisioningState": "Succeeded",
        "systemData": {"createdAt": "2026-01-01T00:00:00Z"},
    },
    {"name": "bare"},
    {"nope": 1},
    "odd",
]


def _azure(monkeypatch, answers):
    """An AKS context: kubelogin signs in; `az` answers by its sub-command."""
    seen = []
    monkeypatch.setattr(
        cluster, "_sign_in_program", lambda _c: {"command": "/usr/bin/kubelogin"}
    )
    monkeypatch.setattr(cluster, "_context_env", lambda _c: None)
    monkeypatch.setattr(
        cluster,
        "_kubeconfig",
        lambda: {
            "contexts": [{"name": "prod", "context": {"cluster": "c"}}],
            "clusters": [
                {
                    "name": "c",
                    "cluster": {"server": "https://prod-dns.hcp.eastus.azmk8s.io:443"},
                }
            ],
        },
    )

    def run(command, timeout, env=None):
        seen.append(command)
        key = command[2] if command[1] == "k8s-extension" else command[1]
        answer = answers[key]
        if isinstance(answer, Exception):
            raise answer
        return answer if isinstance(answer, str) else json.dumps(answer)

    monkeypatch.setattr(cluster, "_run_command", run)
    return seen


def test_an_aks_cluster_is_found_by_the_address_of_its_server(monkeypatch) -> None:
    _azure(monkeypatch, {"aks": AKS_LIST})
    assert cloud_addons.is_aks_context("prod")
    assert cloud_addons.aks_cluster("prod") == ("prod", "rg1")


def test_an_aks_cluster_that_is_not_listed_or_has_no_server_is_an_error(
    monkeypatch,
) -> None:
    _azure(monkeypatch, {"aks": [{"name": "x", "fqdn": "x"}]})
    with pytest.raises(ClusterError, match="not among"):
        cloud_addons.aks_cluster("prod")
    _azure(monkeypatch, {"aks": "not json"})
    with pytest.raises(ClusterError, match="unexpected"):
        cloud_addons.aks_cluster("prod")
    _azure(monkeypatch, {"aks": {"not": "a list"}})
    with pytest.raises(ClusterError, match="not among"):
        cloud_addons.aks_cluster("prod")
    monkeypatch.setattr(cluster, "_kubeconfig", lambda: {})
    with pytest.raises(ClusterError, match="does not say"):
        cloud_addons.aks_cluster("prod")


def test_a_context_that_signs_in_otherwise_is_not_aks(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {"command": "aws"})
    assert not cloud_addons.is_aks_context("x")
    monkeypatch.setattr(cluster, "_sign_in_program", lambda _c: {})
    assert not cloud_addons.is_aks_context("x")


def test_the_extensions_of_an_aks_cluster_are_rows_with_their_version(
    monkeypatch,
) -> None:
    seen = _azure(monkeypatch, {"aks": AKS_LIST, "list": EXTENSIONS})
    rows = cloud_addons.aks_extensions("prod", NOW)
    assert [(r.kind, r.name, r.values) for r in rows] == [
        ("AksExtension", "flux", ("Succeeded", "1.2.3", "AKS")),
        ("AksExtension", "bare", ("—", "—", "AKS")),
    ]
    assert rows[0].age == "10d" and rows[1].age == "—"
    assert seen[-1][:3] == ["az", "k8s-extension", "list"]
    assert seen[-1][5:7] == ["--resource-group", "rg1"]
    _azure(monkeypatch, {"aks": AKS_LIST, "list": {"x": 1}})
    assert cloud_addons.aks_extensions("prod", NOW) == []


def test_an_extension_is_shown_and_updated_with_the_cluster_and_group(
    monkeypatch,
) -> None:
    seen = _azure(monkeypatch, {"aks": AKS_LIST, "show": {"name": "flux"}})
    assert cloud_addons.aks_extension_details("prod", "flux") == {"name": "flux"}
    assert "show" in seen[-1] and "flux" in seen[-1]
    with pytest.raises(ClusterError):
        cloud_addons.aks_extension_details("prod", "a b")
    _azure(monkeypatch, {"aks": AKS_LIST, "show": ["odd"]})
    assert cloud_addons.aks_extension_details("prod", "flux") == {}

    arguments = cloud_addons.aks_update_arguments("prod", "rg1", "flux", "1.3.0")
    assert arguments[:3] == ["az", "k8s-extension", "update"]
    assert "--auto-upgrade-minor-version" in arguments and "--yes" in arguments
    for bad in (
        ("prod", "rg 1", "flux", "1"),
        ("prod", "rg1", "a b", "1"),
        ("prod", "rg1", "flux", ""),
        ("", "rg1", "flux", "1"),
    ):
        with pytest.raises(ClusterError):
            cloud_addons.aks_update_arguments(*bad)


GKE = {
    "addonsConfig": {
        "httpLoadBalancing": {},
        "horizontalPodAutoscaling": {"disabled": True},
        "odd": "x",
    }
}


def _gke(monkeypatch, answer):
    seen = []
    monkeypatch.setattr(cluster, "_context_env", lambda _c: None)

    def run(command, timeout, env=None):
        seen.append(command)
        return json.dumps(answer)

    monkeypatch.setattr(cluster, "_run_command", run)
    return seen


def test_a_gke_context_names_its_project_location_and_cluster() -> None:
    assert cloud_addons.gke_target("gke_proj_us-east1_prod") == (
        "proj",
        "us-east1",
        "prod",
    )
    with pytest.raises(ClusterError):
        cloud_addons.gke_target("arn:aws:eks:x")


def test_the_gke_addons_are_on_or_off_and_have_no_version(monkeypatch) -> None:
    seen = _gke(monkeypatch, GKE)
    rows = cloud_addons.gke_addons("gke_proj_us-east1_prod")
    assert [(r.kind, r.name, r.values) for r in rows] == [
        ("GkeAddon", "horizontalPodAutoscaling", ("Disabled", "—", "GKE")),
        ("GkeAddon", "httpLoadBalancing", ("Enabled", "—", "GKE")),
    ]
    assert seen[-1][:4] == ["gcloud", "container", "clusters", "describe"]
    assert "--project" in seen[-1]
    assert cloud_addons.gke_addon_details(
        "gke_proj_us-east1_prod", "httpLoadBalancing"
    ) == {"httpLoadBalancing": {}}
    with pytest.raises(ClusterError, match="not found"):
        cloud_addons.gke_addon_details("gke_proj_us-east1_prod", "nope")
    _gke(monkeypatch, ["not an object"])
    assert cloud_addons.gke_addons("gke_proj_us-east1_prod") == []


def test_the_installed_list_joins_every_source_by_the_kind_of_cluster(
    monkeypatch,
) -> None:
    monkeypatch.setattr(plugin_latest, "latest_versions", lambda *_a: {})
    monkeypatch.setattr(cluster, "_get_namespaces", lambda _c: ["ops"])
    monkeypatch.setattr(cluster, "_eks_addons", lambda *_a: [])
    monkeypatch.setattr(cluster, "_helm_releases", lambda *_a: [])
    extension = ClusterResource("", "AksExtension", "flux", ("ok", "1", "AKS"), "1d")
    monkeypatch.setattr(cloud_addons, "is_aks_context", lambda c: c == "aks")
    monkeypatch.setattr(cloud_addons, "aks_extensions", lambda *_a: [extension])
    gke = ClusterResource("", "GkeAddon", "lb", ("Enabled", "—", "GKE"), "—")
    monkeypatch.setattr(cloud_addons, "gke_addons", lambda *_a: [gke])

    _, aks_rows = cluster._get_addons("aks", None)
    _, gke_rows = cluster._get_addons("gke_p_l_c", None)
    _, other_rows = cluster._get_addons("other", None)

    assert [r.name for r in aks_rows] == ["flux"]
    assert aks_rows[0].values == ("ok", "1", "—", "AKS")  # no latest to find
    assert [r.name for r in gke_rows] == ["lb"]
    assert other_rows == []


def test_the_details_of_an_extension_and_a_gke_addon_come_from_their_cloud(
    monkeypatch,
) -> None:
    monkeypatch.setattr(cloud_addons, "aks_extension_details", lambda c, n: {"a": n})
    monkeypatch.setattr(cloud_addons, "gke_addon_details", lambda c, n: {"g": n})
    assert cluster.get_resource_details("ctx", "AksExtension", "", "flux") == {
        "a": "flux"
    }
    assert cluster.get_resource_details("ctx", "GkeAddon", "", "lb") == {"g": "lb"}


def test_only_eks_and_helm_have_a_latest_version_to_find() -> None:
    row = ClusterResource("", "AksExtension", "flux", ("ok", "1", "AKS"), "1d")
    assert plugin_latest._latest_call("ctx", row, "")() == "—"


def test_an_age_without_a_time_zone_is_read_as_utc_and_a_bad_one_is_a_dash() -> None:
    assert cloud_addons._age("2026-01-01T00:00:00", NOW) == "10d"
    assert cloud_addons._age("yesterday", NOW) == "—"
