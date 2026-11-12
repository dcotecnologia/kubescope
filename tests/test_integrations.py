import json
import os
import subprocess
from types import SimpleNamespace

import pytest
import yaml

from kubescope import integrations
from kubescope.integrations import Account, Found, IntegrationError

AWS = {
    "access_key_id": "AKIA",
    "secret_access_key": "secret",
    "session_token": "token",
    "regions": "us-east-1, eu-west-1",
}
PROFILE = {"profile": "work", "regions": "us-east-1"}
AZURE = {
    "tenant_id": "t",
    "client_id": "c",
    "client_secret": "s",
    "subscription_id": "sub",
}
GCP = {"project_id": "proj", "key_file": "/keys/sa.json"}


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    monkeypatch.setattr(integrations, "_accounts", {})
    monkeypatch.setattr(integrations, "_secrets", {})
    monkeypatch.setattr(integrations, "find_program", lambda name: f"/bin/{name}")


class Calls:
    """Stands in for the programs of the clouds, answering by their command."""

    def __init__(self, answers: dict[str, str]) -> None:
        self.answers = answers
        self.commands: list[list[str]] = []
        self.envs: list[dict[str, str]] = []

    def __call__(self, command, env=None):
        self.commands.append(command)
        self.envs.append(dict(env or {}))
        return next((v for k, v in self.answers.items() if k in " ".join(command)), "")


def test_an_account_keeps_its_secrets_in_memory_and_the_rest_to_be_saved() -> None:
    account = integrations.add_account("aws", "work", AWS)

    assert account.id.startswith("aws-") and account.name == "work"
    assert "secret_access_key" not in account.saved()["fields"]
    assert account.fields["access_key_id"] == "AKIA"
    assert integrations.values_of(account)["secret_access_key"] == "secret"
    assert integrations.has_keys(account)
    assert integrations.accounts("aws") == [account]
    assert integrations.accounts("gcp") == []
    assert integrations.account_named(account.id) is account

    changed = integrations.update_account(account, {**AWS, "regions": "sa-east-1"})
    assert integrations.account_named(account.id) is changed
    assert changed.fields["regions"] == "sa-east-1"


def test_the_accounts_saved_are_known_again_without_their_keys() -> None:
    saved = [
        {"id": "aws-1", "provider": "aws", "name": "a", "fields": {"profile": "w"}},
        {"id": "gcp-1", "provider": "gcp", "name": "g", "fields": GCP},
        {"id": "dead-1", "provider": "other", "name": "x", "fields": {}},
        {"id": "aws-2", "provider": "aws", "name": "k", "fields": {"regions": "x"}},
    ]
    accounts = integrations.load(saved)

    assert [account.id for account in accounts] == ["aws-1", "gcp-1", "aws-2"]
    assert integrations.has_keys(accounts[0])  # a profile has no keys to type
    assert integrations.has_keys(accounts[1])  # nor a key file
    assert not integrations.has_keys(accounts[2])  # keys of an earlier run are gone
    azure = Account("az-1", "azure", "n", {})
    assert not integrations.has_keys(azure)


def test_the_profiles_of_the_aws_cli_are_listed_with_their_account(
    monkeypatch, tmp_path
) -> None:
    config = tmp_path / "config"
    config.write_text(
        "[default]\nregion = us-east-1\n"
        "[profile sso]\nsso_account_id = 123456789012\n"
        "[profile role]\nrole_arn = arn:aws:iam::210987654321:role/x\n"
        "[sso-session shared]\nsso_region = us-east-1\n"
        "[profile plain]\nregion = eu-west-1\n"
    )
    credentials = tmp_path / "credentials"
    credentials.write_text("[keys]\naws_access_key_id = A\n[sso]\nx = 1\n")
    monkeypatch.setenv("AWS_CONFIG_FILE", str(config))
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", str(credentials))

    assert integrations.aws_profiles() == [
        ("default", ""),
        ("keys", ""),
        ("plain", ""),
        ("role", "210987654321"),
        ("sso", "123456789012"),
    ]

    broken = tmp_path / "broken"
    broken.write_text("no = section\n")  # a file the parser refuses
    monkeypatch.setenv("AWS_CONFIG_FILE", str(broken))
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", str(tmp_path / "missing"))
    assert integrations.aws_profiles() == []


