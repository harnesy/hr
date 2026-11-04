---
name: kickside-backup-restore
description: Back up a KickSide copy and prove the restore - the database, the registry history, the uploads and the lock for the SQLite or Postgres profile, the key file stored apart, encrypted offsite copies with retention, and a monthly restore drill onto a scratch copy with no outside network, with its proof. Use before the first client data, when setting a schedule, before any risky change, and when someone asks whether a copy can be recovered.
---

# KickSide backups that are proven by a restore

A KickSide copy is more than its database. The registry history records which modules are installed and their configuration (a module installed from the running app lands there, not in the lock); the uploads hold people's files; the key file signs tokens and protects stored secrets. Lose the history and the copy forgets its modules; lose the key and the data comes back unusable; keep the key in the same bucket as the data and a stolen backup opens everything. A backup nobody has restored is a hope. This skill makes it a fact.

**Route:** a running copy (kickside-docker-deploy) → **kickside-backup-restore** before the first client data, then on a schedule and before every rollout (kickside-release-rollout).
Before this skill: the owner's OK for the backup target and the schedule; the client's data stays on infrastructure the owner approves. After it: scheduled encrypted copies, the key stored apart, the latest drill's proof, and a report.

## When to use

- Before the first real data goes into a copy.
- Setting or changing the schedule, the target or the retention.
- Before a module rollout, an image update or a risky platform change.
- The monthly restore drill, and any real restore.

## Inputs

- The profile in use: SQLite (`./.wippy/` in the instance folder) or Postgres (a database plus the `/data` volume).
- The backup target the owner chose (an S3 bucket in the client's or owner's account) and its credentials, as files only the backup job reads.
- The owner's recovery targets: how much data may be lost (the schedule) and how long a restore may take.

## What to back up

| Piece | SQLite profile | Postgres profile |
|---|---|---|
| App data | `.wippy/app.db` with `sqlite3 <file> ".backup <copy>"` (safe while running) | `pg_dump -Fc` of the app database |
| Registry history | `.wippy/registry.db`, same command | the `wippy_registry` schema (in the same dump when the history DSN points at the app database; otherwise dump that database too) |
| Uploads and branding | `.wippy/uploads/`, `.wippy/branding/` | `/data/uploads/`, `/data/branding/` |
| Lock and module packs | `wippy.lock`, `.wippy/vendor/` | `/data/wippy.lock`, `/data/.wippy/vendor/` |
| Key file | `.wippy/.env` | `ENCRYPTION_KEY` from the env file or `/data/.env` |
| Workflow engine | none | the Temporal databases, only where Temporal is enabled |

Paths and commands in this table are read from S1, S2 and S9, not tried. The key goes to the owner's secret store, never into the data backup. The deployment files are already in git; env files with secrets go to the owner's secret store too.

If the `kickside/storage-s3` module is installed, processed originals and derived files live in its bucket and their local bytes are deleted. That bucket is then part of the copy: turn on its versioning and lifecycle rules with the owner, and treat it as data in the drill (read from S5, not tried).

## Steps

1. **Dump the database first, then copy the files.** Files copied after the dump are a superset of what the dump refers to: a restore may hold a few orphan files but never miss one. For Postgres stream the dump out of the database container: `docker compose exec -T db pg_dump -U <user> -Fc <database> > <dump-file>` (read from S9, not tried).
   Check: `pg_restore --list <dump-file>` reads it and lists the `wippy_registry` schema; for SQLite `sqlite3 <copy> "PRAGMA integrity_check"` prints `ok`.
2. **Record what the backup holds.** Next to each backup write a small manifest: time, image tag, registry version, the installed-module list, row counts of a few tables the KickSide module developer names, and the sha256 of three sample uploads.
   Check: the manifest exists and has every field.
3. **Encrypt and send offsite.** Use an encrypting backup tool such as restic with the bucket as its repository; its password lives in the owner's store, not on the same machine only. Keep, for example, 7 daily, 4 weekly and 6 monthly copies (`restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune`), and run `restic check` weekly (read from S17, not tried).
   Check: `restic snapshots` shows today's copy; the bucket holds no readable dump.
