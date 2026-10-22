import logging
import os
import sys
import threading
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

import kubescope
from kubescope import cli
from kubescope.dialogs.crash_dialog import show_pending_crash_report
from kubescope.i18n import apply_language
from kubescope.settings import Settings
from kubescope.theme import apply_theme, install_bundled_themes
from kubescope.utils import crashreport
from kubescope.utils.diagnostics import (
    CRASH_FILE,
    LOG_FILE,
    configure_logging,
    purge_old_logs,
    record_runtime,
    trace_input,
)
from kubescope.utils.fonts import apply_fonts
from kubescope.utils.single_instance import SingleInstance
from kubescope.utils.wheel_guard import install_wheel_guard
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
APP_ID = "com.dcotecnologia.KubeScope"  # the same ID the installer gives its shortcuts


def set_app_user_model_id() -> None:
    """Tell Windows which application this process is, so the notice of a new
    version reaches the notification center and the taskbar groups the windows
    under the app's icon."""
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


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
    command = cli.run(sys.argv[1:])
    if command is not None:
        return command
    settings = Settings()
    debugging = configure_debug(settings)
    start_log_purge(settings)
    crashreport.install()
    logger.info("Starting KubeScope")
    set_app_user_model_id()
    application = QApplication(sys.argv)
    instance = SingleInstance()
    if instance.notify_running():
        logger.info("KubeScope is already running; it was asked to come forward")
        return 0
    instance.listen()
    install_wheel_guard(application)  # a select changes on click, not on hover
    application.setApplicationName("KubeScope")
    if debugging:
        record_runtime()
        trace_input(application)
    application.setWindowIcon(load_app_icon())
    apply_fonts(application)
    install_bundled_themes()
    apply_theme(application, settings.theme)
    apply_language(settings.language)
    window = WorkloadWindow(settings)
    instance.activated.connect(window.bring_to_front)
    window.show()
    window.start_update_check()
    show_pending_crash_report(window)
    window.show_welcome()
    exit_code = application.exec()
    logger.info("KubeScope stopped (exit code %s)", exit_code)
    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
