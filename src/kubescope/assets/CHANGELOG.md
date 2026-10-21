# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Pods show a colored square for each container, and workloads one for each replica (up to five): green when running, yellow when pending, red on error or restarting, gray when terminated by @danilogco

## [0.10.2] - 2026-10-21

### Fixed

- `kubescope update --version X.Y.Z` can install an older version of the .deb, which apt used to refuse as a downgrade by @danilogco

## [0.10.1] - 2026-10-21

### Fixed

- On Windows, opening Cluster or Node Groups no longer flashes blank terminal windows: the AWS CLI commands the app runs now start without a console by @danilogco
- The cluster data of the Overview (VPC, subnets, endpoint) now loads after the first sign-in to a context, and when switching to a signed-in one, instead of staying empty until the page was opened again by @danilogco

## [0.10.0] - 2026-10-20

### Added

- Command line options: `kubescope --version`, `kubescope info`, `kubescope cleanup [--all] [--dry-run]` to delete the debug and crash logs, `kubescope check-update`, whose exit code says whether there is a newer version, and `kubescope update [--version X.Y.Z]` to install the latest or the given version by @danilogco
- A setting, on by default, keeps the app running in the background with an icon in the system tray when the window is closed by @danilogco
- The app looks for a new version every hour and, with the tray icon on, tells the operating system when there is one, once a day for the hourly check and every time for a check you ask for by @danilogco

### Fixed

- The message boxes, such as **Query failed**, use the window's own buttons instead of the style's stock ones by @danilogco
- Changing the context no longer shows the Details and Logs tabs of the previous one; they stay open for when it comes back by @danilogco

### Changed

- Each list starts with the NAME column wide enough for its names by @danilogco

## [0.9.1] - 2026-10-20

### Fixed

- The window stays usable while a list loads: the contexts and namespaces can be changed at any time, the load of the one left is cancelled, and the refresh button becomes **Cancel** while it runs by @danilogco
- Add-ons list the Helm releases of every namespace, so the default namespace no longer leaves them out in the contexts that have it by @danilogco

### Changed

- The contexts are listed in alphabetical order, ignoring case by @danilogco
- The code passes pyright, the checker behind Pylance, and pre-commit and CI run it on every change by @danilogco

## [0.9.0] - 2026-10-19

### Added

- The details of a resource open as an **Overview** laid out in sections (Properties, Spec, Status...) with badges for labels and lists, a table for lists of flat items and a subsection for each container, with the **Raw JSON** one click away by @danilogco
- The details of a Pod chart its live CPU and memory when the cluster has metrics-server, with the value marks, a time mark for every minute and a cursor that shows the time and value under the mouse by @danilogco
- The raw JSON of the details shows the line numbers by @danilogco

### Changed

- The JSON and the logs are colored like VS Code (Dark+ on the dark themes, Light+ on the light ones) by @danilogco

## [0.8.0] - 2026-10-19

### Changed

- Python 3.15 is supported: the tests run on 3.12 to 3.15 in CI and `requires-python` is `>=3.12,<3.16`; the releases are built on 3.15 by @danilogco

## [0.7.1] - 2026-10-19

### Changed

- The debug log and the crash log say more about the machine: the system, the desktop session, the Qt variables, the platform plugin Qt picked and where each native library (xkbcommon, fontconfig, GLib, X11...) was loaded from, bundle or system, and the log records the non-text keys pressed (Ctrl, arrows, shortcuts; never typed text) by @danilogco

### Fixed

- The app no longer crashes on the first key press (Ctrl) on a newer distro such as Ubuntu 26.04: the bundle shipped its own keyboard library, built for older keymap data, so the Linux bundle now uses the one of the system and the `.deb` depends on it by @danilogco

## [0.7.0] - 2026-10-17

### Added

- Eight themes inspired by the community: Dark Modern, Light Modern, Solarized Dark, Solarized Light, Monokai, Tomorrow Night Blue, Abyss and Quiet Light by @danilogco
- The theme editor has a **Reset** button that undoes the color changes made since it opened, and **Delete theme...** in Settings removes a theme you made after asking (back to Dark if it was in use; none of the themes that ship with the app can be deleted, and a theme file removed by hand is copied back when the app starts) by @danilogco
- A write mode, off by default and switched in Settings, adds, as buttons above the table and in the right-click menu, the actions that change a cluster: delete or evict a Pod, scale or restart a Deployment (each after a confirmation), and show the complete `kubectl exec` command to open a shell in a Pod, for the container you pick, ready to copy, and **Forward** on a Service shows the complete `kubectl port-forward` command for a port and a local port you pick; on Windows both come for PowerShell and for cmd by @danilogco
- Clicking **Update available** asks to confirm the update, shows the current and the new version and the release notes, then downloads the release, checks its sha256, installs it the way the app was installed (AppImage, `.deb` or the Windows installer) and restarts the app; a Flatpak or a source checkout opens the release page instead by @danilogco

