---
name: photocraft-work
description: Do image work in PhotoCraft over its MCP server - crop and resize, tone and colour on adjustment layers, spot retouching, layered composites with masks and text, PNG/JPEG/WebP exports, the native file and PSD out, folder batches and layers to files - each recipe proven on PhotoCraft 0.10.0, with the check after every step, undo, and the list of what not to promise. Use for any job done in PhotoCraft; it also holds PhotoCraft's Connect table for connecting the app and handing over files.
---

# PhotoCraft work

PhotoCraft is an open-source raster image editor in alpha. Everything it does is a command in one registry, and its MCP server lets an agent run those commands headless: no window, files only inside two folders named at start. This skill is the manual for that work: how to connect, how the app thinks, the recipes that were run for real on PhotoCraft 0.10.0, how to look at the result, how to undo, and what not to promise.

**Route:** connect (with the Connect table below) → agree the deliverables → recipes → look at the result after each step → hand over the files.

## When to use

- A job in PhotoCraft: correct, retouch, resize, composite, convert or export images.
- The owner wants a folder of images processed the same way.
- The owner asks what PhotoCraft can and cannot deliver.

## Inputs

- The read folder `<in>` and the write folder `<out>` the server was started with, as absolute paths.
- The agreed deliverables list.
- The source images. Never a file outside `<in>`.

## Connect table (PhotoCraft)

| Item | Value |
|---|---|
| Programs | `photocraft` (desktop app), `photocraft-cli` (CLI and MCP server) |
| CLI location | Linux deb or rpm: `/usr/bin/photocraft-cli`; Linux tar.gz: `<unpacked folder>/bin/photocraft-cli`, not on the PATH. Windows MSI: `C:\Program Files\PhotoCraft\photocraft-cli.exe`, not on the PATH. macOS: the separate release asset `photocraft-cli-<version>-macos-<arch>.zip`; the app bundle holds only the desktop app |
| Releases | github.com/storytold/photocraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | `--automation-read-root <dir> --automation-write-root <dir>`, present since 0.9.0 (checked on 0.10.0); without a limit that direction of file access is denied |
| Headless start | `photocraft-cli mcp --automation-read-root <in> --automation-write-root <out>` |
| Attach (owner watches) | the owner starts `photocraft --control <port> --control-token-file <private file> --automation-read-root <in> --automation-write-root <out>`; the server is `photocraft-cli mcp --bridge 127.0.0.1:<port> --control-token-file <private file>` |
| Token | required for attach; a private file, never the `--control-token` value on a command line |
| Register | `claude mcp add photocraft -- photocraft-cli mcp --automation-read-root <in> --automation-write-root <out>` |
| Prove | `command_list {filter}` and `doc_inspect` |
| Check commands | reopen with `doc_open`; facts with `photocraft-cli info <file> --compact`; eye with `render_preview {max_side}` (default 1024, at most 2048) |
| Version | `photocraft-cli --version` |

## The model

- A session holds open documents; one is active. `session_list` shows them, `doc_select` switches.
- A document is a layer tree (pixel, adjustment, fill, type, smart object, groups) with masks, effects and a history.
- Every edit is a registry command with JSON parameters: `command_run` runs one, `command_batch` runs several in order. Find ids with `command_list {filter}` and read their `params` before use; never guess an id.

## Rules

- **Absolute paths for every open, save and export**, inside `<in>` for reading and `<out>` for writing. A document opened by a path relative to the read folder cannot be saved in place: the save resolves the same relative path under the write folder and fails.
- **Create sub-folders first** (`mkdir -p <out>/<sub>`): an export does not create missing folders.
- **A batch is not a transaction.** `command_batch` stops at the first failing step (with `stop_on_error: false` it runs the rest) and keeps the steps that ran. After a failure, run `doc_inspect`, then decide: finish the rest, or undo step by step.
- **Selections get used up.** `layer.layerMask.revealSelection` turns the selection into the mask and leaves none, so a `select.deselect` right after it fails and stops the batch. Do not add it there.
- **No folder batch over MCP** (`file.automate.batch` is refused there). Loop over the files one by one, or use `photocraft-cli batch` from the shell. The CLI does not apply the folder limits: keep its `--in`, `--out` and action file inside `<in>` and `<out>` yourself.
- **Headless only.** The `ui_*` and pointer tools need attach mode; do not use them headless. Brush strokes that need a pointer are not done headless.
- **Work non-destructively** where a command allows it: adjustment layers, a duplicated layer, `output: "new"` for fills. For risky experiments make a copy first with `image.duplicate {}`.
- **Exports flatten.** PNG, JPEG and WebP get a flattened image; the reply's warnings say so. The layered result lives in the native `.pcraft`.

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name.

