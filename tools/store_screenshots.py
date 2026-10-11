"""Render the screenshots used by the app stores (Flathub, the Microsoft Store,
the Ubuntu store) and the README, from the preview's fake data.

Every theme gets the overview and the Deployments list; the dark theme
also gets the details of a resource and a log. They are 1600x900 (16:9)
PNGs in docs/screenshots/store/. Run it with `make store-screenshots`.
"""

import sys
import time
from pathlib import Path

import preview  # the fake cluster data, and a throwaway settings folder
from PySide6.QtWidgets import QApplication

from kubescope import window
from kubescope.fonts import apply_fonts
from kubescope.models import PodInfo
from kubescope.theme import apply_theme, install_community_themes

OUTPUT = Path(__file__).resolve().parent.parent / "docs" / "screenshots" / "store"
THEMES = ("dark", "light", "midnight", "sepia", "high-contrast")
SIZE = (1600, 900)
DETAILS = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "api", "namespace": "default", "generation": 3},
    "spec": {
        "replicas": 3,
        "paused": False,
        "selector": {"matchLabels": {"app": "api"}},
        "template": {
            "spec": {
                "containers": [
                    {
                        "name": "api",
                        "image": "registry.example/api:1.25",
                        "resources": {"limits": {"cpu": "500m", "memory": "256Mi"}},
                    }
                ]
            }
        },
    },
    "status": {"readyReplicas": 3, "conditions": [{"type": "Available"}]},
}
LOGS = """2026-10-08T05:00:01.120Z INFO  server started on :8080
2026-10-08T05:00:02.331Z DEBUG loaded 14 routes
2026-10-08T05:00:03.004Z WARN  slow query took 2.4s
2026-10-08T05:00:04.870Z ERROR connection to db lost: timeout
2026-10-08T05:00:05.100Z ts=1728363605 level=info msg="request done" status=200
2026-10-08T05:00:06.500Z {"level":"error","msg":"upstream failed","code":502}
2026-10-08T05:00:07.250Z [warn] disk almost full"""
POD = PodInfo("default", "api-5f7d9c-abcde", "Running", 1, 1, "12d", ("api",))


def settle(application: QApplication, seconds: float = 0.4) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.02)


def shoot(application: QApplication, theme: str, page: str) -> Path:
    apply_theme(application, theme)
    main_window = window.WorkloadWindow()
    main_window.resize(*SIZE)
    main_window.show()
    preview.wait_until_idle(application, main_window)
    preview.open_menus(application, main_window)
    if page == "deployments":
        main_window.nav_deployments.click()
        preview.wait_until_idle(application, main_window)
    elif page == "details":
        main_window._show_json_dialog("Deployment: api", DETAILS)
    elif page == "logs":
        main_window._show_logs_dialog(POD, "api", LOGS)
    settle(application)
    path = OUTPUT / f"{page}-{theme}.png"
    main_window.grab().save(str(path))
    main_window.close()
    return path


def main() -> int:
    application = QApplication(sys.argv[:1])
    apply_fonts(application)
    install_community_themes()  # midnight, sepia and high contrast ship with the app
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        pages = ["overview", "deployments"]
        if theme == "dark":
            pages += ["details", "logs"]
        for page in pages:
            print(shoot(application, theme, page).relative_to(OUTPUT.parent.parent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
