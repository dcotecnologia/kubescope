"""Regenerate every ui_*.py from its .ui file with pyside6-uic.

Run it through `uv run` so it works the same on every platform, with no
shell needed. It exits with the first failing uic status.
"""

import subprocess
import sys
from pathlib import Path

UI_DIR = Path(__file__).resolve().parent.parent / "src" / "kubescope" / "ui"
BIN = Path(sys.executable).parent


def main() -> int:
    uic = BIN / "pyside6-uic"
    for source in sorted(UI_DIR.glob("*.ui")):
        target = source.with_name(f"ui_{source.stem}.py")
        status = subprocess.run(
            [str(uic), str(source), "-o", str(target)], check=False
        ).returncode
        if status:
            return status
    return 0


if __name__ == "__main__":
    sys.exit(main())
