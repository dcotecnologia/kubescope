import shutil

from kubescope.utils import programs


def test_on_windows_the_program_is_found_where_its_installers_put_it(
    monkeypatch, tmp_path
) -> None:
    bin_folder = tmp_path / ".local" / "bin"
    bin_folder.mkdir(parents=True)
    program = bin_folder / "fake-ai.exe"
    program.write_bytes(b"")
    monkeypatch.setattr(programs.sys, "platform", "win32")
    monkeypatch.setattr(programs.Path, "home", lambda: tmp_path)
    monkeypatch.setattr(programs, "_registry_path", lambda: [])
    monkeypatch.delenv("APPDATA", raising=False)
    monkeypatch.delenv("LOCALAPPDATA", raising=False)

    def which(name, path=None):  # not on the path, found only in a given folder
        return str(program) if path == str(bin_folder) else None

    monkeypatch.setattr(shutil, "which", which)

    assert programs.find_program("fake-ai") == str(program)
    assert programs.find_program("elsewhere/fake-ai") is None


def test_the_folders_of_the_installers_are_searched_on_windows(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr(programs.Path, "home", lambda: tmp_path / "home")
    monkeypatch.setattr(programs, "_registry_path", lambda: [str(tmp_path / "kept")])
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    monkeypatch.setenv("APPDATA", str(tmp_path / "roaming"))

    folders = programs._windows_folders()

    assert folders[0] == tmp_path / "kept"  # the path Windows keeps comes first
    assert len(folders) == len(set(folders))
    assert tmp_path / "local" / "Programs" / "OpenAI" / "Codex" / "bin" in folders
    assert tmp_path / "local" / "Programs" / "Amazon" / "AWSCLIV2" in folders
    assert tmp_path / "roaming" / "npm" in folders
    standalone = tmp_path / "home" / ".codex" / "packages" / "standalone"
    assert standalone / "current" / "bin" in folders


def test_on_windows_a_program_in_no_folder_is_not_found(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(programs.sys, "platform", "win32")
    monkeypatch.setattr(programs.Path, "home", lambda: tmp_path)
    monkeypatch.setattr(programs, "_registry_path", lambda: [])
    monkeypatch.setattr(shutil, "which", lambda name, path=None: None)

    assert programs.find_program("fake-ai") is None


def test_off_windows_only_the_path_is_searched(monkeypatch) -> None:
    monkeypatch.setattr(programs.sys, "platform", "linux")
    monkeypatch.setattr(shutil, "which", lambda name, path=None: None)

    assert programs.find_program("fake-ai") is None


def test_the_path_of_the_program_on_the_system_wins(monkeypatch) -> None:
    monkeypatch.setattr(shutil, "which", lambda name, path=None: "/bin/" + name)

    assert programs.find_program("fake-ai") == "/bin/fake-ai"


def test_the_path_windows_keeps_is_read_from_the_registry(monkeypatch) -> None:
    import types

    class Key:
        def __init__(self, value):
            self.value = value

        def __enter__(self):
            return self

        def __exit__(self, *_error):
            return False

    values = {"Environment": "%FAKE_ROOT%\\one;;two", "Session": None}

    def open_key(_root, name):
        if "Session" in name:
            raise OSError  # a key that cannot be read is skipped
        return Key(values[name])

    fake = types.SimpleNamespace(
        HKEY_CURRENT_USER=1,
        HKEY_LOCAL_MACHINE=2,
        OpenKey=open_key,
        QueryValueEx=lambda key, _name: (key.value, 1),
    )
    monkeypatch.setitem(__import__("sys").modules, "winreg", fake)
    monkeypatch.setenv("FAKE_ROOT", "C:\\root")
    monkeypatch.setattr(programs.sys, "platform", "win32")

    found = programs._registry_path()

    assert found[0].endswith("one") and "FAKE_ROOT" not in found[0]
    assert found[1] == "two"
    assert len(found) == 2


def test_off_windows_there_is_no_registry_path(monkeypatch) -> None:
    monkeypatch.setattr(programs.sys, "platform", "linux")

    assert programs._registry_path() == []
