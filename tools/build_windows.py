"""Build the Windows packages: installer (needs Inno Setup) and a portable zip.

Run it on Windows (`make windows`); PyInstaller cannot cross-build from Linux.
"""

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
BUNDLE = DIST / "KubeScope"
INSTALLER_SCRIPT = ROOT / "packaging" / "windows" / "kubescope.iss"
ISCC_CANDIDATES = (
    "iscc",
    r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    r"C:\Program Files\Inno Setup 6\ISCC.exe",
)


def run(*command: str) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, check=True, cwd=ROOT)


def find_iscc() -> str | None:
    for candidate in ISCC_CANDIDATES:
        found = shutil.which(candidate)
        if found:
            return found
    return None


def main() -> int:
    if sys.platform != "win32":
        raise SystemExit(
            "Windows packages must be built on Windows. From another system run "
            "`make windows-remote` to build them on GitHub Actions."
        )
    with (ROOT / "pyproject.toml").open("rb") as handle:
        version = tomllib.load(handle)["project"]["version"]

    if not (ROOT / "vendor" / "kubectl" / "kubectl.exe").is_file():
        run(sys.executable, "tools/fetch_kubectl.py")
    run(sys.executable, "-m", "PyInstaller", "--noconfirm", "KubeScope.spec")

    archive = shutil.make_archive(
        str(DIST / f"KubeScope-{version}-windows-x64"), "zip", DIST, "KubeScope"
    )
    print(f"Created {archive}")

    iscc = find_iscc()
    if iscc is None:
        print(
            "Inno Setup not found: skipped the installer "
            "(winget install JRSoftware.InnoSetup)"
        )
        return 0
    run(iscc, f"/DAppVersion={version}", str(INSTALLER_SCRIPT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
