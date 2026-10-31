---
name: early-warning-signs
description: For each top risk from a pre-mortem, find the earliest thing the team would see if it were starting to happen - how it is observed, the threshold that means look now, who watches it, how often, and who is told when it trips; reuse measures the team already has, and mark items with no early signal so they get a stronger prevention or a ready fallback. Watches nothing and acts on nothing by itself. Use after a pre-mortem, before the hand-over.
---

# Early-warning signs

A risk that is noticed on the day it happens leaves only the fallback. Most failures announce themselves earlier: a test run that keeps getting slower, a reply that stops coming, a number that drifts. This skill gives each top risk the earliest signal the team could see, a threshold that says «look now», and a person who looks.

**Route:** the top items from `pre-mortem` → **early-warning-signs** → `risk-handoff`.

## When to use

- After a pre-mortem, for every top item.
- When a plan's owner asks how they will know a known risk is starting.
- Not for watching the signals during the work: the named watchers do that.

## Inputs

- The top items, each with its cause and effect.
- The plan's milestones and dates.
- The measures the team already collects (dashboards, reports, test runs, budgets, reply times).

## Steps

1. **Ask the question** for each item: what is the first thing we would see if this were starting to happen?
2. **Prefer early over late:** a signal that shows weeks before the failure beats one that shows on the day.
3. **Reuse before inventing:** if the team already measures something that moves first, use it.
4. **Write the signal** as something observable: a number, an event, or something that fails to happen (a missing reply, a skipped review).
5. **Set the threshold** that means «look now», in the signal's own units, and say why that level.
6. **Name the watcher, the rhythm and who is told:** one person, how often they check, and who hears the same day it trips.
7. **Mark items with no early signal.** For those, propose a stronger prevention or a fallback prepared in advance, and say so in the table.
8. **Show the table to the plan's owner** and record changes.

## Rules

- **Observable or it is not a signal.** «Morale drops» needs a measure the watcher can actually read.
- **One watcher per signal.** A signal everyone watches is a signal nobody watches.
- **The agent watches nothing by itself.** It reports on a signal only if the owner asks it to, and acts on none.
- **Thresholds are proposals.** The owner may move them.

## Checks before hand-over

- Every top item has a signal or is marked «no early signal».
- Every signal has a measure, a threshold, a watcher, a rhythm and who is told.
- Items with no early signal have a stronger prevention or a ready fallback.

## Artefacts

- `risks/warning-signs.md`: item, signal, measure, threshold and why, watcher, rhythm, who is told; items with no early signal and their response.

## Hand-over

- **To `risk-handoff`:** the signal and watcher for each item.
- **To the watchers named:** their own rows, through the plan's owner.

## Sources

Built on The Orange Book: Management of Risk – Principles and Concepts (HM Treasury, Crown copyright), adapted: indicators of emerging risk, early-warning indicators kept beside performance measures, reporting each principal risk against its indicators. Contains public sector information licensed under the Open Government Licence v3.0. Built on «Pre-mortem – risk planning», Digital Service Toolkit (© State of New South Wales; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: warning signs written with each reason, how hard a failure is to notice as a ranking factor. © State of New South Wales. For current information go to www.nsw.gov.au.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
