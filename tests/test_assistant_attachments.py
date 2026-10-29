import pytest

from kubescope.assistant import attachments
from kubescope.assistant.attachments import Attachment, AttachmentError

PNG = b"\x89PNG\r\n\x1a\nrest"


def test_an_image_is_read_with_its_type(tmp_path) -> None:
    path = tmp_path / "Shot.PNG"
    path.write_bytes(PNG)

    item = attachments.load(path)

    assert item == Attachment("Shot.PNG", "image", PNG, "image/png")
    assert item.base64 == "iVBORw0KGgpyZXN0"


def test_a_text_file_is_read_and_redacted(tmp_path) -> None:
    path = tmp_path / "app.log"
    path.write_text("ok\nAuthorization: Bearer abcdefghijklmnop\n", encoding="utf-8")

    item = attachments.load(path)

    assert item.kind == "text" and "ok" in item.text
    assert "abcdefghijklmnop" not in item.text


def test_the_text_files_become_a_block_after_the_question_and_images_are_apart(
    tmp_path,
) -> None:
    (tmp_path / "a.yaml").write_text("kind: Pod\n", encoding="utf-8")
    (tmp_path / "b.png").write_bytes(PNG)
    items = (
        attachments.load(tmp_path / "a.yaml"),
        attachments.load(tmp_path / "b.png"),
    )

    assert (
        attachments.text_block(items) == "Attached file a.yaml:\n```\nkind: Pod\n\n```"
    )
    assert [item.name for item in attachments.images(items)] == ["b.png"]
    assert attachments.text_block(()) == ""


@pytest.mark.parametrize(
    ("name", "data", "reason"),
    [
        ("tool.exe", b"MZ", "not an image or a text file"),
        ("binary.txt", b"a\x00b", "is not text"),
    ],
)
def test_what_is_not_an_image_or_text_is_refused(tmp_path, name, data, reason) -> None:
    path = tmp_path / name
    path.write_bytes(data)

    with pytest.raises(AttachmentError, match=reason):
        attachments.load(path)


def test_a_file_that_is_too_large_or_missing_is_refused(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(attachments, "MAX_IMAGE_BYTES", 4)
    monkeypatch.setattr(attachments, "MAX_TEXT_BYTES", 4)
    (tmp_path / "big.png").write_bytes(PNG)
    (tmp_path / "big.log").write_text("too long", encoding="utf-8")

    with pytest.raises(AttachmentError, match="big.png is larger"):
        attachments.load(tmp_path / "big.png")
    with pytest.raises(AttachmentError, match="big.log is larger"):
        attachments.load(tmp_path / "big.log")
    with pytest.raises(AttachmentError, match="gone.log cannot be read"):
        attachments.load(tmp_path / "gone.log")
