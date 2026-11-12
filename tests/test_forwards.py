import json
import socket
import subprocess
import sys

import pytest
from PySide6.QtCore import QCoreApplication

from kubescope import forwards
from kubescope.forwards import FAILED, RUNNING, STARTING, STOPPED, Forward
from kubescope.views import forward_runner
from kubescope.views.forward_runner import ForwardRunner
from tests.qt import get_application
from tests.test_window_flows import _wait_until

application = get_application()


def test_a_port_that_something_listens_on_is_in_use() -> None:
    with socket.socket() as server:
        server.bind(("127.0.0.1", 0))
        server.listen()
        port = server.getsockname()[1]
        assert forwards.port_in_use(port)
    assert not forwards.port_in_use(port)


def test_the_line_that_says_the_port_is_open_is_told_for_each_program() -> None:
    assert (
        forwards.status_of("kubectl", "Forwarding from 127.0.0.1:8080 -> 80") == RUNNING
    )
    assert forwards.status_of("ssm", "Waiting for connections...") == RUNNING
    assert forwards.status_of("ssm", "Port 15432 opened for sessionId x.") == RUNNING
    assert forwards.status_of("kubectl", "error: unable to listen") is None
    assert forwards.status_of("ssm", "Starting session with SessionId: x") is None
    assert forwards.status_of("other", "Forwarding from") is None


def test_a_forward_is_active_until_it_fails_or_stops() -> None:
    forward = Forward(1, "Service api", "kubectl", ["kubectl"])
    assert forward.active and forward.status == STARTING
    for status in (RUNNING,):
        forward.status = status
        assert forward.active
    forward.status = FAILED
    assert not forward.active


LISTENING = "import time; print('Forwarding from 127.0.0.1:1 -> 2'); time.sleep(60)"
BUSY = "import sys; print('error: port busy', file=sys.stderr); sys.exit(1)"
DEAF = "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); "


def _python(code: str) -> list[str]:
    return [sys.executable, "-u", "-c", code]


@pytest.fixture
def runner():
    one = ForwardRunner()
    yield one
    one.stop_all()
    one.wait()
    QCoreApplication.sendPostedEvents(None, 0)


def test_a_forward_runs_says_when_it_listens_and_stops_on_request(runner) -> None:
    changes = []
    runner.changed.connect(lambda: changes.append(1))
    code = "import time; print('Forwarding from 127.0.0.1:1 -> 2'); time.sleep(60)"

    forward = runner.start(
        "Service api", "kubectl", _python(code), {"A": "1"}, 8080, "api:80"
    )
    assert forward.status == STARTING and runner.active_count() == 1
    _wait_until(lambda: forward.status == RUNNING)
    assert forward.detail.startswith("Forwarding from")

    runner.stop(forward)
    assert forward.status == STOPPED  # at once, for the screen
    _wait_until(lambda: forward.number not in runner._processes)
    assert forward.status == STOPPED and runner.active_count() == 0 and changes
    runner.stop(forward)  # already stopped: nothing to do

    runner.clear_finished()
    assert runner.items == []


def test_a_program_that_fails_tells_why_and_one_that_is_missing_too(runner) -> None:
    failed = []
    runner.failed.connect(failed.append)
    broken = runner.start(
        "x",
        "kubectl",
        _python("import sys; print('error: port busy', file=sys.stderr); sys.exit(1)"),
        {},
        1,
        "t",
    )
    silent = runner.start(
        "y", "kubectl", _python("import sys; sys.exit(2)"), {}, 2, "t"
    )
    done = runner.start("z", "kubectl", _python("pass"), {}, 3, "t")
    missing = runner.start("w", "kubectl", ["/no/such/program"], {}, 4, "t")

    _wait_until(lambda: not runner._processes)

    assert broken.status == FAILED and broken.detail == "error: port busy"
    assert silent.status == FAILED and silent.detail == "exit code 2"
    assert done.status == STOPPED  # ended by itself without an error
    assert missing.status == FAILED and "could not start" in missing.detail
    assert {item.title for item in failed} >= {"x", "y", "w"}  # told as they failed
    runner.clear_finished()
    assert runner.items == []


