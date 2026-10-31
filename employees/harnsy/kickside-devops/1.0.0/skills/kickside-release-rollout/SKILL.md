---
name: kickside-release-rollout
description: Move a published KickSide module version or a new image tag from staging to production - backup first, the Hub plan read, staging applied and accepted, the owner's go, production applied by the owner in System > Modules while you watch or through the Hub API with a short-lived scoped credential the owner revokes, the installed-module diff, and the way back named; the Hub's module checks never switched off; configuration without code moved by the transfer module. Use when a new module version is published, a client needs a module installed or updated, or a release must be rolled back.
---

# Published versions, staging first, production second

Modules are built in their own repositories and published to the Hub; a published release can never be edited, only followed by a new version (read from S3). A client's copy changes only by installing such a version, or by running a new image tag built once. This skill moves one of those through staging to production with a backup before each step and a way back named in advance. It never edits code on a copy: a fix is made on the development copy, published, and rolled out like any other version.

**Route:** the KickSide module developer publishes a version → **kickside-release-rollout** (staging) → the KickSide QA tester accepts → the owner's go → **kickside-release-rollout** (production).
Before this skill: a published version or a built image tag; backups working (kickside-backup-restore). After it: both copies on the same version, the diffs and checks, the way back, a report.

The Hub calls below (the version list, the installed list, the plan and the install) were tried as an admin on a scratch loopback copy in S7, Wippy 0.3.51a with KickSide 0.2.18; on a staging or production server they are not tried. Other calls carry their own mark.

## When to use

- A module version was published and a client should get it.
- A client needs a Hub module installed (the KickSide specialist chose it).
- A new runtime or app image tag must reach staging and production.
- Something broke after a rollout and the way back is needed.

## Inputs

