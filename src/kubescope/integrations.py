"""Plug the clusters of cloud accounts into the app with a login made in it.

No Qt.

A cloud account (AWS, Azure or Google Cloud) is given its keys once. The
keys that are secret are kept in the memory of the app only, the rest
(the name, the regions, the project) is saved, and the clusters the
cloud lists are written to a kubeconfig of their own for each account,
in the configuration folder, that the app reads besides the others. The
keys are handed to the cloud's command line program through its
environment, and only to the programs of a cluster of that account: its
kubeconfig names the account, never holds a key. The keys last until the
app quits.
"""

import configparser
import json
import os
import secrets
import shutil
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from kubescope.settings import config_directory
from kubescope.utils.diagnostics import redact
from kubescope.utils.errors import first_line
from kubescope.utils.programs import find_program

TIMEOUT = 120.0
ACCOUNT_VARIABLE = "KUBESCOPE_ACCOUNT"  # names the account in a kubeconfig user


class IntegrationError(Exception):
    """The cloud cannot be reached or refused; the message says why."""


@dataclass(frozen=True, slots=True)
class Field:
    key: str
    label: str
    secret: bool = False
    optional: bool = False
    default: str = ""
    file: bool = False  # the value is the path of a file the person picks


@dataclass(frozen=True, slots=True)
class Provider:
    id: str
    name: str
    title: str  # the heading of its section
    programs: tuple[str, ...]  # what has to be installed
    fields: tuple[Field, ...]


@dataclass(frozen=True, slots=True)
class Account:
    id: str
    provider: str
    name: str
    fields: dict[str, str] = field(default_factory=dict)  # the ones not secret

    def saved(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "provider": self.provider,
            "name": self.name,
            "fields": dict(self.fields),
        }


@dataclass(frozen=True, slots=True)
class Found:
    """A cluster a cloud lists."""

    provider: str
    name: str
    place: str  # the region or the location
    group: str = ""  # the resource group of an Azure cluster

    @property
    def context(self) -> str:
        return f"{self.name}.{self.place}"


PROVIDERS = {
    provider.id: provider
    for provider in (
        Provider(
            "aws",
            "Amazon Web Services",
            "AMAZON EKS",
            ("aws",),
            (
                Field("profile", "AWS profile (instead of keys)", optional=True),
                Field("access_key_id", "Access key ID", optional=True),
                Field(
                    "secret_access_key", "Secret access key", secret=True, optional=True
                ),
                Field("session_token", "Session token", secret=True, optional=True),
                Field("regions", "Regions (comma separated)", default="us-east-1"),
            ),
        ),
        Provider(
            "azure",
            "Microsoft Azure",
            "AZURE AKS",
            ("az", "kubelogin"),
            (
                Field("tenant_id", "Tenant ID"),
                Field("client_id", "Client ID"),
                Field("client_secret", "Client secret", secret=True),
                Field("subscription_id", "Subscription ID"),
            ),
        ),
        Provider(
            "gcp",
            "Google Cloud",
            "GOOGLE GKE",
            ("gcloud",),
            (
                Field("project_id", "Project ID"),
                Field("key_file", "Service account key (JSON file)", file=True),
            ),
        ),
    )
}

_accounts: dict[str, Account] = {}  # the accounts known, by id
_secrets: dict[str, dict[str, str]] = {}  # in memory only, by account id


def load(saved: list[dict[str, Any]]) -> list[Account]:
    """Know the accounts saved in the settings; the keys of a previous run are
    gone, so each one asks for them again."""
    _accounts.clear()
    for item in saved:
        account = Account(item["id"], item["provider"], item["name"], item["fields"])
        if account.provider in PROVIDERS:
            _accounts[account.id] = account
    return accounts()


def account_named(account: str) -> Account | None:
    return _accounts.get(account)


def accounts(provider: str | None = None) -> list[Account]:
    return [
        account
        for account in _accounts.values()
        if provider in (None, account.provider)
    ]


def new_account_id(provider: str) -> str:
    return f"{provider}-{secrets.token_hex(3)}"


def add_account(
    provider: str,
    name: str,
    values: Mapping[str, str],
    account_id: str | None = None,
) -> Account:
    """A new account: its public fields are kept to be saved, its secrets only
    in memory."""
    public = {
        item.key: values.get(item.key, "").strip()
        for item in PROVIDERS[provider].fields
        if not item.secret
    }
    account = Account(account_id or new_account_id(provider), provider, name, public)
    _accounts[account.id] = account
    remember(account.id, values)
    return account


