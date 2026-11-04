---
name: kickside-host-isolation
description: Wall a KickSide container off from its host - never the host network, never beside other services without proof, host.docker.internal blocked, traffic from KickSide's network to the host dropped, and a probe from the container's own network namespace showing every host port unreachable while the Hub still answers. Use before a server copy's first boot, after any Docker, firewall or network change, and when someone asks to run KickSide on a machine that also runs other services.
---

# A wall between KickSide and its host, checked by a probe

Why this skill exists: KickSide runs automations, agents and connections that call other addresses on its users' behalf. So treat every copy as untrusted toward the machine it runs on: whatever else listens on that host, an agent runner or a control port included, must stay out of KickSide's reach. This skill builds that wall and checks it with a probe. The publisher's own cloud descriptor takes the same stance: its network is isolated, denies by default, and lets the app out only to DNS and public HTTPS (read from S2).

**Route:** a server or machine for KickSide → **kickside-host-isolation** → kickside-docker-deploy → the probe again after every change.
Before this skill: the owner's OK for firewall changes on that machine. After it: the wall in files, the probe's output saved as proof, and a report.

## When to use

- Before the first boot of any copy you run on a server: development, staging or production. A local copy on loopback belongs to the KickSide specialist.
- After a Docker upgrade, a reboot, a firewall change, a new compose network or a new service on the host.
- When someone proposes running KickSide on a machine that runs anything else.

## Inputs

- The machine: Docker Engine on Linux, or Docker Desktop; what else runs there.
- The host's listening ports: `ss -ltnH` (all addresses, loopback included).
- KickSide's compose networks and container name.

## Steps

1. **Choose the machine.** Best: KickSide alone on its server or VM. A client's production server runs only KickSide, its database, nginx and the backup and monitoring jobs. If the owner wants KickSide on a machine with other services, it is allowed only in its own container and network and only after step 6 passes; tell the owner the risk in one line.
   Check: the choice and the owner's words are in the report.
2. **Never the host network, never the Docker socket.** No `network_mode: host`, no `privileged`, no mount of `/var/run/docker.sock` (that is root on the host), `cap_drop: [ALL]` and `no-new-privileges` unless a step proves a need (read from S8, not tried).
   Check: `docker inspect <container>` shows network mode not `host`, `Privileged` false, no socket mount.
3. **Own networks, named bridges.** Give each KickSide compose network a fixed bridge name (`driver_opts: com.docker.network.bridge.name: br-ks-app`, and `br-ks-db` for the internal database network) so firewall rules can name them. The database network is `internal: true` (read from S8, not tried).
   Check: `ip link show br-ks-app` exists; `docker network inspect` shows the subnet and gateway of each.
4. **Block host.docker.internal.** On Docker Engine for Linux the name exists only when a compose file maps it to `host-gateway`: never add that. On Docker Desktop the name exists by default and leads to the host, including services that listen only on the host's loopback. Map the name to an address that leads nowhere (`extra_hosts: ["host.docker.internal:192.0.2.1", "gateway.docker.internal:192.0.2.1"]`). This is a seatbelt, not the wall: the host is still reachable by address (read from S8, not tried; the Docker Desktop branch above is not tried at all).
   Check: inside the container's namespace, the name resolves to 192.0.2.1.
5. **Drop traffic from KickSide's bridges to the host.** On Docker Engine, packets from a container to the host's own addresses go through the host's INPUT chain, not Docker's chains. For each KickSide bridge: accept established and related packets (replies to nginx's connections), then drop everything else arriving on that bridge, for IPv4 and IPv6. Write the rules in the host's firewall tool (iptables or nftables) and make them survive a reboot; a Docker restart must not remove them. Optional and stronger, with the Application security reviewer: in the `DOCKER-USER` chain, drop traffic from KickSide's bridges to private ranges and link-local addresses (cloud metadata lives at 169.254.169.254), except KickSide's own subnets (read from S8, not tried). On Docker Desktop these host rules do not apply to containers: if step 6 fails there, KickSide moves to another machine or a VM (read from S8, not tried).
   Check: the rules are in the deployment repository and listed by `iptables -S` or `nft list ruleset` after a reboot.
6. **Probe from the container's own namespace.** Run a throwaway container that shares KickSide's network namespace, so it sees exactly what KickSide sees: `docker run --rm --network container:<kickside-container> <pinned bash image> bash -c '<loop>'`, where the loop tries `timeout 3 bash -c "</dev/tcp/$addr/$port"` for every address and port below and prints `open` or `closed` per pair (built from S8, not tried). Addresses: the gateway of each KickSide network, the host's LAN and public addresses, `host.docker.internal`, `gateway.docker.internal`, 169.254.169.254. Ports: every port from `ss -ltnH` on the host, including any agent or control port on the host, and always 22 and 5432. Then the positive check, in the same namespace with a pinned curl image: the Hub address the image uses answers over HTTPS.
   Check: every host pair says `closed`; the Hub answers; KickSide's own health still answers through nginx (the wall did not cut nginx off).
7. **Save the proof and repeat it.** Keep the probe script in the repository and its dated output with the copy's records. Run it after every change listed in «When to use», and put a monthly run next to the restore drill.
   Check: the latest output is newer than the last Docker, firewall or network change.
8. **Report.** The machine, what else runs there, the rules added, the probe's summary (pairs tried, all closed, Hub reachable), and what is left.
   Check: the report holds the counts and the file of the proof, no secrets.

## Rules (each with its check)

- **No first boot before the probe passes.** Check: the probe output predates the first boot.
- **Owner's OK before firewall changes.** Check: the OK is quoted.
- **Any exception goes to the Application security reviewer first** (a host port KickSide must reach, an outside address to allow, a wider egress). Check: the reviewer's answer is linked.
- **User accounts and roles only after the Application security reviewer's OK for that copy.** The KickSide specialist creates them; before that, check on the copy what ordinary users' policies allow and tell the owner. Check: the reviewer's OK predates the first account other than the owner's.
- **A probe result that says `open` stops the work.** Stop the copy if it runs, report, fix, probe again. Check: no copy runs with an open pair.

## Pitfalls

- Binding the host's own services to 127.0.0.1 is not enough on Docker Desktop: trust the probe, not the bind.
- `docker compose down` and `up` can recreate bridges with new names unless the names are fixed (step 3), and the firewall rules then miss them.
- Names stop resolving after step 5: the container was using a resolver on the host. Give it resolvers outside the host (compose `dns:`) instead of opening the host.
- A probe from a separate container on the same network is not the same as one inside KickSide's namespace when extra hosts or network settings differ; use `--network container:`.

## Hand-over

- **To the Application security reviewer:** every exception, and the probe output when it shows `open`.
- **To the KickSide specialist:** user accounts and roles, once the Application security reviewer has cleared the copy.
- **To the DevOps engineer:** firewall or network work on the host that is not about KickSide.
- **To the owner:** the machine choice when the wall cannot be built there.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken: S2 the KickSide cloud deployment descriptor `app/src/deployment/_index.yaml` (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI) for its network policy; S8 the Docker documentation (docs.docker.com: bridge networks, packet filtering and firewalls, host.docker.internal). Not tried live by us: every step marked «not tried» was only read from the source named, and the probe decides.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
