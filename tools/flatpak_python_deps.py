"""Write the Flatpak module that installs the Kubernetes client from PyPI.

The Flatpak builds offline, so every Python package the app needs must
be a source with a URL and a sha256. This reads them from uv.lock (the
versions the tests ran with) and writes
packaging/flatpak/python3-kubernetes.json:

python tools/flatpak_python_deps.py

Packages with compiled code get one wheel per architecture, for the
Python of the runtime (PYTHON_TAG below); change it when the runtime
moves to another Python.
"""

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "packaging" / "flatpak" / "python3-kubernetes.json"
PYTHON_TAG = "cp313"
ARCHES = {"x86_64": "x86_64", "aarch64": "aarch64"}  # flatpak arch -> wheel arch


def closure(packages: dict, name: str) -> list[str]:
    found: set[str] = set()
    pending = [name]
    while pending:
        current = pending.pop()
        if current not in found:
            found.add(current)
            pending += [
                item["name"] for item in packages[current].get("dependencies", [])
            ]
    return sorted(found)


def sources(package: dict) -> list[dict]:
    wheels = package.get("wheels", [])

    def source(wheel: dict, arch: str | None = None) -> dict:
        digest = wheel["hash"].removeprefix("sha256:")
        entry = {"type": "file", "url": wheel["url"], "sha256": digest}
        if arch:
            entry["only-arches"] = [arch]
        return entry

    pure = [wheel for wheel in wheels if wheel["url"].endswith("-none-any.whl")]
    if pure:
        return [source(pure[0])]
    chosen = []
    for arch, wheel_arch in ARCHES.items():
        pattern = re.compile(
            rf"-({PYTHON_TAG}-{PYTHON_TAG}|cp3\d+-abi3)-manylinux\w*{wheel_arch}"
        )
        match = next(wheel for wheel in wheels if pattern.search(wheel["url"]))
        chosen.append(source(match, arch))
    return chosen


def main() -> None:
    with (ROOT / "uv.lock").open("rb") as handle:
        packages = {item["name"]: item for item in tomllib.load(handle)["package"]}
    files = [
        file
        for name in closure(packages, "kubernetes")
        for file in sources(packages[name])
    ]
    module = {
        "name": "python3-kubernetes",
        "buildsystem": "simple",
        "build-commands": [
            "pip3 install --verbose --exists-action=i --no-index "
            '--find-links="file://${PWD}" --prefix=${FLATPAK_DEST} "kubernetes" '
            "--no-build-isolation"
        ],
        "sources": files,
    }
    OUTPUT.write_text(json.dumps(module, indent=4) + "\n")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {len(files)} files")


if __name__ == "__main__":
    main()
