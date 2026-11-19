import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import subprocess

import pytest
from kubescope.sdk.models import ClusterResource
from PySide6.QtCore import QCoreApplication, QEvent

from kubescope import cluster, plugin_updates
from kubescope.cluster import ClusterError
from kubescope.dialogs.plugin_update_dialog import PluginUpdateDialog
from tests.qt import get_application

application = get_application()


@pytest.fixture
def eks(monkeypatch):
    monkeypatch.setattr(
        cluster, "_eks_target", lambda _c, flag="--cluster-name": [flag, "prod"]
    )
    monkeypatch.setattr(cluster, "_context_env", lambda _c: None)
    monkeypatch.setattr(plugin_updates, "program_missing", lambda _p: False)


def test_the_eks_update_names_the_addon_version_and_conflict_rule(eks) -> None:
    arguments = plugin_updates.eks_update_arguments(
        "ctx", "vpc-cni", "v1.2.3-eksbuild.1"
    )
    assert arguments[:3] == ["aws", "eks", "update-addon"]
    assert arguments[5:7] == ["--addon-name", "vpc-cni"]
    assert "--addon-version" in arguments and "NONE" in arguments


@pytest.mark.parametrize(
    ("addon", "version", "conflicts"),
    [
        ("a b", "v1", "NONE"),
        ("vpc-cni", "", "NONE"),
        ("vpc-cni", "v1", "ALL"),
        ("vpc-cni", "v1; rm", "NONE"),
    ],
)
def test_the_eks_update_refuses_what_is_not_a_name_a_version_or_a_rule(
    eks, addon, version, conflicts
) -> None:
    with pytest.raises(ClusterError):
        plugin_updates.eks_update_arguments("ctx", addon, version, conflicts)


def test_the_versions_are_those_eks_lists_without_repeats(eks, monkeypatch) -> None:
    document = {
        "addons": [
            {
                "addonVersions": [
                    {"addonVersion": "v2"},
                    {"addonVersion": "v1"},
                    {"addonVersion": "v2"},
                    {},
                ]
            }
        ]
    }
    monkeypatch.setattr(cluster, "_eks_json", lambda *_a, **_k: document)
    assert plugin_updates.eks_addon_versions("ctx", "vpc-cni") == ["v2", "v1"]
    with pytest.raises(ClusterError):
        plugin_updates.eks_addon_versions("ctx", "bad name")


def test_the_helm_upgrade_keeps_the_values_and_reads_the_repository() -> None:
    arguments = plugin_updates.helm_upgrade_arguments(
        "ctx", "ops", "web", "nginx", "1.2.3", "https://charts.example.com"
    )
    assert arguments[:6] == ["helm", "--kube-context", "ctx", "upgrade", "web", "nginx"]
    assert arguments[8:10] == ["--repo", "https://charts.example.com"]
    assert "--reuse-values" in arguments and "--version" in arguments
    plain = plugin_updates.helm_upgrade_arguments(
        "ctx", "ops", "web", "repo/nginx", reuse_values=False, values_file="v.yaml"
    )
    assert "--reset-values" in plain and "--repo" not in plain
    assert plain[plain.index("--values") : plain.index("--values") + 2] == [
        "--values",
        "v.yaml",
    ]
    assert "helm --kube-context ctx upgrade web" in plugin_updates.commands(arguments)


@pytest.mark.parametrize(
    "bad",
    [
        {"chart": ""},
        {"chart": "a b"},
        {"version": "1 2"},
        {"repository": "http://insecure"},
        {"values_file": "a b"},
        {"release": "x y"},
    ],
)
def test_the_helm_upgrade_refuses_odd_inputs(bad) -> None:
    inputs = {
        "release": "web",
        "chart": "nginx",
        "version": "",
        "repository": "",
        "values_file": "",
    }
    inputs.update(bad)
    with pytest.raises(ClusterError):
        plugin_updates.helm_upgrade_arguments(
            "ctx",
            "ops",
            inputs["release"],
            inputs["chart"],
            inputs["version"],
            inputs["repository"],
            True,
            inputs["values_file"],
        )


def test_run_update_gives_the_keys_and_reports_failures(
    monkeypatch,
) -> None:
    seen = {}

    def run(program, environment):
        seen.update(program=program, environment=environment)
        return subprocess.CompletedProcess(program, 0, " done \n", "")

    monkeypatch.setattr(plugin_updates, "_run", run)
    monkeypatch.setattr(cluster, "context_environment", lambda _c: {"K": "v"})
    monkeypatch.setattr(cluster, "_kubeconfig_files", ["/a", "/b"])
    assert plugin_updates.run_update("ctx", ["helm", "upgrade"]) == "done"
    assert seen["environment"]["K"] == "v" and "KUBECONFIG" in seen["environment"]
    plugin_updates.run_update("ctx", ["aws", "eks"])
    assert "KUBECONFIG" not in seen["environment"]

    monkeypatch.setattr(
        plugin_updates,
        "_run",
        lambda *_a: subprocess.CompletedProcess([], 1, "", "denied"),
    )
    with pytest.raises(ClusterError, match="denied"):
        plugin_updates.run_update("ctx", ["helm", "upgrade"])

    def missing(*_a):
        raise OSError("no helm")

    monkeypatch.setattr(plugin_updates, "_run", missing)
    with pytest.raises(ClusterError, match="no helm"):
        plugin_updates.run_update("ctx", ["helm", "upgrade"])

    def slow(*_a):
        raise subprocess.TimeoutExpired("helm", 1)

    monkeypatch.setattr(plugin_updates, "_run", slow)
    with pytest.raises(ClusterError, match="timed out"):
        plugin_updates.run_update("ctx", ["helm", "upgrade"])


