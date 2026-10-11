"""Run KubeScope and restart it whenever its source changes.

Saving a .py file restarts the app; saving a .ui file regenerates its
ui_*.py first, and saving a .ts file recompiles its .qm. It polls file
times, so it needs no extra dependency. Stop it with Ctrl+C.
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src" / "kubescope"
BIN = Path(sys.executable).parent
INTERVAL = 0.5


def watched() -> dict[Path, float]:
    """Every file whose change means a restart, with its modification time.

    The generated ui_*.py are left out: they change when their .ui does.
    """
    files = [
        path
        for pattern in ("*.py", "*.ui", "*.ts", "*.json")
        for path in SOURCE.rglob(pattern)
        if not path.name.startswith("ui_")
    ]
    return {path: path.stat().st_mtime for path in files}


def rebuild(path: Path) -> bool:
    """Regenerate what the changed file produces; False if that failed."""
    if path.suffix == ".ui":
        target = path.with_name(f"ui_{path.stem}.py")
        command = [str(BIN / "pyside6-uic"), str(path), "-o", str(target)]
    elif path.suffix == ".ts":
        command = [
            str(BIN / "pyside6-lrelease"),
            str(path),
            "-qm",
            str(path.with_suffix(".qm")),
        ]
    else:
        return True
    return subprocess.run(command, check=False).returncode == 0


def start() -> subprocess.Popen:
    print("dev: starting KubeScope", flush=True)
    return subprocess.Popen([sys.executable, str(ROOT / "main.py")])


def stop(app: subprocess.Popen) -> None:
    app.terminate()
    try:
        app.wait(10)
    except subprocess.TimeoutExpired:
        app.kill()
        app.wait()


def main() -> int:
    known = watched()
    app = start()
    try:
        while True:
            time.sleep(INTERVAL)
            current = watched()
            changed = [
                path for path, mtime in current.items() if known.get(path) != mtime
            ]
            if not changed and app.poll() is None:
                known = current
                continue
            if not changed:  # the app closed or crashed: wait for the next edit
                print("dev: KubeScope exited; waiting for a change", flush=True)
                while watched() == current:
                    time.sleep(INTERVAL)
                changed = [
                    path
                    for path, mtime in watched().items()
                    if current.get(path) != mtime
                ]
            print(
                "dev: changed " + ", ".join(path.name for path in changed), flush=True
            )
            if all(rebuild(path) for path in changed):
                if app.poll() is None:
                    stop(app)
                app = start()
            known = watched()
    except KeyboardInterrupt:
        if app.poll() is None:
            stop(app)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
