---
name: kickside-acceptance
description: Plan, run and report acceptance of a KickSide module - each acceptance criterion from the KickSide analyst turned into a check with role, copy and expected answer; a release checked on a staging copy as the client gets it (installed list saved, backup, the Hub plan read, the install's step answers read, smoke per role, restart, rollback drill); a short acceptance report and one bug report per fault. Use when a module or setup is ready for acceptance, when a new module version must be checked before the client's copy gets it, or when the KickSide analyst needs a report for the client.
---

# Acceptance of a KickSide module

A client module is usually built in its own git repository from the module template, run in a dev copy with fake data, published to the Hub as released versions, and installed on a staging copy and then on the client's copy. The developers' own tests (`make verify`, and `make test-pg` when data changed) prove the module in isolation. Acceptance proves it in an assembled copy, as each role, after a restart, and through the same install the client's copy will get. This skill opens and closes every acceptance item: the plan before testing, the release drill, and the report.

**Route:** an acceptance item → **kickside-acceptance** (plan) → kickside-role-checks, kickside-browser-checks, kickside-module-probes → **kickside-acceptance** (release drill, report) → the KickSide analyst.
Before this skill: the KickSide analyst's acceptance criteria, the module and its version, the copy you may use and the owner's OK for it. After it: a report the KickSide analyst can hand to the client and bug reports with the developers.

## When to use

- A module or a setup is declared ready.
- A new module version must be checked before the client's copy installs it.
- The KickSide analyst needs an acceptance report with screenshots.

## Inputs

- The acceptance criteria, numbered, from the KickSide analyst.
- The module id (`organization/module`) and the version under test.
- The copy: the dev copy (module loaded from its checkout as a workspace replacement) or a staging copy (module installed from the Hub). Its folder `<dir>`, its address in `$BASE`, and how it is started.
- The roles the client will use, and which groups each has.

## Steps

1. **Read the criteria; ask before you guess.** Number each criterion. A criterion that names no role, no data or no visible result goes back to the KickSide analyst with a question.
   Check: every criterion has a role, a starting state and an expected answer, or an open question on the item.
2. **Write the test plan on the item.** One row per check: criterion, role, copy, how (API, page, restart, release), expected answer. Add the checks every module gets even when nobody wrote them: one refused action per role, the record boundary between two members, a restart, leaving the page and coming back, and the console of every screen.
   Check: the plan names what is out of scope and why.
3. **Entry conditions.** Ask the KickSide module developer for the green output of `make verify` (the template's gate: setup, lint, typecheck, build, module checks, UI unit tests and the SQLite suite) and, when data or migrations changed, of `make test-pg` against the template's test Postgres (targets read from S3's Makefile); do not run or edit their suites yourself. Then check the copy: `curl -s "$BASE/api/public/health"` answers healthy (tried in S4); on the dev copy, `wippy registry show <namespace>:definition --config .wippy.workspace.yaml` in `<dir>` shows the module loaded from the checkout (read from S2, not tried); on staging, the installed list (step 5) shows the version under test.
   Check: the version line of the runtime (`wippy version`) and the module version are in your notes.
4. **Run the checks.** Access with kickside-role-checks, screens with kickside-browser-checks, the lead form, payments and backups with kickside-module-probes. Record each result against its plan row as pass, fail or not tested with the reason.
   Check: no plan row is left empty.
5. **Release check on staging, with the owner's OK.** The staging copy comes from the KickSide DevOps engineer and mirrors the client's copy: same modules, same versions, fake data. The list, backup, plan and install calls below are the ones tried in S4; the drill as a whole is not tried yet.
   - Save the installed list: System > Modules, or `GET /api/v1/keeper/hub/dependencies` as the admin (tried in S4). One `module version` line each, with the count.
   - Take the backup before anything changes. On a SQLite copy: `wippy.lock`, `.wippy/registry.db` and `.wippy/app.db` through `sqlite3 <file> ".backup <copy>"`, and the key file `.wippy/.env`, into a folder outside `<dir>` that only the owner can open (tried in S4). On a PostgreSQL copy, the KickSide DevOps engineer takes the database dump (not tried); you still keep the lock, the registry history and the key file.
   - Count what must survive: rows the client cares about (leads, orders, users), by API or page. Write the numbers down.
   - Read the plan: System > Modules, or `POST /api/v1/keeper/hub/dependencies/plan` with the module id (tried in S4). Read every module it pulls in, every requirement and its value, every migration. A missing requirement stops the drill and goes to the KickSide specialist.
   - Never switch off or get around the Hub's module checks, and never show an unverified module as verified. A module that is paid or has its own terms needs the owner's OK before you install it.
   - Apply as read. Read the steps in the answer: validation, governance, migrations and boot reported as passed (tried in S4). Any step that did not pass is a stop: change nothing more, and send the answer to the KickSide DevOps engineer and the KickSide module developer.
   - Diff the installed list: only the module under test moved, plus the modules its plan named.
   - Smoke: the release subset of the plan, as each role, and the counts again.
   - Restart from `<dir>` with the same flags; smoke again.
   - Rollback drill (the way back read from S4's steps, not tried as a drill): stop the copy, put the backed-up files back (or have the KickSide DevOps engineer restore the dump), start it, and check that the installed list equals the saved one, the old version answers, and the counts equal the ones taken before the backup.
   Check: the backup predates the install; both smoke runs and the drill are in the evidence.
6. **Write one bug report per fault.** Title that says what fails and where; numbered steps from a clean start; expected; actual; module version, copy, role, browser; evidence (screenshot names, console lines, the API answer with tokens cut out). Severity is the harm to the client; priority is the order of fixing. Send it to the KickSide module developer (logic, API, migrations) or the KickSide frontend developer (screens), through the item.
   Check: another person can reproduce it from the report alone.
7. **Write the acceptance report for the KickSide analyst.** Plain words; the client reads it. Use this shape:
   - **Verdict:** go or no-go, in one sentence, with the counts (criteria passed, failed, not tested).
   - **What was checked:** each criterion, in the client's words, with pass or fail.
   - **How:** the copy (dev or staging, never the client's), the module version, the roles used, the browser, and that the copy was restarted.
   - **Evidence:** screenshot names next to each criterion; the release drill's before and after lists and counts.
   - **Left:** what was not tested and why, open bugs with their severity, open risks the Application security reviewer named for this copy.
   Check: no token, password, key or real person's data in the report or its screenshots.
8. **Retest.** A fix is retested on the version that contains it, with the checks around it, and the report gets a new date.
   Check: the retest names the version.

## Rules (each with its check)

- **Never the client's production copy, real customers' data, live payment keys or real money.** Check: the report names the copy, and it is dev or staging.
- **The owner's OK before installing, rolling back or creating anything on a copy.** Check: the OK is quoted.
- **Never switch off or get around the Hub's module checks**, and never show an unverified module as verified; a module that is paid or has its own terms needs the owner's OK before you install it. Check: no check turned off; each module's status in the report is the one the platform shows.
- **Backup before every install, and a drill that proves the way back.** Check: the old version and the old counts answered after the restore.
- **Plan read before it is applied.** Check: the modules, requirements and migrations it listed are in your notes.
- **The developers' suites are theirs.** Check: you asked for their green run and changed none of their files.
- **Recommend, do not decide.** Check: the report says go or no-go; the decision is the KickSide analyst's and the client's.
- **No secrets in any artefact.** Check: search the report, the bug reports and the screenshots for tokens and passwords; nothing found.

## Do not promise

- That a rollback keeps data written after the backup: there is no tested way back to older data except a restore (removing a module with the `down` policy undoes its migrations only where each one has a way back, and that is not a release rollback), and what was written after the backup is gone. Say so in the report.
- That a passing staging copy proves the client's copy: it proves the same version and the same steps; the client's own data and settings are checked by the KickSide specialist after the install.
- A compliance certificate for the module or the platform.

## Hand-over

- **To the KickSide analyst:** the acceptance report; criteria that are unclear or missing.
- **To the KickSide module developer:** logic, API, permission and migration faults, as bug reports.
- **To the KickSide frontend developer:** screen faults, with screenshots and console lines.
- **To the KickSide specialist:** a plan with missing requirements; the install on the client's copy.
- **To the KickSide DevOps engineer:** staging copies, database dumps and restores, server faults.
- **To the Application security reviewer:** any security finding, at once.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: S1 the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0), S2 the KickSide app and its developer handbook (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI), S3 the KickSide module template (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy: its Makefile targets). S4: the health check, installed list, backups, Hub plan and install calls as tried in the KickSide specialist's trial on Wippy 0.3.51a with KickSide 0.2.18. Every other step is marked inline where it was read and not tried.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
