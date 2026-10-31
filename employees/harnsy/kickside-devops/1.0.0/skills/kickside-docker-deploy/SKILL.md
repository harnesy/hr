---
name: kickside-docker-deploy
description: Build and run a KickSide copy in Docker for staging or production - the runtime binary checked by sha256, the Hub token only as a BuildKit secret, a non-root user, all state on volumes, the Postgres profile with the database on an internal network, the app published on 127.0.0.1 behind nginx with TLS and WebSocket upgrade, the first boot with the owner's own admin password and never the quickstart profile, then health through nginx and monitoring. Use when someone asks to deploy, move, rebuild or monitor a KickSide server.
---

# KickSide in Docker, behind nginx

A KickSide copy is the Wippy runtime plus a resolved set of modules plus its data. The app repository ships a multi-stage Dockerfile; the app's cloud deployment descriptor (`app/src/deployment/_index.yaml`) shows what a managed deployment adds around it. Read both before you write anything (S1, S2): the descriptor is the best fact source for which paths must live on a volume, which values are secrets and which network rules the publisher itself applies. Most trouble here is quiet: a token left in a layer, an env file that vanishes when the container is recreated, a port open to the internet because Docker's rules go around the host firewall.

**Route:** a request for a server copy → kickside-host-isolation → **kickside-docker-deploy** → kickside-backup-restore before the first client data → kickside-release-rollout for later changes.
Before this skill: the owner's OK for the server, the domain, the port and the certificate; the isolation probe passed. After it: a copy that answers through nginx on HTTPS, reviewed files in the deployment repository, and a report.

## When to use

- A new staging or production copy, or a move to another server.
- A rebuild on a new runtime or app version.
- Setting up health checks and monitoring for a copy.

## Inputs

- The owner's OK, quoted: the server, the public name, who provides the certificate, the backup target.
- The app commit or published app version to deploy, and the runtime version it needs.
- A Hub token that can read the private kickside modules (and any private modules the owner has), which the owner puts in a mode-600 file on the build machine, never in chat.

## Steps

1. **Read the sources first.** The Dockerfile, `.wippy.yaml` (profiles and vars), `app/src/app/env/` (where env values are read from), and the deployment descriptor. Note the runtime version each one names: they can differ, and the module set needs a floor version (read from S1 and S2).
   Check: your notes name the runtime version you will use and why.
2. **Pin the runtime by checksum.** The stock Dockerfile downloads the binary from the Hub and compares it with a sha256 read from the same Hub's release metadata. A sum fetched from the same place as the binary only proves the download is whole, so record the expected sha256 once from a reviewed source (the descriptor lists checksums and signatures for the runtime's public release binaries) and compare against that fixed value in the build (read from S1 and S2, not tried).
   Check: the build fails when you change one character of the expected sum on a scratch build.
3. **Build with the token as a BuildKit secret.** The kickside modules on the Hub are private, so the install stage needs a token. Pass it only as a secret mount: `DOCKER_BUILDKIT=1 docker build --platform linux/amd64 --secret id=wippy_token,src=<token-file> -t <registry>/kickside:<app-commit> .` The stock install stage logs in, resolves and logs out inside one step, so the token never lands in a layer. Never pass it as a build argument or an `ENV` (read from S1 and S8, not tried).
   Check: `docker history --no-trunc <image>` shows no token; `docker save <image> | grep -c -F -f <token-file>` prints 0 (it prints a count, never the token).
4. **Keep the image non-root and small.** The stock final stage runs as an unprivileged user with uid 10001 and declares `/data`. Keep both. Tag the image with the app commit and build it once; staging and production run the same tag (read from S1, not tried).
   Check: `docker run --rm --entrypoint id <image>` shows uid 10001.
5. **Put every piece of state on a volume.** The stock command only moves the instance data folder to `/data`; the lock, the installed module packs and the env file would stay in `/app` inside the container layer and vanish on recreation. Copy the descriptor's pattern in your own start script: working folder `/data`; copy the image's lock and module packs there on start; point the env file, the artifact folder and Keeper's file paths into `/data`; run with `--profile postgres` and `vars.instance_data_dir=/data`. Uploads then live in `/data/uploads` (read from S1 and S2, not tried).
   Check: recreate the container (`docker compose up -d --force-recreate`); the registry version, the installed-module list and a sample upload are unchanged.
6. **Postgres on an internal network.** Run the database image pinned by digest, its data on its own volume, attached only to a compose network with `internal: true`, no published port. The app reaches it by service name; give it the connection through environment values: host and port (`KICKSIDE_PG_HOST`, `KICKSIDE_PG_PORT`), the user and its password (`KICKSIDE_PG_USERNAME`, `KICKSIDE_PG_PASSWORD`) and the database name (`KICKSIDE_PG_DATABASE`). The registry history needs its own libpq DSN (`vars.postgres_history_dsn`, schema `wippy_registry` by default); the profile does not derive it (read from S1 and S2, not tried). Check where that DSN ends up on your copy: if the host's process list shows it with the password, tell the owner before anyone else gets access to that server. Tuning Postgres itself goes to the Database engineer.
   Check: `docker compose port db 5432` prints nothing; the app's log shows the Postgres history backend; `ps -eo args` on the host is reviewed for what it shows.
