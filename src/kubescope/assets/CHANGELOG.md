# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- The **Light** theme is gray instead of white: the page, the side menu, the tables and the fields use soft grays with firmer borders, and the quiet texts are a step stronger to read on them by @danilogco

## [1.3.0-rc2] - 2026-10-29

### Added

- Gabi reads the live CPU and memory of a Pod, by container, beside what each container asks for and may use, as KubeScope shows them, and the lists she reads carry the use of each Pod and workload, so she no longer sends you to `kubectl top` for what she can read by @danilogco

### Changed

- An alpha, a beta or a release candidate now updates to the next pre-release as well as to the stable release that follows it, and never to an older one; a stable installation still updates only to stable releases by @danilogco

### Fixed

- The messages of the chat are no longer cut at the end or squeezed into a narrow bubble: each is as high as its text and as wide as the text needs, up to the room it has by @danilogco

## [1.3.0-rc1] - 2026-10-29

### Added

- **Gabi**, the assistant of DCO Tecnologia and an expert in Kubernetes and KubeScope: a chat in the corner of the window that only talks about Kubernetes and KubeScope, laid out like a phone chat, that asks a coding assistant that is already installed on your computer (Claude Code or Codex) about the cluster, without asking you for credentials or storing any. It sees what you see (the list, the selected row, the open Details or Logs, the numbers of the overviews and the open tabs), reads details, logs, lists and events to look into a problem, answers in the language of the app, and can change the window as you would: go to a list, a page, a tab or the logs of a Pod. A change to the cluster is only a card with **Run**, available with the write mode on; in the read-only mode it has no way to edit, update or delete anything and tells you so when you ask. You can attach images and text files, resize the panel, take it out into a window of its own, and the conversations are kept for each context, without the data that was read. It starts off until you open it and agree, and **Settings** turns it off by @danilogco
- Windows, dialogs and lists rise into place as they first show, and **Settings** can turn it off by @danilogco
- When GitHub limits the update checks, the footer says when to try again by @danilogco
- Gabi asks which container you mean when a Pod or a workload has more than one main container, reads the main one without asking when there is only one, and never takes an init container (a migration, say) unless you ask for it; the lists she reads now show the containers of Pods and workloads by @danilogco
- A guide that opens when there is no Claude Code CLI or Codex CLI on the computer, with a button for the settings and one for the installation guide of each by @danilogco
- The side menu opens with every section open, can be resized by its right edge, and remembers both by @danilogco

### Changed

- The app updates only to **stable** releases: an alpha, a beta or a release candidate is never offered, and a release candidate is told about its own stable release when it comes by @danilogco
- The update check no longer asks GitHub again when the app starts within an hour of finding that it is up to date, so it spends less of the limit GitHub gives an address by @danilogco

## [1.2.0] - 2026-10-29

### Added

- A **Reason** filter in the Events list by @danilogco

### Fixed

- The events lists, in the Workloads overview and the Events view, are ordered by **Age**, youngest first, instead of by name or by when each event was last seen by @danilogco
- The search bar looks through every column, not only the namespace, kind and name by @danilogco

## [1.1.1] - 2026-10-28

### Changed

- The **Age** columns show hours, minutes and seconds, such as `1h5m3s`, and count up on their own by @danilogco

### Removed

- The green background of the Pods younger than an hour by @danilogco

## [1.1.0] - 2026-10-28

### Added

- **Events** in the side menu, below Cluster: the events of the namespace with their type, reason, object, message and count, a filter by type (Normal or Warning), the Details, and, in the write mode, **Edit** (the JSON of the event, replaced on save) by @danilogco
- **Delete**, in the write mode, is on every resource the lists show (workloads, network and config resources), in the buttons and the right-click menu, after a confirmation by @danilogco

### Changed

- Statuses and reasons are badges, a rounded outlined pill, in the Pods, the workloads, the Nodes, the events and the Node Groups and Add-ons: green when fine, amber while it changes, red when it failed. The **RESTARTS** of a Pod or a workload is a badge too, amber from one restart and red from ten by @danilogco
- A Pod of a StatefulSet has a slightly lighter row in the Pods list by @danilogco
- The top items of the side menu are a little shorter by @danilogco

### Fixed

- The Install link of the GitHub Pages site (top bar and footer) opens the install page: the page now has the `/install/` address the links point to by @danilogco

## [1.0.0] - 2026-10-26

### Added

