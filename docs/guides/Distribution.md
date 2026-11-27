---
layout: page
title: Distribution
permalink: /guides/distribution/
---

Where KubeScope is published, how each channel is built and checked, and what we do not
publish, with the reason.

## Where it is published

Every channel is built by the [Release workflow](https://github.com/dcotecnologia/kubescope/blob/main/.github/workflows/release.yml)
from a `v*` tag and published as a [GitHub release](https://github.com/dcotecnologia/kubescope/releases).
That page is the source of truth: a file that is not there is not ours.

| Channel | File | Updates |
| ------- | ---- | ------- |
| Install script | `install.sh`, `install.ps1` | run it again; it picks the right package and checks its sha256 |
| Debian and Ubuntu | `kubescope_<version>_amd64.deb` | `kubescope update`, or install the new `.deb` |
| Fedora | `kubescope-<version>-1.x86_64.rpm` | install the new `.rpm` |
| Arch Linux | `kubescope-<version>-1-x86_64.pkg.tar.zst` | `pacman -U` the new file |
| Any Linux | `KubeScope-<version>-x86_64.AppImage` | `kubescope update` replaces the file |
| Windows | installer and portable zip | `kubescope update` runs the installer silently |
| macOS | zip for Apple silicon and for Intel | download the new zip |
| Python | `pip install` from source | `git pull`, `pip install -e .` |

How to install each one is in the [installation guide]({{ '/guides/installation/' | relative_url }}),
and how to build them is in [building from source]({{ '/guides/building-from-source/' | relative_url }}).

## What every channel keeps

- The file comes from this repository's release, and the install script and
  `kubescope update` check it against the sha256 that GitHub publishes before anything is
  installed.
- It is the same application in all of them: the packages are the same PyInstaller bundle,
  without patches that change how it behaves.
- The dependencies are locked in `uv.lock`, and the licenses of what is bundled are in
  `THIRD_PARTY_NOTICES.txt`.

## Linux: our own packages only

On Linux, KubeScope is published as a `.deb`, an `.rpm`, an Arch Linux package and an
AppImage, built by us from the same bundle and attached to the release.

We do not build or publish a Flatpak or a snap, and we do not plan to distribute KubeScope
through Flathub or any other app store. The reasons:

- **A store decides for us.** Whether an app is listed, and what it may do, is up to the
  reviewers of the store, under rules they write and change. A project has no vote in them
  and no clear way to appeal.
- **The review is hard to trust.** It is case by case, and a reviewer can ask for a change
  to how the app works to fit the store, such as how it signs in to a cluster or runs the
  tools of your system, which is what KubeScope depends on to reach EKS, GKE and AKS.
- **We would lose control of the build.** A store builds and publishes its own copy. We
  could not promise that what you install is exactly the file we released.

None of this says anything about the people who use or maintain those stores. A listing of
KubeScope there that is not from us is not supported by us.

## What to use

Use the [install script]({{ '/guides/installation/' | relative_url }}), the `.deb` or the
AppImage on Linux, the installer or the zip on Windows, and the zip on macOS.

If a channel you need is missing, open an
[issue](https://github.com/dcotecnologia/kubescope/issues).