### Changed

- The version in the footer opens the changelog of the installed version, laid out by version with its date and a badge on the one in use, without what is not released yet by @danilogco
- Settings are grouped into cards (General, Appearance, Cluster access, Debugging, Kubeconfig files, Sign-in commands and Context names) instead of one long list by @danilogco
- The number input of the scale dialog, and the name, base and buttons of the theme editor, follow the style of the rest of the app (same borders, heights and buttons, without the platform icons) by @danilogco
- Light and Dark are stored as JSON files like the other themes, in `src/kubescope/themes/` (renamed from `community_themes/`), and the themes that ship with the app are copied to your themes folder whenever their file is missing, not only the first time by @danilogco

### Fixed

- The selects that choose the Pod or the container for the logs look like the other selects of the app, with the same border, arrow and highlight, instead of the plain system dialog by @danilogco
- The install script lets apt read the downloaded `.deb`, which ends the warning that the download was "performed unsandboxed as root" by @danilogco

## [0.6.2] - 2026-10-16

### Fixed

- The logs of a pod can be opened for its init containers (a migration that runs and stops, for example), which are now offered in the container picker before the regular ones by @danilogco

## [0.6.1] - 2026-10-14

### Fixed

- The tabs of an open Details or Logs can be dragged and closed with the middle button like the pinned ones, and every tab of the top bar can be moved among all the others by @danilogco

## [0.6.0] - 2026-10-14

### Added

- A welcome message on opening the app invites people to contribute, with buttons to the GitHub project and its sponsor page, **Maybe later** and **Don't show again**, which is remembered in the settings by @danilogco
- The Cluster and Workloads **Overview** pages can be pinned to the top bar like the lists, from the right-click menu or a double click by @danilogco
- Pinned tabs can be dragged to reorder them: the tab fades where it was, a translucent copy follows the cursor and a line shows where it will land by @danilogco

### Changed

- Every package now carries `THIRD_PARTY_NOTICES.txt` with the licenses of the libraries it ships (Qt for Python under the LGPL-3.0, the Kubernetes client, the fonts and the others) by @danilogco
- The bundle only ships the Qt modules the app uses (Core, Gui and Widgets) and leaves out the GPL-only Qt Virtual Keyboard, Qt PDF and QML, making it about half the size by @danilogco
- Linux packages also carry `THIRD_PARTY_SYSTEM_LIBRARIES.txt`, the license notices of the system libraries copied into the bundle (GTK, GLib, FreeType, ICU and the others), written by `make build` by @danilogco
- The resource lists fit the window without a horizontal scroll bar, with headers aligned to their cells, no vertical grid lines and denser rows by @danilogco

### Fixed

- Large lists refresh and filter faster: the table repaints once per update instead of once per row by @danilogco

## [0.5.1] - 2026-10-13

### Fixed

- On Windows, updating with the installer no longer leaves the old version showing: the installer now clears the previous install's files before copying the new ones by @danilogco

## [0.5.0] - 2026-10-13

### Added

- Languages are JSON files, replacing the Qt `.ts` and `.qm` files; a file in the `languages` folder of the settings adds a language or replaces a shipped one by @danilogco
- German, Dutch, Polish, Turkish, Indonesian, Vietnamese, Ukrainian, Thai, Chinese (traditional), Hebrew, Persian and Korean translations, selectable in Settings. Hebrew and Persian are written right to left, so the whole layout mirrors; **Automatic** picks the traditional Chinese for Taiwan, Hong Kong and Macau by @danilogco
- The language list in Settings shows each language by its own name followed by its English name, in alphabetical order by the English one by @danilogco
- The app reopens on the page and list you left it on, together with the last context (the same Settings option) by @danilogco
- Pod logs color a JSON object (or a Python dict) written in a line: keys, strings, numbers and literals each get their own color by @danilogco

### Changed

- Debug logs and crash logs older than 30 days are deleted at startup, on a background thread by @danilogco
- Helm releases in Add-ons show the chart and app version, read from the labels of the workloads they installed, instead of only the revision by @danilogco
- Details and Logs no longer have an entry in the side menu: each one opens as a tab in the top bar, next to the pinned lists, with a × to close it by @danilogco

### Fixed

