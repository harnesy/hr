---
name: kickside-hub-modules
description: Add, update or remove KickSide modules from the Hub catalog without losing the way back - the module named from the catalog or its readme, never guessed; a backup of wippy.lock, the registry history, the app database and the key file first; the install plan read before it is applied; the installed-module list diffed before and after; the new feature checked live and again after a restart. Use when someone asks for a module, an update of the platform or a module, or a removal, or when the installed modules do not match what the lock says.
---

# KickSide modules from the Hub

KickSide is built from modules. The app's module page (System → Modules) shows the Hub catalog, builds a plan for the module you pick and applies it to the running platform, migrations included. One fact shapes this whole skill: **a module installed from the running app does not change `wippy.lock`.** The new resolved set of modules goes into the registry history in `./.wippy/registry.db`, and the next start replays it. So a copy of the lock alone is not a backup, and a lock diff alone shows nothing.

**Route:** a request for a module → **kickside-hub-modules** → kickside-build-on-platform to use it.
Before this skill: a running copy (kickside-install-run) and the owner's OK for the change. After it: the module installed or removed on purpose, the backups, the diff and two live checks in the report.

## When to use

- Adding a module from the Hub catalog.
- Updating one module, or the whole platform.
- Removing a module.
- A copy whose modules do not match what someone expects.

## Inputs

- The module's exact id from the catalog page, its catalog entry or its readme, and what it needs from the host.
- The instance folder `<dir>` and its port.

## Steps

Our trial ran these steps through the calls each step names, as an admin signed in to the copy, not by clicking the pages; the pages are the same actions for a person.

1. **Name the module from a source.** Take the id from the catalog page, the module's readme or the docs (wippy-docs for Wippy facts). Never guess a module name or a setting.
   Check: the id and its source are in your notes.
2. **List what is installed now.** Save the installed-module list from the module page, or the list call behind it (`GET /api/v1/keeper/hub/dependencies` as an admin): one row per module the app declares, with its installed version; modules pulled in underneath them show only in the resolved set (step 6).
   Check: the list is saved to a file, one `module version` line each, with its count.
3. **Back up four things.** `wippy.lock`; `./.wippy/registry.db` and `./.wippy/app.db` with the database's own backup command (`sqlite3 <file> ".backup <copy>"`, which also works while the copy runs), not a plain file copy of a live database; and the key file `./.wippy/.env`. Keep the copies in a folder outside `<dir>` that only the owner can open: the key file is a secret, and the backup command makes copies that others could read.
   Check: four files exist with their sizes; the way back is written down (step 10).
4. **Read the plan.** Ask for the plan (the module page, or `POST /api/v1/keeper/hub/dependencies/plan` with the module id). Read every module it pulls in, every host requirement with its default value, and the migrations. Where the person's app already binds a requirement to a resource on purpose (a router, a database, a user scope), bind it the same way instead of taking the default.
   Check: the plan says it can be applied, with nothing missing; every default you keep is one you chose.
5. **Apply with the owner's OK.** Apply the plan as it was read.
   Check: the answer reports validation, governance, migrations and boot steps as passed.
6. **Diff the installed list.** Save the list again and compare it with step 2. For a deeper look, the resolved module set of each registry version can be read from `registry.db` (a copy, not the live file) and compared.
   Check: the list gains only the module you named, and the resolved set only that module and the new modules its plan listed. Anything else stops the work: take the way back (step 10) and report.
7. **Check the feature now, and after a restart.** Open the page or call the endpoint the module adds; restart the copy from `<dir>` with the same flags; check again.
   Check: both answers are in the report.
8. **Update only with a plan, backups and the owner's OK.** First see whether there is anything to update: `GET /api/v1/keeper/hub/versions?module=<id>` lists a module's published versions, newest first; compare the newest with the installed one. If an update is due: back up (step 3) first, read the plan before it is applied, and run `wippy update` on the command line only with the owner's OK, because it re-solves every module and may move all of them. Our trial found no newer version on a fresh copy, so the update itself is not a tried recipe here.
   Check: the owner's OK is quoted, the backups predate the update, and the version diff of the installed list is in the report.
9. **Remove with care.** First find what uses the module (workflows, agents, automations, connections, other modules) and back up (step 3). Then, with the owner's OK, ask for the removal: `POST /api/v1/keeper/hub/dependencies/uninstall` with `{"component": "<id>"}`. A module that ran migrations is refused the first time, and the refusal lists what would go: its entries, who requires it (`required_by` must be empty) and its migrations. Choose what happens to its tables by sending the call again with `"migration_policy"`: `down` undoes the migrations and fails when one of them has no way back (nothing is changed then), `leave` removes the module and keeps its tables and data in the app database.
   Check: the call succeeds; the diff of the installed list shows only that module gone; its pages and calls no longer answer; after a restart from `<dir>` it is still gone; the report says which policy was used and what data stayed.
10. **The way back.** Stop the copy; put the four backed-up files back in their places (`wippy.lock`, `./.wippy/registry.db`, `./.wippy/app.db`, `./.wippy/.env`), owner-only; start it again from `<dir>` with the same flags.
   Check: the installed list matches the list saved before the change, and the module's calls no longer answer.

## Rules (each with its check)

- **Back up before any module change:** lock, registry history, app database and key file, with the database's backup command. Check: four files with sizes, taken after the last change and before this one.
- **Plan, read, apply.** Never apply a plan you did not read. Check: requirements and defaults are listed in your notes.
- **Diff after.** Expect only the named module and its listed dependencies. Check: the diff is in the report.
- **No `wippy update` without the owner's OK and the backups.** Check: the OK is quoted and step 3 ran first.
- **Choose the removal policy on purpose.** `leave` keeps the module's data, `down` deletes it where it can. Check: the policy and the data left are in the report.
- **Never invent module names or settings.** Check: each id in the report has its source.
- **Install only what the owner named or the catalog lists.** The catalog has no signed packages yet; a module from elsewhere installs and shows as unverified. Check: no unverified module without the owner's written OK.
- **Never switch off or get around the Hub's module checks, and never show an unverified module as verified.** Check: no check was turned off, and each module's status in the report is the one the platform shows.
- **A module that is paid or has its own terms needs the owner's OK before you install it.** Check: the OK is quoted in the report.
- **Never edit the lock or the databases by hand.** Check: every change came from the module page, its calls or the runtime.

## Do not promise

- Signed or verified modules: not there yet.
- That a removal is clean when other parts still use the module.
- That a removal deletes the module's data: with `leave` its tables stay, and `down` works only where every migration has a way back.
- That a full update keeps every module at its version: it may move all of them.

## Hand-over

- **To the Lua developer (Wippy):** a module that does not exist yet, a fix inside a module's code, or a new module.
- **To the API integration engineer:** a connection provider for an outside service that misbehaves or is missing.
- **To the Application security reviewer:** a module whose plan opens files, the network, secrets or people's data, before you apply it.
- **To the Go developer:** a resolver or loader fault in the runtime, with the version line, the plan and the log.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: the KickSide website (kickside.ai, read 2026-10-21; © 2026 Spiral Scout LLC d/b/a Wippy.AI), the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0) and the KickSide app (github.com/kicksideai/kickside, commit 82a65d5; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI); the Wippy documentation (github.com/wippyai/docs, commit b05b548; MPL-2.0) and the Wippy runtime (github.com/wippyai/runtime, commit 4137a00; MPL-2.0). Commands and checks from our own trial on Wippy 0.3.51a with KickSide 0.2.18, 2026-10-21.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
