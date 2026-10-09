---
---

# Code signing policy

Free code signing for the KubeScope Windows installer is provided by
[SignPath.io](https://signpath.io), with a certificate from the
[SignPath Foundation](https://signpath.org).

## What is signed

Only the Windows installer (`KubeScope-<version>-windows-x64-setup.exe`) that the
[Release workflow](https://github.com/dcotecnologia/kubescope/blob/main/.github/workflows/release.yml)
builds on GitHub-hosted runners from the public source code. Nothing built on a
developer machine is signed.

## Roles

- **Author, reviewer and approver:** [Danilo Carolino](https://github.com/dcotecnologia),
  the project maintainer. Every release is approved by hand in SignPath before
  the signature is applied.

## Privacy

KubeScope does not collect or send any data to its authors or to any third
party. It reads your local kubeconfig and talks only to the clusters you
choose, through the bundled `kubectl`. See the
[security policy](https://github.com/dcotecnologia/kubescope/blob/main/SECURITY.md).
