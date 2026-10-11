"""Launcher for IDEs such as Qt Creator; the package lives under src/."""

import ctypes
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

if sys.platform == "linux":
    # `make qt-libs` stages libxcb-cursor locally; load it up front so running
    # this file directly works without setting LD_LIBRARY_PATH.
    xcb_cursor = ROOT / "vendor" / "linux" / platform.machine() / "libxcb-cursor.so.0"
    if xcb_cursor.is_file():
        ctypes.CDLL(str(xcb_cursor), mode=ctypes.RTLD_GLOBAL)

if __name__ == "__main__":
    from kubescope.app import main

    raise SystemExit(main())