7. **Secrets and the key file, one way only.** Generate each secret straight into the env file, never on screen: create the file outside the repository with mode 600, owned by the service user, then append `ENCRYPTION_KEY=` with the output of `openssl rand -hex 32` in the same command, so the value is never printed or kept in shell history. The owner then copies the value from that file into the secret store; you never read it back. Tokens are signed with the key, so it must never change for the life of the copy (read from S1 and S2, not tried). The database password goes the same way; the runtime Hub token is put into the file by the owner.
   Check: `git status` shows no env file; `stat -c %a <env-file>` prints 600; the owner confirms the store entry by its label.
8. **Bind to loopback and put nginx in front.** Publish the app as `127.0.0.1:8085:8085`, never `8085:8085`: Docker's published ports bypass host firewall rules such as ufw (read from S8). nginx terminates TLS on 443, redirects 80, proxies to `127.0.0.1:8085`, passes `Host` and `X-Forwarded-Proto`, and upgrades WebSocket connections (the app serves one under `/api/v1/ws/join`) with `proxy_http_version 1.1`, the `Upgrade` and `Connection` headers and a read timeout longer than the default (read from S1 and S10, not tried). Set `PUBLIC_API_URL` to the HTTPS address users open. Set the request body limit with the owner for uploads. A TLS certificate or DNS change is the owner's decision.
   Check: `ss -ltn` shows `127.0.0.1:8085` and no `*:8085`; from another machine 8085 is refused and 443 answers; the browser's live updates work after a minute idle.
9. **First boot with the owner's admin, never quickstart.** The quickstart profile seeds a known admin and is for local trials only. For the first boot, the owner puts `KICKSIDE_USERS_DEFAULT_ADMIN_EMAIL` and `KICKSIDE_USERS_DEFAULT_ADMIN_PASSWORD` (the descriptor asks for at least 16 characters) into the owner-only env file; they count only on the first boot of an empty database. The first boot prints the admin credentials into the log, and `docker logs` keeps that log: once the boot is checked, remove the two values from the env file and have the owner change the password in the app, so the logged one is dead (read from S1 and S2, not tried).
   Check: sign-in with the logged password is refused; the owner's new one works; the env file no longer holds the two values.
10. **Health and monitoring.** The readiness route `/api/public/health` makes a round trip to the database (read from S1, not tried). The image has no curl, so check it from outside: through nginx on HTTPS every minute from an outside monitor, and from the host on `127.0.0.1:8085`. Also watch: certificate expiry (alert at 14 days), free disk on the data and database volumes (alert at 20%), container restarts, and the age of the last good backup and restore drill.
   Check: stop the database for a moment on staging; the monitor fires and clears.
11. **Report.** The image tag and runtime version, the server, the bind line from `ss`, the health answer through nginx, the probe result from kickside-host-isolation, and what is left (DNS, the first backup, the owner's model keys).
   Check: no password, token or key in the report.

## Rules (each with its check)

- **Owner's OK before a server, a port, DNS or TLS changes.** Check: the OK is quoted.
- **No secret in a layer, an argument or the repository.** Check: steps 3 and 7 pass.
- **Loopback bind, nginx alone faces the network.** Check: `ss -ltn` and an outside probe.
- **Never the quickstart profile or a seeded admin in production.** Check: the profile list in the start script; the seeded password refused.
- **All state on volumes.** Check: a forced recreate changes nothing.
- **One image tag per release, built once.** Check: staging and production run the same tag.
- **Not official, not resold.** Running KickSide for the owner or for a client who owns the instance is allowed; hosting it as a paid service, reselling, white-labelling or selling a fork needs a commercial licence from its publisher. Check: no such offer in the deliverables.

## Pitfalls

- The stock Dockerfile builds for amd64 only.
- The Hub token and the key sit in the container's environment. Treat the copy as untrusted toward its host: before the KickSide specialist adds users or roles, check on your copy what ordinary users' policies allow, tell the owner, and wait for the Application security reviewer's OK for that copy.
- Changing the bootstrap admin values after the first boot changes nothing.

## Hand-over

- **To the KickSide specialist:** modules, agents, users and settings once the copy answers; users and roles only after the Application security reviewer's OK for that copy.
- **To the Application security reviewer:** any port, outside address or credential scope beyond this skill's defaults.
- **To the Go developer:** a runtime crash, with the version line and the log.
- **To the Database engineer:** Postgres tuning, sizing and slow queries.
- **To the DevOps engineer:** CI pipelines and infrastructure that is not KickSide.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken: S1 the KickSide app (github.com/kicksideai/kickside, commit b7e0106: Dockerfile, `.wippy.yaml`, `app/src/app`, README) and S2 its cloud deployment descriptor `app/src/deployment/_index.yaml` at the same commit (KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI); S8 the Docker documentation (docs.docker.com: BuildKit secrets, port publishing and packet filtering); S10 the nginx documentation (nginx.org: proxying, WebSocket). Not tried live by us: every step marked «not tried» was only read from the source named.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
