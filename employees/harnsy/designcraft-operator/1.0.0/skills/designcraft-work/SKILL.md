---
name: designcraft-work
description: Do page layout work in DesignCraft over its MCP server - new documents from a preset with margins, columns and bleed, text stories with paragraph styles threaded by hand and checked for overset and added pages, pictures in frames, parent page items, data merge from CSV, print PDF, EPUB, PNG/JPEG pages, IDML with an open-back check, and the native file - each recipe proven on DesignCraft 0.9.0, with the check after every step, undo, and the list of what not to promise. Use for any job done in DesignCraft; it also holds DesignCraft's Connect table for connecting the app and handing over files.
---

# DesignCraft work

DesignCraft is an open-source page layout app at the pre-alpha stage: documents of spreads and pages, with parent pages, text frames that a story threads through, picture frames, paragraph styles, swatches and data merge. Every menu action is a command, and its MCP server lets an agent build, check and export documents headless, with file access fenced to two folders named at start. This skill is the manual for that work: how to connect, how the app thinks, the recipes that were run for real on DesignCraft 0.9.0, how to look at the result, how to undo, and what not to promise.

Status, in one line for the owner: «Pre-alpha: DesignCraft is not ready for everyday layout work yet; this employee checks every page and says what it could not do.»

**Route:** connect (with the Connect table below) → agree the deliverables → recipes → look at the result after each step → hand over the files.

## When to use

- A job in DesignCraft: lay out a newsletter, a flyer, a booklet or cards; flow the owner's text into styled frames; place pictures; merge records from a spreadsheet; export print PDF, EPUB, page images or IDML.
- The owner asks what DesignCraft can and cannot deliver.

## Inputs

- The read folder `<in>` and the write folder `<out>` the server was started with, as absolute paths.
- The agreed deliverables list, with page size, bleed and the PDF settings the printer asked for.
- The brief: text files, pictures, data files, colours and fonts the owner provides. Never invented content in a delivered document without saying so.

## Connect table (DesignCraft)

| Item | Value |
|---|---|
| Programs | `designcraft` (desktop app), `designcraft-cli` (CLI and MCP server). The agent never starts the desktop app: even `designcraft --help` opens its window and writes settings |
| CLI location | Linux tar.gz: `<unpacked folder>/bin/designcraft-cli`, not on the PATH. Linux deb or rpm: `/usr/bin/designcraft-cli`. Windows MSI: the default install path is `C:\Program Files\DesignCraft\designcraft-cli.exe`, not on the PATH; use the full path. macOS: the separate release asset `designcraft-cli-<version>-macos-universal.zip` (the `.app` holds only the desktop app) |
| Releases | github.com/storytold/designcraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | `--automation-read-root <dir>` and `--automation-write-root <dir>`, proven on 0.9.0 only: an older build, update first. Each flag once; each folder must exist or the server does not start; a limit left out grants no access in that direction. Opened files, placed pictures and data sources are reads; saves, exports, renders with a `path` and packages are writes. Anything outside is refused (`automation path rejected: outside the write root <dir>: <path>`, or `… outside the read root <dir>: <path>`) and nothing is written. A relative path counts from the server's working folder: give absolute paths. The write folder may sit inside the read folder |
| Headless start | `designcraft-cli mcp --automation-read-root <in> --automation-write-root <out>`; stderr says `files confined: read root …, write root …` |
| Attach (owner watches) | not offered. `designcraft-cli mcp --connect <port>` refuses the folder limits, the running desktop app cannot be confined, and its control port has no password. Show the owner rendered pages instead |
| Token | none; headless needs none, and the control port has none at all |
| User settings | the headless server may read the user's preferences file (Linux `~/.config/designcraft/prefs.json`), which sits outside the folders. Its default `smartTextReflow: true` adds pages on its own once a primary text frame exists: rule 1 |
| Register | `claude mcp add designcraft -- designcraft-cli mcp --automation-read-root <in> --automation-write-root <out>` (full CLI path when it is not on the PATH) |
| Prove | the server starts with an empty Letter document, so no «new» first: `inspect_document`, `list_commands {filter: "exportPdf"}`, `open_document {path: "<in>/<file>.designcraft"}`, and one `save_document {path: "<parent of out>/escape.designcraft"}` that must be refused |
| Check commands | facts with `inspect_document` (`pageCount`, pages, items, stories with `overset`, parents, styles) and `get_story {story}`; open documents with `execute document.list`; eye with `render_page {page, scale}` (scale 1 = 72 px per inch; 0.3 for a quick look); `execute links.list`, `execute preflight.run {minPpi}`; reopen with `open_document` (native) or `execute file.openIdml`; files with `file`, `pdfinfo -box`, `pdffonts`, `pdftotext`, `unzip -l`; `designcraft-cli validate-pdf <file>` checks PDF/X-4 markers only. There is no `info` command |
| CLI | only `designcraft-cli commands [filter]`, `describe <command>` and `validate-pdf <file inside the folders>`, all read-only. `run`, `script` and `app` ignore the folder limits: never |
| Version | `designcraft-cli --version`; the MCP initialize reply also gives it (`serverInfo.version`) |

