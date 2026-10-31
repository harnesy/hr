---
name: funnel-analysis
description: Measure how people move through the steps of a flow (sign-up, checkout, onboarding, an application form), find the step where most of them stop, and describe it with numbers, queries and dates. Use when a product manager asks where users drop off or why a flow converts less than expected.
---

# Funnel analysis

A funnel shows, step by step, how many of the people who started a flow reached each next step. It points to where people stop; it does not by itself say why. This skill produces a funnel the product manager can trust and a short list of questions worth testing.

**Route:** question → metric-definition (start, steps, end) → **funnel-analysis** → experiment-design or a fix for the product manager to decide.
Before this skill: an approved definition of the start and end of the flow. After it: hypotheses for the product manager and, if wanted, an experiment.

## When to use

- A flow converts less than expected, or less than it used to.
- A new flow has launched and its steps need a first baseline.
- Before an experiment on a flow: to know the current rates and where the largest drop is.

## Inputs

- **The flow:** its start event, each step, its end event, and what counts as «completed». A completed flow is not always a successful one (an application can be completed and refused); say which is measured.
- **Event data:** where each step is recorded and whether every step has its own identifier.
- **The period** and any changes to the flow or its tracking in that period.

## Rules

- Read-only on production data. Work on a read-only connection or a snapshot.
- The base is everyone who started, including those who failed or gave up, not only those who reached the end.
- Internal accounts, test traffic and robots are excluded, and the exclusion is written down.
- Personal data stays out of the result: show counts and rates per step and per segment, never lists of people.
- A drop in a step is a finding about where, not about why. No causal claim from a correlation.

## Steps

1. **Fix the definition** of start, steps, end and time window (with `metric-definition`). Decide whether a person must pass the steps in order and within one session or within N days.
2. **Check the tracking.** For each step, count events per day over the period. Gaps, sudden jumps or a step with more people than the step before it point to tracking problems; report them before analysing.
3. **Build the funnel.** For each step: people who reached it, share of the previous step, share of the start. Keep the query next to the table.
4. **Split by segments that matter for the decision:** device, channel, new or returning, country or plan. Keep segments large enough that a rate is not driven by a handful of people; mark small ones.
5. **Compare with a baseline:** the same funnel in an earlier period, or before a change. Note other things that changed at the same time (a release, a campaign, a season).
6. **Find the largest losses** and, for each, write what the data shows and what it does not, plus one or two hypotheses with what would test them (a usability session, a survey question, an experiment).
7. **Write the short report** for the product manager.

## Checks before hand-over

- The base includes everyone who started; exclusions are listed.
- Each number has its query and the date it was run.
- Tracking problems found in step 2 are stated with their effect on the numbers.
- Small segments are marked; no conclusion rests on them alone.
- Hypotheses are labelled as hypotheses; nothing claims a cause.

## Artefacts

- `funnel/<flow>-<date>.md`: definition, funnel table, segments, baseline comparison, hypotheses.
- `funnel/<flow>.sql`: the queries used.

## Hand-over

- **To the product manager:** the report and the hypotheses; the product manager decides what to change or test.
- **To the data scientist:** a hypothesis chosen for an experiment, with the current rates for sample size.
- **To the data engineer:** tracking gaps and missing step identifiers.
- **To the marketing analyst:** findings by channel.

## Sources

Built on GOV.UK Service Manual, «Measuring completion rate» and «How to set performance metrics for your service» (https://www.gov.uk/service-manual/measuring-success). Contains public sector information licensed under the Open Government Licence v3.0. Also built on the dbt Developer Hub docs on conversion metrics (commit 71495a0 of github.com/dbt-labs/docs.getdbt.com; Apache License 2.0, © dbt Labs), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
