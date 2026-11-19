"""What the extensions are lent of the port forwards
(`kubescope.sdk.Forwards`).

An extension can start one kind of forward, a database through AWS
Systems Manager, and only in the write mode: the command is checked
here, so that it cannot run another program. No Qt.
"""

import re
from collections.abc import Callable

from kubescope.sdk import WriteModeOff
from kubescope.sdk.errors import ClusterError

from kubescope import cluster, forwards

DOCUMENT = "AWS-StartPortForwardingSessionToRemoteHost"
_INSTANCE = re.compile(r"(i|mi)-[0-9a-f]{8,17}")
_OPTIONS = {"--target", "--document-name", "--parameters", "--region", "--profile"}
_VALUE = re.compile(r"[A-Za-z0-9._:/=,{}\[\]\" -]*")


def check_ssm(command: list[str]) -> None:
    """Refuse anything but `aws ssm start-session` to a port forwarding
    document, with the options the app builds it with."""
    if command[:3] != ["aws", "ssm", "start-session"]:
        raise ClusterError("Only an AWS Systems Manager session can be started")
    options = command[3:]
    if len(options) % 2 or len(options) > 2 * len(_OPTIONS):
        raise ClusterError("That session has options the app does not build")
    given = dict(zip(options[::2], options[1::2], strict=True))
    if len(given) != len(options) // 2 or not set(given) <= _OPTIONS:
        raise ClusterError("That session has options the app does not build")
    if given.get("--document-name") != DOCUMENT:
        raise ClusterError(f"Only the document {DOCUMENT} is allowed")
    if not _INSTANCE.fullmatch(given.get("--target", "")):
        raise ClusterError(
            "The target must be an EC2 instance, like i-0123456789abcdef0"
        )
    if any(not _VALUE.fullmatch(value) for value in given.values()):
        raise ClusterError("That session has a value the app does not accept")


class ForwardsBridge:
    def __init__(
        self,
        write_mode: Callable[[], bool],
        begin: Callable[[str, str, list[str], dict[str, str], int, str], bool],
    ) -> None:
        self._write_mode = write_mode
        self._begin = begin  # starts it and shows the Forwards page

    def port_in_use(self, port: int) -> bool:
        return forwards.port_in_use(port)

    def start_ssm(
        self, context: str, title: str, command: list[str], local: int, target: str
    ) -> bool:
        if not self._write_mode():
            raise WriteModeOff("turn on the write mode to start a forward")
        check_ssm(command)
        if not 1 <= local <= 65535:
            raise ClusterError("The local port must be between 1 and 65535")
        return self._begin(
            title,
            "ssm",
            list(command),
            cluster.context_environment(context),
            local,
            target,
        )
