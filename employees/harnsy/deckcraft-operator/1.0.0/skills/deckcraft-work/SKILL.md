---
name: deckcraft-work
description: Do presentation work in DeckCraft over its MCP server - new decks from a theme or a starter template, title and bullet slides, pictures, tables and charts placed by points, speaker notes, theme, fonts, colours, footer and master layouts, slides from an outline with transitions, PDF/PPTX/image/outline/GIF exports, the native file and its reopen check - each recipe proven on DeckCraft 0.8.0, with the check after every step, undo, and the list of what not to promise. Use for any job done in DeckCraft; it also holds DeckCraft's Connect table for connecting the app and handing over files.
---

# DeckCraft work

DeckCraft is an open-source presentation app in alpha: decks of slides built on a theme and a slide master, with placeholders, pictures, tables, charts, notes and transitions. Every menu action is a command, and its MCP server lets an agent build, restyle and export decks headless, with file access fenced to two folders named at start. This skill is the manual for that work: how to connect, how the app thinks, the recipes that were run for real on DeckCraft 0.8.0, how to look at the result, how to undo, and what not to promise.

Status, in one line for the owner: «Alpha: decks from other presentation apps are not tested yet, and PDF slides are exported as images.»

**Route:** connect (with the Connect table below) → agree the deliverables → recipes → look at the result after each step → hand over the files.

## When to use

- A job in DeckCraft: build a deck, fill it with text, pictures, tables and charts, restyle it, write speaker notes, export it.
- The owner has an outline and wants slides from it.
- The owner asks what DeckCraft can and cannot deliver.

## Inputs

- The read folder `<in>` and the write folder `<out>` the server was started with, as absolute paths.
- The agreed deliverables list.
- The brief: slide titles, text, figures, pictures and brand colours the owner provides. Never invented content in a delivered deck without saying so.

## Connect table (DeckCraft)

| Item | Value |
|---|---|
| Programs | `deckcraft` (desktop app), `deckcraft-cli` (CLI and MCP server) |
| CLI location | Linux tar.gz: `<unpacked folder>/bin/deckcraft-cli`, not on the PATH. Linux deb or rpm: `/usr/bin/deckcraft-cli`. Windows MSI: `deckcraft-cli.exe` in the `DeckCraft` program folder, not on the PATH; use the full path. macOS: the separate release asset `deckcraft-cli-<version>-macos-universal.zip` |
| Releases | github.com/storytold/deckcraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | `--automation-read-root <dir>` and `--automation-write-root <dir>`, present in 0.8.0 (older builds not checked: update first). Each flag once; each folder must exist or the server does not start; a limit left out grants no access in that direction. Reads and writes outside are refused (`automation path rejected: outside the write root <dir>: <path>`, or `outside the read root`). A relative path counts from the server's working folder, so give absolute paths |
| Headless start | `deckcraft-cli mcp --automation-read-root <in> --automation-write-root <out>` |
| Attach (owner watches) | not offered. `deckcraft-cli mcp --connect <port>` refuses the folder limits, the desktop app has no folder limits of its own, and its control port has no token: an attached session could read and write anywhere. Show the owner rendered slides instead |
| Token | none; headless needs none, and the control port has no token at all |
| Register | `claude mcp add deckcraft -- deckcraft-cli mcp --automation-read-root <in> --automation-write-root <out>` (full CLI path when it is not on the PATH) |
| Prove | `new_presentation {}` first (every tool answers «no presentation open» until a deck exists), then `list_commands {filter}`, `inspect_document`, and one write outside `<out>` that must be refused |
| Check commands | reopen with `open_presentation`; facts with `inspect_document` and `inspect_slide {index}`, or `deckcraft-cli info <file>` (read-only, paths inside the folders); eye with `render_slide {slide, scale}` (scale 1 = 960×540 px, 0.25 for a quick look); PDFs with `pdfinfo` and `pdftotext` |
| Version | `deckcraft-cli --version`; the MCP initialize reply also gives it (`serverInfo.version`) |

## The model

- A presentation holds slides; each slide uses a layout of the slide master. The theme is a colour scheme, a font scheme and an effect scheme, with colour variants.
- Positions are points on a 960×540 slide, x to the right, y down; a box is `x, y, w, h` or `rect: [x, y, w, h]`. Slide indices count from 0.
- Shape ids are looked up on the current slide: `go_to_slide {index}` before shape commands on another slide. `add_slide` makes the new slide current. An inserted shape becomes the selection, and `format.*` commands act on the selection.
- Every action is a command: find ids and params with `list_commands {filter}`, run one with `run_command {command, params}`, several in order with `batch {commands}`. Never guess an id or a parameter.

## Rules

