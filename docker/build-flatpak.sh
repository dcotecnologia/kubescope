#!/bin/sh
# Runs inside the flatpak container (see Dockerfile): builds the Flatpak from the source
# mounted in /work and leaves it in /work/dist.
set -eu

export UV_PROJECT_ENVIRONMENT=/opt/venv
export UV_PYTHON=3.15
export QT_QPA_PLATFORM=offscreen
# flatpak-builder installs into the user's folder, kept in a volume between builds
export FLATPAK_BUILDER_ARGS="--user"

flatpak remote-add --user --if-not-exists flathub \
  https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user -y --noninteractive flathub \
  org.kde.Platform//6.11 org.kde.Sdk//6.11 io.qt.PySide.BaseApp//6.11

uv sync --extra dev --extra build --frozen
uv run python tools/build_flatpak.py

ls -l dist/*.flatpak