def test_a_program_that_says_nothing_is_taken_as_listening(runner, monkeypatch) -> None:
    monkeypatch.setattr(forward_runner, "READY_MS", 50)
    forward = runner.start(
        "s", "ssm", _python("import time; time.sleep(60)"), {}, 1, "t"
    )
    _wait_until(lambda: forward.status == RUNNING)
    runner._assume_running(forward)  # twice does no harm
    assert forward.status == RUNNING


def test_a_program_that_ignores_the_request_to_stop_is_killed(
    runner, monkeypatch
) -> None:
    monkeypatch.setattr(forward_runner, "STOP_WAIT_MS", 200)
    code = DEAF + "print('up', flush=True); time.sleep(60)"
    forward = runner.start("s", "ssm", _python(code), {}, 1, "t")
    _wait_until(lambda: forward.detail == "up")

    runner.stop_all()
    _wait_until(lambda: forward.number not in runner._processes, seconds=5)

    assert forward.status == STOPPED


def test_waiting_ends_what_is_still_running(runner, monkeypatch) -> None:
    monkeypatch.setattr(forward_runner, "STOP_WAIT_MS", 200)
    forward = runner.start("s", "ssm", _python(DEAF + "time.sleep(60)"), {}, 1, "t")
    runner.wait()  # it ignores the request, so it is killed
    _wait_until(lambda: forward.number not in runner._processes)
    assert not forward.active
    runner._read(forward, False)  # the output of one that is gone: ignored
    runner._kill(forward)


def _sleeper(port: int = 7777) -> subprocess.Popen:
    """A real process that looks like a forward: its program and its port."""
    return subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)", f"{port}:80"]
    )


def _record(process: subprocess.Popen, port: int = 7777, **changes) -> dict:
    record = {
        "title": "Service api",
        "kind": "kubectl",
        "command": [sys.executable, "-c", "x", f"{port}:80"],
        "local": port,
        "target": "api:80",
        "pid": process.pid,
    }
    return {**record, **changes}


@pytest.fixture
def sleeper():
    process = _sleeper()
    yield process
    process.kill()
    process.wait()


def test_the_forwards_that_run_are_kept_without_their_environment(sleeper) -> None:
    running = Forward(
        1, "S", "kubectl", ["k"], {"AWS_SECRET": "x"}, 1, "t", RUNNING, "", 5
    )
    starting = Forward(2, "T", "ssm", ["a"], {}, 2, "t", STARTING, "", 6)
    ended = Forward(3, "U", "ssm", ["a"], {}, 3, "t", STOPPED, "", 7)
    nopid = Forward(4, "V", "ssm", ["a"], {}, 4, "t", RUNNING, "", 0)

    forwards.save([running, starting, ended, nopid])

    text = forwards.state_path().read_text()
    assert [item["pid"] for item in json.loads(text)] == [5, 6]
    assert "AWS_SECRET" not in text

    forwards.state_path().unlink()
    forwards.state_path().mkdir()  # a place that cannot be written: only a warning
    forwards.save([running])


def test_the_forwards_of_an_earlier_run_come_back_only_while_they_run(sleeper) -> None:
    gone = subprocess.Popen([sys.executable, "-c", "pass"])
    gone.wait()
    other = _record(sleeper, command=["kubectl", "port-forward", "7777:80"])  # not it
    wrong_port = _record(sleeper, local=1234)
    records = [
        _record(sleeper),
        _record(gone),
        other,
        wrong_port,
        {"title": "no pid"},
        "odd",
        {**_record(sleeper), "pid": "x"},
    ]
    forwards.state_path().parent.mkdir(parents=True, exist_ok=True)
    forwards.state_path().write_text(json.dumps(records))

    found = forwards.load()

    assert [(f.title, f.pid, f.adopted, f.status) for f in found] == [
        ("Service api", sleeper.pid, True, RUNNING)
    ]
    forwards.state_path().write_text("{not json")
    assert forwards.load() == []
    forwards.state_path().write_text('{"a": 1}')
    assert forwards.load() == []
    forwards.state_path().unlink()
    assert forwards.load() == []


