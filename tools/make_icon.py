"""Build assets/icon.ico (used by the Windows .exe) from assets/icon.png."""

import struct
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PySide6.QtGui import QImage

ASSETS = Path(__file__).resolve().parents[1] / "src" / "kubescope" / "assets"
SIZES = (16, 24, 32, 48, 64, 128, 256)


def png_bytes(image: QImage) -> bytes:
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    return bytes(data)


def main() -> int:
    source = QImage(str(ASSETS / "icon.png"))
    entries = []
    for size in SIZES:
        scaled = source.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        entries.append((size, png_bytes(scaled)))

    header = struct.pack("<HHH", 0, 1, len(entries))
    offset = len(header) + 16 * len(entries)
    directory = b""
    for size, data in entries:
        # a stored size of 0 means 256 in the ICO format
        directory += struct.pack(
            "<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(data), offset
        )
        offset += len(data)
    (ASSETS / "icon.ico").write_bytes(
        header + directory + b"".join(data for _, data in entries)
    )
    print(f"Wrote {ASSETS / 'icon.ico'} with sizes {SIZES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
