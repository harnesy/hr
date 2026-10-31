---
name: figcraft-work
description: Do interface design work in FigCraft over its MCP server - screens with auto layout, starter templates, components with instances and overrides, variables and tokens with modes, PNG/SVG/PDF exports, design-to-code hand-over material, and the native file - each recipe proven on FigCraft 0.7.0, with the check after every step, undo, and the list of what not to promise. Use for any job done in FigCraft; it also holds FigCraft's Connect table for connecting the app and handing over files.
---

# FigCraft work

FigCraft is an open-source interface design app in alpha: pages of frames, shapes, text, components and instances, with auto layout, styles and variables. Every menu action is a command, and its MCP server lets an agent build and inspect designs headless. This skill is the manual for that work: how to connect, how the app thinks, the recipes that were run for real on FigCraft 0.7.0, how to look at the result, how to undo, and what not to promise.

**Route:** connect (with the Connect table below) → agree the deliverables → recipes → look at the result after each step → hand over the files.

## When to use

- A job in FigCraft: lay out screens, build components, set up tokens, export assets, prepare a hand-over for developers.
- The owner asks what FigCraft can and cannot deliver.

## Inputs

- The read folder `<in>` and the write folder `<out>`, as absolute paths.
- The agreed deliverables list.
- The brief: screens, sizes, content, brand colours and type the owner provides. Never invented brand assets.

## Connect table (FigCraft)

| Item | Value |
|---|---|
| Programs | `figcraft` (desktop app), `figcraft-cli` (CLI and MCP server); the Linux AppImage runs the CLI as `<AppImage> cli <args>` |
| CLI location | Linux deb or rpm: `/usr/bin/figcraft-cli`; Linux tar.gz: `<unpacked folder>/bin/figcraft-cli`, not on the PATH. macOS: the separate release asset `figcraft-cli-<version>-macos-universal.zip`. Windows: the program folder of the installer; use the full path |
| Releases | github.com/storytold/figcraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | `--automation-read-root <dir>` and `--automation-write-root <dir>`, first in 0.7.0, proven here; each may repeat, and each folder must exist or the server does not start. Reads only inside a read or write folder, writes only inside a write folder; anything else is refused (`automation path rejected: <path> is outside the folders that may be written: <dir>`) and nothing is written. Without the flags the server reads and writes anywhere the user can. Below 0.7.0 (`figcraft-cli --help` shows only `mcp [--attach PORT]`): stop and ask the owner to update |
| Headless start | with folder limits: `figcraft-cli mcp --automation-read-root <in> --automation-write-root <out>` |
| Attach (owner watches) | the owner starts `figcraft --control <port>` with the same folder limits; the server is `figcraft-cli mcp --attach <port>`, which refuses the limit flags (the app does the confining). The control port has no token: attach only on a single-user machine, and close the app's port after the job |
| Register | `claude mcp add figcraft -- figcraft-cli mcp <flags>` |
| Prove | `list_commands {filter}`, `inspect_document {depth: 1}`, and one write outside `<out>` that must be refused |
| Check commands | reopen a copy with `open_file`; facts with `figcraft-cli info <file> --json`; eye with `screenshot {ids, maxSize}` (default 1600) |
| Version | `figcraft-cli --version` |
| Repeatable text | `--no-system-fonts` uses only the fonts built into the app |

## The model

- A document has pages; a page holds frames, groups, sections, shapes, text, components and instances. Styles and variables (collections with modes) belong to the document.
- Coordinates are page units, x to the right, y down. `x` and `y` count from the top-left corner of the frame a layer sits in; a layer directly on the page uses page coordinates.
- Children of an auto layout frame are placed by the layout (`layout`, `gap`, `padding`, `mainAlign`, `crossAlign`, `sizingH`, `sizingV`), not by `x` and `y`.
- Every action is a command: find ids and params with `list_commands {filter}`, run one with `run_command`, several as one undo step with `batch`. Without `ids`, a command works on whatever is selected, and a newly created layer is selected automatically.

## Rules

- **Create the container first, then fill it.** Make the frame with `create_node`, then batch its children with `parent: <id>`. From 0.7.0 a step of a `batch` may also use the id an earlier step of the same batch returned, `parent: {"$step": 0}` (counted from 0); below 0.7.0 it cannot.
- **A batch is all or nothing**: if one step fails, the whole batch is rolled back and the error names the step.
- **Check after each structural step** with `get_node` (sizes, positions, overrides), and with `screenshot` for the eye.
- **Name the document** when it is created (`file.new {name}`), or with `file.rename {name}`; a save does not name it, and an unnamed document stays «Untitled».
- **Reopening needs a copy.** `open_file` on a path that is already open returns the open document without reading the disk (still in 0.7.0: the reply is only `opened: {index}`). To check a saved file, copy it (`cp <out>/<job>.figcraft <out>/<job>-check.figcraft`) and open the copy, or close the document first.
- **Paths:** absolute, inside `<in>` for reading and `<out>` for writing; the server refuses anything else (files in `<out>` may be read too).
- **No sharing.** Never Share ▸ Online, live sessions, publishing a plugin or a collaboration server without the owner's explicit OK for that file. When asking, say: the file is uploaded to a server (a public one by default), the link is the access, it is not end-to-end encrypted, and there are no accounts.
- **Attached mode:** after a transport error, inspect before retrying; the call may have been applied.

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name.

