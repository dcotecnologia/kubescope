# AGENTS

Guide for agents (human and AI) working in this repository.
Goal: keep the architecture, tests, translations, and commit history consistent.

KubeScope is a desktop viewer for Kubernetes and Amazon EKS, built with
Python 3.12+ and PySide6 (Qt). It talks to the cluster with the official `kubernetes` Python client. It is
read-only by default; the few actions that change a cluster (delete or evict a
Pod, scale or restart a Deployment, and the shell and port-forward commands) exist only behind the write
mode, a user setting that is off by default.

## Project documents

Read the document that covers your task before you start, and follow it. When
two documents disagree, stop and ask instead of picking one.

| Document | Read it when | Rule |
| -------- | ------------ | ---- |
| [COMMITING.md](COMMITING.md) | You write any commit message | Source of truth for the commit format |
| [CONTRIBUTING.md](CONTRIBUTING.md) | You set up, branch, test, or open a PR | The workflow a change goes through |
| [SECURITY.md](SECURITY.md) | You touch credentials, cluster requests, logs, settings, permissions, or packaging | Do not break its guarantees; update it when they change |
| [README.md](README.md) | You change user-facing behavior, requirements, or packaging | Keep it accurate |

## 1) Architecture and responsibilities

Keep the layers separate and the dependency direction one-way
(`window` -> `cluster` -> `models`):

- `src/kubescope/models.py`
  - Plain dataclasses (`Workload`, `PodInfo`, `NodeInfo`, ...), formatters, and sort
    or highlight rules. Pure functions, no Qt and no cluster access.
- `src/kubescope/cluster.py`
  - Everything that talks to the cluster: sends the requests to the API server through
    the `kubernetes` client, parses the JSON, and returns models. No Qt imports.
- `src/kubescope/window.py` and `src/kubescope/views/log_tab.py`
  - Qt widgets and wiring. Blocking cluster calls must run in a worker
    (`RefreshWorker` / `ActionWorker`), never on the UI thread. Show loading
    with the button spinner and the status text, never the busy cursor.
- `src/kubescope/dialogs/` and `src/kubescope/views/`
  - Qt pieces apart from the main window: dialogs (`theme_editor`, `update_dialog`) and tab or widget views (`log_tab`, `widgets`).
- `src/kubescope/utils/`
  - Helpers with no place of their own: `errors`, `diagnostics`, `fonts`, `json_view`, `log_view`, `updates` and `selfupdate`.
- `src/kubescope/utils/crashreport.py` and `src/kubescope/dialogs/crash_dialog.py`
  - The crash report: `utils/crashreport.py` (no Qt) keeps the last INFO records in
    memory, writes a report when an exception escapes and builds the issue link;
    `dialogs/crash_dialog.py` shows the report on the next start. Nothing is sent.
- `src/kubescope/utils/updates.py`
  - The update check against GitHub's public API. No Qt; it never raises.
- `src/kubescope/utils/selfupdate.py` and `src/kubescope/dialogs/update_dialog.py`
  - The confirmed self-update: `utils/selfupdate.py` (no Qt) detects how the app was
    installed, downloads the release file, verifies its sha256 and installs it;
    `dialogs/update_dialog.py` is the dialog and the worker thread that run it.
- `src/kubescope/writes.py`
  - The actions that change a cluster (delete or evict a Pod, scale or restart a Deployment, and the shell and port-forward commands). No Qt; only reachable through the write mode.
- `src/kubescope/settings.py`
  - User preferences stored as JSON; tolerant of missing or damaged files.
- `src/kubescope/i18n.py` and `src/kubescope/languages/`
  - Language selection and the JSON languages: one file per language, with a name, its direction and each English text with its translation.
- `src/kubescope/ui/*.ui`
  - Qt Designer layouts. `ui_*.py` next to them are generated, never edit them by
    hand.
- `tools/`
  - Build and packaging scripts (deb, AppImage, Flatpak, Windows/Wine). `packaging/` holds the static packaging files.
- `tests/`
  - Mirrors `src/kubescope/`: `test_cluster.py`, `test_models.py`,
    `test_settings.py`, `test_window.py`, `test_app.py`, `test_theme.py`.

Golden rule:

- New cluster query or API response parsing -> `cluster.py`
- New data shape, formatter, sort key, or display rule -> `models.py`
- New widget, page, menu, or interaction -> `window.py` and the matching `.ui`
- New preference -> `settings.py` (with a safe default and validation on load)

## 2) Code standards

- Write code that reads like the surrounding code: match its naming, comment
  density, and idioms.
- Target Python 3.12+ (CI runs 3.12 to 3.15; releases are built with 3.15). Do not use APIs deprecated in 3.14.
- Prefer simple functions and dataclasses over class hierarchies. Use classes
  only where Qt requires them (widgets, `QThread` workers).
- Tests are plain `pytest` functions; avoid test classes unless clearly needed.
- Internal code keeps strict contracts (fail fast). Defensive validation belongs at
  the boundaries: API responses, the settings file, and user input.
