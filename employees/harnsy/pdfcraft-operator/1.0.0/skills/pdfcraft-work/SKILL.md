---
name: pdfcraft-work
description: Do PDF work in PdfCraft over its MCP server - merge, split and extract pages, rotate, delete and reorder pages, fill and flatten forms, redact listed text and strip metadata, make scans searchable, text and Word drafts out - each recipe proven on PdfCraft 0.9.0, with the check after every step, undo, and the list of what not to promise. Use for any job done in PdfCraft; it also holds PdfCraft's Connect table for connecting the app and handing over files.
---

# PdfCraft work

PdfCraft is an open-source PDF editor in alpha. Every feature is a named tool with a JSON schema, and its MCP server lets an agent use those tools headless: no window, files only inside two folders named at start. This skill is the manual for that work: how to connect, how the app thinks, the recipes that were run for real on PdfCraft 0.9.0, how to look at the result, how to undo, and what not to promise.

Status to tell the owner: «Alpha: scanned text is read in English only, and .docx export does not keep the layout.»

**Route:** connect (with the Connect table below) → agree the deliverables → recipes → look at the result after each step → hand over the files.

## When to use

- A job in PdfCraft: merge, split, reorder or extract pages; fill a form; black out listed text; make a scan searchable; get the text or a Word draft out of a PDF.
- The owner asks what PdfCraft can and cannot deliver.

## Inputs

- The read folder `<in>` and the write folder `<out>` the server was started with, as absolute paths.
- The agreed deliverables list.
- The source files, and for redaction the owner's written list of what must go. Never a file outside `<in>`.

## Connect table (PdfCraft)

| Item | Value |
|---|---|
| Programs | `pdfcraft` (desktop app), `pdfcraft-cli` (CLI and MCP server) |
| CLI location | Linux, lightest route: the standalone CLI asset `pdfcraft-cli-<version>-linux-<arch>.tar.gz` (`<arch>` is `x86_64` or `aarch64`), the same binary as the full app without the window; unpacked: `<unpacked folder>/pdfcraft-cli`. Linux deb or rpm: `/usr/bin/pdfcraft-cli`. Linux full tar.gz: `<unpacked folder>/bin/pdfcraft-cli`. Windows MSI: `C:\Program Files\PdfCraft\pdfcraft-cli.exe`. macOS: the separate release asset `pdfcraft-cli-<version>-macos-<arch>.zip`. Only the deb and rpm put it on the PATH; elsewhere use the full path |
| Releases | github.com/storytold/pdfcraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | `--automation-read-root <dir> --automation-write-root <dir>`, present in 0.9.0 (proven); each given once, each an existing folder, or the server does not start. A limit left out grants none of that access. Refusals read `automation path rejected: outside the write root <dir>: <path>` (or `read root`) and nothing is written. If the `mcp` line of `pdfcraft-cli --help` has no `--automation-read-root`: stop and ask the owner to update |
| Headless start | `pdfcraft-cli mcp --automation-read-root <in> --automation-write-root <out>`; add `--compact` for a short tool list (every tool still answers by name) |
| Attach (owner watches) | none. The MCP server always runs its own headless session. The desktop window has a separate control channel (`pdfcraft --control <file>`, driven by `pdfcraft-cli ui`), and the folder limits do not cover it: the agent never uses it |
| Token | none headless. The window channel keeps its token in the control file; never print or copy it |
| Register | `claude mcp add pdfcraft -- <full CLI path> mcp --automation-read-root <in> --automation-write-root <out>` |
| Prove | `command_list {filter}` and `doc_inspect {}`; one `doc_save` outside `<out>` that must be refused |
| Check commands | reopen with `doc_open`; facts with `doc_info {doc}` or `pdfcraft-cli info <file>`; text with `text_find` or `pdfcraft-cli text <file>`; eye with `render_preview {doc, page, max_side}` (default 1024, at most 4096); every file opens and renders: `pdfcraft-cli check <out>` |
| Version | `pdfcraft-cli --version` |

## The model

- A session holds open PDFs. `doc_open` or `doc_create` returns an integer `doc`; every later call names it. `doc_list` shows the open ones with their unsaved state.
- Pages count from 1. Rectangles are in PDF points from the top-left corner of the page as displayed.
- Edits change the document in memory and stay undoable; every changing tool returns `dirty`, `undo` and `redo`. Nothing reaches the disk before `doc_save`, except the tools that write a file by themselves (`doc_combine`, `doc_split`, `page_extract` with `out`, `doc_export_text`, `doc_export_office`).
- There is no project file: the native file of a job is the edited PDF saved under the job's name.
- Find the tool before using it: `command_list {filter: "<word>"}` lists the matching menu commands, each with its `id`, `params` and the `tool` that runs it; read the tool's schema in `tools/list` before the first call. An unknown argument key is refused with JSON-RPC error `-32602`.

