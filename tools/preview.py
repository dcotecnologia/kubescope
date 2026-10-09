"""Open KubeScope with fake cluster data to review the UI without a cluster.

python tools/preview.py            # interactive window, every button works;
                                   # saving any .ui regenerates and reopens it
python tools/preview.py out.png    # render the main window to a PNG and exit
"""

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# The preview must never read or overwrite the real user settings.
os.environ.setdefault(
    "KUBESCOPE_CONFIG_DIR", tempfile.mkdtemp(prefix="kubescope-preview-")
)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from PySide6.QtCore import QFileSystemWatcher  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from kubescope import window  # noqa: E402
from kubescope.models import ClusterOverview, NodeInfo, PodInfo, Workload  # noqa: E402
from kubescope.theme import apply_light_theme  # noqa: E402

WORKLOADS = [
    Workload("default", "Deployment", "api", 3, 3, "12d"),
    Workload("default", "Deployment", "worker", 1, 2, "12d"),
    Workload("default", "StatefulSet", "postgres", 0, 1, "40d"),
    Workload("monitoring", "DaemonSet", "node-exporter", 4, 4, "90d"),
    Workload("monitoring", "Deployment", "grafana", 0, 0, "90d"),
    Workload("kube-system", "Deployment", "coredns", 2, 2, "120d"),
]


def fake_pods(_context: str, workload: Workload) -> list[PodInfo]:
    return [
        PodInfo(
            workload.namespace,
            f"{workload.name}-{suffix}",
            "Running" if index < workload.ready else "Pending",
            1 if index < workload.ready else 0,
            2,
            "3d",
            ("app", "sidecar"),
        )
        for index, suffix in enumerate(("5f7d9c-abcde", "5f7d9c-fghij"))
    ]


def fake_overview(_context: str) -> ClusterOverview:
    def node(name: str, ready: bool, cpu: float, memory_gib: float, pods: int):
        return NodeInfo(
            name=name,
            ready=ready,
            roles="—",
            version="v1.30.4-eks",
            age="42d",
            cpu_allocatable=3.92,
            memory_allocatable=7 * 2**30,
            pods_allocatable=58,
            pods_running=pods,
            cpu_requests=cpu,
            memory_requests=memory_gib * 2**30,
            cpu_usage=cpu * 0.6,
            memory_usage=memory_gib * 0.8 * 2**30,
        )

    return ClusterOverview(
        nodes=(
            node("ip-10-0-1-12.ec2.internal", True, 3.6, 5.8, 41),
            node("ip-10-0-2-87.ec2.internal", True, 2.1, 3.2, 28),
            node("ip-10-0-3-45.ec2.internal", False, 0.4, 0.9, 6),
        ),
        namespaces=6,
        deployments=18,
        statefulsets=2,
        daemonsets=4,
        pods_total=80,
        pods_running=75,
        pods_pending=3,
        pods_failed=2,
        metrics_available=True,
    )


window.get_cluster_overview = fake_overview
window.list_contexts = lambda: (["prod-eks", "staging-eks"], "prod-eks")
window.get_workloads = lambda _context, namespace=None: (
    sorted({item.namespace for item in WORKLOADS}),
    [item for item in WORKLOADS if namespace in (None, item.namespace)],
)
window.get_usage = lambda _context, namespace=None: {
    (item.namespace, item.kind, item.name): (
        index % 3,
        0.05 + index * 0.4,
        (index + 1) * 96 * 2**20,
    )
    for index, item in enumerate(WORKLOADS)
}
window.get_workload_pods = fake_pods
window.get_resource_details = lambda _c, kind, namespace, name: {
    "kind": kind,
    "metadata": {"name": name, "namespace": namespace},
    "spec": {"replicas": 3},
}
window.get_pod_logs = lambda *_args, **_kwargs: (
    "2026-10-08T05:00:01Z INFO server started\n2026-10-08T05:00:02Z WARN slow query"
)


UI_DIR = Path(__file__).resolve().parent.parent / "src/kubescope/ui"


def watch_ui(main_window: window.WorkloadWindow) -> QFileSystemWatcher:
    """Regenerate the ui_*.py and restart the preview when a .ui file is saved."""
    files = [str(path) for path in UI_DIR.glob("*.ui")]
    watcher = QFileSystemWatcher(files, main_window)
    uic = Path(sys.executable).parent / "pyside6-uic"

    def changed(path: str) -> None:
        source = Path(path)
        target = source.with_name(f"ui_{source.stem}.py")
        result = subprocess.run([str(uic), str(source), "-o", str(target)], check=False)
        if result.returncode == 0:
            os.execv(sys.executable, [sys.executable, *sys.argv])

    watcher.fileChanged.connect(changed)
    return watcher


def wait_until_idle(application: QApplication, main_window) -> None:
    """Let the fake workers finish and deliver their results to the window."""
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        application.processEvents()
        workers = [main_window._worker, *main_window._action_workers]
        if not any(worker is not None and worker.isRunning() for worker in workers):
            break
        time.sleep(0.05)
    for _ in range(5):
        application.processEvents()


def main() -> int:
    application = QApplication(sys.argv[:1])
    apply_light_theme(application)
    main_window = window.WorkloadWindow()
    main_window.resize(1280, 800)
    main_window.show()
    if len(sys.argv) > 1:
        page = sys.argv[2] if len(sys.argv) > 2 else "overview"
        wait_until_idle(application, main_window)
        if page in ("workloads", "deployments"):
            main_window.nav_deployments.click()
            wait_until_idle(application, main_window)
        main_window.grab().save(sys.argv[1])
        return 0
    watch_ui(main_window)
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
