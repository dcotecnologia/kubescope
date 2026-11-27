---
layout: page
title: Building from source
permalink: /guides/building-from-source/
---

The full workflow lives in the repository:
the [contributing guide]({{ '/guides/contributing/' | relative_url }})
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
| Python 3.15 | `uv` fetches it for you; CI, the releases and the pre-commit hooks all use it (`uv python install 3.15`) |
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
| `make rpm` | `rpmbuild`, from the `rpm` package |
| `make arch` | `zstd`; it needs no `makepkg`, so it builds on any Linux |
| `make appimage` | nothing: `appimagetool` is downloaded and checked, and it runs without FUSE (Linux x86_64 only) |
| `make windows-remote` | the [GitHub CLI](https://cli.github.com) (`gh auth login`); the Windows packages are built only by the Release workflow, which this runs and downloads |
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
make rpm        # Fedora
make arch       # Arch Linux
make appimage   # any Linux
make windows-remote   # installer and zip, built by the Release workflow on GitHub
```

All packages use the bundle in `dist/KubeScope`, so build one platform at a time.

Commit messages follow
the [commit guidelines]({{ '/guides/commit-guidelines/' | relative_url }}).