## The model

- A document holds spreads; a spread holds one or two pages (facing pages pair a left and a right page). Each page has a size, margins, columns and a parent page (`A-Parent` by default). Items on a parent show on every page that uses it.
- Items are text frames, graphic frames and shapes. A story is the text; it can thread through several frames. Paragraph and character styles, swatches (CMYK, RGB, spot) and data sources belong to the document.
- Positions are points in **spread** space, x to the right, y down. In a facing spread, x = page width is where the right-hand page begins. A frame rect is `[x0, y0, x1, y1]` (corners, not width and height); `place_image` takes `x, y, width`. Page indices count from 0; `data.preview {record}` counts from 1. Text offsets are UTF-8 bytes.
- Every action is a command: find ids and params with `list_commands {filter}` (or `designcraft-cli describe <id>`), run one with the `execute` tool, several in order with `batch {commands}`. In the recipes, `execute frame.create {…}` stands for `execute {command: "frame.create", params: {…}}`. Never guess an id or a param: unknown params are refused with the list of the right ones.
- Several documents can be open; tools act on the **active** one. `new_document`, `open_document`, `file.openIdml` and `data.merge` each add a document and make it active. `execute document.list` shows them with `index`, `active` and `dirty`; `execute file.activate {index}` switches.

## Rules

- **1. Never turn on the primary text frame or any autoflow.** It is the app's known pre-alpha fault: it adds pages that cannot be removed, and the user's preferences have smart reflow on by default. Always pass `primaryTextFrame: false` to `new_document`; never run `object.primaryTextFrame`; never pass `autoflow` to `file.place` or `text.thread`. Thread overflow by hand (D2). Check after **every** text step (frame with text, place, `set_story_text`, insert, thread, placeholder): the reply's `pagesAdded` is 0 where the reply has it, and `inspect_document` gives the same `pageCount` as before (or the count you added on purpose with `layout.pages.insert`).
- **2. Headless only, both limits, absolute paths.** Never `--connect`. Every open, place, data, save and export path is absolute, inside `<in>` for reading and `<out>` for writing.
- **3. Overset after every text step.** `get_story {story}` → `overset` must be `null` (fits) before you go on; a number is the byte offset where the hidden text starts. Thread one more frame, or say in the note which story stays overset.
- **4. Ids only from the latest reply.** `frame.create` returns `{id, story}`, `place_image` returns `{asset, id}`. `execute object.fit` with a wrong id returns `null`, the same as with a right one. Check: after a fit, `render_page` shows the picture filling the frame; after any `null` reply, check the effect with `inspect_document` or a render.
- **5. Know the active document.** Run `execute document.list` before every save, export, merge or close; switch with `file.activate {index}`.
- **6. Save before close, always.** `execute file.close {index}` drops unsaved edits without asking, and another document becomes active. Check: `document.list` shows `dirty: false` for that index right before the close (else `save_document`), and again after it, to see which document is active now.
- **7. A merged document is unsaved although it reports `dirty: false`.** Check: `document.list` shows its title as «… merged», not a file name; `save_document {path: "<out>/<job>-merged.designcraft"}` at once.
- **8. A batch is not a transaction.** An unknown param name is refused before the first step runs, but a step that fails while running (a swatch name that does not exist, for example) leaves the earlier steps applied. Check: the error reply's `completed` and `failedIndex`; `inspect_document`; then finish the rest, or `execute edit.undo {}` once per completed step, reading each `undone` label.
- **9. Close before reopen.** `open_document` on a file that is already open adds a second copy with the same title. Check: `document.list` shows the file once before you open it.
- **10. Exports overwrite without warning.** Check before every export: `ls <out>/<name>` must answer «No such file or directory»; if the name is taken, pick a new one. Create sub-folders first (`mkdir -p <out>/png`).
- **11. A frame threaded by hand starts with one column.** Check: after `text.thread`, set the columns again with `execute object.textFrameOptions {ids: [<new id>], columns, gutter}`, then `get_story` for overset.
- **12. Alt text before EPUB or tagged PDF:** `execute object.altText {ids, text}` for each picture. Check: the export reply has no «no alt text» warning.
- **13. Never `prefs.set` or `file.savePreset`:** both write the user's settings outside the folders. Never run the desktop binary `designcraft`.
- **14. Never write `.indd`**, and never promise how an `.indd` or `.indt` file will open.
- **15. Paths of this machine travel in two formats.** `.designcraft` and `.idml` files carry the absolute paths of the placed images on this machine; PDF, EPUB and page images do not. Check: `.designcraft`, `.idml` and `.epub` are zip packages, so `unzip -p <file> | grep -a -c '<home folder>'` (a plain grep on the package finds nothing); PDF and images: `grep -a -c '<home folder>' <file>`. Say it in the note.

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name. After every text step, rule 1 and rule 3 apply even where the step does not repeat them.

