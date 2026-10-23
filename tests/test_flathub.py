from tools import flathub


def test_the_manifest_lets_the_app_run_the_sign_in_tools_of_the_host() -> None:
    manifest = (flathub.ROOT / "packaging" / "flatpak" / flathub.MANIFEST).read_text(
        encoding="utf-8"
    )

    assert "--talk-name=org.freedesktop.Flatpak" in manifest


def test_flathub_is_warned_about_the_permission_to_run_programs_on_the_host() -> None:
    manifest = (flathub.ROOT / "packaging" / "flatpak" / flathub.MANIFEST).read_text(
        encoding="utf-8"
    )

    assert any("flatpak-spawn --host" in found for found in flathub.blockers(manifest))
    assert not any(
        "flatpak-spawn" in found for found in flathub.blockers("finish-args: []")
    )
