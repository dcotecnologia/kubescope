# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A list opens sorted as it was left, for each list by @danilogco
- A list with no row says why and what to do: how many rows the search hides, that the namespace chosen has none while the others may, or to try again when it could not load by @danilogco
- The red banner of a list that failed to load has a **Try again** button by @danilogco
- **Settings → Text size** makes the text of the app smaller or larger, from 85% to 150%; a few small labels keep their size by @danilogco

### Removed

- The NAMESPACE label beside the namespace box of the lists, which a screen reader still reads by the name of the box by @danilogco

### Fixed

- The buttons that have only an icon (the window controls, the clear button of a search box, the corner of a table, and the others with a tooltip) have a name for a screen reader by @danilogco

### Changed

- `make screenshot` and the preview show the extensions installed on the computer, from a copy of their folder, so the real settings are still never read or written by @danilogco
- The buttons, the selects and the text boxes are smaller (28 px high instead of 36 to 38), so the lists and the pages get more room by @danilogco
- On Linux the tray icon is the light one when the desktop theme is dark, and changes with the theme by @danilogco

## [2.10.0] - 2026-11-25

### Added

- The window that draws its own title bar has smooth rounded corners (10 px), as the windows of the desktop do, except while it fills the screen; without a compositing desktop they are cut with a mask by @danilogco
- The details of an extension have the link to its repository, where it was installed from or where the app offers it
- An extension that is installed and that a newer KubeScope outgrew (`max_app`) or an older one cannot run (`min_app`) is kept but not started, and the app tells once, in a message, which ones and why, instead of skipping them in silence by @danilogco
- An extension can declare the newest version of KubeScope it works with (`max_app` in `kubescope-extension.toml`, such as `2.9.0`): the app refuses to install or update to one made for older apps, and offers the newest version of an extension that is within its range, as `min_app` does for the oldest by @danilogco
- The Helm releases that carry the label `kubescope.dev/chart-repo` (`host_path`) tell the extensions where their chart came from, through `Cluster.helm_chart_repository` by @danilogco

### Fixed

- The pages of the extensions can be pinned to the top bar, with a right-click or two quick clicks on their entry in the side menu, as the lists of the app are by @danilogco
- A pick of more than six items (the log files of a database, for one) has a field that narrows the list as you type
- `Ui.pick_row` shows a table that narrows as you type, by a range of dates and sorts by a click on a header; the log files of a database are picked in it
- The title of Details and Logs names the object, as in `Details: Deployment / api` and `Logs: pod / container`
- The title of a list names its menu group before it, as in `Workloads: Pods`, and the app writes the title of the page of an extension as `Group: Title`, so no extension can break the pattern by @danilogco

## [2.9.0] - 2026-11-25

### Added

- The extensions need no Qt of their own: besides the table, the buttons and the fields, `Ui.components` lends them the page and its layouts, dialogs, the error banner, timers, icons, the panel of notices with the button that counts, the search window, the chat of an assistant (`chat_dock`, `chat_view`), work off the UI thread (`background`) and a test kit (`kubescope.extensions.testing`), and the app translates their texts through `kubescope.sdk.translate` (SDK 1.12), so an extension imports nothing from `PySide6` by @danilogco
- The extensions build their pages with the elements of the app through `Ui.components` (SDK 1.12): the table of the lists, with the check box in its header when asked, the sorting by a click on a header, the badges, the buttons, the search box, the selects and the fields, instead of keeping a copy of each by @danilogco

### Changed

- `make dev` links the extensions of the folders next to the app (`../kubescope-*`) to run from them, and runs with the SDK of `../kubescope-sdk` when it is there, so the app always starts with what is in the checkouts by @danilogco
- The badges of the table are as wide as their column, so they line up, and a text that does not fit is cut with an ellipsis by @danilogco
- The headers of every table, in the app and in the extensions, are centered, and a text that does not fit its cell is cut with an ellipsis instead of wrapped; the texts of the cells stay at the left by @danilogco

## [2.8.0] - 2026-11-24

### Added

- A badge in the middle of the footer says whether the app is read-only (closed padlock) or in the write mode (open padlock), on every page, with the note of the side menu as its tip, and a click on it goes to the Settings, to the choice of the access; the note about it at the foot of the side menu is gone by @danilogco
- The row of a table under the cursor is lit with a soft band, in the tables of the extensions too, and the items of the selects are lit under the cursor by @danilogco
- The list of the context select always opens below it, as wide as the select, in a rounded card with roomy rows by @danilogco
- A ring spreads from the context in the top bar and fades when the context is switched, so the change is seen; it follows the animations of the settings by @danilogco
- What was done (a Pod deleted, a workload scaled), the state of a Pod after it and what an extension finished are told to the notifications with a category (`Ui.show_system_notification(..., category)`, SDK 1.10), so they are kept in the bell and the person chooses which are listed and told; without the notifications extension they are notices of the system as before by @danilogco

### Fixed

- The filters of a list (the namespace, the search and, in the events, the type and the reason) go on to a second row when the window is made narrower, instead of standing over each other by @danilogco

## [2.7.0] - 2026-11-24