### R1. Crop and resize to a target size (proven on PhotoCraft 0.10.0)

1. `doc_open {path: "<in>/<file>"}`; note `width` and `height`.
2. `command_run image.crop {x, y, width, height}`.
3. `command_run image.imageSize {width, height, resample: "bicubic"}`. Giving only `width` keeps the aspect ratio.
4. `doc_inspect`: the size matches the target; the history ends with «Crop», «Image Size».
5. `render_preview {max_side: 512}` and look.
6. `doc_export {path: "<out>/<job>-crop.png"}`.

### R2. Tone and colour on adjustment layers (proven on PhotoCraft 0.10.0)

1. `doc_open {path: "<in>/<file>"}`.
2. `command_batch` with the adjustments the job needs, for example:
   `layer.newAdjustmentLayer.levels {inBlack: 10, gamma: 1.1, inWhite: 245}`,
   `layer.newAdjustmentLayer.curves {points: [[0,0],[64,54],[192,205],[255,255]]}`,
   `layer.newAdjustmentLayer.hueSaturation {saturation: 15}`,
   `layer.newAdjustmentLayer.vibrance {vibrance: 20}`.
3. `doc_inspect`: one layer of kind Adjustment per step above the Background, which is unchanged.
4. Before and after: `command_run layer.setProps {layer: <id>, visible: false}` on an adjustment layer, `render_preview {max_side: 512}`, then `visible: true` again and preview once more.
5. Save the native file (R6) so the adjustments stay editable; export the agreed formats (R5).

### R3. Spot retouch and sharpen (proven on PhotoCraft 0.10.0)

1. `doc_open {path: "<in>/<file>"}`; find the spots on a `render_preview` and note their pixel centres.
2. `command_run layer.duplicate {}`: the retouch goes on a copy of the layer, the original stays below.
3. Small spots: `command_run paint.spotHealing {points: [[x, y]], size: <brush px>}`, one point per spot, the size a little larger than the spot.
4. A larger object: `command_run select.rect {x, y, width, height}` covering the whole object with a small margin (a selection inside the object leaves a blot), then `command_run edit.contentAwareFill {output: "new"}` (the fill lands on a new layer), then `command_run select.deselect {}`.
5. Sharpen the retouched copy last: `command_run layer.select {layer: <id from step 2>}`, then `command_run filter.sharpen.smartSharpen {amount: 80, radius: 1}`.
6. `doc_inspect`: the new layers and the history; `render_preview {max_side: 512}` and look at each spot.
Retouching that needs freehand strokes (healing brush, clone stamp along a path) is not done headless: say so and offer attach mode with the owner watching.

### R4. Layered composite with mask, effects and text (proven on PhotoCraft 0.10.0)

1. `doc_new {width, height, background: "#f0f0f0", name: "<job>"}`.
2. `command_batch`:
   `layer.new.layer {name: "Card"}`, `select.rect {...}`, `edit.fill {contents: "color", color: "#2255cc"}`, `select.deselect {}`,
   `layer.layerStyle.dropShadow {color: "#000000", opacity: 60, distance: 8, size: 16}`,
   `layer.new.layer {name: "Overlay"}`, `select.all {}`, `edit.fill {contents: "color", color: "#ff8800"}`,
   `select.rect {...}`, `layer.layerMask.revealSelection {}` (no deselect after it),
   `layer.setProps {blend: "Screen", opacity: 0.7}`,
   `type.create {x, y, text: "<title>", name: "Title", size: 48, color: "#ffffff"}`,
   `layer.layerStyle.stroke {size: 2, position: "outside", color: "#000000"}`.
3. `doc_inspect`: four layers; Overlay has `hasMask: true`, blend Screen, opacity 0.7; Card and Title carry their effects; Title is kind Type.
4. `render_preview {max_side: 512}` and look.
5. Save the native file (R6) before any flattened export.

### R5. Exports: PNG, JPEG, WebP, and a copy without metadata (proven on PhotoCraft 0.10.0)

