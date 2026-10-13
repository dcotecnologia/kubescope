import logging
import os
import sys
import threading
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

import kubescope
from kubescope.diagnostics import (
    CRASH_FILE,
    LOG_FILE,
    configure_logging,
    purge_old_logs,
)
from kubescope.fonts import apply_fonts
from kubescope.i18n import apply_language, install_bundled_languages
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


def start_log_purge(settings: Settings) -> threading.Thread:
    """Delete old logs on a thread of its own, so starting never waits for the
    disk; the files being written now are left alone."""
    keep = (LOG_FILE, CRASH_FILE) if settings.debug_logging else ()
    thread = threading.Thread(
        target=purge_old_logs, kwargs={"keep": keep}, name="log-purge", daemon=True
    )
    thread.start()
    return thread


def main() -> int:
    settings = Settings()
    configure_debug(settings)
    start_log_purge(settings)
    logger.info("Starting KubeScope")
    application = QApplication(sys.argv)
    application.setApplicationName("KubeScope")
    application.setWindowIcon(load_app_icon())
    apply_fonts(application)
    install_community_themes()
    apply_theme(application, settings.theme)
    install_bundled_languages()
    apply_language(settings.language)
    window = WorkloadWindow(settings)
    window.show()
    window.start_update_check()
    exit_code = application.exec()
    logger.info("KubeScope stopped (exit code %s)", exit_code)
    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
