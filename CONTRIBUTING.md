# Contributing to KubeScope

Thanks for helping. KubeScope is a desktop viewer for Kubernetes and Amazon EKS
written in Python with PySide6. This page gets you from a clone to a pull request;
the details live in two other files:

- [AGENTS.md](AGENTS.md): architecture, code standards, UI and translations,
  packaging, and the quality bar. It applies to people and AI assistants alike.
- [COMMITING.md](COMMITING.md): the commit message format (Conventional Commits).

## Set up

```bash
git clone https://github.com/dcotecnologia/kubescope.git
cd kubescope
make setup          # uv sync with the dev and build extras
uv run pre-commit install
python tools/fetch_kubectl.py
```

Run the app against a cluster with `make run`, or without any cluster using fake
data with `make preview`.

## Workflow

1. Pull the latest `main` and create a branch. Do not commit to `main` directly.
2. Make one focused change per commit, with its tests.
3. Run the checks below.
4. Open a pull request that says what changed and why. Link the issue if there is
   one.

## Checks

```bash
make lint     # ruff
make test     # pytest, must stay at 100% coverage (headless: QT_QPA_PLATFORM=offscreen)
uv run pre-commit run --all-files
make ui       # leaves no diff in src/kubescope/ui
make i18n     # leaves no unfinished Portuguese translations
```

CI runs the same pre-commit hooks, the generated-UI check, and the tests on
Python 3.12 and 3.14. A pull request must be green.

## Commit messages

Follow [COMMITING.md](COMMITING.md):

```text
feat(pods): show CPU, memory and restarts columns
fix(cluster): ignore Pod metrics when metrics-server is missing
docs: describe the Flatpak build in the README
```

English, imperative mood, no trailing period, and no AI assistant as co-author.

## Where changes go

| Change | Place |
| ------ | ----- |
| Cluster queries and kubectl parsing | `src/kubescope/cluster.py` |
| Data shapes, formatters, sort and highlight rules | `src/kubescope/models.py` |
| Widgets, pages and interactions | `src/kubescope/window.py` and the `.ui` files |
| Preferences | `src/kubescope/settings.py` |
| Friendly error messages | `src/kubescope/errors.py` |
| Colors, themes and the theme editor | `src/kubescope/theme.py`, `theme_editor.py` |
| A theme to share with everyone | `src/kubescope/community_themes/` (see its README) |

Edit layouts in the `.ui` files and run `make ui`; never edit `ui_*.py` by hand.
Wrap user-visible text in `self.tr(...)` and complete the Portuguese
translations with `make i18n`.

## Security

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md), not
in a public issue.

## License

By contributing you agree that your work is released under the [MIT License](LICENSE).