- **Headless only, both limits, absolute paths.** Never `--connect` (see the Connect table). Every open, save, export and picture path is absolute, inside `<in>` for reading and `<out>` for writing.
- **Save before close, always.** `file.close` drops unsaved edits without asking. Check: `inspect_document` shows `dirty: false` right before `file.close`; if not, `save_presentation` first.
- **Export overwrites without warning.** Check before every export: `ls <out>/<name>` must answer «No such file or directory»; if the name is taken, pick a new one. Create sub-folders first (`mkdir -p <out>/png`).
- **Ids change when a `.pptx` is reopened.** A native reopen keeps shape ids, a `.pptx` reopen renumbers them. Check: after every `open_presentation`, read the ids again with `inspect_slide` and use only ids from that latest reply.
- **Starter templates carry invented sample text and sample speaker notes.** Replace both. Check: `inspect_document` lists every slide's `title` and `notes`, and none of the sample wording is left; tell the owner what was a placeholder.
- **The `insert_chart` tool has no position**: the chart lands in the middle of the slide, on top of other content. Place charts with `run_command insert.chart {type, rect, categories, series}`, or move one with `run_command shape.setBounds {ids, x, y, w, h}`. Check: `inspect_slide` shows the chart's box where you put it, and `render_slide` shows no overlap.
- **A batch is not a transaction.** `batch` stops at the first failing step (with `keepGoing: true` it runs the rest) and keeps the steps that ran. After a failure, run `inspect_document`, then decide: finish the rest, or `edit.undo` once per applied step, reading each reply's `label`. Check: `inspect_document` matches the state before the batch.
- **After a theme or colour change, render every slide that has a table or chart** and look at the contrast.
- **The footer and slide number reach only the slides that exist** when `design.headerFooter` runs; slides added later (`add_slide`, `slide.fromOutline`) have none. Run it again after adding slides. Check: in `inspect_document`, every slide but the title slide has the same `shapes` count as before plus two.
- **The CLI only for `deckcraft-cli info <file>`**, a read-only check, on paths inside the folders. Its `run`, `convert` and `render` ignore the folder limits; never use them for deliverables.
- **Never `review.addToDictionary`**: it writes the user's dictionary file outside the folders, and it is not an undo step.
- **`missingFonts` in an open reply** means text is drawn with a stand-in font on this machine: say so in the hand-over note.

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name.

### K1. New deck from a theme or a starter template (proven on DeckCraft 0.8.0)

1. Choose: `run_command design.themes {}` lists colour, font and effect schemes; `run_command file.templates {}` lists the starter decks, each with its theme.
2. From a theme: `new_presentation {theme: "<name>"}`: one title slide. From a starter: `run_command file.new {template: "<name>"}`: a deck of sample slides.
3. `inspect_document`: theme, fonts, layouts, and each slide's title and notes. `render_slide {slide: 0, scale: 0.25}` and look.
4. Starter only: for each slide, `go_to_slide {index}`, `inspect_slide {index}` for the text ids, `set_text {id, text}` for each sample text, and `run_command slide.notes {index, text}` for the sample notes. `set_text` keeps the bullet levels of the lines it replaces: look at the render, or `text.get`. Check with `inspect_document` (rule on starter templates).
5. `run_command file.properties {title: "<title>", author: "<author>"}`, then save at once: `save_presentation {path: "<out>/<job>.deckcraft"}`.

### K2. Title and bullet slides (proven on DeckCraft 0.8.0)

1. Title slide: `inspect_slide {index: 0}` gives the placeholder ids (kinds `ctrTitle`, `subTitle`); `set_text {id, text}` for each.
2. `add_slide {layout: "titleAndContent", title: "<title>", body: "<line>\n\t<sub-line>\n<line>"}`: a leading tab puts a line one level down. Other layouts: `title`, `sectionHeader`, `twoContent`, `comparison`, `titleOnly`, `blank`, `contentWithCaption`, `pictureWithCaption`.
3. `inspect_slide {index}`: title and body texts, and the body id (the text shows no tabs). `run_command text.get {id: <body id>}`: `paragraphs[].level` shows the indents.
4. `render_slide {slide: <index>, scale: 0.25}` and look; `save_presentation {}`.

### K3. Picture, table and chart on one slide (proven on DeckCraft 0.8.0)