def update_account(account: Account, values: Mapping[str, str]) -> Account:
    """The account with the fields typed again."""
    public = {
        item.key: values.get(item.key, "").strip()
        for item in PROVIDERS[account.provider].fields
        if not item.secret
    }
    changed = Account(account.id, account.provider, account.name, public)
    _accounts[account.id] = changed
    remember(account.id, values)
    return changed


def remember(account: str, values: Mapping[str, str]) -> None:
    provider = PROVIDERS[_accounts[account].provider]
    _secrets[account] = {
        item.key: values.get(item.key, "").strip()
        for item in provider.fields
        if item.secret
    }


def values_of(account: Account) -> dict[str, str]:
    """The fields of an account: the ones saved and the keys of this run."""
    return {**account.fields, **_secrets.get(account.id, {})}


def has_keys(account: Account) -> bool:
    """Whether the keys of this run are there for every secret that is needed;
    an account of an AWS profile needs none."""
    if account.fields.get("profile"):
        return True
    kept = _secrets.get(account.id, {})
    if account.provider == "aws":
        return bool(kept.get("secret_access_key"))
    return all(
        kept.get(item.key)
        for item in PROVIDERS[account.provider].fields
        if item.secret and not item.optional
    )


def aws_profiles() -> list[tuple[str, str]]:
    """The profiles of the AWS CLI on this computer, with the account each one
    names when its file says (an SSO profile, or a role); only the names and
    the account numbers are read, never a key."""
    home = Path.home() / ".aws"
    files = (
        (Path(os.environ.get("AWS_CONFIG_FILE") or home / "config"), "profile "),
        (
            Path(os.environ.get("AWS_SHARED_CREDENTIALS_FILE") or home / "credentials"),
            "",
        ),
    )
    found: dict[str, str] = {}
    for path, prefix in files:
        parser = configparser.RawConfigParser()
        try:
            parser.read(path, encoding="utf-8")
        except OSError, configparser.Error:
            continue
        for section in parser.sections():
            name = section.removeprefix(prefix) if prefix else section
            if name == section and prefix and section != "default":
                continue  # a section of another kind, such as [sso-session x]
            account = parser.get(section, "sso_account_id", fallback="")
            role = parser.get(section, "role_arn", fallback="").split(":")
            if not account and len(role) > 4:
                account = role[4]
            found[name] = found.get(name) or account
    return sorted(found.items())


@dataclass(frozen=True, slots=True)
class SsoProfile:
    """A profile of the AWS CLI that signs in with SSO."""

    name: str
    account: str  # the account number, when the file says
    region: str
    signed_in: bool  # its sign-in has not expired


def _expired(text: object) -> bool:
    """Whether the `expiresAt` of a cached SSO sign-in is past."""
    if not isinstance(text, str):
        return True
    try:
        moment = datetime.fromisoformat(
            text.replace("Z", "+00:00").replace("UTC", "+00:00")
        )
    except ValueError:
        return True
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return moment <= datetime.now(UTC)


def _renewable(document: dict[str, Any]) -> bool:
    """Whether the AWS CLI renews this sign-in by itself: the sessions of a
    profile with an `sso-session` carry a refresh token, good while the
    registration of the CLI with the portal lasts."""
    return bool(document.get("refreshToken")) and not _expired(
        document.get("registrationExpiresAt")
    )


def _signed_in_urls() -> set[str]:
    """The SSO portals this computer is signed in to: only the address, the
    expiry and whether it can be renewed are read from each cached sign-in,
    never a token."""
    cache = Path.home() / ".aws" / "sso" / "cache"
    urls: set[str] = set()
    for path in cache.glob("*.json"):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except OSError, ValueError:
            continue
        if isinstance(document, dict) and (
            not _expired(document.get("expiresAt")) or _renewable(document)
        ):
            url = document.get("startUrl")
            if isinstance(url, str):
                urls.add(url)
    return urls


def sso_profiles() -> list[SsoProfile]:
    """The profiles of the AWS CLI that sign in with SSO, and whether each one
    is signed in now."""
    path = Path(os.environ.get("AWS_CONFIG_FILE") or Path.home() / ".aws" / "config")
    parser = configparser.RawConfigParser()
    try:
        parser.read(path, encoding="utf-8")
    except configparser.Error:
        return []
    urls = _signed_in_urls()
    found: list[SsoProfile] = []
    for section in parser.sections():
        if section != "default" and not section.startswith("profile "):
            continue
        name = section.removeprefix("profile ")
        url = parser.get(section, "sso_start_url", fallback="")
        session = parser.get(section, "sso_session", fallback="")
        if session and not url:
            url = parser.get(f"sso-session {session}", "sso_start_url", fallback="")
        if not url:
            continue  # not an SSO profile
        found.append(
            SsoProfile(
                name,
                parser.get(section, "sso_account_id", fallback=""),
                parser.get(section, "region", fallback=""),
                url in urls,
            )
        )
    return sorted(found, key=lambda profile: profile.name)


