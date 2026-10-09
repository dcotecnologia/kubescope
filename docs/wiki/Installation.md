# Installation

Download the package for your system from the
[releases page](https://github.com/dcotecnologia/kubescope/releases). Every
package already contains `kubectl`.

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

The Flatpak includes the AWS CLI, so EKS contexts can sign in from inside the
sandbox. It can read `~/.kube` (read-only) and `~/.aws`. Other login tools, such
as `gcloud` or `kubelogin`, are not available inside it; use the `.deb` or the
AppImage if your kubeconfig needs them.

## Windows

- **Installer:** run `KubeScope-<version>-windows-x64-setup.exe`.
- **Portable:** unzip `KubeScope-<version>-windows-x64.zip` and run
  `KubeScope\KubeScope.exe`.

## Uninstall

- `.deb`: `sudo apt remove kubescope`
- Flatpak: `flatpak --user uninstall com.dcotecnologia.KubeScope`
- AppImage and portable zip: delete the file or folder.

Your preferences are kept separately in `settings.json`; see
[Troubleshooting](Troubleshooting#where-are-the-settings).
