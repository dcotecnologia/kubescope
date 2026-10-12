# Using KubeScope

## The window

The sidebar has **Overview**, **Workloads**, **Settings**, and a **Details & Logs**
entry that appears once you open something. The bar above the content has the
context box, the namespace filter, a search box and **Refresh**.

## Overview

Totals of nodes ready, Pod counts by state, requested against allocatable CPU and
memory, and the number of namespaces, Deployments, StatefulSets and DaemonSets.
The nodes themselves are listed under **Node Groups** on Amazon EKS. Real CPU and memory usage appears when the cluster
has `metrics-server`.

## Workloads overview

**Workloads > Overview** shows how many Pods, Deployments, DaemonSets, StatefulSets,
ReplicaSets, Jobs and CronJobs the cluster has, each with a bar: green for healthy,
orange for coming up or degraded, red for failing. The grey remainder is idle on
purpose, such as a Deployment scaled to zero. Click a name to open its list. Below,
the **Events** table lists the latest events of the cluster (warnings in orange),
newest first, with their count, age and when they were last seen. A section you are
not allowed to read is named under the bars instead of failing the page.

## Pods and workloads

Click **Workloads** to slide out **Pods**, **Deployments**, **StatefulSets**,
**DaemonSets**, **ReplicaSets**, **ReplicationControllers**, **Jobs** and **CronJobs**.

- **Pods:** every Pod of the selected namespace (or all). Columns: namespace,
  containers, name, ready, status, CPU, memory, restarts and age. Young Pods (under
  an hour) get a soft green row; Pods that are restarting, failing or not ready get
  a soft red one.
- **Deployments**, **StatefulSets**, **DaemonSets**, **ReplicaSets** and
  **ReplicationControllers:** namespace, kind, name, ready, status, CPU, memory,
  restarts and age. The numbers are the sum of the workload's Pods.
- **Jobs:** the same columns, with **Completions** (done / wanted) instead of Ready.
  The status is Complete, Running, Pending, Failed or Suspended.
- **CronJobs:** the **Schedule** replaces Ready. The status is Scheduled, Active (a
  Job is running) or Suspended. Its Pods are the ones of the Jobs it created.

## Network

Click **Network** to slide out **Services**, **Endpoint Slices**, **Endpoints**,
**Ingresses**, **Ingress Classes** and **Network Policies**. It opens next to
**Workloads**; neither closes the other.

- **Services:** type, cluster IP, external IP and ports.
- **Endpoint Slices:** address type, ports and the first addresses.
- **Endpoints:** the first addresses and ports behind the Service.
- **Ingresses:** class, hosts, address and ports (443 when TLS is set).
- **Ingress Classes:** controller and parameters; they belong to the whole cluster,
  so the namespace filter does not apply.
- **Network Policies:** the Pods they select (`*` is all) and their policy types.

Long lists of addresses show the first three and a count. Select a row and use
**Details** for its JSON. Port forwarding is not part of KubeScope yet.

## Pinned lists

Double-click an entry of **Workloads**, **Network** or **Config**, or right-click it
and choose **Pin to the top**. It appears as a tab in the top bar, next to the KubeScope name, in
the order you pinned it; the open list's tab is highlighted. Click a tab to open
the list; middle-click a tab, click its × or right-click it to unpin. A
pinned list that does not apply to the open context, such as Node Groups outside
Amazon EKS, is left out until it does.

## Config

Click **Config** to slide out the configuration of the cluster. It opens next to
**Workloads** and **Network**; none closes the others.

- **Config Maps:** how many keys each holds.
- **Secrets:** type and how many keys. **Details** shows the keys with every value
  replaced by `<redacted>`; KubeScope never shows a Secret's data.
- **Resource Quotas:** used and hard amount of each resource, as `used/hard`.
- **Limit Ranges:** the types they limit (Container, Pod, ...).
- **Horizontal Pod Autoscalers:** the target, minimum and maximum Pods, and the
  current replicas.
- **Pod Disruption Budgets:** minimum available, maximum unavailable and the
  disruptions allowed now.
- **Priority Classes:** value and whether it is the global default.
- **Runtime Classes:** the handler.
- **Leases:** the current holder.
- **Mutating** and **Validating Webhook Configurations:** how many webhooks each
  declares.

