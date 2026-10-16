#!/bin/sh
# Install or update KubeScope on Linux from the files of its GitHub release.
#
#   curl -fsSL https://raw.githubusercontent.com/dcotecnologia/kubescope/main/install.sh | sh
#
# It picks the latest release (or the one you name), checks the download against
# the sha256 that GitHub publishes for the file, and installs it: the .deb on
# Debian and Ubuntu, the AppImage in your home folder everywhere else. Run it
# again to update. On Windows use install.ps1; there is no macOS package yet.
#
# Options:
#   --version X     install release X (for example 0.1.0) instead of the latest
#   --method M      deb or appimage; the default is deb where apt and sudo exist
#   --force         install even if that version is already installed
#   --dry-run       show what would be done and change nothing
#   -h, --help      show this help
#
# For tests and mirrors: KUBESCOPE_REPO (owner/name) and KUBESCOPE_API (the API
# URL, https only except for localhost).

set -eu

REPO="${KUBESCOPE_REPO:-dcotecnologia/kubescope}"
API="${KUBESCOPE_API:-https://api.github.com}"
VERSION=latest
METHOD=auto
FORCE=0
DRY_RUN=0

say() { printf '%s\n' "$*"; }
die() {
  printf 'install.sh: %s\n' "$*" >&2
  exit 1
}

usage() {
  cat <<'EOF'
Usage: install.sh [options]

Install or update KubeScope from the files of its GitHub release.

Options:
  --version X     install release X (for example 0.1.0) instead of the latest
  --method M      deb or appimage; the default is deb where apt and sudo exist
  --force         install even if that version is already installed
  --dry-run       show what would be done and change nothing
  -h, --help      show this help
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --version) [ $# -ge 2 ] || die "--version needs a value"; VERSION="${2#v}"; shift 2 ;;
    --method) [ $# -ge 2 ] || die "--method needs deb or appimage"; METHOD="$2"; shift 2 ;;
    --force) FORCE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h | --help) usage; exit 0 ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
done
case "$METHOD" in auto | deb | appimage) ;; *) die "--method is deb or appimage" ;; esac

# What this script can install, and where.
case "$(uname -s)" in
  Linux) ;;
  Darwin) die "there is no macOS package yet; run it from source: https://github.com/$REPO/wiki/Building-from-source" ;;
  MINGW* | MSYS* | CYGWIN*) die "on Windows use PowerShell: irm https://raw.githubusercontent.com/$REPO/main/install.ps1 | iex" ;;
  *) die "unsupported system: $(uname -s)" ;;
esac
case "$(uname -m)" in
  x86_64 | amd64) ;;
  *) die "only x86_64 packages are published; this machine is $(uname -m)" ;;
esac

# Downloads go over https; plain http is for a local test server only.
case "$API" in
  https://*) PROTO='=https' ;;
  http://127.0.0.1* | http://localhost*) PROTO='=http,https' ;;
  *) die "KUBESCOPE_API must be an https URL" ;;
esac

if command -v curl >/dev/null 2>&1; then
  fetch() { # fetch URL [FILE]
    if [ $# -ge 2 ]; then
      curl -fL --proto "$PROTO" --tlsv1.2 ${PROGRESS:+"$PROGRESS"} -o "$2" "$1"
    else
      curl -fsSL --proto "$PROTO" --tlsv1.2 "$1"
    fi
  }
elif command -v wget >/dev/null 2>&1; then
  fetch() {
    if [ $# -ge 2 ]; then wget -q -O "$2" "$1"; else wget -q -O - "$1"; fi
  }
else
  die "curl or wget is needed to download the release"
fi
if [ -t 1 ]; then PROGRESS="--progress-bar"; else PROGRESS="-sS"; fi

if command -v sha256sum >/dev/null 2>&1; then
  sha256() { sha256sum "$1" | cut -d' ' -f1; }
elif command -v shasum >/dev/null 2>&1; then
  sha256() { shasum -a 256 "$1" | cut -d' ' -f1; }
else
  die "sha256sum or shasum is needed to check the download"
fi

# Which release.
if [ "$VERSION" = latest ]; then
  RELEASE_URL="$API/repos/$REPO/releases/latest"
else
  RELEASE_URL="$API/repos/$REPO/releases/tags/v$VERSION"
fi
RELEASE=$(fetch "$RELEASE_URL") ||
  die "could not read the release at $RELEASE_URL (does that version exist? is GitHub rate limiting you?)"
TAG=$(printf '%s\n' "$RELEASE" | sed -n 's/^  "tag_name": "\(.*\)",$/\1/p' | head -n 1)
[ -n "$TAG" ] || die "the release has no tag name"
TARGET="${TAG#v}"

# Which method.
have_privileges() { [ "$(id -u)" -eq 0 ] || command -v sudo >/dev/null 2>&1; }
if [ "$METHOD" = auto ]; then
  if command -v dpkg >/dev/null 2>&1 && command -v apt-get >/dev/null 2>&1 && have_privileges; then
    METHOD=deb
  else
    METHOD=appimage
  fi
fi
DATA_DIR="${XDG_DATA_HOME:-${HOME:?HOME is not set}/.local/share}/kubescope"
BIN_DIR="${HOME:?HOME is not set}/.local/bin"
case "$METHOD" in
  deb) ASSET="kubescope_${TARGET}_amd64.deb" ;;
  appimage) ASSET="KubeScope-${TARGET}-x86_64.AppImage" ;;