### Added

- The **Cluster Plugins** extension (`kubescope-ext-plugins`), recommended in **Settings → Extensions** and not installed by itself: **Installed** lists the add-ons and Helm releases of the cluster with their chart, app and latest versions, the last update and an origin filter, and updates them in the write mode; **Catalog** browses the Helm charts of Artifact Hub by @danilogco
- A page of an extension whose section is **Monitoring** goes into the section of the app, under a group of its own, instead of a section of its own by @danilogco
- `ClusterAccess.environment`, `helm_chart_name`, `eks_target` and `aks_cluster`, `Writes.run_update` (only `aws eks update-addon`, `helm upgrade` and `az k8s-extension update`) and `Writes.run_remove` (only `aws eks delete-addon`, `helm uninstall` and `az k8s-extension delete`), in the write mode, in the SDK 1.9 by @danilogco
- What was done to the cluster (a Pod deleted, a workload scaled or restarted) is told with a notice of the system, and after a Pod is deleted or evicted the app tells when another takes its place and is ready, or that none is yet by @danilogco

### Changed

- The chart and app version of a Helm release are the ones its own Secret says (read in memory, nothing else is kept), not the labels of one of its workloads, and the add-ons list has the chart, the app, the source and the last update of each by @danilogco
- The refresh button of the page of an extension spins for as long as any action of the extension runs, also when the page looks again by itself by @danilogco
- Every table sorts when its header is clicked, and again to reverse it, by what the cells mean (ages by how long they are, numbers by value, versions in order): the nodes, the events of the overview, the forwards, the Pods of a workload, the extensions and their updates by @danilogco
- A table that is loading and has no rows yet shows grey bars where the rows will be, with a band of light that crosses them (the list on screen, the nodes, the events of the overview and the tables of an extension while it acts); the bars stand still when the animations are off, and a table that tried to load and stayed empty says so in the middle (nothing to show, no result for the search, or could not load) by @danilogco
- **Plugins → Installed** and **Plugins → Catalog** leave the app: install the **Cluster Plugins** extension to have them back by @danilogco

## [2.6.1] - 2026-11-24

### Fixed

- The default shortcuts of Services and Settings are Ctrl+Shift+S and Ctrl+Shift+C, so that Ctrl+C keeps copying by @danilogco

## [2.6.0] - 2026-11-24

### Added

- An accessibility statement, `ACCESSIBILITY.md`, with what the app does, what is known to be missing and how to report a barrier, and an issue form for it by @danilogco

### Changed

- Make the Dark and Light themes more opaque, with the page and the top bar at 98% instead of 90%, so what is behind the window shows through less by @danilogco

## [2.5.0] - 2026-11-23

### Added

