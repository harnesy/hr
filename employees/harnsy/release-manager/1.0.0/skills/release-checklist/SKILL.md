---
name: release-checklist
description: Prepare and track a release with a checklist where every item has a time, an owner, a status and a clear meaning of done, covering readiness, deployment, communication, checks after release, monitoring and a review; the owner gives the go and publishes, the agent never tags or publishes a release itself. Use for any release, and always for a large or first launch.
---

# Release checklist

A release goes wrong most often through something nobody owned. This skill lists every task that affects the release, gives each one an owner, a time and a status, and keeps the list current until the release is reviewed afterwards. It prepares and tracks; the owner decides «go» and publishes.

**Route:** a release scope → **release-checklist** → readiness review with the owner → the owner says go → deploy-with-rollback → checks and monitoring after release → review that updates the checklist.
Before this skill: what is in the release and who owns it. After it: a completed checklist, a go/no-go record and a review note.

## When to use

- Every release; a short version for small, frequent releases and the full version for large ones.
- A first launch, a migration, or any release with downtime, data changes or many audiences.

## Inputs

- The release scope: the changes in it, with links to tickets and the changelog.
- The release-readiness criteria agreed with the owner and QA.
- Owners for each area: code, infrastructure, data, support, communication.
- Dates and windows from other teams, as those teams gave them.

## Rules

- Every item has: date and time (due, and how long it takes), owner, status (pending, in progress, done, blocked), what «done» means, and notes.
- The agent prepares, tracks and reports. The owner gives the go and publishes; the agent never tags, publishes or announces a release itself.
- Nothing is promised that is not in the release. Dates of other teams are never promised; they are written down as given, with the source, and marked «per <team>».
- No promised uptime or speed in any message.
- Known bugs are listed openly with the decision on each: blocks the release, or ships with a workaround.
- Prefer small, frequent releases. A large release is split by user group where possible, with rehearsed data migrations.

## Steps

1. **Create the checklist** from the template sections below and fill in owners and times with them.
2. **Readiness:**
   - known bugs: listed, each marked blocking or not, with a workaround and a support answer for the ones that ship;
   - automated test and build warnings: each recorded as an issue or explained;
   - tests in a production-like environment done, results attached; readiness criteria met;
   - the branch or version to release fixed; a code freeze if needed, and who may approve an exception during it.
3. **Deployment:**
   - network, DNS and firewall changes prepared as change proposals;
   - configuration, environment settings and secrets in place for the target environment;
   - access and permissions for users and administrators set;
   - data migrations rehearsed on a copy, with timing;
   - rollout and rollback plan written with deploy-with-rollback.
4. **Communication** for each audience: stakeholders and management, internal staff and support (what to expect, prepared answers), partners the release depends on (do they know, are they on call), and users (downtime notice, what changes, where to get help). Release notes are drafted with the release-notes skill.
5. **Go/no-go:** walk through the list with the owner. Record the decision, who made it and when. A «no-go» lists what must change.
6. **During the release,** update statuses as items finish, and note any deviation from the plan.
7. **Checks after release:** hands-on checks by the team and, where agreed, by people outside it; how stakeholders can see the result.
8. **Monitoring:** how long to watch, where (dashboards, logs), and what: traffic against the expected range, errors, CPU and memory, bandwidth, outgoing mail volume if any.
9. **Review:** collect what went well and what did not, and update the checklist template for next time.

## Checks before hand-over

- Every item has a time, owner, status and meaning of done.
- Known bugs and their decisions are visible.
- The go/no-go decision is recorded with the owner's name.
- No message promises a feature, date of another team, uptime or speed beyond what is in the release.
- The agent did not tag, publish or announce anything.

## Artefacts

- `releases/<version>-checklist.md`: the checklist with all items and statuses.
- `releases/<version>-go-no-go.md`: decision, who, when, open items.
- `releases/<version>-review.md`: what happened and changes to the template.

## Hand-over

- **To the release owner:** the checklist for go/no-go, and the publish step.
- **To devops, the SRE or the Kubernetes platform engineer:** deployment items and the rollback plan.
- **To the QA engineer:** readiness criteria and checks after release.
- **To support and the product manager:** communication items and release notes.
- **To the security reviewer:** secrets, access and any security fixes in the release.

## Sources

Built on 18F Guides, «Software launch checklist» and «Releasing software» (github.com/18F/guides, commit debc24b; US General Services Administration, public domain in the US and CC0 1.0 elsewhere), adapted; no endorsement by GSA is implied. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
