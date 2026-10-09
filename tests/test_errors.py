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
        ("kubectl timed out while contacting the cluster", "Cluster unreachable"),
        (
            "error: You must be logged in to the server (Unauthorized)",
            "Authentication failed",
        ),
        ("pods is forbidden: User cannot list resource", "Access denied"),
        (
            "Error in configuration: context was not found for specified context: x",
            "Context not found",
        ),
        ("Bundled kubectl is missing. Run fetch", "kubectl is missing"),
        ("something odd\nsecond line", "Something went wrong"),
    ],
)
def test_describe_error_classifies_kubectl_failures(message: str, title: str) -> None:
    info = describe_error(message)

    assert info.title == title
    assert info.details == message.strip()


def test_missing_login_tool_names_the_executable() -> None:
    info = describe_error("getting credentials: exec: executable gcloud not found")

    assert "gcloud" in info.hint


def test_unknown_error_keeps_its_first_line_as_hint() -> None:
    assert describe_error("\n  boom happened\nmore").hint == "boom happened"
