---
name: vectorcraft-work
description: Do vector graphics work in VectorCraft over its MCP server - logos and icons from combined shapes, recolouring to the owner's palette with swatches, text on a path and area type with outlines for hand-off, simple charts, tracing a raster into vectors, SVG/PDF/PNG exports with EPS on request, fixing a client's SVG or PDF, and the native file with its reopen check - each recipe proven on VectorCraft 0.13.1, with the check after every step, undo, and the list of what not to promise. Use for any job done in VectorCraft; it also holds VectorCraft's Connect table for connecting the app and handing over files.
---

# VectorCraft work

VectorCraft is an open-source vector illustration app in alpha: documents of artboards and layers holding paths, live shapes, type, placed images and charts, with swatches and a native lossless file. Every menu action is a command, and its MCP server lets an agent draw, recolour, trace and export headless, with file access fenced to two folders named at start. This skill is the manual for that work: how to connect, how the app thinks, the recipes that were run for real on VectorCraft 0.13.1, how to look at the result, how to undo, and what not to promise.

Status, in one line for the owner: «Alpha: VectorCraft is in alpha; .ai files from other apps may not open as they were made.»

**Route:** connect (with the Connect table below) → agree the deliverables → recipes → look at the result after each step → hand over the files.

## When to use

- A job in VectorCraft: draw a logo, mark or icon, bring artwork onto a palette, set type along a curve, chart a small table, trace a sketch, export a file set.
- A client sends an SVG or PDF that needs fixing.
- The owner asks what VectorCraft can and cannot deliver.

## Inputs

- The read folder `<in>` and the write folder `<out>` the server was started with, as absolute paths.
- The agreed deliverables list.
- The brief: sizes, text, figures, palette (hex values), fonts and source files the owner provides. Never invented brand assets.

## Connect table (VectorCraft)

| Item | Value |
|---|---|
| Programs | `vectorcraft` (desktop app), `vectorcraft-cli` (CLI and MCP server) |
| CLI location | Linux tar.gz: `<unpacked folder>/bin/vectorcraft-cli`, not on the PATH. Linux deb or rpm: `/usr/bin/vectorcraft-cli`. Windows MSI: `C:\Program Files\VectorCraft\vectorcraft-cli.exe`, not on the PATH; use the full path. macOS: the separate release asset `vectorcraft-cli-<version>-macos-universal.zip` (the `.app` holds only the desktop app) |
| Releases | github.com/storytold/vectorcraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | `--automation-read-root <dir>` and `--automation-write-root <dir>`, present in 0.13.1 (older builds not checked: update first). Each flag once; each folder must exist or the server does not start; a limit left out grants no access in that direction; links are followed to where they lead. Reads and writes outside are refused with `automation path rejected: outside the write root <dir>: <path>` (or `outside the read root`), and nothing is written. A relative path counts from the server's working folder and is refused: give absolute paths |
| Headless start | `vectorcraft-cli mcp --headless --automation-read-root <in> --automation-write-root <out>`, always in this form. The bare `vectorcraft-cli mcp` first looks for a running app on 127.0.0.1:7979 and drives it unconfined; only then does it fall back to headless |
| Attach (owner watches) | not offered: not proven on 0.13.1, and the app's control port has no token. Show the owner `render_preview` images instead |
| Token | none; headless needs none |
| Register | `claude mcp add vectorcraft -- vectorcraft-cli mcp --headless --automation-read-root <in> --automation-write-root <out>` (full CLI path when it is not on the PATH) |
| Prove | the server's start message on stderr reads `files confined: read root <in>, write root <out>`; a document «Untitled-1» is already open, so at once: `command_list {filter: "file.new"}`, `doc_inspect {depth: 0}`, `open_file {path: "<in>/<file>"}`, and `save_file {path: "<in>/escape.vectorcraft"}`, which must be refused; then `command_run file.close {}` for the opened file |
| Check commands | facts with `doc_inspect` (children listed front first), `command_run recolor.colors`, `text.missingFonts`, `document.pdfInfo {path}`; eye with `render_preview {max_side: 256}`; reopen an output with `open_file` (read `warnings` and `restored`); files with `vectorcraft-cli info <file>` (read-only, paths inside the folders), `file`, `pdfinfo`, `pdffonts`, `pdftotext`, `pdftoppm` |
| Version | `vectorcraft-cli --version`; also `serverInfo.version` in the MCP initialize reply |

