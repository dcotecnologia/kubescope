# Community themes

Themes made by the community. Each `*.json` file here is copied to the user's themes
folder the first time KubeScope starts with it, so everybody gets them in
**Settings > Theme**. A theme is installed once: one the person edited is never
overwritten, and one they deleted does not come back.

## Add a theme

1. In KubeScope, **Settings > New theme...**, pick the colors and save. Your theme is
   written to the themes folder (**Open the themes folder**).
2. Copy that file here and give it a short, lowercase name (`my-theme.json`). The file
   name is the theme's id.
3. Run `make test`: it checks that every theme here is valid and uses known colors.
4. Open a pull request, ideally with a screenshot.

A theme is JSON with a `name`, a `base` (`light` or `dark`) and the `colors` it
changes; everything else comes from the base. See "Themes" in the main README for the
format and `ROLES` in `src/kubescope/theme.py` for the color names.

Keep text readable: aim for a contrast of at least 4.5:1 between `text` and `page`.
