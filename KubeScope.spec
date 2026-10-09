from pathlib import Path
import os
import platform
import sys

from PyInstaller.utils.hooks import collect_submodules, copy_metadata, get_package_paths


root = Path(SPECPATH)
kubectl_name = "kubectl.exe" if os.name == "nt" else "kubectl"
kubectl = root / "vendor" / "kubectl" / kubectl_name
if not kubectl.is_file():
    raise FileNotFoundError("Run python tools/fetch_kubectl.py before building")

bundled_binaries = [(str(kubectl), "kubectl")]
if sys.platform == "linux":
    xcb_cursor = (
        root
        / "vendor"
        / "linux"
        / platform.machine()
        / "libxcb-cursor.so.0"
    )
    if not xcb_cursor.is_file():
        raise FileNotFoundError(
            "Run python tools/fetch_linux_qt_libs.py before building on Linux"
        )
    bundled_binaries.append((str(xcb_cursor), "."))

# The PySide6 hook can miss the Qt plugins (seen in Wine builds), which leaves the
# app unable to start: "no Qt platform plugin could be initialized". Bundle the
# ones the app needs explicitly.
qt_plugins = []
if sys.platform == "win32":
    plugins_dir = Path(get_package_paths("PySide6")[1]) / "plugins"
    for name in ("platforms", "styles", "imageformats", "iconengines"):
        folder = plugins_dir / name
        if not folder.is_dir():
            raise FileNotFoundError(f"Qt plugin folder not found: {folder}")
        qt_plugins.append((str(folder), f"PySide6/plugins/{name}"))

analysis = Analysis(
    [str(root / "src" / "kubescope" / "app.py")],
    pathex=[str(root / "src")],
    binaries=bundled_binaries,
    datas=[
        *qt_plugins,
        # the footer shows the version, which the app reads from this metadata
        *copy_metadata("kubescope"),
        (str(root / "src" / "kubescope" / "assets" / "icon.png"), "kubescope/assets"),
        *(
            (str(path), "kubescope/community_themes")
            for path in (root / "src" / "kubescope" / "community_themes").glob("*.json")
        ),
        *(
            (str(path), "kubescope/translations")
            for path in (root / "src" / "kubescope" / "translations").glob("*.qm")
        ),
    ],
    hiddenimports=collect_submodules("PySide6"),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(analysis.pure)
executable = EXE(
    pyz,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="KubeScope",
    icon=str(root / "src" / "kubescope" / "assets" / "icon.ico") if os.name == "nt" else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
COLLECT(
    executable,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="KubeScope",
)
