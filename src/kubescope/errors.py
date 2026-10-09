"""Turn raw kubectl failures into a short title and a hint a person can act
on."""

import re
from dataclasses import dataclass

from PySide6.QtCore import QCoreApplication


@dataclass(frozen=True, slots=True)
class ErrorInfo:
    title: str
    hint: str
    details: str  # the original kubectl text, kept for the "Show details" view


_AUTH_WORDS = (
    "unauthorized",
    "you must be logged in",
    "token has expired",
    "sso session",
    "error loading sso token",
    "unable to locate credentials",
    "invalidclienttokenid",
    "security token included in the request",
    "signaturedoesnotmatch",
    "expiredtoken",
)


def is_auth_error(message: str) -> bool:
    """Whether the failure means the user has to sign in again."""
    lowered = message.lower()
    return any(word in lowered for word in _AUTH_WORDS) or (
        "expired" in lowered and ("credential" in lowered or "token" in lowered)
    )


def first_line(text: str) -> str:
    """The first non-empty line, for one-line summaries and logs."""
    return next((line.strip() for line in text.splitlines() if line.strip()), "")


def describe_error(message: str) -> ErrorInfo:
    """Classify a kubectl error message; unknown ones keep their first line."""
    details = message.strip()
    lowered = details.lower()

    plugin = re.search(r"executable (\S+) not found", details)
    if plugin:
        return ErrorInfo(
            QCoreApplication.translate("Errors", "Login tool not found"),
            QCoreApplication.translate(
                "Errors",
                "Your kubeconfig runs “{tool}” to sign in, but it is not installed "
                "or not on the PATH. Install it and refresh.",
            ).format(tool=plugin.group(1)),
            details,
        )
    if "bundled kubectl is missing" in lowered:
        return ErrorInfo(
            QCoreApplication.translate("Errors", "kubectl is missing"),
            QCoreApplication.translate(
                "Errors",
                "The kubectl bundled with the app was not found. Reinstall it.",
            ),
            details,
        )
    if "context was not found" in lowered or "error in configuration" in lowered:
        return ErrorInfo(
            QCoreApplication.translate("Errors", "Context not found"),
            QCoreApplication.translate(
                "Errors",
                "This context is not in your kubeconfig. Check ~/.kube/config.",
            ),
            details,
        )
    if is_auth_error(details):
        return ErrorInfo(
            QCoreApplication.translate("Errors", "Authentication failed"),
            QCoreApplication.translate(
                "Errors",
                "Your credentials may have expired. Sign in again (for example "
                "“aws sso login”) and refresh.",
            ),
            details,
        )
    if "forbidden" in lowered:
        return ErrorInfo(
            QCoreApplication.translate("Errors", "Access denied"),
            QCoreApplication.translate(
                "Errors", "Your user is not allowed to read this resource."
            ),
            details,
        )
    if any(
        word in lowered
        for word in (
            "timed out",
            "i/o timeout",
            "connection refused",
            "no such host",
            "unable to connect",
            "deadline exceeded",
        )
    ):
        return ErrorInfo(
            QCoreApplication.translate("Errors", "Cluster unreachable"),
            QCoreApplication.translate(
                "Errors", "Check your network or VPN and that the cluster is running."
            ),
            details,
        )
    return ErrorInfo(
        QCoreApplication.translate("Errors", "Something went wrong"),
        first_line(details),
        details,
    )
