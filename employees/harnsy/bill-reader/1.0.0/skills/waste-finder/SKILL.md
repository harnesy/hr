---
name: waste-finder
description: Find leftover, idle, oversized and forgotten cloud resources and paid-for capacity left unused - each as a candidate with evidence (utilisation over a window that includes month-end, last access, attachment state, age, owner, environment) and the risk of removing it - and classify each as a clear candidate, ask the owner, or keep with a reason. Read-only; nothing is called waste to others before its owner confirms. Use after a bill breakdown, or when spend grows without a known reason.
---

# Waste finder

Cloud accounts collect things nobody switched off: a storage volume left behind when a server was removed, snapshots kept long past the policy, a test environment that runs all weekend, licences for people who left. Some of what looks idle is not: a standby copy, a quarter-end job, a recovery backup. This skill lists the candidates with the evidence for each and the risk of removing it, and asks the owner before anything is called waste.

**Route:** the breakdown and read-only inventory and utilisation data → **waste-finder** → confirmed candidates to `savings-proposal` → unknown owners to the account owner.

## When to use

- After `bill-breakdown`, on the top services and the untagged spend.
- When spend grows and nobody can say why.
- Not to change anything: the result is a list of candidates for owners to confirm.

## Inputs

- The breakdown for the period.
- Read-only inventory and utilisation exports the owner provides: resources with their size, state, attachment, creation date, tags and environment; utilisation over at least one month-end; last access where available; commitment and licence use.
- The owner's retention and recovery rules, if written.

## Steps

1. **Check each kind of leftover:** storage volumes attached to nothing; snapshots and backups older than the retention rule; sandboxes and test environments with no recent activity; addresses, load balancers or other billable items attached to nothing; unused licences and seats.
2. **Check scheduling:** test and pre-production environments that run nights and weekends when nobody uses them.
3. **Check size:** resources with consistently low utilisation, over a window that includes the last month-end and, where possible, quarter-end.
4. **Check paid-for capacity:** commitments and prepayments shown as unused in the export.
5. **For each candidate, record the evidence:** monthly cost from the export, utilisation and the window it covers, last access, attachment state, age, owner tag, environment.
6. **Record the risk of removing it:** data that may be needed, a standby or recovery role, a contract or warranty term, a minimum size required by a vendor, an unknown owner.
7. **Classify:** clear candidate (evidence strong, owner known, low risk), ask the owner (evidence or ownership unclear), keep (with the reason).
8. **Ask the owners** of the clear candidates to confirm before anything is called waste in a report to others.

## Rules

- **Read-only.** Nothing is stopped, resized, tagged, scheduled or deleted.
- **«Candidate» until confirmed.** The word «waste» is used for an item only after its owner has agreed.
- **Evidence for every item,** with the window it covers.
- **«Keep» is a valid result,** recorded with its reason so the item is not raised again next month.

## Checks before hand-over

- Every candidate has its monthly cost, evidence with a window, risk and owner (or «owner unknown»).
- Utilisation windows include a month-end.
- Nothing was changed in the account.
- Owners were asked before any item was called waste to others.

## Artefacts

- `cost/<period>-candidates.md`: item, kind, monthly cost, evidence, window, risk, owner, status (clear candidate, ask the owner, keep, confirmed by the owner).

## Hand-over

- **To `savings-proposal`:** the candidates the owners confirmed.
- **To the account owner:** items with no known owner.
- **To the service owners:** their candidates, for confirmation.

## Sources

Built on FinOps Framework: “Workload Optimization” by FinOps Foundation (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: kinds of waste (stranded storage, excess snapshots and backups, unused sandboxes, redundant licences and seats), scheduling of pre-production, right-sizing after long-cycle peaks, resources kept large for a reason. Built on the FOCUS Specification v1.4 (Joint Development Foundation Projects, LLC, FinOps Open Cost and Usage Specification (FOCUS) Series and its contributors; CC BY 4.0), modified: commitment discount status showing unused capacity. Built on the GOV.UK Service Manual, «Environmentally sustainable services» (Government Digital Service, Crown copyright), adapted: data that is not needed costs storage. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
