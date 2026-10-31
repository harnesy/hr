---
name: metric-definition
description: Write one agreed definition for a metric (name, purpose, formula, events, filters, source, owner) before anyone builds a chart, a model or an experiment on it. Use when a team asks for a new number, when two reports show different values for «the same» metric, or when a dashboard or experiment needs a success measure.
---

# Metric definition

A metric is only useful when everyone computes it the same way. This skill turns a request («how many active users do we have?») into a written definition that an analyst, an analytics engineer and a dashboard developer can all build from, and that the product manager agrees with.

**Route:** request → **metric-definition** → model-with-tests (the metric in the data model) → dashboard-spec / funnel-analysis / experiment-design.
Before this skill: a question or a decision someone wants a number for. After it: the approved definition goes to whoever builds on it.

## When to use

- Someone asks for a number that has no written definition yet.
- Two reports, dashboards or teams show different values for what they call the same metric.
- An experiment, a funnel or a dashboard needs a success measure or a guardrail.

## Inputs

- **The decision:** what the number will be used to decide, and by whom. A metric with no decision behind it is usually not needed.
- **The purpose of the product or service** it measures, in the owner's words.
- **The data:** which tables or event streams exist, their owner, and how fresh they are.
- **Existing definitions** of the same or similar metrics.

## Rules

- One metric, one definition, one owner. A variant gets its own name.
- A rate always names its numerator and its denominator; a count always names its unit and time window.
- Personal data: the metric is computed on aggregates; no metric needs a named person. When unsure what the data may be used for, ask the privacy specialist first.
- Every published value carries the query (or the model) that produced it and the date it was computed.

## Steps

1. **Start from purpose.** Write the purpose of the product or service, then the two or three benefits it should bring to the people who use it, then for each benefit what would show that it is happening. Only then pick the measure.
2. **Pick the metric type:** a simple count or sum, a ratio (numerator measure over denominator measure), a conversion (share of people who did event B within a time window after event A), or a cumulative or derived metric.
3. **Write the definition:**
   - name (short, unique) and a one-line description in plain words;
   - type and formula; for a ratio both parts; for a conversion the entity, start event, end event and window;
   - filters and exclusions (internal accounts, test traffic, bots, refunds);
   - time grain and time zone;
   - source tables or events and their owner;
   - known caveats (late data, missing tracking before a date);
   - owner who approves changes.
4. **Check it on real data, read-only.** Compute it for a recent period. Compare with any existing figure for the same thing and explain each difference.
5. **Say what it does not tell.** A metric can move for reasons nobody controls; write the main ones next to it. A change in the metric shows that something changed, not why.
6. **Get the owner's approval** and record the version and date. A change later is a new version with a note on what changed and from when.

## Checks before hand-over

- Numerator and denominator (or unit and window) are explicit.
- Filters and exclusions are written, including test and internal traffic.
- A sample value is attached with its query and the date it was run.
- Differences from older figures are explained, not hidden.
- No personal data is needed to compute or show it.

## Artefacts

- `metrics/<name>.md`: the definition, version, owner, sample value with query and date.
- `metrics/changes.md`: the change log of all metric definitions.

## Hand-over

- **To the product manager:** the definition for approval.
- **To the analytics engineer:** the approved definition, to build it once in the data model with tests.
- **To the BI dashboard developer, data analyst and marketing analyst:** the approved definition, so every dashboard and report uses the same one.
- **To the data engineer:** missing events or sources found on the way.

## Sources

Built on the dbt Developer Hub docs (metrics overview, ratio and conversion metrics, at commit 71495a0 of github.com/dbt-labs/docs.getdbt.com; Apache License 2.0, © dbt Labs), adapted; GOV.UK Service Manual, «How to set performance metrics for your service» and «Measuring completion rate» (https://www.gov.uk/service-manual/measuring-success). Contains public sector information licensed under the Open Government Licence v3.0. Role scope from the O*NET 31.0 Database: 15-2051.01 Business Intelligence Analysts and 15-2051.00 Data Scientists. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
