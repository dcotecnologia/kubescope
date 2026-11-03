# Builds the Linux packages (.deb and AppImage) in a clean Ubuntu 22.04, the same
# base as the Release workflow: the oldest glibc keeps more distros working.
# Use it through docker-compose.yml: `make docker-build`.
FROM ubuntu:22.04 AS linux

ENV DEBIAN_FRONTEND=noninteractive

# dpkg-deb comes with dpkg; the rest are the Qt runtime libraries PyInstaller needs
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl git binutils zsync \
        libegl1 libgl1 libxkbcommon0 libfontconfig1 libdbus-1-3 libglib2.0-0 \
    && apt-get clean

# uv, which then fetches Python 3.15
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# the named volumes of the compose file copy these folders (and their rights) the first
# time, so the user that runs the build, not root, can write in them
RUN mkdir -p /opt/venv /tmp/home /tmp/uv-cache \
    && chmod 777 /opt/venv /tmp/home /tmp/uv-cache

WORKDIR /work
COPY docker/build.sh /usr/local/bin/kubescope-build
RUN chmod +x /usr/local/bin/kubescope-build

CMD ["kubescope-build"]


# The Flatpak build, only for `make docker-flatpak`: Ubuntu 24.04 has a flatpak-builder
# recent enough for the manifest (the Release workflow uses it too).
FROM ubuntu:24.04 AS flatpak

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl git flatpak flatpak-builder elfutils \
        libegl1 libgl1 libxkbcommon0 libfontconfig1 libdbus-1-3 libglib2.0-0 \
    && apt-get clean

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN mkdir -p /opt/venv /tmp/home /tmp/uv-cache \
    && chmod 777 /opt/venv /tmp/home /tmp/uv-cache

WORKDIR /work
COPY docker/build-flatpak.sh /usr/local/bin/kubescope-build-flatpak
RUN chmod +x /usr/local/bin/kubescope-build-flatpak

CMD ["kubescope-build-flatpak"]