- Never block the UI thread; long work goes through the existing workers.
- The app is read-only by default. Do not add API calls that change cluster state
  unless the task asks for a write feature. When one does, put it in `writes.py`,
  apart from the read paths in `cluster.py` so those stay obviously safe; show it
  only while `settings.write_mode` is on; and confirm it with the user first.
- Log unexpected errors with `logger.exception(...)` and show the user a clear
  message instead of letting the exception escape a Qt slot.
- Code, comments, identifiers, test names, and commit messages are in English,
  whatever the interface language.

## Logging

- Log with `logging.getLogger(__name__)`. INFO is for milestones a person reading
  a shared log needs (context changed, refresh started and finished, sign-in);
  DEBUG is for detail (each command, its exit code and duration).
- Never log Pod logs, resource contents, kubeconfig data, tokens, or keys. A
  failed command logs only the first line of its error, at DEBUG. Expected cluster
  errors are not logged with a traceback; the window explains them.
- The debug log file is off by default and turned on in Settings; keep new log
  lines safe to share, and update SECURITY.md if what is recorded changes.

## 3) UI and translations

- Edit layouts in the `.ui` files, then run `make ui`. Commit the regenerated
  `ui_*.py` together with the `.ui` (CI fails if they are out of date).
- Every user-visible string goes through `self.tr(...)` (or
  `QCoreApplication.translate(...)` for strings that belong to a `.ui` context), with
  a literal string so Qt can extract it.
- After adding or changing texts, run `make i18n`, fill the translations of every
  language in `languages/<code>.json` (no empty ones), and commit them.
- Kubernetes terms that read the same in the other languages (Pods, Deployments,
  Logs, NAMESPACE) may stay as they are; states such as Pod phases must be
  translated.
- Use `make preview` (fake data, no cluster) to look at UI changes, and
  `make screenshot` to refresh `docs/screenshots/overview.png` when the overview
  changes.
  `make store-screenshots` redraws `docs/screenshots/store/` (every theme, for the
  app stores) when the interface changes.

## 4) Commits: follow COMMITING.md

[COMMITING.md](./COMMITING.md) is the source of truth for commit messages. Read it
before every commit; the points below only reinforce it. For the branch and PR
flow, follow [CONTRIBUTING.md](./CONTRIBUTING.md).

- Use Conventional Commits: `<type>(<optional-scope>): <subject>`.
- Allowed types: `feat`, `fix`, `refactor`, `perf`, `style`, `test`, `docs`,
  `build`, `ops`, `chore`.
- Subject in English, imperative mood, no trailing period (`add`, `fix`, `remove`).
- Use the body to explain why, and the footer for `BREAKING CHANGE:` or `Refs:`.
- One objective per commit. Do not mix refactor, feature, and fix.
- Behavior changes ship with their tests in the same commit.
- Regenerated files (`ui_*.py`) are committed with the source that produced
  them.
- Documentation-only changes use `docs`, never `feat`.
- A version bump also updates `uv.lock` in the same commit.
- The user is the sole author. Never add an AI assistant as co-author, and never
  add attribution trailers such as `Co-Authored-By` to commits or PR descriptions.
- Never commit directly to `main`: create a branch and open a PR, even for small or
  documentation-only changes. Only commit when asked to.
- Before starting work, pull `origin/main` so the branch starts up to date.

Examples:

- `feat(pods): show CPU, memory and restarts columns`
- `fix(cluster): ignore Pod metrics when metrics-server is missing`
- `build(flatpak): package the PyInstaller bundle as a Flatpak`
- `docs: describe the Flatpak build in the README`

## Running checks without freezing the machine

The full test suite (Qt, with coverage) and the type checker are heavy enough to
freeze a developer's computer. Agents follow these rules while they work:

- Never run the whole suite: no `make test`, no `pytest` without arguments. Run
  only the test file of the change:
  `nice -n 19 uv run pytest tests/test_x.py -q --no-cov`.
- Coverage only at the final gate. `--cov` (the required 100%) is the slowest part
  and is left to the human.
- One heavy command at a time. Never run `pytest`, `pyright` and `ruff` one after
  the other without waiting, or in parallel; wait for one to finish before the next.
- Check only what changed: `pyright path/to/file.py` instead of `pyright` on the
  whole project, `ruff check path/to/file.py` instead of `ruff check .`.
- Do not repeat a check when nothing changed since its last run.
- Ask before the full gate. `make test` and `make lint` (section 5) run once, at
  the end, and only after the agent asks for authorization.

## 5) Minimum quality before opening a PR

Run locally and make all of it pass (once, at the end, following the rules above):

- `make lint` (`ruff check` and `ruff format --check`)
- `make test` (pytest, `QT_QPA_PLATFORM=offscreen` on a headless machine)
- `make ui` leaves no diff in `src/kubescope/ui/`
- `make i18n` leaves no empty (untranslated) text in the language files

