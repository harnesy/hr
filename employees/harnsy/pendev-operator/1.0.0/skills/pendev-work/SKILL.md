---
name: pendev-work
description: Do design work in pen.dev over its MCP tools or its headless CLI shell - connect it with the owner's OK in a folder made for the job, check the active document before every edit, design screens, components and styles, import Figma files, images and web pages, export PNG/JPEG/WEBP/PDF and HTML, look at every change - with the never-list and the outside-change check. pen.dev has no folder limits, so this skill connects it itself. Use for any job done in pen.dev.
---

# pen.dev work

pen.dev is a proprietary design editor by High Agency, Inc. It runs as a desktop app, inside VS Code or Cursor as an extension, or headless through its CLI, `pen`. Designs live in `.pen` files, which are JSON (the skill pen-files explains them). An agent works through the MCP tools pen.dev offers: it asks which document is open, runs small scripts that read, change, render and export the design, and loads pen.dev's own drawing instructions. pen.dev cannot be told to stay inside chosen folders, and it writes its own MCP entry into the agent's client. So this skill does the connecting itself, in one narrow way: the owner's OK, a folder made for the job, absolute paths inside it, and a check after the job that nothing outside it changed.

Status, in one line for the owner: «Works with your own pen.dev install and account; pen.dev has no folder limits, so it works only in a job folder you name.»

Cost, in one line for the owner: «pen.dev's Free plan limits the days of agent work per month, and work over MCP counts too; see pen.dev's pricing page.»

How far each step is proven. We have run pen.dev's CLI 0.3.14 without an account and without a window: the install into a user folder, `pen version`, `pen status` while signed out, and the help texts. Those steps say «(proven on CLI 0.3.14)». Every other step that calls pen.dev says «(read from docs.pen.dev, not tried)»: it follows the public docs of 2026-10-31 and has not been run by us. Tell the owner so when such a step matters. A step with no mark is a question to the owner or a plain shell command.

**Route:** connect (Connect below: OK, job folder, marker, link, active document) → agree the deliverables → recipes → look at a screenshot after each change → save to a new file and commit → hand over → the outside-change check.

## When to use

- A job in pen.dev: design or change screens, build components, variables and styles, import a Figma file, images or a web page, export images, PDFs or HTML.
- The owner asks what pen.dev can and cannot deliver, or what it costs in agent days.
- Not for the general connect skill: pen.dev has no folder limits and writes its own MCP entry, so the Connect section below replaces that skill for pen.dev.

## Inputs

- The job folder `<dir>`, made for this job (Connect, step 4), as an absolute path, with `<dir>/in` for the owner's files and `<dir>/out` for the deliverables (the write folder of the hand-over).
- The owner's OK for using pen.dev without folder limits on this machine (Connect, step 3).
- The agreed deliverables list.
- The files the owner gives: `.pen`, `.fig`, PNG, JPEG, SVG, or the address of a page. Only material the owner provides or has the rights to.

## Connect

pen.dev has no folder limits, so the usual rule «never run unconfined» cannot be met. This section is the only way this skill allows instead: pen.dev runs as the owner installed it, but the agent works only in a folder made for the job, with the owner's OK, and the job ends with proof that nothing outside that folder changed.

### Connect table (pen.dev)

| Item | Value |
|---|---|
| Hosts | desktop app (macOS, Windows, Linux AppImage or tarball), the extension for VS Code and Cursor, and the CLI `pen` (npm package `@pen.dev/cli`, Node.js 22.19 or newer). The owner installs the app or the extension |
| CLI licence | the npm package says `UNLICENSED`: it is proprietary. It is never shipped, copied or vendored with a job; the owner installs it under pen.dev's terms |
| MCP server name | `pencil` (pen.dev's former name, kept in the entry, in the second CLI command and in the `~/.pencil` folder) |
| Who writes the entry | pen.dev itself, when the owner turns the client on under Settings → MCP; turning it off takes the entry out again. The agent never writes, edits or removes it |
| How the link works | the client starts pen.dev's MCP server over stdio, and the server talks to the running app through a local socket (a named pipe on Windows). So the app must be running with the job's `.pen` open |
| Tools | `get_app_state`, `execute`, `get_style`, `read_skill`; `browser` only when the server talks to the desktop app; `spawn_agents` only with a start flag, never turned on here |
| Prove | `/mcp` in the client lists `pencil`; `get_app_state()` names the job's file under `<dir>` |
| Version | `pen version` prints `pen 0.3.14` with exit code 0, no account needed (proven on CLI 0.3.14). Never `pen --version`: it is not a version flag and asks for a sign-in. The app's version: ask the owner (About in the app's menu) |
| Sign-in check | `pen status`: «Not authenticated» and exit code 1 when signed out (proven on CLI 0.3.14); exit code 0 when signed in (read from docs.pen.dev, not tried) |
| Session | `~/.pencil/session-cli.json`, written by the owner's own sign-in. The agent never opens, copies or prints it |
| What needs an account | agent runs, exports, the interactive shell and workspaces. Without one, an export and the headless shell both stop with «Authentication required», exit code 1, and write nothing (proven on CLI 0.3.14) |
| Headless shell | `pen interactive --out <new .pen> [--in <file.pen>]`; `pen interactive --app desktop` attaches to the running desktop app instead |
| Folder limits | **none.** Neither the app, the MCP server nor the CLI can be limited to chosen folders |
| Agent days | Free: 5 agent days a month, MCP work included, 1 agent at a time; Pro and Ultra: agent work every day (pen.dev pricing page, read 2026-10-31). Figures change: check the page before quoting them |

