---
name: app-connect-mcp
description: Find, install (only with the owner's OK), start and register a desktop app's MCP server so the agent can work in the app, confined to the project's read and write folders, then prove the link and write a connection note. Use at the start of any job in the app, or when the app is missing, too old or not answering. App facts come from the app's Connect table in its work skill.
---

# App connect over MCP

An app that ships an MCP server can be driven by an agent: open files, run its commands, look at the result. Getting there is a small chain of steps, and each one can go wrong quietly: an old build without folder limits, a download nobody checked, a server that can write anywhere in the home folder, a token left in a config file. This skill walks the chain in order and ends with proof that the link works and that it is fenced in.

Every app fact (program names, where the CLI is installed, start flags, the tools that prove the link, the first version with folder limits) comes from the app's Connect table in its work skill. This skill holds only the procedure.

**Route:** detect → decide with the owner → install (with OK) → choose headless or attach → start with folder limits → register → keep secrets out → prove → connection note. The note goes to the hand-over at the end of the job.

## When to use

- The first job in an app on this machine, or in this project.
- The app or its CLI is missing, older than the Connect table's minimum, or the MCP tools do not answer.
- The owner wants to watch the work in their own app window instead of a headless session.

## Inputs

- Two folders the owner names, as absolute paths: a read folder (the sources of the job) and a write folder for the outputs, inside the project. Both must exist.
- The harness the agent runs in: Claude Code or Codex.
- The app's Connect table: program and CLI names, CLI path per system, release page, start flags for headless and for attach, whether attach needs a token file, discovery and inspect tools, the first version with folder limits, the check commands.

## Rules

- **The owner's OK first** for every install, update or removal, for attaching to the owner's running app, and for replacing an MCP entry that already exists. Name the exact file, its source and where it goes.
- **Never run unconfined.** Start the server with both folder limits. If the installed CLI has no folder-limit flags, stop and ask for an update; do not work around it.
- **Never point a folder limit at the home folder or the filesystem root**, and never at a folder the job does not need.
- **Never write a token** on a command line, into an MCP config file, a log, the hand-over note or a chat message. Pass the path of a private token file only.
- **The apps' own launcher** (github.com/storytold/craft-launcher) is the owner's option: it installs system-wide and has no agent interface, so the agent never runs it.
- **Leave other MCP entries alone.** Edit only the entry for this app.

## Steps

1. **Detect.** Find the system and processor (`uname -sm`; on Windows, read the environment). Look for the CLI on the PATH and at the Connect table's install paths. If it is there, run `<cli> --version` and record the line.
2. **Decide.** If the CLI is missing or older than the table's minimum, tell the owner what you propose: the release asset, the release page it comes from, where it will be installed, and that it needs their OK. Wait for the answer. Mention the launcher as something the owner may choose to run instead.
3. **Install, with the OK.** Download the asset and the release's `SHA256SUMS.txt` into an empty folder. Check with `sha256sum -c --ignore-missing SHA256SUMS.txt` (on Windows, compare `Get-FileHash <file> -Algorithm SHA256` with the listed value). A mismatch stops the install, and the download is deleted. Install with the system's own package tool. Where the table says the CLI ships separately (for example as a zip on macOS), install it too; where it is not on the PATH, use its full path from now on. Run `<cli> --version` again and record it.
4. **Choose the backend.** Headless is the default: the app runs inside the MCP server with no window. Attach only when the owner wants to watch: the owner starts the app with its control port and the folder limits (and a token file where the table says so). The agent never restarts the owner's app.
5. **Start with folder limits.** Build the server command from the table: the read limit on the read folder, the write limit on the write folder, both absolute.
6. **Register.** Claude Code: `claude mcp add <server-name> -- <cli> mcp <flags>` (local scope, private to this project). A shared `.mcp.json` entry only when the owner asks for one; the owner then approves it in an interactive run. Codex: `codex mcp add <server-name> -- <cli> mcp <flags>`. If the name is taken, ask before replacing it.
7. **Keep secrets out.** A control token lives in a private file (mode 600, or a user-only ACL on Windows). Only its path appears in the command. Where the table says the app's control port has no token, attach only on a single-user machine and ask the owner to close the port when the job ends.
8. **Prove the link.** In a fresh session, check the entry: `claude mcp get <server-name>` must show it connected with both folder limits in its arguments (Codex: `codex mcp list`). Call the table's discovery tool with a narrow filter and its inspect tool; both must answer. Open one file inside the read folder. Try one write outside the write folder (for example a save into the parent of the write folder); it must be refused with a readable error. Close what you opened.
9. **Write the connection note** for the hand-over (below).

## Checks before hand-over

- The app and CLI versions are recorded.
- After an install, the checksum line ending in «OK» is kept in the note.
- The registered command carries both folder limits, and neither is the home folder or the root.
- No token value appears in any config, log or note (search for it).
- Discovery and inspect answered; the write outside the write folder was refused.

## Artefacts

- The connection note, five to eight lines: system, app and CLI versions, backend (headless or attach), read and write folders, harness and server name, the result of the prove step, date.

## Hand-over

- The connection note goes into the job's hand-over note.
- A problem the agent may not fix alone (no folder-limit flags, a failed checksum, a server name taken by something else, a port without a token on a shared machine) goes to the owner with what was found and what is proposed.

## Sources

Written from the apps' own public documentation and general practice, in our own words; facts only.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
