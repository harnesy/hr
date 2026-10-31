---
name: gridcraft-work
description: Do spreadsheet work in GridCraft over its MCP server - a sheet from CSV, formulas with their results checked, formatting and number formats, sort and filter, charts, pivot tables, XLSX/CSV/PDF exports, the native save and its reopen check - each recipe proven on GridCraft 0.8.0, with the check after every step, undo, and the list of what not to promise. GridCraft has no folder limits: this skill connects it itself, only in a dedicated project folder with the owner's OK. Use for any job done in GridCraft.
---

# GridCraft work

GridCraft is an open-source spreadsheet app in alpha: workbooks of sheets with formulas, number formats, tables, charts and pivot tables. Every menu action is a command, and its MCP server lets an agent build, check and export workbooks headless. Unlike the other Craft apps, GridCraft 0.8.0 cannot be told to stay inside chosen folders: its server can read and write any file the user can. So this skill does the connecting itself, in one narrow way: a folder made for the job, the owner's OK, absolute paths inside that folder, and a check after the job that nothing outside it changed. It also holds how the app thinks, the recipes that were run for real on GridCraft 0.8.0, how to look at the result, how to undo, and what not to promise.

Status, in one line for the owner: «Alpha: GridCraft cannot be fenced to chosen folders yet, so it runs only in a dedicated project folder, with your OK.»

**Route:** connect (Connect below: OK, project folder, marker, start, prove) → agree the deliverables → recipes → look at the result after each step → hand over the files → the outside-change check.

## When to use

- A job in GridCraft: turn data into a sheet, add formulas and totals, format, sort, filter, chart, pivot, export.
- The owner asks what GridCraft can and cannot deliver.
- Not for the general connect skill: this app has no folder limits, so its own Connect section below replaces that skill for GridCraft.

## Inputs

- The project folder `<dir>`, made for this job (Connect, step 5), as an absolute path, with `<dir>/in` for sources and `<dir>/out` for the deliverables (the write folder of the hand-over).
- The owner's OK for running GridCraft without folder limits on this machine (Connect, step 4).
- The agreed deliverables list.
- The source data the owner provides (CSV or a workbook), copied into `<dir>/in`. Never invented figures in a delivered workbook without saying so.

## Connect

GridCraft 0.8.0 has no folder limits, so the usual rule «never run unconfined» cannot be met. This section is the only way this skill allows instead: the server runs unconfined, but only in a folder made for the job, with the owner's OK, and the job ends with proof that nothing outside that folder changed.

### Connect table (GridCraft)

| Item | Value |
|---|---|
| Programs | `gridcraft` (desktop app), `gridcraft-cli` (CLI and MCP server) |
| CLI location | Linux tar.gz: `<unpacked folder>/bin/gridcraft-cli`, not on the PATH. Linux deb or rpm: `/usr/bin/gridcraft-cli`. Windows MSI: `gridcraft-cli.exe` in the GridCraft program folder; use the full path. macOS: the separate release asset `gridcraft-cli-<version>-macos-universal.zip` |
| Releases | github.com/storytold/gridcraft/releases, each with `SHA256SUMS.txt` |
| Folder limits | **none in 0.8.0.** `gridcraft-cli mcp --automation-read-root <dir>` stops with `gridcraft-cli: unknown option --automation-read-root`. The server reads and writes wherever a call points it. Use the unconfined route below; when a later version lists the limit flags, use them and leave this route |
| Headless start | `sh -c 'cd <dir> && exec <cli> mcp'`: the project folder becomes the server's working folder (Windows: `cmd /c "cd /d <dir> && <cli> mcp"`) |
| Attach (owner watches) | not offered. `gridcraft --control <port>` with `gridcraft-cli mcp --connect <port>` is just as unconfined, the desktop app has no folder limits either, and its control port has no token. Show the owner exported PDFs instead |
| Token | none: headless needs none, and the control port has no token at all |
| Register | `claude mcp add gridcraft -- sh -c 'cd <dir> && exec <cli> mcp'` (Codex: `codex mcp add gridcraft -- sh -c 'cd <dir> && exec <cli> mcp'`); on Windows: `claude mcp add gridcraft -- cmd /c "cd /d <dir> && <cli> mcp"` (Codex the same); `<cli>` as a full path when it is not on the PATH |
| Prove | `list_commands {search: "pivot"}` and `inspect_workbook` answer; the server's working folder is `<dir>` (Linux: `readlink /proc/<pid>/cwd`, the pid from `pgrep -f 'gridcraft-cli mcp'`; macOS: `lsof -a -p <pid> -d cwd`). There is no refused write to prove: nothing is refused |
| Check commands | reopen with `open_workbook` after `file.close`; facts with `inspect_workbook`, `read_range`, `get_cell`, `pivot.list`, or `gridcraft-cli info <file> --json`, `cat <file> --range <r> --formulas`, `check <file>` (read-only, paths inside `<dir>`); eye: export a PDF (G7) and turn its pages into small JPEGs, `pdftoppm -jpeg -scale-to 800 <file>.pdf <dir>/out/look/<name>` |
| Version | `gridcraft-cli version` or `--version` |
| Own files outside `<dir>` | the desktop app writes its log to `~/.config/gridcraft/logs/gridcraft.log`; the MCP server and the read-only CLI checks wrote nothing there in the proof run |