### D1. New document from a preset: size, margins, columns, bleed (proven on DesignCraft 0.9.0)

1. Sizes: `execute file.presets {}` lists the presets in points (Letter, Legal, Tabloid, A0 to A6, B5, Business Card, Postcard and more).
2. `new_document {preset: "A4", pages: 4, facingPages: true, margins: {top: 42, bottom: 56, inside: 48, outside: 36}, bleed: 9, columns: 2, gutter: 14, intent: "print", title: "<title>", primaryTextFrame: false}` → `{index}`: a new active document.
3. The empty start document is still open: `execute document.list`, then `execute file.close {index: <the start document's index>}` (it holds nothing) and `document.list` again: one document, active.
4. `inspect_document`: `pageCount` 4, page size 595.28×841.89, each page's `margins`, `columns` and `side`, parent `A-Parent` with `items: 0` (no primary text frame). Bleed is not listed: `render_page {page: 0, scale: 0.1, bleed: true}` comes out wider and taller than `render_page {page: 0, scale: 0.1}` by about 2 × bleed × 0.1 px; the PDF boxes in D6 are the final proof.
5. `save_document {path: "<out>/<job>.designcraft"}`.

### D2. Text story with paragraph styles, threaded by hand (proven on DesignCraft 0.9.0)

1. Styles: `execute style.paragraph.create {name: "Body", basedOn: "[Basic Paragraph]", para: {spaceAfter: 6}, chars: {fontFamily: "Source Serif 4", size: 10.5, leading: {kind: "points", value: 14}}}`, and a heading style `execute style.paragraph.create {name: "Head", nextStyle: "Body", chars: {fontFamily: "Source Sans 3", fontStyle: "Bold", size: 26, leading: {kind: "points", value: 30}}}`. Check: `execute style.list {}` names both.
2. Frames on the first page (inside its margins): `execute frame.create {rect: [48, 42, 559.28, 140], content: "text", text: "<heading>"}` → `{id, story}`; the body frame `execute frame.create {rect: [48, 150, 559.28, 785.89], content: "text"}` → `{id, story}`. Check `pageCount` (rule 1).
3. Text: `execute file.place {path: "<in>/<text>.txt", frame: <body id>}`, with no `autoflow` → `{overset, pagesAdded: 0, story}`. Short text instead: `set_story_text {story, text}` (`\n` starts a paragraph). Check `pageCount`.
4. Columns: `execute object.textFrameOptions {ids: [<body id>], columns: 2, gutter: 14}` → `{changed: 1}`.
5. Styles on text: `execute text.select {story: <body story>, anchor: 0, focus: <length from get_story>}`, `execute style.paragraph.apply {name: "Body"}`; the same for the heading story with `"Head"`; then `execute text.exitToFrame {}`.
6. Check: `get_story {story}` → `length`, `lines`, `overset` (a number while text is hidden); `inspect_document` → `pageCount` unchanged.
7. Overflow, by hand: `execute text.thread {from: <last frame id>, rect: [36, 42, 547.28, 785.89], spread: 1}` → `{to, overset, pagesAdded: 0}` (the left page of the second spread). Set the new frame's columns (rule 11). Repeat on the next page until `get_story` shows `overset: null`. Out of pages: `execute layout.pages.insert {count, after}` first, then thread; check `pageCount` against the count you asked for.
8. Look: `render_page {page, scale: 0.3}` for each page with text; `save_document {}`.

