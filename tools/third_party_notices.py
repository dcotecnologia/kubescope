"""Write assets/THIRD_PARTY_NOTICES.txt, the licenses a build ships.

python tools/third_party_notices.py

python tools/third_party_notices.py --check

The first rewrites the file; the second fails if it is out of date.

The packages come from uv.lock (what the app needs to run, without the
dev and build extras) and their license files from the installed
distributions, so run it in an environment made by `make setup`. The
file travels in every package: the licenses ask for their notice to
accompany the binaries.
"""

import hashlib
import sys
import tomllib
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# inside the package, so every channel (the bundle, pip, the Flatpak) carries it
OUTPUT = ROOT / "src" / "kubescope" / "assets" / "THIRD_PARTY_NOTICES.txt"
LICENSES = ROOT / "packaging" / "licenses"
FONTS_LICENSE = ROOT / "src" / "kubescope" / "assets" / "fonts" / "LICENSE.txt"

# Qt for Python is one project in several wheels; the app uses Core, Gui and
# Widgets, and the bundle leaves out the rest (see KubeScope.spec).
QT_PACKAGES = {"pyside6", "pyside6-essentials", "pyside6-addons", "shiboken6"}
NOT_BUNDLED = {"pyside6-pdf", "pyside6-webengine"}
RULE = "=" * 78


def runtime_packages(lock: dict) -> dict[str, str]:
    """Name -> version of kubescope's dependencies and theirs, from uv.lock."""
    packages = {entry["name"]: entry for entry in lock["package"]}
    found: dict[str, str] = {}
    pending = [dep["name"] for dep in packages["kubescope"].get("dependencies", [])]
    while pending:
        name = pending.pop()
        if name in found or name in NOT_BUNDLED:
            continue
        found[name] = packages[name]["version"]
        pending += [dep["name"] for dep in packages[name].get("dependencies", [])]
    return dict(sorted(found.items()))


def license_name(info: metadata.PackageMetadata) -> str:
    expression = info.get("License-Expression") or ""
    if expression:
        return expression
    classifiers = [
        text.split("::")[-1].strip()
        for text in info.get_all("Classifier") or []
        if text.startswith("License ::")
    ]
    free_text = (info.get("License") or "").strip()
    if classifiers:
        return " / ".join(classifiers)
    return free_text.splitlines()[0] if free_text else "see the license text"


def license_files(distribution: metadata.Distribution) -> list[tuple[str, str]]:
    """The (name, text) of the files a distribution ships as its license,
    notice or copying terms, from its own metadata folder."""
    files = []
    for file in distribution.files or []:
        upper = file.name.upper()
        if file.parent.name == "licenses" or file.parent.parent.name == "licenses":
            pass  # the PEP 639 folder: every file in it is a license text
        elif not upper.startswith(("LICENSE", "LICENCE", "COPYING", "NOTICE")):
            continue
        if ".dist-info" not in str(file) and ".egg-info" not in str(file):
            continue  # a file of the package itself, not its metadata
        path = Path(str(distribution.locate_file(file)))
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            files.append((file.name, text))
    return files


