import io
import json
import urllib.error

import pytest

from kubescope.utils import artifacthub
from kubescope.utils.artifacthub import CatalogError, Chart, search_charts

PACKAGE = {
    "name": "cert-manager",
    "version": "v1.21.3",
    "app_version": "v1.21.3",
    "description": "A Helm chart for cert-manager",
    "repository": {
        "name": "cert-manager",
        "url": "https://charts.jetstack.io",
        "official": True,
        "verified_publisher": True,
        "cncf": False,
    },
}


def _answer(monkeypatch, body, seen=None):
    def urlopen(request, timeout):
        if seen is not None:
            seen.update(url=request.full_url, headers=dict(request.header_items()))
        response = io.BytesIO(json.dumps(body).encode())
        response.headers = {"Pagination-Total-Count": "7"}  # type: ignore[attr-defined]
        return response

    monkeypatch.undo()  # the tests' offline guard
    monkeypatch.setattr(artifacthub.urllib.request, "urlopen", urlopen)


def test_a_search_asks_for_helm_charts_and_reads_them(monkeypatch) -> None:
    seen: dict = {}
    _answer(monkeypatch, {"packages": [PACKAGE]}, seen)
    monkeypatch.setattr(artifacthub, "__version__", "1.0.0")

    results = search_charts("cert manager")
    charts = results.charts

    assert "kind=0" in seen["url"] and "ts_query_web=cert+manager" in seen["url"]
    assert seen["headers"]["User-agent"] == "KubeScope/1.0.0"
    assert results.total == 7
    assert charts[0].name == "cert-manager" and charts[0].verified
    assert (
        charts[0].link
        == "https://artifacthub.io/packages/helm/cert-manager/cert-manager"
    )
    assert "helm install cert-manager cert-manager/cert-manager" in charts[0].command


def test_an_empty_search_sends_no_text(monkeypatch) -> None:
    seen: dict = {}
    _answer(monkeypatch, {"packages": []}, seen)
    assert search_charts("  ").charts == []
    assert "ts_query_web" not in seen["url"]


def test_a_chart_without_a_name_or_an_https_repository_is_dropped(monkeypatch) -> None:
    http = {**PACKAGE, "repository": {**PACKAGE["repository"], "url": "http://x"}}
    nameless = {**PACKAGE, "name": ""}
    _answer(monkeypatch, {"packages": [http, nameless, "nope", {"name": "a"}, PACKAGE]})
    assert [chart.name for chart in search_charts().charts] == ["cert-manager"]


def test_a_failed_or_odd_answer_is_a_catalog_error(monkeypatch) -> None:
    _answer(monkeypatch, {"packages": "no"})
    with pytest.raises(CatalogError):
        search_charts()

    def offline(request, timeout):
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(artifacthub.urllib.request, "urlopen", offline)
    with pytest.raises(CatalogError, match="no route"):
        search_charts()


def test_the_link_is_built_from_the_names_not_taken_from_the_answer() -> None:
    chart = Chart("a/b", "r s", "1", "1", "", False, False, False, "https://x")
    assert chart.link == "https://artifacthub.io/packages/helm/r%20s/a%2Fb"


def test_a_logo_is_read_from_an_address_built_from_its_id(monkeypatch) -> None:
    seen: dict = {}
    _answer(monkeypatch, {}, seen)
    assert artifacthub.fetch_logo("abc-123-def-456") is not None
    assert seen["url"] == "https://artifacthub.io/image/abc-123-def-456"
    assert artifacthub.fetch_logo("../evil") is None  # never a path of the answer


def test_a_logo_that_is_too_big_or_fails_is_dropped(monkeypatch) -> None:
    monkeypatch.undo()
    monkeypatch.setattr(artifacthub, "MAX_LOGO", 2)
    monkeypatch.setattr(
        artifacthub.urllib.request, "urlopen", lambda *_a, **_k: io.BytesIO(b"abcd")
    )
    assert artifacthub.fetch_logo("abcdef1234") is None

    def offline(*_args, **_kwargs):
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(artifacthub.urllib.request, "urlopen", offline)
    assert artifacthub.fetch_logo("abcdef1234") is None


def test_a_chart_keeps_only_a_well_formed_logo_id(monkeypatch) -> None:
    good = {**PACKAGE, "logo_image_id": "0a1b2c3d-4e5f"}
    bad = {**PACKAGE, "logo_image_id": "../x"}
    _answer(monkeypatch, {"packages": [good, bad]})
    assert [chart.logo_id for chart in search_charts().charts] == ["0a1b2c3d-4e5f", ""]


def test_the_versions_of_a_chart_are_those_artifact_hub_lists(monkeypatch) -> None:
    seen: dict = {}
    body = {
        "available_versions": [
            {"version": "3.6.3"},
            {"version": ""},
            {"x": 1},
            {"version": "3.6.2"},
        ]
    }
    _answer(monkeypatch, body, seen)
    assert artifacthub.package_versions("aws", "aws-lb/x") == ["3.6.3", "3.6.2"]
    assert seen["url"] == "https://artifacthub.io/api/v1/packages/helm/aws/aws-lb%2Fx"
    _answer(monkeypatch, {"nope": 1})
    assert artifacthub.package_versions("a", "b") == []

    def offline(request, timeout):
        raise urllib.error.URLError("no route")

    monkeypatch.setattr(artifacthub.urllib.request, "urlopen", offline)
    with pytest.raises(CatalogError):
        artifacthub.package_versions("a", "b")
