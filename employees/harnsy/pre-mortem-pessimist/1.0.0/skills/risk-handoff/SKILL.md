---
name: risk-handoff
description: Hand the top risks from a pre-mortem to the plan's owner as one plain table they can paste into whatever log the team keeps - risk (cause, event, effect), likelihood, impact, prevention, early sign, watcher, owner - with the owner's scale and accepted level at the top and what the owner accepted, changed or rejected; with the owner's agreement, the same table goes to the program manager who keeps the register during the work. Use at the end of a pre-mortem.
---

# Risk hand-over

A pre-mortem is worth what happens after it. The results have to land in the place the team already looks, in a shape anyone can read without the session notes. This skill writes the top risks as one plain table, records what the owner decided about each, and hands it to the people who will carry it through the work.

**Route:** `pre-mortem` + `early-warning-signs` → **risk-handoff** → the plan's owner → (with the owner's agreement) the program manager.

## When to use

- At the end of a pre-mortem, once the owner has seen the top items and the signals.
- When a plan's owner asks for the risks in a form to paste into their own tracker, spreadsheet or register.
- Not for keeping the register up to date during the work (the program manager or the owner does that).

## Inputs

- The top items with prevention, fallback and proposed owner (from `pre-mortem`).
- The signals, thresholds and watchers (from `early-warning-signs`).
- The owner's scale for likelihood and impact and the accepted level of risk.

## Steps

1. **Write each risk in one line:** cause, the event it leads to, and its effect on the plan.
2. **Add the scores** on the owner's scale, with the scale written once at the top.
3. **Add the response:** prevention (start now), fallback (if it happens anyway).
4. **Add the early sign** with its threshold, and the watcher.
5. **Add the owner** and a review date for each row.
6. **Record the owner's decision per row:** accepted as is, changed (how), or rejected (with the owner's reason).
7. **Keep it plain:** a table with simple columns and no formatting that breaks when pasted; the detail stays in the pre-mortem file, linked.
8. **Hand it over** to the plan's owner; send it on to the program manager only when the owner agrees.

## Rules

- **No row without a prevention and an owner,** unless it is marked open with the person asked to propose one.
- **The owner's words win.** If the owner changes a score or a response, the table shows the owner's version and keeps the original in the linked file.
- **Nothing is sent by the agent.** The owner or the requester passes the table on.
- **About the work, never a person.** Risks describe causes and effects, not people's faults.

## Checks before hand-over

- Every row has risk, likelihood, impact, prevention, early sign, watcher, owner and review date, or an «open» mark with a person asked.
- The scale and the accepted level are at the top.
- The owner's decision is recorded for every row.
- The table pastes cleanly as plain text.

## Artefacts

- `risks/handoff-<date>.md`: the scale and accepted level, the table, a link to the pre-mortem file and the warning-signs table.

## Hand-over

- **To the plan's owner:** the table.
- **To the program manager,** with the owner's agreement: the same table, for the register kept during the work.
- **To the named watchers and owners:** their rows, through the plan's owner.

## Sources

Built on The Orange Book: Management of Risk – Principles and Concepts (HM Treasury, Crown copyright), adapted: a common scale to compare risks, reporting each principal risk with its indicators against the accepted level, owners for each risk. Contains public sector information licensed under the Open Government Licence v3.0. Built on GOV.UK Service Manual, «Governance principles for agile service delivery» (GDS, Crown copyright), adapted: risks cannot all be removed, so own the ones that could affect delivery and respond at the right moment. Contains public sector information licensed under the Open Government Licence v3.0. Built on «Pre-mortem – risk planning», Digital Service Toolkit (© State of New South Wales; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: each risk with a person responsible, actions and a due date, revisited at regular check-ins. © State of New South Wales. For current information go to www.nsw.gov.au.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
