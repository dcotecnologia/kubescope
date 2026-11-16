"""Search the Helm charts of Artifact Hub for the Plugins catalog.

This is the one network call the app makes for a page you open: the
catalog asks the public Artifact Hub API (`artifacthub.io`, over HTTPS)
for charts that match what you type, and sends nothing but a User-Agent
with the app version. It only reads: nothing is installed. The links of
a chart are built here from its repository and name, never taken from
the answer, so they always point at Artifact Hub.
"""

import json
import logging
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote, urlencode

from kubescope import __version__
from kubescope.utils.errors import first_line

logger = logging.getLogger(__name__)

API_URL = "https://artifacthub.io/api/v1/packages/search"
SITE_URL = "https://artifacthub.io/packages/helm"
PACKAGE_URL = "https://artifacthub.io/api/v1/packages/helm"
MAX_VERSIONS = 100  # versions of a chart kept
IMAGE_URL = "https://artifacthub.io/image"
MAX_LOGO = 1_000_000  # bytes of a logo kept
_LOGO_ID = re.compile(r"[0-9a-fA-F-]{8,64}")
TIMEOUT = 15  # seconds
PAGE_SIZE = 60
KIND_HELM = 0  # the `kind` Artifact Hub gives Helm charts
MAX_QUERY = 100  # characters of a search
MAX_DESCRIPTION = 400  # characters of a description kept


class CatalogError(Exception):
    """The catalog could not be read."""


@dataclass(frozen=True, slots=True)
class Chart:
    name: str  # "kube-prometheus-stack"
    repository: str  # "prometheus-community", the name Artifact Hub gives it
    version: str  # the chart version, "93.3.0"
    app_version: str  # the version of what it installs
    description: str
    official: bool  # the publisher is the project the chart installs
    verified: bool  # the publisher proved it owns the repository
    cncf: bool  # the chart belongs to a CNCF project
    repository_url: str  # where the repository is served, for `helm repo add`
    logo_id: str = ""  # the id of its logo at Artifact Hub, when it has one

    @property
    def link(self) -> str:
        repository = quote(self.repository, safe="")
        return f"{SITE_URL}/{repository}/{quote(self.name, safe='')}"

    @property
    def command(self) -> str:
        """The `helm` commands that install it, for the person to run."""
        return (
            f"helm repo add {self.repository} {self.repository_url}\n"
            f"helm repo update\n"
            f"helm install {self.name} {self.repository}/{self.name}"
            f" --version {self.version} --namespace {self.name} --create-namespace"
        )


def _text(value: object, limit: int = 200) -> str:
    return value.strip()[:limit] if isinstance(value, str) else ""


def _chart(item: object) -> Chart | None:
    if not isinstance(item, dict):
        return None
    repository = item.get("repository")
    if not isinstance(repository, dict):
        return None
    name = _text(item.get("name"))
    repo_name = _text(repository.get("name"))
    repo_url = _text(repository.get("url"), 500)
    if not name or not repo_name or not repo_url.startswith("https://"):
        return None
    return Chart(
        name=name,
        repository=repo_name,
        version=_text(item.get("version")),
        app_version=_text(item.get("app_version")),
        description=_text(item.get("description"), MAX_DESCRIPTION),
        official=bool(repository.get("official")),
        verified=bool(repository.get("verified_publisher")),
        cncf=bool(repository.get("cncf")),
        repository_url=repo_url,
        logo_id=logo
        if _LOGO_ID.fullmatch(logo := _text(item.get("logo_image_id"), 64))
        else "",
    )


@dataclass(frozen=True, slots=True)
class Results:
    charts: list[Chart]
    total: int  # how many charts match in all, of which `charts` is a page


def search_charts(query: str = "", offset: int = 0, limit: int = PAGE_SIZE) -> Results:
    """The Helm charts that match a text, the most relevant first (the most
    starred ones when the text is empty).

    Raises CatalogError.
    """
    params: dict[str, Any] = {
        "kind": KIND_HELM,
        "limit": limit,
        "offset": offset,
        "sort": "relevance",
    }
    if query.strip():
        params["ts_query_web"] = query.strip()[:MAX_QUERY]
    request = urllib.request.Request(
        f"{API_URL}?{urlencode(params)}",
        headers={
            "Accept": "application/json",
            "User-Agent": f"KubeScope/{__version__}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = json.load(response)
            total = int(response.headers.get("Pagination-Total-Count") or 0)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
        logger.warning("Artifact Hub search failed: %s", error)
        raise CatalogError(first_line(str(error))) from error
    packages = data.get("packages") if isinstance(data, dict) else None
    if not isinstance(packages, list):
        raise CatalogError("Artifact Hub answered with something unexpected")
    charts = [chart for item in packages if (chart := _chart(item))]
    return Results(charts, max(total, offset + len(packages)))


def fetch_logo(logo_id: str) -> bytes | None:
    """The image of a chart's logo, or None when it has none or cannot be read.

    The address is built here from the id, and an image over MAX_LOGO is
    dropped.
    """
    if not _LOGO_ID.fullmatch(logo_id):
        return None
    request = urllib.request.Request(
        f"{IMAGE_URL}/{logo_id}",
        headers={"User-Agent": f"KubeScope/{__version__}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = response.read(MAX_LOGO + 1)
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        logger.info("Logo %s not read: %s", logo_id, error)
        return None
    return data if 0 < len(data) <= MAX_LOGO else None


def package_versions(repository: str, name: str) -> list[str]:
    """The versions Artifact Hub knows of a chart, the newest first.

    Raises
    CatalogError.
    """
    request = urllib.request.Request(
        f"{PACKAGE_URL}/{quote(repository, safe='')}/{quote(name, safe='')}",
        headers={
            "Accept": "application/json",
            "User-Agent": f"KubeScope/{__version__}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = json.load(response)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as error:
        logger.warning("Artifact Hub versions failed: %s", error)
        raise CatalogError(first_line(str(error))) from error
    found = data.get("available_versions") if isinstance(data, dict) else None
    if not isinstance(found, list):
        return []
    versions = [
        _text(item.get("version"), 100) for item in found if isinstance(item, dict)
    ]
    return [version for version in versions if version][:MAX_VERSIONS]
