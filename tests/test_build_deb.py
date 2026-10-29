import gzip

from tools import build_deb, sync_changelog


def test_the_deb_carries_the_changelog_where_debian_looks_for_it() -> None:
    packed = build_deb.changelog_gz()

    assert gzip.decompress(packed) == sync_changelog.SOURCE.read_bytes()
    assert build_deb.changelog_gz() == packed  # the same bytes every time


def test_a_release_candidate_is_ordered_before_its_release_by_debian() -> None:
    from tools import build_deb

    assert build_deb.debian_version("1.3.0rc1") == "1.3.0~rc1"
    assert build_deb.debian_version("1.3.0a2") == "1.3.0~a2"
    assert build_deb.debian_version("1.3.0b10") == "1.3.0~b10"
    assert build_deb.debian_version("1.3.0") == "1.3.0"
