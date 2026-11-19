import logging
import sys
from pathlib import Path

import pytest

from kubescope.extensions.context import Host
from kubescope.extensions.loader import ExtensionLoader
from kubescope.extensions.manifest import Manifest
from kubescope.extensions.store import Installed
from kubescope.sdk import CONTEXT_CHANGED

counter = iter(range(1, 1000))


class FakeCluster:
    def __getattr__(self, name: str):
        return lambda *arguments: (name, arguments)


def make_host() -> Host:
    return Host(
        cluster=FakeCluster(),
        snapshot=lambda: "screen",
        current_context=lambda: "dev",
        write_mode=lambda: False,
        settings_data=lambda name: {},
        save_settings=lambda: None,
    )


def make_extension(
    tmp_path: Path,
    code: str,
    permissions=("ui.dock",),
    entry_function: str = "activate",
    layout: str = "flat",
) -> tuple[Installed, str]:
    """An extension on disk whose package has a name nobody else has."""
    package = f"ext_pkg_{next(counter)}"
    folder = tmp_path / package
    base = folder / "src" if layout == "src" else folder
    (base / package).mkdir(parents=True)
    (base / package / "__init__.py").write_text(code)
    manifest = Manifest(
        f"dco.{package.replace('_', '-')}",
        "Test",
        "1.0.0",
        f"{package}:{entry_function}",
        frozenset(permissions),
    )
    return Installed(manifest, folder, "file x.zip", "", False), package


GOOD = """
def activate(ctx):
    ctx.add_dock("chat", object)
    ctx.events.on("context_changed", lambda context: HEARD.append(context))

HEARD = []
"""


def test_an_extension_is_imported_and_activated_with_its_context(tmp_path) -> None:
    host = make_host()
    one, package = make_extension(tmp_path, GOOD)

    loaded = ExtensionLoader(host).load(one)

    assert loaded.ok and loaded.error == ""
    assert loaded.context is not None and loaded.context.id == one.manifest.id
    assert [d.key for d in host.contributions.docks] == ["chat"]
    host.events.emit(CONTEXT_CHANGED, context="prod")
    assert sys.modules[package].HEARD == ["prod"]
    ExtensionLoader(host).unload("nothing")  # unloading what is not loaded is harmless


def test_the_code_may_be_in_a_src_folder(tmp_path) -> None:
    host = make_host()
    one, _ = make_extension(tmp_path, GOOD, layout="src")

    assert ExtensionLoader(host).load(one).ok


def test_loading_twice_gives_the_same_result(tmp_path) -> None:
    host = make_host()
    loader = ExtensionLoader(host)
    one, _ = make_extension(tmp_path, GOOD)

    assert loader.load(one) is loader.load(one)
    assert len(host.contributions.docks) == 1


def test_unloading_stops_everything_the_extension_did(tmp_path) -> None:
    host = make_host()
    loader = ExtensionLoader(host)
    one, package = make_extension(tmp_path, GOOD)
    loader.load(one)

    loader.unload(one.manifest.id)

    assert host.contributions.docks == []
    assert package not in sys.modules
    assert str(one.folder) not in sys.path
    assert one.manifest.id not in loader.loaded
    host.events.emit(CONTEXT_CHANGED, context="after")  # nobody is listening
    assert loader.load(one).ok  # and it can come back


def test_an_extension_that_raises_is_isolated_and_cleaned_up(tmp_path, caplog) -> None:
    host = make_host()
    loader = ExtensionLoader(host)
    broken, package = make_extension(
        tmp_path,
        "def activate(ctx):\n"
        "    ctx.add_dock('half', object)\n"
        "    raise RuntimeError('boom\\nsecond line')\n",
    )
    good, _ = make_extension(tmp_path, GOOD)

    with caplog.at_level(logging.ERROR):
        results = loader.load_all([broken, good])

    assert [r.ok for r in results] == [False, True]
    assert results[0].error == "boom"
    assert results[0].context is None
    assert [d.key for d in host.contributions.docks] == ["chat"]  # not "half"
    assert package not in sys.modules and str(broken.folder) not in sys.path
    assert "could not be loaded" in caplog.text


def test_an_error_without_a_message_names_its_type(tmp_path) -> None:
    one, _ = make_extension(tmp_path, "def activate(ctx):\n    raise KeyError()\n")

    assert ExtensionLoader(make_host()).load(one).error == "KeyError"


