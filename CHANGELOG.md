# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `install.sh` (Linux) and `install.ps1` (Windows) install or update KubeScope from the files of the latest GitHub release, after checking each download against the sha256 that GitHub publishes. The README and the wiki recommend them.

### Changed

- The Flatpak manifest builds from public sources, as Flathub requires: the app from its git tag, PySide6 from the `io.qt.PySide.BaseApp` base app, `kubectl` from the Kubernetes source release and the AWS CLI v1 from PyPI. It no longer packages the PyInstaller bundle.

## [0.1.0] - 2026-10-11

The first release.

### Added

- Workloads menu with lists of Pods, Deployments, StatefulSets, DaemonSets, ReplicaSets, ReplicationControllers, Jobs and CronJobs, with CPU, memory and restarts from `metrics-server`, a workloads overview with health bars and the latest cluster events, and a cluster overview.
- Network menu with lists of Services, Endpoint Slices, Endpoints, Ingresses, Ingress Classes and Network Policies. Each kind has its own columns and a **Details** view.
- Right-click menu on the rows of a list, with the actions of the buttons above the table.
- Banner when the kubeconfig has no contexts, and a red banner when the cluster refuses an action for lack of permission, with a **Dismiss** button.
- **Default namespace** in Settings, chosen from a select; each context opens on it.
- **Save** button, an icon under the Details & Logs tabs, that writes the open tab to a file the user picks.
- Colored JSON and logs: Monokai in the dark themes and a light palette in the light ones, following the theme in use. Logs color the timestamp, the level and the `key=value` keys.
- `Ctrl+R` and `F5` press the refresh button of the page on screen.
- Themes: dark and light, custom themes made in Settings, and community themes (Midnight, Sepia, High contrast) that ship with the app.
- Sign-in check for AWS contexts, a **Sign in to AWS** button in the top bar, and an optional debug mode that writes a log file that is safe to share.
- Portuguese translation, a language choice in Settings, and the version and a GitHub link in the footer.
- Noto Sans and Noto Sans Mono ship with the app, so it looks the same on every system. They are under the SIL Open Font License.
- Store screenshots of every theme in `docs/screenshots/store/`, listed in the Flatpak metainfo.
- Tooling: `make dev` restarts the app when the source changes, `make store-screenshots` redraws the screenshots, and `make flatpak-lint` and `make flathub-submission` check and prepare a Flathub submission.

### Changed

- The dark theme is the default.
- Every table shows its last answer at once while fresh data loads, per context and namespace; the overviews keep theirs per context. Nothing is written to disk.
- Pods and workload lists run their `kubectl` calls at the same time and load in parallel with each other, and quick clicks through the menu ask only for the last list.
- The brand moved to the top bar with the logo, Settings is an icon beside the context, the page header is slimmer, the side menu is more compact, scrolls when it does not fit, and its icons follow the theme. The two menus open and close on their own.
- The **READ ONLY** tag left the top bar; the note in the side menu stays.

### Fixed

- The DaemonSets and ReplicaSets rows of the workloads overview did nothing after their lists were added.
- Changing context or namespace left the rows or numbers of the previous one on screen.
- Closing the window stops the running `kubectl` commands and closes at once.
- A white line no longer shows in the tab bar of Details & Logs.

### Security

- Pod logs and resource details are still never written to disk by the app on its own. **Save** is the only exception, and it writes only to the file the user chooses. SECURITY.md says so.

[Unreleased]: https://github.com/dcotecnologia/kubescope/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/dcotecnologia/kubescope/releases/tag/v0.1.0
