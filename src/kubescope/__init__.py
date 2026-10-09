"""Desktop Kubernetes workload viewer."""

from importlib import metadata

PROJECT_URL = "https://github.com/dcotecnologia/kubescope"

try:
    __version__ = metadata.version("kubescope")
except metadata.PackageNotFoundError:  # a source tree that was never installed
    __version__ = "unknown"
