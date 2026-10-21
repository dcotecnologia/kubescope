import pytest

from kubescope.models import (
    POD_SORT_COLUMNS,
    SORT_COLUMNS,
    DetailRow,
    EventInfo,
    PodInfo,
    Workload,
    detail_link,
    detail_sections,
    event_link,
    format_age,
    format_bytes,
    format_cpu,
    format_memory,
    parse_cpu,
    parse_memory,
    pod_sort_key,
    workload_sort_key,
)


@pytest.mark.parametrize(
    ("ready", "desired", "expected"),
    [
        (3, 3, "Healthy"),
        (1, 3, "Degraded"),
        (0, 2, "Unavailable"),
        (0, 0, "Scaled to zero"),
    ],
)
def test_workload_status(ready: int, desired: int, expected: str) -> None:
    workload = Workload("default", "Deployment", "api", ready, desired, "1h")

    assert workload.status == expected


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [(0, "<1m"), (59, "<1m"), (60, "1m"), (3600, "1h"), (86400, "1d")],
)
def test_format_age(seconds: int, expected: str) -> None:
    assert format_age(seconds) == expected


def test_parse_quantities() -> None:
    from kubescope.models import format_bytes, format_cores, parse_cpu, parse_memory

    assert parse_cpu("250m") == 0.25
    assert parse_cpu("2") == 2.0
    assert parse_cpu("1500000n") == 0.0015
    assert parse_cpu(None) == 0.0
    assert parse_memory("512Mi") == 512 * 2**20
    assert parse_memory("2Gi") == 2 * 2**30
    assert parse_memory("1G") == 1e9
    assert parse_memory("129e6") == 129e6
    assert format_cores(3.46) == "3.5"
    assert format_bytes(3 * 2**30) == "3.0 GiB"
    assert format_bytes(512 * 2**20) == "512 MiB"


def test_age_seconds_inverts_format_age() -> None:
    from kubescope.models import age_seconds

    assert age_seconds("<1m") == 0
    assert age_seconds("5m") == 300
    assert age_seconds("3h") == 3 * 3600
    assert age_seconds("12d") == 12 * 86400
    assert age_seconds("unknown") == float("inf")
    assert age_seconds("2d") > age_seconds("47h")


def test_workload_sort_keys_rank_status_worst_first_and_ready_by_fraction() -> None:
    from kubescope.models import workload_sort_key

    healthy = Workload("b", "Deployment", "api", 3, 3, "1d")
    degraded = Workload("a", "Deployment", "web", 1, 4, "2d")
    down = Workload("c", "StatefulSet", "db", 0, 1, "9d")
    off = Workload("a", "Deployment", "job", 0, 0, "3h")
    items = [healthy, degraded, down, off]

    def order(column: int) -> list[str]:
        ranked = sorted(items, key=lambda w: workload_sort_key(w, column))
        return [workload.name for workload in ranked]

    assert order(0) == ["job", "web", "api", "db"]  # namespace, then kind/name
    assert order(1) == ["job", "web", "api", "db"]  # Deployment < StatefulSet
    assert order(2) == ["api", "db", "job", "web"]
    assert order(3) == ["db", "web", "job", "api"]  # 0/1, 1/4, 0/0, 3/3
    assert order(4) == ["db", "web", "job", "api"]  # Unavailable first
    assert order(9) == ["job", "api", "web", "db"]  # youngest first


def test_pod_highlight_flags_problems_over_young_pods() -> None:
    from kubescope.models import PodInfo, pod_highlight

    def pod(phase="Running", ready=1, restarts=0, age="2d") -> PodInfo:
        return PodInfo("d", "p", phase, ready, 1, age, ("a",), restarts=restarts)

    assert pod_highlight(pod()) is None
    assert pod_highlight(pod(age="<1m")) == "young"
    assert pod_highlight(pod(age="59m")) == "young"
    assert pod_highlight(pod(age="1h")) is None
    assert pod_highlight(pod(restarts=2)) == "problem"
    assert pod_highlight(pod(phase="Failed", ready=0)) == "problem"
    assert pod_highlight(pod(ready=0)) == "problem"
    assert pod_highlight(pod(age="5m", restarts=1)) == "problem"  # problem wins
    assert pod_highlight(pod(phase="Pending", ready=0, age="5m")) == "young"


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, 0.0), ("", 0.0), ("250m", 0.25), ("2", 2.0), ("1500u", 0.0015)],
)
def test_parse_cpu(value: str | None, expected: float) -> None:
    assert parse_cpu(value) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, 0.0),
        ("512Mi", 512 * 2**20),
        ("2G", 2e9),
        ("1500m", 1.5),
        ("1024", 1024.0),
    ],
)
def test_parse_memory(value: str | None, expected: float) -> None:
    assert parse_memory(value) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("cores", "expected"), [(None, "—"), (0.25, "250m"), (2.0, "2.00")]
)
def test_format_cpu(cores: float | None, expected: str) -> None:
    assert format_cpu(cores) == expected