1. `add_slide {layout: "titleOnly", title: "<title>"}`: the new slide is current.
2. `insert_picture {path: "<in>/<image>", x, y, w, h}`. PNG, JPEG, GIF, BMP, TIFF or WebP; not SVG. The alt text defaults to the file name: set a real one with `run_command shape.altText {ids: [<picture id>], text: "<what it shows>"}`.
3. `insert_table {rows, cols, data: [["<head>", "<head>"], ["<cell>", "<cell>"]], x, y, w, h}`.
4. Chart with a place: `run_command insert.chart {type: "column", rect: [x, y, w, h], categories: ["<a>", "<b>"], series: [{name: "<series>", values: [<n>, <n>]}]}`. It carries the placeholder title «Chart Title»: set the real one with `run_command chart.options {id: <chart id>, title: "<title>"}`.
5. `inspect_slide {index}`: kinds and boxes, alt text, table cells, chart type, title and series. `render_slide {slide: <index>, scale: 0.25}`: nothing overlaps. A chart in the wrong place: `run_command shape.setBounds {ids: [<chart id>], x, y, w, h}` and look again.
6. `save_presentation {}`.

### K4. Speaker notes (proven on DeckCraft 0.8.0)

1. `run_command slide.notes {index, text: "<line>\n<line>"}`, once per slide.
2. `inspect_document`: each slide's `notes` as typed; `save_presentation {}`.
3. After the notes export (K7): `pdftotext <out>/<job>-notes.pdf - | grep '<a phrase>'` finds each slide's notes.

### K5. Theme, fonts, colours, footer and a master layout (proven on DeckCraft 0.8.0)

1. `run_command design.theme {name: "<theme>"}`; `run_command design.fonts {name: "<font scheme>"}`; `run_command design.variants {}`, then `run_command design.variant {index}`; `run_command design.colors {colors: {accent1: "#RRGGBB"}}`. A theme from the owner's file instead: `run_command design.browseTheme {path: "<in>/<file>.pptx"}` (or `.potx`).
2. Footer and slide number: `run_command design.headerFooter {slideNumber: true, footer: true, footerText: "<text>", hideOnTitle: true}`.
3. A new layout: `run_command view.slideMaster {}`; `run_command master.insertLayout {name: "<layout>"}`; `run_command master.insertPlaceholder {kind: "text", rect: [x, y, w, h]}`; `run_command view.closeMaster {}`.
4. `inspect_document`: theme, fonts, the new layout in `layouts`. `inspect_slide {index}` on a content slide: background colour, footer and number shapes added; the title slide has none. Render every slide with a table or chart (rule on theme changes) and look. Table text hard to read on the new colours: `go_to_slide {index}`, then `run_command table.cellFill {id: <table id>, cells: [[1, 0], [1, 1]], color: "#RRGGBB"}` with a fill that suits the text colour, and render again.
5. `save_presentation {}`.

### K6. Slides from an outline, then transitions (proven on DeckCraft 0.8.0)

1. Read the owner's outline file in `<in>` yourself (`cat <in>/<outline>.md`): `#` headings become slides, `-` items become bullets.
2. `go_to_slide {index}`: the new slides go after this one. `run_command slide.fromOutline {text: "<the file's text>", markdown: true}`.
3. `run_command transition.set {kind: "fade", duration: 600}`, then `run_command transition.applyAll {}`.
4. `inspect_document`: the new titles in order, layout Title and Content, `transition` on every slide.
5. If the deck has a footer (K5), run `design.headerFooter` again with the same params (rule on footers) and check the `shapes` counts. `save_presentation {}`.

An outline that should become a deck of its own: `open_presentation {path: "<in>/<outline>.md"}` opens it as a new deck, one slide per heading.

### K7. Exports: PDF, notes and handouts, PPTX, images, outline, GIF (proven on DeckCraft 0.8.0)

Before each export: `ls <out>/<name>` must find nothing (rule on overwrites).
1. Slides PDF: `export {path: "<out>/<job>.pdf"}`. Notes pages: `export {path: "<out>/<job>-notes.pdf", layout: "notes", paper: "a4"}`. Handouts: `export {path: "<out>/<job>-handouts.pdf", layout: "handouts", perPage: 3, paper: "a4"}` (1, 2, 3, 4, 6 or 9 per page; without `paper`, notes and handouts come out on US Letter).
2. `export {path: "<out>/<job>.pptx"}`.
3. Images: `mkdir -p <out>/png` and `ls <out>/png/<job>*.png` (nothing there), then `export {path: "<out>/png/<job>.png", all: true, scale: 1}` writes `<job>1.png`, `<job>2.png` and on, from 1, at 960×540 px times the scale. One slide: `export {path: "<out>/<job>-s<n>.jpg", slide: <n - 1>, scale: 2}`, where `<n>` is the slide number counted from 1.
4. Outline: `export {path: "<out>/<job>-outline.md", format: "outline"}`. It also carries the footer text and a slide-number mark; clean them out of a copy or warn the owner.
5. GIF: `export {path: "<out>/<job>.gif", width: "small", secondsPerSlide: 2}`: one frame per slide, no transitions.
6. Check: `file <out>/<name>` (type, pixel size); `pdfinfo` (pages, page size: 960×540 pt slides, A4 notes); `pdftotext <file> - | head` (the text is there); `ls <out>/png`. The PDFs carry the title and author from `file.properties` in their metadata (`pdfinfo` shows them): set them to what the owner wants seen. Say in the note that PDF slides are pictures under a searchable text layer (200 dpi by default; `dpi` 36 to 600 changes it).