def clean(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def build() -> str:
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    packages = runtime_packages(lock)
    lines = [
        "KubeScope - third-party notices",
        RULE,
        "",
        "KubeScope is released under the MIT License (see LICENSE). It includes or",
        "uses the software below, each under its own license. This file reproduces",
        "their notices and license texts, as those licenses require.",
        "",
        "Packages",
        "--------",
        "",
    ]
    sections: list[str] = []
    seen: dict[str, str] = {}  # hash of a text -> the package that printed it
    for name, version in packages.items():
        distribution = metadata.distribution(name)
        info = distribution.metadata
        qt = name in QT_PACKAGES
        lines.append(
            f"  {name} {version} - "
            f"{'LGPL-3.0-only (Qt for Python and Qt)' if qt else license_name(info)}"
        )
        texts = [] if qt else license_files(distribution)
        body = []
        for file_name, text in texts:
            digest = hashlib.sha256(clean(text).encode()).hexdigest()
            if digest in seen:
                body.append(f"{file_name}: the same text as {seen[digest]} above.")
            else:
                seen[digest] = f"{name} {version}"
                body.append(f"{file_name}:\n\n{clean(text)}")
        if body:
            sections += [RULE, f"{name} {version}", RULE, "", "\n\n".join(body), ""]
    lines += ["", *QT_NOTICE, "", *fixed_texts(), "", *sections]
    return "\n".join(lines).rstrip() + "\n"


QT_NOTICE = [
    RULE,
    "Qt and Qt for Python (PySide6, Shiboken6)",
    RULE,
    "",
    "KubeScope uses the Qt libraries (QtCore, QtGui and QtWidgets) through Qt for",
    "Python. They are used under the GNU Lesser General Public License, version 3",
    "(LGPL-3.0-only). Copyright (C) The Qt Company Ltd. and other contributors.",
    "",
    "The Qt libraries are shipped as separate shared libraries in the package, not",
    "linked statically, so you can replace them with your own build of the same",
    "Qt version. KubeScope itself is not changed by this, and you may modify and",
    "debug it for your own use.",
    "",
    "The corresponding source code of Qt and of Qt for Python is available from:",
    "",
    "  https://download.qt.io/official_releases/qt/",
    "  https://code.qt.io/cgit/pyside/pyside-setup.git/",
    "",
    "Only the LGPL parts of Qt are shipped; Qt modules that are GPL-only (such as",
    "Qt Virtual Keyboard, Qt Charts and Qt Data Visualization) are left out.",
    "The full texts of the LGPL-3.0 and of the GPL-3.0 it refers to follow.",
]


def fixed_texts() -> list[str]:
    def section(title: str, intro: list[str], text: str) -> list[str]:
        return [RULE, title, RULE, "", *intro, "", clean(text), ""]

    return [
        *section(
            "Noto Sans and Noto Sans Mono (the bundled fonts)",
            [],
            FONTS_LICENSE.read_text(encoding="utf-8"),
        ),
        *section(
            "GNU Lesser General Public License, version 3 (Qt for Python and Qt)",
            [],
            (LICENSES / "LGPL-3.0.txt").read_text(encoding="utf-8"),
        ),
        *section(
            "GNU General Public License, version 3 (referred to by the LGPL-3.0)",
            [],
            (LICENSES / "GPL-3.0.txt").read_text(encoding="utf-8"),
        ),
        *section(
            "Python (the interpreter that runs inside the bundle)",
            [
                "The interpreter is CPython, under the Python Software Foundation",
                "License; this is the LICENSE file of CPython, the same text for",
                "every 3.x release. It is built with OpenSSL (Apache-2.0, the text",
                "is above), expat and libffi (MIT), zlib, mpdecimal and others; the",
                "notices of the ones that are separate libraries on Linux are in",
                "THIRD_PARTY_SYSTEM_LIBRARIES.txt, next to this file.",
                "",
                "Qt also bundles code of other projects (FreeType, HarfBuzz, libpng,",
                "PCRE2, zlib and more) under their own licenses, listed with their",
                "notices at https://doc.qt.io/qt-6/licenses-used-in-qt.html",
            ],
            (LICENSES / "Python-PSF-2.0.txt").read_text(encoding="utf-8"),
        ),
        *section(
            "PyInstaller (the tool that makes the bundle)",
            [
                "The bundle's launcher is PyInstaller's bootloader, GPL-2.0-or-later",
                "with an exception that lets it ship with programs under any license:",
                "https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt",
            ],
            "",
        ),
    ]


def main() -> int:
    text = build()
    if "--check" in sys.argv:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != text:
            print("THIRD_PARTY_NOTICES.txt is out of date; run this script.")
            return 1
        return 0
    OUTPUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
