"""Programs of the host, for the app running in a Flatpak.

The sandbox cannot see the `gcloud`, `az`, `kubelogin` or `oci` of the
system, which the sign-in of a GKE, AKS or OCI context needs, so the
Flatpak asks the host to run them (`flatpak-spawn --host`, through the
permission the manifest gives). The AWS CLI is the exception: the
Flatpak carries its own. No Qt.
"""

import os
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

APP_ID = "com.dcotecnologia.KubeScope"
HOST = ("flatpak-spawn", "--host")
BUNDLED = frozenset({"aws"})  # the programs the Flatpak carries itself
PROBE_TIMEOUT = 10  # seconds the host may take to say whether it has a program


def in_flatpak() -> bool:
    """Whether this app runs inside a Flatpak sandbox."""
    return Path("/.flatpak-info").is_file()


def _bundled(command: Sequence[str]) -> bool:
    return Path(command[0]).name in BUNDLED


def on_host(command: Sequence[str], env: Mapping[str, str] | None = None) -> list[str]:
    """The command to run: as it is, or asked of the host when this is a
    Flatpak.

    `env` is the environment the program is meant to get; what differs
    from the one of the sandbox is handed over, since the host starts it
    with its own.
    """
    if not in_flatpak() or _bundled(command):
        return list(command)
    changed = [
        f"--env={name}={value}"
        for name, value in (env or {}).items()
        if os.environ.get(name) != value
    ]
    return [*HOST, *changed, *command]


def in_terminal(command: Sequence[str]) -> list[str]:
    """The command for a terminal of the host: the AWS CLI of the Flatpak is
    not there, so it is started from the Flatpak itself."""
    if not _bundled(command):
        return list(command)
    app = os.environ.get("FLATPAK_ID", APP_ID)
    return ["flatpak", "run", f"--command={command[0]}", app, *command[1:]]


def host_has(program: str) -> bool:
    """Whether the host has this program on its path."""
    try:
        result = subprocess.run(
            [*HOST, "sh", "-c", 'command -v "$1"', "sh", program],
            capture_output=True,
            timeout=PROBE_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0
