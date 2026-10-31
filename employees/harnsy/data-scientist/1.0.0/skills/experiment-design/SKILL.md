---
name: experiment-design
description: Plan an A/B test or other controlled experiment before it starts: hypothesis, primary metric, guardrails, sample size, duration and stopping rule, written and approved so nobody changes them after seeing data. Use when a team wants to test a change to a product, page, e-mail or process; also serves as the general test plan for conversion and marketing tests.
---

# Experiment design

An experiment answers a question only if the question, the measure and the rule for stopping were fixed before the data came in. This skill writes that plan, sizes the test, and records it so the readout can be checked against it.

**Route:** hypothesis → **experiment-design** → the owner approves → the experiment runs → experiment-readout.
Before this skill: a change someone wants to test and the current rates (from `funnel-analysis` or `metric-definition`). After it: an approved plan for the people who build and run the test, and the same plan for `experiment-readout`.

## When to use

- A team wants to know whether a change improves a metric.
- A test is already running without a written plan: write it now, mark it as written late, and treat its result as exploratory.

## Inputs

- **The change** and the variant(s) to compare with the current version.
- **The decision** the result will feed, and who makes it (usually the product manager or the product owner).
- **The primary metric**, defined with `metric-definition`, and its current rate or mean and spread.
- **Traffic:** how many eligible units (users, accounts, sessions) per day, and the unit of randomisation.
- **The smallest effect worth acting on:** the change in the primary metric that would make the work worth shipping. This comes from the owner, not from a convention.

## Rules

- Everything in the plan is written and approved before the first unit is assigned.
- One primary metric. Other metrics are guardrails (must not get worse) or secondary (reported, not decisive).
- No peeking: the result is read once, at the planned sample size, unless the plan names a sequential method with its own rule.
- Changes to the plan after start are logged with the date and reason; results after a change are exploratory.
- Personal data: assignment and results are analysed in aggregate; the privacy specialist confirms the data use when unsure.
- Production is read-only for this skill; switching a test on or off is a step for the owner or the engineer who runs it.

## Steps

1. **Write the hypothesis:** «changing X for Y will move the primary metric by at least Z, because …».
2. **Name the metrics:** primary (one), guardrails (for example errors, refunds, unsubscribes, page speed), secondary. Link each to its definition.
3. **Choose the unit and the split:** what is randomised (user, account, session), the share in each variant, and who is excluded.
4. **Size the test** with `scripts/sample_size.py`:
   - use the smallest effect worth acting on, not a hoped-for effect;
   - print a range of effects so the owner sees the trade-off between effect size and duration;
   - split alpha when there is more than one primary comparison;
   - add an allowance for units that drop out or cannot be measured.
   If the needed sample is out of reach, say so: a larger effect, a more sensitive metric, a longer run, or no test.
5. **Set duration and the stopping rule:** the sample size, at least one full weekly cycle, the end date, and what stops a test early (a guardrail breached by a stated amount, a broken variant). Nothing else stops it.
6. **Write the analysis plan:** the test or model to be used, two-sided by default, what is confirmatory and what is exploratory, how results will be reported (effect with its interval, not only a p-value).
7. **Plan the checks during the run:** the split ratio (a sample-ratio mismatch means the result cannot be trusted), tracking health, guardrails.
8. **Get approval** from the decision owner and record the version and date.

## Checks before hand-over

- Hypothesis, primary metric, guardrails, unit, split, sample size, duration and stopping rule are all written.
- The smallest effect came from the owner and is used in the sample size.
- The sample size output (with its assumptions) is attached.
- The analysis plan says what is confirmatory and what is exploratory.
- The plan is approved and dated before the start.

## Artefacts

- `experiments/<name>/plan.md`: the approved plan with version and date.
- `experiments/<name>/sample-size.txt`: the calculator output.

## Hand-over

- **To the product manager or product owner:** the plan for approval.
- **To the developer or marketer who sets up the test:** the approved variants, split, eligibility and tracking needs.
- **To `experiment-readout`** (product analyst): the approved plan, which the readout is judged against.

## Scripts

`scripts/sample_size.py` — sample size per group for two proportions or two means, two-sided, normal approximation, with a sensitivity range, alpha split across several primary metrics and drop-out allowance. Standard library only, no network.

```
python3 scripts/sample_size.py proportions --baseline 0.10 --mde-abs 0.01
python3 scripts/sample_size.py proportions --baseline 0.10 --mde-rel 0.05 --metrics 2 --dropout 0.1
python3 scripts/sample_size.py proportions --baseline 0.10 --range 0.005,0.01,0.02
python3 scripts/sample_size.py means --sd 12.5 --mde 1.0 --power 0.9
```

When the planned analysis is not a simple two-group comparison (clusters, ratios of sums, many variants), the formula above is only a first guess; simulate or ask a statistician.

## Sources

Built on the Office of Evaluation Sciences (U.S. General Services Administration) methods papers «Preregistration as a Tool for Strengthening Federal Evaluation» and «Adjusting for Multiple Comparisons» (https://oes.gsa.gov/methods/; US government works), adapted. Built on the statistical-power skill of Scientific Agent Skills (github.com/K-Dense-AI/scientific-agent-skills, commit 92ace75; MIT, © 2025 K-Dense Inc.), adapted; cite as: Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065. https://doi.org/10.48550/arXiv.2609.00065. Built on the ab-test-analysis subagent of awesome-claude-code-subagents (github.com/VoltAgent/awesome-claude-code-subagents, commit 721e973; MIT, © 2025 VoltAgent), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
