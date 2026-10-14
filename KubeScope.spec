from pathlib import Path
import os
import platform
import subprocess
import sys

from PyInstaller.utils.hooks import copy_metadata, get_package_paths


root = Path(SPECPATH)
# The commit goes into the bundle, so a crash log can say which build it is from.
commit_file = root / "src" / "kubescope" / "_commit.txt"
try:
    commit_file.write_text(
        subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        + "\n",
        encoding="utf-8",
    )
except (OSError, subprocess.SubprocessError):
    pass  # not a git checkout: the log says "unknown"
commit_data = [(str(commit_file), "kubescope")] if commit_file.is_file() else []

bundled_binaries = []
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
        *commit_data,
        # the footer shows the version, which the app reads from this metadata
        *copy_metadata("kubescope"),
        (str(root / "src" / "kubescope" / "assets" / "icon.png"), "kubescope/assets"),
        (
            str(root / "src" / "kubescope" / "assets" / "THIRD_PARTY_NOTICES.txt"),
            "kubescope/assets",
        ),
        # next to the app's files, where a person who got the bundle finds them
        (str(root / "LICENSE"), "."),
        (str(root / "src" / "kubescope" / "assets" / "THIRD_PARTY_NOTICES.txt"), "."),
        *(
            (str(path), "kubescope/assets/fonts")
            for path in (root / "src" / "kubescope" / "assets" / "fonts").iterdir()
        ),
        *(
            (str(path), "kubescope/community_themes")
            for path in (root / "src" / "kubescope" / "community_themes").glob("*.json")
        ),
        *(
            (str(path), "kubescope/translations")
            for path in (root / "src" / "kubescope" / "translations").glob("*.qm")
        ),
    ],
    # Only these Qt modules are used. Collecting every PySide6 module would ship
    # Qt WebEngine (Chromium), Qt Charts and the rest, which the app never loads and
    # whose licenses (some GPL-only) the bundle would then have to honor.
    hiddenimports=["PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtWebEngineQuick",
        "PySide6.Qt3DCore",
        "PySide6.QtCharts",
        "PySide6.QtDataVisualization",
        "PySide6.QtQuick",
        "PySide6.QtQml",
        "PySide6.QtMultimedia",
        "PySide6.QtPdf",
        "PySide6.QtNetwork",
    ],
    noarchive=False,
    optimize=0,
)
# Qt parts a desktop widgets app never loads, which only come in through plugins:
# Qt Virtual Keyboard is GPL-3.0 only (the rest of Qt is LGPL-3.0), and Qt PDF
# carries Chromium's PDFium and its licenses; QML and Quick are not used at all.
not_shipped = ("virtualkeyboard", "qt6pdf", "libqpdf", "qt6quick", "qt6qml")
analysis.binaries = [
    entry for entry in analysis.binaries if not any(n in entry[0].lower() for n in not_shipped)
]
analysis.datas = [
    entry for entry in analysis.datas if not any(n in entry[0].lower() for n in not_shipped)
]
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