## Rules

Each rule ends with the check that proves it was kept.

- **Absolute paths**, inside `<in>` for reading and `<out>` for writing; a relative path is resolved against the server's own folder and refused. Check: every path in the call starts with `<in>/` or `<out>/`.
- **Never write onto an existing name.** `doc_save` with a `path`, `doc_combine`, `page_extract`, `doc_split`, `doc_export_text` and `doc_export_office` all replace a file that is already there, with no refusal and no warning: the reply looks the same as for a new file. Check: right before each of these calls, `ls <out>/<name>` answers «No such file or directory»; for a split, the folder `<out>/<job>-parts` must not exist yet (the tool creates it). After the call, `ls -la <out>` shows exactly the new entries expected.
- **Split into a fresh folder.** `doc_split` names its parts `<source name>-partK.pdf`. A second split of the same source into the same folder replaces the parts it writes and leaves older parts with higher numbers in place, so the folder then mixes two splits. Check: one new folder per split, as above, and the files in it match the reply's `files` list one to one.
- **Sources stay untouched.** A file opened from `<in>` cannot be saved in place (the save is refused); always save as a new file in `<out>`. After a save-as the open document points at the new file, and a later `doc_save {doc}` without a path writes there, as an incremental update. Check: the `path` of each save reply.
- **Unsaved work is not thrown away by accident.** `doc_close` refuses a document with unsaved changes; `discard_changes: true` only on purpose. Check: `doc_list` shows the document not dirty before a plain close.
- **A batch is not a transaction.** `command_batch` stops at the first failing step (with `stop_on_error: false` it runs the rest) and keeps the steps that ran. Check: after a failure, `doc_inspect {doc}`, then `edit_undo {doc}` once per completed step, reading each reply's `undone`.
- **Merging drops the title and author** of the sources (one bookmark per source file is kept); splits, extracts and page edits keep the source's. Check: `pdfcraft-cli info <file>` on every output → `title`, `author`, `producer`; set them as the owner wants (P1 step 5).
- **A new PDF from images carries the file name as title and «PdfCraft» as producer.** Check: `doc_info` before saving; set or clear them (P7).
- **Redaction removes only what was marked.** Find every listed item with `text_find` first; pattern marks match only well-formed values, and an item misread by text recognition is not found. Never call a redaction complete: report what was listed, marked and checked (P6). Check: `text_find` per item on the reopened file gives 0, the audit finds nothing, and the hidden-information counts are read.
- **`doc_remove_hidden` without `categories` removes every category**, flattens the form fields and drops bookmarks and links. Check: always pass the list the owner agreed, and read the reply's counts.
- **Headless only.** The window channel is not confined by the folder limits: never start or drive the owner's PdfCraft window.
- **The CLI ignores the folder limits.** Use it only for read-only facts: `info`, `text`, `check`, `audit`, on files inside `<out>`, without `--json` (that option writes a file). Never `combine`, `split`, `extract`, `edit`, `render`, `run` or `batch` from the shell. Check: the command line holds one of those four words and paths under `<out>` only.
- **No signing and no printing**: not part of this work in 1.0.0; the folder limits do not cover signing identities in system stores or printers.

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name; before each write, the name check from the rules.

### P1. Merge files, with title and author (proven on PdfCraft 0.9.0)

1. `doc_combine {paths: ["<in>/<a>.pdf", "<in>/<b>.pdf"], out: "<out>/<job>-merged.pdf"}` → `bytes`, `path`.
2. `doc_open {path: "<out>/<job>-merged.pdf"}`: `pages` is the sum of the inputs' pages.
3. `text_find {doc, query: "<a line from the second file>"}`: the first page of the second file.
4. `doc_info {doc}`: `outline` holds one bookmark per source, named after its file; `title` and `author` are `null`.
5. When the owner wants them: `doc_set_info {doc, key: "Title", value: "<title>"}`, the same for `"Author"` (an empty value removes an entry), then `doc_save {doc}` (in place: the file is in `<out>`), and `doc_info {doc}` reads them back.
6. `render_preview {doc, page: <that page>, max_side: 512}` and look.

### P2. Split into parts (proven on PdfCraft 0.9.0)

1. `doc_open {path: "<in or out>/<file>.pdf"}` (a source, or a file made earlier in the job).
2. `doc_split {doc, every: <N>, out_dir: "<out>/<job>-parts"}`, or `{doc, before: [<first pages of new parts>], out_dir}`: the reply lists `files` with `first_page` and `last_page`.
3. Check: the number of files and every range in the reply; `ls <out>/<job>-parts`; `pdfcraft-cli info <part>` → `pages` for each.

