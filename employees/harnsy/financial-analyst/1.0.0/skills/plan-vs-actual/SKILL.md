---
name: plan-vs-actual
description: Monthly comparison of closed actuals with the approved plan: variances over the owner's threshold split into their drivers, explained in plain words with an outlook and an action, a bridge from plan to actual that adds up exactly, and an updated forecast for the rest of the year with last month's forecast error. Use after each approved close or when someone asks why spending or revenue is off plan.
---

# Plan versus actual

The point of comparing plan with actual is not to describe the past but to decide what to do next. This skill finds the differences that matter, says what caused them, and updates the outlook.

**Route:** closed actuals from the accountant + approved plan from `budget-model` → **plan-vs-actual** → owner and budget holders decide actions → next month's forecast.

## When to use

- After each close that a person has approved and locked.
- When someone asks «why are we over?» or «why are we under?».
- Not before the close is approved: wait, or label every figure «pre-close, may change».

## Inputs

- **Jurisdiction and frame:** country, currency, fiscal year, the plan version in force.
- **Closed actuals** from the accountant, and the approved plan or latest forecast.
- **The owner's thresholds:** what size of difference, in money or share, needs a written explanation. Asked once, written into the report, then used.
- Driver data: headcount and pay, volumes and prices, rates and mix, as each line needs.

## Steps

1. **Load actuals and plan** for the same period and the same version; note both versions on the report.
2. **Apply the owner's thresholds** and rank what is over them by size, by surprise, by a move against the trend, and by growth over several months.
3. **Split each variance into drivers:** price against volume, rate against mix, headcount against pay per person, or whatever moves the line. Show each part in money.
4. **Write each explanation:** what moved and in which direction, how much, why in plain words, whether it will continue, and what to do about it.
5. **Reject empty explanations:** «higher because it was higher», «timing» with no dates, «various items» for a large amount, or naming the largest driver while an offsetting one goes unmentioned.
6. **Build the bridge:** plan, then each driver's effect, ending exactly at the actual figure. Any leftover is shown as its own line, not hidden.
7. **Look forward:** update the forecast for the rest of the year; record how far last month's forecast was from the actual, and keep that record over time.

## Checks before hand-over

- The bridge adds up exactly from plan to actual.
- Every explained line has drivers, a cause, an outlook and an action.
- None of the empty-explanation patterns remain.
- Actuals match the closed books; nothing pre-close is unlabelled.
- Forward figures are labelled as a forecast with their assumptions, not as a commitment.

## Artefacts

- `pva/<YYYY-MM>/variances.csv`: line, plan, actual, difference, drivers.
- `pva/<YYYY-MM>/report.md`: the ranked explanations, the bridge, the updated forecast, last forecast's error, open questions.

## Hand-over

- **To the owner and the budget holders:** the report, for decisions on actions.
- **To the accountant:** any question about an actual figure. The analyst never changes actuals.
- **To `budget-model`:** a re-forecast request when the outlook has shifted beyond the owner's threshold.

## Sources

Adapted from the variance-analysis skill in github.com/anthropics/knowledge-work-plugins, finance folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Also adapted from the finance-fpa-analyst agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors). Scope from the O*NET 31.0 Database, 13-2031.00 Budget Analysts. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
