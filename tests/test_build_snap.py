import re
import subprocess
from pathlib import Path

import pytest

from tools import build_snap, sync_changelog


def _bundle(tmp_path: Path) -> Path:
    bundle = tmp_path / "dist" / "KubeScope"
    (bundle / "_internal").mkdir(parents=True)
    (bundle / "KubeScope").write_text("#!/bin/sh\n", encoding="utf-8")
    (bundle / "_internal" / "libqt.so.6").write_text("lib", encoding="utf-8")
    (bundle / "_internal" / "libqt.so").symlink_to("libqt.so.6")
    return bundle


@pytest.fixture
def workdir(monkeypatch, tmp_path: Path) -> Path:
    monkeypatch.setattr(build_snap, "BUNDLE", _bundle(tmp_path))
    monkeypatch.setattr(build_snap, "STAGING", tmp_path / "build" / "snap")
    monkeypatch.setattr(sync_changelog, "check_bundle", lambda bundle: None)
    return tmp_path


def test_the_manifest_gets_the_version_of_the_app() -> None:
    text = build_snap.render_snapcraft("1.2.3")

    assert 'version: "1.2.3"' in text
    assert not build_snap.PLACEHOLDER.search(text)


def test_the_snap_is_classic_so_it_runs_the_tools_of_every_cloud() -> None:
    text = (build_snap.PACKAGING / "snapcraft.yaml").read_text(encoding="utf-8")

    assert "confinement: classic" in text
    # the PyInstaller bootloader breaks when its ELF is patched for the snap
    assert "no-patchelf" in text
    assert "personal-files" not in text  # nothing to ask the store for but classic


def test_a_manifest_with_an_unfilled_value_is_refused(monkeypatch, tmp_path) -> None:
    (tmp_path / "snapcraft.yaml").write_text("version: @SOMETHING_NEW@\n")
    monkeypatch.setattr(build_snap, "PACKAGING", tmp_path)

    with pytest.raises(SystemExit, match="@SOMETHING_NEW@"):
        build_snap.render_snapcraft("1.0.0")


def test_staging_lays_out_the_bundle_and_the_store_files(workdir) -> None:
    staging = build_snap.stage("1.2.3")

    assert (staging / "bundle" / "KubeScope").is_file()
    assert (staging / "bundle" / "_internal" / "libqt.so").is_symlink()
    assert (staging / "snap" / "gui" / "dco-kubescope.desktop").is_file()
    assert (staging / "snap" / "gui" / "dco-kubescope.png").is_file()
    assert 'version: "1.2.3"' in (staging / "snap" / "snapcraft.yaml").read_text()


def test_staging_starts_from_nothing(workdir) -> None:
    left_over = build_snap.STAGING / "bundle" / "old.txt"
    left_over.parent.mkdir(parents=True)
    left_over.write_text("old")

    build_snap.stage("1.2.3")

    assert not left_over.exists()


def test_the_snap_has_the_name_the_store_was_asked_for() -> None:
    text = (build_snap.PACKAGING / "snapcraft.yaml").read_text(encoding="utf-8")

    assert re.search(rf"^name: {build_snap.SNAP_NAME}$", text, re.MULTILINE)
    assert build_snap.SNAP_NAME != "kubescope"  # reserved by the store


def test_the_desktop_file_names_the_app_of_the_manifest() -> None:
    desktop = (build_snap.PACKAGING / "dco-kubescope.desktop").read_text(
        encoding="utf-8"
    )
    manifest = (build_snap.PACKAGING / "snapcraft.yaml").read_text(encoding="utf-8")

    assert "Exec=dco-kubescope\n" in desktop
    assert re.search(r"^apps:\n  dco-kubescope:\n", manifest, re.MULTILINE)


def test_packing_runs_snapcraft_on_the_staged_folder(
    workdir, monkeypatch, capsys
) -> None:
    calls = []
    monkeypatch.setattr(build_snap, "ROOT", workdir)
    monkeypatch.setattr(build_snap.shutil, "which", lambda name: "/usr/bin/snapcraft")
    monkeypatch.setattr(
        build_snap.subprocess,
        "run",
        lambda command, **kwargs: (
            calls.append((command, kwargs["cwd"])),
            (workdir / "dist" / "dco-kubescope_9.9.9_amd64.snap").write_bytes(b"snap"),
            subprocess.CompletedProcess(command, 0),
        )[-1],
    )
    monkeypatch.setattr(build_snap, "project_version", lambda: "9.9.9")
    monkeypatch.setenv("SNAPCRAFT_BUILD_ARGS", "--destructive-mode")

    assert build_snap.main([]) == 0

    command, cwd = calls[0]
    assert command[:2] == ["snapcraft", "pack"]
    assert command[-1] == "--destructive-mode"
    assert command[command.index("--output") + 1] == str(
        workdir / "dist" / "dco-kubescope_9.9.9_amd64.snap"
    )
    assert cwd == build_snap.STAGING
    assert "Created" in capsys.readouterr().out


def test_staging_only_does_not_need_snapcraft(workdir, monkeypatch, capsys) -> None:
    monkeypatch.setattr(build_snap.shutil, "which", lambda name: None)
    monkeypatch.setattr(
        build_snap.subprocess,
        "run",
        lambda *a, **k: pytest.fail("snapcraft must not run"),
    )

    assert build_snap.main(["--stage"]) == 0

    assert "Staged" in capsys.readouterr().out
    assert (build_snap.STAGING / "snap" / "snapcraft.yaml").is_file()


def test_packing_without_snapcraft_says_how_to_get_it(workdir, monkeypatch) -> None:
    monkeypatch.setattr(build_snap.shutil, "which", lambda name: None)

    with pytest.raises(SystemExit, match="snap install snapcraft"):
        build_snap.main([])


def test_packing_without_a_bundle_says_to_build_it_first(
    workdir, monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr(build_snap, "BUNDLE", tmp_path / "nothing")

    with pytest.raises(SystemExit, match="make build"):
        build_snap.main([])


def test_a_snap_is_only_built_on_linux(monkeypatch) -> None:
    monkeypatch.setattr(build_snap.sys, "platform", "win32")

    with pytest.raises(SystemExit, match="only be built on Linux"):
        build_snap.main([])


def test_the_version_comes_from_pyproject() -> None:
    assert re.fullmatch(r"\d+\.\d+\.\d+((a|b|rc)\d+)?", build_snap.project_version())


def test_a_pre_release_is_a_devel_snap_and_a_release_is_stable() -> None:
    assert "grade: devel" in build_snap.render_snapcraft("1.3.0rc1")
    assert "grade: devel" in build_snap.render_snapcraft("1.3.0a1")
    stable = build_snap.render_snapcraft("1.3.0")
    assert "grade: stable" in stable and "grade: devel" not in stable
