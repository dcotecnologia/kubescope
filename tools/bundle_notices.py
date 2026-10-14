"""Write THIRD_PARTY_SYSTEM_LIBRARIES.txt into the Linux bundle.

python tools/bundle_notices.py

Run it after `pyinstaller KubeScope.spec`. PyInstaller copies the shared
libraries the app needs from the build machine (GTK, GLib, FreeType,
ICU, OpenSSL...). Each comes with its own license, which asks for its
notice to travel with the copy, so this finds the Debian package every
bundled library belongs to and writes that package's copyright file. It
fails when a library has no known package, so none goes out without a
notice.
"""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = (
    Path(os.environ.get("KUBESCOPE_BUNDLE", ROOT / "dist" / "KubeScope")) / "_internal"
)
VENDOR = ROOT / "vendor" / "linux"
OUTPUT_NAME = "THIRD_PARTY_SYSTEM_LIBRARIES.txt"
RULE = "=" * 78
# Qt and the Python interpreter are covered by THIRD_PARTY_NOTICES.txt, and the
# Python extension modules are the Python packages listed there.
# ICU comes inside the Qt for Python wheel, not from the system; the build machine's
# libicu package has the same license text.
SHIPPED_WITH_QT = {"libicu": "libicu[0-9]*"}
COVERED_PREFIXES = ("libQt6", "libpyside6", "libshiboken6", "libpython")


def bundled_libraries(bundle: Path) -> list[Path]:
    """The shared libraries PyInstaller copied next to the app (the ones in
    PySide6/ and the Python packages are covered elsewhere)."""
    return sorted(
        path
        for path in bundle.glob("*.so*")
        if path.is_file() and not path.name.startswith(COVERED_PREFIXES)
    )


def system_path(name: str) -> Path | None:
    """Where the build machine keeps a library, for its package to be found."""
    for vendored in VENDOR.rglob(name):
        return vendored
    listing = subprocess.run(
        ["ldconfig", "-p"], capture_output=True, text=True, check=True
    ).stdout
    for line in listing.splitlines():
        if line.strip().startswith(f"{name} "):
            return Path(line.rsplit("=>", 1)[1].strip())
    return None


def installed_package(pattern: str) -> str | None:
    result = subprocess.run(
        ["dpkg-query", "-W", "-f=${Package}\n", pattern],
        capture_output=True,
        text=True,
    )
    names = result.stdout.split() if result.returncode == 0 else []
    return names[0] if names else None


def package_of(path: Path) -> str | None:
    """The Debian package that owns a file, or None."""
    for candidate in dict.fromkeys((path, path.resolve())):
        result = subprocess.run(
            ["dpkg-query", "-S", str(candidate)], capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout.split(":", 1)[0].strip()
    return None


def copyright_of(package: str) -> str:
    path = Path("/usr/share/doc") / package / "copyright"
    staged = next(VENDOR.rglob(f"{package}.copyright"), None)  # not installed here
    path = staged or path
    return path.read_text(encoding="utf-8", errors="replace").strip()


def render(owners: dict[str, list[str]], copyrights: dict[str, str]) -> str:
    lines = [
        "KubeScope - system libraries in this package",
        RULE,
        "",
        "These shared libraries were copied into the package from the machine that",
        "built it. Each is the work of its own authors, under the license in the",
        "copyright file of the Debian package it came from, reproduced below.",
        "Libraries under the LGPL are shipped as separate files, so you can replace",
        "them with your own build.",
        "",
    ]
    for package, libraries in owners.items():
        lines += [RULE, f"{package}: {', '.join(libraries)}", RULE, ""]
        lines += [copyrights[package], ""]
    return "\n".join(line.rstrip() for line in lines) + "\n"


def main() -> int:
    if not BUNDLE.is_dir():
        raise SystemExit("Run `make build` first: there is no dist/KubeScope bundle")
    owners: dict[str, list[str]] = {}
    unknown = []
    for library in bundled_libraries(BUNDLE):
        source = system_path(library.name)
        package = package_of(source) if source else None
        if package is None and source is not None and VENDOR in source.parents:
            package = "libxcb-cursor0"  # staged by tools/fetch_linux_qt_libs.py
        for prefix, pattern in SHIPPED_WITH_QT.items():
            if package is None and library.name.startswith(prefix):
                package = installed_package(pattern)
        if package is None:
            unknown.append(library.name)
        else:
            owners.setdefault(package, []).append(library.name)
    if unknown:
        raise SystemExit(
            "No Debian package (so no license notice) for: " + ", ".join(unknown)
        )
    copyrights = {package: copyright_of(package) for package in owners}
    (BUNDLE / OUTPUT_NAME).write_text(
        render(dict(sorted(owners.items())), copyrights), encoding="utf-8"
    )
    print(f"Wrote {len(owners)} package notices to {BUNDLE / OUTPUT_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
