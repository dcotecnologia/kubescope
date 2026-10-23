import subprocess
from pathlib import Path

import pytest

from kubescope.utils import flatpak


@pytest.fixture
def sandbox(monkeypatch):
    """The app runs inside a Flatpak."""
    monkeypatch.setattr(flatpak, "in_flatpak", lambda: True)


def test_a_flatpak_is_told_by_the_file_the_sandbox_leaves(monkeypatch) -> None:
    assert not flatpak.in_flatpak()  # the tests do not run in one

    monkeypatch.setattr(Path, "is_file", lambda self: str(self) == "/.flatpak-info")
    assert flatpak.in_flatpak()


def test_outside_a_flatpak_a_command_runs_as_it_is() -> None:
    assert flatpak.on_host(["gcloud", "auth", "login"]) == ["gcloud", "auth", "login"]


def test_in_a_flatpak_a_command_is_asked_of_the_host(sandbox) -> None:
    assert flatpak.on_host(["gcloud", "auth", "login"]) == [
        "flatpak-spawn",
        "--host",
        "gcloud",
        "auth",
        "login",
    ]


def test_the_aws_cli_is_the_one_of_the_host_too(sandbox) -> None:
    assert flatpak.on_host(["aws", "eks", "get-token"]) == [
        "flatpak-spawn",
        "--host",
        "aws",
        "eks",
        "get-token",
    ]


def test_only_the_environment_that_differs_is_handed_to_the_host(
    sandbox, monkeypatch
) -> None:
    monkeypatch.setenv("SAME", "kept")
    monkeypatch.setenv("CHANGED", "old")

    command = flatpak.on_host(
        ["kubelogin", "get-token"],
        {"SAME": "kept", "CHANGED": "new", "KUBERNETES_EXEC_INFO": "{}"},
    )

    assert command == [
        "flatpak-spawn",
        "--host",
        "--env=CHANGED=new",
        "--env=KUBERNETES_EXEC_INFO={}",
        "kubelogin",
        "get-token",
    ]


def test_the_host_is_asked_whether_it_has_a_program(monkeypatch) -> None:
    asked = []

    def run(command, **options):
        asked.append(command)
        return subprocess.CompletedProcess(
            command, 0 if command[-1] == "konsole" else 1
        )

    monkeypatch.setattr(flatpak.subprocess, "run", run)

    assert flatpak.host_has("konsole")
    assert not flatpak.host_has("xterm")
    assert asked[0] == [
        "flatpak-spawn",
        "--host",
        "sh",
        "-c",
        'command -v "$1"',
        "sh",
        "konsole",
    ]


@pytest.mark.parametrize(
    "error", [OSError("no flatpak-spawn"), subprocess.TimeoutExpired("x", 1)]
)
def test_a_host_that_does_not_answer_has_nothing(monkeypatch, error) -> None:
    def run(*_args, **_options):
        raise error

    monkeypatch.setattr(flatpak.subprocess, "run", run)

    assert not flatpak.host_has("konsole")
