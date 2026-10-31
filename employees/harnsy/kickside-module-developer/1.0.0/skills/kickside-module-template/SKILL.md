---
name: kickside-module-template
description: Start and run a KickSide module from the official template - create the repository, make init once, read the layout, load it into a development copy as a workspace replacement, work files first with restarts only after Lua or registry changes, use Keeper's live tools on the development copy only with an expiring token, and port every live edit back into the module source with tests. Use when someone asks for a new module, when work on a module starts on a copy, or when a change made live has to become real.
---

# A KickSide module from the template, files first

A KickSide module is a Wippy package: a manifest (`wippy.yaml`), registry entries under `src/` and a separate test harness under `test/`. KickSide publishes an official module template (`kicksideai/module`) that already holds a working module: a table with migrations, a status endpoint, an access policy, an automation port, a Block, a web page and tests on SQLite and Postgres. This skill keeps one rule above the others: **the module's own git repository is the only source of its code.** The running copy is where you look and try; a change made there is a draft until it is in the files and tested.

**Route:** a task with acceptance criteria → **kickside-module-template** → kickside-module-capabilities and kickside-endpoints-access for the work → kickside-module-release.
Before this skill: the task, the owner's OK to create the repository, and a development copy that runs (the KickSide specialist sets one up when there is none). After it: a module that lints, tests green and loads in the development copy.

Marks: «(read from Sx, not tried)» means the step was read in that source and not run by us; the Sources section at the end names each Sx. Steps without a mark were run in our trial (S6).

## When to use

