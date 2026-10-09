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

## Pods and Deployments

Click **Workloads** to slide out **Pods** and **Deployments**.

- **Pods:** every Pod of the selected namespace (or all). Columns: namespace,
  containers, name, ready, status, CPU, memory, restarts and age. Young Pods (under
  an hour) get a soft green row; Pods that are restarting, failing or not ready get
  a soft red one.
- **Deployments:** namespace, kind, name, ready, status, CPU, memory, restarts and
  age. The numbers are the sum of the Deployment's Pods.

Select a row, then use **Details** (the JSON of the resource) or **Logs**. From a
Deployment you can also open **Pods** to list its Pods. Double-click a row for
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

Language (automatic, English or Portuguese), remembering the last context, and
display names for contexts.
