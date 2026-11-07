---
name: buggregator-setup
description: Install and start a local Buggregator server with the owner's OK - install script, single binary or Docker, every port and what listens on it, binding to 127.0.0.1, in-memory or persistent storage, projects, the version check and the connection note. Use before any other Buggregator skill, and when the owner asks how to run it.
---

# Buggregator setup

Buggregator is a free, self-hosted debugging server for local development. One program takes in what an app sends while it runs: Sentry errors, Ray and VarDumper dumps, Monolog logs, mail sent over SMTP, Inspector traces, XHProf profiles, HTTP requests and SMS. It shows them in a web UI and, when the owner turns it on, offers them to an AI agent over MCP. It is built for a developer's own machine, not for production.

Two facts shape this skill. First, the program listens on every network interface unless told otherwise, and its HTTP proxy on port 8080 is always on and decrypts HTTPS: on a laptop in a café or a shared server, anyone who can reach the ports can read or add events and use the proxy. So every start here pins each address to `127.0.0.1`. Second, its default database lives in memory: a restart wipes every event, which is often what a developer wants and sometimes a surprise.

Status, in one line for the owner: «Runs on your machine under your account; I start it only with your OK and keep every port on 127.0.0.1.»

How far each step is proven: commands and defaults here come from the Buggregator docs and the server code at release v2.7.0 (sources at the end). We have not run every command ourselves; say so when a step matters and has failed once.

**Addresses.** Buggregator speaks plain HTTP on this machine, without TLS. This skill writes its local addresses without the scheme, as `127.0.0.1:8000/...`; curl accepts them so. Where a setting or a client needs a full URL (a DSN, `INSPECTOR_URL`, `PROFILER_ENDPOINT`, a proxy URL, an MCP client entry), put `http` and `://` in front of the address shown.

**Route:** the owner's OK → pick the install script, the binary or Docker → pin addresses → pick storage → start → version check → connection note → hand on to buggregator-app-connect or buggregator-mcp.

## When to use

- A job needs Buggregator and it is not running yet, or runs with addresses nobody checked.
- The owner asks how to install, start, keep data across restarts, or split events by project.
- Not for wiring the app's SDKs (buggregator-app-connect) or the agent link (buggregator-mcp).

## Inputs

- The owner's OK to install and start it on this machine (rule 1 below), with: binary or Docker; in-memory or persistent; which ports are free.
- The project folder of the app being debugged, if any, as an absolute path.
- Whether the app runs on the host or in Docker containers: it decides which host name the app uses (`127.0.0.1` or the container name).

## Rules

1. **The owner's OK, each time.** Downloading the binary, pulling an image, starting or stopping the server, changing its settings, and deleting its data all change the owner's machine. Ask before each, and say what will happen.
2. **Loopback only.** Every address is `127.0.0.1:<port>`; with Docker every `-p` is `127.0.0.1:<host>:<container>`. Never `0.0.0.0` and never a bare `-p 8000:8000`, even when an example online shows one.
3. **A pinned version.** Download a named release or use a version tag of the image, record it, and never update it unasked. `latest` is fine only when the owner says so; record what `GET /api/version` reports.
4. **No production data.** Point only development and test apps at it. If the owner wants to aim a staging or production app at it, stop and hand that decision back: real users' data would land in a tool with no login by default.
5. **No secrets in files you write.** SSO client secrets, JWT secrets and the MCP token are the owner's: they set them in their own environment; you never print, store or repeat them.

## Ports

| Port | What listens | Setting (env) | Default bind |
|---|---|---|---|
| 8000 | Web UI, REST API, WebSocket, and HTTP intake for Sentry, Ray, Inspector, XHProf, HTTP dumps, SMS | `HTTP_ADDR` (flag `-http-addr`) | all interfaces |
| 1025 | SMTP server that catches mail | `SMTP_ADDR` (flag `-smtp-addr`) | all interfaces |
| 9912 | Symfony VarDumper server (not on Windows) | `VAR_DUMPER_ADDR` (flag `-vardumper-addr`) | all interfaces |
| 9913 | Monolog socket handler, JSON lines | `MONOLOG_ADDR` (flag `-monolog-addr`) | all interfaces |
| 8080 | HTTP forward proxy that records traffic and decrypts HTTPS; always on | `PROXY_ADDR` (no flag) | all interfaces |
| 8001 | MCP over HTTP, only when the owner turns MCP on with HTTP transport | `MCP_ADDR` | all interfaces |

