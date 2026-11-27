# Store screenshots

Screenshots of KubeScope in several themes, for the README, the docs and anywhere else the app is shown. They are
1600x900 PNGs (16:9) drawn from the preview's fake data, so they hold no real
cluster names.

| Screenshot | Shows |
| ---------- | ----- |
| `overview-<theme>.png` | The cluster overview with the Workloads and Network menus open |
| `deployments-<theme>.png` | The Deployments list |
| `details-dark.png` | The JSON of a resource, colored |
| `logs-dark.png` | Pod logs with colored levels |

The themes are `dark`, `light`, `midnight`, `sepia` and `high-contrast`. The
details and logs are made in the dark theme only.

To redraw all of them, for example after the interface changed:

```bash
make store-screenshots
```

Commit the PNGs it rewrites together with the change that made them differ.