@pytest.mark.parametrize(
    ("size", "expected"),
    [(None, "—"), (512 * 2**20, "512 MiB"), (3 * 2**30, "3.0 GiB")],
)
def test_format_memory_and_bytes(size: float | None, expected: str) -> None:
    assert format_memory(size) == expected
    if size is not None:
        assert format_bytes(size) == expected


def test_workload_sort_key_covers_every_column() -> None:
    workload = Workload("ns", "Deployment", "Api", 1, 2, "3h", 4, 0.5, 100.0)
    bare = Workload("ns", "Deployment", "api", 0, 0, "1d")

    keys = [workload_sort_key(workload, column) for column in range(len(SORT_COLUMNS))]

    assert keys[3][:2] == (0.5, 2)
    assert workload_sort_key(bare, 3)[:2] == (1.0, 0)
    assert workload_sort_key(bare, 5)[0] == -1.0
    assert workload_sort_key(workload, 5)[0] == 0.5
    assert workload_sort_key(workload, 9)[0] == 3 * 3600
    selected = Workload("ns", "Deployment", "a", 1, 1, "1d", node_selector="Disk=ssd")
    assert workload_sort_key(selected, 8)[0] == "disk=ssd"
    assert workload_sort_key(workload, 1)[0] == "Deployment"
    assert workload_sort_key(workload, 2)[0] == "api"
    assert workload_sort_key(workload, 0)[0] == "ns"


def test_pod_sort_key_covers_every_column() -> None:
    pod = PodInfo("ns", "Web", "Running", 1, 2, "2d", ("a", "b"), 3, 0.2, 50.0)
    empty = PodInfo("ns", "web", "Weird", 0, 0, "1h", ())

    assert len(POD_SORT_COLUMNS) == 12
    assert pod_sort_key(pod, 1)[0] == 2
    assert pod_sort_key(pod, 3)[:2] == (0.5, 2)
    assert pod_sort_key(empty, 3)[:2] == (1.0, 0)
    assert pod_sort_key(pod, 4)[0] == 3
    assert pod_sort_key(empty, 4)[0] == 4
    assert pod_sort_key(empty, 5)[0] == -1.0
    assert pod_sort_key(pod, 7)[0] == 3
    assert pod_sort_key(pod, 11)[0] == 2 * 86400
    assert pod_sort_key(pod, 2)[0] == "web"
    assert pod_sort_key(pod, 0)[0] == "ns"
    placed = PodInfo(
        "ns", "w", "Running", 1, 1, "2d", ("a",), owner=("Deployment", "d"), node="N1"
    )
    assert pod_sort_key(placed, 8)[0] == "deployment"
    assert pod_sort_key(pod, 8)[0] == ""
    assert pod_sort_key(placed, 9)[0] == "n1"
    assert pod_sort_key(placed, 10)[0] == ""


def test_job_and_cron_job_states_replace_the_replica_status() -> None:
    complete = Workload("ns", "Job", "j", 1, 1, "1h", state="Complete")
    cron = Workload(
        "ns", "CronJob", "c", 0, 0, "1h", state="Suspended", schedule="* * * * *"
    )

    assert complete.status == "Complete" and cron.status == "Suspended"
    failed = Workload("ns", "Job", "k", 0, 1, "1h", state="Failed")
    assert workload_sort_key(failed, 4) < workload_sort_key(complete, 4)  # worst first


