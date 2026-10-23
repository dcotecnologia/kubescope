# Installation

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

- **Linux:** it installs the `.deb` through `apt` (it asks for your password) on
  Debian and Ubuntu, and otherwise puts the AppImage in `~/.local/share/kubescope`
  and links it as `~/.local/bin/kubescope`. An update replaces the old file.
- **Windows:** it runs the installer silently for your user. An update installs over
  the old version.
- **Options:** save the script to pass them. `--dry-run` (`-DryRun`) shows what would
  happen, `--version 0.1.0` (`-Version 0.1.0`) picks a release, `--force` (`-Force`)
  reinstalls, and on Linux `--method deb` or `--method appimage` picks the package.
- **Safety:** a script piped into a shell runs with your rights, so you can read
  [install.sh](https://github.com/dcotecnologia/kubescope/blob/main/install.sh) and
  [install.ps1](https://github.com/dcotecnologia/kubescope/blob/main/install.ps1)
  first. The sha256 check catches a damaged or swapped download; it trusts GitHub and
  the repository.
- **AppImage:** it needs FUSE 2 (`libfuse2`); if it will not start, install that.

## Install by hand

Download the package for your system from the
[releases page](https://github.com/dcotecnologia/kubescope/releases). You do
not need `kubectl`.

## Debian and Ubuntu (.deb)

```bash
sudo apt install ./kubescope_<version>_amd64.deb
kubescope
```

## Any Linux (AppImage)

```bash
chmod +x KubeScope-<version>-x86_64.AppImage
./KubeScope-<version>-x86_64.AppImage
```

## Flatpak

```bash
flatpak install --user KubeScope-<version>.flatpak
flatpak run com.dcotecnologia.KubeScope
```

The Flatpak reads `~/.kube` (read-only) and carries no cloud CLI. To sign in to EKS,
GKE, AKS or OCI it asks the host to run the tools of your system (`aws`, `gcloud`,
`az`, `kubelogin`, `oci`...), so install them there as usual. It does this through the
`org.freedesktop.Flatpak` permission, which lets the app run programs outside the
sandbox; read [SECURITY.md](https://github.com/dcotecnologia/kubescope/blob/main/SECURITY.md)
before you install it.

## Windows

- **Installer:** run `KubeScope-<version>-windows-x64-setup.exe`.
- **Portable:** unzip `KubeScope-<version>-windows-x64.zip` and run
  `KubeScope\KubeScope.exe`.

## macOS and other systems

There is no package yet. Run it from source with Python 3.12 or newer; the steps
are in [Building from source](Building-from-source).

## Uninstall

- `.deb`: `sudo apt remove kubescope`
- Flatpak: `flatpak --user uninstall com.dcotecnologia.KubeScope`
- AppImage and portable zip: delete the file or folder.

Your preferences are kept separately in `settings.json`; see
[Troubleshooting](Troubleshooting#where-are-the-settings).
