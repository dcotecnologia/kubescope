---
layout: page
title: Guides
permalink: /guides/
---

KubeScope is a desktop IDE for Kubernetes, including Amazon EKS, Google GKE and Azure AKS. Open it, pick a
context from your kubeconfig, and see the cluster: overview, Pods, Deployments,
details and live logs. It uses the official Kubernetes Python client, so it needs no `kubectl`, and is read-only unless you turn on the write mode.

![KubeScope cluster overview]({{ '/screenshots/overview.png' | relative_url }})

## Start here

- [Installation]({{ '/guides/installation/' | relative_url }}): get the app for Linux, Windows or macOS.
- [Connecting to clusters]({{ '/guides/connecting-to-clusters/' | relative_url }}): kubeconfig, EKS, GKE and AKS login, and the
  permissions KubeScope needs.
- [Using KubeScope]({{ '/guides/using-kubescope/' | relative_url }}): a tour of every screen.
- [Troubleshooting]({{ '/guides/troubleshooting/' | relative_url }}): what the error messages mean.
- [Building from source]({{ '/guides/building-from-source/' | relative_url }}): run, test and package it yourself.

## Project links

- [Source code](https://github.com/dcotecnologia/kubescope) and
  [downloads]({{ '/install/' | relative_url }})
- [Contributing](https://github.com/dcotecnologia/kubescope/blob/main/CONTRIBUTING.md)
- [Security policy](https://github.com/dcotecnologia/kubescope/blob/main/SECURITY.md)
