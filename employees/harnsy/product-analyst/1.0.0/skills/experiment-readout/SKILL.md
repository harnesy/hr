---
name: experiment-readout
description: Read out a finished experiment against its approved plan: check the run was healthy, report the effect with its uncertainty, check guardrails, and recommend ship, no-ship, extend or inconclusive for the product owner to decide. Use when an A/B test or other controlled experiment reaches its planned end.
---

# Experiment readout

A readout says what the experiment showed, how sure we can be, and whether the run itself can be trusted. It recommends; the product owner or product manager decides whether to ship.

**Route:** experiment-design (approved plan) → the test runs → **experiment-readout** → the product owner decides.
Before this skill: the approved plan and a finished run. After it: the decision, recorded by its owner.

## When to use

- An experiment has reached the sample size and end date in its plan.
- A test was stopped early by its stopping rule: read it out as such.
- Someone asks for a result before the planned end: explain why the answer waits, unless the plan has a sequential rule.

## Inputs

- The approved plan (`experiments/<name>/plan.md`) with its primary metric, guardrails, smallest effect worth acting on and analysis plan.
- The assignment and outcome data, read-only.
- A log of anything that happened during the run (releases, incidents, campaigns, tracking changes).

## Rules

- Judge the result against the plan, not against what looks interesting now.
- Analyse everyone as assigned, whether or not they saw or finished the change.
- Report the effect and its uncertainty. A p-value alone is not a result.
- Segments not named in the plan are exploratory; they may suggest a new test, not a decision.
- The agent recommends; the decision owner decides.
- Every number carries its query and the date it was run; personal data stays aggregated.

## Steps

1. **Health check before results:**
   - the split matches the plan (a sample-ratio mismatch means the result is not trusted until explained);
   - the planned sample size and duration were reached;
   - tracking was stable for both variants;
   - nothing in the run log breaks the comparison.
2. **Primary metric:** the control value, the difference between variants with its 95% interval, and the p-value as planned. For rates, give the difference in percentage points first; a relative change may be added.
3. **Practical size:** compare the interval with the smallest effect worth acting on. A result can be statistically clear and still too small to matter, or promising but too uncertain.
4. **Guardrails:** each with its difference and interval; flag any that got worse beyond the agreed limit.
5. **Several primary comparisons:** apply the correction named in the plan and say so.
6. **Exploratory findings:** clearly separated, never part of the recommendation.
7. **Recommendation** in one of four forms, with the reason:
   - ship: the primary metric moved by at least the smallest worthwhile effect, guardrails held, the run was healthy;
   - no-ship: no worthwhile effect or a guardrail harmed;
   - extend: only if the plan allows it, with the new end;
   - inconclusive: the run cannot answer the question, and why.
8. **Write it so a non-specialist can follow:** one paragraph of plain words first, then the table and chart.

## Checks before hand-over

- Health checks are done and stated.
- Every result has its interval; rates are in percentage points.
- The recommendation follows the plan's rules; exploratory findings are kept apart.
- Queries and run dates are attached.
- The text says who decides.

## Artefacts

- `experiments/<name>/readout.md`: summary, health checks, results, guardrails, recommendation.
- `experiments/<name>/readout.sql`: the queries.
- A chart of the effect with its interval (see `chart-report`).

## Hand-over

- **To the product owner or product manager:** the readout and the recommendation; the decision and its date are recorded by them.
- **To the data scientist:** questions the run raised for a next experiment.
- **To the marketing analyst:** findings about channels, when the test touched them.

## Sources

Built on the Office of Evaluation Sciences (U.S. General Services Administration) methods papers «Reporting statistical results in text and in graphs» and «Adjusting for Multiple Comparisons» (https://oes.gsa.gov/methods/; US government works), adapted. Built on the ab-test-analysis subagent of awesome-claude-code-subagents (github.com/VoltAgent/awesome-claude-code-subagents, commit 721e973; MIT, © 2025 VoltAgent), adapted. Built on «The AQuA Book» (2025, https://www.gov.uk/guidance/the-aqua-book). Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
