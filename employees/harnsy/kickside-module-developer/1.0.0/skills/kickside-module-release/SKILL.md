---
name: kickside-module-release
description: Release a KickSide module to the Hub and get it onto the next copy - lint, typecheck, build, both test suites, the release check with a publish dry run, a version the owner approves published as a private module, then the install on a staging or client copy through a Hub plan with a backup and a way back, done by the KickSide specialist; settings without code move by transfer. Use when a module is ready to ship, when a client needs a new version, or when a release fails.
---

# Release to the Hub, install on the next copy

A module reaches a client's copy one way: a published, immutable version on the Wippy Hub, installed through the copy's module page or Keeper's Hub plan, with a backup first. Nothing is copied into a client's folder by hand. This skill keeps one rule above the others: **the owner decides what is published and where it is installed; every gate runs before that question is asked.**

**Route:** a module that lints, tests and works live → **kickside-module-release** → the KickSide specialist installs it on staging, then on the client's copy.
Before this skill: acceptance met on the development copy, the Application security reviewer's answer for any public door. After it: a published version, its release notes, and an install handed over with its plan.

Marks: «(read from Sx, not tried)» means the step was read in that source and not run by us; the Sources section at the end names each Sx. No release check, publish or install of a module of ours was run.

## When to use

- A module is ready for its first release or a new version.
- A client needs a fix or a new feature that is already in the module.
- A release or an install failed.

## Inputs

- A clean checkout on the default branch (`git status` empty).
- The owner's Hub organization, and a Hub login made by the owner (`wippy auth login` keeps it outside the repository).
- The target copies: staging when there is one, then production.

## Steps

1. **Run every gate.** `make verify` (setup, module checks, lint, typecheck, build, UI tests, SQLite suite), then, for any change to data, the Postgres suite (`make test-pg`, with the database started by `make postgres-up` and stopped by `make postgres-down`) (`make verify` and the Postgres targets read from S2, not tried; lint and the SQLite suite ran in S6). On a shared machine, run heavy jobs through whatever queue that machine uses.
   Check: each target is green; the outputs with their case counts go in the report.
2. **Look at what ships.** `wippy.yaml` has no pinned release version, embeds the built page folder and excludes `test/`, local state, the root lock, `node_modules` and source maps. The rebuilt `static/` is committed when the page changed. A stored-shape change carries its forward-only migration, tested on both databases with data from the previous version.
   Check: `git diff --check` is clean; `static/index.js` and `wippy-meta.json` match `ui/`; `git status` shows nothing untracked that should ship.
3. **Dry run.** (Read from S1 and S2, not tried: no Hub login was made in our trial.) `wippy auth status` must show the owner's login; then `make release-check`, which runs the gates again and packs the module with `wippy publish --dry-run --create --module-visibility private` and the page folder embedded.
   Check: the dry run packs without error. Not logged in is a stop: ask the owner, never use someone else's token.
4. **Choose the version.** Semantic versions: a fix is a patch, a new feature a minor, a change that breaks callers or stored references a major. Published entry ids, requirements, endpoints, contracts and event types stay stable unless their callers migrate together. A published version can never be edited; a mistake is fixed by the next version.
   Check: the version and why are in the report.
5. **Publish only with the owner's OK.** (Read from S1 and S2, not tried.) Follow the module's own Makefile. The current template has no working `make publish`: that target only says releases go through the release workflow and stops with an error. The release workflow publishes: merge to the default branch, review the release pull request it opens (version, changelog, CI), merge it, and the workflow publishes with the Hub token the owner stored as a repository secret. An older checkout may still have a direct `make publish`; read its Makefile before you run it. Either way the module is private to the owner's organization unless the owner asks for public. A private-module quota can stop the publish; report it, do not switch to public.
   Check: the owner's OK is quoted; the Hub lists the version as private.
6. **Hand the install to the KickSide specialist.** (The Hub plan, backups and install were tried in the KickSide specialist's trial, S7; installing a module built from this template was not.) Give the module id, the version, the requirement values the copy must bind (database, authenticated router, public router, HTTP server, members group), the migrations it runs and what to check. The specialist backs up the lock, the registry history, the database and the key file, reads the plan, installs on staging first, then on the client's copy with the client's OK.
   Check: the hand-over lists every requirement and its value, and the way back.
7. **Check after the install.** With the specialist or the KickSide QA tester: the status endpoint, the page, a member and an outsider, existing data intact, and again after a restart.
   Check: the answers from the staging copy, then from production, are in the report.
8. **Settings without code move separately.** (Read from S1, not tried.) CRM schemas, workflows and agents built in the platform are not in the module; they move by the platform's transfer export and import or the CRM's configuration export, done by the specialist. Client data never moves; secrets are entered by the owner on each copy.
   Check: the report lists what moved by transfer and what the owner still has to enter.
9. **When it fails.** Read the failing gate's output first; fix the source, not the check. A failed install is the specialist's way back from the backups; then a new version.
   Check: the cause, the fix and the new version are on the item.

## Rules (each with its check)

- **No publish and no install without the owner's OK.** Check: the OK is quoted.
- **Private by default.** Check: visibility is private unless the owner asked otherwise in writing.
- **Never edit a lock or copy source into a client's copy.** Check: the install came from the Hub plan.
- **Staging before production when there is a staging copy.** Check: both sets of answers, in that order.
- **Backups before every install, with a tested way back.** Check: the specialist's backup list predates the install.
- **Hub tokens and secrets stay with the owner.** Check: none in the repository, CI logs, chat or reports.
- **Never switch off or get around the Hub's module checks, and never show an unverified module as verified.** A module that is paid or has its own terms needs the owner's OK before it is installed. Check: no check was turned off, each module's status in the report is the one the platform shows, and any such OK is quoted.

## Do not promise

- That a published version can be changed: it cannot.
- That `make publish` works the same in every checkout: follow the module's own Makefile.
- That transfer carries every kind of setting: check what it moved, piece by piece.

## Hand-over

- **To the KickSide specialist:** the install on staging and production, with the plan and the requirement values.
- **To the KickSide DevOps engineer:** server backups before the install, a staging copy, the Hub token on a server.
- **To the KickSide QA tester:** the acceptance run on the installed copy.
- **To the Release manager:** a release calendar across several modules, or the order in which modules ship together.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken. S1: the KickSide developer handbook pages on publishing, checklists and the dev loop (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI). S2: the KickSide module template, its Makefile and release workflow (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy). S4: the Wippy documentation page guides/publishing (wippy.ai, read 2026-10-23; MPL-2.0). S6: our own trial with Wippy 0.3.52a, 2026-10-23: lint and the SQLite suite ran, `wippy auth status` and the publish flags were read; no release check or publish was run, as no Hub login was made. S7: the KickSide specialist's trial on Wippy 0.3.51a with KickSide 0.2.18, 2026-10-21: a Hub module plan read and installed with backups and a diff.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
