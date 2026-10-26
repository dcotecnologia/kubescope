"""Desktop IDE for Kubernetes."""

from importlib import metadata

PROJECT_URL = "https://github.com/dcotecnologia/kubescope"
COMPANY_URL = "https://dcotecnologia.com"
SPONSOR_URL = "https://github.com/sponsors/danilogco"
LICENSE_URL = f"{PROJECT_URL}/blob/main/LICENSE"

try:
    __version__ = metadata.version("kubescope")
except metadata.PackageNotFoundError:  # a source tree that was never installed
    __version__ = "unknown"
