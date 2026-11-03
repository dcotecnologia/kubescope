#!/bin/sh
# Runs inside the container (see Dockerfile): builds the bundle, the .deb and the
# AppImage from the source mounted in /work, and leaves them in /work/dist.
set -eu

# the virtual environment lives in the container, so it never touches the host's .venv
export UV_PROJECT_ENVIRONMENT=/opt/venv
export UV_PYTHON=3.15
export QT_QPA_PLATFORM=offscreen

uv sync --extra dev --extra build --frozen
uv run python tools/sync_changelog.py
uv run python tools/fetch_linux_qt_libs.py
uv run pyinstaller --noconfirm KubeScope.spec
uv run python tools/bundle_notices.py
uv run python tools/build_deb.py
uv run python tools/build_appimage.py

ls -l dist/*.deb dist/*.AppImage*
