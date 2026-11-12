"""The port forwards the app runs for the person: what a forward is and what
the output of its program says about it. No Qt.

A forward is a `kubectl port-forward` or an `aws ssm start-session` that
the app started when the person pressed Run, and that stays listed until
it is stopped.
"""

import contextlib
import json
import logging
import os
import signal
import socket
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path, PureWindowsPath
from typing import Any

from kubescope.settings import config_directory

logger = logging.getLogger(__name__)

STARTING = "starting"
RUNNING = "running"
FAILED = "failed"
STOPPED = "stopped"


@dataclass
class Forward:
    number: int
    title: str  # what is forwarded, such as "Service api" or "RDS orders"
    kind: str  # "kubectl" or "ssm"
    command: list[str]
    env: dict[str, str] = field(default_factory=dict)
    local: int = 0  # the local port
    target: str = ""  # where it goes, such as "api:80"
    status: str = STARTING
    detail: str = ""  # the last thing its program said
    pid: int = 0  # the process of its program, once it started
    adopted: bool = False  # found running after the app restarted

    @property
    def active(self) -> bool:
        return self.status in (STARTING, RUNNING)


def port_in_use(port: int) -> bool:
    """Whether something already listens on a local port."""
    with socket.socket() as probe:
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return True
    return False


def status_of(kind: str, line: str) -> str | None:
    """The status a line of output tells, None when it tells none: the line
    that says the port is open, for each program."""
    if kind == "kubectl" and line.startswith("Forwarding from"):
        return RUNNING
    if kind == "ssm" and ("Waiting for connections" in line or "opened for" in line):
        return RUNNING
    return None


def state_path() -> Path:
    return config_directory() / "forwards.json"


def save(items: list[Forward]) -> None:
    """Keep the forwards that are running, with their process, so that an app
    that is restarted or dies can find them again.

    The environment, which can hold keys, is never kept.
    """
    saved = [
        {
            "title": item.title,
            "kind": item.kind,
            "command": item.command,
            "local": item.local,
            "target": item.target,
            "pid": item.pid,
        }
        for item in items
        if item.active and item.pid
    ]
    try:
        state_path().parent.mkdir(parents=True, exist_ok=True)
        state_path().write_text(json.dumps(saved, indent=2), encoding="utf-8")
    except OSError as error:
        logger.warning("Could not keep the forwards: %s", error)


def load() -> list[Forward]:
    """The forwards of an earlier run whose program is still running."""
    try:
        document: Any = json.loads(state_path().read_text(encoding="utf-8"))
    except OSError, ValueError:
        return []
    found = []
    for item in document if isinstance(document, list) else []:
        try:
            forward = Forward(
                0,
                str(item["title"]),
                str(item["kind"]),
                [str(argument) for argument in item["command"]],
                {},
                int(item["local"]),
                str(item["target"]),
                RUNNING,
                "",
                int(item["pid"]),
                True,
            )
        except KeyError, TypeError, ValueError:
            continue
        if process_alive(forward.pid) and process_matches(forward):
            found.append(forward)
    return found


def _tasklist(pid: int) -> str:
    result = subprocess.run(
        ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def process_alive(pid: int) -> bool:
    if sys.platform == "win32":
        return f'"{pid}"' in _tasklist(pid)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # it exists, and is not ours to signal
    return True


def process_matches(forward: Forward) -> bool:
    """Whether a process is still the program of this forward and not another
    one that got the number later."""
    if sys.platform == "win32":
        name = PureWindowsPath(forward.command[0]).stem if forward.command else ""
        return bool(name) and name.lower() in _tasklist(forward.pid).lower()
    program = Path(forward.command[0]).stem if forward.command else ""
    result = subprocess.run(
        ["ps", "-p", str(forward.pid), "-o", "args="],
        capture_output=True,
        text=True,
        check=False,
    )
    line = result.stdout
    return bool(program) and program in line and str(forward.local) in line


def terminate(pid: int) -> None:
    """Ask a process to end."""
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, check=False
        )
        return
    with contextlib.suppress(OSError):  # it may be gone already
        os.kill(pid, signal.SIGTERM)
