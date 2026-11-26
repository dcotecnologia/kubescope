# Accessibility

KubeScope is a desktop app for Kubernetes. We want people to be able to use it whatever way they work:
with a keyboard only, with a screen reader or a magnifier, with a high contrast theme, with less motion,
or in a language that is read from right to left. This page says what we do, what we know is missing and
how to tell us about a barrier.

## Where we stand

KubeScope **has not been audited for accessibility**, and we do not claim to conform to WCAG, EN 301 549
or Section 508. What follows is what the app does by design and what we know from reading and using it. It
is not the result of tests with assistive technology, which we have not done yet. If this page says
something is there and you find it is not, that is a bug: please tell us.

This page covers the desktop app, [the site](https://kubescope.dcotecnologia.com/) and its guides. The
extensions are projects of their own; the pages they add are made of the same widgets, but each one is
the work of its author.

## Our commitment

- We treat a barrier as a bug. It is fixed in the normal flow of the project, first the ones that stop a
  person from doing a task at all.
- When we add or change the interface, we try not to rely on color alone, to keep it reachable by keyboard
  and to leave the text to the system and to the translations.
- We keep this page true: what is fixed leaves the list of limitations, and what we learn is added to it.

## What the app does today

- **Standard controls.** The window is made of Qt widgets, which expose their names, roles and states to the
  accessibility interface of each system (UI Automation on Windows, AT-SPI on Linux, NSAccessibility on
  macOS). We have not checked how well each screen reader reads each screen.
- **Keyboard.** The menus, buttons, tables, dialogs and Settings are the standard controls of the platform,
  so they follow its keyboard conventions. The main screens and the global search have shortcuts
  (for example `/` and `Ctrl+K` for the search); on a list, `Enter` opens the details of the row and, in the write mode, `Delete` and `Ctrl+E` delete and edit it, and every shortcut can be changed or turned off in
  **Settings → Shortcuts**.
- **Themes and contrast.** There are a Light and a Dark theme, and you can make your own in **Settings →
  Theme**, with every color role editable. The Themes extension adds a High Contrast theme among others.
  The window follows the theme in use at once.
- **Not only color.** The status of a Pod or an event is also written in the list, in a badge
  with its name ("Running", "Warning", "Failed", ...), and the numbers of the overview are shown as text
  beside their bars.
- **Motion.** The animations (windows and lists rising into place, the side menu sliding) can be turned off
  in **Settings**.
- **Text size.** **Settings → Text size** goes from 85% to 150% of the usual size; a few small labels drawn
  with a fixed size do not follow it. The app also follows the scaling of the operating system.
- **Language.** The interface is translated into 21 languages, including Arabic, Persian and Hebrew, and the
  direction of the layout follows the language.
- **The window.** By default the window draws its own title bar. **Settings → Use the title bar of the
  system** gives it the one of your desktop.

## Supported environments

KubeScope runs on Linux, Windows and macOS (see [the install page](https://kubescope.dcotecnologia.com/install/)). We have **not tested it with any
screen reader**. The ones we would most like to hear about are Orca on Linux, NVDA and Narrator on Windows
and VoiceOver on macOS. A report of a barrier with a combination that works for you or does not is useful
in either case.

## Known limitations

These come from reviewing the code, not from an audit, so there may be more.

- **Mouse only.** The box in the header of the lists that checks every row, dragging the dividers to
  resize a column, and the **Reorganize** menu that moves a block of the side menu (right click on its
  title) have no way of being done from the keyboard yet. The boxes of the rows can be toggled with the
  space key.
- **Drawn by hand.** The box in the header, the pills of the status and the small squares that show the
  state of each container are drawn by the app and not by the system, so a screen reader may not announce
  them as a check box or a state. The state of the containers is color, with its name only in the tooltip
  that shows when the pointer is on it; the ready count (`1/1`) beside it is text.
- **The icons of the groups** that the extension for custom resources adds to the side menu are the first
  letters of the name of the group on a color made from it. The color helps to tell them apart, but the
  letters are what to rely on.
- **The site** has not been checked with assistive technology either.

## Tell us about a barrier

- Open an
  [accessibility issue](https://github.com/dcotecnologia/kubescope/issues/new?template=accessibility.yml).
  It asks for what you were trying to do, what stopped you, the assistive technology you use and your system.
- Or email <danilogcarolino@gmail.com> with the subject `KubeScope accessibility`.

Please do not paste credentials, tokens, kubeconfig contents, Pod logs or cluster data. A description and
a screenshot are enough.

You can expect an acknowledgement within a few days. We will say whether we can fix it and, when we can,
which release has the fix. If you suggest a way to make something easier, that is as welcome as a bug.
