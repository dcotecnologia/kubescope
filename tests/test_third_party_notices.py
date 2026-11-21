import tomllib

from tools import bundle_notices, third_party_notices


def test_the_notices_cover_every_runtime_dependency_and_are_up_to_date() -> None:
    lock = tomllib.loads(
        (third_party_notices.ROOT / "uv.lock").read_text(encoding="utf-8")
    )
    notices = third_party_notices.OUTPUT.read_text(encoding="utf-8")
    packages = third_party_notices.runtime_packages(lock)

    assert {"kubernetes", "pyside6", "certifi"} <= set(packages)
    assert not {"pyinstaller", "pytest", "pyside6-webengine"} & set(packages)
    for name, version in packages.items():
        assert f"  {name} {version} - " in notices
    assert "GNU LESSER GENERAL PUBLIC LICENSE" in notices.upper()
    assert third_party_notices.main.__module__  # the script is importable


def test_the_notices_file_matches_what_the_script_writes(monkeypatch) -> None:
    monkeypatch.setattr("sys.argv", ["third_party_notices.py", "--check"])
    assert third_party_notices.main() == 0


def test_bundle_notices_group_libraries_by_package_and_skip_covered_ones(
    tmp_path,
) -> None:
    for name in (
        "libz.so.1",
        "libQt6Core.so.6",
        "libpython3.14.so.1.0",
        "libpng16.so.16",
    ):
        (tmp_path / name).write_bytes(b"")

    libraries = [path.name for path in bundle_notices.bundled_libraries(tmp_path)]
    text = bundle_notices.render(
        {"zlib1g": ["libz.so.1"], "libpng16-16t64": ["libpng16.so.16"]},
        {"zlib1g": "zlib copyright  ", "libpng16-16t64": "png copyright"},
    )

    assert libraries == ["libpng16.so.16", "libz.so.1"]
    assert "zlib1g: libz.so.1" in text and "zlib copyright\n" in text
    assert "png copyright" in text


def test_the_qt_notice_says_what_the_lgpl_asks_for() -> None:
    lock = tomllib.loads(
        (third_party_notices.ROOT / "uv.lock").read_text(encoding="utf-8")
    )
    version = third_party_notices.runtime_packages(lock)["pyside6"]
    series = ".".join(version.split(".")[:2])
    notices = third_party_notices.OUTPUT.read_text(encoding="utf-8")

    assert f"Qt {version}" in notices  # which Qt is in the package
    assert "LGPL-3.0-only" in notices
    assert f"qt/{series}/{version}/single/" in notices  # the source of that version
    assert f"tag v{version}" in notices  # and of Qt for Python
    assert third_party_notices.ISSUES in notices  # where to ask for it
    assert "does not change the code of Qt" in notices
    assert "Replacing the Qt libraries" in notices
    for place in (".deb", "Windows", "AppImage", "Flatpak, Snap", "pip"):
        assert place in notices  # how to replace them, for each way of installing
    assert "limits what the LGPL-3.0 gives you" in notices  # no right is taken away


def test_the_packages_carry_the_license_texts_and_say_that_they_use_qt() -> None:
    from tools import build_deb

    root = third_party_notices.ROOT
    spec = (root / "KubeScope.spec").read_text(encoding="utf-8")
    installer = (root / "packaging/windows/kubescope.iss").read_text(encoding="utf-8")
    copyright_file = build_deb.copyright_text()

    assert '"licenses"' in spec and "packaging" in spec  # LGPL-3.0 as a file
    assert (root / "packaging/licenses/LGPL-3.0.txt").is_file()
    assert "InfoBeforeFile=QT_NOTICE.txt" in installer
    notice = (root / "packaging/windows/QT_NOTICE.txt").read_text(encoding="utf-8")
    assert "LGPL-3.0" in notice and "_internal\\PySide6" in notice
    assert "License: LGPL-3" in copyright_file
    assert "/usr/share/common-licenses/LGPL-3" in copyright_file
    assert "License: MIT\n Copyright (c) 2026 DCO Tecnologia" in copyright_file


def test_the_notices_cover_what_the_other_licenses_ask_for() -> None:
    lock = tomllib.loads(
        (third_party_notices.ROOT / "uv.lock").read_text(encoding="utf-8")
    )
    certifi = third_party_notices.runtime_packages(lock)["certifi"]
    notices = third_party_notices.OUTPUT.read_text(encoding="utf-8")

    # the FreeType License: a credit for the FreeType inside Qt
    assert "copyright (c) The FreeType Project" in notices
    assert "https://doc.qt.io/qt-6/licenses-used-in-qt.html" in notices
    # the MPL-2.0: where the source code of certifi is, for the version shipped
    assert f"https://pypi.org/project/certifi/{certifi}/#files" in notices
    assert "Mozilla Public License" in notices
    # what the build tools put in the packages, and where the colors come from
    assert "The AppImage runtime" in notices
    assert "vcruntime140.dll" in notices
    assert "Solarized" in notices and "Monokai" in notices
    assert "The extensions that ship with KubeScope" in notices
    assert "PyInstaller" in notices
    assert "\n\n\n\n" not in notices  # a section with no text leaves no gap
