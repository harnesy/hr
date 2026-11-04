---
name: safe-migration
description: Plan a schema or data change on a live database as a proposal; name the current state, the change, the expected effect and the way back, classify each operation by risk (long locks, table rewrites, large updates, columns that running code still reads), split risky work into small safe steps with an undo for each, rehearse on a copy, and apply to production only after the owner's OK. Use for any migration that will run against a database with real data or traffic.
---

# Safe migration

On a database that is in use, a migration that looks harmless can hold a lock that queues every other query behind it, rewrite a whole table, or remove something the running code still reads. This skill treats each migration as a change proposal: it finds the risky operations, rewrites them as a sequence of safe steps that the application survives at every point, rehearses them on a copy, and hands them to the owner to approve and apply.

**Route:** a needed change to tables or data → **safe-migration** → a proposal with steps, timings from the rehearsal and an undo per step → the owner approves → the steps are applied one deploy at a time → checks after each step.
Before this skill: what the data model must look like afterwards, and why. After it: an approved plan, migration files under review, and a log of each step applied.

## When to use

- Any migration that will run where there is real data or traffic: adding, removing, renaming or retyping columns and tables, adding indexes or constraints, moving or rewriting data.
- Data fixes and backfills, even when the schema does not change.

## Inputs

- The target shape of the data and the reason for it.
- The current schema, table sizes and row counts, and how busy the tables are (as the owner or monitoring shows them).
- The database engine and version, and how deploys run (does the code deploy before or after migrations; can several versions of the code run at once).
- A copy of the database, or a realistic subset, where rehearsal is allowed.

## Rules

- **Read-only on production by default.** Every change to live schema or data is a proposal: current state → change → expected effect → undo. It is applied only after the owner approves that change.
- Rehearse every step on a copy first and record how long it took and what it locked.
- The application must work at every step, with the old code and the new code, because deploys are not instant.
- Never remove or rename something that running code still reads. First change the code to stop using it, deploy, and only then remove it.
- Data backfills are separate from schema changes, run in batches, outside one long transaction, and can be stopped and resumed.
- Every migration has a way down, or says plainly that it cannot be undone and what the recovery is (for example, a restore from a backup taken just before).
- Set a short lock timeout and a longer statement timeout for migration runs, so a migration that cannot get its lock fails fast instead of blocking everyone. The values are the owner's choice.
- Per-database behaviour is stated as a dated fact from its source, never as «always instant» or «always safe».

## Risky operations and their safer form

| Operation | Why it is risky | Safer sequence |
|---|---|---|
| Removing a column | running code may still read or cache it | stop using it in code and deploy; then remove it in a later migration; then clean up the code |
| Renaming a column or table | old code breaks the moment the name changes | add the new one, write to both, backfill, move reads, stop writing the old one, remove it later |
| Changing a column's type | may rewrite the whole table under a lock | add a new column of the new type, backfill, move reads and writes, remove the old column later |
| Adding an index | a plain index build can block writes for its whole duration | build it with the engine's non-blocking option, outside a transaction |
| Adding a foreign key or check constraint | checking existing rows holds locks | add it without validating old rows, then validate in a separate step |
| Making an existing column required | the check scans the table under a lock | add an unvalidated check that the column is not empty, validate it, then make the column required |
| A default computed per row, or an expression default | may rewrite every row | add the column without that default, set it for new rows, backfill old rows in batches |
| Backfilling inside a schema migration | keeps the table locked for the whole update | a separate step, in batches, with pauses between them |

## Steps

1. **Describe the change** as a proposal: current state, target state, why, which code reads and writes the affected tables.
2. **Classify each operation** with the table above and the engine's own documentation. Mark each as safe, risky with a safer form, or irreversible.
3. **Split into steps.** Each step is one deploy or one migration: add what is new, backfill in batches, move reads, then remove the old thing in a later release. Write the undo for each step next to it.
4. **Write the migrations** in the project's style, one concern per file, each with its down path or an «irreversible» note. Keep data backfills in their own step.
5. **Rehearse on the copy:** run every step in order with the planned timeouts, time it, watch for locks and errors, run the application's tests against the result, then run the undo of each step and check that it works.
6. **Write the proposal** for the owner: steps, timings from the rehearsal, expected locks, the undo per step, the backup to take before irreversible steps, and how to tell that a step went well.
7. **Wait for the owner's OK,** step by step for anything risky.
8. **Apply one step at a time,** as the owner decides and through the project's normal deploy. After each step, check errors, slow queries and the data itself before the next.
9. **Close:** record what was applied, when and by whom, and any later step still due (for example, removing an old column next release).

## Checks before hand-over

- Each operation is classified, and every risky one has a safer form or a stated reason why not.
- Every step has an undo, or is marked irreversible with a backup and recovery plan.
- The plan was rehearsed on a copy, with timings and lock notes.
- Old and new code both work at every step.
- Nothing was applied to production without the owner's OK for that step.

## Artefacts

- `migrations/<date>-<name>-plan.md`: the proposal with steps, risks, rehearsal results and undo per step.
- The migration files and the code changes, as reviewable changes, one per step.
- `migrations/<date>-<name>-log.md`: what was applied, when, by whom, and checks after each step.

## Hand-over

- **To the database owner or database engineer:** the plan for approval, and the log.
- **To the reviewer:** the migration files and the code changes for each step.
- **To devops or the SRE:** the deploy order, the timeouts, and the backup before irreversible steps.
- **To the QA tester:** the test run against the rehearsed copy.

## Per stack

- **Ruby on Rails:** migrations are versioned files that run in order and are recorded in the database; a migration that the framework can reverse on its own may define one change method, otherwise it needs explicit up and down methods or an irreversible marker. The schema file in the repository shows the current shape after all migrations. Run and roll back a single step on the copy during rehearsal. Data changes go into their own migration or task, not into the schema change. For tables the running code reads, tell the model to ignore a column before the migration that removes it. The Strong Migrations gem checks migrations for many of the risky operations above, sets lock and statement timeouts, and can be set to make some operations safe by default.
- **PostgreSQL:** facts as of the Strong Migrations README dated 26 September 2026: create and drop indexes concurrently, outside a transaction; add foreign keys and check constraints without validation first and validate them separately; to make a column not null, add and validate a check constraint first. If a connection pooler runs in transaction mode, set the timeouts on the database user.
- **MySQL and MariaDB:** facts from the same README and date: do not force the table-copy algorithm, which blocks writes, or explicit shared or exclusive locks, which block writes or both reads and writes; leave the engine's default.
- **Other engines and frameworks:** look up each operation's locking behaviour in the engine's own documentation for the version in use, and write it into the plan with its source and date.

## Sources

Built on the Strong Migrations README (github.com/ankane/strong_migrations, commit 23d8e1f; © 2013 Bob Remeika and David Waller, 2015-2026 Andrew Kane; MIT licence), adapted.

Ideas only (no text taken): Ruby on Rails Guides, «Active Record Migrations» (github.com/rails/rails, commit 736156e; Rails Core Team and contributors, CC BY-SA 4.0).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
