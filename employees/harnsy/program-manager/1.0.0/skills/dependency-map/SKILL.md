---
name: dependency-map
description: Map the dependencies between teams in a programme or project (who needs what from whom, by when, the giving owner, kind, status and fallback), list what is at risk this week, and propose ways to shrink dependencies to the owners. Use right after the plan is approved and every week after.
---

# Dependency map

Most programme delays sit in the joints: one team waiting for another, for a supplier or for a decision. The map makes each joint visible with an owner on the giving side and a date, so a slip is seen before it lands.

**Route:** approved plan (from `plan-and-milestones`) → **dependency-map**, weekly → at-risk items to both owners → slips to `status-report` and `risk-log`.

## When to use

- A plan is approved and involves more than one team, a supplier or open decisions.
- Every week while the work runs.
- When two teams disagree about who does what.

## Inputs

- The approved plan and its milestones.
- Each team's own plan or tracker (read-only).
- The owners on each side: project managers, team leads, supplier contacts.

## Steps

1. **List each dependency** in one row:
   - needing team and giving team (or supplier, or decider);
   - what exactly is needed;
   - need-by date (when the needing side must have it to keep its milestone);
   - owner on the giving side, by name;
   - kind: technical (a piece of system), another team's work, an outside supplier, a decision or research still missing, a strict order of steps;
   - status: agreed, in progress, at risk, late, done;
   - what happens if it slips, and the fallback.
2. **Find the missing owners.** A dependency with no giving owner is raised the same day with both sides and the plan's owner.
3. **Raise cross-team ones early.** Every dependency between teams is confirmed with the giving owner, not assumed.
4. **Propose ways to shrink them,** each as a proposal to the owners on both sides: a smaller first version, an interface agreed in advance so both sides can work at once, a different order of work, or the needing team doing the piece itself.
5. **Weekly update.** Ask each giving owner for status; record the date of each answer. List what is at risk this week.
6. **Optional diagram.** A simple picture of teams and arrows, if readers find it easier; the table stays the source.

## Rules

- Dates are recorded as the giving owner stated them, with the date of the statement; the agent never promises another team's date.
- Proposals to shrink a dependency are decided by the owners, not by the agent.

## Checks before hand-over

- Every dependency has a giving owner, a need-by date and a status.
- Missing owners are raised, with the date raised.
- Every at-risk item names its fallback.
- Slips are passed to `status-report` and `risk-log`.

## Artefacts

- `plan/dependencies.csv`: needing, giving, what, need-by, owner, kind, status, fallback, last update.
- `plan/at-risk-<YYYY-MM-DD>.md`: this week's at-risk list.

## Hand-over

- **To owners on both sides:** at-risk items and proposals to shrink dependencies.
- **To the plan's owner:** missing owners and dependencies that put a milestone at risk.
- **To `status-report` and `risk-log`:** slips and new risks.

## Sources

Adapted from the roadmap-update skill, dependency mapping section, in github.com/anthropics/knowledge-work-plugins, product-management folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Also built on «The Orange Book: Management of Risk – Principles and Concepts» (HM Treasury; © Crown copyright): risks outside the organisation's control. Contains public sector information licensed under the Open Government Licence v3.0. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