- A CodeQL workflow scans the Python code and the workflows for security problems every two weeks, and on demand by @danilogco
- A search bar in the Logs and in the Details (which looks in the Raw JSON), with **Aa** to match the case and **.\*** to read a regular expression: it marks every match, says how many there are, and goes to the next or the previous with Enter and Shift+Enter (Ctrl+F focuses it, Esc clears it). The search box of the lists has the same two switches by @danilogco
- **Forward**, in the write mode, is also on Pods (in the Pods list and in the Pods of a workload) and on StatefulSets: it shows the complete `kubectl port-forward` command for a TCP port you pick and a local port: the ports their containers declare and the ones the Services that select them send to (the app reads the Services of the namespace for that), or, when there is none, the port you type by @danilogco
- In the write mode, the buttons and the right-click menu show only the actions the cluster lets you do: the app asks it, for the namespace of the selected row, with one access review for each action (the question `kubectl auth can-i` asks), and the answer is kept for five minutes. Until the cluster answers, or when a review fails, every action is shown and the cluster decides when it is tried by @danilogco

### Changed

- The GitHub Pages site loads Google Tag Manager and Google Analytics (`google_tag_manager_id` and `google_analytics_id` in `docs/_config.yml`; an empty one leaves its tag out) by @danilogco
- The GitHub Pages site uses a landing page adapted from the Automatic Jekyll theme (MIT): the app in a desktop window, direct download buttons, the features and an install page, in place of the Cayman theme by @danilogco
- KubeScope is now described as a desktop IDE for the whole Kubernetes ecosystem, not only a viewer or an EKS tool, in the README, the docs, the package descriptions (pip, deb, AppImage, Snap and Flatpak) and the guides for contributors by @danilogco
- The Flatpak no longer carries the AWS CLI: like `gcloud`, `az`, `kubelogin` and `oci`, the `aws` of the system runs on the host through `flatpak-spawn --host`, so EKS contexts use the version and the profiles of the person's own installation (the bundled AWS CLI v1 rejected some commands that the app sends), and the `~/.aws` permission is gone from the manifest by @danilogco

### Removed

- The Flatpak and Snap Store workflows: the Flatpak is no longer built and attached to the release after it, and the snap is no longer sent to the Snap Store from GitHub, so both are uploaded by hand by @danilogco

## [0.14.0] - 2026-10-23

### Added

- KubeScope is packaged as a snap named `dco-kubescope` (`make snap`; the Snap Store reserves `kubescope`). It is classic, like kubectl and helm, so it runs the sign-in tools of every cloud (aws, gcloud, az, kubelogin, oci...) from the system. The Release workflow builds it, and a separate Snap Store workflow sends it to the `candidate` channel of the store after a Release of a tag by @danilogco
- A Flatpak workflow builds `KubeScope-<version>.flatpak` after a Release of a tag and attaches it to the GitHub release by @danilogco
- The Flatpak works with GKE, AKS, OCI and the other clouds: the sign-in programs of the kubeconfig and the login commands run on the host through `flatpak-spawn --host` (the manifest asks for the `org.freedesktop.Flatpak` permission, which SECURITY.md explains), while the AWS CLI stays the one the Flatpak carries by @danilogco

### Changed

- The list on screen is redrawn only when the cluster's answer differs from what is shown, so the quiet read every five seconds no longer rebuilds the table, and the scroll position, the selection and the hover stay still by @danilogco
- A list that keeps failing is read again less and less often (up to once a minute) instead of every five seconds, and goes back to five seconds as soon as the cluster answers by @danilogco
- Lists ask the API server for its cached copy (`resourceVersion=0`), which is cheaper for the cluster than reading its datastore every few seconds by @danilogco
- The namespaces of a cluster are read once a minute instead of with every refresh by @danilogco
- Pod CPU and memory are read from the metrics server at most every 15 seconds, the pace at which it samples, instead of with every refresh by @danilogco
- An open log asks the cluster only for the lines after the last one shown and adds them to the end, instead of downloading and redrawing the last 500 lines every three seconds; the Refresh button still reads the whole tail, and a log that keeps growing holds up to 5,000 lines by @danilogco
- When a read changes a few rows of a list, only those rows are rewritten instead of every cell of the table by @danilogco
- A sign-in that failed, such as an expired AWS SSO token, is not run again for 30 seconds, so a list no longer starts the `aws` program a dozen times just to fail the same way; the Refresh button tries again at once by @danilogco
- Requests to the cluster accept a gzip-compressed answer, which the API server uses for large lists, so a big list crosses the network in a fraction of its size by @danilogco
- The app starts about 110 ms sooner: the Kubernetes client library is loaded by the first request to a cluster, on a worker, instead of before the window shows by @danilogco
- The bundle is never compressed with UPX, even when the tool is installed on the machine that builds it, so the Qt libraries are not unpacked at every start and antivirus scanners have no packed binary to flag by @danilogco
- The colors of the status column are worked out once per list instead of once per row by @danilogco

