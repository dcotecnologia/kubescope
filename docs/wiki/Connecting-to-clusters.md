# Connecting to clusters

## Which kubeconfig is used

KubeScope reads the kubeconfig with the official Kubernetes client, so it finds
the same configuration `kubectl` would:

- the files listed in the `KUBECONFIG` environment variable, if it is set;
- otherwise `~/.kube/config` (`%USERPROFILE%\.kube\config` on Windows).

Every context in that file shows up in the context box. In **Settings** you can
give a context a friendlier display name; the real name is still used for every
request.

## Amazon EKS

EKS kubeconfigs call `aws eks get-token`, so the **AWS CLI must be installed** and
you must be signed in (for example `aws sso login`). On Windows it has to be on
the `PATH`. The Flatpak bundles the AWS CLI for you.

When you open a context, KubeScope checks that you are signed in. If your AWS SSO
session has expired, a **Sign in to AWS** button appears in the footer. It runs
`aws sso login` with the profile your kubeconfig uses, opens the browser, and
reloads the data when you are done. The button names the profile it will use. If
the profile uses access keys instead, the button reads **Configure AWS
credentials** and opens a terminal with `aws configure` for that profile; type
the keys there, then press Refresh. KubeScope never sees the keys.

## Google GKE

GKE kubeconfigs call `gke-gcloud-auth-plugin`, so install it and the Google Cloud
CLI (`gcloud`), and make sure both are on the `PATH`. When your credentials
expire, a **Sign in to Google Cloud** button appears in the footer. It runs
`gcloud auth login`, opens the browser, and reloads the data when you are done.

## Azure AKS

AKS kubeconfigs call `kubelogin`, so install it and the Azure CLI (`az`), and make
sure both are on the `PATH`. When your credentials expire, a **Sign in to Azure**
button appears in the footer. It runs `az login`, opens the browser, and reloads
the data when you are done. This fits kubeconfigs converted with
`kubelogin convert-kubeconfig -l azurecli`; with other login modes of `kubelogin`
(service principal, device code) sign in the way that mode asks.

## Permissions

Use a read-only role. KubeScope needs:

| What | Used for |
| ---- | -------- |
| `get`, `list` on `namespaces` | Namespace filter |
| `get`, `list` on `pods`, `services`, `endpoints`, `replicationcontrollers`, `deployments`, `statefulsets`, `daemonsets`, `replicasets`, `jobs`, `cronjobs` | Lists, details, overview |
| `get`, `list` on `endpointslices`, `ingresses`, `ingressclasses`, `networkpolicies` | The Network menu |
| `get` on `pods/log` | Logs |
| `get`, `list` on `events` | Events in the workloads overview (optional) |
| `get`, `list` on `nodes` | Overview (optional) |
| `get`, `list` on `pods` and `nodes` in `metrics.k8s.io` | CPU and memory usage (optional) |

A sample role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kubescope-viewer
rules:
  - apiGroups: [""]
    resources: [namespaces, nodes, pods, pods/log, replicationcontrollers, services, endpoints]
    verbs: [get, list]
  - apiGroups: [apps]
    resources: [deployments, statefulsets, daemonsets, replicasets]
    verbs: [get, list]
  - apiGroups: [networking.k8s.io]
    resources: [ingresses, ingressclasses, networkpolicies]
    verbs: [get, list]
  - apiGroups: [discovery.k8s.io]
    resources: [endpointslices]
    verbs: [get, list]
  - apiGroups: [batch]
    resources: [jobs, cronjobs]
    verbs: [get, list]
  - apiGroups: [""]
    resources: [events]
    verbs: [get, list]
  - apiGroups: [metrics.k8s.io]
    resources: [nodes, pods]
    verbs: [get, list]
```

Sections you cannot read are reported on the page instead of failing it.

## Metrics

CPU and memory in the lists and on the overview come from `metrics-server`. If
the cluster does not have it, those columns show `—` and everything else works.
