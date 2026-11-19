import json
import sys
import types
from itertools import count
from pathlib import Path

import pytest
from kubescope.sdk.errors import ClusterError
from kubescope.sdk.paths import config_directory

from kubescope import cli, cli_cluster, cluster, integrations
from kubescope.extensions.manifest import MANIFEST_NAME
from kubescope.extensions.store import ExtensionStore
from kubescope.extensions.terminal import TerminalBridge, owner_of

numbers = count(1)

CODE = """
import terminal_log

RESULT = terminal_log.entries
CTX = []


def run(arguments):
    ctx = CTX[0]
    RESULT.append(("run", arguments, ctx.ui, ctx.cli is not None, ctx.app.write_mode))
    RESULT.append(("names", ctx.app.language_names[:1]))
    ctx.settings.set("seen", ctx.cli.choose_context("given"))
    return 7 if "--fail" in arguments else 0


def activate(ctx):
    CTX.append(ctx)
    ctx.on_unload(lambda: RESULT.append("unloaded"))
    ctx.add_cli_command("COMMAND", run)
"""


def make_extension(
    tmp_path: Path,
    command: str = "hello",
    code: str = CODE,
    permissions: str = '"cli", "ui.window"',
) -> tuple[Path, str, str]:
    number = next(numbers)
    package = f"terminal_ext_{number}"
    extension = f"dco.terminal{number}"
    folder = tmp_path / package
    (folder / package).mkdir(parents=True)
    (folder / package / "__init__.py").write_text(code.replace("COMMAND", command))
    (folder / MANIFEST_NAME).write_text(
        f'id = "{extension}"\nname = "T"\nversion = "1.0.0"\napi = "0"\n'
        f'entry = "{package}:activate"\npermissions = [{permissions}]\n'
        f'commands = ["{command}"]\n'
    )
    return folder, package, extension


def install(folder: Path) -> ExtensionStore:
    store = ExtensionStore(config_directory() / "extensions")
    store.install(store.prepare_link(folder))
    return store


@pytest.fixture(autouse=True)
def log(monkeypatch):
    """Where the extension writes what it saw: a module that is not unloaded
    with it."""
    module = types.ModuleType("terminal_log")
    module.entries = []  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "terminal_log", module)
    return module.entries


@pytest.fixture
def configured(monkeypatch):
    seen: list = []
    monkeypatch.setattr(integrations, "load", lambda accounts: seen.append("load"))
    monkeypatch.setattr(integrations, "kubeconfig_files", lambda: ["/i.yaml"])
    monkeypatch.setattr(cluster, "configure", lambda *a: seen.append(a))
    monkeypatch.setattr(cli_cluster, "_context", lambda name: f"chosen {name}")
    return seen


def test_an_extension_runs_its_command_and_its_exit_code_is_the_one_of_the_terminal(
    tmp_path, configured, log
) -> None:
    folder, package, extension = make_extension(tmp_path)
    install(folder)

    assert cli.run(["hello", "a", "--fail"]) == 7
    assert cli.run(["hello"]) == 0

    assert log[0] == ("run", ["a", "--fail"], None, True, False)
    assert log[1] == ("names", ("English",))  # what the app says of its languages
    assert log[2] == "unloaded"  # it is not kept after the command


def test_the_cluster_is_set_up_as_the_person_configured_it_before_the_command(
    tmp_path, configured
) -> None:
    folder, _, _ = make_extension(tmp_path)
    install(folder)

    cli.run(["hello"])

    assert configured == ["load", ([], {}, ["/i.yaml"])]


def test_the_terminal_lends_the_choice_of_a_context_and_the_preferences_are_kept(
    tmp_path, configured
) -> None:
    folder, _, extension = make_extension(tmp_path)
    install(folder)

    cli.run(["hello"])

    saved = json.loads((config_directory() / "settings.json").read_text())
    assert saved["extensions"][extension] == {"seen": "chosen given"}


def test_the_confirmation_of_the_terminal_is_the_one_of_the_commands_of_the_app(
    monkeypatch,
) -> None:
    asked: list = []
    monkeypatch.setattr(
        cli_cluster,
        "_confirm",
        lambda question, yes: asked.append((question, yes)) or True,
    )

    assert TerminalBridge().confirm("Go on?") is True
    assert asked == [("Go on?", False)]


def test_what_no_extension_adds_opens_the_window(tmp_path) -> None:
    assert cli.run(["-platform", "offscreen"]) is None
    assert cli.run(["nothing"]) is None
    assert cli.run([]) is None


def test_a_command_of_the_app_comes_first(tmp_path, configured, capsys) -> None:
    folder, package, _ = make_extension(tmp_path, command="info")
    install(folder)

    assert cli.run(["info"]) == 0

    assert "KubeScope" in capsys.readouterr().out
    assert package not in sys.modules  # the extension was never run


def test_an_extension_the_app_ships_is_run_by_the_window_not_found_by_its_commands(
    tmp_path,
) -> None:
    shipped = tmp_path / "shipped" / "tool"
    shipped.mkdir(parents=True)
    (shipped / MANIFEST_NAME).write_text(
        'id = "dco.shipped"\nname = "S"\nversion = "1.0.0"\napi = "0"\n'
        'entry = "s:go"\npermissions = ["cli"]\ncommands = ["chat"]\n'
    )
    store = ExtensionStore(config_directory() / "extensions", tmp_path / "shipped")

    assert [one.bundled for one in store.installed()] == [True]
    assert owner_of(store, "chat") is None


def test_an_extension_that_fails_to_load_is_told_and_the_exit_code_is_one(
    tmp_path, configured, capsys
) -> None:
    folder, _, extension = make_extension(
        tmp_path, code="def activate(ctx):\n    raise RuntimeError('boom')\n"
    )
    install(folder)

    assert cli.run(["hello"]) == 1

    assert (
        f"the extension {extension} could not be loaded: boom"
        in capsys.readouterr().err
    )


def test_an_extension_that_does_not_register_the_command_it_declared_is_told(
    tmp_path, configured, capsys
) -> None:
    folder, _, extension = make_extension(
        tmp_path, code="def activate(ctx):\n    pass\n"
    )
    install(folder)

    assert cli.run(["hello"]) == 1

    assert f"the extension {extension} does not run hello" in capsys.readouterr().err


def test_a_cluster_that_cannot_be_set_up_is_told_and_nothing_runs(
    tmp_path, configured, monkeypatch, capsys
) -> None:
    folder, package, _ = make_extension(tmp_path)
    install(folder)

    def broken(accounts):
        raise ClusterError("the accounts are damaged")

    monkeypatch.setattr(integrations, "load", broken)

    assert cli.run(["hello"]) == 1

    assert "kubescope: the accounts are damaged" in capsys.readouterr().err
    assert package not in sys.modules


def test_the_help_of_a_command_of_an_extension_is_its_own(
    tmp_path, configured, log
) -> None:
    folder, package, _ = make_extension(tmp_path)
    install(folder)

    assert cli.run(["help", "hello"]) == 0

    assert log[0][:2] == ("run", ["--help"])