### Steps

1. **Detect.** `uname -sm` (Windows: read the environment). Look for `gridcraft-cli` on the PATH and at the table's install paths. If found, `<cli> --version` and record the line. Never run the desktop `gridcraft` to ask for help: `gridcraft --help` tries to open a window.
2. **Decide.** Missing or too old: tell the owner the release asset you propose, the release page, where it will go, and that it needs their OK. Mention the apps' own launcher (github.com/storytold/craft-launcher) as something the owner may run themselves; the agent never runs it.
3. **Install, with the OK.** Download the asset and the release's `SHA256SUMS.txt` into an empty folder; `sha256sum -c --ignore-missing SHA256SUMS.txt` must print the asset's name with «OK» (Windows: `Get-FileHash <file> -Algorithm SHA256` equals the listed value). A mismatch stops the install and the download is deleted. Install with the system's package tool, or unpack the tar.gz in the user's folder (for example `~/.local/opt/gridcraft-<version>/`), no admin rights. `<cli> --version` again; keep the «OK» line for the note.
4. **The owner's OK for running without folder limits**, once per machine. Ask in these words: «GridCraft cannot be limited to chosen folders yet: while it runs, it can read and write any file your user can. I will run it only in a new folder made for this job, give it only paths inside that folder, and check after the job that nothing outside the folder changed. OK?» Record the answer, who gave it and the date in the connection note. No OK, no GridCraft: say what was found and stop.
5. **Make the project folder** for the job: `mkdir -p <dir>/in <dir>/out`. A new, empty folder: never the home folder, the filesystem root, or a folder that already holds a project or the owner's files. Copy the sources in (`cp <owner's file> <dir>/in/`); the owner's original stays where it was and is never opened by GridCraft.
6. **Set the marker** before the server starts: `touch <dir>/.job-start`.
7. **Start** with the table's headless start: `<dir>` is the server's working folder, so a path that slips through without its folder lands inside `<dir>`, not in the home folder. Still give every path in full, starting with `<dir>/`.
8. **Register** with the table's line (local scope, private to this project). A shared `.mcp.json` entry only when the owner asks, and they approve it in an interactive run. If the name `gridcraft` is taken, ask before replacing it. Leave other MCP entries alone.
9. **Prove the link** in a fresh session: `claude mcp get gridcraft` (Codex: `codex mcp list`) shows the entry with the `cd <dir>` in it; `list_commands {search: "pivot"}` and `inspect_workbook` answer; the server's working folder is `<dir>` (table, «Prove»).
10. **Write the connection note** (Artefacts) for the hand-over.

### After the job: the outside-change check

Run it after the last file is written and the server is stopped (or idle).

1. `find <home> -newer <dir>/.job-start -type f -not -path '<dir>/*' > <dir>/outside-changes.txt` (Windows: `Get-ChildItem <home> -Recurse -File | Where-Object { $_.LastWriteTime -gt (Get-Item <dir>\.job-start).LastWriteTime -and $_.FullName -notlike '<dir>\*' }`). On a busy machine this takes a while and lists many files written by other programs; `find` ends with exit code 1 when some folders cannot be read, and the list is still usable.
2. Narrow it to what this job could have written: `grep -i -E 'gridcraft|<job>|\.(xlsx|xlsm|csv|tsv|json|html|pdf|png)$' <dir>/outside-changes.txt`.
3. Explain every line of the narrowed list: GridCraft's own log (`~/.config/gridcraft/logs/gridcraft.log`) is expected only if the desktop app ran; a file of another program or another project is named as such; any file a GridCraft call or the agent may have written is a stray write: tell the owner at once, with the path and time, and do not delete it without their OK.
4. Put the result in the hand-over note: the marker time, the size of the full list, the narrowed lines and what each one is, and «no file outside `<dir>` was written by this job» only when that is what the check showed. `outside-changes.txt` stays in `<dir>`, not in `<dir>/out`.

## The model

- A session holds open workbooks; one is active. A workbook has sheets; the active sheet is where calls without a `sheet` act. `select {range: "<sheet>!A1"}` switches sheets.
- Cells are A1-style. `write_range` writes a block of rows from its top-left cell; a string starting with `=` is a formula, other strings are read as if typed into the cell.
- Every action is a command: find ids and params with `list_commands {search}`, run one with `execute_command {command, params}`. The tools (`write_range`, `format_range`, `sort_range`, `filter`, `insert_chart`, `create_table`) are short forms of commands. Never guess an id or a parameter.
- Headless there is no window and no screenshot: the eye check is a PDF export turned into a small picture.

## Rules

- **Only inside `<dir>`.** Every open, save, import and export path is absolute and starts with `<dir>/`: sources in `<dir>/in`, outputs in `<dir>/out`. No path to the owner's other files, even to read them: copy them into `<dir>/in` first (Connect, step 5). The server does not refuse a path outside, so this rule is the only fence.
- **Every write overwrites without warning**: `save_workbook`, `file.exportCsv` and `file.exportPdf` replace an existing file silently, the source CSV included. Before each one, `ls <dir>/out/<name>` must answer «No such file or directory»; if the name is taken, pick a new one.
- **A workbook opened from CSV saves back to the CSV.** `save_workbook {}` writes values only into the file it came from, and the formulas are lost there. Save it at once under its native name with `save_workbook {path: "<dir>/out/<job>.xlsx"}` (G1); from then on `save_workbook {}` writes the `.xlsx`.
- **Reopening needs a close.** `open_workbook` on a path that is open answers `alreadyOpen: true` and does not read the disk. To check a saved file: `save_workbook {}`, `execute_command file.close {}`, then `open_workbook`.
- **Close refuses unsaved work.** `file.close {}` on a changed workbook answers `closed: false, dirty: true`; `force: true` throws the changes away. Save first; force only on purpose.
- **A chart takes one block.** Give `insert_chart` one contiguous range whose first column holds the labels and the next columns the numbers. A range of two separate areas (`A1:A7,F1:F7`) gave a chart with no bars. Build a small summary block first (G5).
- **Keep totals out of a sort.** Give `sort_range` the data rows only, with `header: true`, and keep a totals row out of that range (a blank row between them is not enough without the range).
- **Look at numbers before formats.** `read_range` gives values; `formatted: true` gives what the owner sees; `formulas: true` gives the formulas. Check all three where it matters.
- **The CLI only for reading and checks**: `info`, `cat`, `eval`, `check`, `commands`, `functions`, `version`, on paths inside `<dir>`. Never `run`, `convert` or `send`: they write wherever they are told and bypass the call log. Never the desktop `gridcraft`.
- **No attach, no screenshot tool, no web functions.** `screenshot` needs the desktop app; `WEBSERVICE` and other external-data commands are not used.

## Recipes

Each recipe was run with these exact steps. `<job>` is the job's short name; `<data>` is the CSV's name without `.csv`, which becomes the sheet name.

### G1. A sheet from CSV, saved as a workbook (proven on GridCraft 0.8.0)

1. The CSV is in `<dir>/in/<data>.csv` (Connect, step 5).
2. `open_workbook {path: "<dir>/in/<data>.csv"}`: the reply lists one sheet named `<data>` and `warnings` (empty when the import was clean).
3. `inspect_workbook`: `usedRange` covers the header and every data row; `read_range {}` shows numbers as numbers (`12.0`, not `"12"`).
4. At once: `ls <dir>/out/<job>.xlsx` finds nothing, then `save_workbook {path: "<dir>/out/<job>.xlsx"}`; `inspect_workbook` shows `path` ending in `.xlsx` and `dirty: false`.
5. Or into an existing workbook as a table on a new sheet: `execute_command data.fromTextCsv {path: "<dir>/in/<data>.csv", sheet: "<name>"}`; the reply gives `rows` and `cols`, and `inspect_workbook` shows the new sheet with a table over the data.

### G2. Formulas and their checked results (proven on GridCraft 0.8.0)

1. A computed column: `write_range {range: "F1", values: [["Revenue"], ["=D2*E2"], ["=D3*E3"], …]}`, one formula per data row.
2. A totals row below a blank row: `write_range {range: "A9", values: [["Total", null, null, "=SUM(D2:D7)", null, "=SUM(F2:F7)"]]}`.
3. `read_range {range: "F2:F9"}`: every result is a number; none is an `{"error": …}` object. `read_range {range: "A9:F9", formulas: true}` shows the formulas as typed.
4. Cross-check a total another way without touching the sheet: `evaluate_formula {formula: "=SUMPRODUCT(D2:D7,E2:E7)"}` equals the value in F9. `get_cell {cell: "F9"}` shows `type: number`, the formula and the value.
5. Work out one row by hand and compare; say in the note which checks were made.

### G3. Formatting and number formats (proven on GridCraft 0.8.0)

1. Header: `format_range {range: "A1:F1", bold: true, fillColor: "#DDEBF7", borders: "bottom"}`; the reply lists the commands applied.
2. Money: `format_range {range: "E2:F9", numberFormat: "Currency"}`. Totals: `format_range {range: "A9:F9", bold: true, borders: "top"}`.
3. Fit the columns to the new text: `execute_command home.autofitColumnWidth {cols: "A:F"}`. Without it a wide formatted total is printed as `#######` in the PDF.
4. Check: `read_range {range: "E2:F3", formatted: true}` shows the display text (`$18.50`); `get_cell {cell: "A1"}` shows `font.bold: true`, the fill and the bottom border in `style`.
5. `save_workbook {}`.