### Fixed

- Changing the language while a list with few columns is on screen no longer fails with an error: the table gets back the columns its layout has before the texts are translated, and the list draws its own columns again right after by @danilogco

## [0.13.0] - 2026-10-22

### Changed

- The list on screen is read again every five seconds instead of ten by @danilogco

### Added

- The window draws its own title bar in the top bar, with the minimize, maximize and close buttons, which saves a row of space; the window moves by dragging the bar and resizes from its edges, and a Settings option brings back the title bar of the system by @danilogco

### Fixed

- The tabs of the top bar take the room they need instead of being scrolled while there is space left by @danilogco
- The installed app starts again: the bundle left out the Qt network module that the single-instance check needs, so it stopped with "No module named PySide6.QtNetwork" by @danilogco
- On Windows the notice of a new version reaches the notification center: the app and the shortcuts of the installer now share one application ID by @danilogco

## [0.12.1] - 2026-10-22

### Fixed

- Starting KubeScope again brings the running one forward instead of opening a second window, also when it is in the system tray by @danilogco
- The list on screen follows the cluster: it is read again every ten seconds, quietly, so Pods that come and go show up without a manual refresh, and the selected row stays on the same item by @danilogco

## [0.12.0] - 2026-10-21

### Added

- A Wrap lines option in the logs breaks long lines to the width of the view, to read them without scrolling sideways; it is off by default and the choice is remembered by @danilogco

## [0.11.2] - 2026-10-21

### Fixed

- The languages are listed again in the installed app: the bundle did not ship the language files by @danilogco
- A select no longer changes when the wheel scrolls the page over it: the wheel goes to the page, and a select changes by a click or the keys by @danilogco
- The default namespace of the Settings is a text field, with the namespaces of the cluster offered as you type, instead of a select by @danilogco

## [0.11.1] - 2026-10-21

### Fixed

- The links in the Details of a resource open the resource when clicked by @danilogco

## [0.11.0] - 2026-10-21

### Added

- Pods show a colored square for each container, and workloads one for each replica (up to five): green when running, yellow when pending, red on error or restarting, gray when terminated by @danilogco
- The Pods list has Controlled By, Node and QoS columns, and READY grows to fit the squares of the widest row by @danilogco
- Quick links: the Node and Controlled By of a Pod, the Nodes of the Node Groups, the resource of an event, and the Node, Namespace, controller, ConfigMap and Secret named in a resource's Details open their own Details when clicked by @danilogco
- A NODE SELECTOR column in the Deployments, StatefulSets, DaemonSets, ReplicaSets, Jobs and CronJobs lists by @danilogco
- Right-click on a tab of the top bar offers Close and Close all by @danilogco

### Fixed

- The tabs of the top bar scroll sideways, with the wheel, when they do not fit, instead of cutting the first ones by @danilogco

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

[Unreleased]: https://github.com/dcotecnologia/kubescope/compare/v1.3.0-rc2...HEAD
[1.3.0-rc2]: https://github.com/dcotecnologia/kubescope/compare/v1.3.0-rc1...v1.3.0-rc2
[1.3.0-rc1]: https://github.com/dcotecnologia/kubescope/compare/v1.2.0...v1.3.0-rc1
[1.2.0]: https://github.com/dcotecnologia/kubescope/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/dcotecnologia/kubescope/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/dcotecnologia/kubescope/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/dcotecnologia/kubescope/compare/v0.14.0...v1.0.0
[0.14.0]: https://github.com/dcotecnologia/kubescope/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/dcotecnologia/kubescope/compare/v0.12.1...v0.13.0
[0.12.1]: https://github.com/dcotecnologia/kubescope/compare/v0.12.0...v0.12.1
[0.12.0]: https://github.com/dcotecnologia/kubescope/compare/v0.11.2...v0.12.0
[0.11.2]: https://github.com/dcotecnologia/kubescope/compare/v0.11.1...v0.11.2
[0.11.1]: https://github.com/dcotecnologia/kubescope/compare/v0.11.0...v0.11.1
[0.11.0]: https://github.com/dcotecnologia/kubescope/compare/v0.10.2...v0.11.0
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
