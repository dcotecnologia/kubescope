# KubeScope

Desktop viewer for Kubernetes workloads, including Amazon EKS clusters available
through the local Kubernetes configuration. The packaged application includes
its own `kubectl` executable.

## Requirements

- Python 3.12 or newer to run from source
- Linux Mint/Ubuntu: `apt-get` and `dpkg-deb` to stage the Qt XCB runtime library
- AWS CLI and valid AWS credentials for EKS contexts whose kubeconfig uses the
  AWS `exec` credential plugin
- Read access to namespaces, deployments, statefulsets, and daemonsets

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

## Author

Danilo Carolino <danilogcarolino@gmail.com>

## License

[MIT](LICENSE)
