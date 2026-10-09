import logging
import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

import kubescope
from kubescope.diagnostics import configure_logging
from kubescope.i18n import apply_language
from kubescope.settings import Settings
from kubescope.theme import apply_theme, install_community_themes
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


logger = logging.getLogger(__name__)
DEBUG_ENV = "KUBESCOPE_DEBUG"


def configure_debug(settings: Settings) -> bool:
    """Set up logging: the Debug mode setting writes a log file; the
    KUBESCOPE_DEBUG=1 variable also prints DEBUG lines to the terminal."""
    console = os.environ.get(DEBUG_ENV) == "1"
    configure_logging(to_file=settings.debug_logging, to_console=console)
    return console or settings.debug_logging


def main() -> int:
    settings = Settings()
    configure_debug(settings)
    logger.info("Starting KubeScope")
    application = QApplication(sys.argv)
    application.setApplicationName("KubeScope")
    application.setWindowIcon(load_app_icon())
    install_community_themes()
    apply_theme(application, settings.theme)
    apply_language(settings.language)
    window = WorkloadWindow(settings)
    window.show()
    exit_code = application.exec()
    logger.info("KubeScope stopped (exit code %s)", exit_code)
    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