def test_network_sort_key_orders_by_text_and_by_age() -> None:
    from kubescope.models import ClusterResource, resource_sort_key

    web = ClusterResource("ns", "Service", "web", ("ClusterIP", "10.0.0.1"), "2d")
    api = ClusterResource("ns", "Service", "api", ("NodePort", "10.0.0.2"), "5h")

    assert resource_sort_key(web, 2) > resource_sort_key(api, 2)  # by name
    assert resource_sort_key(web, 3) < resource_sort_key(api, 3)  # ClusterIP < NodePort
    assert resource_sort_key(web, 5) > resource_sort_key(api, 5)  # 2d is older than 5h


def test_safe_file_name_keeps_letters_digits_dots_and_dashes() -> None:
    from kubescope.models import safe_file_name

    assert safe_file_name("Deployment: api", ".json") == "Deployment-api.json"
    assert safe_file_name("api-1/app v2", ".log") == "api-1-app-v2.log"
    assert safe_file_name("???", ".json") == "kubescope.json"


DETAILS_NOW = 1_760_900_000.0  # 2025-10-19T19:33:20Z


def test_detail_sections_lay_out_properties_spec_and_status() -> None:
    document = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {
            "name": "api-1",
            "namespace": "ns",
            "creationTimestamp": "2025-10-19T16:13:20Z",
            "labels": {"app": "api", "tier": "back"},
            "annotations": {"note": "x" * 200},
            "ownerReferences": [{"kind": "ReplicaSet", "name": "api-5f"}, "junk"],
            "managedFields": [{"manager": "kubectl"}],
        },
        "spec": {
            "nodeName": "node-1",
            "hostNetwork": False,
            "args": ["--a", "--b"],
            "containers": [
                {"name": "app", "image": "api:1", "ports": [{"containerPort": 80}]},
                {"image": "side:1"},
            ],
            "volumes": [],
        },
        "status": {
            "phase": "Running",
            "conditions": [
                {"type": "Ready", "status": "True"},
                {"type": "Initialized", "status": "True", "reason": None},
            ],
        },
    }

    sections = {s.title: s.rows for s in detail_sections(document, DETAILS_NOW)}

    assert list(sections) == [
        "Properties",
        "Spec",
        "containers: app",
        "containers: 1",
        "Status",
    ]
    properties = {row.label: row.values for row in sections["Properties"]}
    assert properties["Kind"] == ("Pod",)
    assert properties["Created"][0].startswith("2h ago (")
    assert properties["Name"] == ("api-1",)
    assert properties["Labels"] == ("app=api", "tier=back")
    assert properties["Annotations"][0].endswith("...")
    assert properties["Controlled by"] == ("ReplicaSet/api-5f",)
    spec = {row.label: row.values for row in sections["Spec"]}
    assert spec["nodeName"] == ("node-1",)
    assert spec["hostNetwork"] == ("false",)
    assert spec["args"] == ("--a", "--b")
    app = sections["containers: app"]
    assert (app[1].label, app[1].values) == ("image", ("api:1",))
    assert app[2].headers == ("containerPort",)
    assert sections["containers: 1"][0].values == ("side:1",)
    assert "volumes" not in spec
    conditions = sections["Status"][-1]
    assert conditions == DetailRow(
        "conditions",
        headers=("type", "status", "reason"),
        table=(("Ready", "True", ""), ("Initialized", "True", "")),
    )


def test_detail_sections_tolerate_odd_documents() -> None:
    assert detail_sections({}) == []
    odd = {"metadata": {"creationTimestamp": "soon", "ownerReferences": []}}
    assert detail_sections(odd)[0].rows[0].values == ("soon",)
    naive = {"metadata": {"creationTimestamp": "2025-10-19T16:13:20"}}
    assert detail_sections(naive)[0].rows[0].values == ("2025-10-19T16:13:20",)
    assert detail_sections({"metadata": "x", "data": {"k": "v"}})[0].title == "Data"
    assert detail_sections({"items": [1, 2]})[0].rows[0].values == ("1", "2")


