---
name: wordcraft-work
description: Do document work in WordCraft over its MCP server - new documents with house styles, a table of contents, styled tables, page breaks with headers and page-number footers, find and replace, tracked changes and comments with a clean copy, DOCX/PDF/ODT/Markdown/HTML exports - each recipe proven on WordCraft 0.8.0, with the check after every step, undo, and the list of what not to promise. Use for any job done in WordCraft; it also holds WordCraft's Connect table for connecting the app and handing over files.
---

# WordCraft work

WordCraft is an open-source word processor in alpha. Every action in it is a command in one registry, and its MCP server lets an agent write, format and review documents headless: no window, files only inside two folders named at start. This skill is the manual for that work: how to connect, how the app thinks, the recipes that were run for real on WordCraft 0.8.0, how to look at the result, how to undo, and what not to promise.

**Status to give the owner:** «Alpha: .docx files from other apps are not yet tested at scale, so layout may shift.»

**Route:** connect (with the Connect table below) → agree the deliverables → recipes → look at the result after each step → hand over the files.

## When to use

- A job in WordCraft: write a document, apply house styles, add contents, tables, headers and page numbers, review with tracked changes, export.
- The owner wants a `.docx` checked, edited or turned into PDF, ODT or Markdown.
- The owner asks what WordCraft can and cannot deliver.

## Inputs

- The read folder `<in>` and the write folder `<out>` the server was started with, as absolute paths.
- The agreed deliverables list, with the paper size (A4 or Letter).
- The text and the house style the owner provides. Never invented facts in a document meant for real use.
- Your own name for the `--author` flag, so that tracked changes and comments show an agent made them.

## Connect table (WordCraft)

| Item | Value |
|---|---|
| Programs | `wordcraft` (desktop app), `wordcraft-cli` (CLI and MCP server) |
| CLI location | Linux tar.gz: `<unpacked folder>/bin/wordcraft-cli`, not on the PATH; there is no separate Linux CLI asset. Linux deb or rpm: `/usr/bin/wordcraft-cli` (from the package docs; check after install). Windows MSI: the program folder of the installer; use the full path. macOS: the separate release asset `wordcraft-cli-<version>-macos-universal.zip` |
| Releases | github.com/storytold/wordcraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | `--automation-read-root <dir> --automation-write-root <dir>`, proven on 0.8.0. Each folder must exist or the server does not start (`cannot open the automation write root`). A limit left out grants none of that access. Refusals read `automation path rejected: outside the write root <dir>: <path>` (or `outside the read root`), and nothing is written. If `wordcraft-cli --help` shows no `--automation-read-root` in its `mcp` line, stop and ask the owner to update |
| Headless start | `wordcraft-cli mcp --author "<your name> (agent)" --automation-read-root <in> --automation-write-root <out>`, for example `--author "Odrena (agent)"` |
| Attach (owner watches) | not used. `wordcraft-cli mcp --connect` refuses the folder limits (`a running app is not confined by them`), and the desktop app has no folder limits of its own, so an attached session could read and write anywhere. WordCraft work is headless only |
| Token | none headless. Nothing to store or pass |
| Register | `claude mcp add wordcraft -- wordcraft-cli mcp --author "<your name> (agent)" --automation-read-root <in> --automation-write-root <out>` (full CLI path where it is not on the PATH) |
| Prove | `list_commands {query}` and `inspect_document {}`; `open_document` on one file in `<in>`; one `save_document` into the parent of `<out>`, which must be refused |
| Check commands | numbers with `inspect_document {}` and `execute file.info {}`; text with `get_text {}`; eye with `render_page {page, scale}`; for a written file `wordcraft-cli info <file>`, `wordcraft-cli text <file>`, `wordcraft-cli inspect <file>` (documents only, not PDF); PDF pages with `file <file>`; reopen with `open_document` only after the current document is saved (rule below) |
| Version | `wordcraft-cli --version` |

## The model

- **One document per session.** `new_document {template}` (blank, sample, letter, resume, report) or `open_document {path}` replaces the one that is open. `execute file.close {}` does nothing headless: the document stays until the next open or the end of the session.
- A document is a list of blocks (paragraphs and tables) in stories: the body, each header, each footer, the comments. A position is `{story: "body", path: [block, (row, cell, block)…], off: <byte offset>}`.
- A caret and a selection drive every edit. `type_text` writes at the caret (with `paragraphs: true`, each `\n` starts a new paragraph); `select_text {text, occurrence}` selects the n-th match; style, table and review commands act where the caret or selection is.
- Every action is a registry command: find its id and parameters with `list_commands {query}`, run it with `execute {command, params}`, several with `batch {commands}`. Read the parameters before first use; never guess an id.
- The native file is `.docx`. `save_document` picks the format from the extension: docx, odt, rtf, html, md, tex, txt, json, pdf, png (page 1), xml.

