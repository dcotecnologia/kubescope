"""Build the Windows packages: installer (needs Inno Setup) and a portable zip.

Run it on Windows (`make windows`). On Linux, `make windows` runs it in
Wine through windows_wine.py, because PyInstaller cannot cross-build.
"""

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

try:  # as a module (the tests) or as a script (tools/ is then the import path)
    from tools import sync_changelog
except ImportError:
    import sync_changelog  # type: ignore[no-redef]

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
            "Windows packages must be built on Windows or in Wine. From Linux run "
            "`make windows`, or `make windows-remote` to build on GitHub Actions."
        )
    with (ROOT / "pyproject.toml").open("rb") as handle:
        version = tomllib.load(handle)["project"]["version"]

    sync_changelog.main()  # the app shows the changelog of the version it ships
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
