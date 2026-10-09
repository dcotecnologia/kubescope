import faulthandler
import logging
import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

import kubescope
from kubescope.i18n import apply_language
from kubescope.settings import Settings
from kubescope.theme import apply_light_theme
from kubescope.window import WorkloadWindow

# __file__ of the entry script points at the bundle root once frozen, so anchor
# on the package instead
ICON_PATH = Path(kubescope.__file__).resolve().parent / "assets" / "icon.png"
ICON_SIZES = (16, 24, 32, 48, 64, 128, 256, 512)


def load_app_icon() -> QIcon:
    """Several sizes, so taskbars and docks never have to scale one huge
    image."""
    source = QPixmap(str(ICON_PATH))
    icon = QIcon()
    for size in ICON_SIZES:
        icon.addPixmap(
            source.scaled(
                size,
                size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    return icon


DEBUG_ENV = "KUBESCOPE_DEBUG"


def configure_debug() -> bool:
    """With KUBESCOPE_DEBUG=1, log at DEBUG level to stderr (never to disk) and
    dump the traceback if the process crashes."""
    if os.environ.get(DEBUG_ENV) != "1":
        return False
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    faulthandler.enable()
    return True


def main() -> int:
    configure_debug()
    application = QApplication(sys.argv)
    application.setApplicationName("KubeScope")
    application.setWindowIcon(load_app_icon())
    apply_light_theme(application)
    settings = Settings()
    apply_language(settings.language)
    window = WorkloadWindow(settings)
    window.show()
    return application.exec()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