def test_a_missing_permission_fails_the_extension_only(tmp_path) -> None:
    one, _ = make_extension(tmp_path, GOOD, permissions=())

    loaded = ExtensionLoader(make_host()).load(one)

    assert not loaded.ok and "did not ask for ui.dock" in loaded.error


def test_a_module_that_does_not_import_is_isolated(tmp_path) -> None:
    one, _ = make_extension(tmp_path, "import module_that_is_not_there\n")

    assert "module_that_is_not_there" in ExtensionLoader(make_host()).load(one).error


@pytest.mark.parametrize("code", ["x = 1\n", "activate = 3\n"])
def test_an_entry_that_is_not_a_function_is_refused(tmp_path, code) -> None:
    one, _ = make_extension(tmp_path, code)

    assert "has no function activate" in ExtensionLoader(make_host()).load(one).error


def test_a_package_named_like_one_already_loaded_is_refused(tmp_path) -> None:
    host = make_host()
    loader = ExtensionLoader(host)
    first, package = make_extension(tmp_path, GOOD)
    loader.load(first)
    other = tmp_path / "other"
    (other / package).mkdir(parents=True)
    (other / package / "__init__.py").write_text(GOOD)
    twin = Installed(
        Manifest(
            "dco.twin", "Twin", "1.0.0", f"{package}:activate", frozenset({"ui.dock"})
        ),
        other,
        "file y.zip",
        "",
        False,
    )

    loaded = loader.load(twin)

    assert "name of another package" in loaded.error
    assert [d.extension for d in host.contributions.docks] == [first.manifest.id]
    assert package in sys.modules  # the first one still runs


def test_a_package_without_an_init_file_is_refused(tmp_path) -> None:
    one, package = make_extension(tmp_path, GOOD)
    (one.folder / package / "__init__.py").unlink()

    assert not ExtensionLoader(make_host()).load(one).ok


def test_reloading_runs_the_code_again_as_it_is_now(tmp_path) -> None:
    host = make_host()
    loader = ExtensionLoader(host)
    one, package = make_extension(tmp_path, GOOD)
    loader.load(one)
    (one.folder / package / "__init__.py").write_text(GOOD.replace('"chat"', '"chat2"'))

    loaded = loader.reload(one)

    assert loaded.ok
    assert [d.key for d in host.contributions.docks] == ["chat2"]  # and not both


def test_reloading_something_that_broke_reports_it_and_keeps_the_app_up(
    tmp_path,
) -> None:
    host = make_host()
    loader = ExtensionLoader(host)
    one, package = make_extension(tmp_path, GOOD)
    loader.load(one)
    (one.folder / package / "__init__.py").write_text("def activate(ctx:\n")  # syntax

    loaded = loader.reload(one)

    assert not loaded.ok
    assert "never closed" in loaded.error  # the first line of the syntax error
    assert host.contributions.docks == []
    (one.folder / package / "__init__.py").write_text(GOOD)
    assert loader.reload(one).ok  # fixed: it comes back


def test_what_the_extension_asked_to_close_is_closed_when_it_unloads(tmp_path) -> None:
    host = make_host()
    loader = ExtensionLoader(host)
    one, package = make_extension(
        tmp_path,
        "CLOSED = []\n"
        "def activate(ctx):\n"
        "    ctx.on_unload(lambda: CLOSED.append('first'))\n"
        "    ctx.on_unload(lambda: CLOSED.append('second'))\n",
    )
    loader.load(one)
    closed = sys.modules[package].CLOSED

    loader.unload(one.manifest.id)

    assert closed == ["second", "first"]  # the last one made is the first undone


def test_a_cleanup_that_fails_does_not_stop_the_others(tmp_path, caplog) -> None:
    loader = ExtensionLoader(make_host())
    one, package = make_extension(
        tmp_path,
        "CLOSED = []\n"
        "def activate(ctx):\n"
        "    ctx.on_unload(lambda: CLOSED.append('ok'))\n"
        "    ctx.on_unload(lambda: 1 / 0)\n",
    )
    loader.load(one)
    closed = sys.modules[package].CLOSED

    with caplog.at_level(logging.ERROR):
        loader.unload(one.manifest.id)

    assert closed == ["ok"]
    assert "A cleanup of the extension" in caplog.text