- The module id and version (from the release, the Hub's version list or the KickSide module developer), or the image tag; its changelog and migrations.
- Staging and production addresses, and admin access for this window: either the owner applies the change in System > Modules while you watch, or the owner gives you a short-lived credential scoped to the module calls and revokes it afterwards.

## Steps

1. **Know exactly what moves.** For a module: the id, the version and what the release says about migrations. `GET /api/v1/keeper/hub/versions?module=<id>` lists a module's published versions, newest first (tried in S7). For an image: the tag and the commit it was built from.
   Check: the id, version or tag and its source are in your notes.
2. **Make staging look like production.** Same image tag, same profile, same installed modules. Save the installed-module list of both (System > Modules, or `GET /api/v1/keeper/hub/dependencies` as an admin; tried in S7) and diff them.
   Check: the two lists are equal, or the differences are explained before you go on.
3. **Back up staging.** Run kickside-backup-restore steps 1 to 3 on staging.
   Check: the manifest is newer than any change on staging.
4. **Read the plan on staging.** Ask for the plan (System > Modules, or `POST /api/v1/keeper/hub/dependencies/plan` with the module and its version range; tried in S7 with a module id, the version range is read from S3, not tried). Read every module it pulls in, every host requirement with its default, every migration, and each module's verification status as the platform shows it. Where the copy already binds a requirement on purpose, bind it the same way.
   Check: the plan says it can be applied; every kept default is one you chose; a plan that pulls in modules nobody asked for goes to the KickSide specialist first.
5. **Apply on staging, then check twice.** Apply the plan as read (`POST /api/v1/keeper/hub/dependencies/install`, or the page; tried in S7). Diff the installed list; check the feature; restart the copy; check again.
   Check: the list changed only by the planned modules; health answers through nginx before and after the restart.
6. **Acceptance and the owner's go.** Hand staging to the KickSide QA tester with the version and what changed. When the KickSide QA tester accepts, ask the owner for production in one line: version, what changes, the way back and its time.
   Check: the KickSide QA tester's verdict and the owner's go are quoted.
7. **Back up production, then read its plan.** Fresh backup with its manifest. Ask production for the same plan and compare it with staging's.
   Check: the plans match; if they differ, stop and find out why.
8. **Apply on production without development tools.** No full-access Keeper credential is ever created on production (team rule S11): Keeper work belongs on the development copy. The owner applies the plan in System > Modules while you watch, or you apply it through the Hub API with the short-lived scoped credential the owner gave you for this window, and the owner revokes it afterwards. Diff the installed list, check health through nginx, restart, check again, and ask the KickSide QA tester for a short check.
   Check: the diff equals staging's; the credential is revoked; the KickSide QA tester's short check is quoted.
9. **Name the way back before you need it.** If an install fails, compare the installed list with the saved one; if they differ, the way back is the pre-change backup. After a successful install, an older version is not the way back when migrations ran, because there is no tested way back to older data except a restore (read from S3): the way back is the pre-change backup, restored with the owner's OK (kickside-backup-restore step 9). A new module that must go is removed with `POST /api/v1/keeper/hub/dependencies/uninstall`, choosing `leave` (keeps its tables) or `down` (undoes migrations where it can); in S7 `leave` worked, the first call can be refused while other modules depend on it, and `down` failed with a server error, so prefer `leave` and say which data stays.
   Check: the change note names the way back and its expected time.
10. **New image tags follow the same path.** Staging first with the new tag, the same checks, the KickSide QA tester, the owner's go, production. The way back is the previous tag, plus the backup when the start ran migrations.
    Check: both copies report the same tag; the previous tag is still in the registry.
11. **Configuration without code.** CRM schemas, workflows and similar settings move with the `kickside/transfer` module (export and import of a user's own components and their data) or the CRM's own configuration export and import (read from S4, not tried). The KickSide specialist does the move; you take a backup first and confirm on staging what the transfer really carried.
    Check: the backup predates the import; staging shows the moved pieces.
12. **Report.** Versions on staging and production, the plan summary, the diffs, the checks, the KickSide QA tester's and the owner's words, the way back.
    Check: no tokens, keys or session values in the report.

## Rules (each with its check)

- **Backup first, every copy, every time.** Check: manifests predate both applies.
- **Staging before production, same version, same plan.** Check: step 7's comparison.
- **Never `wippy update` on production,** and never Update all without reading the plan, staging and the owner's go: both can move every module. Check: the commands run are listed.
- **No full-access Keeper credential near production.** Check: production's credential list holds none.
- **Only published versions and reviewed image tags.** No source copied into a copy, no hand edits of the lock or the databases. Check: every change came from the Hub or an image tag.
- **Never switch off or get around the Hub's module checks, and never show an unverified module as verified.** Check: no check was turned off, and each module's status in the report is the one the platform shows.
- **A module that is paid or has its own terms needs the owner's OK before you install it.** Check: the OK is quoted in the report.
- **The owner's go before production.** Check: it is quoted.

## Pitfalls

- A production copy needs a Hub token that can read the owner's private modules, and it sits in the copy's environment: check on your copy what ordinary users' policies allow and tell the owner before the KickSide specialist adds users.
- A plan that looks the same can bind different defaults when production was configured differently; compare, do not assume.
- A rollback by older version on a migrated database can break data; restore instead.

## Hand-over

- **To the KickSide module developer:** a version that fails on staging, with the plan, the log and the steps.
- **To the KickSide specialist:** module choice, configuration moves, users and settings.
- **To the KickSide QA tester:** acceptance on staging and the short check on production.
- **To the Application security reviewer:** a plan that opens files, the network, secrets or people's data.
- **To the Release manager:** the release calendar across several modules and clients.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken: S3 the KickSide developer handbook in the app (github.com/kicksideai/kickside, commit b7e0106, `app/src/app/docs/kickside-development`: publishing, Hub install and update, migrations; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI); S4 the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0: module list, transfer). S7: Hub calls from our own trial on a scratch loopback copy, Wippy 0.3.51a with KickSide 0.2.18, 2026-10-21. S11: team rule. Not tried live by us: every step marked «not tried» was only read from the source named.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
