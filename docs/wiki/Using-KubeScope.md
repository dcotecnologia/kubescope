# Using KubeScope

## The window

The sidebar has **Overview**, **Workloads**, **Settings**, and a **Details & Logs**
entry that appears once you open something. The bar above the content has the
context box, the namespace filter, a search box and **Refresh**.

## Overview

Nodes (ready or not, roles, version, requested against allocatable CPU and
memory), Pod counts by state, and the number of namespaces, Deployments,
StatefulSets and DaemonSets. Real CPU and memory usage appears when the cluster
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

Click **Workloads** to slide out **Pods**, **Deployments**, **StatefulSets**, **Jobs**
and **CronJobs**.

- **Pods:** every Pod of the selected namespace (or all). Columns: namespace,
  containers, name, ready, status, CPU, memory, restarts and age. Young Pods (under
  an hour) get a soft green row; Pods that are restarting, failing or not ready get
  a soft red one.
- **Deployments** and **StatefulSets:** namespace, kind, name, ready, status, CPU,
  memory, restarts and age. The numbers are the sum of the workload's Pods.
- **Jobs:** the same columns, with **Completions** (done / wanted) instead of Ready.
  The status is Complete, Running, Pending, Failed or Suspended.
- **CronJobs:** the **Schedule** replaces Ready. The status is Scheduled, Active (a
  Job is running) or Suspended. Its Pods are the ones of the Jobs it created.

Select a row, then use **Details** (the JSON of the resource) or **Logs**. From a
workload you can also open **Pods** to list its Pods. Double-click a row for
details.

## Logs

Logs open in their own tab. If the Pod has several containers you pick one first.
The tab shows the latest lines and refreshes on its own; pause it with the
checkbox, or refresh by hand. Close a tab with its **x**.

## Tables

- Drag a column border to resize it.
- Click a header to sort; click again to reverse.
- Right-click a header to hide or show columns. The choice is saved per list.
  The name column always stays.

## Settings

Language (automatic, English or Portuguese), the theme, remembering the last
context, display names for contexts, and the debug log.

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
