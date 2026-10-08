"""Launcher for IDEs such as Qt Creator; the package lives under src/."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from kubescope.app import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