### Steps

1. **Detect.** `uname -sm`; `command -v pen`; if found, `pen version` and record the line (proven on CLI 0.3.14). Ask the owner which host they use (desktop app or IDE extension) and its version. Never `pen --version`, and never `pen login` in any form: no flags, not even `--help`, which starts the sign-in.
2. **CLI, only when needed and only with the OK.** The CLI is needed for the headless route (step 7). If it is missing, propose the exact command `npm i -g @pen.dev/cli@<version>`, say where it goes and that it needs the owner's OK; record the version and never update it unasked. A user folder works without admin rights: `npm i -g @pen.dev/cli@<version> --prefix <folder> --ignore-scripts`, then `<folder>/bin/pen version` (proven on CLI 0.3.14). Whether exports need the install scripts this skips is not tried.
3. **The owner's OK for working without folder limits**, once per machine. Ask in these words: «pen.dev cannot be limited to chosen folders: while I am connected to it, it can read and write any file your user can. I will work only in a new folder made for this job, use only paths inside it, and check after the job that nothing outside it changed. OK?» Record the answer, who gave it and the date in the connection note. No OK, no pen.dev: say what was found and stop.
4. **Make the job folder:** `mkdir -p <dir>/in <dir>/out`, then `git init <dir>`. A new, empty folder: never the home folder, the filesystem root, or a folder that already holds a project. Copy the owner's files in (`cp <file> <dir>/in/`) and commit them; the originals stay where they were. For a `.pen` that will be changed, make the work copy now: `cp <dir>/in/<name>.pen <dir>/out/<job>.pen`.
5. **Set the marker:** `touch <dir>/.job-start`, before the owner turns anything on.
6. **Route A, desktop app or IDE (default).** The owner opens `<dir>/out/<job>.pen` in pen.dev, turns on «Claude Code CLI» (or «Codex CLI») under Settings → MCP and restarts the client; pen.dev writes the `pencil` entry itself (read from docs.pen.dev, not tried). Then in a fresh session: `/mcp` lists `pencil` (read from docs.pen.dev, not tried); `read_skill()` loads pen.dev's own instructions (read from docs.pen.dev, not tried); `get_app_state()` names `<dir>/out/<job>.pen` (read from docs.pen.dev, not tried). Another document → ask the owner to open the right one; never edit.
7. **Route B, headless CLI.** The owner signs in on their own: `pen login` in their own terminal, or `PEN_CLI_KEY` set in their own environment. The agent only runs `pen status` and reads its exit code (exit 1 signed out: proven on CLI 0.3.14; exit 0 signed in: read from docs.pen.dev, not tried). Then `pen interactive --in <dir>/in/<name>.pen --out <dir>/out/<job>.pen`, the tool calls in the shell, `save()`, then `exit()` (read from docs.pen.dev, not tried). This route starts no second agent; treat a session as one agent day until proven otherwise.
8. **Write the connection note** (Artefacts) for the hand-over.

### After the job: the outside-change check

Run it after the last file is written, the document saved and closed in pen.dev, and the shell stopped.