- An **Extensions** page on the site, in its menu and footer, with an index of the extensions KubeScope recommends, what each does and what it asks for, and a README table with all six by @danilogco
- The extension [`kubescope-ext-custom-resources`](https://github.com/dcotecnologia/kubescope-ext-custom-resources) is recommended in **Settings → Extensions**, as a card to install, and is not installed by default by @danilogco
- Lend the extensions a read and a merge patch (the latter only in the write mode) of the custom resources (CRDs) of a cluster, never of a built-in group by @danilogco
- Let an extension give the side menu pages while the app runs, for entries known only then, such as the custom resources of a cluster by @danilogco
- In the write mode, every list that has an action for many rows (Evict on the Pods, Restart on the Deployments, Delete on all) has a check box in each row and one in the header to check all that show: those actions then act on the ones checked, after one confirmation that names them, and the buttons of one row leave while some are checked, by @danilogco
- Draw a divider between the columns of the tables, so it is easy to see where to drag to resize one by @danilogco
- Right-click the title of a block of the side menu (MONITORING, AWS, ...) and choose **Reorganize** to move it up or down; the order is kept by @danilogco

### Changed

- Show the numbers of the overview (nodes, Pods, CPU, memory and the counts of the workloads) above the details of the cluster and its network by @danilogco

### Fixed

- Give Plugins an icon of its own, a plug, instead of the tiles of Workloads by @danilogco
- Let the columns of the events table of the workloads overview be dragged to resize, which the contents-sized and stretched columns did not allow by @danilogco
- Give each group that extensions add to the side menu an icon of its own, its first letters on a color made from its name, so none repeats by @danilogco
- Indent the entries of the groups that extensions add to the side menu like the groups of the app by @danilogco
- Make the refresh button of the page of an extension spin while it reads and turn green when it is done, as the ones of the app do by @danilogco
- Leave some air above each block of the side menu, except the first one that shows, so the titles do not stick together when they are folded by @danilogco

## [2.4.1] - 2026-11-22

### Fixed

- Set Ctrl+O, Ctrl+P, Ctrl+D, Ctrl+S and Ctrl+C as the default shortcuts for Overview, Pods, Deployments, Services and Settings by @danilogco
- Let the shortcuts table fill the remaining height of the Settings page by @danilogco

## [2.4.0] - 2026-11-22

### Added

- Small icons to follow us on X, Instagram, Facebook and LinkedIn in the **Contribute** card of the welcome page, out of the way of the rest of the app by @danilogco
- Links to our X, Instagram, Facebook and LinkedIn as icons in the footer of the site, with the profiles in its meta tags (`twitter:site`, `rel="me"` and the structured data of the company), and badges in the README by @danilogco
- An extension can declare the oldest version of KubeScope it works with (`min_app` in `kubescope-extension.toml`, such as `2.4.0`): the app refuses to install or update to one that needs a newer app and says to update the app first, and it offers (and installs, for a recommended one) the newest version of an extension that works with the app, reading the manifest of its newest few tags by @danilogco
- An extension is told when the Settings are opened or left (the event `SETTINGS_SHOWN`), so a panel over the pages can step aside by @danilogco
- An extension can ask where the pages are (`Ui.content_area`), to fill them and leave the top bar and the footer as they are, and hide the side menu while it needs the whole width (`Ui.hide_side_menu`); the choice of the person is kept and comes back when the extension lets go or is unloaded by @danilogco

### Changed

- The footer has one item, **Licenses**, in place of **MIT License** and **Third-party licenses**: it opens the window of the licenses, which now starts with the MIT License of KubeScope by @danilogco
- The welcome message is now a page over the middle of the app, between the top bar and the footer, with what is useful to know, the links to contribute, the changelog of the latest release (or of everything since the version you had, after an update); **Settings → General** has an option to show it or not when the app starts (after an update it opens anyway, to tell what is new), and the page can turn it off for good by @danilogco

### Fixed

- A context that is disconnected is no longer listed to the extensions (`ClusterAccess.list_contexts`), so the **Notifications** extension stops reading its events and telling about them by @danilogco

## [2.3.1] - 2026-11-21

### Fixed

- The packages did not meet what the LGPL-3.0 of Qt asks for: the third-party notices now say which Qt version is shipped, link its source code and that of Qt for Python, offer the code on request, say that Qt is not changed and how to replace its libraries in each kind of package, and that nothing in the license of KubeScope limits those rights; the license texts of Qt and Python are files of their own in the `licenses` folder of the bundles, the Windows installer shows a notice about Qt before it installs, the Debian `copyright` file declares Qt under the LGPL-3, and the README has a section about it by @danilogco
- The third-party notices left out what the other licenses ask for: the credit that the FreeType License wants for the FreeType inside Qt and where to read the notices of the other projects built into Qt, where the source code of certifi is (Mozilla Public License 2.0), the AppImage runtime, the Microsoft Visual C++ runtime on Windows, where the colors of the themes come from and the licenses of the extensions that ship with the app by @danilogco
- The third-party notices could only be opened by handing the file to the system, which may have no program for it: the **Third-party notices** button of the About box now opens them in a window of the app, with a list of the components, a filter and the text of the one chosen, and a **Third-party licenses** link in the footer opens it too by @danilogco

## [2.3.0] - 2026-11-21

### Added

- **Settings → Kube → Contexts** (before, *Context names*) has a **Connected** column to connect or disconnect each context: one that is not connected is left out of the selector in the top bar, and the choice is kept; if the one in use is disconnected the app moves to another by @danilogco
- With no context in the kubeconfig, or none of them connected, the side menu, its button and the selector of contexts go away and the **Kube** section of the Settings opens, to add a kubeconfig file or connect a context by @danilogco

### Changed

- The word **CONTEXT** over the context selector in the top bar is gone: the selector says what it is by itself by @danilogco

### Fixed

- The four buttons of the welcome message look alike (outlined), where two of them were filled and two outlined by @danilogco
- The update button in the top bar, its menu and the tray menu look for newer versions of the extensions too, as the button in **Settings → Extensions** does, and not only for a new version of the app by @danilogco

## [2.2.0] - 2026-11-20

### Added

- The extension [`kubescope-notifications`](https://github.com/dcotecnologia/kubescope-notifications) is recommended in **Settings → Extensions**, as a card to install, and is not installed by default by @danilogco
- **Settings → General → Terminal** chooses the terminal that opens for a shell in a Pod, a port-forward or a sign-in that asks for keys: Automatic (the first one the computer has), one of the terminals it finds (gnome-terminal, konsole, alacritty, kitty, wezterm, tilix, foot, ghostty and others on Linux, Windows Terminal and PowerShell on Windows, Terminal and iTerm2 on macOS), or a command line of your own, such as `alacritty -e`; macOS has a terminal now, which it did not before, and the variables a command needs reach it in a script that only you can read and that deletes itself; a choice that is not installed falls back to the first one by @danilogco
- An extension can read the Warning events of the cluster with their identity and times (`ClusterAccess.get_events`) and add a button to the top bar, beside the Settings (`Ui.add_top_bar_button`), which the app takes out when the extension is unloaded by @danilogco
- An extension can list the contexts of the kubeconfig (`ClusterAccess.list_contexts`) and show a notification of the operating system, through the tray, whose click brings the window forward (`Ui.show_system_notification`) by @danilogco
- The app tells the extensions about the errors it shows in the banner (except a failed sign-in, which the banner already says), the warnings and errors of its message boxes and a new version of KubeScope (the event `notification`, which now names the context in use), so an extension can list them by @danilogco

### Changed

- The groups of the side menu that extensions add (like RDS, under AWS) look as the ones of the app do: an icon and an arrow at the header, which folds the group, and the entries indented under a line by @danilogco
- The gear in the top bar opens the Settings and, on the Settings, takes you back to the page you came from when clicked again, as the bell does with its panel by @danilogco
- The title of a block of the side menu (MONITORING, AWS, ...) folds the whole block when clicked and brings it back when clicked again, with the arrow of the entries that fold; the blocks you fold stay folded the next time you open the app, and a screen reached by a shortcut unfolds its block by @danilogco
- The card of each section of the Settings goes down to the bottom of the page instead of stopping under what is in it, and the table of the extensions grows with it by @danilogco
- A button at the start of the page header hides the side menu, which slides away toward the left, and brings it back when clicked again; it stays as you left it the next time you open the app by @danilogco
- The app icon has slightly rounded corners and a small margin, so it sits at the same size as the other icons in the launcher and the dock, with a soft sheen and edge; the tray icon is a tighter version of it, to fill its small slot by @danilogco
- The **Sign in** button in the top bar just says **Sign in**, with no cloud or profile name; the status bar still says which one by @danilogco
- Removed `make windows` and the Wine tooling (`tools/windows_wine.py`): the Windows installer and zip are built only by the Release workflow, which `make windows-remote` runs from here by @danilogco

## [2.1.0] - 2026-11-20

### Added

- The color themes besides Light and Dark leave the app and are the extension `kubescope-themes`, installed by default like Gabi: they show in **Settings → Theme** as before, and an extension can now offer themes (`add_theme`, with the permission `ui.theme`); a theme you chose is put on as soon as the extension has run, and the default is used if it is uninstalled by @danilogco; the copies of those themes that older versions put in your themes folder are removed at the start when you never edited them, so they show only while the extension is installed
- An installed extension keeps only what runs (its manifest, code, translations, README and LICENSE): its tests, pipeline, tooling and project documents are left out, and the ones installed whole by an earlier version are cleaned at the start; the sha256 shown is still that of everything that was downloaded, and an extension run from the folder of its author is never touched by @danilogco

### Changed

- The `kubescope-extension.toml` of an extension says what is for production: an optional `production` list of the folders and files at the top of the extension that stay when it is installed. The manifest itself, `LICENSE`, `README.md` and `src` are required (an extension without one is refused) and always stay, and so does `languages` when there is one; everything else not listed is left out by @danilogco

## [2.0.0] - 2026-11-19

### Added

- The extensions installed by default (Gabi and the global search) ship with the app, as the latest release found when it was built, so that a first run installs them without a network; a build made offline has no copy and the app downloads them, and a newer version is suggested later as for any extension by @danilogco
- The extensions download from `codeload.github.com` and read the tags from the feed of the repository on `github.com`, not from the GitHub API, whose limit of 60 anonymous requests an hour a first run could use up (`GitHub answered 403`); what is installed by default is now quiet when GitHub cannot be reached and is tried again at the next start by @danilogco
- The global search is the extension [`kubescope-search`](https://github.com/dcotecnologia/kubescope-search), recommended by the app and installed the first time it runs (`/` and `Ctrl+K` as before, and the keys you chose are kept); it can be uninstalled in **Settings → Extensions**, and an extension can now search the resources of the cluster and read the lists of the side menu by @danilogco
- The global search leaves the app and is the extension `kubescope-search`, installed by default like Gabi: `/` and `Ctrl+K` still open it, the keys you chose are kept, and an extension can now search the resources of the cluster (`search_resources`) and read the lists of the side menu (the command `views`) by @danilogco
- **Settings → Extensions** shows the author and latest available version of recommended extensions that are not installed by @danilogco
- When extensions have a newer version, a window like the one of the app's own updates lists them, from which version to which, and **Update** goes through them one at a time, each shown with its permissions and hash before it replaces the one installed; it shows once for each new version, and the **Update...** button of **Settings → Extensions** opens it again by @danilogco
- The README, CONTRIBUTING and AGENTS point to the SDK and to the extensions (Gabi and AWS), each a project of its own with a pipeline of tests and releases, and the README has a section on extensions by @danilogco
- **Settings → Extensions** shows the extensions in a table like the other lists (name, version, status, author, when installed and updated, source and description), with a star on the ones KubeScope recommends, and what can be done with one (Details, Install, Update, Reinstall, Uninstall) is in its right-click menu; a double click opens **Details**, a dialog with a dialog with its id, source, folder, sha256, permissions, commands and any load error by @danilogco
- The app looks for newer versions of the extensions that were installed from GitHub and suggests them: a card says **Update available** with a button to update, a line above the cards counts them, and **Check for updates** looks again. What the app recommends is updated to the version it pins; the other repositories are asked for their tags at most once a day, only while the check for updates is on in the Settings, and a new version is downloaded and reviewed like any install by @danilogco
- The card of an extension in **Settings → Extensions** says, in lowercase, when it was installed and when it was last updated; the app keeps both days and the first one never changes on a reinstall by @danilogco
- A page of an extension can ask for the refresh button of the header of the window, the same as the other pages have, so its own page does not draw one by @danilogco
- The AWS RDS instances page leaves the app and is the extension `kubescope-aws` (**Settings → Extensions → AWS**, recommended and not installed by itself), with the same list, details, logs and Systems Manager forward by @danilogco
- An extension brings its own translations: the JSON files of its `languages` folder are added to the languages of the app while it runs, in contexts of their own that can never replace one of the app by @danilogco
- An extension can show details in a tab, open a text as a log with a refresh button, ask the person to pick an item, and, with the permission `forward` and only in the write mode, start the port forward to a database through AWS Systems Manager, which the app checks is that command and nothing else by @danilogco
- An extension can read the AWS account of a cluster context (permission `aws.read`): only commands of `rds`, `ec2`, `eks` and `ssm` that read are run, with the profile or keys of the context, and never one that changes something, reveals a secret or moves the request to another account, region or server by @danilogco
- An extension can add a page to the side menu, in a section and a group of its own (with the permission `ui.page`), shown only while the extension says it should, which is what lets features like the AWS RDS instances leave the app and become extensions by @danilogco
- Extensions the app recommends, such as Gabi, show in **Settings → Extensions** with a star and an Install button; each is the latest release of its repository (its highest final tag, found on GitHub), not a fixed version, and the first time the app runs it installs Gabi once, without a dialog, so that she is there by default and can be uninstalled by @danilogco
- The SDK that extensions are written against, a project of its own (`kubescope-sdk`) that the app depends on: events, named commands, the contributions of an extension to the window, the settings of each extension, and the cluster read paths and writes behind the permissions its manifest asks for by @danilogco
- The code behind installing extensions from a folder or a GitHub repository by their `kubescope-extension.toml`, uninstalling and reinstalling them, running one from its own folder in development mode and reloading it when its files change, with what is copied under strict limits and the manifest checked before anything of it runs by @danilogco
- **Settings → Extensions** shows a card for each extension and installs one from a folder (pick its `kubescope-extension.toml`) or a GitHub repository after a dialog shows where it comes from, its permissions and its sha256, with a development mode that runs the folder in place, and uninstalls and reinstalls them; Gabi, which ships with the app, can be uninstalled and reinstalled there by @danilogco
- Extensions installed from Settings run in the app without restarting it: they hear the context, the theme, the language and the shutdown, they can use the window, the settings of their own and the commands of the window, and one that fails to load shows why on its card without stopping the others by @danilogco
- An extension can add keyboard shortcuts, which show in the shortcuts of the Settings and can be changed there, and sections of its own to the Settings, saved with the rest; one that runs from its own folder (development mode) is reloaded when its files change by @danilogco
- An extension can add commands to `kubescope`, named in its manifest so that the app knows them without running it: the app sets the cluster up as configured, runs only that extension with no window, lends it the choice of a context and the confirmation of the terminal, and unloads it by @danilogco
- **Changed:** Gabi, the assistant, is an extension of its own project (`kubescope-gabi`), installed from **Settings → Extensions**: her chat, her section of the Settings, her shortcut and the command `chat` are hers, and what the app kept for her (the preferences, the consent, the size of the panel and the key of her shortcut) moves under her id the first time the settings are read by @danilogco

### Changed

- The README and the site put Gabi, the Kubernetes assistant, in the foreground with examples of her investigation, navigation, attachments and safeguards by @danilogco

## [1.12.0] - 2026-11-18

### Added

- On Windows the frameless window resizes from its own edge, with the system's shadow, border and rounded corners, instead of a strip drawn by KubeScope by @danilogco

### Changed

- The README and the site show the Deployments list, the resource details and the Pod logs besides the overview by @danilogco

### Fixed

- The generated-ui hook no longer needs `sh`, which Windows does not have: a Python script regenerates the ui files on every platform by @danilogco
- Line endings are normalized to LF with a `.gitattributes` file, so tools on Windows no longer show whole files as changed by @danilogco

## [1.11.0] - 2026-11-17

### Added

- **macOS Light** and **macOS Dark** themes: the system colors of macOS (system blue accent, the grays of the window and the controls, the system green, orange and red for the states), with a translucent window, page and top bar by @danilogco
- Themes can have an `opacity` object that makes the color of a role translucent, with a slider and a number box for each role in the theme editor by @danilogco

## [1.10.0] - 2026-11-16

### Added

- **Plugins** menu with **Catalog** and **Installed**. The Catalog lists the Helm charts of Artifact Hub as cards (search, **Learn More**, **Install**); **Install** shows the `helm` commands to copy and run, KubeScope installs nothing by @danilogco
- **Plugins → Installed** has an **Update** button in the write mode: an EKS add-on is moved to a version EKS offers, with the rule for the fields changed by hand, and a Helm release is upgraded with a chart, repository, version and values file; the exact `aws eks update-addon` or `helm upgrade` command is shown and runs only when you press **Update** by @danilogco
- **Plugins → Installed** has a **Latest** column: for an EKS add-on the newest version EKS offers for the cluster's Kubernetes version, for a Helm release the version of the chart of the same name at Artifact Hub (the official or verified publisher first, so it is the best match, not a certainty). A row with a newer version shows an icon, and **Update** offers that version first by @danilogco
- **Plugins → Installed** also lists the managed extensions of an AKS cluster (version and **Update**, with `az k8s-extension`, the cluster found by the address of its API server) and the add-ons of a GKE cluster (on or off, from `gcloud container clusters describe`, the cluster named by its context); a GKE add-on has no version, so no **Update** by @danilogco

### Changed

- **Add-ons** left the Config menu: the Helm releases and EKS add-ons it listed are now **Plugins → Installed** by @danilogco

## [1.9.1] - 2026-11-13

### Fixed

- Gabi reads a log of a window of time that it always asks for, from how many minutes ago (`since_minutes`, and `until_minutes` to end it earlier) or from a date and time with its time zone (`since` and `until`), the whole window and not only the last lines, with `search` to keep the lines with some terms; an answer that is too long stops and says where, to ask again from there, and it is told the range of every number of an action (it asked for 5000 lines when the limit was 500). When it asks for two reads at once both are made, instead of only the first by @danilogco
- Gabi reads a log that is short enough for one answer whole, with no window to ask for; the window (`since_minutes` or `since`) is asked only for a longer one by @danilogco

## [1.9.0] - 2026-11-12

### Added

- The **Shell command** dialog of a Pod has an **Open in terminal** button that opens the terminal of the system already in the container, and a node of the Node Groups list has a **Shell (SSM)** entry that opens a shell on its EC2 instance through AWS Systems Manager, in the terminal of the system by @danilogco
- **Forward** dialogs (Service, Pod, StatefulSet and RDS) have a **Run in KubeScope** button: the forward runs from the app and is listed on the new **Forwards** page of the side menu, with its status (starting, running, failed or stopped) and a **Stop** button; they all stop when the app quits, and the ones left running by an app that died or was restarted are listed again by @danilogco
- **Forward with SSM** on an RDS instance builds the `aws ssm start-session` command for a port of the database through an EC2 instance of the VPC, already filled with the instance, the region and the profile by @danilogco
- The **RDS instances** page has a **Region** select, which starts in the region of the selected context, to look for the instances of the account in another region by @danilogco
- **Details** and **Logs** on an RDS instance: everything the AWS CLI says about it, and the end of any of its log files, such as the ones of PostgreSQL, in a Logs tab by @danilogco
- While an AWS account is plugged in, or an AWS SSO profile of this computer is signed in, the side menu has an **AWS** block, under the Kubernetes ones, with **RDS → Instances**: the database instances of every region of your AWS accounts, with engine, version, class, status, storage, Multi-AZ, region, account and endpoint by @danilogco

### Changed

- The errors of `kubectl`, the AWS CLI and the cluster, permissions included, show in a red banner with a short line and the original text one click away (**Details**), at the top of the window and above the table of the RDS instances, instead of dialogs and of a line of the status bar by @danilogco
- Ages show seconds only while they are under a minute, and then their two biggest units (`22m`, `4h4m`, `3d4h`), with days (`d`) and years (`a`) when they are that old by @danilogco

## [1.8.0] - 2026-11-11

### Added

- **Settings** has an **Integrations** section, in the style of Lens, to plug the clusters of AWS (EKS), Azure (AKS) and Google Cloud (GKE) with as many accounts as you like: an AWS profile or keys, found and added from a dialog; the secret keys stay in memory until the app quits and the clusters go to a kubeconfig of KubeScope for each account, apart from yours by @danilogco
- Every dialog and window of the app gets the title bar of the main window, while the app is set to draw its own, instead of the one of the system by @danilogco
- The check boxes are a visible box, filled with a tick when on and empty when off, so it is clear at a glance what is active by @danilogco
- The side menu shows an arrow on the groups that have entries under them and a line along those entries, which are closer together by @danilogco

## [1.7.0] - 2026-11-10

### Added

- Paste (`Ctrl+V`) into the chat of the assistant to attach a picture, files copied from a file manager or a long text; each shows as a card above the message field and as a pill (picture, name and size) in the sent message, and a click on either opens it by @danilogco
- **Settings** has a **Shortcuts** section to choose the keys of refresh, the global search, the assistant, the main screens, the filter of the list and the cluster switch, with keys like Headlamp's (`G` then `P` for Pods, `?` for the list), and to turn one off by @danilogco
- **Global search**: press `/` (or `Ctrl+K`) to find a screen, a setting or a resource of any namespace by its name, and open it by @danilogco
- **Settings** has a **Time zone** option to show dates and times in the zone you prefer; the default is the local time of the computer by @danilogco

## [1.6.0] - 2026-11-04

### Added

- `kubescope chat` (or `kubescope assistant`) opens a conversation with Gabi on the terminal, with the same program, reads and limits as the chat of the window, or asks one question and leaves when you give it words; on a terminal the answer is in color (bold, code, headings, lists and code blocks) and the line can be edited, and `NO_COLOR` turns the colors off by @danilogco
- `kubescope help` lists the commands and `kubescope help COMMAND` shows the options of one by @danilogco
- `kubescope` works as a command line for the cluster: `contexts`, `pods`, `workloads`, `nodes`, `events`, `get KIND NAME` and `logs POD` read what the window shows (`-o json` and `-o yaml` for scripts), and without `--context` it asks which context on a terminal by @danilogco
- `kubescope login --context NAME` (also `kubescope auth`) signs in to a context (AWS SSO or access keys, Google Cloud, Azure, or the command set in Settings) on the terminal, and a command that fails for an expired sign-in points to it by @danilogco
- `kubescope delete`, `evict`, `scale` and `restart` change a cluster from the terminal, only while the write mode is on, and ask for confirmation unless `--yes` is given by @danilogco

## [1.5.0] - 2026-11-04

### Added

- The details of a resource have a **Raw YAML** button next to **Raw JSON**; the search and **Save to a file** use the one shown, and the file is a `.yaml` by @danilogco
- The Release workflow builds a macOS app (`KubeScope.app` in a zip) for Apple silicon (`macos-14`) and Intel (`macos-15-intel`) by @danilogco
- The download buttons of the site, the install page and the installation guide list every package of the latest release, macOS and snap included by @danilogco
- `make docker-build` builds the `.deb` and the AppImage in a clean Ubuntu 22.04 container with Docker Compose, so only Docker is needed, and `make docker-flatpak` builds the Flatpak the same way, only when asked by @danilogco
- The AppImage carries update information and the release has its `.zsync` file, so AppImageUpdate downloads only what changed by @danilogco
- The guides are pages of the site (`/guides/`) and no longer send you to the GitHub wiki, and the security policy, the contributing guide and the commit guidelines are pages of the site too by @danilogco

### Fixed

- Starting a second KubeScope no longer prints `QAbstractSocket::waitForBytesWritten() is not allowed in UnconnectedState` by @danilogco

### Changed

- The Flatpak is not built or published with the releases for now, because its runtime has Python 3.13 and the app needs 3.15 by @danilogco

## [1.4.0] - 2026-11-02

### Added

- **Settings** has three sections: General, Kube (the kubeconfig files, the sign-in commands and the names of the contexts) and Assistant, and the guide of the assistant opens the last by @danilogco
- A context without a name of its own shows the end of its name, such as `shop-eks-hml-us-east-1` for the ARN of a cluster, in the list of contexts and in Settings by @danilogco
- The refresh buttons turn green with a tick for a moment when a reload ends well by @danilogco
- A computer set to Portuguese of Portugal (or to any territory the app has no translation for) reads the translation of the same language, which for Portuguese is the Brazilian one, `pt_BR`; a choice of `pt` saved by an older version still works by @danilogco
- The default English is `en_US`, and a choice of `en` saved by an older version still works by @danilogco
- **Settings** lets you choose the model and the effort each assistant program uses, from what Claude Code and Codex allow by @danilogco
- The header of the assistant says which program, model and effort answer; when none is chosen it shows the ones the program is set to use, and Codex is told them explicitly by @danilogco
- A gear button in the header of the assistant opens the **Assistant** section of Settings by @danilogco
- **/debug** in the chat of the assistant answers, without asking the program, which assistant is in use and all of its configuration: program, file, model, effort, what it allows and the command by @danilogco
- **/kube** (or **/kubectl**) in the chat of the assistant answers, without asking the program, what the computer has for kubectl: its version, the kubeconfig files and the contexts in them, with no token, certificate or server address by @danilogco
- In the chat of the assistant, **Enter** sends the message and **Shift+Enter** goes to the next line by @danilogco
- **Ctrl+G** opens the assistant with the cursor in the chat, and puts it away when the cursor is in it already by @danilogco

### Changed

- Python 3.15 is the only version supported: `requires-python`, the CI, the pre-commit hooks and the documentation say so, and the Windows build installs Python into `Python315` by @danilogco
- Save, cancel and close buttons are only an icon, with the words as a tip by @danilogco

## [1.3.2] - 2026-11-01

### Fixed

- **Quit** in the menu of the tray icon now ends the app when its window is hidden in the tray, which on Windows left it running with the icon still there by @danilogco
- The footer shows the version as `v1.3.2` instead of `Version 1.3.2` by @danilogco

## [1.3.1] - 2026-10-30

### Fixed

- The window no longer freezes with a full list: only an Age or Last seen under a minute counts the seconds live, older ones wait for the next reload by @danilogco
- The Node Groups list is read again in the background like the other lists, so what is added or removed on the cluster shows up by @danilogco

## [1.3.0] - 2026-10-29

### Added

- Gabi reads the live CPU and memory of a Pod, by container, beside what each container asks for and may use, as KubeScope shows them, and the lists she reads carry the use of each Pod and workload, so she no longer sends you to `kubectl top` for what she can read by @danilogco
- **Gabi**, the assistant of DCO Tecnologia and an expert in Kubernetes and KubeScope: a chat in the corner of the window that only talks about Kubernetes and KubeScope, laid out like a phone chat, that asks a coding assistant that is already installed on your computer (Claude Code or Codex) about the cluster, without asking you for credentials or storing any. It sees what you see (the list, the selected row, the open Details or Logs, the numbers of the overviews and the open tabs), reads details, logs, lists and events to look into a problem, answers in the language of the app, and can change the window as you would: go to a list, a page, a tab or the logs of a Pod. A change to the cluster is only a card with **Run**, available with the write mode on; in the read-only mode it has no way to edit, update or delete anything and tells you so when you ask. You can attach images and text files, resize the panel, take it out into a window of its own, and the conversations are kept for each context, without the data that was read. It starts off until you open it and agree, and **Settings** turns it off by @danilogco
- Windows, dialogs and lists rise into place as they first show, and **Settings** can turn it off by @danilogco
- When GitHub limits the update checks, the footer says when to try again by @danilogco
- Gabi asks which container you mean when a Pod or a workload has more than one main container, reads the main one without asking when there is only one, and never takes an init container (a migration, say) unless you ask for it; the lists she reads now show the containers of Pods and workloads by @danilogco
- A guide that opens when there is no Claude Code CLI or Codex CLI on the computer, with a button for the settings and one for the installation guide of each by @danilogco
- The side menu opens with every section open, can be resized by its right edge, and remembers both by @danilogco

### Changed

- The **Light** theme is gray instead of white: the page, the side menu, the tables and the fields use soft grays with firmer borders, and the quiet texts are a step stronger to read on them by @danilogco
- An alpha, a beta or a release candidate now updates to the next pre-release as well as to the stable release that follows it, and never to an older one; a stable installation still updates only to stable releases by @danilogco
- The app updates only to **stable** releases: an alpha, a beta or a release candidate is never offered, and a release candidate is told about its own stable release when it comes by @danilogco
- The update check no longer asks GitHub again when the app starts within an hour of finding that it is up to date, so it spends less of the limit GitHub gives an address by @danilogco

### Fixed

- On Windows, Gabi finds the `claude` and `codex` programs where their installers put them (`%USERPROFILE%\.local\bin`, the Codex folder in `%LOCALAPPDATA%\Programs\OpenAI`, the npm folder) even when the app was started with a shorter path than the terminal's, runs it by its whole name so a `.cmd` file starts, and no console window flashes up when she answers by @danilogco
- On Windows, the sign-in programs of the kubeconfig (such as `aws eks get-token`) no longer open a terminal window each time Gabi, or any list, reads the cluster by @danilogco
- The messages of the chat are no longer cut at the end or squeezed into a narrow bubble: each is as high as its text and as wide as the text needs, up to the room it has by @danilogco

## [1.3.0-rc3] - 2026-10-29

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

[Unreleased]: https://github.com/dcotecnologia/kubescope/compare/v2.10.0...HEAD
[2.10.0]: https://github.com/dcotecnologia/kubescope/compare/v2.9.0...v2.10.0
[2.9.0]: https://github.com/dcotecnologia/kubescope/compare/v2.8.0...v2.9.0
[2.8.0]: https://github.com/dcotecnologia/kubescope/compare/v2.7.0...v2.8.0
[2.7.0]: https://github.com/dcotecnologia/kubescope/compare/v2.6.1...v2.7.0
[2.6.1]: https://github.com/dcotecnologia/kubescope/compare/v2.6.0...v2.6.1
[2.6.0]: https://github.com/dcotecnologia/kubescope/compare/v2.5.0...v2.6.0
[2.5.0]: https://github.com/dcotecnologia/kubescope/compare/v2.4.1...v2.5.0
[2.4.1]: https://github.com/dcotecnologia/kubescope/compare/v2.4.0...v2.4.1
[2.4.0]: https://github.com/dcotecnologia/kubescope/compare/v2.3.1...v2.4.0
[2.3.1]: https://github.com/dcotecnologia/kubescope/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/dcotecnologia/kubescope/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/dcotecnologia/kubescope/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/dcotecnologia/kubescope/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/dcotecnologia/kubescope/compare/v1.12.0...v2.0.0
[1.12.0]: https://github.com/dcotecnologia/kubescope/compare/v1.11.0...v1.12.0
[1.11.0]: https://github.com/dcotecnologia/kubescope/compare/v1.10.0...v1.11.0
[1.10.0]: https://github.com/dcotecnologia/kubescope/compare/v1.9.1...v1.10.0
[1.9.1]: https://github.com/dcotecnologia/kubescope/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.com/dcotecnologia/kubescope/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/dcotecnologia/kubescope/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/dcotecnologia/kubescope/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/dcotecnologia/kubescope/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/dcotecnologia/kubescope/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/dcotecnologia/kubescope/compare/v1.3.2...v1.4.0
[1.3.2]: https://github.com/dcotecnologia/kubescope/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/dcotecnologia/kubescope/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/dcotecnologia/kubescope/compare/v1.3.0-rc3...v1.3.0
[1.3.0-rc3]: https://github.com/dcotecnologia/kubescope/compare/v1.3.0-rc2...v1.3.0-rc3
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