@pytest.mark.parametrize(
    ("workload", "expected"),
    [
        (Workload("n", "Deployment", "a", 3, 3, "1d"), ("running",) * 3),
        (Workload("n", "Deployment", "a", 1, 3, "1d"), ("running",) + ("pending",) * 2),
        (Workload("n", "Deployment", "a", 0, 2, "1d"), ("error", "error")),
        (Workload("n", "Deployment", "a", 0, 0, "1d"), ("terminated",)),
        (Workload("n", "Deployment", "a", 40, 40, "1d"), ("running",) * 5),
        (
            Workload("n", "Deployment", "a", 1, 40, "1d"),
            ("running",) + ("pending",) * 4,
        ),
        (Workload("n", "Job", "a", 0, 1, "1d", state="Failed"), ("error",)),
        (Workload("n", "Job", "a", 1, 1, "1d", state="Complete"), ("terminated",)),
        (Workload("n", "Job", "a", 0, 1, "1d", state="Running"), ("running",)),
        (Workload("n", "Job", "a", 0, 1, "1d", state="Pending"), ("pending",)),
    ],
)
def test_a_workload_shows_one_state_for_each_replica(workload, expected) -> None:
    assert workload.states == expected


def test_detail_values_that_name_a_resource_link_to_it() -> None:
    document = {
        "kind": "Pod",
        "metadata": {
            "name": "p",
            "namespace": "ns",
            "ownerReferences": [
                {"kind": "ReplicaSet", "name": "api-5d"},
                {"kind": "Mystery", "name": "x"},
            ],
        },
        "spec": {
            "nodeName": "n1",
            "serviceAccountName": "sa",
            "volumes": [{"name": "c", "configMap": {"name": "cm1"}}],
        },
    }
    links = {
        row.label: row.links
        for section in detail_sections(document)
        for row in section.rows
        if row.links
    }

    assert links["Namespace"] == (("Namespace", "", "ns"),)
    assert links["Controlled by"] == (("ReplicaSet", "ns", "api-5d"), None)
    assert links["nodeName"] == (("Node", "", "n1"),)
    assert links["configMap.name"] == (("ConfigMap", "ns", "cm1"),)
    assert "serviceAccountName" not in links


def test_detail_links_skip_empty_values_and_tables() -> None:
    assert detail_link("secretRef.name", "", "ns") is None
    assert detail_link("secret.secretName", "s", "ns") == ("Secret", "ns", "s")
    assert detail_link("Controlled by", "ReplicaSet", "ns") is None  # no name


def test_an_event_links_to_the_resource_it_is_about() -> None:
    def event(involved: str) -> EventInfo:
        return EventInfo("Normal", "s", "ns", involved, "m", 1, "1h", "1h")

    assert event_link(event("Pod: api-1")) == ("Pod", "ns", "api-1")
    assert event_link(event("Node: n1")) == ("Node", "", "n1")
    assert event_link(event("Mystery: x")) is None
    assert event_link(event("?: ?")) is None


def test_secrets_are_linked_wherever_a_pod_names_them() -> None:
    document = {
        "kind": "Pod",
        "metadata": {"name": "p", "namespace": "ns"},
        "spec": {
            "imagePullSecrets": [{"name": "regcred"}],
            "volumes": [
                {"name": "v", "projected": {"sources": [{"secret": {"name": "ps"}}]}}
            ],
            "containers": [
                {
                    "name": "app",
                    "env": [
                        {
                            "name": "A",
                            "valueFrom": {"secretKeyRef": {"name": "sk", "key": "k"}},
                        }
                    ],
                }
            ],
        },
    }
    found = {
        row.label: row.links
        for section in detail_sections(document)
        for row in section.rows
        if row.links
    }

    assert found["imagePullSecrets"] == (("Secret", "ns", "regcred"),)
    assert found["secret.name"] == (("Secret", "ns", "ps"),)
    assert found["valueFrom.secretKeyRef.name"] == (("Secret", "ns", "sk"),)


def test_a_table_that_is_not_a_list_of_names_has_no_links() -> None:
    document = {
        "kind": "Pod",
        "metadata": {"name": "p", "namespace": "ns"},
        "spec": {"imagePullSecrets": [{"other": "x"}], "tolerations": [{"key": "a"}]},
    }

    assert not any(
        row.links
        for section in detail_sections(document)
        for row in section.rows
        if row.label != "Namespace"
    )
