# KubeScope

[![CI](https://github.com/dcotecnologia/kubescope/actions/workflows/ci.yml/badge.svg)](https://github.com/dcotecnologia/kubescope/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB.svg?logo=python&logoColor=white)](pyproject.toml)
[![Qt for Python](https://img.shields.io/badge/Qt-PySide6-41CD52.svg?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20Windows-lightgrey.svg)](#packaging)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS%20ready-326CE5.svg?logo=kubernetes&logoColor=white)](https://kubernetes.io/)

Desktop viewer for Kubernetes workloads, including Amazon EKS clusters available
through the local Kubernetes configuration. The packaged application includes
its own `kubectl` executable.

## Requirements

- Python 3.12 or newer to run from source
- Linux Mint/Ubuntu: `apt-get` and `dpkg-deb` to stage the Qt XCB runtime library
- AWS CLI and valid AWS credentials for EKS contexts whose kubeconfig uses the
  AWS `exec` credential plugin
- Read access to namespaces, deployments, statefulsets, and daemonsets
- Optional, for the cluster overview page: read access to nodes and pods across
  namespaces, and `metrics-server` for real CPU/memory usage. Sections the role
  cannot read are reported on the page instead of failing it

## Run from source

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python tools/fetch_kubectl.py
make run
```

`make run` stages `libxcb-cursor.so.0` locally on Linux and adds it to the
runtime library path. This avoids installing `libxcb-cursor0` system-wide. On
non-Linux systems, the target starts the app without the Linux-specific library.

The app reads contexts from the default kubeconfig (`~/.kube/config` or the path
in `KUBECONFIG`). It only reads cluster resources. Configure a read-only
Kubernetes role for the contexts used by the app.

## Build a bundled application

Build on each target operating system and architecture. The fetch script obtains
the official stable `kubectl` release and verifies its published SHA-256 before
PyInstaller includes it in the application bundle.

```bash
python -m pip install -e '.[build]'
python tools/fetch_kubectl.py
python tools/fetch_linux_qt_libs.py  # Linux only
pyinstaller --noconfirm KubeScope.spec
```

The distributable application is created under `dist/KubeScope/`.

## Settings and language

The **Settings** page (sidebar) stores preferences as JSON in
`~/.config/kubescope/settings.json` (`%APPDATA%\\kubescope` on Windows,
`~/Library/Application Support/kubescope` on macOS; override with
`KUBESCOPE_CONFIG_DIR`). It lets you pick the language (automatic, English or
Portuguese), remember the last context, and give each kubeconfig context a
friendlier display name. The real context name is still used for every request.

Source strings are English; translations live in
`src/kubescope/translations/*.ts` (editable in Qt Linguist). After adding or
changing texts run `make i18n` to extract new strings and compile the `.qm` files.

## Packaging

```bash
make build      # PyInstaller bundle in dist/KubeScope
make deb        # dist/kubescope_<version>_amd64.deb (Debian/Ubuntu)
make appimage   # dist/KubeScope-<version>-x86_64.AppImage (any Linux with glibc)
```

Windows packages cannot be cross-built. The **Release** workflow
(`.github/workflows/release.yml`) builds everything on GitHub runners: the Linux
`.deb` and AppImage on Ubuntu 22.04 (lower glibc requirement) and the Windows
installer plus a portable zip on Windows. Run it from the Actions tab, or push a
`v*` tag to also publish a GitHub release.

## Editing the UI

The screens are Qt Designer files in `src/kubescope/ui/`:

```bash
make designer   # open the .ui files in Qt Designer
make ui         # regenerate ui_*.py after saving (commit both)
make preview    # open the app with fake data, no cluster needed
```

Widget `objectName`s are used by the style sheet and by `window.py`, so keep
them when renaming or moving widgets.

## Author

Danilo Carolino <danilogcarolino@gmail.com>

---

Developed by **DCO Tecnologia** · Released under the [MIT License](LICENSE).