1. `find <home> -newer <dir>/.job-start -type f -not -path '<dir>/*' > <dir>/outside-changes.txt`. On a busy machine the list is long and holds other programs' files; `find` ends with exit code 1 when some folders cannot be read, and the list is still usable.
2. Narrow it: `grep -i -E 'pen|pencil|mcp|<job>|\.(pen|png|jpe?g|webp|pdf|html|svg|fig)$' <dir>/outside-changes.txt`.
3. Explain every narrowed line. Expected and changed by pen.dev itself: the client's MCP configuration with the `pencil` entry (written when the owner turned the client on), pen.dev's own app files, and `~/.pencil/latest-preview.png` if previews were on (read from docs.pen.dev, not tried). A file of another program is named as such. Any other file this job may have written is a stray write: tell the owner at once with the path and time, and do not delete it without their OK.
4. Put the result in the hand-over note: the marker time, the size of the full list, the narrowed lines and what each one is, and «no file outside `<dir>` was written by this job» only when the check showed that. `outside-changes.txt` stays in `<dir>`, not in `<dir>/out`.

## The model

- One document is active at a time; its path and the selection come from `get_app_state()`. Every edit acts on that document, so it is checked first.
- `execute` takes a short JavaScript snippet and a `description` (a few words saying what the call does). Inside it, functions such as `Get(...)` read the node tree, insert and change nodes, `TakeScreenshot([...])` renders nodes for the agent to look at, and `Export(...)` writes image, PDF or HTML files. Load the exact functions and arguments with `read_skill({ path: "execute.md" })` before the first call; never guess them.
- A failed `execute` call answers with an `editId`: retry by sending `edits` with that `editId`, not by sending the whole snippet again.
- `get_style()` lists visual styles; `get_style({ name })` loads one. A style gives reference values for fonts, colours and imagery; it does not create variables.
- `browser` (desktop app only) opens a page in pen.dev's built-in browser, imports it or one element as layers, or returns a screenshot for the agent to look at.
- Saving: in the desktop app an existing file changes on disk only when it is saved; until then edits sit in a recovery backup, which is not history. Drafts made from the app's dashboard save on their own, outside `<dir>`: do not use them. In the headless shell, `save()` writes the `--out` file.

## Rules

- **Only inside `<dir>`.** Every path in a prompt, a call or an export is absolute and starts with `<dir>/`. The help's own example writes to a relative folder: never copy that. Nothing refuses a path outside, so this rule is the only fence.
- **Check the document before every edit:** `get_app_state()`, and the path and selection match the job. Write the path into the step log.
- **Never over the input.** `--out` is always a new file, never the `--in` file; the input's `sha256sum` is the same before and after.
- **Git is the history.** Commit in `<dir>` after each agreed step. The recovery backup does not replace it.
- **Look after every change:** `TakeScreenshot([<ids>])` inside `execute`, then look at the picture, before saying «done». Never read a full-size image into the conversation: at most 800 px on the long side.
- **Check every export twice:** the exit code, and that the file exists and is not empty. A failed export can print an error and still exit 0.
- **Set the export type.** On the CLI `--export-type` sets the format (png, jpeg, webp or pdf); the file name's extension does not.
- **CLI agent mode only on OK.** `pen --prompt …` (and `--agent`, `--model`, `--tasks`) starts pen.dev's own second agent, on the owner's model keys, and spends an agent day. Ask for each job, saying both. A `--tasks` file stops after the first task that succeeds: one command per task.
- **No extra agents.** Never start the MCP server with `spawn_agents`, and never run agents in parallel.
- **Agent days.** On Free, tell the owner when a job is about to start a new day of agent work.
- **Libraries are for good.** Turning a file into a `.lib.pen` library cannot be undone: only with the OK of the owner or the design system keeper.

## Recipes

`<job>` is the job's short name; `<id>` a node id from `Get(...)` or `get_app_state()`.

### P1. Open and check the document

1. Route A: the owner opens `<dir>/out/<job>.pen`; route B: the headless shell from Connect, step 7 (read from docs.pen.dev, not tried).
2. `read_skill()`, then the files it names for the task, at least `execute.md` and `pen-schema.md` (read from docs.pen.dev, not tried).
3. `get_app_state()`: the path is `<dir>/out/<job>.pen`, the selection is what the job expects (read from docs.pen.dev, not tried).
4. List the top-level nodes and the components with `Get(...)` inside `execute`, and write the ids into the step log (read from docs.pen.dev, not tried).

### P2. Screens, components and styles