### D3. Pictures into frames (proven on DesignCraft 0.9.0)

1. `execute frame.create {spread: <n>, rect: [x0, y0, x1, y1], content: "graphic"}` → `{id}`.
2. `place_image {path: "<in>/<image>", frame: <id>}` → `{asset, id}`. A wrong frame id is refused (`no such item`). Then `execute object.fit {mode: "fillProportionally", ids: [<id>]}` (or `fitProportionally`, `fitContentToFrame`, `centerContent`, `fitFrameToContent`); it answers `null` whatever the id (rule 4).
3. A picture in a new frame instead: `place_image {path: "<in>/<image>", spread: <n>, x, y, width}`: the height follows the picture.
4. Alt text now (rule 12): `execute object.altText {ids: [<id>], text: "<what it shows>"}` → `{changed: 1}`.
5. Check: `execute links.list {}` → each picture `status: ok`, its page and effective `ppi`; `execute preflight.run {minPpi: 150}` → `errors: 0`, `warnings: 0`; `render_page {page, scale: 0.3}`: the crop and the fill look right. `save_document {}`.

### D4. Parent page items: running text, a rule, a colour (proven on DesignCraft 0.9.0)

1. Running text on the parent: `execute frame.create {spread: {kind: "parent", index: 0}, rect: [36, 800, 300, 824], content: "text", text: "<running text>"}`; in a facing parent, x = page width is where the right-hand page begins (for A4, `rect: [890.55, 800, 1154.56, 824]`). Check `pageCount` (rule 1).
2. A rule across both pages: `execute frame.create {spread: {kind: "parent", index: 0}, rect: [36, 30, 1154.56, 34], content: "graphic"}`, `execute swatch.create {name: "<colour name>", color: {c, m, y, k}}`, `execute object.fill {swatch: "<colour name>", ids: [<rule id>]}` → `{changed: 1}`.
3. A page without the parent (a cover): `execute layout.pages.applyParent {pages: [0], parent: null}`; it answers `null`, so check in step 5.
4. One parent item changed on one page: `execute layout.overrideParentItems {page: <index>, ids: [<parent item id>]}` → `{ids}` of that page's own copies; edit those copies only.
5. Check: `inspect_document` → `parents[].items` counts the parent items, each page's `parent` (the cover's is empty); `render_page {page, scale: 0.3}` on the cover and on a page with the parent: furniture absent and present. `save_document {}`.

Page numbers: no command in 0.9.0 inserts an automatic page number (do not promise).

### D5. Data merge from CSV: cards, labels, letters (proven on DesignCraft 0.9.0)