A module the owner does not need can be switched off (`CLIENT_SUPPORTED_EVENTS=sentry,smtp,...` keeps only the listed ones; YAML `modules.<name>: false`); its TCP port then stays closed. Module names: `sentry`, `ray`, `var-dump`, `inspector`, `monolog`, `smtp`, `sms`, `http-dump`, `profiler`. The proxy on 8080 cannot be switched off this way: pin it to loopback. Only the traffic of your own apps goes through the recording proxy: it decrypts HTTPS, and recording other people's traffic can be unlawful.

The Xdebug proxy (ports 9003 in, 9004 to the IDE) is in buggregator-xdebug; it is in Buggregator since 2.6.0 and off by default.

## Steps

1. **Ask.** Say what you plan: install script, binary or Docker, the version, the ports, in-memory or a data folder. Wait for the yes.
2. **Check the ports are free.** `ss -ltn | grep -E ':(8000|1025|9912|9913|8080)\b'` (macOS: `lsof -nP -iTCP -sTCP:LISTEN`). A port in use: pick another for that setting and tell the owner, or stop the other program only on the owner's word.
3. **Install, route A: the install script** (since Buggregator 2.6.0). Use the copy of the script at the release tag, never the one on master: Linux and macOS `https://raw.githubusercontent.com/buggregator/server/v2.7.0/scripts/install.sh`, Windows the `install.ps1` next to it. Save it, show it to the owner, and run it only on the owner's yes:

   ```
   curl -fsSL -o install.sh https://raw.githubusercontent.com/buggregator/server/v2.7.0/scripts/install.sh
   # show install.sh to the owner; on their yes:
   BUGGREGATOR_VERSION=v2.7.0 sh ./install.sh
   ```

   On Windows: save `install.ps1` with `Invoke-WebRequest <script URL> -OutFile install.ps1`, show it, then on the yes set `$env:BUGGREGATOR_VERSION="v2.7.0"` and run `.\install.ps1`. Never pipe a script straight into a shell. The Linux and macOS script puts the binary in `~/.local/bin` without sudo (if that folder is not on `PATH`, run `~/.local/bin/buggregator`); the Windows one in `%LOCALAPPDATA%\Programs\buggregator`, which is not added to `PATH`, so run it by its full path. Both pick the file for this system and CPU and compare it with the release's `checksums.txt`: that shows the file arrived intact, not who made it. Settings: `BUGGREGATOR_VERSION` (a tag such as `v2.7.0`), `BUGGREGATOR_INSTALL_DIR` (another folder). Never set `BUGGREGATOR_NO_VERIFY=1` (it skips the checksum), and never set `BUGGREGATOR_BASE_URL` (it points the download elsewhere). The docs also have a one-pass page for agents that installs and starts in one go; this skill still asks first. Then start the binary as in route B.
4. **Start, route B: the binary.** Files on the releases page are named `buggregator-linux-amd64`, `buggregator-linux-arm64`, `buggregator-darwin-amd64`, `buggregator-darwin-arm64`, `buggregator-windows-amd64.exe`, and since 2.6.0 `buggregator-windows-arm64.exe`; each release lists their checksums in `checksums.txt`. Download the asset of the agreed release from `https://github.com/buggregator/server/releases`, check it with `sha256sum` against `checksums.txt` (intact, not who made it), `chmod +x`, and start it with pinned addresses. A file saved from a browser may be blocked once: on macOS (the binary is not notarized by Apple) the owner clears it with `xattr -d com.apple.quarantine buggregator`; on Windows SmartScreen asks, or `Unblock-File .\buggregator.exe`. Clearing that mark is the owner's step. Start:

   ```
   HTTP_ADDR=127.0.0.1:8000 SMTP_ADDR=127.0.0.1:1025 \
   VAR_DUMPER_ADDR=127.0.0.1:9912 MONOLOG_ADDR=127.0.0.1:9913 \
   PROXY_ADDR=127.0.0.1:8080 ./buggregator
   ```

   Settings can also live in `buggregator.yaml` (or `.yml`) in the working folder, or a file named with `-config <path>`; a file may use `${VAR}` and `${VAR:default}`. Order of strength: flag, then env, then file, then default. A broken file only warns and the defaults apply, so check the addresses after the start. Since 2.6.0 the start stops when a port is taken, and the log names it with `address already in use`.