- A new module, for example a lead form, payments, backups or a module for one client.
- Work on an existing module begins on a development copy.
- Someone changed something live through Keeper (KickSide's built-in governance tools) and it has to become real.

## Inputs

- The module identity: Hub organization, module name (lowercase slug), title. The organization is the owner's.
- The development copy's folder and port. Never a client's copy, never someone else's running copy.
- The runtime build the copy really uses (`wippy version`).

## Steps

1. **Create the repository from the template.** Copy a checkout of `kicksideai/module` into a new folder and `git init` there, or use your git host's "use this template" feature (read from S2, not tried). Read `README.md`, `AGENTS.md` and `.kickside-module.json`.
   Check: `.kickside-module.json` says `"initialized": false`.
2. **Initialize once.** `make init ORG=<org> MODULE_NAME=<name> TITLE="<Title>"`; add `NAMESPACE=`, `TAG=` or the repository-owner variable the template's README names only when the defaults are wrong. It rewrites the template's identity across the checkout, and it refuses to re-initialize a checkout to a different identity.
   Check: `.kickside-module.json` says `"initialized": true` with your namespace, web component tag and route; `node scripts/check-module.mjs` prints that the module checks passed.
3. **Resolve and run the gates standalone.** `make setup` (resolves the module and the harness from the Hub and installs the UI packages; the UI install was not tried), then `make lint test`. On a shared machine, run heavy jobs through whatever queue that machine uses.
   Check: lint reports no issues, and the test run lists its suites and a case count with every case passing. A run that finds no tests fails on purpose: never "fix" that check.
4. **Learn the layout before you add to it.** One root `ns.definition` in `src/_index.yaml`; each folder with entries has its own `_index.yaml` and namespace: `api/` endpoints, `persist/` the SQL, `migrations/`, `security/` policies, `sink/` writable bindings, `blocks/`, `traits/` for agent tools, `ui/src` page source, `static/` the built page. Host resources (database, router, HTTP server, members group) come in through `ns.requirement` entries; the module never names an `app:*` resource itself.
   Check: you can say which namespace and which requirement each new entry will use.
5. **Find a real example first.** Before a new kind of entry, read a working one: the template, the handbook page for that surface, or an installed module on the development copy through Keeper's Hub tools (the installed-dependencies list with its entries) or its explore tool (read from S1, not tried).
   Check: your notes name the example you copied the shape from.
6. **Load it into the development copy.** In the copy's folder create an untracked `.wippy.workspace.yaml` that maps the module identity (`<org>/<name>`) to the checkout's path under `workspace.replacements`, and add the module's namespace to the managed-namespaces override as the handbook shows. Start the copy with `--config .wippy.workspace.yaml` and the same profiles and flags it always uses. The workspace file is never written to the lock or published (read from S1, not tried).
   Check: `wippy registry show <namespace>:definition --config .wippy.workspace.yaml` finds the module, and its page or status endpoint answers.
7. **Work files first.** Edit `src/`, run lint and tests, then restart the copy. A restart is needed after Lua or registry changes on disk, after adding or retargeting a replacement, after a profile or override change and after a runtime upgrade. A page rebuilt into an existing `static/` folder needs no restart: reload the browser (read from S1, not tried).
   Check: the copy answers with the new behaviour after the restart, not only the files.
8. **Keeper only on the development copy.** When live tools help (exploring installed modules, a live probe, running a migration, a test, an endpoint check, a screenshot), ask the owner's OK first. The handbook mints a Keeper MCP token with a call that names a preset, and its root preset gives full access (read from S1, not tried). Before you mint one, confirm on that copy's Keeper version how a token gets an expiry and how it is revoked; if it cannot be given an expiry or revoked, do not mint it and ask the owner. Use the token for the session only, revoke it when the work ends, never mint one on a client's copy and never write the token anywhere.
   Check: the report names the copy, the Keeper version, when the token was minted, and that it expired or was revoked.
9. **Port every live edit back.** A change pushed through Keeper lives in that copy's registry history only; it does not reach your checkout, and Keeper's sync to files writes an application layout, not a module layout (read from S1, not tried). Copy the accepted change into the module's `src/` by hand, run lint and both suites, restart from the checkout and check again.
   Check: `git diff` holds the change, tests are green, and the copy started from the files behaves as the live edit did.

## Rules (each with its check)

- **Initialize once, never rename by hand.** Check: `.kickside-module.json` and `check-module.mjs` agree on the identity.
- **The checkout is the source.** Check: nothing is "done" that exists only in a copy's registry history.
- **No module source inside the copy's own `src/`.** Pointing Keeper's file sync at a module tree creates a second copy of the same entries. Check: the copy loads the module only through the workspace replacement.
- **Never edit `wippy.lock` or a database by hand.** Check: every change came from the files, the runtime or the Hub tools.
- **Keeper tokens expire and are revoked.** Check: the token list on the copy shows none of yours alive after the work.
- **Never switch off or get around the Hub's module checks, and never show an unverified module as verified.** A module that is paid or has its own terms needs the owner's OK before you install it, also when you install it on the development copy only to study it. Check: no check was turned off, each module's status in the report is the one the platform shows, and any such OK is quoted.
- **Development copy holds made-up data only.** Check: no client export, dump or screenshot in the copy or the repository.
- **Never weaken a check to land a change.** Check: the Makefile, `check-module.mjs` and the tests are unchanged unless their own rule was wrong, and the report says why.

## Do not promise

- That a live edit is portable: it must be ported by hand.
- That Keeper's tool names and token calls are the same on every copy: they were read in the handbook (S1); confirm them on the copy's Keeper version first.
- That a restart is instant: wait for the copy to answer before you check.

## Hand-over

- **To the Lua developer (Wippy):** a supervised process or service, a message protocol between processes, a Lua dialect question, a runtime fault, or a Wippy app that is not a KickSide module.
- **To the KickSide specialist:** a development copy that has to be created, moved or repaired.
- **To the KickSide frontend developer:** the module's page in `ui/src`, with the endpoints it calls.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken. S1: the KickSide app and its developer handbook, pages on the dev loop, testing, layout and conventions (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI). S2: the KickSide module template (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy). S6: our own trial with Wippy 0.3.52a, 2026-10-23: make init, the two resolves inside make setup (the UI packages were not installed), make lint test and the module checks; the workspace replacement on a running copy and the Keeper steps were not tried there.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
