"""Run the installed extensions: import the entry point, call `activate(ctx)`.

One extension that fails to load never stops the app or the others: the
error is logged (its first line is kept to show) and whatever the
extension had already added is taken back. An extension is Python from
the person's own disk, installed after a confirmation, and it runs in
the app, so nothing here sandboxes it. No Qt.
"""

import importlib
import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from kubescope.sdk.errors import first_line

from kubescope.extensions.context import ExtensionContext, Host
from kubescope.extensions.store import Installed

logger = logging.getLogger(__name__)


@dataclass
class Loaded:
    installed: Installed
    context: ExtensionContext | None = None
    error: str = ""  # why it did not load; empty when it did

    @property
    def ok(self) -> bool:
        return not self.error


def _roots(folder: Path) -> list[Path]:
    """Where the code of an extension is: its folder, and `src` when it has
    one."""
    src = folder / "src"
    return [folder, src] if src.is_dir() else [folder]


class ExtensionLoader:
    def __init__(self, host: Host) -> None:
        self.host = host
        self.loaded: dict[str, Loaded] = {}

    def load_all(self, installed: list[Installed]) -> list[Loaded]:
        return [self.load(one) for one in installed]

    def load(self, one: Installed) -> Loaded:
        """Import and activate an extension; the result says whether it ran."""
        extension = one.manifest.id
        if extension in self.loaded:
            return self.loaded[extension]
        module_name, _, function = one.manifest.entry.partition(":")
        roots = _roots(one.folder)
        for root in reversed(roots):
            sys.path.insert(0, str(root))
        importlib.invalidate_caches()
        context: ExtensionContext | None = None
        try:
            module = importlib.import_module(module_name)
            if not self._inside(module, roots):
                raise ImportError(
                    f"{module_name} is the name of another package that is loaded"
                )
            activate = getattr(module, function, None)
            if not callable(activate):
                raise ImportError(f"{module_name} has no function {function}")
            context = ExtensionContext(extension, one.manifest.permissions, self.host)
            activate(context)
        except Exception as error:
            logger.exception("The extension %s could not be loaded", extension)
            if context is not None:
                context.close()
            self._forget(roots)
            result = Loaded(one, error=first_line(str(error)) or type(error).__name__)
        else:
            logger.info("Loaded the extension %s %s", extension, one.manifest.version)
            result = Loaded(one, context)
        self.loaded[extension] = result
        return result

    def reload(self, one: Installed) -> Loaded:
        """Unload an extension and load it again from its folder, as the author
        sees it now (the manifest is read again by the caller)."""
        self.unload(one.manifest.id)
        return self.load(one)

    def unload(self, extension: str) -> None:
        """Stop an extension and forget its code; it can be loaded again."""
        result = self.loaded.pop(extension, None)
        if result is None:
            return
        if result.context is not None:
            result.context.close()
        self._forget(_roots(result.installed.folder))
        logger.info("Unloaded the extension %s", extension)

    @staticmethod
    def _inside(module: object, roots: list[Path]) -> bool:
        """Whether the module was imported from the folders of the extension (a
        package without an `__init__.py` has no file, so it is not)."""
        file = getattr(module, "__file__", None)
        return bool(file) and any(
            Path(file).resolve().is_relative_to(root.resolve()) for root in roots
        )

    @staticmethod
    def _forget(roots: list[Path]) -> None:
        for root in roots:
            while str(root) in sys.path:
                sys.path.remove(str(root))
        resolved = [root.resolve() for root in roots]
        for name, module in list(sys.modules.items()):
            file = getattr(module, "__file__", None)
            if file and any(Path(file).resolve().is_relative_to(r) for r in resolved):
                del sys.modules[name]
        importlib.invalidate_caches()
