---
name: dashboard-spec
description: Specify a dashboard before building it: who uses it for which decisions, the metrics (each from an approved definition), the layout, filters, refresh and access, and what each chart must carry (title with the message, source, date, notes). Use when someone asks for a new dashboard or a redesign of one nobody trusts.
---

# Dashboard spec

A dashboard is worth building when someone makes a decision with it. This skill starts from those people and their decisions, uses only agreed metric definitions, and writes a spec the owner approves before any chart is built.

**Route:** request → **dashboard-spec** → the owner approves → build (in any BI tool) → chart-report checks → release.
Before this skill: a request. After it: an approved spec for the builder, and the metric definitions it relies on.

## When to use

- A new dashboard is requested.
- An existing dashboard is not used, not trusted, or shows numbers that differ from other reports.

## Inputs

- **Users and decisions:** who opens it, how often, and what they decide with it.
- **Metrics:** existing definitions (from `metric-definition`); missing ones are defined first.
- **Data:** the models or tables behind each metric, their owner and refresh time.
- **Access:** who may see it, and whether any figure is sensitive.

## Rules

- One metric, one definition: no dashboard computes its own version of a defined metric.
- Each tile answers one question. A tile nobody can tie to a decision is dropped.
- Personal data: dashboards show aggregates; small groups that could identify a person are suppressed or merged; access follows the owner's rule; the privacy specialist decides when unsure.
- Every tile shows its source and the time the data was last refreshed.
- The dashboard reads data; it never writes to production systems.

## Steps

1. **Interview the users** (or the requester for them): the three to five questions they need answered, how often, and what they do when a number moves.
2. **Map questions to metrics**, each with its definition, grain, time window and comparison (previous period, target set by the owner, or both).
3. **Choose each chart** by the relationship it shows (a trend over time, a comparison between groups, parts of a whole, a distribution) — see `chart-report` for chart rules.
4. **Lay out the page:** the most important question top left; a short text line under the title saying what the dashboard is for and who owns it; related tiles together; filters that apply to the whole page at the top.
5. **Specify each tile:** title stating the message or question, metric and definition link, chart type, filters, comparison, source, refresh time, notes and caveats, a text alternative for screen-reader users.
6. **Specify behaviour:** refresh schedule, what happens when data is late (a visible warning), alerts if any and who receives them, access rights.
7. **Get approval** from the owner and record the version and date.

## Checks before hand-over

- Every tile is tied to a user question and an approved metric definition.
- Every tile has source, refresh time and notes specified.
- Small groups and personal data are handled; access is set.
- The spec is approved and dated.

## Artefacts

- `dashboards/<name>/spec.md`: users and decisions, tiles, layout sketch, behaviour, access, version and approval.

## Hand-over

- **To the owner** (often the product manager): the spec for approval.
- **To the analytics engineer:** metrics or models that must exist before building.
- **To the builder** (the BI dashboard developer): the approved spec.
- **To the privacy specialist:** any tile with personal or sensitive data.

## Sources

Built on «Data visualisation: charts» by the Government Analysis Function (https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/; source acknowledged; Crown copyright) and the GOV.UK Service Manual, «How to set performance metrics for your service» (https://www.gov.uk/service-manual/measuring-success/how-to-set-performance-metrics-for-your-service). Contains public sector information licensed under the Open Government Licence v3.0. Role scope from the O*NET 31.0 Database: 15-2051.01 Business Intelligence Analysts. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
