---
name: budget-model
description: Build or check a driver-based budget model: every line tied to what moves it, all typed inputs in one dated assumptions sheet, formulas everywhere else, base, downside and upside switched in one place, self-checks in every scenario, and the gap between the leadership target and the teams' build shown. Use for an annual or quarterly budget, a re-forecast, or a review of someone's model. Never loads anything into a live system.
---

# Budget model

A budget is a set of decisions about money, written as numbers. This skill builds the model those decisions rest on, so that anyone can see what drives each line and what would have to be true for the result. The owner decides; the model shows.

**Route:** goals and targets from the owner, requests from budget holders → **budget-model** → owner or finance lead decides → approved budget becomes the plan for `plan-vs-actual`.

## When to use

- A new annual or quarterly budget.
- A re-forecast after a change in the business.
- A request to check a model someone else built (review mode: report, change nothing).

## Inputs

- **Jurisdiction and frame:** the country, the currency, the fiscal year, the accounting basis, and the owner's approval process.
- **The top-down target** from the owner or leadership, if there is one.
- **Each team's request** and the person who owns it.
- **Actuals so far,** closed by the accountant; anything not yet closed is labelled «pre-close, may change».
- The owner's rules: approval limits, what counts as a material change.

## Steps

1. **Agree the frame:** country, currency, fiscal year, approval route.
2. **Find the driver of every line** with the line's owner: people × cost per person, customers × price, units × unit cost, and so on. A line with no driver (last year plus a percentage) is flagged as such.
3. **Write one assumptions sheet.** Each assumption has a value, unit, source, date and owner. Only actuals and assumptions are typed numbers; every other cell is a formula that points back to them.
4. **Build the calculation sheets** with formulas only, the same units and periods throughout, and clear labels.
5. **Show both builds and the gap:** the target from the top next to the sum of the teams' requests, the difference, and options to close it.
6. **Pair every request for more with its cost elsewhere:** what is cut or moved later to pay for it. The owner chooses.
7. **Add scenarios:** base, downside and upside, chosen from one switch on the assumptions sheet, each with the event that would make it the likely one.
8. **Run the self-checks in every scenario:** totals add across and down; where there is a balance sheet it balances every period; ending cash equals cash on the balance sheet; downside sits below base and base below upside.
9. **Summarise on one page:** the result per scenario and the three assumptions that move it most.

### Review mode (someone else's model)

Do not edit the file. List findings with a severity: **wrong result** (a formula or link gives the wrong number), **risky** (a typed number inside a formula, a broken check, a hidden input), **style** (labels, units, layout). Propose the fix for each; change the model only when its owner asks.

## Checks before hand-over

- No typed number outside the assumptions and actuals.
- Every assumption has a source, a date and an owner; units are stated.
- All self-checks pass in every scenario, or the failure is reported.
- Every scenario is labelled as a scenario with its assumptions, not as a promise.
- Any rate or rule from outside the business (tax rate, social charges, exchange rate) names its official source and the date checked; tax questions are written for a tax professional.

## Artefacts

- `budget/<period>/assumptions.csv` (value, unit, source, date, owner).
- `budget/<period>/model.csv` or the workbook, with a scenario switch.
- `budget/<period>/summary.md`: result per scenario, top drivers, the top-down versus bottom-up gap and the options.
- `budget/<period>/findings.md` in review mode.

## Hand-over

- **To the owner or finance lead:** the model, the summary and the options. That person decides; the approved version is the plan.
- **To budget holders:** questions about their drivers.
- **To the accountant:** questions about actuals.
- Nothing is loaded into a planning or accounting system by the agent; a change to a shared model in use is a proposal (current value → new value → effect → how to undo).

## Sources

Adapted from the finance-fpa-analyst agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors) and from the audit-xls and 3-statement-model skills in github.com/anthropics/financial-services-plugins (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Scope from the O*NET 31.0 Database, 13-2031.00 Budget Analysts and 13-2051.00 Financial and Investment Analysts. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
