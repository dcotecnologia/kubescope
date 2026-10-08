"""Package dist/KubeScope (from `make build`) as a Debian .deb."""

import hashlib
import platform
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "dist" / "KubeScope"
ICON = ROOT / "src" / "kubescope" / "assets" / "icon.png"
STAGING = ROOT / "build" / "deb"

ARCHITECTURES = {"x86_64": "amd64", "aarch64": "arm64"}
ICON_SIZES = (48, 64, 128, 256, 512)

# System libraries the PyInstaller bundle still loads (checked with ldd); Qt,
# xcb, xkbcommon and fontconfig are already inside the bundle.
DEPENDS = (
    "libegl1",
    "libgl1",
    "libxcb1",
    "libwayland-client0",
    "libwayland-cursor0",
    "libwayland-egl1",
)

DESKTOP_ENTRY = """[Desktop Entry]
Type=Application
Name=KubeScope
Comment=Desktop viewer for Kubernetes and Amazon EKS workloads
Exec=kubescope
Icon=kubescope
Terminal=false
Categories=Development;System;
StartupWMClass=KubeScope
"""


def project_metadata() -> dict:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]


def write(path: Path, content: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    path.chmod(mode)


def copyright_text() -> str:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    return (
        "Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/\n"
        "Upstream-Name: KubeScope\n"
        "Upstream-Contact: DCO Tecnologia\n"
        "Source: https://github.com/dcotecnologia/kubescope\n\n"
        "Files: *\n"
        "Copyright: 2026 DCO Tecnologia\n"
        "License: MIT\n\n"
        "License: MIT\n"
        + "".join(
            f" {line}\n" if line.strip() else " .\n"
            for line in license_text.splitlines()[2:]
        )
    )


def md5sums(root: Path) -> str:
    lines = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink() and "DEBIAN" not in path.parts:
            digest = hashlib.md5(path.read_bytes(), usedforsecurity=False).hexdigest()
            lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
    return "\n".join(lines) + "\n"


def main() -> int:
    if sys.platform != "linux" or not shutil.which("dpkg-deb"):
        raise SystemExit("Building a .deb needs Linux with dpkg-deb installed")
    if not (BUNDLE / "KubeScope").is_file():
        raise SystemExit("Run `make build` before packaging the .deb")
    architecture = ARCHITECTURES.get(platform.machine())
    if architecture is None:
        raise SystemExit(f"Unsupported architecture: {platform.machine()}")

    metadata = project_metadata()
    version = metadata["version"]
    package = STAGING / f"kubescope_{version}_{architecture}"
    if STAGING.exists():
        shutil.rmtree(STAGING)

    shutil.copytree(BUNDLE, package / "opt" / "kubescope", symlinks=True)
    binary = package / "usr" / "bin" / "kubescope"
    binary.parent.mkdir(parents=True)
    binary.symlink_to("/opt/kubescope/KubeScope")
    write(package / "usr/share/applications/kubescope.desktop", DESKTOP_ENTRY)
    write(package / "usr/share/doc/kubescope/copyright", copyright_text())

    source = QImage(str(ICON))
    for size in ICON_SIZES:
        target = package / f"usr/share/icons/hicolor/{size}x{size}/apps/kubescope.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        source.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        ).save(str(target), "PNG")

    # Debian policy: directories 755, executables 755, everything else 644
    for path in [package, *package.rglob("*")]:
        if path.is_symlink():
            continue
        if path.is_dir() or path.stat().st_mode & 0o111:
            path.chmod(0o755)
        else:
            path.chmod(0o644)

    glibc = platform.libc_ver()[1] or "2.35"
    size_kib = (
        sum(
            path.lstat().st_size
            for path in package.rglob("*")
            if path.is_file() and not path.is_symlink()
        )
        // 1024
    )
    control = (
        "Package: kubescope\n"
        f"Version: {version}\n"
        "Section: devel\n"
        "Priority: optional\n"
        f"Architecture: {architecture}\n"
        f"Depends: libc6 (>= {glibc}), {', '.join(DEPENDS)}\n"
        "Recommends: fonts-dejavu-core | fonts-noto-core\n"
        f"Installed-Size: {size_kib}\n"
        f"Maintainer: DCO Tecnologia <{metadata['authors'][0]['email']}>\n"
        "Homepage: https://github.com/dcotecnologia/kubescope\n"
        f"Description: {metadata['description']}\n"
        " KubeScope is a read-only desktop console for Kubernetes and Amazon EKS:\n"
        " cluster overview, workloads, Pod details and live logs. It bundles its\n"
        " own kubectl.\n"
    )
    write(package / "DEBIAN" / "control", control)
    write(package / "DEBIAN" / "md5sums", md5sums(package))
    (package / "DEBIAN").chmod(0o755)

    output = ROOT / "dist" / f"kubescope_{version}_{architecture}.deb"
    subprocess.run(
        [
            "dpkg-deb",
            "--root-owner-group",
            "-Zxz",
            "--build",
            str(package),
            str(output),
        ],
        check=True,
    )
    print(f"Created {output} ({output.stat().st_size / 2**20:.0f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
