"""What the extensions are lent of the AWS account of a context.

Only commands that read are run: a service and a verb from the list
below, and nothing that moves a request to another account, region or
server. No Qt.
"""

import re
from typing import Any

from kubescope.sdk.errors import ClusterError

from kubescope import cluster, integrations
from kubescope.sdk import AwsScope

# service -> the verbs it may run, by prefix (ending in "-") or whole
ALLOWED: dict[str, tuple[str, ...]] = {
    "rds": ("describe-", "list-", "download-db-log-file-portion"),
    "ec2": ("describe-",),
    "eks": ("describe-", "list-"),
    "ssm": ("describe-instance-information",),
}

_WORD = re.compile(r"[a-z0-9][a-z0-9-]*")
_MOVES = ("--profile", "--region", "--endpoint-url", "--output", "--cli-", "--debug")
MAX_ARGUMENTS = 40


def check(command: list[str]) -> None:
    """Refuse a command that is not a read of an allowed service."""
    if len(command) < 2 or len(command) > MAX_ARGUMENTS:
        raise ClusterError("That AWS command is not allowed")
    service, verb = command[0], command[1]
    if not (_WORD.fullmatch(service) and _WORD.fullmatch(verb)):
        raise ClusterError("That AWS command is not allowed")
    allowed = ALLOWED.get(service, ())
    if not any(
        verb.startswith(rule) if rule.endswith("-") else verb == rule
        for rule in allowed
    ):
        raise ClusterError(f"The AWS command {service} {verb} is not allowed")
    for argument in command[2:]:
        if argument.startswith(_MOVES) or argument.startswith("file://"):
            raise ClusterError(f"The AWS option {argument} is not allowed")


class AwsBridge:
    def uses_aws(self, context: str | None) -> bool:
        if (
            integrations.accounts("aws")
            or integrations.sso_accounts()
            or integrations.sso_profiles()
        ):
            return True
        return bool(context) and cluster.is_eks_context(context or "")

    def scope(self, context: str) -> AwsScope:
        region, profile, account = cluster._aws_scope(context)
        return AwsScope(region, profile, account)

    def regions(self) -> tuple[str, ...]:
        return tuple(cluster.AWS_REGIONS)

    def run(self, context: str, command: list[str], region: str = "") -> dict[str, Any]:
        check(command)
        if region and not re.fullmatch(r"[a-z]{2}(-[a-z]+)+-\d", region):
            raise ClusterError(f"{region} is not an AWS region")
        return cluster._aws_json(context, list(command), region)
