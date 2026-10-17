# Themes

The themes that come with the app, one `*.json` file each. `light.json` and
`dark.json` are the two built-in themes: KubeScope reads them at start (`dark.json`
lists in `palette` exactly what each light color becomes). Every other file is copied
to the user's themes folder when KubeScope starts, whenever that file is missing, so
everybody gets it in **Settings > Theme** and a file deleted by hand comes back. A
file that is there is never overwritten, so the person's edits are kept. None of the
themes here can be deleted from the app; only the themes the person makes can.

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