1. PNG: `doc_export {path: "<out>/<job>.png"}`.
2. JPEG: `doc_export {path: "<out>/<job>.jpg", quality: 85}` (quality 1 to 100).
3. WebP lossy: `doc_export {path: "<out>/<job>.webp", quality: 80}`; WebP lossless: the same without `quality`.
4. Check each: `file <out>/<name>` (type and size) and `photocraft-cli info <out>/<name> --compact` (width, height, mode).
5. Metadata: PhotoCraft 0.10.0 copies the source's Exif, location included, into PNG, JPEG and WebP exports; `file.fileInfo {}` shows the camera but not the location, the Export Preferences metadata setting does not change `doc_export`, and Export As presets are refused over MCP. When a source photo carries metadata and the owner did not approve it, export from a clean copy:
   `command_batch` `select.all {}`, `edit.copyMerged {}`; then `doc_new {width, height, name: "<job>-clean"}`; then `command_batch` `edit.pasteSpecial.pasteInPlace {}`, `layer.flattenImage {}`; then export as above and check the file again for metadata.

### R6. Native file, save in place, and PSD out (proven on PhotoCraft 0.10.0)

1. `doc_save {path: "<out>/<job>.pcraft"}`: lossless; keeps layers, masks, effects and editable type.
2. To edit later: `doc_open {path: "<out>/<job>.pcraft"}` with the absolute path, edit, then `doc_save {}` writes it back in place.
3. PSD when asked: `doc_export {path: "<out>/<job>.psd"}`. Reopen it with `doc_open` and compare `doc_inspect` with the native document: layer count, names, masks, blend modes, type layers.
4. Deliver every PSD with this line, because the export itself gives no warning: «PhotoCraft is in alpha: PSD files it writes may not open correctly in other editors yet. The .pcraft file is the reference.»

### R7. The same steps over a folder (proven on PhotoCraft 0.10.0)

Over MCP, one file at a time:
1. `mkdir -p <out>/batch`.
2. For each file: `doc_open {path: "<in>/batch/<name>"}`, `command_run image.imageSize {width: 320}`, `doc_export {path: "<out>/batch/<stem>.webp", quality: 80}`, `doc_close {}`.

From the shell, one command:
1. Write the steps as JSON pairs into `<out>/resize.json`, for example `[["image.imageSize", {"width": 256}]]`.
2. `photocraft-cli batch --actions <out>/resize.json --in <in>/batch --out <out>/batch-cli --format jpg --quality 80`. It refuses `--out` equal to `--in` unless `--in-place` is given; never use `--in-place` unasked.

Check: the number of files in equals the number out, and `file` on every output shows the size expected.

### R8. Layers to separate files (proven on PhotoCraft 0.10.0)

1. Open the layered document (native or PSD), absolute path.
2. `doc_export_layers {dir: "<out>/layers", format: "png"}`: the tool creates the folder, and refuses to overwrite a file that is already there.
3. Check the reply's `count` and file list. Square brackets and other special characters in layer names become «_» in the file names; tell the owner which file is which layer.

## Look at the result

- Numbers first: `doc_inspect` after every step (size, layers, kinds, masks, effects, history).
- Then the eye: `render_preview {max_side}`: 256 to 512 is enough to check layout and colour, 1024 (the default) for detail, 2048 at most. Never read a full-size image into the conversation.
- For a written file: `photocraft-cli info <file> --compact` and `file <file>`.

## Undo

- `command_run edit.undo {}` steps back one history entry; `edit.redo {}` forward. Check with `doc_inspect` (`history`, `canUndo`, `canRedo`).
- After a failed batch, undo once per step that did complete, checking the history as you go.
- Undo does not remove files already written. A wrong export is replaced under a new name, and the note says which file is current.
- For a fresh start: `doc_close {}` without saving and reopen the source.

## Do not promise

- PSD files that other editors accept: PSD files it writes may not open correctly in other editors yet.
- Speed on very large or many-layer documents.
- AI or generative features of any kind.
- Third-party plug-ins.
- AVIF reading, JPEG XL, multi-page PDF writing, PDF reading, export to other editors' native formats.
- More than the first frame of a GIF when opened.
- Right-to-left and complex-script type.
- Freehand brush work headless.

## Checks before hand-over

- Every output was reopened or inspected and looked at (deliverable hand-over steps).
- The `.pcraft` file sits next to the exports.
- Every PSD carries the line from R6.
- Metadata of every photo was checked (R5).
- All documents are closed: `session_list` shows none.

## Artefacts

- `<out>/<job>.pcraft`, the agreed exports, `HANDOVER.md`, `SHA256SUMS.txt`.

## Hand-over

- Files stay in `<out>`; the owner sends or publishes them.
- Work that needs freehand strokes or the owner's eye on a live window goes back to the owner with an offer to attach.

## Sources

No endorsement by these projects or their authors is implied.

Built on PhotoCraft documentation (github.com/storytold/photocraft, commit 8407d9ccb125af52944fca9d228383459f94aaef; © 2026 ArtCraft Team and the PhotoCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
