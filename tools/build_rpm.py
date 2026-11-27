"""Package dist/KubeScope (from `make build`) as an .rpm for Fedora and the
other distributions that use rpm.

The bundle is laid out like the .deb, packed in a tarball and installed
by a spec file; rpmbuild only has to wrap it (the bundle already carries
its own libraries, so rpm must not strip it or look for what it needs).
"""

import platform
import shutil
import subprocess
import sys
import tarfile

try:  # as a module (the tests) or as a script (tools/ is then the import path)
    from tools import build_deb, sync_changelog
except ImportError:
    import build_deb  # type: ignore[no-redef]
    import sync_changelog  # type: ignore[no-redef]

ROOT = build_deb.ROOT
BUNDLE = build_deb.BUNDLE
STAGING = ROOT / "build" / "rpm"

ARCHITECTURES = {"x86_64": "x86_64", "aarch64": "aarch64"}

# The same system libraries as the .deb (see DEPENDS there), by their names in
# Fedora.
REQUIRES = (
    "mesa-libEGL",
    "mesa-libGL",
    "libxcb",
    "libX11",
    "libX11-xcb",
    "libxkbcommon",
    "libxkbcommon-x11",
    "fontconfig",
    "freetype",
    "harfbuzz",
    "glib2",
    "dbus-libs",
    "libwayland-client",
    "libwayland-cursor",
    "libwayland-egl",
)
RECOMMENDS = ("dejavu-sans-fonts", "google-noto-sans-cjk-ttc-fonts")

SPEC = """\
%global debug_package %{{nil}}
%global __strip /bin/true
%global __os_install_post %{{nil}}
%global _build_id_links none
AutoReqProv: no

Name:           kubescope
Version:        {version}
Release:        1
Summary:        {summary}
License:        MIT AND LGPL-3.0-only
URL:            https://github.com/dcotecnologia/kubescope
Source0:        kubescope-root.tar.gz
ExclusiveArch:  {architecture}
{requires}

%description
KubeScope is a desktop IDE for Kubernetes: cluster overview, workloads, Pod
details and live logs.

%prep
%setup -q -n kubescope-root

%install
mkdir -p %{{buildroot}}
cp -a . %{{buildroot}}/

%files
%license /usr/share/licenses/kubescope/LICENSE
/opt/kubescope
/usr/bin/kubescope
/usr/share/applications/kubescope.desktop
/usr/share/doc/kubescope
/usr/share/icons/hicolor/*/apps/kubescope.png
"""


def spec_text(version: str, summary: str, architecture: str) -> str:
    """The spec file: rpm orders a release candidate with a tilde, like Debian."""
    lines = [f"Requires:       {name}" for name in REQUIRES]
    lines += [f"Recommends:     {name}" for name in RECOMMENDS]
    return SPEC.format(
        version=build_deb.debian_version(version),
        summary=summary,
        architecture=architecture,
        requires="\n".join(lines),
    )


def main() -> int:
    if sys.platform != "linux" or not shutil.which("rpmbuild"):
        raise SystemExit("Building an .rpm needs Linux with rpmbuild installed")
    if not (BUNDLE / "KubeScope").is_file():
        raise SystemExit("Run `make build` before packaging the .rpm")
    sync_changelog.main()
    sync_changelog.check_bundle(BUNDLE)
    architecture = ARCHITECTURES.get(platform.machine())
    if architecture is None:
        raise SystemExit(f"Unsupported architecture: {platform.machine()}")

    metadata = build_deb.project_metadata()
    version = metadata["version"]
    if STAGING.exists():
        shutil.rmtree(STAGING)
    root = STAGING / "kubescope-root"
    build_deb.lay_out(root)
    license_target = root / "usr/share/licenses/kubescope/LICENSE"
    build_deb.write(license_target, (ROOT / "LICENSE").read_text(encoding="utf-8"))

    for path in [root, *root.rglob("*")]:
        if path.is_symlink():
            continue
        if path.is_dir() or path.stat().st_mode & 0o111:
            path.chmod(0o755)
        else:
            path.chmod(0o644)

    sources = STAGING / "SOURCES"
    sources.mkdir(parents=True)
    with tarfile.open(sources / "kubescope-root.tar.gz", "w:gz") as archive:
        archive.add(root, arcname="kubescope-root")
    spec = STAGING / "kubescope.spec"
    spec.write_text(
        spec_text(version, metadata["description"], architecture), encoding="utf-8"
    )
    subprocess.run(
        [
            "rpmbuild",
            "-bb",
            "--define",
            f"_topdir {STAGING}",
            "--define",
            "_binary_payload w19.zstdio",
            str(spec),
        ],
        check=True,
    )
    built = sorted((STAGING / "RPMS").rglob("*.rpm"))
    if not built:
        raise SystemExit("rpmbuild produced no .rpm")
    output = ROOT / "dist" / built[0].name
    shutil.copy2(built[0], output)
    print(f"Created {output} ({output.stat().st_size / 2**20:.0f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
