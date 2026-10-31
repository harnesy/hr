---
name: lead-routing-rules
description: Write and change the rules that decide who owns a new lead: an ordered rule tree from the most specific match to a fallback queue with an owner, existing account owners first, fair weighted rotation that pauses people who are away, the rule named on every assignment, and a replay on past leads before any change. Use when leads reach the wrong person, wait unassigned, or a team or territory changes.
---

# Lead routing rules

Routing decides which person answers a new lead. Good rules give the same answer for the same lead every time, send every contact of one account to one owner, and leave nobody waiting. This skill writes the rules down, tests a change on past leads, and proposes it with an undo.

**Route:** a routing problem or a team change (from the sales lead, a sales development representative or an account executive) → **lead-routing-rules** → replay on past leads → proposal through `crm-change-proposal` → the sales lead approves → the owner applies.

## When to use

- Leads from one company reach several owners.
- Leads wait unassigned, or some people get far more than others.
- A person joins, leaves, goes on leave or comes back; territories or segments change.
- People keep overriding the same assignment for the same reason.
- Not for deciding territories or quotas as a management matter: the sales lead decides those, and the rules then follow.

## Inputs

- The current rules, written or as configured, with the date read.
- The assignment log or a lead export with arrival order, the fields the rules use and the owner each lead got.
- The team list: who takes which kind of lead, weights, who is away and until when.
- Override and rejection records, with reasons.

## Steps

1. **Write the current rules down** as an ordered tree, even if they live only in a tool's settings. Note gaps (leads that match nothing) and conflicts (leads that match two rules).
2. **Order from specific to general.**
   - The existing account owner, and the owner of an open deal with that account, come first.
   - Then named accounts, then segment, then territory.
   - Then a fair rotation within the matching group.
   - Last, a fallback queue with a named owner, so no lead waits unassigned.
3. **One owner per account.** All contacts from one account go to the same owner.
4. **Fair rotation.** Weights written down; people who are away are paused and rebalanced on return; counts reset on a fixed cycle (for example monthly). The weights are the sales lead's decision.
5. **Name the rule on every assignment.** Each routing card says which rule fired, the owner, what is known about the lead, and what is missing. A person accepts or overrides it; override reasons are recorded.
6. **Send-backs and recycling.** When sales turns a lead back, the reason is recorded; recycled leads return to nurture with that reason.
7. **Replay before changing.** Run the proposed rules on past leads (see Tools): how many assignments would change, for whom, and why.
8. **Propose.** Through `crm-change-proposal`: the current rules, the new rules, the replay result, the expected effect, and how to switch back. Repeated override reasons become proposed rule changes the same way.
9. **After the change,** check the assignment log for a week: unassigned leads, split accounts, rotation balance.

## Rules

- **Deterministic.** Same input, same rule, same owner.
- **Read-only.** Rule changes are proposals; the sales lead approves, the owner applies.
- **No ranking of people.** Rotation weights are the sales lead's decision and never a reward or penalty computed by the agent.
- **Lead data minimum.** The rules use business fields (company, region, size, source), not personal traits.

## Checks before hand-over

- Every lead in the replay matched exactly one rule or the fallback.
- No account is split between owners in the replay.
- The fallback queue has a named owner.
- The proposal shows the number and list of changed assignments and the way back.

## Artefacts

- `sales/routing/rules-<date>.md` and `rules-<date>.json`: the rule tree in words and as data for the replay.
- `sales/routing/replay-<date>.csv`: per lead, the rule, the proposed owner, the current owner, changed or not.
- `sales/routing/overrides.md`: override and send-back reasons with counts.

## Hand-over

- **To the sales lead:** the proposal with the replay, for approval.
- **To `crm-change-proposal`:** the change rows, including reassignments of existing leads.
- **To the sales development representatives and account executives:** the approved rules in plain words.

## Tools

`scripts/route_replay.py` replays a rules file on a lead export and reports how many assignments would change, by rule and by proposed owner; with `--out` it writes one row per lead. Python 3 standard library only, no network; it reads files and reassigns nothing.

- Arguments: the rules file (JSON: an ordered list of rules, rotation pools with weights and people away, and a fallback with an owner; the format is in the script's header) and the lead export (CSV, in arrival order).
- Options: `--id-col`, `--current-col` (the owner each lead actually got), `--account-col` (keeps every lead of one account with one owner), `--out` (per-lead CSV).
- It refuses a rules file without a fallback owner, a rule that assigns nobody, and an unknown pool.

## Sources

Adapted from the route-lead skill in github.com/anthropics/knowledge-work-plugins, sales folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Built on the revops skill, its routing-rules reference and the lead rejection and recycling section of its lifecycle reference in github.com/coreyhaines31/marketingskills (MIT, © 2025 Corey Haines), adapted. Built on the PostHog handbook, /contents/ folder, lead assignment tracker and lead scoring pages (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