1. Template: `new_document {preset: "Business Card", pages: 1, facingPages: false, margins: 12, bleed: 9, primaryTextFrame: false, title: "<title>"}`.
2. `execute data.source.select {path: "<in>/<data>.csv"}` → `{fields, records, warnings: []}` (TSV and `.xlsx` too).
3. Frames: `execute frame.create {rect: [12, 12, 170, 132], content: "text", text: ""}` → `{id, story}`; a graphic frame for a picture field, `execute frame.create {rect: [180, 12, 240, 72], content: "graphic"}`.
4. Fields: `execute data.placeholder.add {field: "<name>", story, at: 0}`; text between fields: `execute text.select {story, anchor: <end>, focus: <end>}`, `execute text.insert {text: "\n"}`, then the next `data.placeholder.add {field, story, at: <byte offset>}` (take offsets from `get_story`). Picture field: `execute data.placeholder.add {field: "<photo>", role: "image", item: <graphic frame id>}`; the file names in that column are read next to the CSV, inside `<in>`. Check `pageCount` after each text step (rule 1).
5. Check: `get_story` shows `<<name>>` and the other fields; `execute data.fields {}` → each `uses: 1`; `execute data.preview {record: 1}` and `render_page {page: 0, scale: 1}` (a card is small); `execute data.preview.stop {}`.
6. `save_document {path: "<out>/<job>-template.designcraft"}`, then `execute data.merge {fitting: "fillProportionally"}` → `{records, pages, missingImages: [], oversetStories: 0}`: a new active document.
7. Check: `execute document.list` (rule 7); `inspect_document` → `pageCount` equals the record count; `render_page {page, scale: 0.6}` for each page; `save_document {path: "<out>/<job>-merged.designcraft"}` at once.

### D6. Exports: print PDF with bleed and marks, EPUB, page images (proven on DesignCraft 0.9.0)

Before each export: `execute document.list` (the right document is active; rule 5) and `ls <out>/<name>` (the name is free; rule 10).
1. Print PDF: `execute file.exportPdf {path: "<out>/<job>-print.pdf", bleed: true, marks: true, title: "<title>", author: "<author>"}` → `{pages, warnings: []}`. Check: `pdfinfo -box <file>`: TrimBox is the page size, BleedBox is the trim plus the bleed on each side, MediaBox is larger for the marks; title and author are set. `pdffonts <file>`: every font `emb yes`. `pdftotext -f 1 -l 1 <file> - | head`: the text is live.
2. PDF/X-4, only when the owner or the printer asks for it: `execute file.exportPdf {path: "<out>/<job>-x4.pdf", bleed: true, marks: true, standard: "x4"}`. Check: `designcraft-cli validate-pdf <out>/<job>-x4.pdf` → `"valid": true`; `pdfinfo` → PDF version 1.6. The hand-over note says exactly: «marked PDF/X-4; passed DesignCraft's own check; no independent check run». Nothing more.
3. EPUB, after alt text (rule 12): `execute file.exportEpub {path: "<out>/<job>.epub", title: "<title>", author: "<author>", language: "en"}` → `warnings: []`. Check: `unzip -l <file>` (`mimetype`, `OEBPS/content.opf`, `OEBPS/nav.xhtml`, `OEBPS/content.xhtml`, the images); `unzip -p <file> OEBPS/content.xhtml | grep -c 'alt="'` above 0; `unzip -p <file> OEBPS/nav.xhtml` shows the contents list, one entry per story, a parent item a page overrode included: tell the owner.
4. Page images: `mkdir -p <out>/png`, then `export_png {path: "<out>/png/<job>-p<n>.png", page: <n - 1>, scale: 2}` → `{width, height}` (scale 1 = 72 ppi; a path ending in `.jpg` gives JPEG). Check: `file <out>/png/*`.

### D7. IDML for other layout apps, with an open-back check (proven on DesignCraft 0.9.0)

1. `save_document {}` on the native, then `ls <out>/<job>.idml` (free) and `execute file.exportIdml {path: "<out>/<job>.idml"}` → `{bytes}`. Keep the native `inspect_document` reply to compare.
2. `execute file.openIdml {path: "<out>/<job>.idml"}` → `{index, warnings: []}`: a new active document.
3. Compare its `inspect_document` with the native one: `pageCount`, page size, `parents` and their item counts, each page's parent, paragraph styles, item kinds and bounds, story lengths and `overset`, swatches, margins, columns. The ids differ: renumbered on open (rule 4). `execute links.list {}` → pictures ok. `render_page` the same pages at the same scale: they look the same.
4. `execute document.list`, then `execute file.close {index: <the IDML copy>}` (nothing to save) and `document.list` again (rule 6).
5. Tell the owner: the package holds the pictures and also names this machine's image paths (rule 15); other layout apps were not tested on it.

### D8. Undo, reopen and close (proven on DesignCraft 0.9.0)

