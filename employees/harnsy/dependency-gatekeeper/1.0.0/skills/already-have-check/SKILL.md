---
name: already-have-check
description: Before a new library, tool or outside service is considered, write the need in one sentence and list what in the current stack (lock files, platforms, services already run) already does it or most of it, with the gap, and the running cost of a second tool - people who must learn it, upgrades, security watching, monitoring, on-call, duplicated data - then recommend use what we have, extend what we have, or a new tool is justified. Use first on every request to adopt something new.
---

# Already-have check

The cheapest dependency is the one not added. Teams often reach for a new tool because it is familiar from elsewhere, while something already running would do the job with a small change. This skill writes down the need, looks at what is already in use, and counts what a second tool would cost to keep running, so that a new tool is added only for a reason the existing one cannot meet.

**Route:** a request to adopt something new → **already-have-check** → if a new tool is justified, `dependency-check` and `exit-cost` → verdict to the requester and the software architect.

## When to use

- First, on every request to add a library, tool or outside service.
- When two teams are about to adopt different tools for the same job.
- Not to block experiments in a throwaway script: be freer for one-off work, stricter for long-lived systems that will be handed over.

## Inputs

- The need, from the requester.
- The current stack: lock files, the list of platforms and services already run, the team's defaults (for example one datastore, one queue).

## Steps

1. **Write the need** in one sentence, without naming the candidate: «We need to retry failed jobs with a delay», not «We need tool X».
2. **List what already exists** that does this or part of it: a library already in the lock file, a feature of a platform already run, a common service the organisation already provides. For each, the gap against the need.
3. **Count the running cost of a second tool:** who must learn it, upgrades and their rhythm, security watching and advisories, monitoring and alerts, on-call, backups, duplicated data, and the hand-over to whoever maintains it later.
4. **Weigh the gap against that cost.** A real wall (the existing tool cannot meet a stated requirement) justifies a new tool; a preference does not.
5. **Recommend one of three:** use what we have (with how), extend what we have (with the change and its effort), or a new tool is justified (with the wall it removes).

## Rules

- **The need comes before the candidate.**
- **The team default wins unless there is a real wall,** stated as a requirement the default cannot meet.
- **Long-lived systems get the stricter bar;** one-off scripts a lighter one.
- **Read-only.** Nothing is installed or changed.

## Checks before hand-over

- The need is written without naming a product.
- Every existing option has its gap stated.
- The running cost of a second tool is listed item by item.
- The recommendation is one of the three, with its reason.

## Artefacts

- `deps/<need>-already-have.md`: need, existing options and gaps, running cost of a second tool, recommendation.

## Hand-over

- **To the requester and the software architect:** the recommendation.
- **To `dependency-check`:** the candidate, if a new tool is justified.

## Sources

Built on the Concise Guide for Evaluating Open Source Software (OpenSSF Best Practices Working Group; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: consider first whether a new dependency is needed at all. Built on the GOV.UK Service Manual, «Managing software dependencies», «Choosing technology» and «Using common platforms» (Government Digital Service, Crown copyright), adapted: reuse saves time but every component is a dependency to manage; adopt only when nothing already in use fits. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Guides, «Language selection» and «Datastore selection» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: a team default first, another tool only at a real wall; stricter for long-lived projects.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
