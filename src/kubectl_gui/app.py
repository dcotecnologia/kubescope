import sys

from PySide6.QtWidgets import QApplication

from kubectl_gui.window import WorkloadWindow


def main() -> int:
    application = QApplication(sys.argv)
    application.setApplicationName("KubeScope")
    application.setStyle("Fusion")
    window = WorkloadWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