4. **Store the key apart.** The key was generated straight into a mode-600 env file (kickside-docker-deploy step 7); the owner copies it from there into the secret store once, labelled with the copy's name. You never print or read it back. Never in the backup bucket, the repository or a report.
   Check: the owner confirms the entry exists; a search of the bucket and the repository finds no key.
5. **Schedule it.** A systemd timer or cron job runs steps 1 to 3 at the time the owner chose, writes its result to a log, and the monitor alerts when the newest good copy is older than the schedule allows.
   Check: the timer is listed; one scheduled run has finished; on staging, a short alert threshold (for example one hour) and one skipped run fire the alert, and it clears after the next good run.
6. **Monthly restore drill on a scratch copy cut off from the outside.** A restored copy holds the client's connections, automations and schedules with live credentials: with network access it could send messages, charge cards or call webhooks for real. So the drill runs as a separate compose project on infrastructure the owner approved, the same image tag, every network `internal: true`, no published port. Restore the volumes, `pg_restore` into an empty database, have the owner supply the key from the store into the scratch copy's mode-600 env file, start (read from S1, S2 and S9, not tried).
   Check: health answers inside the scratch network; the registry version, the installed-module list, the row counts and the three sample checksums equal the manifest; the time from start to healthy is written down as the measured restore time.
7. **With the S3 module, protect the bucket during the drill.** A drill copy with an older database could treat newer objects as unowned and clean them up. Keep the drill copy off the network (step 6), or give it a read-only credential on a copy of the bucket, never the production credential (read from S5, not tried).
   Check: the drill's credential, if any, is read-only.
8. **Tear the drill down.** Remove the scratch project and its volumes; the owner's OK covers this deletion because it touches only the scratch copy.
   Check: `docker volume ls` shows no scratch volumes.
9. **A real restore.** Only with the owner's OK: stop the app, keep the current volumes aside under a new name (never delete them first), restore as in step 6 on the real networks, start, check, then tell the owner what was lost since the backup.
   Check: the same checks as the drill pass; the set-aside volumes stay until the owner says.
10. **Report.** Last good backup, the drill's date, result and measured restore time, retention, where the key is stored (by name, not value), what is left.
    Check: no key, password or token in the report.

## Rules (each with its check)

- **No client data before a drill has passed on that copy.** Check: the drill's proof predates the first real data.
- **The key never travels with the data.** Check: step 4.
- **The drill copy has no outside network.** Check: `docker network inspect` shows `internal: true` for every network of the scratch project.
- **Never restore over a running copy without the owner's OK, and never delete the current state first.** Check: the OK is quoted; the set-aside volumes exist.
- **Never edit the databases or the lock by hand.** Check: every change came from the runtime, the app or a restore of a whole backup.

## Pitfalls

- A plain file copy of a running SQLite database can be torn; use the backup command.
- Backing up only the lock loses every module installed from the running app.
- `storage-s3` moves files to S3; it is not a backup of the database or the key.
- Restoring with a different key: tokens signed with the old key stop working, and so does whatever else the key protects. Stop and find the right key; never generate a new one for a restored copy.

## Hand-over

- **To the KickSide module developer:** the code of a backup module the owner has, or a table that needs its own export.
- **To the Database engineer:** a dump or restore that is too slow or too large, and Postgres tuning.
- **To the owner:** a failed drill the same day, with what is at risk and the next step.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken: S1 the KickSide app (github.com/kicksideai/kickside, commit b7e0106: README on where data lives, `.wippy.yaml` profiles) and S2 its cloud deployment descriptor `app/src/deployment/_index.yaml` at the same commit (KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI); S5 the KickSide components repository (github.com/kicksideai/components, commit bc5e866: the S3 storage module's readme; same licence); S9 the PostgreSQL documentation (postgresql.org: pg_dump, pg_restore); S17 the restic documentation (restic.readthedocs.io: repositories, forget and prune, check). Not tried live by us: every step marked «not tried» was only read from the source named.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