def test_the_environment_hands_each_cloud_its_keys() -> None:
    aws = Account("aws-1", "aws", "a", {})
    env = integrations.environment(aws, AWS)
    assert env["AWS_ACCESS_KEY_ID"] == "AKIA" and env["AWS_SESSION_TOKEN"] == "token"
    assert env["AWS_DEFAULT_REGION"] == "us-east-1"
    bare = integrations.environment(aws, {**AWS, "session_token": "", "regions": " "})
    assert "AWS_SESSION_TOKEN" not in bare and bare["AWS_DEFAULT_REGION"] == "us-east-1"
    assert integrations.environment(aws, PROFILE) == {
        "AWS_PROFILE": "work",
        "AWS_DEFAULT_REGION": "us-east-1",
    }
    azure = integrations.environment(Account("az-1", "azure", "n", {}), AZURE)
    assert azure["AZURE_CONFIG_DIR"].endswith(os.path.join("az-1", "azure"))
    assert azure["AAD_SERVICE_PRINCIPAL_CLIENT_SECRET"] == "s"
    gcp = integrations.environment(Account("gcp-1", "gcp", "g", {}), GCP)
    assert gcp["GOOGLE_APPLICATION_CREDENTIALS"] == "/keys/sa.json"


def test_a_sign_in_program_gets_the_keys_of_the_account_it_names() -> None:
    account = integrations.add_account("aws", "work", AWS)
    named = {integrations.ACCOUNT_VARIABLE: account.id, "A": "1"}

    assert integrations.exec_environment(None) is None
    assert integrations.exec_environment({"A": "1"}) == {"A": "1"}
    merged = integrations.exec_environment(named)
    assert merged is not None and merged["AWS_ACCESS_KEY_ID"] == "AKIA"
    assert merged["A"] == "1"
    unknown = {integrations.ACCOUNT_VARIABLE: "nobody"}
    assert integrations.exec_environment(unknown) == unknown
    integrations._secrets.clear()  # the keys of the run are gone
    assert integrations.exec_environment(named) == named


def test_missing_names_the_first_required_field_left_empty() -> None:
    assert integrations.missing("aws", {}) == "Access key ID"
    assert integrations.missing("aws", {"access_key_id": "a"}) == "Secret access key"
    assert integrations.missing("aws", AWS) is None
    assert integrations.missing("aws", PROFILE) is None
    assert integrations.missing("azure", {"tenant_id": "t"}) == "Client ID"
    assert integrations.missing("gcp", GCP) is None


def test_aws_lists_the_clusters_of_every_region(monkeypatch) -> None:
    calls = Calls({"us-east-1": '{"clusters": ["a"]}', "eu-west-1": "{}"})
    monkeypatch.setattr(integrations, "_run", calls)

    found = integrations.discover(Account("aws-1", "aws", "w", {}), AWS)

    assert found == [Found("aws", "a", "us-east-1")]
    assert found[0].context == "a.us-east-1"
    assert calls.envs[0]["AWS_ACCESS_KEY_ID"] == "AKIA"
    assert integrations.discover(Account("aws-1", "aws", "w", {}), PROFILE)


def test_azure_signs_in_then_lists_the_clusters(monkeypatch) -> None:
    listed = '[{"name": "k", "location": "eastus", "resourceGroup": "rg"}, {}, 3]'
    calls = Calls({"aks list": listed})
    monkeypatch.setattr(integrations, "_run", calls)

    found = integrations.discover(Account("az-1", "azure", "n", {}), AZURE)

    assert found == [Found("azure", "k", "eastus", "rg")]
    assert calls.commands[0][:3] == ["az", "login", "--service-principal"]


def test_google_cloud_activates_the_key_then_lists_the_clusters(monkeypatch) -> None:
    calls = Calls({"clusters list": '[{"name": "g", "location": "us-central1-a"}, {}]'})
    monkeypatch.setattr(integrations, "_run", calls)

    found = integrations.discover(Account("gcp-1", "gcp", "g", {}), GCP)

    assert found == [Found("gcp", "g", "us-central1-a")]
    assert calls.commands[0][:3] == ["gcloud", "auth", "activate-service-account"]
    assert integrations._items({"not": "a list"}) == []


def test_discover_refuses_missing_fields_and_programs(monkeypatch) -> None:
    account = Account("aws-1", "aws", "w", {})
    with pytest.raises(IntegrationError, match="Access key ID is required"):
        integrations.discover(account, {})
    monkeypatch.setattr(integrations, "find_program", lambda name: None)
    with pytest.raises(IntegrationError, match="aws is not installed"):
        integrations.discover(account, AWS)


def test_an_answer_that_is_not_json_is_told(monkeypatch) -> None:
    monkeypatch.setattr(integrations, "_run", Calls({"list-clusters": "nope"}))
    with pytest.raises(IntegrationError, match="unexpected"):
        integrations.discover(Account("aws-1", "aws", "w", {}), AWS)