def test_each_dialog_asks_for_what_its_kind_takes(eks) -> None:
    addon = ClusterResource("", "Addon", "vpc-cni", ("ACTIVE", "v1", "EKS"), "1d")
    dialog = PluginUpdateDialog(None, "ctx", addon, ["v2", "v1"])
    assert dialog.eks_version.currentText() == "v2"
    assert dialog.update_button.isEnabled()
    assert "--addon-version v2" in dialog.command.toPlainText()
    dialog.eks_version.setEditText("")
    assert not dialog.update_button.isEnabled() and dialog.problem.text()

    release = ClusterResource(
        "ops", "HelmRelease", "web", ("Deployed", "chart 1", "Helm"), "1d"
    )
    helm = PluginUpdateDialog(
        None, "ctx", release, ["2.0", "1.0"], "https://repo.example"
    )
    assert helm.chart.text() == "web" and helm.arguments[0] == "helm"
    assert helm.helm_version.currentText() == "2.0"
    assert helm.repository.text() == "https://repo.example"
    helm.repository.setText("http://x")
    assert not helm.update_button.isEnabled()
    helm.repository.setText("https://x.example")
    helm.reuse.setChecked(False)
    assert "--reset-values" in helm.command.toPlainText()
    for widget in (dialog, helm):
        widget.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete.value)


def test_the_versions_are_asked_in_the_region_of_the_cluster(monkeypatch) -> None:
    seen = {}
    monkeypatch.setattr(
        cluster,
        "_eks_target",
        lambda _c: ["--cluster-name", "prod", "--region", "sa-east-1"],
    )
    monkeypatch.setattr(cluster, "_context_env", lambda _c: None)

    def eks_json(subcommand, target, *_a, **_k):
        seen.update(subcommand=subcommand, target=target)
        return {}

    monkeypatch.setattr(cluster, "_eks_json", eks_json)
    assert plugin_updates.eks_addon_versions("ctx", "vpc-cni") == []
    assert seen["target"] == ["--addon-name", "vpc-cni", "--region", "sa-east-1"]


def test_the_update_runs_the_program_with_the_timeout_and_environment(
    monkeypatch,
) -> None:
    seen = {}

    def run_process(program, timeout, env):
        seen.update(program=program, timeout=timeout, env=env)
        return subprocess.CompletedProcess(program, 0, "ok", "")

    monkeypatch.setattr(cluster, "_run_process", run_process)
    monkeypatch.setattr(cluster, "context_environment", lambda _c: {})
    assert plugin_updates.run_update("ctx", ["aws", "eks"]) == "ok"
    assert seen["timeout"] == plugin_updates.UPDATE_TIMEOUT
    assert seen["program"] == ["aws", "eks"]


def test_the_dialog_selects_the_latest_version_among_the_offered(eks) -> None:
    addon = ClusterResource("", "Addon", "vpc-cni", ("A", "v1", "v2", "EKS"), "1d")
    dialog = PluginUpdateDialog(None, "ctx", addon, ["v3", "v2", "v1"])
    assert dialog.eks_version.currentText() == "v2"
    dialog.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete.value)


def test_without_the_program_the_dialog_shows_the_command_but_cannot_run_it(
    eks, monkeypatch
) -> None:
    monkeypatch.setattr(plugin_updates, "program_missing", lambda program: True)
    values = ("Deployed", "chart 1", "Helm")
    release = ClusterResource("ops", "HelmRelease", "web", values, "1d")
    dialog = PluginUpdateDialog(None, "ctx", release, ["2.0"])
    assert "helm --kube-context ctx upgrade web" in dialog.command.toPlainText()
    assert not dialog.update_button.isEnabled() and dialog.arguments == []
    assert "helm is not installed" in dialog.problem.text()
    monkeypatch.setattr(plugin_updates, "program_missing", lambda program: False)
    dialog.reuse.setChecked(False)  # a change asks again: now it can run
    assert dialog.update_button.isEnabled() and dialog.arguments[0] == "helm"
    dialog.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete.value)


def test_a_program_is_missing_when_it_is_not_found_outside_a_flatpak(
    monkeypatch,
) -> None:
    monkeypatch.setattr(plugin_updates, "in_flatpak", lambda: False)
    monkeypatch.setattr(plugin_updates, "find_program", lambda _p: None)
    assert plugin_updates.program_missing("helm")
    monkeypatch.setattr(plugin_updates, "find_program", lambda _p: "/usr/bin/helm")
    assert not plugin_updates.program_missing("helm")
    monkeypatch.setattr(plugin_updates, "find_program", lambda _p: None)
    monkeypatch.setattr(plugin_updates, "in_flatpak", lambda: True)
    assert not plugin_updates.program_missing("helm")  # the host's, not seen here


def test_an_aks_extension_asks_for_a_version_and_builds_the_az_command(
    eks, monkeypatch
) -> None:
    values = ("Succeeded", "1.0.0", "—", "AKS")
    row = ClusterResource("", "AksExtension", "flux", values, "1d")
    dialog = PluginUpdateDialog(None, "ctx", row, [], target=("prod", "rg1"))
    assert not dialog.update_button.isEnabled()  # no version typed yet
    dialog.eks_version.setEditText("1.3.0")
    command = dialog.command.toPlainText()
    assert command.startswith("az k8s-extension update --name flux")
    assert "--resource-group rg1" in command and "--version 1.3.0" in command
    assert dialog.update_button.isEnabled()
    dialog.deleteLater()
    QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete.value)