## Rules

- **Absolute paths** for every open and save, inside `<in>` for reading and `<out>` for writing.
- **Opening or creating drops unsaved edits.** RULE: before any `open_document` or `new_document`, save the current document. CHECK: `execute file.info {}` shows `dirty: false` first; headless WordCraft gives no warning and the edits are gone.
- **A save without a path writes nothing.** RULE: always pass `path` to `save_document`. CHECK: the reply holds `saved: true` and the path you asked for; an untitled document saved with `{}` answers `saved: false`, with no error, and no file appears.
- **Saves overwrite silently.** RULE: a new name for every save. CHECK: `ls <out>/<name>` reports no such file before the save; WordCraft replaces an existing file without a word.
- **Read back what you set.** Property objects (`chr`, `para`) ignore field names they do not know, with no error. Lengths are points, colours `"RRGGBB"`. Check with `execute styles.manage {}` (each style's `format`) or `inspect_document`.
- **Table style names come from the app.** RULE: pick the name from `execute styles.manage {}` (entries with `type: "table"`), for example `Grid Table 4 – Blue` with an en dash. A name from another program is refused (`bad parameters: no table style`).
- **Back to the body after a header or footer.** RULE: after `insert.header` or `insert.footer`, run `execute caret.set {pos: {story: "body", path: [0], off: 0}}` before the next body edit. CHECK: the `caret.set` reply shows `story: "body"`; without it the caret stays in the header, and a page break or text lands there.
- **Match case on replace.** RULE: `edit.replaceAll` with `matchCase: true` (and `wholeWord: true` for whole words). CHECK: the `replaced` count equals what you expect; by default case is ignored and the replacement keeps its own case, so a capitalised title changes too.
- **Tracking is an explicit switch.** `review.trackChanges {value: true}` or `{value: false}`; without `value` it toggles. Tracked changes and comments carry the `--author` name.
- **`get_text` hides tracked deletions.** CHECK tracked work with `inspect_document`: runs marked `ins` and `del`; a replacement is one of each.
- **Contents lines count as matches.** After a table of contents, a heading's text is found first in the contents: select the heading with `occurrence: 2`.
- **Properties travel.** Title and author go into the PDF (its XMP metadata too) and the `.docx`, and the `--author` name becomes the `.docx` «last modified by»: set them on purpose with `file.properties` and read them back with `wordcraft-cli info`.
- **Paper follows the machine's region** (A4 or Letter): set it with `execute layout.size {name: "A4"}` (or `"Letter"`) and check `pageW` and `pageH` in the reply.
- **Templates hold sample text.** A `new_document` template other than blank comes with placeholder text: replace all of it.
- **CLI for reading only:** `wordcraft-cli info`, `text` and `inspect`. The CLI does not apply the folder limits, so all edits and saves go through the MCP server.

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name. W2 to W5 work on the document W1 left open; W6 and W7 open saved files.

### W1. New document with house styles (proven on WordCraft 0.8.0)

1. `new_document {template: "blank"}`.
2. `execute layout.size {name: "A4"}` (or the owner's size); the reply shows `pageW` 595.28 and `pageH` 841.89 for A4.
3. `execute styles.modify {style: "Heading1", chr: {font: "Georgia", size: 20, bold: true, color: "1B3A6B"}, para: {spaceBefore: 18, spaceAfter: 6, keepNext: true}}` and `execute styles.modify {style: "Normal", chr: {font: "Source Serif 4", size: 11}, para: {spaceAfter: 6, lineSpacing: {rule: "multiple", value: 1.15}}}`, with the owner's fonts and colours.
4. `execute file.properties {title: "<title>", author: "<owner or company>"}`.
5. `type_text {text: "<title>"}`, `execute para.style {style: "Title"}`, `execute text.newParagraph {}`, `execute para.style {style: "Normal"}`.
6. `type_text {text: "<heading 1>\n<body 1>\n<heading 2>\n<body 2>", paragraphs: true}`; then for each heading `select_text {text: "<heading>"}` and `execute para.style {style: "Heading 1"}`.
7. Check: `inspect_document {}` gives each block's `style` by id (`Title`, `Heading1`, `Normal`) and the `properties` title; `execute styles.manage {}` shows the new font, size and colour in the `format` of Heading 1 and Normal.
8. `render_page {page: 1, scale: 0.4}` and look.

### W2. Table of contents (proven on WordCraft 0.8.0)

1. Put the caret in a new paragraph under the title: `select_text {text: "<title>"}`, `execute caret.end {}`, `execute text.newParagraph {}`, `execute para.style {style: "Normal"}`. Do not insert at the start of a heading: that leaves an empty heading paragraph above the contents.
2. `execute references.toc {levels: 2, title: "Contents"}`.
3. After every later change to headings or page breaks: `execute references.updateToc {}`.
4. Check: `inspect_document {}` shows a `TOCHeading` block «Contents» and one `TOC1` block per heading, its text a tab and the page number (an empty Normal paragraph stays below the contents); the headings are now found as occurrence 2.
5. `render_page {page: 1, scale: 0.4}` and look.

### W3. Table from tab-separated lines, styled (proven on WordCraft 0.8.0)

1. Caret at the end of the text: `execute caret.docEnd {}`, `execute text.newParagraph {}`.
2. `type_text {text: "Item\tQ1\tQ2\nAlpha\t10\t12\nBeta\t7\t9", paragraphs: true}`.
3. Select the lines: `select_text {text: "Item"}`, `execute caret.docEnd {extend: true}`; then `execute table.fromText {separator: "tab"}`. The reply's caret `path` has four numbers: the caret is in the table.
4. `execute styles.manage {}` and pick a name with `type: "table"`; `execute table.style {style: "Grid Table 4 – Blue"}`, `execute table.look {headerRow: true, bandedRows: true}`, `execute table.repeatHeader {}`.
5. A new row: `select_text {text: "Alpha"}`, `execute table.insertRowBelow {}`, `type_text {text: "Gamma"}` (it goes into the first cell of the new row).
6. Check: `get_text {}` shows the rows tab-separated with «Gamma» under «Alpha»; `inspect_document {}` shows a block of type table.
7. `render_page {page: 1, scale: 0.4}`: a coloured header row and banded rows.

### W4. Page break, header and page-number footer (proven on WordCraft 0.8.0)

1. Page break before a heading: `select_text {text: "<heading 2>", occurrence: 2}` (occurrence 1 is the contents line), `execute caret.home {}`, `execute insert.pageBreak {}`.
2. `execute insert.footer {preset: "pageNumber"}`, then `execute insert.header {text: "<header text>"}`.
3. Back to the body: `execute caret.set {pos: {story: "body", path: [0], off: 0}}`; the reply shows `story: "body"`.
4. `execute references.updateToc {}` when there is a table of contents.
5. Check: `execute file.info {}` gives `pages`; `inspect_document {}` lists the header and the footer under `parts`, each with its text (the footer shows the page number).
6. `render_page {page: 2, scale: 0.4}` and look: header at the top, the page number at the bottom.

### W5. Find and replace across the document (proven on WordCraft 0.8.0)

1. `execute edit.replaceAll {text: "<old>", with: "<new>", matchCase: true, wholeWord: true}`; read `replaced`.
2. Compare the count with what the owner expects (for example, the body uses the word twice in lower case and the title once capitalised: expect 2, not 3).
3. `get_text {}` and read the changed lines and the lines that must stay.
4. With tracking on, each replacement becomes a tracked change: review it as in W6.
5. Save the draft: `ls <out>/<job>-draft.docx` must report no such file, then `save_document {path: "<out>/<job>-draft.docx"}`: `saved: true`, and `execute file.info {}` shows `dirty: false`.

### W6. Review: tracked changes and comments, then a clean copy (proven on WordCraft 0.8.0)

1. The server runs with `--author "<your name> (agent)"`. `open_document {path: "<out>/<job>-draft.docx"}` (the current document saved first).
2. `execute review.trackChanges {value: true}`: the reply is `value: true`.
3. Replace a phrase: `select_text {text: "<old phrase>"}`, `type_text {text: "<new phrase>"}`.
4. Comment: `select_text {text: "<passage>"}`, `execute review.newComment {text: "<question>"}`.
5. Check: `inspect_document {}` shows a run marked `ins` and one marked `del` in that paragraph, and `comments: 1`; `get_text {}` shows only the new phrase, which is expected.
6. `save_document {path: "<out>/<job>-review.docx"}`; `execute file.exportPdf {path: "<out>/<job>-review-markup.pdf", markup: true}` for readers without an editor (changes marked, comments beside the page).
7. Check the files: `wordcraft-cli info <out>/<job>-review.docx` gives `comments: 1` and `trackChanges: true`; `unzip -p <out>/<job>-review.docx word/document.xml | grep -o 'w:author="[^"]*"'` shows the agent's name.
8. To undo one change instead of all: `execute review.nextChange {}`, `execute review.reject {}`, and for a replacement once more `execute review.nextChange {}`, `execute review.reject {}`: a replacement is two changes, and after the first reject `get_text` already looks wrong because the deletion is still pending. Check with `inspect_document {}` that no `ins` or `del` run is left there.
9. Clean copy, when the owner approves the changes: `execute review.acceptAll {}`, `execute review.deleteComment {all: true}`, `execute review.trackChanges {value: false}`, then `save_document {path: "<out>/<job>.docx"}`. Check: `inspect_document {}` has no `ins` or `del` runs, `comments: 0`, `trackChanges: false`.

### W7. Exports: DOCX, PDF, ODT, Markdown, HTML, and reopen each (proven on WordCraft 0.8.0)

1. With the final document open (`open_document {path: "<out>/<job>.docx"}` when the session is new), save one file per agreed format, each under a free name: `save_document {path: "<out>/<job>.pdf"}`, `.odt`, `.md`, `.html`; `.png` gives page 1 as an image.
2. Check each reply: `saved: true`.
3. Check the files: `file <out>/<job>.pdf` shows the page count; `file <out>/<job>.odt` shows «OpenDocument Text»; `wordcraft-cli info <out>/<job>.odt` gives pages and words; `wordcraft-cli text <out>/<job>.md` holds the text. Where PdfCraft is installed, `pdfcraft-cli info` and `pdfcraft-cli text` on the PDF show the paper size, title, author, header and page numbers.
4. Reopen to compare (each save went to its own file, so nothing is lost): `get_text {}` on the open document first, then `open_document {path: "<out>/<job>.odt"}`, `get_text {}`, `render_page {page: 1, scale: 0.4}`, then the same for the `.md`. The text matches the `.docx`; in Markdown the contents tab becomes spaces.
5. Tell the owner what each format keeps, as seen on 0.8.0: PDF and DOCX keep everything, header, footer and contents with leaders included. ODT, HTML and Markdown keep the text, the headings and the table but drop the header and the footer; ODT also drops the house fonts and colours, and its contents become plain lines. In Markdown the Title becomes a level-1 heading like Heading 1, the contents lines become links, and the table becomes a pipe table.
6. A save as `.odt` makes the open document point at the `.odt` file, while PDF, Markdown and HTML saves leave it pointing where it was (`execute file.info {}` shows the `path`). Name every later save in full.

## Look at the result

- Numbers first: `inspect_document {}` after every step (blocks, styles, tables, runs marked `ins` and `del`, comments, pages, sections); `execute file.info {}` for pages, words, `dirty`, `trackChanges`.
- Then the eye: `render_page {page, scale}`, where `scale` is pixels per point (default 1). 0.4 to 0.5 shows layout; never read a full-size page into the conversation.
- For written files: `wordcraft-cli info|text|inspect <file>` and `file <file>`.

## Undo

- `execute edit.undo {}` steps back one edit; `execute edit.redo {}` forward. Check with `inspect_document {}` (`canUndo`, `canRedo`, the blocks).
- A rejected tracked change can be brought back with `edit.undo`.
- Undo does not touch files already written. A wrong file is replaced under a new name, and the note says which file is current.
- For a fresh start: `open_document` the last saved file (after saving or deciding to drop the current edits).

## Do not promise

- That `.docx` files from other apps open with the same layout or page breaks.
- Charts, SmartArt, ink and embedded objects from other apps surviving a round trip.
- Writing `.doc` files (they open only), or opening the oldest and encrypted `.doc` files.
- Full fidelity of RTF and ODT: notes, comments and sections come through only in part, and an ODT written by 0.8.0 has no header, footer or house fonts.
- Running macros, add-ins, cloud storage or co-authoring.
- Spelling and grammar checks beyond a few languages.
- Accessibility with real screen readers; speed on very long documents.
- Turning a PDF into an editable document.
- Work the owner watches live in their own window: attach is not confined, so it is not offered.

## Checks before hand-over

- Every output was reopened or checked and looked at (deliverable hand-over steps).
- The final `.docx` sits next to the exports; review copies are named as such.
- No tracked change or comment is left in a clean copy; review copies show the agent as author.
- Title, author and paper size are the ones agreed.
- No file was overwritten (every save went to a free name).

## Artefacts

- `<out>/<job>.docx`, the agreed exports, review copies when asked, `HANDOVER.md`, `SHA256SUMS.txt`.

## Hand-over

- Files stay in `<out>`; the owner sends or publishes them.
- Review copies go to the owner with the note that changes and comments are by the agent and still need a person's decision.

## Sources

No endorsement by these projects or their authors is implied.

Built on WordCraft documentation (github.com/storytold/wordcraft, commit f2e15cf8f899a79899a2d9595ca4ce7df1e5ea22; © 2026 ArtCraft Team and the WordCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
