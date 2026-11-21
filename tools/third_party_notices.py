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
    lines += [
        "",
        *qt_notice(packages["pyside6"]),
        "",
        *fixed_texts(packages),
        "",
        *sections,
    ]
    return "\n".join(lines).rstrip() + "\n"


ISSUES = "https://github.com/dcotecnologia/kubescope/issues"


def qt_notice(version: str) -> list[str]:
    """What the LGPL-3.0 asks to travel with Qt: that it is used, under which
    license, where the exact source is, how to replace the libraries, and that
    nothing here takes those rights away.

    Qt for Python has the version of the Qt it ships.
    """
    series = ".".join(version.split(".")[:2])
    return [
        RULE,
        "Qt and Qt for Python (PySide6, Shiboken6)",
        RULE,
        "",
        "KubeScope is built with Qt for Python (PySide6 and Shiboken6) and Qt "
        f"{version}.",
        "They are used under the GNU Lesser General Public License, version 3",
        "(LGPL-3.0-only). Copyright (C) The Qt Company Ltd. and other contributors.",
        "The libraries used are QtCore, QtGui, QtNetwork and QtWidgets, with the Qt",
        "plugins they load (platforms, styles, image formats and icon engines).",
        "",
        "The Qt libraries are the ones The Qt Company publishes in the PySide6",
        f"{version} wheels. KubeScope does not change the code of Qt.",
        "",
        "The corresponding source code",
        "-----------------------------",
        "",
        f"  Qt {version}:",
        f"    https://download.qt.io/official_releases/qt/{series}/{version}/single/",
        f"    https://download.qt.io/archive/qt/{series}/{version}/single/",
        f"  Qt for Python {version} (tag v{version}):",
        "    https://code.qt.io/cgit/pyside/pyside-setup.git/",
        "",
        "If you cannot get it from there, ask for it at",
        f"  {ISSUES}",
        "and it is sent to you, or a link to it, for as long as this version of",
        "KubeScope is distributed and for at least three years after.",
        "",
        "Replacing the Qt libraries",
        "--------------------------",
        "",
        "The Qt libraries are separate shared libraries, not linked into the",
        "KubeScope program, so you can replace them with your own build of the same",
        "Qt version (a build that keeps the binary interface). KubeScope starts and",
        "runs with whatever it finds; it does not check them. They are in the PySide6",
        "folder of the _internal folder of the application:",
        "",
        "  .deb          /opt/kubescope/_internal/PySide6/Qt/lib/",
        "  Windows       the _internal\\PySide6\\ folder of the install folder",
        "  tarball, zip  KubeScope/_internal/PySide6/Qt/lib/",
        "  macOS         PySide6/ inside KubeScope.app/Contents",
        "  AppImage      ./KubeScope.AppImage --appimage-extract, change the files",
        "                in squashfs-root/ and start squashfs-root/AppRun",
        "  Flatpak, Snap Qt comes from the runtime (org.kde.Platform and the",
        "                io.qt.PySide.BaseApp base app) and not from the package:",
        "                use a runtime of your own, or build the package as",
        "                docs/guides/Building-from-source.md says",
        "  pip           a PySide6 of another build in the same environment",
        "",
        "Nothing in the MIT License of KubeScope, in this file or in the installers",
        "limits what the LGPL-3.0 gives you for Qt: you may use, modify and replace",
        "it, and look inside KubeScope (its source is open) to debug your changes.",
        "",
        "Only the LGPL parts of Qt are shipped; Qt modules that are GPL-only (such as",
        "Qt Virtual Keyboard, Qt Charts and Qt Data Visualization) are left out.",
        "The full texts of the LGPL-3.0 and of the GPL-3.0 it refers to follow, and",
        "are also in the licenses folder of the application.",
    ]


def fixed_texts(packages: dict[str, str]) -> list[str]:
    def section(title: str, intro: list[str], text: str) -> list[str]:
        body = [clean(text), ""] if text.strip() else []
        return [RULE, title, RULE, "", *intro, "", *body]

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
                "THIRD_PARTY_SYSTEM_LIBRARIES.txt, next to this file. On Windows the",
                "Microsoft Visual C++ runtime (vcruntime140.dll, msvcp140.dll) comes",
                "with Python and is shipped under Microsoft's terms for it. The source",
                "code of Python is at https://www.python.org/downloads/source/",
            ],
            (LICENSES / "Python-PSF-2.0.txt").read_text(encoding="utf-8"),
        ),
        *section(
            "Components built into Qt",
            [
                "The Qt libraries contain code of other projects, under their own",
                "licenses, among them FreeType, HarfBuzz, libpng, libjpeg, zlib,",
                "PCRE2, double-conversion, md4c and ICU. Their licenses are permissive",
                "(BSD, MIT and zlib type, the FreeType License and the Unicode",
                "License) and ask that their notices travel with the binaries. The",
                "notices, with the text of each license, are published by Qt at",
                "https://doc.qt.io/qt-6/licenses-used-in-qt.html and are in the source",
                "code of Qt linked above (the 3rdparty folders). On Linux, the notices",
                "of the ones that are separate files are in",
                "THIRD_PARTY_SYSTEM_LIBRARIES.txt, next to this file.",
                "",
                "Portions of this software are copyright (c) The FreeType Project",
                "(www.freetype.org). All rights reserved.",
            ],
            "",
        ),
        *section(
            f"certifi {packages['certifi']} (Mozilla Public License 2.0)",
            [
                "certifi is used as it is published: KubeScope does not change it. The",
                "MPL-2.0 asks to say where its source code is, and it is at",
                f"https://pypi.org/project/certifi/{packages['certifi']}/#files and at",
                "https://github.com/certifi/python-certifi. The bundle of certificates",
                "in it is the one of Mozilla (https://wiki.mozilla.org/CA). The text",
                "of the MPL-2.0 is in the certifi section below.",
            ],
            "",
        ),
        *section(
            "The AppImage runtime (the AppImage packages only)",
            [
                "An AppImage file begins with the AppImage runtime, MIT License,",
                "https://github.com/AppImage/type2-runtime, which comes with the",
                "libraries it is built with; that project lists them, with their",
                "licenses and source code.",
            ],
            "",
        ),
        *section(
            "Color themes",
            [
                "The viewers of logs and JSON are colored like Monokai (by Wimer",
                "Hazenberg), and the color themes of KubeScope and of its Themes",
                "extension take the look of well-known ones: Solarized (Ethan",
                "Schoonover, MIT), Tomorrow Night Blue (Chris Kempson, MIT), and",
                "Abyss, Dark Modern, Light Modern, High Contrast and Quiet Light of",
                "Visual Studio Code (Microsoft, MIT). Only colors are used, no code or",
                "file of those projects. Their names belong to their owners; macOS is",
                "a trademark of Apple Inc. and only says what a theme looks like.",
            ],
            "",
        ),
        *section(
            "The extensions that ship with KubeScope",
            [
                "Gabi, AWS Resources, Global Search and Themes are written by DCO",
                "Tecnologia and released under the MIT License, as KubeScope is; each",
                "one has its own LICENSE file in its package, and their dependencies",
                "are the ones listed above.",
            ],
            "",
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
