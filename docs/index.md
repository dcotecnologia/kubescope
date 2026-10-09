---
---


# KubeScope

Desktop viewer for Kubernetes workloads, including Amazon EKS clusters available
through your local Kubernetes configuration. It ships with its own `kubectl` and
is read-only for now: it lists and inspects resources but does not change the
cluster.

![KubeScope cluster overview](screenshots/overview.png)

## Features

- **Overview:** nodes, Pod counts, CPU and memory requests against capacity.
- **Workloads:** Pods and Deployments with status, CPU, memory and restarts,
  filtered by namespace and searchable by name.
- **Details and logs:** JSON details and live Pod logs, each in its own tab.
- **Readable errors:** short messages with a hint, with the original `kubectl`
  text one click away.
- **English and Portuguese**, selectable in Settings.

## Get it

- [Latest release](https://github.com/dcotecnologia/kubescope/releases/latest):
  `.deb`, AppImage, Flatpak and Windows installer.
- [Installation guide](https://github.com/dcotecnologia/kubescope/wiki/Installation)

## Learn more

- [Connecting to clusters](https://github.com/dcotecnologia/kubescope/wiki/Connecting-to-clusters)
- [Using KubeScope](https://github.com/dcotecnologia/kubescope/wiki/Using-KubeScope)
- [Troubleshooting](https://github.com/dcotecnologia/kubescope/wiki/Troubleshooting)
- [Source code](https://github.com/dcotecnologia/kubescope) (MIT license)