1. When the owner wants a ready style: `get_style()`, then `get_style({ name })` (read from docs.pen.dev, not tried).
2. One `execute` call per change, with a `description` and the snippet; on failure, retry with `edits` and the `editId` (read from docs.pen.dev, not tried).
3. Components, instances, variables and themes as pen-files describes them; reuse a component before drawing a copy (read from docs.pen.dev, not tried).
4. `TakeScreenshot([<id>])` and look: layout, text, spacing, colours against the brief (read from docs.pen.dev, not tried).
5. Save: route A, the owner or the app saves the file (Cmd/Ctrl+S); route B, `save()`. Then `git -C <dir> commit -am "<step>"` (read from docs.pen.dev, not tried).

### P3. Images and PDF

1. `Export(...)` inside `execute` with the node ids, the format (png, jpeg, webp or pdf) and the absolute folder `<dir>/out`; take the exact arguments from `execute.md` (read from docs.pen.dev, not tried).
2. CLI alternative: the docs show `pen --in <file> --export <dir>/out/<name>.png --export-type png --export-scale 2` as an export, while the 0.3.14 help describes `--export` as an image of an agent run's result, with `--prompt` required. Without an account we could not tell which holds, so prefer step 1; a run with `--prompt` falls under the agent-mode rule (help text proven on CLI 0.3.14; the run read from docs.pen.dev, not tried).
3. `ls -l <dir>/out/<name>` (exists, not empty), `file <dir>/out/<name>` (the type agreed), then look at a small copy (read from docs.pen.dev, not tried).

### P4. Code from the design

1. HTML with Tailwind or with plain CSS is the only code pen.dev exports: `Export(...)` with HTML output, or the Code section of the properties panel in the app, which the owner uses (read from docs.pen.dev, not tried).
2. Open the HTML file in a browser the owner approves, or read it, and compare with a screenshot of the frame (read from docs.pen.dev, not tried).
3. React, Vue or other framework code only if the owner asks: it is written by an agent from the design, not exported. The note says «written by an agent from the design», and the code goes to the TypeScript developer, the react frontend developer or the vue frontend developer, by the project's stack.

### P5. Imports

1. Figma: a `.fig` file the owner gives, from `<dir>/in`, through the app's import (read from docs.pen.dev, not tried). Layers pasted from Figma come without their images: say so, or ask for the `.fig`.
2. Images: PNG, JPEG or SVG from `<dir>/in`; SVG becomes editable layers, PNG and JPEG become image layers (read from docs.pen.dev, not tried).
3. A web page (desktop app only): `browser` loads the page the owner names and imports it or one element as layers (read from docs.pen.dev, not tried). Its JavaScript does not come across, and fonts and effects need a check against the page. A signed-in page only after the owner says it shows nothing private.
4. `TakeScreenshot` of the imported frames and a side-by-side look with the source; list what did not come across (read from docs.pen.dev, not tried).

### P6. CLI agent mode (only on the owner's OK)

1. Tell the owner: this starts pen.dev's own second agent, on their model keys, and counts as an agent day. Wait for a yes for this job.
2. `pen --in <dir>/in/<name>.pen --out <dir>/out/<job>-v2.pen --repo <dir> --prompt "<the owner's request>"` (read from docs.pen.dev, not tried).
3. Check the exit code, that the output file exists, then open it and look at a screenshot (read from docs.pen.dev, not tried).

Not in these recipes: slides and presentations, hosted image generation, workspaces, shared libraries across a team.

## Look at the result

- Facts first: `get_app_state()` for the document and selection, `Get(...)` for nodes and components, `jq` on the saved `.pen` for reading only (pen-files).
- Then the eye: `TakeScreenshot` of each changed frame, and for exports a small copy of the file (at most 800 px).
- For written files: `ls -l`, `file`, `sha256sum`; `pdfinfo` for a PDF; for HTML, a look in a browser the owner approves.

## Going back

- Between steps, Git is the way back: `git -C <dir> log`, then `git -C <dir> checkout <commit> -- out/<job>.pen` and open it again in pen.dev.
- A wrong export is replaced under a new name, and the note says which file is current.
- In route A, close the document without saving to drop changes since the last save (read from docs.pen.dev, not tried); the recovery backup is not a history to go back to.

## Do not promise

