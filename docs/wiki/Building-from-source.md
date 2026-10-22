# Building from source

The full workflow lives in the repository:
[CONTRIBUTING.md](https://github.com/dcotecnologia/kubescope/blob/main/CONTRIBUTING.md)
and [README.md](https://github.com/dcotecnologia/kubescope/blob/main/README.md).
The short version:

```bash
git clone https://github.com/dcotecnologia/kubescope.git
cd kubescope
make setup                       # install dependencies with uv and the pre-commit hook
make run                         # start the app
make preview                     # start it with fake data, no cluster needed
```

## What you need installed

Everything else comes from `uv`, from the first `make` and from the hooks, so the
list is short.

### To work on the app

| Tool | Why |
| ---- | --- |
| `git` | the source and the pre-commit hooks |
| `make` | the commands above |
| [`uv`](https://docs.astral.sh/uv/) | it makes the virtual environment, installs the dependencies and finds Python |
| Python 3.12 or newer | `uv` fetches it for you; CI tests 3.12 to 3.15, releases are built with 3.15, and the pre-commit hooks are set to 3.12 (`uv python install 3.12`) |
| A network connection | the first `make setup`, and `uv run pre-commit run` download things; pre-commit installs its own Go and Node for `gitleaks` and `markdownlint` |
| `libxcb-cursor.so.0` on Linux | Qt needs it to open a window. On Debian and Ubuntu `make run` fetches it for you with `apt-get download libxcb-cursor0`; on other distributions install the package that provides it |

PySide6 (with `pyside6-uic`, `pyside6-lupdate` and `pyside6-lrelease`), `pytest`,
`ruff`, `pre-commit` and `pyinstaller` are installed by `make setup` in `.venv`; do
not install them yourself. The tests and the screenshots run without a display, with
`QT_QPA_PLATFORM=offscreen`. You do not need `kubectl` or a cluster: `make preview` uses fake
data.

### Only for some tasks

| To do this | Install |
| ---------- | ------- |
| Try it on a real cluster | a kubeconfig; for EKS, the AWS CLI and a profile that can sign in |
| `make deb` | `dpkg-deb`, from the `dpkg` package |
| `make appimage` | nothing: `appimagetool` is downloaded and checked, and it runs without FUSE (Linux x86_64 only) |
| `make flatpak` | `flatpak` and `flatpak-builder`, with the runtimes `org.kde.Platform//6.11`, `org.kde.Sdk//6.11` and `io.qt.PySide.BaseApp//6.11` (`flatpak install flathub ...`) |
| `make flatpak-lint` | `appstreamcli` (package `appstream`), `desktop-file-validate` (package `desktop-file-utils`) and `flatpak install flathub org.flatpak.Builder` for the Flathub linter |
| `make windows` on Linux | Wine (`sudo apt install wine64`); Python and Inno Setup are downloaded into `.wine/` |
| `make windows` on Windows | Inno Setup with `iscc` on the `PATH` |
| `make windows-remote` | the [GitHub CLI](https://cli.github.com) (`gh auth login`) |
| `make designer` | nothing more: Qt Designer comes with PySide6 |
| Edit translations | any text editor, or Qt Linguist (`pyside6-linguist` in `.venv`) |
| The install script tests | `curl`; `wget` and PowerShell (`pwsh`) are optional, and their tests are skipped without them. To lint the script: `uvx --from shellcheck-py shellcheck install.sh` |

`make help` lists every command.

## Checks

```bash
make lint     # every pre-commit hook on all files
make test
```

## Packages

```bash
make build      # PyInstaller bundle in dist/KubeScope
make deb        # Debian and Ubuntu
make appimage   # any Linux
make flatpak    # builds from source; needs flatpak-builder and its runtimes
make windows    # installer and zip; on Linux it builds inside Wine
```

All packages use the bundle in `dist/KubeScope`, so build one platform at a time.

## Flathub

Flathub has no deploy command: an app is added by a pull request to
[flathub/flathub](https://github.com/flathub/flathub), reviewers read it, and Flathub
builds it. Two commands prepare that, and neither sends anything:

```bash
make flatpak-lint         # validate the metainfo, the desktop file and the manifest
make flathub-submission   # gather the files in dist/flathub/ and print the steps
```

`make flatpak-lint` runs `appstreamcli` and `desktop-file-validate`, and
`flatpak-builder-lint` (what Flathub runs) when it is installed:
`flatpak install flathub org.flatpak.Builder`.

The manifest builds everything from public sources, as Flathub requires: the app
from its git tag, PySide6 from the `io.qt.PySide.BaseApp` base app, the Kubernetes
client (`python3-kubernetes.json`, made by `python tools/flatpak_python_deps.py`
from `uv.lock`) and the AWS CLI v1 from PyPI. `make flatpak`
builds it with the app taken from your working tree instead of the tag, so a change
that is not committed can be tried; it needs the runtimes, installed with
`flatpak install flathub org.kde.Platform//6.11 org.kde.Sdk//6.11
io.qt.PySide.BaseApp//6.11`.

To move to a new release, change the `tag` and `commit` of the `kubescope` module,
regenerate `python3-kubernetes.json` if `uv.lock` changed, and run `make flatpak-lint`, which
checks that the tag exists and points at that commit.
Commit messages follow
[COMMITING.md](https://github.com/dcotecnologia/kubescope/blob/main/COMMITING.md).
