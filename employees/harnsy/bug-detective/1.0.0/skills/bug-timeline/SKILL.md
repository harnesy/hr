---
name: bug-timeline
description: Build the timeline of a bug from the last known good state to the first known bad one - commits, deploys, dependency updates, configuration and flag changes, data imports and migrations, traffic shifts - each with its time stamp and source, treat every event as a suspect, and rule each in or out with a test and its evidence. Read-only. Use after reproducing a bug, or when it will not reproduce and the history is the best evidence.
---

# Bug timeline

When something that worked stops working, something changed. The most recent or most visible change is not always the cause. This skill writes down every change in the window, with a time stamp and the place it was found, then settles each one with evidence. The suspects that survive become the hypotheses of the investigation; the ones ruled out stay on the page so nobody spends time on them again.

**Route:** the reproduction and the first-seen time → **bug-timeline** → surviving suspects become hypotheses in `debug-root-cause` → infrastructure or data causes to their owners.

## When to use

- After `repro-steps`, on any bug that began at a point in time.
- When the bug will not reproduce, and the history is the best evidence there is.
- Not for planning prevention across a whole incident: that is the incident review, which can reuse this timeline.

## Inputs

- The reproduction file, the first time the problem was seen, and the last time it was known to work.
- Read-only access, or exports from the owner, of: commit history, deploy log, dependency lock file history, configuration and feature flag history, data change records (imports, migrations, backfills), logs and monitoring.

## Steps

1. **Set the window:** last known good (time and version) and first known bad (time and version). Say how each was established.
2. **Collect events** in the window from every source: commits merged, deploys, dependency updates, configuration and flag changes, data imports and migrations, scheduled jobs, traffic or usage shifts, infrastructure changes. One row per event: time stamp with time zone, what changed, source (link, log line or commit id).
3. **Add the signals:** the first error in the logs, when slow pages, failed transactions or error rates moved, and which machines or services reported them. Note whether errors come from one machine or the whole service.
4. **Mark every event as a suspect.** For each, write the test that would rule it in or out: does the first error come before it; does reverting it on a copy remove the failure; does the failure appear when only it is applied; halving the range of versions between the good and the bad one.
5. **Run the tests on copies** and write each result with its evidence: in, out, or open.
6. **Keep the ruled-out suspects** on the page with their evidence.
7. **Name the survivors** in order of evidence and hand them to the debugging as hypotheses. Several surviving factors together are a normal result.

## Rules

- **Read-only.** Nothing is reverted, redeployed or reconfigured on a live system; every test runs on a copy. A revert in production is a proposal for the owner.
- **One time base.** Every time stamp carries its time zone or is converted to one; the source of each time is named.
- **Evidence or «open».** A verdict without a log line, a commit, a test result or a rate stays «open».
- **Factors, not people.** The timeline says what changed, never who is to blame.

## Checks before hand-over

- The window's two ends are stated with how they were established.
- Every event has a time stamp, a source and a verdict (in, out or open) with evidence.
- Ruled-out suspects are still listed.
- No live system was changed.

## Artefacts

- `debug/<date>-<short-name>/timeline.md`: the window, the event table, the signal rows, and a verdict column with evidence.

## Hand-over

- **To `debug-root-cause`:** the surviving suspects as hypotheses, strongest evidence first.
- **To the DevOps engineer or the site reliability engineer:** suspects in deploys, infrastructure or configuration, with the evidence.
- **To the database engineer:** suspects in data changes or migrations.
- **To whoever runs the incident review:** the timeline, if the bug affected users.

## Sources

Built on 18F Guides, «Incident reports» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: a timeline from discovery to resolution with deploys, configuration changes and moments of discovery written before analysis, the events found to be causes added later, contributing factors without blame, one root cause or several. Built on the GOV.UK Service Manual, «Monitoring the status of your service» (Government Digital Service, Crown copyright), adapted: errors tracked by recurrence and by machine, monitoring signals combined to find where users have problems. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
