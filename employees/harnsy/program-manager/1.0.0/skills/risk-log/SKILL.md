---
name: risk-log
description: Keep a risk log for a project, programme or team: each risk written as cause, event and consequence, scored on one shared likelihood and impact scale, compared with the level of risk the leadership accepts, with a chosen response, owner, early-warning signs and a review date; opportunities logged too. Use from the first day of the work and at every review.
---

# Risk log

A risk log is a short, honest list of what could go wrong (or unexpectedly right), how much it matters, and what is being done about it. One shared scale lets risks from different teams be compared.

**Route:** plan assumptions and dependencies (from `plan-and-milestones`, `dependency-map`), meetings and reviews → **risk-log** → risk owners act → `status-report` says whether risks sit inside the accepted level → anything above it goes to the owner.

## When to use

- At the start of any project or programme.
- At every review, status date and meeting where a new risk shows up.
- When a dependency slips or an assumption turns out wrong.

## Inputs

- The plan's assumptions and the dependency map.
- The **level of risk leadership accepts** (its appetite), in their words. If nobody has set it, ask the owner; do not assume one.
- The scale: how likelihood and impact are scored (for example 1-5 each), agreed once and used by everyone.

## Steps

1. **Look everywhere.** Plans and their assumptions, dependencies, reviews, meetings, supplier dates, gaps in information, causes outside the work's control, and the team's own optimism. Log opportunities too.
2. **Write each risk in three parts:** because of <cause>, <event> may happen, which would lead to <consequence>. A risk without a cause or a consequence goes back for rewriting.
3. **Score it** on the shared scale for likelihood and for impact; record the level and compare it with the accepted level.
4. **Choose a response** and record why. Options: avoid it (change the plan), accept it by an informed decision, make it less likely, soften its impact (with a fallback plan), share it (with a supplier, insurer or partner), or take it on deliberately for an opportunity.
5. **Record the response:** the actions, who approves the response, who acts, what it needs, early-warning signs to watch, and dates.
6. **Name one owner** per risk, by name.
7. **Review on date.** Check whether the response works, re-score, and update the status: open, treated, accepted, closed.
8. **Learn.** When a risk happens or closes, write one line on what to do differently next time.

## The register

One row per risk: id; cause, event, consequence; likelihood; impact; level; inside or above the accepted level; response and its reason; actions; approver; owner; early-warning signs; status; review date; last updated.

## Rules

- The agent proposes scores and responses; risk owners act, and the owner or leadership accepts any risk above the accepted level.
- Changes to plans or live systems arising from a response are proposals (current state, change, expected effect, how to undo it).

## Checks before hand-over

- Every risk is written as cause, event and consequence.
- Every risk is scored on the shared scale and compared with the accepted level.
- Every risk has one owner, a response with its reason and a review date.
- Accepted risks name who accepted them and when.
- Risks above the accepted level are flagged to the owner.

## Artefacts

- `risks/register.csv`: the register.
- `risks/scale.md`: the agreed scale and the accepted level, with who set them and when.
- `risks/lessons.md`: one line per risk that happened or closed.

## Hand-over

- **To risk owners:** their risks and actions.
- **To the owner or leadership:** risks above the accepted level, for a decision.
- **To `status-report`:** the risks that matter this period, and whether responses are working.

## Sources

Built on «The Orange Book: Management of Risk – Principles and Concepts» (HM Treasury, May 2023 edition, page updated 29 July 2026; © Crown copyright). Contains public sector information licensed under the Open Government Licence v3.0. Adapted from the risk-assessment skill in github.com/anthropics/knowledge-work-plugins, operations folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Also built on the risk management page of the Code-With Engineering Playbook (© Microsoft; CC BY 4.0). All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
