---
name: kickside-install-run
description: Install and run a KickSide copy on the Wippy runtime with the owner's OK - read the Hub install script before it runs, a fresh folder and a free port, bound to loopback, the admin's own password set at first boot (or the seeded default changed at once), a health check, a clean restart from the same folder and a clean stop. Use when someone asks to set up, start, restart or move a KickSide instance, or when a copy listens wider than it should or still has its seeded admin.
---

# Install and run KickSide

KickSide is a platform that runs on the Wippy runtime. One install is one folder: the lock, the app database, the registry history, the key file and the uploads all live there, and the runtime starts the platform from that folder. Most trouble at this stage is quiet: a copy that listens on every network interface, an admin account that still has the password everyone can read, a script that edits the person's shell files without asking. This skill starts private and narrow, and widens only when the owner says so.

**Route:** a request to set up or run KickSide → **kickside-install-run** → kickside-hub-modules for modules → kickside-build-on-platform for agents, automations, connections and users.
Before this skill: the owner's OK for the machine and the folder. After it: a running copy on a known folder and port, its admin password known only to the owner, and a report.

## When to use

- A new KickSide copy on a machine the owner names.
- A restart, a move to another port, or a stop.
- A copy that listens on all interfaces, or whose admin may still have the seeded password.

## Inputs

- The owner's answers: which machine, which folder, which port, local only or reachable from other machines, and the admin email.
- The machine's free memory, load and listening ports.

`<dir>` is the instance folder, `<port>` the port, `<wippy>` the path of the installed `wippy` binary. Local addresses are written as `127.0.0.1:<port>` and `localhost:<port>`.

## Steps

1. **Ask first.** Get the owner's OK for the machine, the folder, the port, «local only» or «reachable», and who the admin is.
   Check: the OK is quoted in your notes. Without it, stop here.
2. **Look at the machine.** Free memory, load, and `ss -ltn` for the port. A first boot downloads and unpacks several hundred megabytes of modules.
   Check: the port is free, and `<dir>` is empty or does not exist yet. A folder that already holds an instance is someone's data: pick another one.
3. **Read the installer before it runs.** Download the Hub install script to a file; never pipe it straight into a shell. Read it in full and tell the owner what it does: it places one binary in the Wippy home folder, writes an env file there, and adds a line to the person's shell start-up files unless `WIPPY_NO_MODIFY_PATH=1` is set; it checks no checksum or signature of the download; it needs no admin rights.
   Check: with the owner's OK, run it with `WIPPY_NO_MODIFY_PATH=1` unless the owner wants the shell files changed; `<wippy> version` prints a version; the shell files are unchanged when opted out.
4. **First boot: loopback and the admin's own password, kept out of the command line.** Put two lines in a file outside `<dir>` that only the owner can read (mode 600): `KICKSIDE_USERS_DEFAULT_ADMIN_EMAIL=<email>` and `KICKSIDE_USERS_DEFAULT_ADMIN_PASSWORD=<password>`. Load it into the shell that starts the copy (`set -a; . <file>; set +a`), then, in the empty `<dir>`:
   `<wippy> run kickside/kickside -c --profile quickstart --set vars.local_port=<port> --set vars.local_public_api_url=<full local address> -o app:gateway:addr=127.0.0.1:<port> > <private log> 2>&1`
   The full local address is `localhost:<port>` with the plain web scheme in front, as the profile's own default shows. These two values win over the profile's seeded admin, and they count only once, when a fresh folder boots for the first time; changing them later does not reset an existing account. They never appear on the command line, but the running process keeps them in its environment, and the first boot prints the admin's email and password into its log. So send that log to a file only the owner can read, and delete it, or cut the password out of it, once the boot is checked; never paste it into a report. Never type the password into the chat. The first boot resolves the platform from the Hub, writes `wippy.lock`, downloads the module packs, runs migrations and then starts; give it minutes, not seconds.
   Check: while it boots, `ps -eo args` shows no password; `curl -s 127.0.0.1:<port>/api/public/health` answers healthy; `ss -ltn` shows `127.0.0.1:<port>`, not `*:<port>`; signing in with the seeded default password is refused, both for the seeded admin email and for the owner's; signing in with the owner's password works and the account is an admin. Then delete the file with the two lines, or move it to the owner's password store.