def test_plug_writes_the_clusters_and_names_the_account_in_the_kubeconfig(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path))
    account = Account("aws-1", "aws", "w", {})
    target = integrations.kubeconfig_path("aws-1")
    document = {"users": [{"name": "u", "user": {"exec": {"command": "aws"}}}, {}]}

    def writes(command, env=None):
        target.write_text(yaml.safe_dump(document))
        return ""

    monkeypatch.setattr(integrations, "_run", writes)

    assert integrations.plug([], account, AWS) == []
    found = [Found("aws", "a", "us-east-1")]
    assert integrations.plug(found, account, AWS) == found
    assert integrations.plug(found, account, AWS) == found  # again: named once

    users = yaml.safe_load(target.read_text())["users"]
    assert users[0]["user"]["exec"]["env"] == [
        {"name": integrations.ACCOUNT_VARIABLE, "value": "aws-1"}
    ]
    assert "AKIA" not in target.read_text()  # no key is written
    assert integrations.kubeconfig_files() == []  # the account is not known yet
    integrations.load([account.saved()])
    assert integrations.kubeconfig_files() == [str(target)]


def test_plug_asks_each_cloud_for_the_credentials_of_a_cluster(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path))
    calls = Calls({})
    monkeypatch.setattr(integrations, "_run", calls)
    monkeypatch.setattr(integrations, "_name_the_account", lambda *_a: None)

    integrations.plug(
        [Found("aws", "a", "us-east-1")], Account("aws-1", "aws", "w", {}), AWS
    )
    assert calls.commands[0][:3] == ["aws", "eks", "update-kubeconfig"]
    assert calls.envs[0]["KUBECONFIG"].endswith("kubeconfig")

    integrations.plug(
        [Found("azure", "k", "eastus", "rg")], Account("az-1", "azure", "n", {}), AZURE
    )
    assert calls.commands[-2][:3] == ["az", "aks", "get-credentials"]
    assert calls.commands[-1][:2] == ["kubelogin", "convert-kubeconfig"]

    integrations.plug(
        [Found("gcp", "g", "us-central1")], Account("gcp-1", "gcp", "g", {}), GCP
    )
    assert calls.commands[-1][:4] == [
        "gcloud",
        "container",
        "clusters",
        "get-credentials",
    ]


def test_a_kubeconfig_that_cannot_be_read_is_told(tmp_path) -> None:
    with pytest.raises(IntegrationError, match="Could not read the kubeconfig"):
        integrations._name_the_account(tmp_path / "missing", "aws-1")
    bad = tmp_path / "bad"
    bad.write_text("a: [")
    with pytest.raises(IntegrationError, match="Could not read the kubeconfig"):
        integrations._name_the_account(bad, "aws-1")
    empty = tmp_path / "empty"
    empty.write_text("")
    integrations._name_the_account(empty, "aws-1")  # nothing to name


def test_removing_an_account_forgets_its_keys_and_its_files(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path))
    account = integrations.add_account("aws", "work", AWS)
    folder = integrations.account_directory(account.id)
    (folder / "azure").mkdir(parents=True)
    (folder / "kubeconfig").write_text("x")
    assert integrations.integrations_directory().name == "integrations"

    integrations.remove(account)

    assert not folder.exists()
    assert integrations.accounts() == [] and integrations.values_of(account) == {
        **account.fields
    }


def _completed(code: int, out: str = "", err: str = ""):
    return SimpleNamespace(returncode=code, stdout=out, stderr=err)


def test_run_gives_the_output_and_tells_a_failure_without_the_command(
    monkeypatch,
) -> None:
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _completed(0, "ok"))
    assert integrations._run(["aws", "x"], {"A": "1"}) == "ok"

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: _completed(1, "", "denied\nmore"),
    )
    with pytest.raises(IntegrationError) as error:
        integrations._run(["az", "login", "--password", "hunter2"])
    assert "hunter2" not in str(error.value) and "denied" in str(error.value)

    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _completed(2))
    with pytest.raises(IntegrationError, match="az failed"):
        integrations._run(["az"])

    def late(*_a, **_k):
        raise subprocess.TimeoutExpired("az", 1)

    monkeypatch.setattr(subprocess, "run", late)
    with pytest.raises(IntegrationError, match="timed out"):
        integrations._run(["az"])

    def broken(*_a, **_k):
        raise OSError(2, "No such file")

    monkeypatch.setattr(subprocess, "run", broken)
    with pytest.raises(IntegrationError, match="Could not start az"):
        integrations._run(["az"])

    monkeypatch.setattr(integrations, "find_program", lambda name: None)
    with pytest.raises(IntegrationError, match="not installed"):
        integrations._run(["az"])