def sso_accounts() -> list[Account]:
    """The SSO profiles that are signed in, as accounts of the integrations
    without having been added: they count as plugged in, unless an account
    already uses the profile."""
    used = {account.fields.get("profile") for account in accounts("aws")}
    return [
        Account(
            f"sso-{profile.name}",
            "aws",
            profile.name,
            {"profile": profile.name, "regions": profile.region or "us-east-1"},
        )
        for profile in sso_profiles()
        if profile.signed_in and profile.name not in used
    ]


def integrations_directory() -> Path:
    return config_directory() / "integrations"


def account_directory(account: str) -> Path:
    return integrations_directory() / account


def kubeconfig_path(account: str) -> Path:
    return account_directory(account) / "kubeconfig"


def kubeconfig_files() -> list[str]:
    """The kubeconfigs the accounts wrote, for the cluster layer to read."""
    return [
        str(kubeconfig_path(account.id))
        for account in _accounts.values()
        if kubeconfig_path(account.id).is_file()
    ]


def environment(account: Account, values: Mapping[str, str]) -> dict[str, str]:
    """The variables the cloud's programs need to act with these keys."""
    base = account_directory(account.id)
    if account.provider == "aws":
        first = regions(values)[0]
        if values.get("profile"):  # the keys stay in the files of the AWS CLI
            return {
                "AWS_PROFILE": values["profile"],
                "AWS_DEFAULT_REGION": first,
            }
        env = {
            "AWS_ACCESS_KEY_ID": values["access_key_id"],
            "AWS_SECRET_ACCESS_KEY": values["secret_access_key"],
            "AWS_DEFAULT_REGION": first,
        }
        if values.get("session_token"):
            env["AWS_SESSION_TOKEN"] = values["session_token"]
        return env
    if account.provider == "azure":
        return {
            "AZURE_CONFIG_DIR": str(base / "azure"),
            "AZURE_TENANT_ID": values["tenant_id"],
            "AZURE_CLIENT_ID": values["client_id"],
            "AZURE_CLIENT_SECRET": values["client_secret"],
            "AAD_SERVICE_PRINCIPAL_CLIENT_ID": values["client_id"],
            "AAD_SERVICE_PRINCIPAL_CLIENT_SECRET": values["client_secret"],
        }
    return {
        "CLOUDSDK_CONFIG": str(base / "gcloud"),
        "CLOUDSDK_CORE_PROJECT": values["project_id"],
        "GOOGLE_APPLICATION_CREDENTIALS": values["key_file"],
    }


def exec_environment(env: Mapping[str, str] | None) -> dict[str, str] | None:
    """The environment of a sign-in program of a kubeconfig, with the keys of
    the account it names; unchanged for any other program."""
    if env is None or ACCOUNT_VARIABLE not in env:
        return None if env is None else dict(env)
    account = _accounts.get(env[ACCOUNT_VARIABLE])
    if account is None or not has_keys(account):
        return dict(env)
    return {**env, **environment(account, values_of(account))}


def regions(values: Mapping[str, str]) -> list[str]:
    regions = [part.strip() for part in values.get("regions", "").split(",")]
    return [region for region in regions if region] or ["us-east-1"]


def missing(provider: str, values: Mapping[str, str]) -> str | None:
    """The label of the first field that is required and empty."""
    if provider == "aws":  # a profile, or both keys
        if values.get("profile", "").strip():
            return None
        for key, label in (
            ("access_key_id", "Access key ID"),
            ("secret_access_key", "Secret access key"),
        ):
            if not values.get(key, "").strip():
                return label
        return None
    return next(
        (
            item.label
            for item in PROVIDERS[provider].fields
            if not item.optional and not (values.get(item.key) or item.default).strip()
        ),
        None,
    )