### P3. Extract pages in a chosen order (proven on PdfCraft 0.9.0)

1. `doc_open {path: "<in or out>/<file>.pdf"}`.
2. `page_extract {doc, pages: [<p>, <q>], out: "<out>/<job>-extract.pdf"}`: the pages are written in the order given.
3. `doc_open {path: "<out>/<job>-extract.pdf"}`; `text_extract {doc}`: the pages come in that order.
4. `render_preview {doc, page: 1, max_side: 512}` and look.

### P4. Rotate, delete and reorder pages, with undo (proven on PdfCraft 0.9.0)

1. `doc_open {path: "<in>/<file>.pdf"}`.
2. `page_rotate {doc, degrees: 90, pages: [1]}` (positive is clockwise); `page_delete {doc, pages: [3]}`; `page_move {doc, pages: [<p>], to: 1}` (positions counted before the move). Each reply names its `undo` step.
3. `doc_info {doc}`: page count, each page's `rotation`, bookmarks following the moves.
4. To take back the last step: `edit_undo {doc}` → `undone` names it; `doc_info {doc}` again.
5. `doc_save {doc, path: "<out>/<job>-pages.pdf"}`; `pdfcraft-cli info <out>/<job>-pages.pdf` → `pages`, and `title` and `author` still those of the source (change them as in P1 step 5 if the owner wants); `render_preview {doc, page: 1, max_side: 512}` and look.

### P5. Fill a form: live and flattened copies (proven on PdfCraft 0.9.0)

1. `doc_open {path: "<in>/<form>.pdf"}`; `form_fields {doc}`: names, types, values, pages.
2. `form_fill {doc, values: {"<text field>": "<value>", "<checkbox>": true}}` → `filled` (strings for text, combo and radio fields, `true`/`false` for checkboxes). An unknown name is refused: `there is no field named "<name>" (see form_fields)`.
3. `form_fields {doc}`: every value reads back as given.
4. `doc_save {doc, path: "<out>/<job>-filled.pdf"}`: the fields stay editable; `pdfcraft-cli info <out>/<job>-filled.pdf` → `fields` as before.
5. When a copy that cannot be edited is wanted: `doc_flatten {doc}`, then `doc_save {doc, path: "<out>/<job>-flat.pdf"}`; `pdfcraft-cli info <out>/<job>-flat.pdf` → `fields: 0`, and `pdfcraft-cli text <out>/<job>-flat.pdf` shows the values.
6. `render_preview {doc, page: 1, max_side: 512}` and look at every field.

### P6. Redact listed text and strip metadata (proven on PdfCraft 0.9.0)

1. `doc_open {path: "<in>/<file>.pdf"}`; `text_find {doc, query: "<item>"}` for each item on the owner's list: note the pages and the count.
2. `redact_mark {doc, find: "<exact text>"}` per item; other forms: `words: [...]`, `pattern: "email" | "phone" | "credit-card" | "ssn" | "date"`, `rect` with `page`, `whole_pages`. Each reply gives `marks_pending`. A pattern that finds nothing is refused (`nothing matched, so nothing was marked`): mark the exact text instead.
3. `doc_audit_redactions {doc}`: every pending mark (`kind: "unapplied-mark"`) with its page and the line of text it sits in (`covered_text`); compare with the list.
4. `redact_apply {doc}` → `applied`, `marks_pending: 0`.
5. `doc_hidden_info {doc}`: counts per category; `doc_remove_hidden {doc, categories: ["metadata"]}` (add only the categories the owner agreed).
6. `doc_save {doc, path: "<out>/<job>-redacted.pdf"}`; `doc_close {doc}`.
7. Check the saved file: `doc_open {path: "<out>/<job>-redacted.pdf"}`; `text_find` per item → `count: 0`; `doc_audit_redactions {doc}` → `count: 0`; `doc_hidden_info {doc}` → only the save date is left under metadata; `pdfcraft-cli audit <out>/<job>-redacted.pdf` → `"count":0`; `pdfcraft-cli info <out>/<job>-redacted.pdf` → no title, author or producer; `pdfcraft-cli text <out>/<job>-redacted.pdf | grep -c "<item>"` → 0 per item; `grep -a -c "<item>" <out>/<job>-redacted.pdf` → 0 (the raw bytes); `render_preview {doc, page: <each affected page>, max_side: 512}` and look at the black boxes.
8. In the hand-over, write: the list of items, the count found before and after for each, «text layer checked with `text_find` and `pdfcraft-cli text`, audit 0, metadata checked with `doc_hidden_info` and `pdfcraft-cli info`», and the sentence «Only the listed items were searched for and removed; this does not show that the file holds nothing else sensitive.»

