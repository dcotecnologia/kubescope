---
---


# KubeScope

Desktop viewer for Kubernetes workloads, including Amazon EKS, Google GKE and Azure AKS clusters available
through your local Kubernetes configuration. It uses the official Kubernetes Python client, so it needs no `kubectl`, and
is read-only by default: it lists and inspects resources. An optional write mode
adds delete, evict, shell, scale and restart actions.

![KubeScope cluster overview](screenshots/overview.png)

## Features

- **Overview:** nodes, Pod counts, CPU and memory requests against capacity.
- **Workloads:** Pods and Deployments with status, CPU, memory and restarts,
  filtered by namespace and searchable by name.
- **Details and logs:** JSON details and live Pod logs, each in its own tab.
- **Readable errors:** short messages with a hint, with the original error
  text one click away.
- **English, Portuguese, Spanish, Italian, French, Chinese, Japanese, Arabic, Hindi
  and Russian**, selectable in Settings.

## Get it

<p id="download-version">Direct downloads of the
<a href="https://github.com/dcotecnologia/kubescope/releases/latest">latest release</a>:</p>

<ul id="downloads">
  <li><a data-asset="\.deb$" href="https://github.com/dcotecnologia/kubescope/releases/latest">Debian and Ubuntu (.deb)</a></li>
  <li><a data-asset="\.AppImage$" href="https://github.com/dcotecnologia/kubescope/releases/latest">Any Linux (AppImage)</a></li>
  <li><a data-asset="-windows-x64-setup\.exe$" href="https://github.com/dcotecnologia/kubescope/releases/latest">Windows installer (.exe)</a></li>
  <li><a data-asset="-windows-x64\.zip$" href="https://github.com/dcotecnologia/kubescope/releases/latest">Windows portable (.zip)</a></li>
</ul>

<script>
  // File names carry the version, so the links are resolved from the latest release.
  // Without JavaScript they stay pointed at the release page.
  fetch("https://api.github.com/repos/dcotecnologia/kubescope/releases/latest")
    .then(function (response) { return response.ok ? response.json() : Promise.reject(); })
    .then(function (release) {
      document.querySelectorAll("#downloads a[data-asset]").forEach(function (link) {
        var pattern = new RegExp(link.dataset.asset);
        var asset = release.assets.find(function (item) { return pattern.test(item.name); });
        if (asset) { link.href = asset.browser_download_url; }
      });
      document.getElementById("download-version").textContent =
        "Direct downloads of KubeScope " + release.tag_name.replace(/^v/, "") + ":";
    })
    .catch(function () {});
</script>

### Install or update from the command line

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
has the one-command install script and the steps for each package.

## Learn more

- [Connecting to clusters](https://github.com/dcotecnologia/kubescope/wiki/Connecting-to-clusters)
- [Using KubeScope](https://github.com/dcotecnologia/kubescope/wiki/Using-KubeScope)
- [Troubleshooting](https://github.com/dcotecnologia/kubescope/wiki/Troubleshooting)
- [Source code](https://github.com/dcotecnologia/kubescope) (MIT license)
