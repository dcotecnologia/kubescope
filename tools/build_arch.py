"""Package dist/KubeScope (from `make build`) as a package for Arch Linux and
the distributions that use pacman: `kubescope-<version>-1-<arch>.pkg.tar.zst`.

It is made without makepkg, so it builds on any Linux: a package is a
tarball with a `.PKGINFO` first, and pacman installs it with `pacman
-U`.
"""

import os
import platform
import shutil
import subprocess
import sys
import tarfile
import time

try:  # as a module (the tests) or as a script (tools/ is then the import path)
    from tools import build_deb, sync_changelog
except ImportError:
    import build_deb  # type: ignore[no-redef]
    import sync_changelog  # type: ignore[no-redef]

ROOT = build_deb.ROOT
BUNDLE = build_deb.BUNDLE
STAGING = ROOT / "build" / "arch"

ARCHITECTURES = {"x86_64": "x86_64", "aarch64": "aarch64"}

# The same system libraries as the .deb (see DEPENDS there), by their names in
# Arch.
DEPENDS = (
    "libglvnd",
    "libxcb",
    "libx11",
    "libxkbcommon",
    "libxkbcommon-x11",
    "fontconfig",
    "freetype2",
    "harfbuzz",
    "glib2",
    "dbus",
    "wayland",
)
OPTDEPENDS = (
    "ttf-dejavu: the default font",
    "noto-fonts-cjk: Chinese, Japanese and Korean text",
)


def pkginfo(
    version: str, description: str, architecture: str, size: int, built: int
) -> str:
    """The `.PKGINFO` that pacman reads.

    The package release is always 1: the
    version of the app is the one that changes.
    """
    lines = [
        "pkgname = kubescope",
        "pkgbase = kubescope",
        f"pkgver = {version}-1",
        f"pkgdesc = {description}",
        "url = https://github.com/dcotecnologia/kubescope",
        f"builddate = {built}",
        "packager = DCO Tecnologia",
        f"size = {size}",
        f"arch = {architecture}",
        "license = MIT",
        "license = LGPL3",
        *[f"depend = {name}" for name in DEPENDS],
        *[f"optdepend = {name}" for name in OPTDEPENDS],
    ]
    return "\n".join(lines) + "\n"


def _owned_by_root(info: tarfile.TarInfo) -> tarfile.TarInfo:
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    return info


def main() -> int:
    if sys.platform != "linux" or not shutil.which("zstd"):
        raise SystemExit("Building an Arch package needs Linux with zstd installed")
    if not (BUNDLE / "KubeScope").is_file():
        raise SystemExit("Run `make build` before packaging for Arch")
    sync_changelog.main()
    sync_changelog.check_bundle(BUNDLE)
    architecture = ARCHITECTURES.get(platform.machine())
    if architecture is None:
        raise SystemExit(f"Unsupported architecture: {platform.machine()}")

    metadata = build_deb.project_metadata()
    version = metadata["version"]
    if STAGING.exists():
        shutil.rmtree(STAGING)
    root = STAGING / "root"
    build_deb.lay_out(root)
    build_deb.write(
        root / "usr/share/licenses/kubescope/LICENSE",
        (ROOT / "LICENSE").read_text(encoding="utf-8"),
    )
    for path in [root, *root.rglob("*")]:
        if path.is_symlink():
            continue
        if path.is_dir() or path.stat().st_mode & 0o111:
            path.chmod(0o755)
        else:
            path.chmod(0o644)

    size = sum(
        path.lstat().st_size
        for path in root.rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    built = int(os.environ.get("SOURCE_DATE_EPOCH", time.time()))
    info_file = STAGING / ".PKGINFO"
    info_file.write_text(
        pkginfo(version, metadata["description"], architecture, size, built),
        encoding="utf-8",
    )

    tarball = STAGING / "kubescope.pkg.tar"
    with tarfile.open(tarball, "w") as archive:
        archive.add(info_file, arcname=".PKGINFO", filter=_owned_by_root)
        for path in sorted(root.rglob("*")):
            archive.add(
                path,
                arcname=path.relative_to(root).as_posix(),
                recursive=False,
                filter=_owned_by_root,
            )
    output = ROOT / "dist" / f"kubescope-{version}-1-{architecture}.pkg.tar.zst"
    subprocess.run(
        ["zstd", "-T0", "-19", "-f", "-q", str(tarball), "-o", str(output)], check=True
    )
    print(f"Created {output} ({output.stat().st_size / 2**20:.0f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
