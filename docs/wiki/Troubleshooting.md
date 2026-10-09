# Troubleshooting

KubeScope turns common `kubectl` failures into a short message with a hint. The
original text is always available: hover the message, or press **Show details** in
an error dialog.

| Message | What it means | What to do |
| ------- | ------------- | ---------- |
| Login tool not found | The kubeconfig runs a program (usually `aws`) that is not installed or not on the `PATH` | Install it, make sure it is on the `PATH`, then Refresh |
| Authentication failed | The credentials are missing or expired | Use the **Sign in to AWS** button, or run `aws sso login` yourself, then Refresh. For access keys, use **Configure AWS credentials** or run `aws configure` |
| Access denied | Your user cannot read that resource | Ask for a read-only role; see [Connecting to clusters](Connecting-to-clusters#permissions) |
| Cluster unreachable | The API server did not answer | Check the network or VPN and that the cluster is running |
| Context not found | The context is not in your kubeconfig | Check `~/.kube/config` or `KUBECONFIG` |
| kubectl is missing | The bundled `kubectl` was not found | Reinstall the app |

## Reporting a problem

Turn on **Settings > Debug mode**, reproduce the problem, then use **Open the log
folder** and attach `kubescope.log` (and `crash.log` if the app closed by itself)
to your report. The log records the commands the app ran and how they ended,
never Pod logs or resource contents, and hides tokens and keys. It does include
context names, so read it first and edit what you do not want to share.

## CPU and memory show a dash

The cluster has no `metrics-server`, or your role cannot read `metrics.k8s.io`.
The other columns are unaffected.

## A Deployment's CPU or memory looks too low

The numbers add up only the Pods that have metrics. Pods that just started may not
have reported yet.

## EKS works in a terminal but not in the Flatpak

The Flatpak only has the AWS CLI. If your kubeconfig uses another login tool, use
the `.deb` or the AppImage.

## Where are the settings

- Linux: `~/.config/kubescope/settings.json`
- Windows: `%APPDATA%\kubescope\settings.json`
- macOS: `~/Library/Application Support/kubescope/settings.json`

Set `KUBESCOPE_CONFIG_DIR` to use another folder. Delete the file to reset
everything.

## Still stuck

Open an [issue](https://github.com/dcotecnologia/kubescope/issues) with your
version, platform and the error text. Remove cluster names, account IDs and tokens
first. For security problems, follow the
[security policy](https://github.com/dcotecnologia/kubescope/blob/main/SECURITY.md)
instead.