def test_a_process_is_told_alive_or_gone_and_asked_to_end(sleeper, monkeypatch) -> None:
    assert forwards.process_alive(sleeper.pid)
    forwards.terminate(sleeper.pid)
    sleeper.wait(timeout=10)
    assert not forwards.process_alive(sleeper.pid)
    forwards.terminate(sleeper.pid)  # already gone: nothing to do

    def not_ours(pid, signal):
        raise PermissionError

    monkeypatch.setattr(forwards.os, "kill", not_ours)
    assert forwards.process_alive(1)  # it exists, but is not ours to signal
    assert not forwards.process_matches(Forward(1, "x", "k", [], {}, 1, "t"))


def test_on_windows_a_process_is_looked_up_and_ended_with_its_own_tools(
    monkeypatch,
) -> None:
    monkeypatch.setattr(forwards.sys, "platform", "win32")
    calls = []

    def run(command, **options):
        calls.append(command)
        text = (
            '"kubectl.exe","42","Console","1","10 K"'
            if command[0] == "tasklist"
            else ""
        )
        return subprocess.CompletedProcess(command, 0, stdout=text, stderr="")

    monkeypatch.setattr(forwards.subprocess, "run", run)
    forward = Forward(
        1, "S", "kubectl", ["C:\\bin\\kubectl.exe"], {}, 80, "t", RUNNING, "", 42
    )

    assert forwards.process_alive(42) and not forwards.process_alive(43)
    assert forwards.process_matches(forward)
    forwards.terminate(42)
    assert calls[-1] == ["taskkill", "/PID", "42", "/T", "/F"]


def test_the_runner_takes_back_what_an_earlier_run_left_and_stops_it(
    sleeper, monkeypatch
) -> None:
    forwards.state_path().parent.mkdir(parents=True, exist_ok=True)
    forwards.state_path().write_text(json.dumps([_record(sleeper)]))
    runner = ForwardRunner()
    runner.adopt()
    runner.adopt()  # asked twice: listed twice is not wanted
    [forward] = runner.items[:1]
    assert forward.adopted and forward.status == RUNNING and forward.number == 1
    assert "before the app was restarted" in forward.detail
    assert runner.active_count() >= 1
    assert runner._watch.isActive()

    runner.stop(forward)  # by its process number
    sleeper.wait(timeout=10)
    assert forward.status == STOPPED
    assert not forwards.process_alive(sleeper.pid)
    assert json.loads(forwards.state_path().read_text()) == []
    runner._watch.stop()


def test_a_forward_found_again_that_ends_by_itself_is_marked_ended(sleeper) -> None:
    forwards.state_path().parent.mkdir(parents=True, exist_ok=True)
    forwards.state_path().write_text(json.dumps([_record(sleeper)]))
    runner = ForwardRunner()
    runner.adopt()
    forward = runner.items[0]
    runner._look_at_adopted()  # still running: left alone
    assert forward.status == RUNNING

    sleeper.kill()
    sleeper.wait()
    runner._look_at_adopted()

    assert forward.status == STOPPED and forward.detail == "ended"
    runner._look_at_adopted()  # not looked at again
    runner._watch.stop()
    assert ForwardRunner().items == []  # nothing to take back: no timer


def test_a_started_forward_is_kept_with_its_process_and_forgotten_when_it_ends(
    runner,
) -> None:
    forward = runner.start("s", "kubectl", _python(LISTENING + "# 5555"), {}, 5555, "t")
    _wait_until(lambda: forward.pid != 0)
    kept = json.loads(forwards.state_path().read_text())
    assert [item["pid"] for item in kept] == [forward.pid]

    runner.stop(forward)
    _wait_until(lambda: forward.number not in runner._processes)
    assert json.loads(forwards.state_path().read_text()) == []


def test_blank_lines_of_a_program_are_skipped(runner) -> None:
    code = "import time; print(); print('  '); print('hello'); time.sleep(60)"
    forward = runner.start("s", "kubectl", _python(code), {}, 1, "t")
    _wait_until(lambda: forward.detail == "hello")