1. Undo: `execute edit.undo {}` → `{undone: "<label>"}`; `execute edit.redo {}` → `{redone: "<label>"}`; `execute document.history {}` lists the step labels (the history survives a save). Check with `inspect_document` or `get_story`.
2. After a failed batch: rule 8.
3. Native reopen (rule 9): `execute document.list` → the file is open and `dirty: false` (else `save_document {}`); `execute file.close {index}`; `document.list` (the file is gone); `open_document {path: "<out>/<job>.designcraft"}` → `{index}`. `inspect_document`: the same pages, stories, ids, parents and styles as before the close; `render_page {page, scale: 0.3}` and look.
4. End: for every open document, `document.list` shows `dirty: false` (else save), then `file.close {index}`, until `document.list` is empty.

Not in these recipes (not proven): tables, books, contents and index, footnotes, interactive PDF, `.pptx` export, the package folder, printing.

## Look at the result

- Numbers first: `inspect_document` (pages, spreads, items with bounds, stories with `overset`, parents, styles, swatches), `get_story {story}` (overset offset, lines, frames), `execute document.list` (active, dirty), `execute links.list` (picture status, ppi), `execute preflight.run`.
- Then the eye: `render_page {page, scale}`: 0.3 is enough for layout (about 180×250 px for A4); `scale: 1` only for a small page or a crop such as a card. `bleed: true` shows the bleed area. Never read a full-size image into the conversation.
- For a written file: `file`, `pdfinfo -box`, `pdffonts`, `pdftotext`, `unzip -l` and `unzip -p` for EPUB and IDML, `designcraft-cli validate-pdf` for a PDF/X-4 export, and a reopen.

## Undo

- `execute edit.undo {}` steps back one history entry and names it in `undone`; `execute edit.redo {}` steps forward. Check with `inspect_document` or `get_story`.
- After a failed batch, undo once per completed step (rule 8).
- Undo does not remove files already written. A wrong export is replaced under a new name, and the note says which file is current.
- For a fresh start: `execute file.close {index}` without saving discards the edits; then reopen the saved file. Do this only on purpose.

## Do not promise

- Everyday production layout: the app is pre-alpha; every page is checked and the gaps are named.
- Long text that flows on and adds pages by itself: the operator threads frames by hand (rule 1).
- Automatic page numbers: no command for them in 0.9.0.
- `.indd` or `.indt` files opening as they were made; writing `.indd` at all.
- IDML to or from other layout apps keeping every frame, font and line break: not measured on real files; an opened file may reflow.
- PDF/X-4 conformance beyond the hand-over line in D6; PDF/A-2b; PDF/X-1a, PDF/X-3 and named PDF presets.
- The owner's installed fonts always found: some are missed, and the text falls back to a default font.
- Hyphenation beyond English, Spanish, Portuguese, Norwegian and Greek; spelling beyond English.
- Fixed-layout EPUB with live text (its pages are images); HTML beyond one page.
- EPS artwork beyond its preview; PSD layers.
- Printing to a printer, PostScript.
- Books with a shared contents list or index.
- Speed on large documents.
- Scripts or plug-ins written for other layout apps; AI features.
- Watching the work live in the app window: attach is not offered.
- Closing that asks to save: it does not, so the agent always saves first.

## Checks before hand-over

- Every output was reopened or checked and looked at (deliverable hand-over steps).
- The `.designcraft` file sits next to the exports.
- `pageCount` is the agreed count, and every story shows `overset: null` (or the note names the one that does not).
- The note carries the rule 15 line on machine paths, and the D6 PDF/X-4 line if that file was made.
- All documents are closed after a save: `execute document.list` is empty.

## Artefacts

- `<out>/<job>.designcraft`, the agreed exports, `HANDOVER.md`, `SHA256SUMS.txt`.

## Hand-over

- Files stay in `<out>`; the owner sends or publishes them.
- For files that leave this machine, prefer PDF or EPUB; send `.designcraft` or `.idml` with the rule 15 line.
- An owner who wants to watch the work live gets rendered pages, and the reason attach is not offered.

## Sources

No endorsement by these projects or their authors is implied.

Built on DesignCraft documentation (github.com/storytold/designcraft, commit 7cb8b12507def48fb9346e5004340b5e8e4cfcb7; © 2026 ArtCraft Team and the DesignCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
