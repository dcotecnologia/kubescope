# Submitting KubeScope to Flathub

Flathub has no upload. An app is added by a pull request to
[flathub/flathub](https://github.com/flathub/flathub); reviewers read it, and Flathub
builds the app from the manifest. Once accepted, Flathub creates
`github.com/flathub/com.dcotecnologia.KubeScope`, and later updates are commits to that
repository. The rules are in the
[submission guide](https://docs.flathub.org/docs/for-app-authors/submission).

Nothing here is automated, on purpose: read Flathub's generative AI policy on the
[requirements page](https://docs.flathub.org/docs/for-app-authors/requirements) first. A
manifest and the text of the pull request must be written by a person, and an AI tool must
not open the pull request. The files that `make flathub-submission` writes are a starting
point to check and to rewrite by hand, not text to send.

## Before it is opened

- The release tag exists on GitHub (for example `v1.2.0`). Flathub builds from it.
- The git source of `packaging/flatpak/com.dcotecnologia.KubeScope.yml` names that tag
  and the commit it points at (`git rev-parse v1.2.0^{}`; the commit, not the tag
  object).
- The manifest was reviewed by hand, including the permissions in `finish-args`. The ones
  that reviewers question, and why the app has them, are in [SECURITY.md](../SECURITY.md).
- The app ID `com.dcotecnologia.KubeScope` is tied to a domain that the project controls;
  Flathub verifies it with a file on the website. Without that domain, Flathub asks for an
  ID based on the code host, and the ID changes in every packaging file.

```bash
make flatpak-lint          # validates the metainfo, the desktop file and the manifest
make flathub-submission    # writes dist/flathub/com.dcotecnologia.KubeScope/
```

Run `make flathub-submission` again after any change to `packaging/flatpak/`, or the copy
in `dist/` is out of date.

## Open the pull request

Fork `flathub/flathub` with "Copy the master branch only" **unchecked**, or the `new-pr`
branch is not in the fork. This project's fork is `dcotecnologia/flathub`.

```bash
# 1. clone on the new-pr branch
git clone --branch=new-pr git@github.com:dcotecnologia/flathub.git ~/flathub
cd ~/flathub
git checkout -b add-com.dcotecnologia.KubeScope new-pr

# 2. the files made by make flathub-submission, at the root
cp -r /path/to/kubescope/dist/flathub/com.dcotecnologia.KubeScope/. .
git add .
git commit -m "Add com.dcotecnologia.KubeScope"
git push origin add-com.dcotecnologia.KubeScope

# 3. the pull request, against the new-pr base of the original repository
gh pr create --repo flathub/flathub --base new-pr \
  --head dcotecnologia:add-com.dcotecnologia.KubeScope \
  --title "Add com.dcotecnologia.KubeScope"
```

- The base is `new-pr`, not `master`. Keep the template of the pull request and answer its
  checklist.
- Your account needs push access to `dcotecnologia/flathub`.
- Do not add an AI assistant as a co-author of the commit.

## After it is opened

- Reviewers answer on the pull request, and a Flathub bot builds the app to test it.
  The permission `--talk-name=org.freedesktop.Flatpak` makes the linter report
  `finish-args-flatpak-spawn-access`; an exception has to be requested and may be denied.
  Without that permission the Flatpak cannot run any sign-in program, so only kubeconfigs
  with a token or a certificate of their own work; the `.deb`, the AppImage and the snap
  cover the other cases.
- When it is accepted, the repository `flathub/com.dcotecnologia.KubeScope` is created.
  Updates are commits to it: change `tag` and `commit` of the git source, and regenerate
  `python3-kubernetes.json` with `python tools/flatpak_python_deps.py` when `uv.lock`
  changes the dependencies.
- An `x-checker-data` block on the git source lets Flathub's bot open the update pull
  requests for new tags. Write it by hand, like the rest of the manifest.
