"""Where the extensions live: install, uninstall and reinstall them.

No Qt. An extension comes bundled with the app or is installed from a
zip or a repository into the configuration folder. Installing is two
steps, so the person decides between them: `prepare` unpacks the archive
into a staging folder and reports what it is (its manifest, where it
came from, the sha256 of its content, what it replaces) and `install`
puts it in place. Nothing of an extension runs here.

A bundled extension is part of the app, so uninstalling it only records
that the person does not want it, and reinstalling takes that back.
"""

import hashlib
import json
import logging
import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kubescope.extensions import archive
from kubescope.extensions.manifest import (
    MANIFEST_NAME,
    Manifest,
    ManifestError,
    read_manifest,
)

logger = logging.getLogger(__name__)

REGISTRY = "registry.json"
_ID = re.compile(r"[a-z0-9][a-z0-9_.-]{0,99}")
_SOURCE_MAX = 500
MAX_DEPTH = 3  # folders down, where the manifest is looked for


class StoreError(Exception):
    """What was asked cannot be done; the message says why."""


@dataclass(frozen=True)
class Candidate:
    """An extension unpacked and waiting for the person's decision."""

    manifest: Manifest
    source: str  # "file name.zip" or "github owner/repo@ref"
    sha256: str  # of the archive
    folder: Path  # where it is staged
    replaces: Manifest | None = None  # the version installed now, if any
    content_changed: bool = False  # it replaces one whose sha256 differs
    dev: bool = False  # linked, not copied: `folder` is the author's own


@dataclass(frozen=True)
class Installed:
    manifest: Manifest
    folder: Path
    source: str  # "bundled" for the ones that ship with the app
    sha256: str
    bundled: bool
    dev: bool = False  # run from the author's folder, which is watched


