---
layout: page
title: Gabi, the assistant
permalink: /assistant/
---

Gabi is the AI assistant of KubeScope, made by DCO Tecnologia. She is an expert in Kubernetes and KubeScope, she only talks about them, and she answers in the language of the app, in any of its 21 languages.

## How it works

Gabi does not run on a server of KubeScope. She runs on a coding assistant that is **already installed and signed in on your computer**: [Claude Code](https://claude.com/claude-code) or [Codex](https://github.com/openai/codex). KubeScope hands that program your question and shows its answer. It asks you for no credentials and stores none: the sign-in stays with the program.

The program is started so that it can only answer, never act. Claude Code runs with no tools, and Codex with its shell, file viewing, plugins, browser and web search switched off. Gabi cannot read a file of your computer or run a command.

## Set it up

1. Install Claude Code or Codex and sign in, as you would to use them in a terminal.
2. Open the round button in the corner of the window. The first time, you agree that what you ask and what she reads from the cluster go to that program and to its service. Nothing is sent before that.
3. In **Settings**, the **Assistant** card turns the button on or off, picks the program, and takes the path of a program the system does not find by itself.

## What she can do

- **See what you see:** the list and its rows, the selected row, the namespace and the search, the open Details or Logs, the numbers of the overviews and your open tabs.
- **Look into a problem:** she reads the details of a resource, the logs of a Pod, lists and events, and tells you what she checked, what the evidence shows and how sure she is.
- **Take you there:** she goes to a list, an overview, Settings, a namespace, a context, a search, the details of a resource, the logs of a Pod or a tab that is open, as if you had clicked.
- **Propose a change:** only with the write mode on, as a card with **Run** and **Cancel**. She never does it herself.

In the default **read-only mode** she cannot edit, update or delete anything, and she says so when you ask. She may still show the command or YAML for you to review and run yourself.

## In the chat

Resize the panel by its edges, take it out into a window of its own, and attach images and text files with **+** or by pasting a picture. Conversations are kept on your computer for each context, without the data that was read, and you can clear them.

## What leaves your computer

What you type and attach, a description of the window and what Gabi asks the app to read, with Secret values hidden and tokens and keys redacted. A password that an application prints inside a sentence of a log can still go, so be careful on a cluster whose logs hold secrets. The [security notes](https://github.com/dcotecnologia/kubescope/blob/main/SECURITY.md) have the whole account.

Gabi is an AI and can be wrong: read the commands she suggests before you run them.
