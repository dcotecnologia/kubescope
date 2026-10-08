import hashlib
import os
import platform
import sys
import tempfile
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "vendor" / "kubectl"


def target_platform() -> tuple[str, str, str]:
    operating_system = platform.system().lower()
    architecture = platform.machine().lower()
    architectures = {
        "aarch64": "arm64",
        "arm64": "arm64",
        "x86_64": "amd64",
        "amd64": "amd64",
    }
    if operating_system not in {"linux", "darwin", "windows"}:
        raise RuntimeError(f"Unsupported operating system: {operating_system}")
    if architecture not in architectures:
        raise RuntimeError(f"Unsupported architecture: {architecture}")
    executable_name = "kubectl.exe" if operating_system == "windows" else "kubectl"
    return operating_system, architectures[architecture], executable_name


def download(url: str) -> bytes:
    with urlopen(url, timeout=30) as response:
        return response.read()


def main() -> int:
    version = os.environ.get("KUBECTL_VERSION")
    if not version:
        version = download("https://dl.k8s.io/release/stable.txt").decode().strip()
    if not version.startswith("v"):
        raise RuntimeError("KUBECTL_VERSION must look like v1.34.1")

    operating_system, architecture, executable_name = target_platform()
    base_url = (
        f"https://dl.k8s.io/release/{version}/bin/"
        f"{operating_system}/{architecture}/kubectl"
    )
    binary = download(f"{base_url}{'.exe' if operating_system == 'windows' else ''}")
    expected_hash = download(
        f"{base_url}{'.exe' if operating_system == 'windows' else ''}.sha256"
    )
    expected_hash = expected_hash.decode().strip().split()[0]
    actual_hash = hashlib.sha256(binary).hexdigest()
    if actual_hash != expected_hash:
        raise RuntimeError("kubectl SHA-256 verification failed")

    DESTINATION.mkdir(parents=True, exist_ok=True)
    target = DESTINATION / executable_name
    with tempfile.NamedTemporaryFile(dir=DESTINATION, delete=False) as temporary:
        temporary.write(binary)
        temporary_path = Path(temporary.name)
    temporary_path.replace(target)
    if operating_system != "windows":
        target.chmod(0o755)
    print(f"Installed verified kubectl {version} for {operating_system}/{architecture}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, URLError, RuntimeError) as error:
        print(f"Unable to fetch kubectl: {error}", file=sys.stderr)
        raise SystemExit(1) from error