- Pod logs no longer show the color codes of loggers such as coloredlogs as boxes by @danilogco
- Working offline now shows **No network connection**, with a hint to check the internet or VPN, instead of a generic error when the AWS CLI cannot reach its endpoint by @danilogco

## [0.4.0] - 2026-10-12

### Added

- Hindi and Russian translations, selectable in Settings; **Automatic** follows the system language by @danilogco
- A Config menu with Config Maps, Secrets, Resource Quotas, Limit Ranges, Horizontal Pod Autoscalers, Pod Disruption Budgets, Priority Classes, Runtime Classes, Leases and the Mutating and Validating Webhook Configurations, read only and with Details. The Details of a Secret never show its values by @danilogco
- A Cluster info card and a Networking card on the Overview of Amazon EKS contexts, read with `aws eks describe-cluster` by @danilogco
- Node Groups (a main-menu entry under Overview) for Amazon EKS contexts, and Add-ons (in Config) with the Helm releases of any cluster and the EKS add-ons, read through the AWS CLI and the Kubernetes API, without the data of any Secret, with the AMI version of each node group, the cluster's nodes in the same view and no namespace filter by @danilogco
- Pin any list as a tab in the top bar with a double-click (or a right-click), and unpin it with the middle button, for quick access by @danilogco

### Changed

- The Nodes table moved from the Overview to the Node Groups view, and the Namespace and Kind columns are no longer shown in any list by @danilogco

## [0.3.0] - 2026-10-11

### Added

- Spanish, Italian, French, Chinese (simplified), Japanese and Arabic translations, selectable in Settings; **Automatic** follows the system language. Arabic is written right to left, so the whole layout mirrors. The `.deb` recommends `fonts-noto-cjk` for the Chinese and Japanese text by @danilogco

### Changed

- The release notes on GitHub are the section of this changelog for the version, with the author of each line, instead of a list of pull requests by @danilogco

## [0.2.0] - 2026-10-11

### Added

- The window opens at the size, position and maximized state it had when it was closed by @danilogco
- Google GKE and Azure AKS contexts: when their credentials expire (`gke-gcloud-auth-plugin`, `kubelogin`), a **Sign in to Google Cloud** or **Sign in to Azure** button runs `gcloud auth login` or `az login` and reloads the data, as the AWS button does. Their sign-in errors show as "Authentication failed" by @danilogco
- An update check against GitHub's public API: an icon in the footer spins while it looks, shows "Up to date" for a moment, or an **Update available** link to the download page, and a click checks again. It runs when the app starts, sends only the app version, and **Settings** can turn the startup check off by @danilogco
- `install.sh` (Linux) and `install.ps1` (Windows) install or update KubeScope from the files of the latest GitHub release, after checking each download against the sha256 that GitHub publishes. The README and the wiki recommend them by @danilogco
- `crash.log` starts every session with the KubeScope version and git commit, the Python, PySide6 and Qt versions, the system and the time, so a crash can be tied to a build. Bundles record their commit when they are built by @danilogco
- **Clear the cache** in Settings: forgets the lists and overviews already loaded and the sign-in of every cluster; your settings are kept by @danilogco
- **Kubeconfig files** in Settings: read the files you choose instead of the `KUBECONFIG` variable or `~/.kube/config`. The list only shows once it has files by @danilogco
- **Sign-in commands** in Settings: for a cloud KubeScope does not know, map the sign-in program of your kubeconfig (such as `oci`) to the command that signs you in. The **Sign in** button runs it, without a shell, and offers it when that program fails. The table only shows once it has rows by @danilogco

### Changed

- The sign-in button reads **Sign in to {cloud}** and the Authentication failed hint names the three login commands by @danilogco
- KubeScope talks to the cluster with the official `kubernetes` Python client instead of a bundled `kubectl`, with the same features: it reads the kubeconfig and runs its sign-in plugins (such as `aws eks get-token`), and only sends `GET` requests. The packages no longer ship a `kubectl` binary, `make kubectl` and `tools/fetch_kubectl.py` are gone, and the "kubectl is missing" error no longer exists by @danilogco
- Each context keeps one client, with its token and connections, so lists load faster: the sign-in program of the kubeconfig (such as `aws eks get-token`) runs once, not once per request, and runs again only when the cluster refuses the token or after you sign in by @danilogco
- Closing the window gives up on the requests in flight at once, as it did with the `kubectl` commands by @danilogco
- The Flatpak installs the Kubernetes Python client from PyPI (`python3-kubernetes.json`, made by `tools/flatpak_python_deps.py` from `uv.lock`) instead of building `kubectl`. It still bundles only the AWS CLI, so GKE and AKS sign-in need the `.deb` or the AppImage by @danilogco
- The Flatpak manifest builds from public sources: the app from its git tag, PySide6 from the `io.qt.PySide.BaseApp` base app, and the Kubernetes Python client and the AWS CLI v1 from PyPI. It no longer packages the PyInstaller bundle by @danilogco