esac

# What is installed now.
installed_version() {
  if [ "$METHOD" = deb ]; then
    # only a package that is installed counts, not one removed with its settings kept
    status=$(dpkg-query -W -f='${db:Status-Abbrev}|${Version}' kubescope 2>/dev/null || true)
    case "$status" in ii*\|*) printf '%s\n' "${status#*|}" ;; esac
  else
    for file in "$DATA_DIR"/KubeScope-*-x86_64.AppImage; do
      [ -e "$file" ] || continue
      name=${file##*/}
      name=${name#KubeScope-}
      printf '%s\n' "${name%-x86_64.AppImage}"
    done | sort -V | tail -n 1
  fi
}
CURRENT=$(installed_version)

is_newer() { # is_newer A B: A is a later version than B
  [ "$1" != "$2" ] && [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | tail -n 1)" = "$1" ]
}

if [ -n "$CURRENT" ] && [ "$FORCE" -eq 0 ]; then
  if [ "$CURRENT" = "$TARGET" ]; then
    say "KubeScope $CURRENT is already installed and up to date."
    exit 0
  fi
  if [ "$VERSION" = latest ] && is_newer "$CURRENT" "$TARGET"; then
    say "KubeScope $CURRENT is newer than the latest release ($TARGET); nothing to do."
    exit 0
  fi
fi

if [ -n "$CURRENT" ]; then
  say "Updating KubeScope $CURRENT -> $TARGET ($METHOD)."
else
  say "Installing KubeScope $TARGET ($METHOD)."
fi

# Find the file and the sha256 GitHub publishes for it.
URL=$(printf '%s\n' "$RELEASE" |
  sed -n "s|^ *\"browser_download_url\": \"\\(.*/$ASSET\\)\",\\{0,1\\}\$|\\1|p" | head -n 1)
[ -n "$URL" ] || die "release $TAG has no file named $ASSET"
DIGEST=$(printf '%s\n' "$RELEASE" | awk -v want="$ASSET" '
  index($0, "\"name\": \"" want "\"") { found = 1; next }
  found && /"digest":/ { sub(/.*"sha256:/, ""); sub(/".*/, ""); print; exit }')
if [ -z "$DIGEST" ] && [ "${KUBESCOPE_ALLOW_UNVERIFIED:-0}" != 1 ]; then
  die "GitHub gives no sha256 for $ASSET, so the download cannot be checked (set KUBESCOPE_ALLOW_UNVERIFIED=1 to go on anyway)"
fi

say "  file:   $ASSET"
say "  from:   $URL"
say "  sha256: ${DIGEST:-not published}"
if [ "$METHOD" = deb ]; then
  say "  to:     the system, with apt (it may ask for your password)"
else
  say "  to:     $DATA_DIR, linked as $BIN_DIR/kubescope"
fi
if [ "$DRY_RUN" -eq 1 ]; then
  say "Dry run: nothing was downloaded or changed."
  exit 0
fi

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
trap 'exit 1' INT TERM HUP
say "Downloading..."
fetch "$URL" "$TMP/$ASSET" || die "the download failed"
if [ -n "$DIGEST" ]; then
  [ "$(sha256 "$TMP/$ASSET")" = "$DIGEST" ] ||
    die "the sha256 of the download does not match what GitHub published; nothing was installed"
  say "Checked the sha256."
fi

if [ "$METHOD" = deb ]; then
  # mktemp makes the folder private; apt downloads as the _apt user, which must be
  # able to reach the file or it falls back to root with a warning.
  chmod 755 "$TMP"
  chmod 644 "$TMP/$ASSET"
  if [ "$(id -u)" -eq 0 ]; then
    apt-get install -y "$TMP/$ASSET"
  elif command -v sudo >/dev/null 2>&1; then
    sudo apt-get install -y "$TMP/$ASSET"
  else
    die "installing the .deb needs root or sudo; try --method appimage"
  fi
  say "Done. Start it with: kubescope"
else
  mkdir -p "$DATA_DIR" "$BIN_DIR"
  cp "$TMP/$ASSET" "$DATA_DIR/$ASSET"
  chmod 755 "$DATA_DIR/$ASSET"
  ln -sf "$DATA_DIR/$ASSET" "$BIN_DIR/kubescope"
  for old in "$DATA_DIR"/KubeScope-*-x86_64.AppImage; do
    if [ -e "$old" ] && [ "$old" != "$DATA_DIR/$ASSET" ]; then rm -f "$old"; fi
  done
  say "Done. Start it with: kubescope"
  case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) say "Note: $BIN_DIR is not in your PATH; add it, or run $BIN_DIR/kubescope." ;;
  esac
  say "Note: an AppImage needs FUSE 2 (libfuse2); if it will not start, install it."
fi
