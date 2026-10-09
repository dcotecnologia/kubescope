# Building from source

The full workflow lives in the repository:
[CONTRIBUTING.md](https://github.com/dcotecnologia/kubescope/blob/main/CONTRIBUTING.md)
and [README.md](https://github.com/dcotecnologia/kubescope/blob/main/README.md).
The short version:

```bash
git clone https://github.com/dcotecnologia/kubescope.git
cd kubescope
make setup                       # install dependencies with uv
uv run pre-commit install        # run the checks on every commit
python tools/fetch_kubectl.py    # download the verified kubectl
make run                         # start the app
make preview                     # start it with fake data, no cluster needed
```

## Checks

```bash
make lint
make test
uv run pre-commit run --all-files
```

## Packages

```bash
make build      # PyInstaller bundle in dist/KubeScope
make deb        # Debian and Ubuntu
make appimage   # any Linux
make flatpak    # needs flatpak-builder
make windows    # installer and zip; on Linux it builds inside Wine
```

All packages use the bundle in `dist/KubeScope`, so build one platform at a time.
Commit messages follow
[COMMITING.md](https://github.com/dcotecnologia/kubescope/blob/main/COMMITING.md).