## The model

- A document holds artboards and layers; a layer holds paths, compound paths, live shapes (rectangle, ellipse, polygon, star), groups, type, placed images and charts. Several documents may be open at once; `doc_inspect` reports the active one. Document indices count the open documents from 0 and shift when one closes, and after a close another document becomes active: confirm with `doc_inspect {depth: 0}` (`title`).
- Positions are points, x to the right, y down, counted from the top-left corner of the first artboard. A new document from the server is 612×792 pt unless `file.new` gets a size.
- `doc_inspect` lists children front first: the first child is the one on top.
- A new object becomes the selection; most commands work on `ids` when given, otherwise on the selection.
- Every action is a command: find ids and params with `command_list {filter: "<word>", brief: false}`, run one with `command_run {id, params}`, several with `command_batch {steps: [{id, params}]}` (a tool name such as `draw_shape` works as a step id). The server refuses unknown parameters and names the ones it takes: never guess.

## Rules

Each rule carries the check that shows it was kept.

- **Headless, both limits, absolute paths.** Start only as the Connect table says. Check: the stderr start message names both folders, and the prove step's write into `<in>` was refused.
- **New documents come from `command_run file.new {width, height, name}`**; there is no tool for it. The new one becomes active. Check: before every save or export, `doc_inspect {depth: 0}` shows the expected `title` and `path`; switch with `command_run document.activate {index}`.
- **Pass the paint on every draw** (`fill`, and `stroke` or `stroke: "none"`): left out, the app uses its current new-art paint (white fill, black 1 pt stroke at the start). Check: `doc_inspect` shows the fills and strokes you asked for.
- **A `pathfinder` result takes the paint and stacking place of the front object** (`minusFront` is the exception: it keeps the back shape's). A `unite` of a shape that sat behind with one in front can paint the result in the wrong colour and move it over other art. Check: after each `pathfinder`, `doc_inspect` (order and fill of the new object) and `render_preview`; fix with `set_paint {ids, fill}` and `command_run object.arrange.bringToFront {ids}` (or `sendToBack`).
- **One call at a time; «busy» means wait.** The engine runs one call. A call sent while another has been running for two seconds comes back as JSON-RPC error `-32003` «the engine is busy … this request was not run». Never retry in a loop: wait for the reply of the running call, then send the refused call once. To stop a long export, send `notifications/cancelled {requestId}`; nothing is written. Check: every call has its own reply before the next one goes out.
- **Exports and saves overwrite without asking.** Check before every `export` and every `save_file` to a new path: `ls <out>/<name>` must answer «No such file or directory»; otherwise pick a new name. Make sub-folders first (`mkdir -p <out>/set`).
- **A batch is not rolled back, even with `atomic: true`.** The steps before the failing one stay in the document; `atomic: true` only makes them one undo step under `label`. Check: after a reply with `failed` above 0, `doc_inspect` shows what `created` lists; then one `undo` for an atomic batch, or one `undo` per applied history step without it, until `doc_inspect` matches the state before.
- **Closing drops unsaved edits without asking.** `file.close` and `file.closeAll` never ask to save. Check: `doc_inspect {depth: 0}` shows `dirty: false` right before each close; if not, `save_file` first.
- **A missing font is replaced without a stop.** A PDF or SVG whose font is not on this machine opens and saves in a stand-in font; only a warning line says so. Check: read the `warnings` of every `open_file`, run `command_run text.missingFonts {}` (`count: 0` wanted), and after a PDF save `pdffonts <file>` lists the font you meant. Replace a missing family with `command_run text.replaceFont {from: {family: "<missing>"}, to: {family: "<installed>"}}`. A generic SVG family such as `sans-serif` is never reported: set a real font.
- **Client PDFs: `options: {preserveEditing: false}`.** By default a PDF (and an EPS) from VectorCraft carries a full copy of the native document inside it, hidden content included. Check: reopening the PDF gives `restored: false`. Keep the editable master as `.vectorcraft`.
- **EPS only on request**, with two notes for the owner: RGB colours are written as CMYK unless `options: {cmykPostScript: false}`, and the page is the art's bounds, not the artboard. Check: `grep -a -m1 '%%BoundingBox' <file>` matches the art's bounds from `doc_inspect` (the box counts y up from the bottom: its second value is the artboard height minus the art's lower edge).
- **A source from `<in>` is never saved in place**: `save_file {}` on it is refused. Save under a new name in `<out>`.
- **Swatch groups first.** `swatch.newGroup {name}` before `swatch.new {…, group}`. Names are unique: a taken name gets a number added, and the `swatch.new` reply may spell it differently from the list. Check: `swatch.list {group}` and use the names it returns.
- **Charts:** select the chart (`select.set {ids: [<chart id>]}`) before `graph.setData` or `graph.setType`, re-read part ids after new data (the parts are rebuilt), and paint series by id, never with `recolor.apply` (axes and labels share the series' default black).
- **An SVG's `<title>` is the document title**, which a client file keeps from its old name. Check: `grep '<title>' <file>`; set it with `command_run file.info {title}` before the export.
- **The CLI only for `vectorcraft-cli info <file>` and `vectorcraft-cli commands`**, both read-only, on paths inside the folders. Its `run` and `convert` ignore the folder limits: never use them for deliverables.
- **No window tools headless** (`type_text`, `open_panel`, `ui_inspect`, `ui_screenshot`, `inspect_ui`, and `screenshot` with `window`).

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name. Every `export` and every new `save_file` path follows the rule on overwrites (`ls` first).

### V1. A logo or icon from combined shapes (proven on VectorCraft 0.13.1)

1. `command_run file.new {width: 256, height: 256, name: "<job>"}` → `{index}`.
2. One `draw_shape` per part, each with paint and name, for example `draw_shape {shape: "ellipse", x: 28, y: 28, width: 200, height: 200, fill: "#3C6E71", stroke: "none", name: "disc"}`, `{shape: "ellipse", x: 78, y: 78, width: 100, height: 100, fill: "#000000", stroke: "none", name: "hole"}`, `{shape: "star", cx: 128, cy: 128, radius1: 44, radius2: 20, points: 5, fill: "#E4572E", stroke: "none", name: "star"}`, `{shape: "rectangle", x: 20, y: 118, width: 216, height: 20, fill: "#1B2A41", stroke: "none", name: "band"}`; note each `id`.
3. Combine: `pathfinder {ids: [<disc>, <hole>], operation: "minusFront"}` → `{ids: [<ring>]}`; `pathfinder {ids: [<ring>, <band>], operation: "unite"}` → `{ids: [<mark>]}`. Other operations: `unite`, `intersect`, `exclude`, `minusFront`.
4. Check (rule on `pathfinder`): `doc_inspect` gives each result's kind, bounds and fill, and the order front first; `render_preview {max_side: 128}` and look. Here the united mark takes the band's navy and sits over the star: `set_paint {ids: [<mark>], fill: "#3C6E71"}`, `command_run object.arrange.bringToFront {ids: [<star>]}`, then inspect and look again.
5. `command_run object.group {ids: [<mark>, <star>]}`; `command_run object.align {horizontal: "center", vertical: "center", to: "artboard"}`; `command_run object.setProps {name: "<job>-mark"}`. Check: `doc_inspect {ids: [<group>]}`: the star first, bounds centred on the artboard.
6. `save_file {path: "<out>/<job>.vectorcraft"}`. Exports: V6.

### V2. Recolour to the owner's palette, with swatches (proven on VectorCraft 0.13.1)

1. `command_run swatch.newGroup {name: "<brand>"}`; per colour `command_run swatch.new {name: "<colour>", color: "#RRGGBB", global: true, group: "<brand>"}`. Check: `command_run swatch.list {group: "<brand>"}`: use the names it returns (rule on swatches).
2. `command_run select.all {}`; `command_run recolor.colors {}` lists the colours in use, with counts.
3. `command_run recolor.apply {map: {"#<old>": "#<new>"}, limitTo: "document"}` → `{changed}`. A new colour equal to a swatch is linked to it. To link one object by hand: `command_run paint.setFill {ids: [<id>], swatch: "<name>"}`.
4. Check: `doc_inspect` shows fills as `"<swatch> (#hex)"`; `render_preview {max_side: 128}` and look. A later palette change is one call, `command_run swatch.edit {name, color: "#RRGGBB"}` → `{relinked}`; inspect again: the linked art follows.
5. Palette files for the owner: `command_run swatch.library.save {path: "<out>/<job>-palette.ase", names: ["<brand>"]}` (also `.css` or `.gpl`) → `{count}`. Check: `cat <out>/<job>-palette.css` lists one custom property per colour, named after the swatch (`Sand 2` becomes `--sand-2`).
6. `save_file {}` (the document was saved under `<out>` before).

### V3. Text on a path and area type, outlined for hand-off (proven on VectorCraft 0.13.1)

1. `command_run file.new {width: 400, height: 300, name: "<job>"}`. Fonts this machine has: `command_run text.fontList {}`.
2. Path text: `draw_path {d: "M 60 200 C 120 80 280 80 340 200", fill: "none", stroke: "#3C6E71", name: "arc"}` → `{id}`; `add_text {text: "<line>", path: <id>, mode: "onPath", font: "<family>", size: 20, color: "#1B2A41"}`. The path turns into the type object and loses its stroke.
3. Area type: `add_text {text: "<paragraph>", x: 60, y: 215, width: 280, height: 30, font: "<family>", size: 11, color: "#1B2A41"}`. A reply with `overflow: true` means hidden text: `command_run text.areaOptions {ids: [<id>], fit: "autoHeight"}` → `overflow: false`.
4. Check: `doc_inspect` (two Type objects, `overflow: false`); `render_preview {max_side: 256}` and look.
5. `save_file {path: "<out>/<job>.vectorcraft"}`: the master keeps live type.
6. Hand-off copies with outlined text: `export {path: "<out>/<job>.svg", outlineText: true}`; `export {path: "<out>/<job>.pdf", options: {preserveEditing: false, advanced: {outlineText: true}}}`. Check: `grep -c '<text' <out>/<job>.svg` prints 0; `pdffonts <out>/<job>.pdf` lists no font rows. A live-text PDF instead (receiver has the fonts): leave out `outlineText`; `pdffonts` then shows the font embedded as a subset.
7. Outlines inside the document only on request: `command_run select.all {}`, `command_run type.createOutlines {}`; `undo {}` brings the type back (`undone: "Create Outlines"`).

### V4. A simple chart (proven on VectorCraft 0.13.1)

1. `command_run file.new {width: 480, height: 320, name: "<job>"}`.
2. `create_graph {type: "column", x: 60, y: 40, width: 360, height: 220, csv: "<the CSV text>"}` → `{id}`. Other types: `bar`, `line`, `area`, `pie`. The first row is a corner cell, then the series names; the first column holds the categories.
3. Check: `command_run select.set {ids: [<chart id>]}`; `command_run graph.setData {id: <chart id>}` with no data reads back series, categories and rows; `render_preview {max_side: 256}` and look.
4. Colours by id (rule on charts): `doc_inspect {ids: [<chart id>], depth: 2}` gives one group per series, holding its columns and its legend mark; `set_paint {ids: [<every path id in that series group>], fill: "#RRGGBB"}` for each series.
5. Options and new data: `command_run graph.setType {id, legendAcrossTop: true, axisMin: 0, axisMax: <top>, ticks: 4}`; `command_run graph.setData {id, csv: "<new CSV>"}`. Then `doc_inspect {ids: [<chart id>], depth: 2}` again for the new part ids, and render: series colours stay.
6. `save_file {path: "<out>/<job>.vectorcraft"}` (the chart stays editable after a reopen, once selected). For a PDF (V6), `pdftotext <file> -` shows the labels as text.

### V5. Trace a raster into vectors (proven on VectorCraft 0.13.1)

1. `command_run file.new {width: <image width>, height: <image height>, name: "<job>"}`; `command_run file.place {path: "<in>/<image>", link: false}` → `{ids, width, height}`.
2. `command_run imageTrace.presets {}` lists the presets; `command_run imageTrace.make {preset: "3 Colors", params: {ignoreWhite: true, shapes: true}}` → `{id, paths, colors, warnings}`. For a one-colour mark, `"Black and White Logo"`.
3. `command_run imageTrace.expand {id: <trace id>}`: the trace becomes a group of paths and live shapes.
4. Check: `doc_inspect` gives each part's bounds and fill: compare them with the source's shapes and colours; `render_preview {max_side: 200}` and look side by side with a small copy of the source.
5. Bring it onto the palette (V2), then `save_file {path: "<out>/<job>.vectorcraft"}`.

### V6. Export set: SVG, PDF, PNG at 1x and 2x, EPS on request (proven on VectorCraft 0.13.1)

1. `command_run document.activate {index: <job's index>}`; `doc_inspect {depth: 0}`: `title` and `dirty: false` (else `save_file {}`). `mkdir -p <out>/set` and `ls <out>/set/` (rule on overwrites).
2. `export {path: "<out>/set/<job>.svg"}`; `export {path: "<out>/set/<job>.pdf", options: {preserveEditing: false}}`; `export {path: "<out>/set/<job>@1x.png", scale: 1}`; `export {path: "<out>/set/<job>@2x.png", scale: 2}`. Only on request: `export {path: "<out>/set/<job>.eps", options: {cmykPostScript: false}}` (rule on EPS).
3. Check every reply's `warnings`, then: `file <out>/set/*` (PNG pixel size = artboard × scale); `pdfinfo <out>/set/<job>.pdf` (one page per artboard, page size = artboard in pt); EPS: the `%%BoundingBox` line against the art's bounds, said in the note; `pdftoppm -png -scale-to 128 -singlefile <pdf> <out>/<job>-look` for a small look, removed afterwards.
4. Reopen the SVG and the PDF with `open_file`: the SVG keeps groups, names and fills (`restored: false`, no swatch links); the PDF gives `restored: false` and plain paths. `doc_inspect`, a `render_preview {max_side: 128}`, then `command_run file.close {}` for each copy (nothing was edited).
5. Long exports (large `scale`): send nothing else until the reply comes (rule on «busy»).

### V7. Open a client SVG or PDF and fix it (proven on VectorCraft 0.13.1)

1. PDF first: `command_run document.pdfInfo {path: "<in>/<file>.pdf"}` (pages, boxes, password). Then `open_file {path: "<in>/<file>"}`: read `warnings` (a missing font shows here).
2. `doc_inspect`: look for objects outside the artboard bounds, off-palette fills, hairline strokes, placeholder text; `command_run text.missingFonts {}`.
3. Fix: `command_run edit.clear {ids: [<stray>]}`; `command_run select.all {}` and `command_run recolor.apply {map: {"#<old>": "#<new>"}}`; `set_paint {ids: [<id>], stroke: "none"}`; `command_run text.setText {id, text: "<owner's text>"}`; `command_run text.setStyle {ids: [<id>], font: "<family>", size: <pt>}`; `command_run text.replaceFont {from: {family: "<missing>"}, to: {family: "<installed>"}}`; `command_run file.info {title: "<title>"}`.
4. Check: `doc_inspect` again (strays gone, fills on palette); `text.missingFonts` gives `count: 0`; `render_preview {max_side: 256}` and look.
5. Save under a new name in `<out>` (rule on sources): `save_file {path: "<out>/<job>-fixed.svg"}` or `export {path: "<out>/<job>-fixed.pdf", options: {preserveEditing: false}}`. Check: SVG: `grep '<title>' <file>` and the fills; PDF: `pdffonts` names the intended font, not a stand-in; `pdftotext <file> -` has the text.
6. `command_run file.close {}` once `doc_inspect {depth: 0}` shows `dirty: false`; a client file that was fixed but only exported stays dirty: close it on purpose, the source in `<in>` is untouched.

### V8. Save, reopen, undo, batch and close (proven on VectorCraft 0.13.1)

1. `save_file {path: "<out>/<job>.vectorcraft"}`; later saves of that document: `save_file {}`.
2. Reopen check: `open_file {path: "<out>/<job>.vectorcraft"}` adds a second document with a new `index` (the open one stays). `doc_inspect` on it: artboards, objects, names, fills and swatch links as saved. Close the copy with `command_run file.close {}`.
3. Undo: `undo {}` → `{undone: "<step>"}`; `redo {}` → `{redone: "<step>"}`. Check with `doc_inspect` (`dirty: false` again when back at the saved state).
4. Several edits as one undo step: `command_batch {steps: [{id: "draw_shape", params: {…}}, …], atomic: true, label: "<what>"}`. On a reply with `failed`, follow the rule on batches: `doc_inspect`, then `undo {}` once → `{undone: "<label>"}`.
5. End: for each open document, `doc_inspect {depth: 0}` shows `dirty: false` (else `save_file {}`), then `command_run file.close {}`; or, when every document is saved, `command_run file.closeAll {}` → `{closed}`. Check: `doc_inspect` now answers «no document open».

Not in these recipes (not proven): attach, symbols, brushes, blends, 3D, perspective, effects beyond a blur, plug-ins, scripting, `.ai` and EPS files from other apps, `.psd` input.

## Look at the result

- Numbers first: `doc_inspect` (tree front first, bounds, fills and strokes, swatch links, `overflow`, `dirty`, `history`), `recolor.colors`, `text.missingFonts`, `swatch.list`, `graph.setData {id}` with no data, `document.pdfInfo`.
- Then the eye: `render_preview {max_side}`; 128 to 256 is enough for layout and colour, larger only for detail. Never read a full-size image into the conversation.
- For a written file: `file`, `pdfinfo`, `pdffonts`, `pdftotext`, `pdftoppm -scale-to 128`, `vectorcraft-cli info <file>`, and a reopen with `open_file`.

## Undo

- `undo {}` and `redo {}` step through history and name the step. A `draw_shape` with paint and a name can be up to three steps (shape, paint, name). Check with `doc_inspect`.
- After a failed batch, follow the rule on batches.
- Undo does not remove files already written; a wrong export is replaced under a new name, and the note says which file is current.

## Do not promise

- `.ai` exchange of any kind: `.ai` files from other apps may open with the wrong layers, and `.ai` files written here are not checked in other apps. Deliver SVG and PDF.
- `.psd` input beyond the merged picture; files for other illustration apps (`.afdesign` and the like are never written).
- PDF/X or PDF/A conformance.
- EPS with exact colours or sized to the artboard (see the rule on EPS); EPS files from other apps.
- Fonts that are not on the machine: a stand-in is written.
- The missing raster effects and the effect gallery; 3D beyond a first revolve; vertical CJK type; scripting; generative AI features.
- Watching the work live in the app window: attach is not offered.
- The desktop app starting on every machine.
- Speed on very large rasters or documents: one call runs at a time.
- Closing that asks to save: it does not, so the agent always saves first.

## Checks before hand-over

- Every output was reopened or checked and looked at (deliverable hand-over steps).
- The `.vectorcraft` master sits next to the exports.
- Client PDFs were written with `preserveEditing: false`; EPS only on request, with its two notes.
- `text.missingFonts` gave `count: 0` before the last save, and `pdffonts` shows the intended fonts.
- No export overwrote an earlier file.
- All documents are closed after a save: `file.closeAll` was run only with every `dirty: false`.

## Artefacts

- `<out>/<job>.vectorcraft`, the agreed exports, palette files when asked, `HANDOVER.md`, `SHA256SUMS.txt`.

## Hand-over

- Files stay in `<out>`; the owner sends or publishes them.
- An owner who wants to watch the work live gets `render_preview` images, and the reason attach is not offered.

## Sources

No endorsement by these projects or their authors is implied.

Built on VectorCraft documentation (github.com/storytold/vectorcraft, commit 904f0fe5227bd987d55319e89a38b4b8f046998c; © 2026 ArtCraft Team and the VectorCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
