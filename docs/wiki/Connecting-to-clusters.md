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
the `PATH`. The Flatpak runs the `aws` of your system on the host, so install it there
as usual.

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
| `get` on the non-resource URL `/version` | Checking that the cluster answers (most clusters allow it to every signed-in user) |
| `get`, `list` on `namespaces` | Namespace filter |
| `get`, `list` on `pods`, `services`, `endpoints`, `replicationcontrollers`, `deployments`, `statefulsets`, `daemonsets`, `replicasets`, `jobs`, `cronjobs` | Lists, details, overview |
| `get`, `list` on `endpointslices`, `ingresses`, `ingressclasses`, `networkpolicies` | The Network menu |
| `get`, `list` on `configmaps`, `secrets` (values are never shown), `resourcequotas`, `limitranges`, `horizontalpodautoscalers`, `poddisruptionbudgets`, `priorityclasses`, `runtimeclasses`, `leases`, `mutatingwebhookconfigurations`, `validatingwebhookconfigurations` | The Config menu |
| `get` on `pods/log` | Logs |
| `get`, `list` on `events` | Events in the workloads overview (optional) |
| `get`, `list` on `nodes` | Overview (optional) |
| `get`, `list` on `pods` and `nodes` in `metrics.k8s.io` | CPU and memory usage (optional) |

Leave `secrets` out of the role if you do not want the Secrets list; the other
lists keep working, but **Add-ons** then shows no Helm releases, because Helm stores
them as Secrets (KubeScope reads only their labels). On EKS, the IAM identity you sign in with must also be mapped
to the cluster (an access entry or the `aws-auth` ConfigMap) and bound to this
role; KubeScope itself asks AWS for nothing beyond `sts:GetCallerIdentity`.

A sample role:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kubescope-viewer
rules:
  - apiGroups: [""]
    resources: [namespaces, nodes, pods, pods/log, replicationcontrollers, services, endpoints, configmaps, secrets, resourcequotas, limitranges]
    verbs: [get, list]
  - apiGroups: [autoscaling]
    resources: [horizontalpodautoscalers]
    verbs: [get, list]
  - apiGroups: [policy]
    resources: [poddisruptionbudgets]
    verbs: [get, list]
  - apiGroups: [scheduling.k8s.io]
    resources: [priorityclasses]
    verbs: [get, list]
  - apiGroups: [node.k8s.io]
    resources: [runtimeclasses]
    verbs: [get, list]
  - apiGroups: [coordination.k8s.io]
    resources: [leases]
    verbs: [get, list]
  - apiGroups: [admissionregistration.k8s.io]
    resources: [mutatingwebhookconfigurations, validatingwebhookconfigurations]
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
  - nonResourceURLs: [/version]
    verbs: [get]
```

Sections you cannot read are reported on the page instead of failing it.

### Write mode

The actions of the write mode (Settings, off by default) need more rights, only
for the contexts where you use them:

| What | Used for |
| ---- | -------- |
| `delete` on `pods` | Delete a Pod |
| `create` on `pods/eviction` | Evict a Pod |
| `patch` on `deployments/scale` | Scale a Deployment |
| `patch` on `deployments` | Restart a Deployment |

The commands the menu shows are run by you with `kubectl`, not by the app: the
shell needs `create` on `pods/exec`, and Forward needs `get` on `services` and
`pods` and `create` on `pods/portforward`.

## Cluster info, Node Groups and EKS add-ons (EKS only)

These come from the AWS API, not from the cluster, so they need IAM
permissions on the identity you sign in with, besides the Kubernetes role:

| What | Used for |
| ---- | -------- |
| `eks:DescribeCluster` | The Cluster info card on the Overview |
| `eks:ListNodegroups`, `eks:DescribeNodegroup` | The Node Groups entry |
| `eks:ListAddons`, `eks:DescribeAddon` | The EKS add-ons in **Add-ons** (Config menu) |

The cluster name, region and profile are read from the `aws eks get-token`
command in your kubeconfig. Contexts that are not EKS do not show these entries,
and without the permissions the list reports the access error.

## Metrics

CPU and memory in the lists and on the overview come from `metrics-server`. If
the cluster does not have it, those columns show `—` and everything else works.
