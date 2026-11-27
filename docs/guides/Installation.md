---
layout: page
title: Installation
permalink: /guides/installation/
---

## The install script (recommended)

One command installs the latest release and, run again, updates it. It picks the
right package for your system and checks the download against the sha256 that GitHub
publishes for it before installing anything.

Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/dcotecnologia/kubescope/main/install.sh | sh
```

Windows (PowerShell, for your user, no administrator needed):

```powershell
irm https://raw.githubusercontent.com/dcotecnologia/kubescope/main/install.ps1 | iex
```

- **Linux:** it installs the `.deb` through `apt` on Debian and Ubuntu, the
  `.rpm` through `dnf` on Fedora and the package through `pacman` on Arch Linux (each asks
  for your password), and otherwise puts the AppImage in `~/.local/share/kubescope`
  and links it as `~/.local/bin/kubescope`. An update replaces the old file.
- **Windows:** it runs the installer silently for your user. An update installs over
  the old version.
- **Options:** save the script to pass them. `--dry-run` (`-DryRun`) shows what would
  happen, `--version 0.1.0` (`-Version 0.1.0`) picks a release, `--force` (`-Force`)
  reinstalls, and on Linux `--method deb`, `rpm`, `arch` or `appimage` picks the package.
- **Safety:** a script piped into a shell runs with your rights, so you can read
  [install.sh](https://github.com/dcotecnologia/kubescope/blob/main/install.sh) and
  [install.ps1](https://github.com/dcotecnologia/kubescope/blob/main/install.ps1)
  first. The sha256 check catches a damaged or swapped download; it trusts GitHub and
  the repository.
- **AppImage:** it needs FUSE 2 (`libfuse2`); if it will not start, install that.

## Install by hand

Download the package for your system from the
[releases page]({{ '/install/' | relative_url }}). You do
not need `kubectl`.

## Debian and Ubuntu (.deb)

```bash
sudo apt install ./kubescope_<version>_amd64.deb
kubescope
```

## Fedora (.rpm)

```bash
sudo dnf install ./kubescope-<version>-1.x86_64.rpm
kubescope
```

## Arch Linux

```bash
sudo pacman -U kubescope-<version>-1-x86_64.pkg.tar.zst
kubescope
```

## Any Linux (AppImage)

```bash
chmod +x KubeScope-<version>-x86_64.AppImage
./KubeScope-<version>-x86_64.AppImage
```

## Windows

- **Installer:** run `KubeScope-<version>-windows-x64-setup.exe`.
- **Portable:** unzip `KubeScope-<version>-windows-x64.zip` and run
  `KubeScope\KubeScope.exe`.

## macOS

Download the zip for your Mac: `KubeScope-<version>-macos-arm64.zip` for Apple silicon
(M1 and newer) or `KubeScope-<version>-macos-x86_64.zip` for Intel. Unzip it and move
`KubeScope.app` to Applications. The app is not signed yet, so the first time,
right-click it and choose **Open**.

## Other systems

There is no package. Run it from source with Python 3.15; the steps
are in [Building from source]({{ '/guides/building-from-source/' | relative_url }}).

## Uninstall

- `.deb`: `sudo apt remove kubescope`
- AppImage and portable zip: delete the file or folder.
- macOS: delete `KubeScope.app`.

Your preferences are kept separately in `settings.json`; see
[Troubleshooting]({{ '/guides/troubleshooting/' | relative_url }}#where-are-the-settings).
