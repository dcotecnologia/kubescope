"""Notice when the files of an extension that runs from its author's folder
change.

Polling, so it needs nothing of the system: a scan of a few hundred
small files every second is cheap, and the files of a repository that
are not code (`.git`, a virtual environment, caches) are left out. No
Qt.
"""

import os
from pathlib import Path

from kubescope.extensions.archive import IGNORED

MAX_FILES = 5000  # a folder with more than this is not an extension


class FolderWatcher:
    def __init__(self, root: Path) -> None:
        self.root = root
        self._seen = self._scan()

    def _scan(self) -> dict[str, tuple[int, int]]:
        found: dict[str, tuple[int, int]] = {}
        for folder, names, files in os.walk(self.root, followlinks=False):
            names[:] = [name for name in names if name not in IGNORED]
            for name in files:
                if name.endswith(".pyc"):
                    continue
                path = os.path.join(folder, name)
                try:
                    info = os.stat(path)
                except OSError:  # it went away while we looked
                    continue
                found[path] = (info.st_mtime_ns, info.st_size)
                if len(found) >= MAX_FILES:
                    return found
        return found

    def changed(self) -> bool:
        """Whether a file was added, removed or edited since the last call."""
        now = self._scan()
        different = now != self._seen
        self._seen = now
        return different
