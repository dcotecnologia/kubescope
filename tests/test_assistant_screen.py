from kubescope.assistant import actions, knowledge, runner
from kubescope.assistant.screen import ROW_LIMIT, VIEWER_LIMIT, Screen, describe


def _list(**overrides) -> Screen:
    base = {
        "context": "prod",
        "page": 1,
        "view": "pods",
        "headers": ("Namespace", "Name", "Status"),
        "rows": (("ns", "web-1", "Running"), ("ns", "web-2", "CrashLoopBackOff")),
    }
    return Screen(**{**base, **overrides})


def test_a_list_is_described_with_what_narrows_it_and_what_is_selected() -> None:
    text = describe(
        _list(
            namespace="ns",
            search="web",
            regex=True,
            case=True,
            selected=("ns", "web-2", "CrashLoopBackOff"),
        )
    )

    assert "Context: prod" in text and "Page: the pods list" in text
    assert "Namespace filter: ns" in text
    assert 'Search: "web" (regular expression, match case)' in text
    assert "Selected row: ns | web-2 | CrashLoopBackOff" in text
    assert "Rows shown: 2\nNamespace | Name | Status\nns | web-1 | Running" in text


def test_the_defaults_say_all_namespaces_and_leave_out_what_is_not_set() -> None:
    text = describe(_list(search="x", headers=()))

    assert "Namespace filter: all namespaces" in text
    assert 'Search: "x"\n' in text
    assert "Selected row" not in text and "Name |" not in text


def test_a_long_list_is_cut_to_the_rows_that_fit() -> None:
    rows = tuple((f"r{number}",) for number in range(ROW_LIMIT + 5))

    text = describe(_list(rows=rows, headers=("N",)))

    assert f"Rows shown: {ROW_LIMIT + 5}" in text
    assert f"r{ROW_LIMIT - 1}" in text and f"r{ROW_LIMIT}\n" not in text
    assert "[5 more rows left out]" in text


def test_an_open_tab_gives_its_text_and_the_end_of_a_long_one() -> None:
    short = describe(Screen("prod", 3, viewer_title="Pod: web", viewer_text="{}"))
    long = describe(
        Screen("prod", 3, viewer_title="Logs", viewer_text="x" * VIEWER_LIMIT + "END")
    )

    assert "Page: an open tab, Pod: web\n{}" in short
    assert "[earlier text left out]" in long and long.endswith("END")


def test_the_other_pages_are_named_and_extras_follow() -> None:
    assert "Page: Cluster overview" in describe(Screen("prod", 0))
    assert "Page: Workloads overview" in describe(Screen("prod", 4))
    assert "Page: Settings" in describe(Screen("prod", 2))
    assert "Page: the window" in describe(Screen("prod", 9, extra=("note",)))
    assert describe(Screen("prod", 9, extra=("note",))).endswith("note")


def test_what_is_seen_is_redacted_like_every_read() -> None:
    text = describe(_list(rows=(("ns", "Bearer abcdefghijklmnop", "x"),)))

    assert "abcdefghijklmnop" not in text


def test_the_chat_is_told_the_app_the_way_to_look_into_a_problem_and_the_actions() -> (
    None
):
    told = knowledge.system_prompt()

    assert told.startswith(runner.SYSTEM_PROMPT)
    assert "KubeScope" in told and "write mode" in told
    assert "get_events" in knowledge.DIAGNOSE and "get_logs" in knowledge.DIAGNOSE
    assert told.endswith(actions.instructions())


def test_the_chat_is_told_to_answer_in_the_language_of_the_client() -> None:
    portuguese = knowledge.system_prompt("Portuguese")

    assert "Answer in Portuguese, the language of the client" in portuguese
    assert "Answer in English" in knowledge.system_prompt()
    assert "unless the person writes to you in another one" in portuguese


def _overview():
    from kubescope.models import ClusterOverview, NodeInfo

    node = NodeInfo(
        "node-1",
        True,
        "worker",
        "v1.30",
        "9d",
        4.0,
        16 * 2**30,
        110,
        20,
        1.5,
        4 * 2**30,
    )
    sick = NodeInfo("node-2", False, "worker", "v1.30", "9d", 2.0, 8 * 2**30, 110)
    return ClusterOverview(
        nodes=(node, sick),
        namespaces=12,
        deployments=30,
        pods_total=200,
        pods_running=190,
        pods_pending=7,
        pods_failed=3,
        warnings=("metrics unavailable",),
    )


def test_the_overview_of_the_cluster_gives_its_numbers_and_its_nodes() -> None:
    from kubescope.assistant.screen import describe_cluster_overview

    text = "\n".join(describe_cluster_overview(_overview()))

    assert "Nodes: 2 (1 ready)" in text and "Namespaces: 12" in text
    assert "Deployments: 30, StatefulSets: unknown, DaemonSets: unknown" in text
    assert "Pods: 200 total, 190 running, 7 pending, 3 failed" in text
    assert "CPU: 1.50 requested of 6.00 allocatable, usage —" in text
    assert "Node node-1: Ready, worker, v1.30, pods 20/110" in text
    assert "Node node-2: NotReady" in text and "Warning: metrics unavailable" in text
    assert describe_cluster_overview(None) == ("The overview has not loaded yet.",)


def test_the_overview_of_the_workloads_gives_each_kind_and_the_events() -> None:
    from kubescope.assistant import screen
    from kubescope.assistant.screen import describe_workloads_overview
    from kubescope.models import EventInfo, KindSummary, WorkloadsOverview

    events = tuple(
        EventInfo("Warning", "kubelet", "ns", f"Pod: p{n}", "BackOff", 3, "1h", "2m")
        for n in range(screen.EVENT_ROWS + 2)
    )
    overview = WorkloadsOverview(
        {"Deployment": KindSummary(10, 7, 2, 1), "Pod": KindSummary(5, 5)},
        events,
        unreadable=("DaemonSet",),
    )

    text = "\n".join(describe_workloads_overview(overview))

    assert (
        "Deployment: 10 in all, 7 healthy, 2 degraded or coming up, 1 failing" in text
    )
    assert "Not readable by this user: DaemonSet" in text
    assert "Warning Pod: p0 in ns: BackOff (x3, age 1h, last seen 2m)" in text
    assert "[2 more events left out]" in text
    assert describe_workloads_overview(None) == ("The overview has not loaded yet.",)
    few = WorkloadsOverview({}, events[:1])
    assert "more events" not in "\n".join(describe_workloads_overview(few))
    nameless = WorkloadsOverview(
        {}, (EventInfo("Normal", "k", "", "Pod: x", "m", 1, "1s", "1s"),)
    )
    assert "in -:" in "\n".join(describe_workloads_overview(nameless))
