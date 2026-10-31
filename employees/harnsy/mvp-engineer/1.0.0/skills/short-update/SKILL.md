---
name: short-update
description: Write a five-line status update about one small build - shipped, works, broken, next, needs - one sentence each, with numbers, versions and links, no adjectives about effort or mood, «nothing known» only after checking. Use on an agreed rhythm (for example twice a week) while building a first version or a small project; raise blockers at once instead of waiting for the next update.
---

# Short update

A status update should take a few minutes to write and half a minute to read, and it should point the reader to the working software where there is some. This skill keeps the update to five fixed lines that a person can check against the links in it.

**Route:** the work since the last update → **short-update** → posted on the work item for the owner → the project manager may fold it into a project status report.

## When to use

- On the rhythm agreed with the owner while a small build or a first version is under way.
- At the end of a release, as its record.
- Not for a whole project with several teams and sponsors (use a project status report), and never instead of raising a blocker the moment it appears.

## Inputs

- What changed since the last update: releases, commits, test results, user feedback.
- Open problems and their impact.
- Decisions, access or help the work is waiting for.

## Steps

1. **Shipped:** what reached users or the test group since the last update, with version and link. «Nothing shipped» is allowed and honest.
2. **Works:** what was checked to work, and how (tests, a user, a measurement), with a number where there is one.
3. **Broken:** what does not work or is known to be risky, with its impact on users. Write «nothing known» only after checking the error log, the tests and the open reports.
4. **Next:** the one or two things in progress, each with the «done when» line it aims at.
5. **Needs:** decisions, access or help, from whom and by when. «Nothing» is allowed.
6. **Read it back:** five lines, one sentence each; every claim has a number, a version or a link; no adjectives about effort, speed or mood; no date that belongs to another team.
7. **Add a demo link** when there is something to see.

## Rules

- **Five lines, always the same order.** Details go behind links, not into the update.
- **True before kind.** A broken item is named even when the rest went well.
- **No promises for others.** Dates owned by another team are not given; ask them instead.
- **Blockers do not wait.** Anything that stops the work is raised at once on the item, then repeated in «Needs».

## Checks before hand-over

- Exactly five lines in the fixed order, each one sentence.
- Every line has a number, a version, a link or an explicit «nothing».
- «Broken» was checked against the error log, the tests and open reports.
- Nothing in the update promises a result or another team's date.

## Artefacts

- The update, posted on the work item; earlier updates stay in the item's history.

## Hand-over

- **To the owner (product owner or founder):** every update, on the item.
- **To the project manager:** the updates, to fold into the project's status report where there is one.

## Sources

Built on the GOV.UK Service Manual, «Measuring and reporting progress» (Government Digital Service, Crown copyright), adapted: reports show progress without extra work for the team, and extra reporting only when it adds value. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Guides, product guide and oversight principles (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: seeing working software over reading reports about it, progress shared regularly.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
