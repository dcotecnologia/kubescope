# Themes

The themes that are built into the app, `light.json` and `dark.json`: KubeScope reads them at start, and
`palette` lists exactly what each light color becomes (Light softens the white of the code into grays).

Any other theme is not here: the app has no theme besides these two. The themes people made are files in their
themes folder, and the others come from extensions: the extension
[`kubescope-themes`](https://github.com/dcotecnologia/kubescope-themes) offers Abyss, Midnight, Monokai,
Solarized and more, and installs with the app. To add a theme to it, see its README.

A theme is JSON with a `name`, a `base` (`light` or `dark`) and the `colors` it changes; everything else comes
from the base. See "Themes" in the main README for the format and `ROLES` in `src/kubescope/theme.py` for the
color names.

## Transparency

A theme can add an `opacity` object that gives any color role an opacity from `0`
(clear) to `1` (solid), for example `"opacity": {"page": 0.8, "topbar": 0.75}`. The
theme editor has a slider for each role. That role's color is drawn translucent, and
the window lets the desktop show through. It needs a desktop compositor; the blur
behind the window, as macOS does it, is not available.

Be careful with `surface` and `surface_alt`: lists, trees and scroll areas draw them,
and a translucent background there can be painted over its own old pixels, which
shows as ghost text.
