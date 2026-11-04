---
name: pen-files
description: Read and keep .pen files safe - the object tree, components and instances, slots, variables and themes, libraries, the schema version read every job, the safe edit routine with a new output file and Git, and the conflict routine without hand-editing JSON. Use whenever a job opens, changes, merges or hands over a .pen file.
---

# .pen files

A `.pen` file is pen.dev's design document: plain JSON that Git can track like code. This skill says what is inside one, so the agent can read a design, plan a change and check the result, and how to keep the file safe: read the version first, change it only through pen.dev's tools, write to a new file, and commit. It follows pen.dev's public schema page as read on 2026-10-31, when the schema version was `2.21`. pen.dev says the format may still change in ways that break old readers, so nothing here is taken for granted on a file with another version.

Marks as in pendev-work: «(read from docs.pen.dev, not tried)» follows the public docs and has not been run by us; a step with no mark is a plain shell command or a question to the owner.

**Route:** read the version → read the structure → plan the change in pen.dev terms → safe edit routine → reopen and look → commit.

## When to use

- A job opens, changes, merges or hands over a `.pen` or `.lib.pen` file.
- Planning a change: which frame, component or variable it touches.
- Git reports a conflict in a `.pen` file.

## Inputs

- The file in `<dir>/in` (pendev-work, Connect, step 4), committed.
- The job folder `<dir>` is a Git repository.

## What is inside

- **The document.** A top-level object with `version`, optional `themes`, `imports` and `variables`, and `children`: the objects placed on an endless canvas.
- **Objects.** Every object has an `id` that is unique in the document and a `type` such as frame, group, rectangle, ellipse, path, text, icon or ref; the schema on pen.dev's page lists them all. Objects nest: a child's position is counted from its parent's top-left corner.
- **Layout.** A parent can lay out its children in a row or a column, flexbox-style (`layout`, `justifyContent`, `alignItems`, gaps); a child can fill its parent or keep a fixed size, and a parent can fit its children. Inside such a layout, `x` and `y` of the children are ignored.
- **Look.** Fills (solid colour, gradients, an image, a mesh gradient, and more), one stroke that may carry several fills, and effects, all applied in the order written.
- **Components and instances.** `reusable: true` turns an object into a component. An object of type `ref` pointing at its id is an instance. An instance can override its own properties, change parts inside it through `descendants` (nested parts by joined ids with a slash), or swap the children of a container part. A part marked as a `slot` is meant to be filled with instances of the components it suggests.
- **Variables and themes.** Document-wide variables for colours, numbers, strings and booleans, used by `$name`. A variable can hold several values, one per theme; `themes` names the axes (for example mode and spacing) with the first value as the default, and a frame can set its own theme for everything under it.
- **Libraries.** `imports` maps a short alias to a relative path of a `.lib.pen` file whose components and variables the document uses. Images, fonts and libraries are found by relative paths, so they move together with the file.

## Rules

- **Read the version every job** (F1). The schema may change; a file with another version is kept as it was before pen.dev opens it.
- **Read freely, write never.** Reading the JSON with `jq` is fine. Every change goes through pen.dev, the CLI shell or the MCP tools; never write the JSON by hand, not even one id.
- **New file out.** The input stays in `<dir>/in`; the changed design is a new file in `<dir>/out` (pendev-work, rule «Never over the input»).
- **Git is the history.** Commit the input before the first change and after each agreed step. Save and close the file in pen.dev before switching branches or pulling.
- **Assets travel together.** Keep images, fonts and `.lib.pen` files at the relative paths the document uses inside `<dir>`.
- **A library is for good.** Turning a file into a library cannot be undone: only with the OK of the owner or the design system keeper.

## Recipes

### F1. Read the version (every job)

1. `jq -r .version <dir>/in/<name>.pen` and write it into the step log. On 2026-10-31 the schema page said `2.21`.
2. Another version than the one on the schema page: keep the committed original in `<dir>/in` untouched, tell the owner, and work on the copy in `<dir>/out`. pen.dev converts older formats when it opens a file and saves the new one; it refuses a format it does not know, which means the app needs an update, the owner's step (read from docs.pen.dev, not tried).

### F2. Read the structure, without changing it

pen.dev also reads JSON with comments. If `jq` cannot parse the file, it holds comments: read it through pen.dev (step 4) instead.

1. Top level: `jq -r '.children[] | [.id, .type, (.name // "")] | @tsv' <dir>/in/<name>.pen`.
2. Components: `jq -r '.. | objects | select(.reusable == true) | [.id, (.name // "")] | @tsv' <dir>/in/<name>.pen`.
3. Variables, themes and libraries: `jq '{themes, imports, variables: (.variables // {} | keys)}' <dir>/in/<name>.pen`.
4. In pen.dev: `get_app_state()` for the active document and selection, `Get(...)` inside `execute` for the live tree (read from docs.pen.dev, not tried).

### F3. The safe edit routine

1. `sha256sum <dir>/in/<name>.pen > <dir>/in.sha256`, commit.
2. Open the work copy `<dir>/out/<job>.pen` in pen.dev, or start the headless shell with `--in` and `--out` (pendev-work, Connect).
3. `get_app_state()`, then the change through `execute` (read from docs.pen.dev, not tried).
4. Save, reopen the file and take a screenshot of the changed frames (read from docs.pen.dev, not tried).
5. `sha256sum -c <dir>/in.sha256` prints «OK»; `jq -r .version <dir>/out/<job>.pen`; commit.

### F4. A Git conflict in a .pen file

1. Keep both sides as separate files: `git -C <dir> show :2:<path> > <dir>/out/<job>-ours.pen` and `git -C <dir> show :3:<path> > <dir>/out/<job>-theirs.pen`.
2. Choose one as the base, with the owner if the choice is not obvious.
3. Open the base in pen.dev and make the other side's changes again there, looking at the other file side by side (read from docs.pen.dev, not tried).
4. Never fix the conflict markers or the JSON by hand.
5. Save, reopen, look at every frame the two sides touched, then commit the result (read from docs.pen.dev, not tried).

### F5. Libraries and assets

1. List libraries with `jq .imports <dir>/out/<job>.pen`; in the headless shell, `list_libraries()` (read from docs.pen.dev, not tried).
2. Import or remove a library only for the job and with the owner's OK: `import_library({ path })` and `remove_library({ id })` in the shell; removing turns its instances into plain copies (read from docs.pen.dev, not tried).
3. Before the hand-over, check that every relative path the document uses exists inside `<dir>`.

## Checks before hand-over

- The version was read and logged, and a different one was reported.
- The input's checksum is unchanged; the output is a new file.
- No `.pen` was written by hand: every change is in a pen.dev step log.
- Every relative asset and library path resolves inside `<dir>`.
- A commit per agreed step.

## Hand-over

- The `.pen` and its assets in `<dir>/out`, with the version in the note.
- Libraries, tokens and variable sync with code go to the design system keeper.

## Sources

This skill is made by harnsy, not an official pen.dev product. pen.dev is a product of High Agency, Inc.; no endorsement by High Agency, Inc. is implied.

Facts only, no text taken: the pen.dev documentation (https://docs.pen.dev/for-developers/the-pen-format, schema version 2.21; https://docs.pen.dev/core-concepts/pen-files; https://docs.pen.dev/core-concepts/design-libraries; https://docs.pen.dev/for-developers/pen-cli), read 2026-10-31; © 2026 High Agency, Inc. The `jq` and Git commands are our own.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
