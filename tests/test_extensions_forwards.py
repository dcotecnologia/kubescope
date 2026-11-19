import pytest
from kubescope.sdk.errors import ClusterError

from kubescope import cluster, forwards
from kubescope.extensions.context import ExtensionContext
from kubescope.extensions.forward_access import ForwardsBridge, check_ssm
from kubescope.sdk import PermissionDenied, WriteModeOff
from kubescope.writes import ssm_forward_arguments
from tests.test_extensions import make_host

INSTANCE = "i-0123456789abcdef0"


def command(instance=INSTANCE, profile="work"):
    return ssm_forward_arguments(
        instance, "db.example.com", 5432, 15432, "us-east-1", profile
    )


def test_the_command_the_app_builds_is_accepted() -> None:
    check_ssm(command())
    check_ssm(command(profile=""))


@pytest.mark.parametrize(
    "bad",
    [
        ["rm", "-rf", "/"],
        ["aws", "s3", "rm", "s3://x"],
        ["aws", "ssm", "send-command"],
        ["aws", "ssm", "start-session"],
        ["aws", "ssm", "start-session", "--target", INSTANCE],
        [
            *command()[:-2],
            "--endpoint-url",
            "http://evil",
        ],
        [*command(), "--target", INSTANCE],
        [*command(), "--profile", "other"],
        [*command()[:-1]],
    ],
)
def test_anything_but_the_forward_the_app_builds_is_refused(bad) -> None:
    with pytest.raises(ClusterError):
        check_ssm(bad)


def test_the_target_must_be_an_ec2_instance() -> None:
    with pytest.raises(ClusterError, match="EC2 instance"):
        check_ssm(command(instance="$(reboot)"))
    with pytest.raises(ClusterError, match="EC2 instance"):
        check_ssm(command(instance="<EC2-INSTANCE-ID>"))


def test_another_document_is_refused() -> None:
    bad = command()
    bad[bad.index("AWS-StartPortForwardingSessionToRemoteHost")] = "AWS-RunShellScript"

    with pytest.raises(ClusterError, match="document"):
        check_ssm(bad)


def test_a_value_with_a_shell_trick_is_refused() -> None:
    bad = command()
    bad[bad.index("--region") + 1] = "us-east-1; reboot"

    with pytest.raises(ClusterError, match="value"):
        check_ssm(bad)


def make(write_mode: bool, taken: bool = False):
    started = []
    bridge = ForwardsBridge(
        lambda: write_mode,
        lambda *args: started.append(args) or not taken,
    )
    return bridge, started


def test_a_forward_starts_in_the_write_mode_with_the_keys_of_the_context(
    monkeypatch,
) -> None:
    monkeypatch.setattr(cluster, "context_environment", lambda context: {"K": context})
    bridge, started = make(True)

    assert bridge.start_ssm("ctx", "RDS orders", command(), 15432, "db:5432")

    [(title, kind, arguments, env, local, target)] = started
    assert (title, kind, local, target) == ("RDS orders", "ssm", 15432, "db:5432")
    assert env == {"K": "ctx"} and arguments == command()


def test_without_the_write_mode_nothing_starts() -> None:
    bridge, started = make(False)

    with pytest.raises(WriteModeOff):
        bridge.start_ssm("ctx", "t", command(), 15432, "db:5432")
    assert started == []


def test_a_refused_command_or_port_starts_nothing() -> None:
    bridge, started = make(True)

    with pytest.raises(ClusterError):
        bridge.start_ssm("ctx", "t", ["rm", "-rf", "/"], 15432, "x")
    with pytest.raises(ClusterError, match="port"):
        bridge.start_ssm("ctx", "t", command(), 0, "x")
    assert started == []


def test_a_port_in_use_says_so(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "context_environment", lambda context: {})
    bridge, _ = make(True, taken=True)
    monkeypatch.setattr(forwards, "port_in_use", lambda port: port == 80)

    assert not bridge.start_ssm("ctx", "t", command(), 15432, "x")
    assert bridge.port_in_use(80) and not bridge.port_in_use(81)


def test_the_extension_needs_the_permission_to_forward() -> None:
    host, _, _ = make_host()

    with pytest.raises(PermissionDenied, match="forward"):
        _ = ExtensionContext("dco.a", frozenset(), host).forwards
    assert isinstance(
        ExtensionContext("dco.a", frozenset({"forward"}), host).forwards,
        ForwardsBridge,
    )