Requirements:

- The test suite passes. New behavior has tests; bug fixes have a regression test.
- Test coverage stays at 100%. `make test` enforces it (`--cov-fail-under=100`), so
  a change that leaves lines or branches uncovered fails. Cover the code with
  tests; never lower the threshold or widen the coverage omissions to get green.
  Generated `ui_*.py` files are the only omission. A `# pragma: no cover` needs a
  reason, and is for code a test cannot reach, such as an
  `if __name__ == "__main__":` guard.
- Do not introduce `DeprecationWarning` or `PendingDeprecationWarning`. Fix them
  with the recommended API, or update the dependency. Do not hide them with warning
  filters without a documented reason.
- Keep dependencies on their latest stable versions; pin an older one only with a
  documented reason.
- Do not edit generated or vendored output: `ui_*.py`, `vendor/`, `dist/`,
  `build/`, `.wine/`.

## 6) Packaging

- `make build` creates the PyInstaller bundle in `dist/KubeScope`; `make deb` and
  `make appimage` package that bundle. `make flatpak` does not: its manifest builds
  from public sources, as Flathub does, and uses this working tree for the app.
- `install.sh` and `install.ps1` install the files of a GitHub release. The names of
  those files (in `release.yml`, `tools/build_deb.py`, `tools/build_appimage.py` and
  `packaging/windows/kubescope.iss`) are what the scripts look for, so change them
  together; `tests/test_install_script.py` checks the Linux script against a fake
  GitHub API.
- `make windows` builds the Windows zip and installer (in Wine on Linux);
  `make windows-remote` builds them on GitHub Actions.
- Building for another platform replaces `dist/KubeScope`, so run the Linux
  packages and the Windows build one after the other, not at the same time.
- The Flatpak app ID is `com.dcotecnologia.KubeScope`; keep it consistent across the
  manifest, desktop file, metainfo, `tools/build_flatpak.py` and `tools/flathub.py`.
- `python3-kubernetes.json` lists the Python packages of the Kubernetes client for
  the Flatpak; regenerate it with `python tools/flatpak_python_deps.py` whenever
  `uv.lock` changes them.

## 7) Security

Follow [SECURITY.md](SECURITY.md); its guarantees are part of the product.

- Never read, store, print, or log credentials, tokens, kubeconfig contents, or
  secrets. The `kubernetes` client and the credential plugins of the kubeconfig handle authentication.
- Never commit secrets, real cluster names, ARNs, or account IDs; use fake data
  in tests and in `tools/preview.py`. The `gitleaks` hook must pass.
- When `uv.lock` changes the runtime dependencies (or the Qt modules the bundle
  ships), the `third-party-notices` pre-commit hook rewrites
  `src/kubescope/assets/THIRD_PARTY_NOTICES.txt`: stage it and commit again (or run
  `make notices`). A test fails while it is out of date. Keep GPL-only Qt modules out of the bundle.
- Do not add telemetry or network calls of the app's own, beyond the update
  check in `utils/updates.py` (GitHub's public API, sends only the version, can be turned
  off in Settings) and the update the person confirms in `utils/selfupdate.py` (only
  from this project's GitHub releases, over HTTPS, and only with a verified sha256). Cluster traffic goes through the `kubernetes` client only;
  never write to the kubeconfig.
- Keep `settings.json` free of secrets, and validate it on load.
- Build request paths with the encoded names (`_resource_path`), and run programs
  as an argument list, never as a shell string; treat names that come from the
  cluster as untrusted data.
- Keep Pod logs and resource details on screen; do not write them to disk on your
  own. The only exception is the **Save...** button, which writes a tab to a file
  the user picks.
- Do not widen the Flatpak permissions or add dependencies without a reason.
- When a change affects what SECURITY.md describes (a write action, a new
  permission, stored data, a new network call), update SECURITY.md in the same
  pull request.
- If you find a vulnerability while working, report it as SECURITY.md describes;
  do not describe it in a public issue, commit message, or PR.

## 8) Quick checklist for agents

- Identify the layer the change belongs to (`models`, `cluster`, `window`,
  `settings`) and keep it there.
- Keep cluster access read-only unless it is a write action behind the write mode, and off the UI thread.
- Add or update tests next to the code, in English and function-based, and keep
  coverage at 100%.
- Edit the `.ui` and regenerate `ui_*.py`; never hand-edit generated files.
- Wrap new UI text in `tr(...)` and complete the translations of every language.
- Read the documents in the table above that apply, and follow them.
- Check the change against [SECURITY.md](SECURITY.md); update it if the change
  alters what it promises.
- Update README.md and CONTRIBUTING.md when setup, behavior, or packaging changes.
- Run `make lint` and `make test` before finishing.
- Write the commit message following [COMMITING.md](./COMMITING.md), with no
  AI co-author.
- Branch from an up-to-date `origin/main`, never commit to `main` directly, and only
  commit or push when asked.