### G4. Sort and filter (proven on GridCraft 0.8.0)

1. Sort the data rows only: `sort_range {range: "A1:F7", header: true, keys: [{column: "F", order: "desc"}]}`; the reply names the rows sorted (`A2:F7`).
2. Check: `read_range {range: "A1:F9"}`: header in place, rows in the new order, the totals row unchanged; `read_range {range: "F2:F3", formulas: true}`: each formula still points at its own row.
3. Filter: `filter {range: "A1:F7", column: "A", values: ["North", "East"]}` (or `custom: {op: ">=", value: "10"}`); the reply gives `hiddenRows`.
4. Check which rows show: `select {range: "A1:F7"}`, then `execute_command edit.goToSpecial {kind: "visible"}`: the selection lists only the header and the kept rows. `evaluate_formula {formula: "=SUBTOTAL(103,A2:A7)"}` counts the visible rows.
5. Clear: `filter {range: "A1:F7", column: "A", clear: true}` (`hiddenRows: 0`); remove the filter buttons with `execute_command data.filter {range: "A1:F7"}` (`filter: false`); `inspect_workbook` shows `autofilter: null`. Keep a filter in the file only when the owner asked for it.
6. `save_workbook {}`.

### G5. A chart (proven on GridCraft 0.8.0)

1. A summary block next to the data, labels first: `write_range {range: "H1", values: [["Region", "Revenue"], ["East", "=SUMIF(A2:A7,H2,F2:F7)"], ["North", "=SUMIF(A2:A7,H3,F2:F7)"], ["West", "=SUMIF(A2:A7,H4,F2:F7)"]]}`; `read_range {range: "H1:I4"}` shows the sums, and their total equals F9.
2. `insert_chart {range: "H1:I4", type: "column", title: "<title>", at: "K2"}`: the reply gives the chart id.
3. `inspect_workbook`: the sheet's `charts` lists kind `ColumnClustered`, the title, `at: "K2"` and `series: 1`.
4. Legend and axis titles: `execute_command chart.set {chart: <id>, legend: "none", xTitle: "<text>", yTitle: "<text>"}`. `inspect_workbook` does not show these; the picture in the next step does.
5. Eye: export the PDF (G7, steps 3 and 4) and look at the page of the data sheet: one bar per label, heights in the right order, the axis titles, no legend. `save_workbook {}`.

