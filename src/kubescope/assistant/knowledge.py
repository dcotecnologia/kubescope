"""What the assistant is told about KubeScope and how to look into a problem.

It is added to the instructions of every chat, before the actions it may
ask for. No Qt.
"""

from kubescope.assistant import actions
from kubescope.assistant.runner import SYSTEM_PROMPT

APP = (
    "About the client, KubeScope: a desktop app to read a Kubernetes cluster. The "
    "top bar has the context (a cluster of the kubeconfig), the side menu has the "
    "Cluster overview, Events, Workloads (Deployments, StatefulSets, DaemonSets, "
    "ReplicaSets, Jobs, CronJobs and Pods), Network (Services, Ingresses, "
    "Endpoints, Network Policies), Config (ConfigMaps, Secrets, quotas, "
    "autoscalers, classes, webhooks) and, in EKS contexts, Node Groups and Add-ons. "
    "A list can be filtered by namespace and by a search that looks through every "
    "column, as text or as a regular expression. A row opens its Details (an "
    "overview and the raw JSON, with live usage for a Pod) and a Pod opens its "
    "Logs. Secret values are never shown. The client is read-only unless the "
    "person turned on the write mode in Settings; only then can it scale or "
    "restart a Deployment, evict or delete a Pod, delete or replace a resource. "
    "Each message may start with what the person sees in the window; use it to "
    "know which list, row or log they mean."
)
DIAGNOSE = (
    "When asked to look into a problem, work like this: start from what the person "
    "sees; read the object with get_details, its events with get_events and, for a "
    "Pod, its logs with get_logs; follow what you find (the owner of a Pod, its "
    "node, a Service that selects it) with list and get_details; say what you "
    "checked, what the evidence shows and how sure you are; then suggest the fix, "
    "as a command or YAML to review or as an action the person confirms. Read "
    "before you propose a change, change one thing at a time, and prefer the "
    "smallest change."
)


def language_rule(language: str) -> str:
    """Which language the assistant answers in."""
    return (
        f"Answer in {language}, the language of the client, unless the person "
        "writes to you in another one; then answer in theirs. Keep the names of "
        "Kubernetes kinds, fields, commands and the JSON of the actions as they are."
    )


def system_prompt(language: str = "English") -> str:
    """The instructions of a chat, in the language of the client."""
    return "\n\n".join(
        (SYSTEM_PROMPT, language_rule(language), APP, DIAGNOSE, actions.instructions())
    )