- **Add-ons:** the Helm releases of the cluster (status and revision, one row per
  release) and, on Amazon EKS, the EKS add-ons (status and version). The Source
  column tells them apart. Helm releases are read from the labels of the Secrets
  where Helm 3 stores them, so no `helm` program is needed; the contents of those
  Secrets are never requested. Releases kept by Helm 2 or by another storage
  driver are not listed.

Priority Classes, Runtime Classes and the two webhook configurations belong to the
whole cluster, so the namespace filter does not apply to them.

## Cluster info (EKS only)

On an Amazon EKS context the **Overview** starts with a **Cluster info** card:
status, Kubernetes version, platform version, creation time, provider, API server
endpoint, cluster ARN, cluster IAM role ARN and the OpenID Connect provider URL.
The text can be selected and copied. It comes from `aws eks describe-cluster`; if
that call is denied the card is simply not shown. Support period, upgrade insights
and health are not shown yet.

A **Networking** card follows it: VPC, cluster security group, additional security
groups, API server endpoint access (public, private or both), IP address family,
service IPv4 range, the public access allowlist and the subnets, one per line.
It comes from the same `describe-cluster` call.

## Node Groups

On an Amazon EKS context, **Node Groups** appears under **Overview**; other
contexts do not show it. The
list shows each managed node group's status, instance types, nodes (`desired
(min–max)`), AMI type and AMI version. It has no namespace filter and no
Namespace or Kind column, as these are not Kubernetes objects. KubeScope reads
them with `aws eks list-nodegroups` and `aws eks describe-nodegroup` (and the
`addon` equivalents) using the profile and region of your kubeconfig. **Details**
shows the JSON that `describe-nodegroup` returns.

Select a row, then use **Details** (the JSON of the resource) or **Logs**. From a
workload you can also open **Pods** to list its Pods. Double-click a row for
details.

## Logs

Logs open in their own tab. If the Pod has several containers you pick one first.
The tab shows the latest lines and refreshes on its own; pause it with the
checkbox, or refresh by hand. Close a tab with its **x**.

## Saving details and logs

**Save...**, at the top right of the tab bar, writes the open tab to a file: the
JSON of a resource, or the lines of a log as shown (the latest 500). You choose
where; nothing is written until you do, and the app keeps no copy. Logs can
contain secrets printed by an application, so keep the file somewhere safe.

## Tables

- Drag a column border to resize it.
- Click a header to sort; click again to reverse.
- Right-click a header to hide or show columns. The choice is saved per list.
  The name column always stays.

## Settings

Language (automatic, English, Portuguese, Spanish, Italian, French, Chinese,
Japanese, Arabic, Hindi or Russian), the theme, remembering the last
context, display names for contexts, and the debug log.

### Updates

When it starts, KubeScope asks the public GitHub API for the latest release. The
icon in the footer spins while it looks, shows **Up to date** for a moment, or
shows **Update available**: click it to open the download page. Click the icon at
any time to check again. Only the app version is sent, and nothing is installed.
To turn the startup check off, clear **Check GitHub for a new version when the app
starts** in Settings.

### Themes

Choose **Light**, **Dark**, or a theme of your own. **New theme...** opens an editor
that starts from the selected theme: name it, click a color to change it, and save.
**Edit theme...** changes one of yours (the built-in ones are fixed; copy one with
**New theme...** instead). A theme is a JSON file in the `themes` folder next to
`settings.json`; **Open the themes folder** takes you there. The page scrolls when
the window is small.

```json
{
  "name": "Midnight",
  "base": "dark",
  "colors": { "page": "#0b0f14", "accent": "#7aa2f7", "topbar": "#000000" }
}
```

A theme starts from its `base` (`light` or `dark`) and lists only the colors it
changes. The names are the ones the editor shows, such as `page`, `surface`, `text`,
`accent`, `topbar`, `good` and `bad`. A file that is damaged or names an unknown
color is skipped, and the debug log says why.

KubeScope also ships a few **community themes** (Midnight, High contrast, Sepia). The
first time it starts with one, it copies the file into your `themes` folder, where you
can edit or delete it: edits are kept and a deleted theme does not come back. To share
a theme, see the README in `src/kubescope/community_themes/` in the repository.