### G6. A pivot table (proven on GridCraft 0.8.0)

1. `execute_command insert.pivotTable {source: "<data>!$A$1:$F$7", rows: ["Region"], values: [{field: "Revenue", func: "sum"}], name: "<pivot>"}`: the reply gives the new sheet (placed before the data sheet, so it is also the first page of a PDF of all sheets; named `Sheet1` or the next free name), the anchor `A3` and the range.
2. `execute_command sheet.rename {sheet: "<sheet from the reply>", name: "Pivot"}`.
3. `read_range {sheet: "Pivot"}`: «Row Labels», one row per region, «Grand Total» equal to F9 on the data sheet.
4. A second dimension: `execute_command pivot.addField {pivot: "<pivot>", field: "Product", area: "columns"}`; `read_range {sheet: "Pivot"}` shows one column per product and the grand totals both ways.
5. `execute_command pivot.list {}`: name, sheet, source, rows, columns, values and function, as asked. Refer to the pivot by its name: its `id` changes when the file is reopened. `save_workbook {}`.

### G7. Exports: XLSX, CSV and PDF (proven on GridCraft 0.8.0)

Before each export: `ls <dir>/out/<name>` must find nothing (rule on overwrites).
1. XLSX is the native file: `save_workbook {}` once the workbook carries the `.xlsx` path from G1.
2. CSV of one sheet: `execute_command file.exportCsv {path: "<dir>/out/<job>-<data>.csv", sheet: "<data>"}`: the whole used range of that sheet (summary blocks too) as the owner sees it, number formats included (`$120.00`; a value with a comma in quotes). For plain numbers, export before G3 or from a sheet without number formats. Check: `head <dir>/out/<job>-<data>.csv` matches `read_range {sheet: "<data>", formatted: true}`.
3. PDF: `execute_command file.exportPdf {path: "<dir>/out/<job>.pdf", sheets: "all", fitToPage: true}`: the reply gives `pages` and `bytes`; without `sheets: "all"` only the active sheet is printed.
4. Check the PDF: `pdfinfo` (pages as in the reply), `pdftotext <dir>/out/<job>.pdf - | grep '<a label>'` (the text is there), `pdftotext <dir>/out/<job>.pdf - | grep -c '##'` answers 0 (no column too narrow: G3, step 3), then `mkdir -p <dir>/out/look` and `pdftoppm -jpeg -scale-to 800 <dir>/out/<job>.pdf <dir>/out/look/<job>` (one picture per page) and look at each. Remove `<dir>/out/look` before the checksums, or list it as a check file.
5. Metadata: `unzip -p <dir>/out/<job>.xlsx docProps/core.xml` (empty unless `file.properties` set a title or author) and `pdfinfo` (Title is the workbook's file name, Creator «GridCraft»). Set `execute_command file.properties {title, author}` only with words the owner gave.

### G8. Save, reopen and check (proven on GridCraft 0.8.0)

1. `save_workbook {}`; `inspect_workbook` shows `dirty: false`.
2. `execute_command file.close {}` answers `closed: true` (with `closed: false, dirty: true`, save first: rule on close).
3. `open_workbook {path: "<dir>/out/<job>.xlsx"}`: the sheets as saved, `warnings` empty.
4. `inspect_workbook`: sheets, used ranges, the chart (kind, title, place, series); `execute_command pivot.list {}`: the pivot with its fields; `read_range {sheet: "<data>", formulas: true}`: the formulas; `read_range {sheet: "<data>", range: "E2:F3", formatted: true}`: the number formats.
5. From the shell, read-only: `gridcraft-cli info <dir>/out/<job>.xlsx --json` (sheets, cells, charts); `gridcraft-cli cat <dir>/out/<job>.xlsx --sheet <data> --range F1:F9 --formulas`; `gridcraft-cli eval '=SUM(F2:F7)' --in <dir>/out/<job>.xlsx --sheet <data>` equals the total; `gridcraft-cli check <dir>/out/<job>.xlsx`: every formula matched and «round trip: all equal», exit code 0.
6. End: `execute_command file.close {}`; `inspect_workbook` then answers «no workbook open».

Not in these recipes (not proven): JSON and HTML exports, conditional formats, data validation, slicers, recorded scripts, Solver and the other analysis tools.

## Look at the result

- Numbers first: `inspect_workbook` (sheets, used ranges, charts, tables, filters, `dirty`, history), `read_range` with and without `formulas` and `formatted`, `get_cell` for one cell's type, formula and style, `pivot.list` for pivots, `evaluate_formula` for cross-checks.
- Then the eye: a PDF export turned into a JPEG of at most 800 px (G7, step 4). Never read a full-size image into the conversation.
- For a written file: `file`, `pdfinfo`, `pdftotext`, `head` for CSV, and the read-only `gridcraft-cli info`, `cat`, `eval` and `check`.

## Undo

- `undo {}` steps back one change and names it (`undone: "Insert Chart"`); `undo {steps: n}` goes back several; `redo {}` forward. Check with `inspect_workbook` (`undo` and `redo` lists) or `read_range`.
- A wrong sort or filter: `undo {}` once; check the row order or `hiddenRows` again.
- Undo does not remove files already written, and a reopened workbook starts with an empty history. A wrong export is replaced under a new name, and the note says which file is current.
- For a fresh start: `execute_command file.close {force: true}` drops the changes, then reopen the saved file. Do this only on purpose.

## Do not promise

- Confinement: GridCraft 0.8.0 cannot be limited to chosen folders; the only fence is this skill's route.
- Workbooks it saves opening cleanly in other spreadsheet apps: its `.xlsx` files are tested on its own files only.
- Large workbooks: very big files may not open, and recalculation runs on a single thread.
- Slicers, timelines and data-model content surviving a save of a workbook that had them.
- Chart types and options surviving a round trip beyond the simple ones, or resizing a chart.
- Text in non-Latin scripts in the grid or the PDF.
- The exact result of every function: some calculation bugs are known; check key figures (G2).
- `.xls` beyond values, formulas and number formats; `.xls`, XLSB or ODS output; saving with a password.
- Pivot slicers, calculated items and pivot charts.
- An interface in another language, queries to external data, and the solver or other analysis tools.
- Watching the work live in the app window: attach is not offered.
- AI features of any kind.

## Checks before hand-over

- Every output was reopened or checked and looked at (deliverable hand-over steps); the `.xlsx` passed `gridcraft-cli check`.
- Key figures were cross-checked (G2) and match in the reopened file.
- No filter is left on unless asked; every chart was looked at in a PDF picture.
- The source CSV in `<dir>/in` is unchanged (`sha256sum` before and after, or a fresh copy of the owner's file).
- All workbooks are closed: `inspect_workbook` answers «no workbook open».
- The outside-change check ran and its result is in the note.

## Artefacts

- `<dir>/out/<job>.xlsx`, the agreed exports, `HANDOVER.md`, `SHA256SUMS.txt`; `<dir>/.job-start` and `<dir>/outside-changes.txt` next to them, outside `<dir>/out`.
- The connection note, five to ten lines: system; `gridcraft-cli` version; install source and the checksum «OK» line (after an install); backend headless; «no folder limits: the owner's OK» with who and when; the project folder and that the server's working folder was checked to be it; harness and server name; the prove result; the marker time; date.

## Hand-over

- Files stay in `<dir>/out`; the owner sends or publishes them. The note carries the connection note and the outside-change result.
- A stray write outside `<dir>`, a refused OK or a failed checksum goes to the owner with what was found and what is proposed.
- An owner who wants to watch the work live gets PDF pictures, and the reason attach is not offered.

## Sources

No endorsement by these projects or their authors is implied.

Built on GridCraft documentation (github.com/storytold/gridcraft, commit 823c56582d00be91e31b4f7f3680496cf89e84fb; © 2026 ArtCraft Team and the GridCraft contributors, MIT (taken under the MIT option of MIT OR Apache-2.0), https://opensource.org/licenses/MIT), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
