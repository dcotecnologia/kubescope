---
layout: page
title: Install
permalink: /install/
---

## Direct downloads

The packages of the [latest release](https://github.com/dcotecnologia/kubescope/releases/latest): a `.deb` for Debian and Ubuntu, an AppImage for any Linux, and a Windows installer and portable `.zip`.

## Install or update from the command line

One command installs the latest release and, run again, updates it. It picks the
right package for your system and checks the download against the sha256 that GitHub
publishes before installing anything.

Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/dcotecnologia/kubescope/main/install.sh | sh
```

Windows (PowerShell, for your user, no administrator needed):

```powershell
irm https://raw.githubusercontent.com/dcotecnologia/kubescope/main/install.ps1 | iex
```

On Debian and Ubuntu it installs the `.deb` with `apt` (it asks for your password);
elsewhere it puts the AppImage in `~/.local/share/kubescope`. You can read
[install.sh](https://github.com/dcotecnologia/kubescope/blob/main/install.sh) and
[install.ps1](https://github.com/dcotecnologia/kubescope/blob/main/install.ps1) first.

The [installation guide](https://github.com/dcotecnologia/kubescope/wiki/Installation)
has the steps for each package.

## Learn more

- [Connecting to clusters](https://github.com/dcotecnologia/kubescope/wiki/Connecting-to-clusters)
- [Using KubeScope](https://github.com/dcotecnologia/kubescope/wiki/Using-KubeScope)
- [Troubleshooting](https://github.com/dcotecnologia/kubescope/wiki/Troubleshooting)
- [Source code](https://github.com/dcotecnologia/kubescope) (MIT license)
