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
from its git tag, PySide6 from the `io.qt.PySide.BaseApp` base app, `kubectl` from the
Kubernetes source release with Go, and the AWS CLI v1 from PyPI. `make flatpak`
builds it with the app taken from your working tree instead of the tag, so a change
that is not committed can be tried; it needs the runtimes, installed with
`flatpak install flathub org.kde.Platform//6.11 org.kde.Sdk//6.11
io.qt.PySide.BaseApp//6.11 org.freedesktop.Sdk.Extension.golang//25.08`.

To move to a new release, change the `tag` and `commit` of the `kubescope` module,
the version of `kubectl` if you want it newer, and run `make flatpak-lint`, which
checks that the tag exists and points at that commit.
Commit messages follow
[COMMITING.md](https://github.com/dcotecnologia/kubescope/blob/main/COMMITING.md).