def _run(command: list[str], env: Mapping[str, str] | None = None) -> str:
    """Run a program of the cloud and give what it printed; the message of a
    failure never repeats the command line, which can hold a secret."""
    program = find_program(command[0])
    if program is None:
        raise IntegrationError(f"{command[0]} is not installed")
    try:
        result = subprocess.run(
            [program, *command[1:]],
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            env={**os.environ, **(env or {})},
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise IntegrationError(f"{command[0]} timed out") from error
    except OSError as error:
        raise IntegrationError(
            f"Could not start {command[0]}: {error.strerror}"
        ) from error
    if result.returncode != 0:
        detail = redact(result.stderr.strip() or result.stdout.strip())
        raise IntegrationError(first_line(detail) or f"{command[0]} failed")
    return result.stdout


def _json(output: str) -> object:
    try:
        return json.loads(output)
    except ValueError as error:
        raise IntegrationError(
            "The cloud answered with something unexpected"
        ) from error


def _items(document: object) -> list[dict[str, object]]:
    return (
        [item for item in document if isinstance(item, dict)]
        if isinstance(document, list)
        else []
    )


def discover(account: Account, values: Mapping[str, str]) -> list[Found]:
    """The clusters the cloud lists for these keys."""
    provider = account.provider
    problem = missing(provider, values)
    if problem:
        raise IntegrationError(f"{problem} is required")
    for program in PROVIDERS[provider].programs:
        if find_program(program) is None:
            raise IntegrationError(f"{program} is not installed")
    env = environment(account, values)
    if provider == "aws":
        found: list[Found] = []
        for region in regions(values):
            command = ["aws", "eks", "list-clusters", "--region", region]
            document = _json(_run([*command, "--output", "json"], env))
            names = document.get("clusters") if isinstance(document, dict) else None
            found += [Found("aws", str(name), region) for name in names or []]
        return found
    if provider == "azure":
        login = ["az", "login", "--service-principal", "--username"]
        _run(
            [
                *login, values["client_id"],
                "--password", values["client_secret"],
                "--tenant", values["tenant_id"],
            ],
            env,
        )  # fmt: skip
        listed = _json(
            _run(
                [
                    "az",
                    "aks",
                    "list",
                    "--subscription",
                    values["subscription_id"],
                    "--output",
                    "json",
                ],
                env,
            )  # fmt: skip
        )
        return [
            Found(
                "azure",
                str(item.get("name", "")),
                str(item.get("location", "")),
                str(item.get("resourceGroup", "")),
            )
            for item in _items(listed)
            if item.get("name")
        ]
    activate = ["gcloud", "auth", "activate-service-account", "--key-file"]
    _run([*activate, values["key_file"]], env)
    listed = _json(
        _run(
            [
                "gcloud",
                "container",
                "clusters",
                "list",
                "--project",
                values["project_id"],
                "--format",
                "json",
            ],
            env,
        )  # fmt: skip
    )
    return [
        Found("gcp", str(item.get("name", "")), str(item.get("location", "")))
        for item in _items(listed)
        if item.get("name")
    ]


def plug(
    found: list[Found], account: Account, values: Mapping[str, str]
) -> list[Found]:
    """Write the clusters to the kubeconfig of the account; the first one that
    cannot be written raises IntegrationError."""
    if not found:
        return []
    target = kubeconfig_path(account.id)
    target.parent.mkdir(parents=True, exist_ok=True)
    env = {**environment(account, values), "KUBECONFIG": str(target)}
    for cluster in found:
        if account.provider == "aws":
            command = [
                "aws", "eks", "update-kubeconfig", "--name", cluster.name,
                "--region", cluster.place, "--kubeconfig", str(target),
                "--alias", cluster.context,
            ]  # fmt: skip
        elif account.provider == "azure":
            command = [
                "az", "aks", "get-credentials", "--name", cluster.name,
                "--resource-group", cluster.group,
                "--subscription", values["subscription_id"],
                "--file", str(target), "--overwrite-existing",
            ]  # fmt: skip
        else:
            command = [
                "gcloud", "container", "clusters", "get-credentials", cluster.name,
                "--location", cluster.place, "--project", values["project_id"],
            ]  # fmt: skip
        _run(command, env)
    if account.provider == "azure":
        convert = ["kubelogin", "convert-kubeconfig", "--login", "spn"]
        _run([*convert, "--kubeconfig", str(target)], env)
    _name_the_account(target, account.id)
    return found


def _name_the_account(path: Path, account: str) -> None:
    """Add to the sign-in program of every user of a kubeconfig the name of the
    account, so the app knows which keys to hand to it.

    No key is written.
    """
    try:
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as error:
        raise IntegrationError(f"Could not read the kubeconfig: {error}") from error
    for item in document.get("users") or []:
        sign_in = (item.get("user") or {}).get("exec")
        if not isinstance(sign_in, dict):
            continue
        variables = [
            entry
            for entry in sign_in.get("env") or []
            if entry.get("name") != ACCOUNT_VARIABLE
        ]
        sign_in["env"] = [*variables, {"name": ACCOUNT_VARIABLE, "value": account}]
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def remove(account: Account) -> None:
    """Forget an account: its keys, its clusters and what its programs kept."""
    _secrets.pop(account.id, None)
    _accounts.pop(account.id, None)
    shutil.rmtree(account_directory(account.id), ignore_errors=True)