### K8. Save, reopen, check the PPTX, undo and close (proven on DeckCraft 0.8.0)

1. `save_presentation {path: "<out>/<job>.deckcraft"}`. A deck opened by its absolute path saves in place with `save_presentation {}`.
2. Native reopen. Opening a file that is already open adds a second copy next to the first, so close first: `inspect_document` shows `dirty: false`, then `run_command file.close {}`; `inspect_document` answers «no presentation open». Then `open_presentation {path: "<out>/<job>.deckcraft"}`: `damagedMedia` empty; note `missingFonts`. `inspect_document`: slides, titles, notes, theme, transitions and shape ids as saved.
3. PPTX check: `open_presentation {path: "<out>/<job>.pptx"}` (a second document; `inspect_document` now shows it), then `inspect_document` and `inspect_slide {index}` compared with the native: titles, layouts, notes, transitions, boxes (the ids differ: rule on ids). `render_slide {slide: <index>, scale: 0.25}` and look. From the shell: `deckcraft-cli info <out>/<job>.pptx`.
4. Undo: `run_command edit.undo {}` returns the `label` of the step undone; `run_command edit.redo {}` brings it back. Check with `text.get` or `inspect_document`.
5. End: `inspect_document` shows `dirty: false` (else `save_presentation {}`), then `run_command file.close {}`, which closes the active document only. Repeat for each open document until `inspect_document` answers «no presentation open».

Not in these recipes (not proven): animations, audio and video, SmartArt, comments, compare and review.

## Look at the result

- Numbers first: `inspect_document` for the deck (theme, fonts, layouts, slides, notes, transitions, `dirty`), `inspect_slide {index}` for one slide (shapes, boxes, text, table cells, chart series, background), `run_command text.get {id}` for bullet levels.
- Then the eye: `render_slide {slide, scale}`: 0.25 is enough for layout and colour, larger only for detail. Never read a full-size image into the conversation.
- For a written file: `file`, `pdfinfo`, `pdftotext`, `deckcraft-cli info <file>`, and a reopen with `open_presentation`.

## Undo

- `run_command edit.undo {}` steps back one history entry and names it in `label`; `run_command edit.redo {}` steps forward. Check with `inspect_document` or `text.get`.
- After a failed batch, undo once per step that did complete (rule on batches).
- Undo does not remove files already written. A wrong export is replaced under a new name, and the note says which file is current.
- For a fresh start: `run_command file.close {}` without saving discards the edits, then reopen the saved file. Do this only on purpose.

## Do not promise

- Decks from other presentation apps opening faithfully: only decks the project made itself are tested.
- Media playback options and animation rewind surviving a `.pptx` round trip.
- Vector PDF: PDF slides are exported as images, with a text layer on top.
- `.ppt`, `.pps`, `.pot`, `.odp`, `.thmx` or macro decks; `.potx` and `.ppsx` saved as real templates or shows (they hold plain deck content).
- SVG pictures; video export; a GIF with transitions or builds.
- Printing.
- Font faces beyond Regular, Bold and Italic.
- An interface in a language other than English.
- The presenter view on a second display; the full set of animation effects; editing chart data in a grid; the newer chart types.
- Watching the work live in the app window: attach is not offered.
- Speed on big decks: slides render on the CPU.
- AI features of any kind.
- Closing that asks to save: it does not, so the agent always saves first.

## Checks before hand-over

- Every output was reopened or checked and looked at (deliverable hand-over steps).
- The `.deckcraft` file sits next to the exports.
- No sample text or sample notes from a starter are left.
- Every slide with a chart or table was rendered after the last style change.
- The note says that PDF slides are images, and names any `missingFonts`.
- All decks are closed after a save: `inspect_document` answers «no presentation open».

## Artefacts

- `<out>/<job>.deckcraft`, the agreed exports, `HANDOVER.md`, `SHA256SUMS.txt`.

## Hand-over

- Files stay in `<out>`; the owner sends or publishes them.
- An owner who wants to watch the work live gets rendered slides, and the reason attach is not offered.

## Sources

No endorsement by these projects or their authors is implied.

Built on DeckCraft documentation (github.com/storytold/deckcraft, commit 22db9261f9d1a214c296fd390173130c45d76d66; © 2026 ArtCraft Team and the DeckCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
