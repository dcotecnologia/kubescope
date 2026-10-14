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