class ExtensionStore:
    def __init__(self, directory: Path, bundled: Path | None = None) -> None:
        self.directory = directory
        self.bundled = bundled
        self._installed: dict[str, dict[str, str]] = {}
        self._removed: set[str] = set()
        self._load()

    # the registry of what was installed and what was removed

    def _load(self) -> None:
        try:
            document: Any = json.loads(
                (self.directory / REGISTRY).read_text(encoding="utf-8")
            )
        except OSError, ValueError:
            return
        if not isinstance(document, dict):
            return
        installed = document.get("installed")
        if isinstance(installed, dict):
            for key, entry in installed.items():
                if (
                    isinstance(key, str)
                    and _ID.fullmatch(key)
                    and isinstance(entry, dict)
                    and isinstance(entry.get("source"), str)
                    and isinstance(entry.get("sha256"), str)
                ):
                    kept = {
                        "source": entry["source"][:_SOURCE_MAX],
                        "sha256": entry["sha256"][:64],
                    }
                    if isinstance(entry.get("path"), str):
                        kept["path"] = entry["path"][:_SOURCE_MAX]
                    self._installed[key] = kept
        removed = document.get("removed")
        if isinstance(removed, list):
            self._removed = {
                one for one in removed if isinstance(one, str) and _ID.fullmatch(one)
            }

    def _save(self) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self.directory / REGISTRY
        temporary = path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(
                {"installed": self._installed, "removed": sorted(self._removed)},
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)

    # what is there

    def _folder(self, extension: str) -> Path:
        return self.directory / "installed" / extension

    def _bundled(self) -> list[Installed]:
        if self.bundled is None or not self.bundled.is_dir():
            return []
        found: list[Installed] = []
        for folder in sorted(self.bundled.iterdir()):
            try:
                manifest = read_manifest(folder)
            except ManifestError:
                continue  # not an extension: a package that has no manifest
            found.append(Installed(manifest, folder, "bundled", "", True))
        return found

    def installed(self) -> list[Installed]:
        """What the app runs: the installed ones, and the bundled ones the
        person did not uninstall and did not replace."""
        found: list[Installed] = []
        for extension, entry in sorted(self._installed.items()):
            folder = Path(entry["path"]) if "path" in entry else self._folder(extension)
            try:
                manifest = read_manifest(folder)
            except ManifestError:
                logger.debug("The extension %s is damaged and is skipped", extension)
                continue
            found.append(
                Installed(
                    manifest,
                    folder,
                    entry["source"],
                    entry["sha256"],
                    False,
                    dev="path" in entry,
                )
            )
        taken = {one.manifest.id for one in found}
        found += [
            one
            for one in self._bundled()
            if one.manifest.id not in self._removed and one.manifest.id not in taken
        ]
        return sorted(found, key=lambda one: one.manifest.id)

    def removed_bundled(self) -> list[Manifest]:
        """The bundled extensions the person uninstalled, to reinstall."""
        return [
            one.manifest
            for one in self._bundled()
            if one.manifest.id in self._removed
            and one.manifest.id not in self._installed
        ]

    def source_of(self, extension: str) -> str:
        """Where an installed extension came from, to fetch it again."""
        entry = self._installed.get(extension)
        if entry is None:
            raise StoreError(f"{extension} was not installed from an archive")
        return entry["source"]

    # install

    def _new_staging(self) -> Path:
        staging = self.directory / "staging" / uuid.uuid4().hex
        staging.mkdir(parents=True)
        return staging

    def _describe(self, staging: Path, digest: str, source: str) -> Candidate:
        root = self._root(staging)
        manifest = read_manifest(root)
        current = next(
            (one for one in self.installed() if one.manifest.id == manifest.id), None
        )
        return Candidate(
            manifest=manifest,
            source=source[:_SOURCE_MAX],
            sha256=digest,
            folder=root,
            replaces=current.manifest if current else None,
            content_changed=bool(
                current and current.sha256 and current.sha256 != digest
            ),
        )

    def prepare(self, data: bytes, source: str) -> Candidate:
        """Unpack `data`, a zip, and say what it is; nothing is installed."""
        staging = self._new_staging()
        try:
            archive.extract(data, staging)
            return self._describe(staging, hashlib.sha256(data).hexdigest(), source)
        except (archive.ArchiveError, ManifestError, StoreError) as error:
            shutil.rmtree(staging, ignore_errors=True)
            raise StoreError(str(error)) from error

    def prepare_folder(self, source: Path) -> Candidate:
        """Copy the folder `source` and say what it is; nothing is installed.

        The manifest is looked for in it, so any folder of the
        repository will do.
        """
        staging = self._new_staging()
        try:
            archive.copy_tree(source, staging)
            return self._describe(
                staging, archive.tree_digest(staging), f"folder {source}"
            )
        except (archive.ArchiveError, ManifestError, StoreError) as error:
            shutil.rmtree(staging, ignore_errors=True)
            raise StoreError(str(error)) from error

    def prepare_link(self, source: Path) -> Candidate:
        """Say what the folder `source` is, to run it from where it is: nothing
        is copied, so the author edits it and the app follows."""
        try:
            root = self._root(source.resolve())
            manifest = read_manifest(root)
        except (ManifestError, StoreError, OSError) as error:
            raise StoreError(str(error)) from error
        current = next(
            (one for one in self.installed() if one.manifest.id == manifest.id), None
        )
        return Candidate(
            manifest=manifest,
            source=f"dev {root}"[:_SOURCE_MAX],
            sha256="",
            folder=root,
            replaces=current.manifest if current else None,
            dev=True,
        )

    @staticmethod
    def _root(staging: Path) -> Path:
        """The folder with the manifest, looked for from the top: the
        shallowest one (a repository has its code in a folder, or in a folder
        of its own)."""
        level = [staging]
        for _ in range(MAX_DEPTH + 1):
            found = [folder for folder in level if (folder / MANIFEST_NAME).is_file()]
            if len(found) == 1:
                return found[0]
            if found:
                raise StoreError(f"There is more than one {MANIFEST_NAME} in it")
            level = [
                child
                for folder in level
                for child in sorted(folder.iterdir())
                if child.is_dir()
                and not child.is_symlink()
                and child.name not in archive.IGNORED
            ]
        raise StoreError(f"There is no {MANIFEST_NAME} in it")

    def _staging_of(self, candidate: Candidate) -> Path:
        """The staging folder of a prepared extension; an error for a folder
        that is not one of ours."""
        base = (self.directory / "staging").resolve()
        try:
            parts = candidate.folder.resolve().relative_to(base).parts
        except ValueError:
            parts = ()
        if not parts:
            raise StoreError("That is not a prepared extension")
        return base / parts[0]

    def install(self, candidate: Candidate) -> Installed:
        """Put a prepared extension in place, replacing the one with its id."""
        extension = candidate.manifest.id
        if not _ID.fullmatch(extension):
            raise StoreError("That is not a valid id")
        if candidate.dev:
            return self._link(candidate)
        staged = self._staging_of(candidate)
        target = self._folder(extension)
        target.parent.mkdir(parents=True, exist_ok=True)
        previous = target.with_name(f"{extension}.old")
        shutil.rmtree(previous, ignore_errors=True)
        if target.exists():
            target.replace(previous)
        candidate.folder.replace(target)
        shutil.rmtree(previous, ignore_errors=True)
        shutil.rmtree(staged, ignore_errors=True)
        self._installed[extension] = {
            "source": candidate.source,
            "sha256": candidate.sha256,
        }
        self._save()
        logger.info(
            "Installed the extension %s %s", extension, candidate.manifest.version
        )
        return Installed(
            candidate.manifest, target, candidate.source, candidate.sha256, False
        )

    def _link(self, candidate: Candidate) -> Installed:
        """Record that an extension runs from the folder of its author."""
        extension = candidate.manifest.id
        if "path" not in self._installed.get(extension, {}):
            shutil.rmtree(self._folder(extension), ignore_errors=True)  # a copy
        self._installed[extension] = {
            "source": candidate.source,
            "sha256": "",
            "path": str(candidate.folder),
        }
        self._save()
        logger.info("Linked the extension %s to %s", extension, candidate.folder)
        return Installed(
            candidate.manifest, candidate.folder, candidate.source, "", False, dev=True
        )

    def discard(self, candidate: Candidate) -> None:
        """Throw away a prepared extension the person declined (the folder of
        one that is linked is the author's, and stays)."""
        if candidate.dev:
            return
        shutil.rmtree(self._staging_of(candidate), ignore_errors=True)

    # uninstall and reinstall

    def uninstall(self, extension: str) -> None:
        """Remove an installed extension; a bundled one is only set aside."""
        if extension in self._installed:
            if "path" not in self._installed[extension]:  # not the author's own
                shutil.rmtree(self._folder(extension), ignore_errors=True)
            del self._installed[extension]
        elif any(one.manifest.id == extension for one in self._bundled()):
            self._removed.add(extension)
        else:
            raise StoreError(f"{extension} is not installed")
        self._save()
        logger.info("Uninstalled the extension %s", extension)

    def restore_bundled(self, extension: str) -> None:
        """Reinstall a bundled extension the person uninstalled."""
        if extension not in self._removed:
            raise StoreError(f"{extension} was not uninstalled")
        self._removed.discard(extension)
        self._save()
        logger.info("Reinstalled the bundled extension %s", extension)
