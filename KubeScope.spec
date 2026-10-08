from pathlib import Path
import os
import platform
import sys

from PyInstaller.utils.hooks import collect_submodules


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

analysis = Analysis(
    [str(root / "src" / "kubescope" / "app.py")],
    pathex=[str(root / "src")],
    binaries=bundled_binaries,
    datas=[
        (str(root / "src" / "kubescope" / "assets" / "icon.png"), "kubescope/assets"),
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
