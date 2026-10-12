import pytest

from kubescope.errors import describe_error


@pytest.mark.parametrize(
    ("message", "title"),
    [
        (
            "Unable to connect to the server: getting credentials: exec: "
            "executable aws not found\n\nIt looks like you are trying to use a "
            "client-go credential plugin that is not installed.",
            "Login tool not found",
        ),
        (
            "Unable to connect to the server: dial tcp: i/o timeout",
            "Cluster unreachable",
        ),
        ("The request timed out while contacting the cluster", "Cluster unreachable"),
        (
            "HTTPSConnection(host='x', port=443): Failed to establish a new "
            "connection: [Errno -2] Name or service not known",
            "Cluster unreachable",
        ),
        (
            "error: You must be logged in to the server (Unauthorized)",
            "Authentication failed",
        ),
        (
            "The SSO session associated with this profile has expired or is not valid",
            "Authentication failed",
        ),
        ("Unable to locate credentials", "Authentication failed"),
        (
            "exec: process returned 1. ERROR: Reauthentication failed. "
            "Please run: gcloud auth login",
            "Authentication failed",
        ),
        (
            "exec: process returned 1. AADSTS70043: The refresh token has expired",
            "Authentication failed",
        ),
        ("Please run 'az login' to setup account.", "Authentication failed"),
        (
            "An error occurred (InvalidClientTokenId) when calling the "
            "GetCallerIdentity operation",
            "Authentication failed",
        ),
        ("pods is forbidden: User cannot list resource", "Access denied"),
        (
            "Error in configuration: context was not found for specified context: x",
            "Context not found",
        ),
        (
            "This list is only available for Amazon EKS contexts",
            "Not an Amazon EKS cluster",
        ),
        (
            "The AWS CLI answered with something unexpected",
            "Unexpected answer from AWS",
        ),
        (
            "An error occurred (AccessDeniedException) when calling the "
            "ListNodegroups operation: User is not authorized to perform: "
            "eks:ListNodegroups",
            "Access denied",
        ),
        ("something odd\nsecond line", "Something went wrong"),
    ],
)
def test_describe_error_classifies_cluster_failures(message: str, title: str) -> None:
    info = describe_error(message)

    assert info.title == title
    assert info.details == message.strip()


def test_missing_login_tool_names_the_executable() -> None:
    info = describe_error("getting credentials: exec: executable gcloud not found")

    assert "gcloud" in info.hint


def test_unknown_error_keeps_its_first_line_as_hint() -> None:
    assert describe_error("\n  boom happened\nmore").hint == "boom happened"


def test_first_line_skips_blank_lines() -> None:
    from kubescope.errors import first_line

    assert first_line("\n  \n  boom  \nsecond") == "boom"
    assert first_line("") == ""


def test_forbidden_is_told_apart_from_a_sign_in_problem() -> None:
    from kubescope.errors import forbidden_action, is_forbidden

    message = (
        'Error from server (Forbidden): services is forbidden: User "x" cannot '
        'list resource "services" in API group "" in the namespace "ops"'
    )

    assert is_forbidden(message)
    assert not is_forbidden("Unauthorized: token has expired, forbidden")
    assert not is_forbidden("connection refused")
    assert forbidden_action(message) == "list services"
    assert forbidden_action("pods is forbidden") is None
