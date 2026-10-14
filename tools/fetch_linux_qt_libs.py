import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "libxcb-cursor0"


def main() -> int:
    if platform.system() != "Linux":
        print("Qt XCB libraries are only needed on Linux")
        return 0

    destination = ROOT / "vendor" / "linux" / platform.machine()
    library_target = destination / "libxcb-cursor.so.0"
    # its license notice travels with it into the bundle (tools/bundle_notices.py)
    copyright_target = destination / f"{PACKAGE_NAME}.copyright"
    if library_target.is_file() and copyright_target.is_file():
        print(f"Using staged library: {library_target}")
        return 0

    with tempfile.TemporaryDirectory(prefix="kubescope-xcb-") as temp_dir:
        download_dir = Path(temp_dir) / "download"
        extract_dir = Path(temp_dir) / "extract"
        download_dir.mkdir()
        extract_dir.mkdir()
        subprocess.run(
            ["apt-get", "download", PACKAGE_NAME],
            check=True,
            cwd=download_dir,
        )
        package = next(download_dir.glob("*.deb"), None)
        if package is None:
            raise RuntimeError(f"apt-get did not download {PACKAGE_NAME}")
        subprocess.run(
            ["dpkg-deb", "-x", str(package), str(extract_dir)],
            check=True,
        )
        library = next(extract_dir.rglob("libxcb-cursor.so.0"), None)
        if library is None:
            raise RuntimeError(f"{PACKAGE_NAME} did not contain libxcb-cursor.so.0")
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(library, library_target)
        notice = next(extract_dir.rglob("copyright"), None)
        if notice is None:
            raise RuntimeError(f"{PACKAGE_NAME} did not contain its copyright file")
        shutil.copy2(notice, copyright_target)

    print(f"Staged {library_target}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError, RuntimeError) as error:
        print(f"Unable to stage Linux Qt libraries: {error}", file=sys.stderr)
        raise SystemExit(1) from error
