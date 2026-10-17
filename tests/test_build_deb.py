import gzip

from tools import build_deb, sync_changelog


def test_the_deb_carries_the_changelog_where_debian_looks_for_it() -> None:
    packed = build_deb.changelog_gz()

    assert gzip.decompress(packed) == sync_changelog.SOURCE.read_bytes()
    assert build_deb.changelog_gz() == packed  # the same bytes every time
