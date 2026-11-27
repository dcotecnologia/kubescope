from tools import build_rpm


def test_the_spec_names_the_version_the_summary_and_the_libraries_it_needs() -> None:
    spec = build_rpm.spec_text("1.3.0", "A desktop IDE", "x86_64")

    assert "Version:        1.3.0\n" in spec
    assert "Summary:        A desktop IDE\n" in spec
    assert "ExclusiveArch:  x86_64\n" in spec
    assert "Requires:       mesa-libEGL\n" in spec
    assert "Recommends:     dejavu-sans-fonts\n" in spec


def test_the_spec_leaves_the_bundle_as_it_is() -> None:
    spec = build_rpm.spec_text("1.3.0", "A desktop IDE", "x86_64")

    assert "AutoReqProv: no" in spec  # the bundle carries its own libraries
    assert "%global __strip /bin/true" in spec
    assert "/opt/kubescope\n" in spec


def test_a_release_candidate_is_ordered_before_its_release_by_rpm() -> None:
    spec = build_rpm.spec_text("1.3.0rc1", "A desktop IDE", "x86_64")

    assert "Version:        1.3.0~rc1\n" in spec
