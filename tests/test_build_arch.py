import tarfile

from tools import build_arch


def test_the_pkginfo_names_the_package_its_version_and_its_dependencies() -> None:
    text = build_arch.pkginfo("1.3.0", "A desktop IDE", "x86_64", 2048, 1700000000)

    assert "pkgname = kubescope\n" in text
    assert "pkgver = 1.3.0-1\n" in text
    assert "arch = x86_64\n" in text
    assert "size = 2048\n" in text
    assert "builddate = 1700000000\n" in text
    assert "depend = libglvnd\n" in text
    assert "optdepend = ttf-dejavu: the default font\n" in text


def test_the_files_of_the_package_belong_to_root() -> None:
    info = build_arch._owned_by_root(tarfile.TarInfo("usr/bin/kubescope"))

    assert (info.uid, info.gid, info.uname, info.gname) == (0, 0, "root", "root")