- Folder limits: pen.dev cannot be kept to chosen folders; the only fence is this skill's route.
- React, Vue or other framework «exports»: only HTML with Tailwind or CSS is exported.
- Images in layers pasted from Figma, or JavaScript in an imported page.
- An imported page or Figma file matching its source exactly.
- A stable file format: pen.dev may change the `.pen` schema; pen-files reads the version every job.
- An export being good because the command ended without an error.
- A `--tasks` file running all its tasks.
- Taking back a share link's copies: revoking a link does not remove files already downloaded.
- Turning a library back into an ordinary file.
- More than one agent at a time on the Free plan, or agent work on more days than the plan allows.
- Any step marked «read from docs.pen.dev, not tried» working exactly as written.

## Never

- Bulk-export, scrape, crawl or extract datasets from pen.dev or its outputs: importing one page the owner gives is fine, a loop over many pages is not (pen.dev's EULA §3).
- Use pen.dev or its outputs to train or improve a model (pen.dev's EULA §3).
- Reverse-engineer, decompile or copy pen.dev, its CLI or its instructions; never ship or vendor the CLI.
- Make a share link, upload or send a file without the owner's word: anyone with a link can open and download the files.
- Ask for, read, keep or print the owner's password, session file, `PEN_CLI_KEY` or model keys; never put them in a prompt, a log or a note.
- Run `pen login` in any form, or pass it any flag; run `pen --version`.
- Write, edit or remove the `pencil` MCP entry; that is pen.dev's.
- Turn on `spawn_agents` or parallel agents; run CLI agent mode without the owner's OK for that job.
- Install or update pen.dev or its CLI unasked.
- Put real payment card, ID, health or children's data into a design: placeholders only.
- Import a file or page the owner did not give or has no rights to; import a signed-in page before the owner says it holds nothing private.
- Write over the input file, or edit `.pen` JSON by hand.
- Call code written by an agent an export.

## Checks before hand-over

- Every change was looked at on a screenshot; every output was opened again and looked at (deliverable-handoff steps).
- `get_app_state()` was checked before every edit, and the step log has the paths.
- The input files in `<dir>/in` are unchanged (`sha256sum` before and after); the output is a new file.
- `<dir>` is a Git repository with a commit per agreed step.
- No agent-mode run without the owner's OK in the note; no share link made.
- The `.pen` is saved and closed, the shell stopped, and the outside-change check ran and its result is in the note.

## Artefacts

- `<dir>/out/<job>.pen`, the agreed exports, `HANDOVER.md`, `SHA256SUMS.txt`; `<dir>/.job-start` and `<dir>/outside-changes.txt` next to them, outside `<dir>/out`.
- The connection note, five to ten lines: system; host (desktop app or IDE extension) and its version; CLI version if used; route A or B; «no folder limits: the owner's OK» with who and when; the job folder; `pencil` seen in `/mcp` or the `pen status` exit code; `get_app_state()` path; plan (Free, Pro or Ultra) as the owner says; the marker time; the date; which steps were read from the docs and not tried.

## Hand-over

- Files stay in `<dir>/out`; the owner sends, shares or publishes them. The note carries the connection note and the outside-change result.
- Visual decisions nobody has made go to the ui designer; tokens, variables synced with code and shared libraries to the design system keeper.
- Code from the design goes to the TypeScript developer, the react frontend developer or the vue frontend developer, by the project's stack, with the HTML export and screenshots.
- Work in FigCraft goes to the FigCraft operator; importing a `.fig` into pen.dev stays here.
- A stray write outside `<dir>`, a refused OK or a missing sign-in goes to the owner with what was found and what is proposed.

## Sources

This skill is made by harnsy, not an official pen.dev product. pen.dev is a product of High Agency, Inc.; no endorsement by High Agency, Inc. is implied.

Facts only, no text taken: the pen.dev documentation (https://docs.pen.dev/getting-started/installation, https://docs.pen.dev/getting-started/authentication, https://docs.pen.dev/getting-started/ai-integration, https://docs.pen.dev/for-developers/pen-cli, https://docs.pen.dev/core-concepts/pen-files, https://docs.pen.dev/core-concepts/import-and-export, https://docs.pen.dev/core-concepts/sharing, https://docs.pen.dev/core-concepts/ai-agents, https://docs.pen.dev/core-concepts/design-libraries, https://docs.pen.dev/design-and-code/design-to-code, https://docs.pen.dev/troubleshooting), the pricing page (https://www.pen.dev/pricing), the End User License Agreement (https://www.pen.dev/eula) and the Terms of Use (https://www.pen.dev/terms-of-use), all read 2026-10-31; © 2026 High Agency, Inc. Commands and answers marked «proven» come from our own trial of the CLI 0.3.14 without an account, 2026-10-31.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