5. **If the seeded default was used, change it before anything else.** The quick-start profile without the admin file from step 4 creates an admin with a seeded default password and prints it in the boot log, while the copy listens on every interface unless step 4's bind was given. Sign in and change the password at once (the user's own profile asks for the current password). Never write the default password's value anywhere; call it «the seeded default password from the boot log».
   Check: signing in with the default is refused; the old session is refused; signing in with the new password works. A password change ends every session of that account.
6. **Restart from the folder.** Stop, then start again in `<dir>` with the same profile, port and bind flags, without the platform name and in a shell without the admin file loaded: the lock and the registry history in the folder say what to run.
   Check: health answers again; `ss -ltn` still shows loopback; the restart is much faster than the first boot.
7. **Reachable from other machines only on purpose.** If the owner wants it, bind to the address the owner names, and hand TLS, the reverse proxy and the firewall to the DevOps engineer.
   Check: the owner's words are in the report; the copy is not left open on plain web without TLS.
8. **Stop clean.** Send SIGTERM to the process you started (check its executable path first) and wait for the port to close, not for a fixed time.
   Check: no process left for `<dir>`, the port is free.
9. **Report.** The runtime version, the folder, the port and the bind address, «admin password set by the owner» or «seeded default changed», and what is left (model provider key, TLS, backups on a schedule).
   Check: no password, token or key in the report.

## Rules (each with its check)

- **The owner's OK before install, before a bind beyond loopback, and before any change to the person's shell files.** Check: the OK is quoted.
- **No blind pipe to shell.** The script is read first and its effects told to the owner. Check: the script file was saved and read; its effects are in the report.
- **Loopback unless the owner says otherwise.** Check: `ss -ltn` shows `127.0.0.1:<port>`.
- **No seeded default password left.** Own password at first boot, or the default changed before any other step. Check: sign-in with the default is refused.
- **No password on the command line or in a kept log.** The first-boot password comes from an owner-only file, never from a flag; the first-boot log, which prints it, stays private and is deleted or cut. Check: `ps -eo args` during the boot shows no password; no log you keep or send holds it.
- **Never write the default password's value,** not in files, notes, reports or messages. Check: search your notes and report for it; nothing found.
- **The folder is the instance.** Never edit `wippy.lock`, `./.wippy/app.db`, `./.wippy/registry.db` or `./.wippy/.env` by hand, and keep them together. Check: you started and stopped the copy only with the runtime.
- **Never a person's running instance for trials.** A fresh folder and a free port. Check: the port was free before the start and belongs to your process after.
- **Not official, not resold.** Never present the work as KickSide's or Wippy's. KickSide's licence is source-available: running it for the owner, building the owner's product on it and building for a client who owns the instance are allowed; offering KickSide itself as a hosted or managed service, reselling it, white-labelling it or selling a fork needs a commercial licence from its publisher: do not do it, tell the owner. Check: no such claim or package in the deliverables.

## Do not promise

- That the installer verifies the download: it does not.
- An exact time for the first boot: it depends on the machine and the network.
- Production hosting, TLS, an outside database server or backups on a schedule: those go to the DevOps engineer.

## Hand-over

- **To the DevOps engineer:** a copy that must be reachable, with TLS, a proxy, an outside database server or scheduled backups.
- **To the Go developer:** a runtime crash or start-up fault, with the version line and the log lines around it.
- **To the owner:** the folder, the port, the bind address and what is left.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: the KickSide website (kickside.ai, read 2026-10-21; © 2026 Spiral Scout LLC d/b/a Wippy.AI), the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0) and the KickSide app (github.com/kicksideai/kickside, commit 82a65d5; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI); the Wippy documentation (github.com/wippyai/docs, commit b05b548; MPL-2.0) and the Wippy runtime (github.com/wippyai/runtime, commit 4137a00; MPL-2.0). Commands and checks from our own trial on Wippy 0.3.51a with KickSide 0.2.18, 2026-10-21.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
