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

- **Cluster access goes through `kubectl`.** The app runs the `kubectl` bundled
  with it and passes it the context you chose. It never reads or stores tokens,
  certificates, or cloud credentials itself; `kubectl` and its credential plugins
  (for example `aws eks get-token`) do that.
- **It is read-only for now.** The app only runs read commands (`get`, `config
  get-contexts`, `config view`, `logs`). Write actions are planned, and they will
  be explicit and confirmed by the user.
- **The sign-in check and button run the AWS CLI, not the app.** To tell whether
  you are signed in, the app runs `aws sts get-caller-identity` and `aws configure
  get` for the profile your kubeconfig names, and reads that profile from
  `kubectl config view` without `--raw`, so secrets stay redacted. The **Sign in
  to AWS** button runs `aws sso login` for you to approve in the browser. For an
  access-key profile, **Configure AWS credentials** opens a terminal running `aws
  configure` so you type the keys there. The app never sees, asks for, or stores
  keys or tokens, and it does not change the cluster.
- **No telemetry and no network calls of its own.** The only traffic is what
  `kubectl` sends to your clusters.
- **Local settings hold no secrets.** `settings.json` keeps the language, the
  last context, context display names, and hidden table columns. It lives in your
  user configuration directory (`~/.config/kubescope` on Linux).
- **Logs and resource details are shown on screen only.** They are not written to
  disk or sent anywhere. Pod logs can contain secrets printed by an application,
  so treat screenshots and recordings with care.
- **The bundled `kubectl` is verified.** `tools/fetch_kubectl.py` downloads the
  official stable release and checks its published SHA-256 before PyInstaller
  includes it.

## Recommendations for users

- Use a read-only Kubernetes role for the contexts you open in KubeScope.
- Keep `~/.kube/config` private (`chmod 600`) and prefer short-lived credentials
  such as `aws sso login`.
- Install packages only from the project's releases.
- The Flatpak can read `~/.kube` (read-only) and `~/.aws`, and has network
  access. It bundles the AWS CLI so EKS contexts can sign in. Review these
  permissions with `flatpak info --show-permissions com.dcotecnologia.KubeScope`.

## Supply chain

- Dependencies are locked in `uv.lock` and CI installs them with `--frozen`.
- The pre-commit hooks include `gitleaks` to catch secrets before they are
  committed, and `actionlint` for the GitHub workflows.
- Releases are built by GitHub Actions from tagged commits.
