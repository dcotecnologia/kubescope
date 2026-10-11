# Store screenshots

Screenshots of KubeScope in several themes, for the app stores (Flathub, the
Microsoft Store, the Ubuntu store) and for anywhere else the app is shown. They are
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

The Flatpak metainfo points at these files on `main`, so a store listing picks them
up when they change. For another store, upload the files you want; check its current
size and number limits first.

To redraw all of them, for example after the interface changed:

```bash
make store-screenshots
```

Commit the PNGs it rewrites together with the change that made them differ.
