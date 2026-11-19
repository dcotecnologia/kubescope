"""Run a command that an extension added to `kubescope`, in the terminal.

The app knows the commands of an extension from its manifest, so it does
not run code to find out. Once one is asked for, the app sets the
cluster up as the person configured it, runs only the extension that
owns the command, with no window, and gives it the terminal's own
helpers; then it unloads it. No Qt.
"""

import sys
from collections.abc import Sequence

from kubescope.sdk.errors import ClusterError

from kubescope import cli_cluster, cluster, integrations
from kubescope.extensions.cluster_access import ClusterBridge
from kubescope.extensions.context import Host, data_directory
from kubescope.extensions.loader import ExtensionLoader
from kubescope.extensions.store import ExtensionStore, Installed
from kubescope.i18n import language_name, resolve_language
from kubescope.settings import Settings


class TerminalBridge:
    """What the terminal lends to a command (`kubescope.sdk.Cli`)."""

    def choose_context(self, name: str | None) -> str:
        return cli_cluster._context(name)

    def confirm(self, question: str) -> bool:
        return cli_cluster._confirm(question, False)


def owner_of(store: ExtensionStore, command: str) -> Installed | None:
    """The installed extension that adds `command`, if one does."""
    return next(
        (
            one
            for one in store.installed()
            if command in one.manifest.commands
            # the one the app ships is run by the window, not found by its commands
            and not one.bundled
        ),
        None,
    )


def run_command(
    store: ExtensionStore, command: str, arguments: Sequence[str]
) -> int | None:
    """Run `command` with `arguments`; its exit code, or None when no extension
    adds it."""
    owner = owner_of(store, command)
    if owner is None:
        return None
    settings = Settings()
    try:
        integrations.load(settings.integration_accounts)
        cluster.configure(
            settings.kubeconfig_files,
            settings.sign_in_commands,
            integrations.kubeconfig_files(),
        )
    except (ClusterError, ValueError) as error:
        print(f"kubescope: {error}", file=sys.stderr)
        return 1
    host = Host(
        cluster=ClusterBridge(),
        snapshot=lambda: "",
        current_context=lambda: None,
        write_mode=lambda: settings.write_mode,
        settings_data=settings.extension_data,
        save_settings=settings.save,
        language=lambda: settings.language,
        resolved_language=lambda: resolve_language(settings.language),
        language_name=lambda: language_name(settings.language),
        data_directory=data_directory,
        cli=TerminalBridge(),
    )
    loader = ExtensionLoader(host)
    try:
        loaded = loader.load(owner)
        if not loaded.ok:
            print(
                f"kubescope: the extension {owner.manifest.id} could not be loaded: "
                f"{loaded.error}",
                file=sys.stderr,
            )
            return 1
        added = next(
            (
                one
                for one in host.contributions.cli_commands
                if one.extension == owner.manifest.id and one.name == command
            ),
            None,
        )
        if added is None:
            print(
                f"kubescope: the extension {owner.manifest.id} does not run {command}",
                file=sys.stderr,
            )
            return 1
        return added.run(list(arguments))
    finally:
        loader.unload_all()
