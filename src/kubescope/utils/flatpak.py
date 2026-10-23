"""Programs of the host, for the app running in a Flatpak.

The sandbox cannot see the `aws`, `gcloud`, `az`, `kubelogin` or `oci`
of the system, which the sign-in of an EKS, GKE, AKS or OCI context
needs, so the Flatpak asks the host to run them (`flatpak-spawn --host`,
through the permission the manifest gives). It carries none of them: the
tools, their versions and their profiles are the ones of the person's
own system. No Qt.
"""

import os
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

HOST = ("flatpak-spawn", "--host")
PROBE_TIMEOUT = 10  # seconds the host may take to say whether it has a program


def in_flatpak() -> bool:
    """Whether this app runs inside a Flatpak sandbox."""
    return Path("/.flatpak-info").is_file()


def on_host(command: Sequence[str], env: Mapping[str, str] | None = None) -> list[str]:
    """The command to run: as it is, or asked of the host when this is a
    Flatpak.

    `env` is the environment the program is meant to get; what differs
    from the one of the sandbox is handed over, since the host starts it
    with its own.
    """
    if not in_flatpak():
        return list(command)
    changed = [
        f"--env={name}={value}"
        for name, value in (env or {}).items()
        if os.environ.get(name) != value
    ]
    return [*HOST, *changed, *command]


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
