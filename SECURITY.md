# Security Policy

## Supported versions

KubeScope is young, so only the latest release receives security fixes.

| Version | Supported |
| ------- | --------- |
| latest `0.x` release | Yes |
| anything older | No |

## Reporting a vulnerability

Please do not open a public issue for a security problem.

- Use GitHub's private reporting: **Security → Report a vulnerability** on the
  [repository](https://github.com/dcotecnologia/kubescope/security/advisories/new).
- Or email <danilogcarolino@gmail.com> with the subject `KubeScope security`.

Include what you found, the version and platform (deb, AppImage, Flatpak,
Windows, or source), and the steps to reproduce it. Do not include real
credentials, tokens, or cluster data.

You can expect an acknowledgement within a few days. A fix and a coordinated
disclosure follow once the report is confirmed; you will be credited unless you
prefer otherwise.

## How KubeScope handles sensitive data

- **Cluster access goes through the official Kubernetes Python client.** The app
  uses the `kubernetes` library with the context you chose, and the library reads
  your kubeconfig and runs its credential plugins (for example `aws eks
  get-token`). The app never stores tokens, certificates, or cloud credentials,
  and it never writes the kubeconfig: refreshed credentials are not saved back to
  it. Certificate data that sits inline in a kubeconfig is written by the library
  to a temporary file readable only by you, which is removed when the app quits.
- **It is read-only unless you turn on the write mode.** By default the app only
  sends `GET` requests to the cluster (lists, single objects, Pod logs,
  `/version`, and metrics). **Write mode** is a setting that is off by default
  and is never turned on by the app itself. While it is off, the actions that
  change a cluster are not even shown. While it is on, the right-click menu
  offers: delete a Pod (`DELETE`), evict a Pod (`POST` of an Eviction, which
  respects its disruption budget), scale a Deployment (`PATCH` of its scale),
  restart a Deployment (`PATCH` that stamps the Pod template, as `kubectl rollout
  restart` does). Each of these asks for confirmation first (Cancel is the
  default), uses the credentials of the context you chose,
  and nothing else is ever written: the code for these requests lives apart from
  the read paths, in `writes.py`. The cluster's RBAC still decides: without the
  right, it refuses and the app shows its message. For a shell in a Pod the
  menu only shows the complete `kubectl exec` command (with the context, the
  namespace and the container) for you to copy and run in your own terminal. The
  same goes for **Forward** on a Service, a Pod or a StatefulSet, which shows the
  complete `kubectl port-forward` command for a port it exposes (or its
  containers declare, or a Service that selects it sends to; for that the app
  reads the Services of the namespace) and a local port you pick. The
  app runs neither, and does not need `kubectl`. To show only what you may do,
  the write mode also sends the cluster a `SelfSubjectAccessReview` for each
  action, in the namespace of the selected row. It asks and changes nothing, and
  carries no data of yours besides the namespace.
- **Cluster info, Node Groups and Add-ons use the AWS CLI.** On an Amazon EKS
  context the app also runs `aws eks describe-cluster` (the Cluster info and
  Networking cards of the Overview), `list-nodegroups`, `describe-nodegroup`,
  `list-addons` and `describe-addon`. They only read. The cluster name, region and
  profile come from the sign-in command of your kubeconfig; no credentials are
  read or stored.
- **Helm releases are read from Secret metadata only.** **Add-ons** lists the
  Secrets that carry the label `owner=helm`, asking the API for their metadata
  alone (`PartialObjectMetadataList`), so the data of a Secret, which holds the
  release and its values, is not even sent to the app. Only the labels name,
  status and version are used. The chart and app version of a release come from
  the labels of the Deployments, StatefulSets and DaemonSets it installed, also
  metadata only. It needs `list` on `secrets`.
- **Secret values are never shown.** The Secrets list shows only the type and the
  number of keys. **Details** of a Secret replaces every value in `data` and
  `stringData` with `<redacted>` before it reaches the screen, and drops the
  `last-applied-configuration` annotation, which repeats them. The role you give
  KubeScope still needs `get` and `list` on `secrets`; leave it out if you do not
  want the Secrets list.
- **The sign-in check and button run the cloud CLIs, not the app.** To tell whether
  you are signed in, the app runs `aws sts get-caller-identity` and `aws configure
  get` for the profile your kubeconfig names, and reads that profile from the
  sign-in command of your kubeconfig entry, never its credentials. The **Sign in
  to AWS** button runs `aws sso login` for you to approve in the browser. For an
  access-key profile, **Configure AWS credentials** opens a terminal running `aws
  configure` so you type the keys there. The app never sees, asks for, or stores
  keys or tokens, and it does not change the cluster. For Google Cloud the button
  runs `gcloud auth login`, and for Azure `az login`; both open the browser, and
  the app only reads which sign-in program your kubeconfig names.
- **No telemetry.** The traffic is what the Kubernetes client sends to your
  clusters, plus one optional call of the app's own: the update check. When the
  app starts (and when you press the update icon in the footer) it asks the public
  GitHub API (`api.github.com`, over HTTPS) for the latest release of the
  project, and only a stable release counts: a pre-release (alpha, beta or release
  candidate) is never offered. It sends no identifier, only a `User-Agent` with the app version, and
  GitHub sees your IP address as in any request. Checking never downloads or
  installs anything. Turn the startup check off in Settings.
- **The assistant sends what you ask to a program of your computer.** Gabi, the
  assistant of DCO Tecnologia, is an AI that runs on a coding assistant installed
  on your computer; she tells you so if asked. The chat in the corner does nothing until you open it and agree, once, that what you type
  and attach, and what the assistant reads from the cluster to answer, are sent
  to the program (Claude Code or Codex, installed and signed in on your
  computer, which you choose in Settings) and from it to its service. KubeScope
  does not talk to that service, asks you for no credentials, holds no key for it
  and never sees your sign-in. The program is started with **no tools** (it can
  read no file and run no command), with no saved session and from the temporary
  folder. Claude Code is started with `--tools ""`; Codex with its shell, file
  viewing, plugins, apps, browser and computer tools switched off, a read-only
  sandbox, no web search and without your Codex configuration, because its
  read-only sandbox alone still lets it read any file of the computer. What goes: your questions; the images and text files you attach (a text
  file is read with tokens and keys redacted); a description of what the window
  shows (the list, the selected row, the open Details or Logs, the numbers of the
  overviews, the names of the open tabs); and what the assistant asks the app to
  read: a resource document (Secret values are hidden), the last lines of a Pod
  log, a list or the events. Tokens and keys are redacted from all of it, but
  text an application prints in a log, such as a password in a sentence, can
  still go, so open the chat with care on a cluster whose logs hold secrets. The
  assistant only **asks**: moving the window runs at once, as if you had clicked,
  and a change to the cluster is a card that you run, available only with the
  write mode on, through the same functions and limits as the buttons. **With the
  write mode off (the default) the assistant cannot edit, update, delete, scale,
  restart or evict anything**: it is not even told that those actions exist, one
  it asks for anyway is refused with a note in the chat and no card, and when you
  ask for a change it is told to say plainly that KubeScope is in read-only mode,
  that nothing was changed and that the write mode is in Settings. It reads
  at most five times for a question. **Settings** turns the chat off.
- **The assistant's conversations are kept on your computer.** For each context,
  `assistant_history.json` in the configuration directory holds what you said,
  what the assistant answered and the notes of the app, with tokens and keys
  redacted. It never holds the documents, logs, screens or files that were read
  or attached (only the names of the files). **Clear history** in the chat forgets
  a context and **Settings** forgets every one.
- **Updating is explicit and verified.** Only when you click **Update available**
  and confirm, the app downloads the file of that release from the project's GitHub
  releases (`github.com/dcotecnologia/kubescope/releases/download/`, over HTTPS; a
  redirect away from HTTPS is refused). The file must match the sha256 that GitHub
  publishes for it, or nothing is installed, and a release without a published
  sha256 is not installed by the app. It installs the way the app was installed:
  an AppImage replaces itself; a `.deb` is installed with `apt-get` through
  `pkexec`, so the system asks for your password and the app never sees it; the
  Windows installer runs silently for your user. A Flatpak or a source checkout
  never updates itself.
- **Local settings hold no secrets.** `settings.json` keeps the language, the
  last context, the page and list you were on, context display names, hidden table columns, the pinned lists, the size
  and position of the window, and the size and place of the assistant panel. It lives in your
  user configuration directory (`~/.config/kubescope` on Linux). Next to it, the
  `languages` folder can hold translation files you add, plain text that the app only
  reads as a dictionary of texts.
- **Logs and resource details are shown on screen.** The app does not write them
  to disk or send them anywhere on its own, not even in the debug log below. The
  assistant, when you ask it, sends what it reads to its program, as above. The one
  exception is **Save...** in the Details & Logs page: it writes the text of the
  open tab to a file only after you pick where, and the app keeps no copy. Pod
  logs can contain secrets printed by an application, so treat saved files,
  screenshots and recordings with care.
- **No separate `kubectl` is shipped.** The packages bundle the Python
  `kubernetes` library, pinned in `uv.lock`, instead of a downloaded binary.

## The debug log

- **Off by default.** Turn it on in Settings (Debug mode) to write a log file you
  can attach to a bug report. It lives in the `logs` folder next to
  `settings.json` and rotates, so it stays small (about 1 MB, 3 backups). At startup, a background thread deletes the log and crash
  files not written for 30 days.
- **What it records:** which cluster requests and cloud CLI commands ran, how long they
  took and how they ended, the first line of an error, and the app and Qt versions.
  Command lines include context names (often an EKS ARN with the account id) and
  namespaces. To explain crashes it also records the machine: the Linux
  distribution name and version, the session type and desktop (X11 or Wayland), the
  `QT_*` environment variables, the Qt platform plugin, and where each native
  library (xkbcommon, fontconfig, GLib...) was loaded from, with its path. The
  paths can include your user name. It records the keys that are not text (Ctrl,
  Shift, arrows, shortcuts) and the kind of widget that got them.
- **What it never records:** Pod logs, resource contents (YAML or JSON), the text
  you type (letters, digits and symbols are skipped, so a password typed in a field
  never reaches it), or credentials. As a second guard, tokens, passwords, access key ids and similar
  patterns are scrubbed from every line.
- **Read it before sharing**, since scrubbing patterns cannot catch everything.
  The log is never sent anywhere by the app.

## The crash report

- **Always on, in memory and on your disk only.** Even with Debug mode off, the app
  keeps the last 200 records of level INFO and above (milestones and warnings, such
  as the context you opened or a sign-in check; never the per-request DEBUG detail)
  in memory, and nothing else is written. When an exception escapes unhandled, in
  the main thread or in another one, it writes one file, `crash-report.txt`, in the
  `logs` folder next to `settings.json`, replacing the earlier one. Appending a
  record costs next to nothing, and the text is only built when a report is written.
- **What it holds:** the app, Python, Qt and system versions, the stack trace, the
  **first line** of the error message only (an error from the cluster can quote what
  it was reading), and those recent records, scrubbed like the debug log. They can
  include context names (often an EKS ARN with the account id), namespaces and, in
  the trace, paths with your user name. It never holds Pod logs, resource contents,
  typed text or credentials.
- **Nothing is sent by the app.** On the next start a window shows the report in
  full. **Open an issue on GitHub** opens your browser on the project's new-issue page
  with the start of the report in the address (you read it and press submit there),
  **Copy report** puts it on the clipboard, and **Discard** drops it. The file is
  deleted when the window closes.
- **Read it before sharing**, since scrubbing patterns cannot catch everything.

## Recommendations for users

- Use a read-only Kubernetes role for the contexts you open in KubeScope, and turn
  the write mode on only for the contexts where you want to change things.
- Keep `~/.kube/config` private (`chmod 600`) and prefer short-lived credentials
  such as `aws sso login`, `gcloud auth login` or `az login`.
- Install packages only from the project's releases. The install scripts
  (`install.sh` and `install.ps1`) do that: they download only from this project's
  GitHub releases over HTTPS and check each file against the sha256 that GitHub
  publishes before installing it. That catches a damaged or swapped download, and it
  trusts GitHub and this repository.
- The Flatpak can read `~/.kube` (read-only) and has network access. It carries no
  cloud CLI: it asks the host to run the programs that sign in (`aws`, `gcloud`, `az`,
  `kubelogin`, `oci`...) through `org.freedesktop.Flatpak`, used with
  `flatpak-spawn --host`. That permission lets the app run any program of your
  session outside the sandbox, so the sandbox is not a boundary against the app
  itself. It runs only the programs your kubeconfig names to sign in, and the
  login tools above. Review the permissions with
  `flatpak info --show-permissions com.dcotecnologia.KubeScope`. If you remove that one
  (`flatpak override --user --no-talk-name=org.freedesktop.Flatpak`), no sign-in program
  runs and only kubeconfigs with a token or a certificate of their own work.
- The snap is classic: it has no sandbox and runs with your permissions, like the
  `.deb` and the AppImage, so it can run the sign-in tools of any cloud. Use the
  Flatpak if you want a sandbox.

## Supply chain

- Dependencies are locked in `uv.lock` and CI installs them with `--frozen`.
- The pre-commit hooks include `gitleaks` to catch secrets before they are
  committed, and `actionlint` for the GitHub workflows.
- Releases are built by GitHub Actions from tagged commits.
