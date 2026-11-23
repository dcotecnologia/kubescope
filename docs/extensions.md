---
layout: page
title: Extensions
permalink: /extensions/
---

KubeScope stays small: a feature that is not for everyone is an **extension**, a project of its own that you install and uninstall in **Settings → Extensions**. These are the ones KubeScope recommends, all made by DCO Tecnologia. Three come with the app; the others are a card in **Settings → Extensions** that you install when you want them.

| Extension | What it does | Comes with KubeScope | Needs |
| --------- | ------------ | -------------------- | ----- |
| [Gabi - AI Assistant](#gabi---ai-assistant) | Ask about your cluster in plain language | Yes | KubeScope 2.4 |
| [Global Search](#global-search) | Find a screen, a list or a resource by its name | Yes | |
| [Themes](#themes) | Thirteen color themes, light and dark | Yes | |
| [AWS Resources](#aws-resources) | The RDS databases of the account of the cluster | No, a card to install | |
| [Notifications](#notifications) | A bell with the Warning and Error events of every context | No, a card to install | |
| [Custom Resources](#custom-resources) | The custom resources of the cluster by API group, and a resync of the ExternalSecrets | No, a card to install | KubeScope 2.5 |

## Gabi - AI Assistant

Ask about your cluster in plain language: she reads workloads, events, logs and live CPU and memory, explains what is wrong and how to fix it, and takes you to the right list or tab. Changes (scale, edit) only in write mode, each one confirmed. She uses the coding assistant you already signed in to. [Read more about Gabi]({{ '/assistant/' | relative_url }}).

- **Asks for:** to read your clusters, to change them in the write mode, to run programs of your computer, to use the window, to add a section to the Settings and the `kubescope chat` command.
- **Source:** [kubescope-ai-gabi](https://github.com/dcotecnologia/kubescope-ai-gabi)

## Global Search

Press `/` or `Ctrl+K` to find a screen, a list or a resource of any namespace by its name, and open it.

- **Asks for:** to read your clusters and to use the window.
- **Source:** [kubescope-search](https://github.com/dcotecnologia/kubescope-search)

## Themes

Thirteen color themes, light and dark: Abyss, Dark Modern, High Contrast, Light Modern, macOS Dark and Light, Midnight, Monokai, Quiet Light, Sepia, Solarized Dark and Light, and Tomorrow Night Blue. They show in **Settings → Theme**, where you can copy and edit them.

- **Asks for:** to add color themes.
- **Source:** [kubescope-themes](https://github.com/dcotecnologia/kubescope-themes)

## AWS Resources

Look at your AWS account from KubeScope: the RDS databases of the account of the selected cluster, in any region, with their details and logs, and a port forward to a database through Systems Manager in the write mode. It adds an **AWS** block to the side menu.

- **Asks for:** to read your AWS account (RDS, EC2, EKS and Systems Manager), to start a port forward in the write mode, to add a page and to use the window. The keys of the account never reach the extension.
- **Source:** [kubescope-aws](https://github.com/dcotecnologia/kubescope-aws)

## Notifications

A bell in the top bar that keeps the Warning and Error events of every context, and the errors and new versions KubeScope itself reports, and lists them in a panel that slides in from the right. A new one also shows a notice of the operating system that opens the app when clicked.

- **Asks for:** to read your clusters, to use the window and to add a section to the Settings.
- **Source:** [kubescope-notifications](https://github.com/dcotecnologia/kubescope-notifications)

## Custom Resources

Browse the custom resources of the cluster by API group, as Lens does: a **Custom Resources** block in the side menu with the definitions and a list for each kind, with the columns its CRD asks for, a namespace filter, a search and the details. The ExternalSecrets of the External Secrets Operator show how their last sync went and can be resynced, one or all the ones shown, in the write mode and after a confirmation.

- **Asks for:** to read your clusters, to change them in the write mode (only the `force-sync` annotation of an ExternalSecret), to add pages to the side menu and to use the window.
- **Needs:** KubeScope 2.5 or newer.
- **Source:** [kubescope-ext-custom-resources](https://github.com/dcotecnologia/kubescope-ext-custom-resources)

## Install an extension

1. Open **Settings → Extensions**. The table lists what is installed and what KubeScope recommends.
2. Double-click a row for its details, or right-click it to install, update, reinstall or uninstall it. A recommended extension that is not installed has a card with an **Install** button.
3. Before anything of an extension runs, a dialog shows where it comes from, its permissions and the sha256 of its content. Read it, and confirm only if you trust the source.

You can also install one from any GitHub repository with **Install from GitHub...** (type `owner/name`), or from a folder with **Install from a folder...**. KubeScope looks for newer versions and suggests them, and never updates an extension by itself.

An extension is Python code that runs with the same rights as the app: the permissions tell you what it does, but are not a sandbox. Install only the ones you trust; see the [security policy]({{ '/guides/security/' | relative_url }}).

## Write your own

An extension is a project written against the [KubeScope SDK](https://github.com/dcotecnologia/kubescope-sdk) and nothing else of the app. Its guides cover [getting started](https://github.com/dcotecnologia/kubescope-sdk/blob/main/docs/getting-started.md), [the manifest](https://github.com/dcotecnologia/kubescope-sdk/blob/main/docs/manifest.md), [the context](https://github.com/dcotecnologia/kubescope-sdk/blob/main/docs/api.md), [contributions](https://github.com/dcotecnologia/kubescope-sdk/blob/main/docs/contributions.md) and [permissions and security](https://github.com/dcotecnologia/kubescope-sdk/blob/main/docs/permissions.md).