def _sso_files(monkeypatch, tmp_path, cached_until: str = "2999-01-01T00:00:00Z"):
    """An AWS config with SSO profiles of both styles and the cache of the
    portals."""
    monkeypatch.setenv("HOME", str(tmp_path))
    config = tmp_path / ".aws" / "config"
    cache = tmp_path / ".aws" / "sso" / "cache"
    cache.mkdir(parents=True)
    config.write_text(
        "[default]\nregion = us-east-1\n"
        "[profile modern]\nsso_session = shared\nsso_account_id = 111122223333\n"
        "region = sa-east-1\n"
        "[profile legacy]\nsso_start_url = https://old.awsapps.com/start\n"
        "sso_account_id = 444455556666\n"
        "[profile renewed]\nsso_session = renewing\nsso_account_id = 777788889999\n"
        "[profile lapsed]\nsso_session = lapsing\nsso_account_id = 000011112222\n"
        "[sso-session shared]\nsso_start_url = https://new.awsapps.com/start\n"
        "[sso-session renewing]\nsso_start_url = https://renew.awsapps.com/start\n"
        "[sso-session lapsing]\nsso_start_url = https://lapse.awsapps.com/start\n"
        "[profile plain]\nregion = eu-west-1\n"
        "[services other]\nx = 1\n"
    )
    past, future = "2001-01-01T00:00:00Z", "2999-01-01T00:00:00Z"
    portals = {
        "a.json": ("https://new.awsapps.com/start", cached_until, {}),
        "old.json": ("https://old.awsapps.com/start", past, {}),
        # the access token ran out, but the CLI renews it by itself
        "renew.json": (
            "https://renew.awsapps.com/start",
            past,
            {"refreshToken": "x", "registrationExpiresAt": future},
        ),
        # and here the registration with the portal ran out too
        "lapse.json": (
            "https://lapse.awsapps.com/start",
            past,
            {"refreshToken": "x", "registrationExpiresAt": past},
        ),
    }
    for name, (url, expires, more) in portals.items():
        document = {"startUrl": url, "expiresAt": expires, **more}
        (cache / name).write_text(json.dumps(document))
    for name, text in (
        ("broken.json", "{not json"),
        ("list.json", "[]"),
        ("nourl.json", '{"expiresAt": "2999-01-01T00:00:00Z"}'),
    ):
        (cache / name).write_text(text)
    return config


def test_the_sso_profiles_are_found_with_whether_they_are_signed_in(
    monkeypatch, tmp_path
) -> None:
    config = _sso_files(monkeypatch, tmp_path)
    monkeypatch.setenv("AWS_CONFIG_FILE", str(config))

    assert integrations.sso_profiles() == [
        integrations.SsoProfile("lapsed", "000011112222", "", False),
        integrations.SsoProfile("legacy", "444455556666", "", False),  # expired
        integrations.SsoProfile("modern", "111122223333", "sa-east-1", True),
        integrations.SsoProfile("renewed", "777788889999", "", True),  # renewable
    ]

    monkeypatch.setenv("AWS_CONFIG_FILE", str(tmp_path / "missing"))
    assert integrations.sso_profiles() == []
    broken = tmp_path / "broken"
    broken.write_text("no = section\n")
    monkeypatch.setenv("AWS_CONFIG_FILE", str(broken))
    assert integrations.sso_profiles() == []


def test_a_sign_in_that_expired_or_has_no_date_is_not_a_sign_in() -> None:
    assert integrations._expired(None) and integrations._expired("soon")
    assert integrations._expired("2001-01-01T00:00:00UTC")
    assert not integrations._expired("2999-01-01T00:00:00")  # no zone: UTC


def test_the_signed_in_sso_profiles_count_as_accounts_unless_one_uses_them(
    monkeypatch, tmp_path
) -> None:
    config = _sso_files(monkeypatch, tmp_path)
    monkeypatch.setenv("AWS_CONFIG_FILE", str(config))

    found = integrations.sso_accounts()

    assert [(a.id, a.name, a.fields) for a in found] == [
        ("sso-modern", "modern", {"profile": "modern", "regions": "sa-east-1"}),
        ("sso-renewed", "renewed", {"profile": "renewed", "regions": "us-east-1"}),
    ]
    assert integrations.has_keys(found[0])  # a profile needs no keys typed
    integrations.add_account("aws", "mine", {"profile": "modern"})
    assert [a.name for a in integrations.sso_accounts()] == ["renewed"]  # not "modern"