## [0.1.0] - 2026-10-11

The first release.

### Added

- Workloads menu with lists of Pods, Deployments, StatefulSets, DaemonSets, ReplicaSets, ReplicationControllers, Jobs and CronJobs, with CPU, memory and restarts from `metrics-server`, a workloads overview with health bars and the latest cluster events, and a cluster overview by @danilogco
- Network menu with lists of Services, Endpoint Slices, Endpoints, Ingresses, Ingress Classes and Network Policies. Each kind has its own columns and a **Details** view by @danilogco
- Right-click menu on the rows of a list, with the actions of the buttons above the table by @danilogco
- Banner when the kubeconfig has no contexts, and a red banner when the cluster refuses an action for lack of permission, with a **Dismiss** button by @danilogco
- **Default namespace** in Settings, chosen from a select; each context opens on it by @danilogco
- **Save** button, an icon under the Details & Logs tabs, that writes the open tab to a file the user picks by @danilogco
- Colored JSON and logs: Monokai in the dark themes and a light palette in the light ones, following the theme in use. Logs color the timestamp, the level and the `key=value` keys by @danilogco
- `Ctrl+R` and `F5` press the refresh button of the page on screen by @danilogco
- Themes: dark and light, custom themes made in Settings, and community themes (Midnight, Sepia, High contrast) that ship with the app by @danilogco
- Sign-in check for AWS contexts, a **Sign in to AWS** button in the top bar, and an optional debug mode that writes a log file that is safe to share by @danilogco
- Portuguese translation, a language choice in Settings, and the version and a GitHub link in the footer by @danilogco
- Noto Sans and Noto Sans Mono ship with the app, so it looks the same on every system. They are under the SIL Open Font License by @danilogco
- Store screenshots of every theme in `docs/screenshots/store/`, listed in the Flatpak metainfo by @danilogco
- Tooling: `make dev` restarts the app when the source changes, `make store-screenshots` redraws the screenshots, and `make flatpak-lint` and `make flathub-submission` check and prepare a Flathub submission by @danilogco

### Changed

- The dark theme is the default by @danilogco
- Every table shows its last answer at once while fresh data loads, per context and namespace; the overviews keep theirs per context. Nothing is written to disk by @danilogco
- Pods and workload lists run their `kubectl` calls at the same time and load in parallel with each other, and quick clicks through the menu ask only for the last list by @danilogco
- The brand moved to the top bar with the logo, Settings is an icon beside the context, the page header is slimmer, the side menu is more compact, scrolls when it does not fit, and its icons follow the theme. The two menus open and close on their own by @danilogco
- The **READ ONLY** tag left the top bar; the note in the side menu stays by @danilogco

### Fixed

- The DaemonSets and ReplicaSets rows of the workloads overview did nothing after their lists were added by @danilogco
- Changing context or namespace left the rows or numbers of the previous one on screen by @danilogco
- Closing the window stops the running `kubectl` commands and closes at once by @danilogco
- A white line no longer shows in the tab bar of Details & Logs by @danilogco

### Security

- Pod logs and resource details are still never written to disk by the app on its own. **Save** is the only exception, and it writes only to the file the user chooses. SECURITY.md says so by @danilogco

[Unreleased]: https://github.com/dcotecnologia/kubescope/compare/v0.10.2...HEAD
[0.10.2]: https://github.com/dcotecnologia/kubescope/compare/v0.10.1...v0.10.2
[0.10.1]: https://github.com/dcotecnologia/kubescope/compare/v0.10.0...v0.10.1
[0.10.0]: https://github.com/dcotecnologia/kubescope/compare/v0.9.1...v0.10.0
[0.9.1]: https://github.com/dcotecnologia/kubescope/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/dcotecnologia/kubescope/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/dcotecnologia/kubescope/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/dcotecnologia/kubescope/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/dcotecnologia/kubescope/compare/v0.6.2...v0.7.0
[0.6.2]: https://github.com/dcotecnologia/kubescope/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/dcotecnologia/kubescope/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/dcotecnologia/kubescope/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/dcotecnologia/kubescope/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/dcotecnologia/kubescope/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/dcotecnologia/kubescope/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/dcotecnologia/kubescope/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/dcotecnologia/kubescope/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/dcotecnologia/kubescope/releases/tag/v0.1.0