### P7. Scan to a searchable PDF, English only (proven on PdfCraft 0.9.0)

1. `ocr_status {}` → `available: true`, languages `en`.
2. `doc_create {from: "images", paths: ["<in>/<scan>.png"], dpi: <scan resolution>}`: one page per image. Without `dpi` an image with no resolution tag gets one point per pixel and a page far too large. A scanned PDF instead: `doc_open {path}`.
3. `text_find {doc, query: "<a word on the page>"}` → 0: the page is only a picture.
4. `ocr_recognize {doc}`: `words` and the recognised `text` per page; read the text against the preview, because words can be misread (on the test scan «ID» came out as «D»).
5. `text_find {doc, query: "<the same word>"}` → found now.
6. `doc_info {doc}`: page size in points and the title from the file name. `doc_set_info {doc, key: "Title", value: "<title>"}`; `doc_set_info {doc, key: "Producer", value: ""}` when the owner wants no app name inside.
7. `doc_save {doc, path: "<out>/<job>-searchable.pdf"}`; `pdfcraft-cli text <out>/<job>-searchable.pdf` shows the text; `render_preview {doc, page: 1, max_side: 512}` and look.
Tell the owner that the hidden text layer may hold misread words and was proofread only where listed.

### P8. Text out and a Word draft (proven on PdfCraft 0.9.0)

1. `doc_open {path: "<in>/<file>.pdf"}`.
2. `doc_export_text {doc, path: "<out>/<job>.txt"}` → `pages`; pages are separated by form feeds.
3. When asked: `doc_export_office {doc, path: "<out>/<job>.docx"}` (`.pptx`, `.html` and `.rtf` by the same tool, by extension).
4. Check: `file <out>/<job>.txt <out>/<job>.docx`; `grep -c "<a line>" <out>/<job>.txt`; `unzip -p <out>/<job>.docx word/document.xml | grep -c "<a word>"`.
5. Deliver the Word file with this line: «The Word file keeps the text, headings, bold and italic; the page layout is not kept.»

## Look at the result

- Numbers first: `doc_info {doc}` or `doc_inspect {doc}` (pages, sizes, rotation, fields, bookmarks, title), `form_fields`, `text_find`.
- Then the eye: `render_preview {doc, page, max_side}`: 256 to 512 is enough for layout, 1024 (the default) for detail. Never read a full-size page image into the conversation.
- For a written file: `pdfcraft-cli info <file>`, `pdfcraft-cli text <file>`, and `pdfcraft-cli check <out>` (every PDF in the folder opens and renders; the reply counts them).

## Undo

- `edit_undo {doc}` steps back one edit, `edit_redo {doc}` forward; the reply names the step. On a document with no edits: `nothing to undo`.
- Undo works on the open document only; it does not touch files already written. A wrong output is written again under a new name, and the note says which file is current.
- For a fresh start: `doc_close {doc, discard_changes: true}` and reopen the source.

## Do not promise

- Reading scans in any language but English (unaccented Latin letters only), or text recognition without mistakes.
- A Word, PowerPoint or RTF export that keeps the page layout.
- Turning Word, spreadsheet, slide, HTML, Markdown or PostScript files into PDF.
- Reliable editing of the existing text of real files, above all CJK and right-to-left scripts.
- PDF/A, PDF/X or PDF/UA conformance, preflight, print production.
- Accessibility tagging: there is a checker only.
- Digital signatures and printing: not part of this work in 1.0.0.
- Full XFA or scripted forms; certificate-encrypted files.
- Rendering identical to other viewers, speed on very large files, or that a damaged or hostile file never hangs the app.
- That a redaction found everything: only the listed items were searched for and checked.

## Checks before hand-over

- Every output was reopened or checked and looked at (deliverable hand-over steps); `pdfcraft-cli check <out>` reports every PDF ok.
- No output replaced another file: the listing of `<out>` matches the list.
- Every redacted file carries the P6 note on how the text layer and metadata were checked.
- Every Word file carries the line from P8; every searchable scan carries the line from P7.
- Title, author and producer of every PDF were read and match what the owner wants.
- All documents are closed: `doc_list` shows none.

## Artefacts

- `<out>/<job>.pdf` (or the recipe's names), the agreed exports, `HANDOVER.md`, `SHA256SUMS.txt`.

## Hand-over

- Files stay in `<out>`; the owner sends or publishes them.
- Signing, printing, or a job the owner wants to watch in the window goes back to the owner: those are outside this work.

## Sources

No endorsement by these projects or their authors is implied.

Built on PdfCraft documentation (github.com/storytold/pdfcraft, commit 645016addcfb9078c557f0189559ab47cdcee057; © 2026 ArtCraft Team and the PdfCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
