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

The manifest here packages the PyInstaller bundle and the AWS CLI already built.
Flathub builds from public sources, so both commands list what has to change before
the pull request can be accepted.
Commit messages follow
[COMMITING.md](https://github.com/dcotecnologia/kubescope/blob/main/COMMITING.md).