5. **Start, route C: Docker.** Image `ghcr.io/buggregator/server` (tags such as `2.7.0`, `2.7`, `2` and `latest`; use the exact one):

   ```
   docker run --rm --name buggregator \
     -p 127.0.0.1:8000:8000 -p 127.0.0.1:1025:1025 \
     -p 127.0.0.1:9912:9912 -p 127.0.0.1:9913:9913 \
     ghcr.io/buggregator/server:2.7.0
   ```

   The image declares 8000, 1025, 9912 and 9913; publish 8080 or 8001 yourself only when the job needs them, on `127.0.0.1` too. In Compose, other services reach it as `buggregator:<port>`; the host ports stay on `127.0.0.1`. A config file goes in with `-v ./buggregator.yaml:/buggregator.yaml`.
   **Memory** (since 2.7.0): with a memory limit on the container (or a systemd `MemoryMax`), Buggregator sets Go's soft memory limit to 90% of the smallest limit it finds and logs `go memory limit`; `GOMEMLIMIT` (for example `400MiB`) overrides it, `GOMEMLIMIT=off` turns it off. With no limit anywhere there is none, and the in-memory database grows with the events.
6. **Storage.** Default: SQLite in memory and attachments in memory, all gone on restart. To keep data, with the owner's OK: for the binary `-db ./buggregator.db` (the file is made on the first start); in general `DATABASE_DSN=/data/buggregator.db`, `STORAGE_MODE=filesystem`, `STORAGE_PATH=/data/storage`, and a folder the owner names (Docker: a volume on `/data`). Tell the owner there is no retention limit: a kept database grows until someone clears it.
7. **Projects (optional).** Project `default` always exists. More projects are listed in YAML: `projects: [{key: shop, name: Shop}]`; an unknown key also appears when its first event arrives. There is no REST call to create one. How each SDK names its project is in buggregator-app-connect.
8. **Check.** `curl -s 127.0.0.1:8000/api/version` returns `{"version":"..."}`; open `127.0.0.1:8000` once. There is no `--version` flag and no health endpoint. Then confirm each port listens on `127.0.0.1` only: `ss -ltn | grep -E ':(8000|1025|9912|9913|8080)\b'` must show `127.0.0.1:`, never `0.0.0.0:` or `*:`.
9. **Write the connection note** (Artefacts).

## Login for the UI (only on the owner's word)

The UI and API are open to anyone who reaches port 8000. On a shared host the owner may turn on single sign-on: `AUTH_ENABLED=true`, `AUTH_PROVIDER` (`auth0`, `google`, `github`, `keycloak`, `gitlab` or `oidc`), `AUTH_PROVIDER_URL`, `AUTH_CLIENT_ID`, `AUTH_CLIENT_SECRET`, `AUTH_CALLBACK_URL` (path `/auth/sso/callback`), `AUTH_JWT_SECRET` (required, else the start fails). The owner enters the secrets. Know its limits: intake, the TCP ports, the proxy and MCP never ask for a login. Since 2.6.0 the module APIs (Sentry, profiler, SMTP, mocks) and the live feed need the session token when SSO is on; on older builds they answered without one. SSO does not make a server safe to open to the internet; loopback does.

## Stopping and going back

- Stop: Ctrl+C on the binary, or `docker stop buggregator`, only on the owner's word. With in-memory storage, say first that the events will be gone.
- Wrong settings: stop, fix the env or file, start again, repeat step 7.
- Remove: delete the binary or the image and any data folder only on the owner's word.

## Do not promise

- A login on intake, the SMTP port, the proxy or MCP: none exists.
- Events kept after a restart with the default storage.
- A size cap or automatic cleanup: there is none.
- That a port is local because an example said so: check with `ss`.
- The install script on a build before 2.6.0: it came with that release.

## Artefacts

- The connection note, five to ten lines: system; install route; binary path and release, or image and tag; `GET /api/version` answer; each address as `ss` shows it; storage (memory, or the DSN and folder); modules switched off; projects; MCP on or off; who said yes to the start, and when; the date.

## Hand-over

- Next: buggregator-app-connect to point the app at it; buggregator-mcp to give an agent read access.
- A host that must be reachable by other people or machines: to the owner and their DevOps engineer, with the facts above; you do not open ports beyond loopback.

## Sources

This skill is made by harnsy, not an official Buggregator product; no endorsement by the Buggregator project is implied.

Facts only: commands, settings and short technical phrases as written; no passages taken: the Buggregator documentation at https://github.com/buggregator/docs (commit f6b2b4f, the head on 2026-11-07; pages getting-started, install, agent-setup, config/server, config/projects, config/sso, config/http-proxy), which carries no licence; the Buggregator server release v2.7.0 (release notes https://github.com/buggregator/server/releases/tag/v2.7.0, source https://github.com/buggregator/server/tree/v2.7.0; its README states MIT), read 2026-11-07. The install scripts were read in the same release (scripts/install.sh, scripts/install.ps1). The docs and the code agree that every port listens on all interfaces by default.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