### F1. A screen with auto layout (proven on FigCraft 0.7.0)

1. `run_command file.new {name: "<job>"}`.
2. `create_node {type: "frame", name: "Screen / Home", x: 0, y: 0, width: 390, height: 844, props: {fill: "#FFFFFF", layout: "vertical", gap: 16, padding: 24, sizingV: "fixed"}}`; note the id.
3. `batch` the content with `parent: <frame id>`, for example `node.create {type: "text", parent, name: "Title", text: "<title>", props: {fontSize: 28, fontStyle: "Bold", fill: "#111827"}}`, a subtitle text, `node.create {type: "rectangle", parent, name: "Hero", width: 342, height: 180, props: {fill: "#DBEAFE", cornerRadius: 16}}`.
4. `get_node {id: <frame id>, depth: 1}`: children stacked from `y` 24 with the gap between them, widths as set.
5. `screenshot {ids: [<frame id>], maxSize: 300}` and look.

### F2. Start from a starter template (proven on FigCraft 0.7.0)

1. `run_command template.list {}`: ids such as `mobile-app`, `landing-page`, `dashboard`, `design-system`.
2. `run_command file.newFromTemplate {template: "<id>", name: "<job>"}`: a new, unsaved document becomes active.
3. `inspect_document {depth: 1}`: pages, top-level frames, styles; `screenshot {maxSize: 300}`.
4. Before delivery, replace the sample content with the owner's (`type_text {id, text}` for text). Tell the owner that the template's names, text and pictures are invented placeholders.

### F3. Components, instances and overrides (proven on FigCraft 0.7.0)

1. `create_node {type: "frame", name: "Button", x: 500, y: 0, props: {fill: "#2563EB", cornerRadius: 8, layout: "horizontal", padding: [12, 20, 12, 20], sizingH: "hug", sizingV: "hug", mainAlign: "center", crossAlign: "center"}}`.
2. `create_node {type: "text", parent: <button id>, name: "Label", text: "Continue", props: {fontSize: 16, fontStyle: "Medium", fill: "#FFFFFF"}}`.
3. `run_command component.create {ids: [<button id>]}`: the frame becomes a component in place.
4. `run_command instance.create {component: <button id>, parent: <screen frame id>}`, once per instance.
5. Overrides: find the label inside the instance with `get_node {id: <instance id>, depth: 1}`, then `set_properties {ids: [<label id>], props: {characters: "Cancel"}}`; `set_properties {ids: [<instance id>], props: {fill: "#E5E7EB", name: "Button / Secondary"}}`.
6. `get_node {id: <instance id>, depth: 1}`: `overrides` lists what changed; a change on the main component (for example `cornerRadius`) reaches every instance; `run_command component.list {}` shows the instance count.

### F4. Variables and tokens with modes (proven on FigCraft 0.7.0)

1. `run_command variable.createCollection {name: "Tokens", modes: ["Light", "Dark"]}`; note the collection id.
2. `run_command variable.create {collection, name: "color/surface-accent", type: "color", values: {Light: "#DBEAFE", Dark: "#1E3A8A"}}` and `variable.create {collection, name: "space/md", type: "number", values: {Light: 16, Dark: 24}}`.
3. Bind: `run_command variable.bind {ids: [<hero id>], field: "fill", variable: <colour id>}`; `variable.bind {ids: [<frame id>], field: "gap", variable: <spacing id>}`.
4. Check both modes: `run_command variable.setMode {ids: [<frame id>], collection, mode: "Dark"}`, `get_node` (the fill and the gap changed), `screenshot`; then back to `"Light"`.
5. Export: `run_command variable.export {format: "json", path: "<out>/<job>-tokens.json"}` and `{format: "css", path: "<out>/<job>-tokens.css"}`. The CSS file writes numbers without a unit (`--space-md: 16;`, still in 0.7.0). Add the unit in a hand-over copy, `sed -E 's/(--space-[^:]*: [0-9.]+);/\1px;/' <out>/<job>-tokens.css > <out>/<job>-tokens-px.css` (adjust the name pattern to the spacing tokens), or say in the note that the values are pixels.

### F5. Exports: PNG, SVG, PDF (proven on FigCraft 0.7.0)

