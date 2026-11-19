"""Download the latest release of each extension that KubeScope installs by
default, to ship it with the app, so that a first run needs no network.

The zip and a file with the repository and the tag are written to
`src/kubescope/assets/extensions/`. The build runs this; a failure (no
network) only means the build has no copy and the app downloads the
extensions at its first run.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "kubescope" / "assets" / "extensions"


def bundle(target: Path = TARGET) -> int:
    """Write the copies; the number of extensions that have one."""
    sys.path.insert(0, str(ROOT / "src"))  # the app, from the sources
    from kubescope.extensions.defaults import DEFAULTS
    from kubescope.extensions.github import Repo, download, list_tags
    from kubescope.extensions.updates import latest_tag

    target.mkdir(parents=True, exist_ok=True)
    done = 0
    for one in DEFAULTS:
        if not one.automatic:
            continue
        try:
            tag = one.repo.ref or latest_tag(list_tags(one.repo))
            if tag is None:
                raise ValueError(f"{one.repo.label} has no release yet")
            repo = Repo(one.repo.owner, one.repo.name, tag)
            data = download(repo)
        except Exception as error:
            print(f"bundle_extensions: no copy of {one.id}: {error}", file=sys.stderr)
            continue
        (target / f"{one.id}.zip").write_bytes(data)
        (target / f"{one.id}.json").write_text(
            json.dumps({"repo": f"{repo.owner}/{repo.name}", "tag": tag}) + "\n"
        )
        print(f"bundle_extensions: {one.id} {tag}")
        done += 1
    return done


if __name__ == "__main__":
    sys.exit(0 if bundle() else 1)
