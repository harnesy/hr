---
name: deliverable-handoff
description: Agree the list of files a job delivers, save the app's native file, export each listed file into the write folder, reopen and look at every output, check metadata and checksums, and leave a one-page HANDOVER.md next to the files. Use at the end of every job in a desktop app that produces files, and before the job starts to agree the list.
---

# Deliverable hand-over

An export reply that says «written» proves little: the file can have the wrong size, the wrong format, a flattened layer the owner needed, or a camera's location still inside it. This skill turns the end of a job into a short, checkable routine. Every file on the agreed list is exported, opened again and looked at, and the hand-over note says what was checked, what the app could not do and where everything is. Nothing leaves the write folder unless the owner sends it.

**Route:** agreed list (before the work) → native file saved → one export per row → reopen and look at each output → metadata → checksums → HANDOVER.md → the owner takes it from the write folder.

## When to use

- At the start of a job: to write the list of deliverables and get a yes.
- At the end of every job that produces files from a desktop app.
- When a delivered file is replaced: the same checks run again for the new file.

## Inputs

- The agreed deliverables list. Each row: file name, format, pixel size or scale (or page size for documents), colour space where it matters, what it is for. Agree it before the work starts; if the owner gave none, write one and ask for a yes.
- The native document of the job.
- The connection note from connecting the app.
- The app's check commands from the Connect table in its work skill: how to reopen a file or print its facts, and how to take a preview or screenshot.

## Rules

- **Native first.** The app's own lossless file is saved before any export, next to the exports.
- **One export per list row**, into the write folder only. Never overwrite a file that already exists: use a new name, or ask.
- **Reopen, do not trust the reply.** Every output is opened again, its facts compared with its list row, and a preview of the reopened file looked at.
- **Location data needs a yes.** A photo that still carries location or camera-owner data is delivered only after the owner says so.
- **Hand over in place.** The files stay in the write folder. Uploading, sharing links, sending or publishing is the owner's step, or needs the owner's explicit OK for each destination.
- **Say what the app could not do**, quoting the line from the app's «do not promise» list that applied.

## Steps

1. **Agree the list** (before the work). Write the table of deliverables and get a yes. Changes later go into the note with the reason.
2. **Save the native file** into the write folder, named after the job.
3. **Export each row.** One export per row, the name from the list, into the write folder. If a name is taken, stop and pick a new one.
4. **Reopen and check each output:**
   - `file <name>` shows the type agreed and, for images, the pixel size (on Windows, which has no `file`: the app's info command gives the type and size);
   - the app's reopen or info command reports the expected format, size or page count, and the layers or pages the row asked for;
   - a preview or screenshot of the reopened file is looked at, at a bounded size;
   - vector files and PDFs: the page count, and text kept as text or outlined as agreed;
   - the size in bytes is above zero.
5. **Check metadata** of every photo or raster file: `file <name>` shows «Exif» for a JPEG that carries it; for any format, `grep -a -c -E 'Exif|EXIF|eXIf|xmpmeta' <name>` above 0 means metadata is inside (on Windows: `findstr /m "Exif EXIF eXIf xmpmeta" <name>` prints the file name when a marker is inside). If metadata is there and the source came from a camera or a phone, treat location as present unless a metadata reader shows otherwise; ask the owner before delivering, or make a clean copy with the app's own method.
6. **Checksums.** `sha256sum <every delivered file> > SHA256SUMS.txt` in the write folder (on Windows: `Get-FileHash -Algorithm SHA256 <file>` in PowerShell, one line per file into the same list).
7. **List the folder** (`ls -la <write folder>`; on Windows `Get-ChildItem <write folder>`) and compare it with the list: every row has a file, nothing extra was written, nothing outside the folder.
8. **Write HANDOVER.md** in the write folder (below), at most one page.

## Checks before hand-over

- Every list row has a file, and every file was reopened and looked at.
- The native file sits next to the exports.
- No file was written outside the write folder, and none was overwritten.
- Metadata was checked; any location data was cleared or approved by the owner.
- `SHA256SUMS.txt` lists every delivered file.
- The gaps that applied are stated in the note.

## Artefacts

`HANDOVER.md` (or the project's own format) in the write folder:

- the file table: name, format, pixel size or pages, bytes, what it is;
- the native file and how to reopen it;
- the connection note: app and CLI versions, backend, folders;
- what was checked and how (commands, previews looked at);
- metadata found and what was done about it;
- what the app could not do, with the «do not promise» line quoted;
- changes from the agreed list, and why;
- open points for the owner.

## Hand-over

- The owner gets the path of the write folder and the note. The owner decides where the files go next.
- A file that failed its check is not delivered: the note names it, says what failed and what is proposed.

## Sources

Written from the apps' own public documentation and general practice, in our own words; facts only.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
