# AGENTS

Guide for agents (human and AI) working in this repository.
Goal: keep the architecture, tests, translations, and commit history consistent.

KubeScope is a read-only desktop viewer for Kubernetes and Amazon EKS, built with
Python 3.12+ and PySide6 (Qt). It shells out to a bundled `kubectl`. It is
read-only for now; that is a current scope limit, not a permanent rule, and write
actions are expected later.

## 1) Architecture and responsibilities

Keep the layers separate and the dependency direction one-way
(`window` -> `cluster` -> `models`):

- `src/kubescope/models.py`
  - Plain dataclasses (`Workload`, `PodInfo`, `NodeInfo`, ...), formatters, and sort
    or highlight rules. Pure functions, no Qt and no kubectl.
- `src/kubescope/cluster.py`
  - Everything that talks to the cluster: runs the bundled `kubectl`, parses its
    JSON, and returns models. No Qt imports.
- `src/kubescope/window.py` and `src/kubescope/log_tab.py`
  - Qt widgets and wiring. Blocking cluster calls must run in a worker
    (`RefreshWorker` / `ActionWorker`), never on the UI thread.
- `src/kubescope/settings.py`
  - User preferences stored as JSON; tolerant of missing or damaged files.
- `src/kubescope/i18n.py` and `src/kubescope/translations/`
  - Language selection and the Qt `.ts` / `.qm` files.
- `src/kubescope/ui/*.ui`
  - Qt Designer layouts. `ui_*.py` next to them are generated, never edit them by
    hand.
- `tools/`
  - Build and packaging scripts (deb, AppImage, Flatpak, Windows/Wine, kubectl
    fetch). `packaging/` holds the static packaging files.
- `tests/`
  - Mirrors `src/kubescope/`: `test_cluster.py`, `test_models.py`,
    `test_settings.py`, `test_window.py`.

Golden rule:

- New cluster query or kubectl parsing -> `cluster.py`
- New data shape, formatter, sort key, or display rule -> `models.py`
- New widget, page, menu, or interaction -> `window.py` and the matching `.ui`
- New preference -> `settings.py` (with a safe default and validation on load)

## 2) Code standards

- Write code that reads like the surrounding code: match its naming, comment
  density, and idioms.
- Target Python 3.12+ (CI also runs 3.14). Do not use APIs deprecated in 3.14.
- Prefer simple functions and dataclasses over class hierarchies. Use classes
  only where Qt requires them (widgets, `QThread` workers).
- Tests are plain `pytest` functions; avoid test classes unless clearly needed.
- Internal code keeps strict contracts (fail fast). Defensive validation belongs at
  the boundaries: kubectl output, the settings file, and user input.
- Never block the UI thread; long work goes through the existing workers.
- The app is read-only for now. Do not add kubectl verbs that change cluster state
  unless the task asks for a write feature. When one does, keep it explicit and
  confirmed by the user, and keep the write logic apart from the read paths in
  `cluster.py` so the read-only parts stay obviously safe.
- Log unexpected errors with `logger.exception(...)` and show the user a clear
  message instead of letting the exception escape a Qt slot.
- Code, comments, identifiers, test names, and commit messages are in English,
  whatever the interface language.

## 3) UI and translations

- Edit layouts in the `.ui` files, then run `make ui`. Commit the regenerated
  `ui_*.py` together with the `.ui` (CI fails if they are out of date).
- Every user-visible string goes through `self.tr(...)` (or
  `QCoreApplication.translate(...)` for strings that belong to a `.ui` context), with
  a literal string so Qt can extract it.
- After adding or changing texts, run `make i18n`, fill the Portuguese translations
  in `kubescope_pt.ts` (no `unfinished` entries), and commit the `.ts` and the
  compiled `.qm`.
- Kubernetes terms that read the same in Portuguese (Pods, Deployments, Logs,
  NAMESPACE) may stay as they are; states such as Pod phases must be translated.
- Use `make preview` (fake data, no cluster) to look at UI changes, and
  `make screenshot` to refresh `docs/screenshots/overview.png` when the overview
  changes.

## 4) Commits: follow COMMITING.md

[COMMITING.md](./COMMITING.md) is the source of truth for commit messages. Read it
before committing; the points below only reinforce it.

- Use Conventional Commits: `<type>(<optional-scope>): <subject>`.
- Allowed types: `feat`, `fix`, `refactor`, `perf`, `style`, `test`, `docs`,
  `build`, `ops`, `chore`.
- Subject in English, imperative mood, no trailing period (`add`, `fix`, `remove`).
- Use the body to explain why, and the footer for `BREAKING CHANGE:` or `Refs:`.
- One objective per commit. Do not mix refactor, feature, and fix.
- Behavior changes ship with their tests in the same commit.
- Regenerated files (`ui_*.py`, `.qm`) are committed with the source that produced
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

## 5) Minimum quality before opening a PR

Run locally and make all of it pass:

- `make lint` (`ruff check` and `ruff format --check`)
- `make test` (pytest, `QT_QPA_PLATFORM=offscreen` on a headless machine)
- `make ui` leaves no diff in `src/kubescope/ui/`
- `make i18n` leaves no `unfinished` translations

Requirements:

- The test suite passes. New behavior has tests; bug fixes have a regression test.
- Do not introduce `DeprecationWarning` or `PendingDeprecationWarning`. Fix them
  with the recommended API, or update the dependency. Do not hide them with warning
  filters without a documented reason.
- Keep dependencies on their latest stable versions; pin an older one only with a
  documented reason.
- Do not edit generated or vendored output: `ui_*.py`, `.qm`, `vendor/`, `dist/`,
  `build/`, `.wine/`.

## 6) Packaging

- `make build` creates the PyInstaller bundle in `dist/KubeScope`; `make deb`,
  `make appimage`, and `make flatpak` package that bundle.
- `make windows` builds the Windows zip and installer (in Wine on Linux);
  `make windows-remote` builds them on GitHub Actions.
- Building for another platform replaces `dist/KubeScope`, so run the Linux
  packages and the Windows build one after the other, not at the same time.
- The Flatpak app ID is `com.dcotecnologia.KubeScope`; keep it consistent across the
  manifest, desktop file, metainfo, and `tools/build_flatpak.py`.

## 7) Quick checklist for agents

- Identify the layer the change belongs to (`models`, `cluster`, `window`,
  `settings`) and keep it there.
- Keep cluster access read-only (until a task says otherwise) and off the UI thread.
- Add or update tests next to the code, in English and function-based.
- Edit the `.ui` and regenerate `ui_*.py`; never hand-edit generated files.
- Wrap new UI text in `tr(...)` and complete the Portuguese translations.
- Run `make lint` and `make test` before finishing.
- Write the commit message following [COMMITING.md](./COMMITING.md), with no
  AI co-author.
- Branch from an up-to-date `origin/main`, never commit to `main` directly, and only
  commit or push when asked.
