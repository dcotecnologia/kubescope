import pytest
from kubescope.sdk import PermissionDenied
from kubescope.sdk.errors import ClusterError

from kubescope import cluster
from kubescope.extensions import aws_access
from kubescope.extensions.aws_access import AwsBridge, check
from kubescope.extensions.context import ExtensionContext
from tests.test_extensions import make_host


@pytest.mark.parametrize(
    "command",
    [
        ["rds", "describe-db-instances"],
        ["rds", "describe-db-instances", "--db-instance-identifier", "orders"],
        ["rds", "describe-db-log-files", "--db-instance-identifier", "orders"],
        ["rds", "download-db-log-file-portion", "--log-file-name", "error/x.log"],
        ["ec2", "describe-instances", "--instance-ids", "i-1", "i-2"],
        ["ssm", "describe-instance-information"],
        ["eks", "list-clusters"],
    ],
)
def test_the_commands_that_read_are_run(command) -> None:
    check(command)


@pytest.mark.parametrize(
    "command",
    [
        ["rds", "delete-db-instance", "--db-instance-identifier", "x"],
        ["rds", "modify-db-instance"],
        ["rds", "describe_db"],
        ["ec2", "terminate-instances"],
        ["ec2", "run-instances"],
        ["ssm", "send-command"],
        ["ssm", "start-session"],
        ["ssm", "get-parameter", "--with-decryption"],
        ["sts", "get-session-token"],
        ["secretsmanager", "get-secret-value"],
        ["configure", "get"],
        ["rds"],
        [],
        ["rds", "describe-db-instances", *["x"] * 50],
        ["../x", "describe-y"],
    ],
)
def test_the_commands_that_change_or_reveal_are_refused(command) -> None:
    with pytest.raises(ClusterError, match="not allowed"):
        check(command)


@pytest.mark.parametrize(
    "option",
    [
        "--profile",
        "--region",
        "--endpoint-url=http://evil",
        "--output",
        "--cli-input-json",
        "--debug",
        "file:///etc/passwd",
    ],
)
def test_an_option_that_moves_the_request_is_refused(option) -> None:
    with pytest.raises(ClusterError, match="not allowed"):
        check(["rds", "describe-db-instances", option])


def test_run_asks_the_cluster_module_with_what_was_checked(monkeypatch) -> None:
    asked = []
    monkeypatch.setattr(
        cluster,
        "_aws_json",
        lambda context, command, region: (
            asked.append((context, command, region)) or {"ok": 1}
        ),
    )

    answer = AwsBridge().run("ctx", ["rds", "describe-db-instances"], "eu-west-1")

    assert answer == {"ok": 1}
    assert asked == [("ctx", ["rds", "describe-db-instances"], "eu-west-1")]


def test_a_region_that_is_not_one_is_refused(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_aws_json", lambda *args: {})

    with pytest.raises(ClusterError, match="is not an AWS region"):
        AwsBridge().run("ctx", ["rds", "describe-db-instances"], "x; rm -rf")


def test_the_scope_is_the_region_profile_and_account(monkeypatch) -> None:
    monkeypatch.setattr(cluster, "_aws_scope", lambda context: ("sa-east-1", "w", "1"))

    scope = AwsBridge().scope("ctx")

    assert (scope.region, scope.profile, scope.account) == ("sa-east-1", "w", "1")
    assert "us-east-1" in AwsBridge().regions()


def test_aws_is_in_use_with_an_account_or_an_eks_context(monkeypatch) -> None:
    monkeypatch.setattr(aws_access.integrations, "accounts", lambda cloud: [])
    monkeypatch.setattr(aws_access.integrations, "sso_accounts", lambda: [])
    monkeypatch.setattr(aws_access.integrations, "sso_profiles", lambda: [])
    monkeypatch.setattr(cluster, "is_eks_context", lambda context: context == "eks")

    assert AwsBridge().uses_aws("eks") and not AwsBridge().uses_aws("kind")
    assert not AwsBridge().uses_aws(None)
    monkeypatch.setattr(aws_access.integrations, "sso_profiles", lambda: ["x"])
    assert AwsBridge().uses_aws(None)


def test_the_extension_needs_the_permission_to_read_aws() -> None:
    host, _, _ = make_host()

    with pytest.raises(PermissionDenied, match="aws.read"):
        _ = ExtensionContext("dco.a", frozenset(), host).aws
    assert isinstance(
        ExtensionContext("dco.a", frozenset({"aws.read"}), host).aws, AwsBridge
    )
