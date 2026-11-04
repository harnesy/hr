---
name: exit-cost
description: Estimate what it would take to remove a library, tool or outside service later - removal steps and an effort range, how data gets out and in which format, commercial lock-in (contract length, notice) and technical lock-in (unique features, architecture shaped around it, skills concentrated on it) - and give a lock-in rating with reasons and what would lower it. Use before a verdict on adopting anything new, and when renewing a contract.
---

# Exit cost

Joining is usually quick; leaving is where the cost hides. Some lock-in is a fair price for speed and less to run, but only if it is known up front. This skill writes down how the candidate would be removed, how the data would get out, and how tightly the contract and the architecture would tie the team to it, so that the cost of leaving is part of the decision to join.

**Route:** the candidate and how deeply it would be used → **exit-cost** → verdict card (yes / no / yes with conditions) to the requester and the software architect.

## When to use

- Before a verdict on any new library, tool or outside service that would hold data or shape the architecture.
- When a contract with a supplier comes up for renewal.
- Not for small, easily swapped libraries used in one place: one line («swap in a day») is enough there.

## Inputs

- The candidate and the dependency check.
- How it would be used: which parts of the system call it, what data it would hold.
- Contract terms, if it is a paid service (from the owner).

## Steps

1. **Removal steps:** what would have to change to take it out (code that calls it, data it holds, configuration, people's habits), and an effort range in days.
2. **Data path out:** whether all data can be exported, in which format, whether that format is an open standard, whether export is self-service or needs a request, and how long it takes.
3. **Commercial lock-in:** contract length, notice period, minimum spend, what happens to discounts on leaving. Contract terms are flagged for the owner, never interpreted as legal advice.
4. **Technical lock-in:** features with no equivalent elsewhere, an architecture that would be shaped around it, skills that would concentrate on it, proprietary formats.
5. **Rate the lock-in** low, medium or high, with the reasons.
6. **Say what would lower it:** an interface of our own around it, data kept in our own store as the source of truth, open formats, using only its common features, a periodic check of the switching cost.
7. **Write the verdict card** with the dependency check: yes, no or yes with conditions, each condition checkable.

## Rules

- **Estimate leaving before joining,** as an effort range, not a single number.
- **Value against portability:** accept low portability only for high value, and say so.
- **Contracts are the owner's:** terms are listed, not judged; licence questions go to the open source licence specialist.
- **Read-only.** Nothing is adopted, configured or signed.

## Checks before hand-over

- Removal steps and an effort range are written.
- The data path out is described, including format and whether it is an open standard.
- Commercial and technical lock-in are both covered.
- The rating has reasons and the ways to lower it.

## Artefacts

- `deps/<name>-exit-cost.md`: removal steps, effort range, data path out, lock-in rating, ways to lower it.
- `deps/<name>-verdict.md`: the verdict card, with the dependency check and the exit cost.

## Hand-over

- **To the requester and the software architect:** the verdict card.
- **To the owner:** contract terms that need a decision.
- **To the open source licence specialist:** licence questions.

## Sources

Built on «Managing technical lock-in in the cloud» (Government Digital Service / Central Digital and Data Office, Crown copyright), adapted: commercial and technical lock-in, value weighed against portability, exit cost and time in plans, open formats and export, loose coupling, re-estimating switching cost. Built on the GOV.UK Service Manual, «Choosing technology» and «Working with open standards» (Government Digital Service, Crown copyright), adapted: choose so you can change your mind later, open standards make change easier. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
