"""About KubeScope: its version and its addresses.

There is no `__init__.py` in `kubescope`: it is a namespace that the app
shares with the SDK (`kubescope.sdk`), which is a project of its own.
"""

from importlib import metadata

PROJECT_URL = "https://github.com/dcotecnologia/kubescope"
COMPANY_URL = "https://dcotecnologia.com"
SPONSOR_URL = "https://github.com/sponsors/danilogco"
LICENSE_URL = f"{PROJECT_URL}/blob/main/LICENSE"
# the social profiles of the company: the name, the address and the icon
# (`assets/social/<icon>.png`, a mask the theme colors)
SOCIAL = (
    ("X", "https://x.com/dcotecnologia", "x"),
    ("Instagram", "https://www.instagram.com/dcotecnologia/", "instagram"),
    ("Facebook", "https://www.facebook.com/dcotecnologia/", "facebook"),
    ("LinkedIn", "https://www.linkedin.com/company/86377820/", "linkedin"),
)

try:
    __version__ = metadata.version("kubescope")
except metadata.PackageNotFoundError:  # a source tree that was never installed
    __version__ = "unknown"
