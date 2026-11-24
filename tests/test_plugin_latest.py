from dataclasses import replace

import pytest
from kubescope.sdk.models import ClusterResource

from kubescope import cluster, plugin_latest
from kubescope.cluster import ClusterError
from kubescope.utils import artifacthub
from kubescope.utils.artifacthub import Chart, Results

DOCUMENT = {
    "addons": [
        {
            "addonVersions": [
                {"addonVersion": "v3", "compatibilities": [{"clusterVersion": "1.35"}]},
                {"addonVersion": "v2", "compatibilities": [{"clusterVersion": "1.34"}]},
            ]
        }
    ]
}


def _eks(monkeypatch, document=None, error=None):
    monkeypatch.setattr(cluster, "_eks_target", lambda _c: ["--cluster-name", "p"])
    monkeypatch.setattr(cluster, "_context_env", lambda _c: None)

    def eks_json(*_a, **_k):
        if error:
            raise error
        return document

    monkeypatch.setattr(cluster, "_eks_json", eks_json)


def test_the_latest_eks_version_is_the_newest_the_cluster_can_run(monkeypatch) -> None:
    _eks(monkeypatch, DOCUMENT)
    assert plugin_latest.eks_latest("ctx", "vpc-cni", "1.34") == "v2"
    assert plugin_latest.eks_latest("ctx", "vpc-cni", "1.35") == "v3"
    assert plugin_latest.eks_latest("ctx", "vpc-cni", "1.20") == "—"
    assert plugin_latest.eks_latest("ctx", "vpc-cni", "") == "v3"  # version unknown


def test_a_failed_read_is_a_dash(monkeypatch) -> None:
    _eks(monkeypatch, error=ClusterError("denied"))
    assert plugin_latest.eks_latest("ctx", "vpc-cni", "1.34") == "—"


def _chart(name, version, **seals):
    seals = {"official": False, "verified": False, "cncf": False, **seals}
    return Chart(name, "r", version, "", "", repository_url="https://x", **seals)


def _hub(monkeypatch, found, versions):
    monkeypatch.setattr(
        artifacthub, "search_charts", lambda *_a: Results(found, len(found))
    )
    monkeypatch.setattr(
        artifacthub, "package_versions", lambda repo, name: versions[(repo, name)]
    )


def test_the_chart_taken_is_the_one_that_has_the_installed_version(monkeypatch) -> None:
    plugin_latest._helm_cache.clear()
    other = _chart("grafana", "1.4.8", official=True)  # another chart of the name
    mine = _chart("grafana", "3.6.3")
    mine = replace(mine, repository="mine", repository_url="https://mine")
    _hub(
        monkeypatch,
        [_chart("x", "9"), other, mine],
        {("r", "grafana"): ["1.4.8", "1.4.7"], ("mine", "grafana"): ["3.6.3", "3.6.2"]},
    )
    assert plugin_latest.helm_match("grafana", "3.6.2") == (
        "https://mine",
        ["3.6.3", "3.6.2"],
    )
    assert plugin_latest.helm_latest("grafana", "v3.6.2") == "3.6.3"
    # without a match, the best publisher's
    assert plugin_latest.helm_match("grafana", "0.0.1")[1] == ["1.4.8", "1.4.7"]
    assert plugin_latest.helm_match("grafana")[1] == ["1.4.8", "1.4.7"]


def test_a_chart_without_versions_falls_back_to_its_own_and_none_is_a_dash(
    monkeypatch,
) -> None:
    plugin_latest._helm_cache.clear()
    _hub(monkeypatch, [_chart("g", "5")], {("r", "g"): []})
    assert plugin_latest.helm_match("g") == ("https://x", ["5"])
    _hub(monkeypatch, [], {})
    assert plugin_latest.helm_match("g") == ("", [])
    assert plugin_latest.helm_latest("g") == "—"


def test_artifact_hub_down_is_a_dash(monkeypatch) -> None:
    plugin_latest._helm_cache.clear()

    def down(*_a):
        raise artifacthub.CatalogError("no route")

    monkeypatch.setattr(artifacthub, "search_charts", down)
    assert plugin_latest.helm_latest("x") == "—"


@pytest.mark.parametrize(
    ("installed", "latest", "expected"),
    [
        ("v1", "v2", True),
        ("v2", "v2", False),
        ("v2", "—", False),
        ("—", "v2", False),
        ("v1.3.0", "1.3.0", False),
        ("1.2.0", "v1.3.0", True),
    ],
)
def test_an_update_is_available_when_the_latest_differs(
    installed, latest, expected
) -> None:
    assert plugin_latest.update_available(installed, latest) is expected


def test_latest_versions_asks_each_row_by_its_kind(monkeypatch) -> None:
    monkeypatch.setattr(
        cluster, "get_cluster_info", lambda _c: type("I", (), {"version": "1.34"})()
    )
    monkeypatch.setattr(
        plugin_latest, "eks_latest", lambda _c, name, v: f"eks-{name}-{v}"
    )
    monkeypatch.setattr(
        plugin_latest, "helm_latest", lambda name, installed: f"helm-{name}-{installed}"
    )
    monkeypatch.setitem(cluster._helm_chart_names, ("ctx", "ops", "web"), "site")
    rows = [
        ClusterResource("", "Addon", "vpc-cni", ("A", "v1", "EKS"), "1d"),
        ClusterResource("ops", "HelmRelease", "web", ("d", "1", "v9", "Helm"), "1d"),
    ]
    assert plugin_latest.latest_versions("ctx", rows) == {
        ("Addon", "vpc-cni"): "eks-vpc-cni-1.34",
        ("HelmRelease", "web"): "helm-site-1",  # the chart, not the release,
    }
    assert plugin_latest.latest_versions("ctx", []) == {}


def test_a_chart_read_before_is_not_asked_again(monkeypatch) -> None:
    plugin_latest._helm_cache.clear()
    asked = []

    def match(name, installed=""):
        asked.append(name)
        return "https://x", ["2", "1"]

    monkeypatch.setattr(plugin_latest, "helm_match", match)
    assert plugin_latest.helm_latest("web", "1") == "2"
    assert plugin_latest.helm_latest("web", "1") == "2"
    assert asked == ["web"]


def test_a_cluster_whose_version_cannot_be_read_still_gets_its_latest(
    monkeypatch,
) -> None:
    def refuse(_context):
        raise ClusterError("denied")

    monkeypatch.setattr(cluster, "get_cluster_info", refuse)
    seen = []
    monkeypatch.setattr(
        plugin_latest, "eks_latest", lambda _c, name, v: seen.append(v) or "v9"
    )
    row = ClusterResource("", "Addon", "vpc-cni", ("A", "v1", "EKS"), "1d")
    assert plugin_latest.latest_versions("ctx", [row]) == {("Addon", "vpc-cni"): "v9"}
    assert seen == [""]
