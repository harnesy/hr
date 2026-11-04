---
name: plan-and-milestones
description: Write a plan for one project or for several teams working toward one outcome: the goal and what done means, milestones with dates and owners, the dependencies each milestone waits on, and the assumptions; plan changes go to the owner as proposals with their effect and a way back. Use at the start of a project or programme and whenever its scope changes.
---

# Plan and milestones

A plan is a short promise about how a goal will be reached and how anyone will know it is on track. It works for one project (kept by its project manager) and for a programme of several teams (kept by the program manager, with a programme view on top).

**Route:** a goal from the owner → **plan-and-milestones** → the owner approves → `dependency-map` and `risk-log` start → `status-report` each cycle → plan changes back here as proposals.

## When to use

- A project or programme starts and needs a plan.
- The scope, deadline or team changes.
- A milestone will be missed and the plan needs a proposed change.
- Not for assigning people or setting budgets: those are decisions for named people.

## Inputs

- The goal, in the owner's words, and the deadline if any.
- The teams involved and, for a programme, each team's project manager or lead.
- Known constraints: dates fixed from outside, people's availability as their managers state it, money as the owner states it.
- Existing plans of the teams, if any.

## Steps

1. **Goal and done.** One or two sentences for the goal, and a short list of checks that say it is done.
2. **Milestones.** A handful of points where something can be seen or used (not just «phase 2 started»). For each: what is visible, the date, and one owner.
3. **Work under each milestone,** at the level the reader needs. Each item has an owner and a date. Detailed task lists stay in the teams' own trackers.
4. **Dependencies.** For each milestone, what it waits on (another team, a supplier, a decision, a piece of research), with the need-by date. These go to `dependency-map`.
5. **Assumptions.** What the plan takes as true (people available, a supplier date, a tool working). Each is a candidate risk for `risk-log`.
6. **Programme view** (several teams only). One table of the joint milestones across teams, with the team plan each one comes from. Each project manager keeps their own plan; the programme view only joins them.
7. **Buffers.** Where a date depends on something outside the team's control, say how much slack the plan holds, and why.
8. **Approval.** The owner approves the plan. The approved version gets a number and a date.

## Plan changes

A change is always a proposal to the owner:

- the current plan (milestone, date, owner);
- the proposed change;
- the effect on other milestones and other teams;
- how to undo it if it does not work.

The plan changes only after the owner approves; the new version gets a number, and the old one is kept.

## Rules

- Dates of other teams or suppliers are reported as their owners gave them, with the date they gave them. They are never promised by the agent.
- The agent never assigns people, approves changes or sets budgets.

## Checks before hand-over

- The goal has done-criteria.
- Every milestone has a date, one owner and its dependencies.
- Every assumption is listed and passed to `risk-log`.
- For a programme, every joint milestone links to a team plan.
- The plan has a version and an approval line for the owner.

## Artefacts

- `plan/plan.md`: goal, done-criteria, milestones, work, dependencies, assumptions, version.
- `plan/programme-view.md` (several teams): joint milestones across teams.
- `plan/changes.md`: proposals with effect and undo, and the owner's decisions.

## Hand-over

- **To the owner:** the plan and any change proposals, for approval.
- **To each team's project manager or lead:** their part of the plan and the dependencies they give or receive.
- **To `dependency-map`, `risk-log` and `status-report`:** the approved plan.

## Sources

Adapted from the status-report and roadmap-update skills (dependency mapping) in github.com/anthropics/knowledge-work-plugins (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Scope from the O*NET 31.0 Database, 13-1082.00 Project Management Specialists and 15-1299.09 Information Technology Project Managers (nearest occupations). This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