1. PNG: `export {ids: [<frame id>], format: "png", scale: 2, path: "<out>/<job>@2x.png"}`: pixel size is the frame size times the scale.
2. SVG: `export {ids: [<frame id>], format: "svg", svgOutlineText: false, path: "<out>/<job>.svg"}` keeps text as `<text>`; leave `svgOutlineText` out to get outlines.
3. PDF: `export {ids: [<frame id>], format: "pdf", path: "<out>/<job>.pdf"}`, one page per frame; for every top-level frame of the page in one file: `run_command file.exportFramesPdf {path: "<out>/<job>-all.pdf"}`.
4. Check: `file <out>/<name>` gives the PNG pixel size and the PDF page count; `head -c 300 <out>/<job>.svg` shows the SVG's `width` and `height`; reopen the SVG with `open_file` (a new document; read `opened.warnings`), look at a `screenshot {maxSize: 300}`, then close it with `run_command file.close {index: <its index>}`.

### F6. Design-to-code hand-over (proven on FigCraft 0.7.0)

1. Mark the frame: `set_properties {ids: [<frame id>], props: {devStatus: "readyForDev"}}`. An edit inside it afterwards turns it «Changed» (`devChanged: true` in `get_node`); setting the status again clears that.
2. Code: `run_command inspect.code {id: <frame id>, language: "css"}`; for a component, `run_command inspect.componentCode {id: <component id>, language: "react"}`.
3. Properties with token names: `run_command inspect.properties {id: <layer id>}`.
4. Assets: give every layer that ships as a file an export setting, `run_command export.add {ids: [<layer id>], setting: {format: "svg"}}` (an image or icon may be listed without one); `run_command inspect.assets {ids: [<frame id>]}` lists them; then `run_command file.exportLayers {ids: [<frame id>], assets: true, dir: "<out>/assets"}`. Mark the frame ready again (step 1) after these edits.
5. Write what came back into files in `<out>` (`<job>-screen.css`, `<job>-Button.tsx`, `<job>-properties.txt`) and say in the note that generated code is a starting point for a developer, not tested code.

### F7. Save the native file and check it (proven on FigCraft 0.7.0)

1. `save_file {path: "<out>/<job>.figcraft"}`.
2. `cp <out>/<job>.figcraft <out>/<job>-check.figcraft`; `open_file {path: "<out>/<job>-check.figcraft"}`: a second document opens.
3. Compare: the `open_file` reply (`opened.summary` with name and pages, `opened.repairs` empty), `get_node` on the frame (`devStatus`, `boundVariables`) and `get_node {id: <instance id>, depth: 1}` (overrides kept); `figcraft-cli info <out>/<job>.figcraft --json` for pages, frames and variable counts.
4. `run_command file.close {index: <copy index>}`, then `rm <out>/<job>-check.figcraft`: the copy is not a deliverable.
5. A `.fig` export (`export {format: "fig", path}`) is experimental: deliver it only on request, with its `warnings` quoted and the line «written by FigCraft, checked only by reopening in FigCraft; other apps may not open it».

## Look at the result

- Numbers first: `get_node` or `inspect_document` (sizes, positions, fills, layout, overrides, bound variables).
- Then the eye: `screenshot {ids, maxSize}`; 300 is enough for layout, the default 1600 for detail. `window: true` only when attached and the owner watches.

## Undo

- `undo` and `redo` step through history: one command, one batch or one gesture per step. Check with `get_node` after each.
- A failed command or batch leaves the document unchanged; there is nothing to undo.
- Undo does not remove files already written; a wrong export is replaced under a new name.

## Do not promise

- Faithful opening of `.fig` files (best effort), or `.fig` files other apps accept (experimental).
- Results checked against real files of other design apps.
- Plugins written for other design apps.
- Multiplayer, accounts or a team cloud: sharing is a preview.
- Speed on very large files: the canvas renders on the CPU.
- Print-ready CMYK: PDF CMYK is a simple conversion without an output profile.
- HEIC images or video.
- Screen-reader accessibility of the app itself.
- Generated code as production code.

## Checks before hand-over

- Every output was reopened or checked and looked at (deliverable hand-over steps).
- The `.figcraft` file sits next to the exports; the document has a name.
- Token CSS carries units or the note says the values are pixels.
- Nothing was shared or uploaded.
- All documents are closed: `inspect_ui` shows no documents, including the empty «Untitled» one a headless session starts with.

## Artefacts

- `<out>/<job>.figcraft`, the agreed exports, code and token files, `HANDOVER.md`, `SHA256SUMS.txt`.

## Hand-over

- Files stay in `<out>`; the owner sends or publishes them.
- Code and tokens go to the developer as starting material, with the note's caveats.

## Sources

No endorsement by these projects or their authors is implied.

Built on FigCraft documentation (github.com/storytold/figcraft, commit 47438dd4a2e8b49a7e6bb3dfd480262dadc37f12; © 2026 ArtCraft Team and the FigCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
