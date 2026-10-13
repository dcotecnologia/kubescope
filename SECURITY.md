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
- **It is read-only for now.** The app only sends `GET` requests to the cluster
  (lists, single objects, Pod logs, `/version`, and metrics). Write actions are
  planned, and they will be explicit and confirmed by the user.
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
  project. It sends no identifier, only a `User-Agent` with the app version, and
  GitHub sees your IP address as in any request. It never downloads or installs
  anything; the link opens the release page in your browser. Turn the startup
  check off in Settings.
- **Local settings hold no secrets.** `settings.json` keeps the language, the
  last context, the page and list you were on, context display names, hidden table columns, the pinned lists, and the size
  and position of the window. It lives in your
  user configuration directory (`~/.config/kubescope` on Linux).
- **Logs and resource details are shown on screen.** The app does not write them
  to disk or send them anywhere, not even in the debug log below. The one
  exception is **Save...** in the Details & Logs page: it writes the text of the
  open tab to a file only after you pick where, and the app keeps no copy. Pod
  logs can contain secrets printed by an application, so treat saved files,
  screenshots and recordings with care.
- **No separate `kubectl` is shipped.** The packages bundle the Python
  `kubernetes` library, pinned in `uv.lock`, instead of a downloaded binary.

## The debug log

- **Off by default.** Turn it on in Settings (Debug mode) to write a log file you
  can attach to a bug report. It lives in the `logs` folder next to
  `settings.json` and rotates, so it stays small (about 1 MB, 3 backups).
- **What it records:** which cluster requests and cloud CLI commands ran, how long they
  took and how they ended, the first line of an error, and the app and Qt versions.
  Command lines include context names (often an EKS ARN with the account id) and
  namespaces.
- **What it never records:** Pod logs, resource contents (YAML or JSON), or
  credentials. As a second guard, tokens, passwords, access key ids and similar
  patterns are scrubbed from every line.
- **Read it before sharing**, since scrubbing patterns cannot catch everything.
  The log is never sent anywhere by the app.

## Recommendations for users

- Use a read-only Kubernetes role for the contexts you open in KubeScope.
- Keep `~/.kube/config` private (`chmod 600`) and prefer short-lived credentials
  such as `aws sso login`, `gcloud auth login` or `az login`.
- Install packages only from the project's releases. The install scripts
  (`install.sh` and `install.ps1`) do that: they download only from this project's
  GitHub releases over HTTPS and check each file against the sha256 that GitHub
  publishes before installing it. That catches a damaged or swapped download, and it
  trusts GitHub and this repository.
- The Flatpak can read `~/.kube` (read-only) and `~/.aws`, and has network
  access. It bundles the AWS CLI so EKS contexts can sign in. Review these
  permissions with `flatpak info --show-permissions com.dcotecnologia.KubeScope`.

## Supply chain

- Dependencies are locked in `uv.lock` and CI installs them with `--frozen`.
- The pre-commit hooks include `gitleaks` to catch secrets before they are
  committed, and `actionlint` for the GitHub workflows.
- Releases are built by GitHub Actions from tagged commits.
