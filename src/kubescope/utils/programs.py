"""Find a program of the person's computer, even where the app's own path does
not reach it.

An app started from the Start menu, or before an installation, has a
shorter path than a terminal, and the installers of these programs often
put them in a folder of the person that is on no path at all.
"""

import ntpath
import os
import shutil
import sys
from pathlib import Path

# where Rancher Desktop keeps kubectl and helm, inside its folder
_RANCHER_BIN = ("resources", "resources", "win32", "bin")


def _registry_path() -> list[str]:
    """The path of the person and of the system as Windows keeps it, which is
    newer than the one an app started before an installation has."""
    if sys.platform != "win32":  # only Windows has the registry
        return []
    import winreg  # noqa: PLC0415

    keys = (
        (winreg.HKEY_CURRENT_USER, "Environment"),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        ),
    )
    folders: list[str] = []
    for root, name in keys:
        try:
            with winreg.OpenKey(root, name) as key:
                value, _kind = winreg.QueryValueEx(key, "Path")
        except OSError:
            continue
        if isinstance(value, str):
            folders += [ntpath.expandvars(part) for part in value.split(";") if part]
    return folders


def _windows_folders() -> list[Path]:
    """Where these programs may be on Windows: the path Windows keeps now and
    the folders their installers use."""
    home = Path.home()
    folders = [Path(part) for part in _registry_path()]
    folders += [
        home / ".local" / "bin",  # the installer of Claude Code
        home / ".claude" / "local",  # its older, local installation
        home / ".codex" / "packages" / "standalone" / "current" / "bin",
        home / ".npm-global",
        home / ".bun" / "bin",
        home / ".cargo" / "bin",
        home / "scoop" / "shims",
        home / "bin",
        home / "go" / "bin",
        home / ".krew" / "bin",  # kubectl plugins
        home / ".azure-kubelogin",
        home / ".rd" / "bin",  # Rancher Desktop: kubectl, helm
        home / ".docker" / "bin",
    ]
    for variable, *parts in (
        ("APPDATA", "npm"),  # npm install -g
        ("APPDATA", "pnpm"),
        ("LOCALAPPDATA", "pnpm"),
        ("LOCALAPPDATA", "Yarn", "bin"),
        ("LOCALAPPDATA", "Volta", "bin"),
        ("LOCALAPPDATA", "Programs", "OpenAI", "Codex", "bin"),  # the Codex installer
        ("LOCALAPPDATA", "Programs", "OpenAI", "Codex"),
        ("LOCALAPPDATA", "Programs", "claude"),
        ("LOCALAPPDATA", "Programs", "Claude Code"),
        ("LOCALAPPDATA", "Programs", "Amazon", "AWSCLIV2"),  # the AWS CLI, per user
        ("LOCALAPPDATA", "Google", "Cloud SDK", "google-cloud-sdk", "bin"),
        ("LOCALAPPDATA", "Microsoft", "WinGet", "Links"),
        ("PROGRAMDATA", "chocolatey", "bin"),
        ("PROGRAMFILES", "Amazon", "AWSCLIV2"),  # the AWS CLI, for everyone
        ("PROGRAMFILES(X86)", "Amazon", "AWSCLIV2"),
        ("PROGRAMFILES", "Google", "Cloud SDK", "google-cloud-sdk", "bin"),
        ("PROGRAMFILES", "Microsoft SDKs", "Azure", "CLI2", "wbin"),
        ("PROGRAMFILES(X86)", "Microsoft SDKs", "Azure", "CLI2", "wbin"),
        ("PROGRAMFILES", "Docker", "Docker", "resources", "bin"),  # kubectl
        ("PROGRAMFILES", "Kubernetes"),
        ("PROGRAMFILES", "kubectl"),
        ("PROGRAMFILES", "helm"),
        ("PROGRAMFILES", "Helm"),
        ("PROGRAMFILES", "Rancher Desktop", *_RANCHER_BIN),
        ("LOCALAPPDATA", "Programs", "Rancher Desktop", *_RANCHER_BIN),
        ("LOCALAPPDATA", "Programs", "kubectl"),
        ("LOCALAPPDATA", "Programs", "helm"),
        ("PROGRAMFILES", "Oracle", "OCI CLI"),
        ("LOCALAPPDATA", "Programs", "Oracle", "OCI CLI"),
        ("PROGRAMFILES", "nodejs"),
        ("PROGRAMFILES", "nodejs", "node_modules", ".bin"),
        ("PROGRAMFILES", "Claude"),
        ("PROGRAMFILES", "OpenAI", "Codex", "bin"),
    ):
        if base := os.environ.get(variable):
            folders.append(Path(base, *parts))
    return list(dict.fromkeys(folders))


def find_program(program: str) -> str | None:
    """The full path of a program: on the path of the system or, on Windows, in
    the folders its installers use."""
    if found := shutil.which(program):
        return found
    if sys.platform != "win32" or os.path.dirname(program):
        return None
    for folder in _windows_folders():
        if found := shutil.which(program, path=str(folder)):
            return found
    return None
