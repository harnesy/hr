---
name: unit-economics
description: Read a young company's unit economics from the data it actually has: each metric defined with its formula before its value, recurring revenue walked from start to end, customers grouped by start month, segments instead of one blended number, gross and net retention side by side, gaps and assumptions listed, and at most three weak points. Use when a founder shares revenue or customer numbers or asks how healthy the business is.
---

# Unit economics

Unit economics answer one question: does each customer bring in more than it costs to win and serve? This skill computes what the data allows, says plainly what it does not allow, and points at no more than three things to fix. It gives no benchmark as a fact and no valuation or investment advice.

**Route:** founder's numbers (and raw data pulled by the data analyst) → **unit-economics** → the founder decides → inputs for `scenario-model` and `investor-pack-draft`.

## When to use

- A founder shares revenue, customer or spend numbers.
- A founder asks «are we healthy?», «what is our churn?», «what is a customer worth?».
- Before building scenarios or an investor pack.

## Inputs

- **Jurisdiction and currency:** the company's country and reporting currency; who the accountant is.
- **The business model:** subscription, recurring services, usage-based, one-off sales, or a mix. The metrics differ; decide this first.
- **Best:** a customer list with start date, end date (if any) and amount per month. Ask for it; totals hide problems.
- **Otherwise:** monthly recurring revenue by month; customers at start and end of each month; new, expansion, contraction and lost revenue; sales and marketing spend; gross margin; services revenue apart from recurring.
- Ask for everything missing **in one grouped message**, not one question at a time.

## Steps

1. **Fix the model and the period.** Write which revenue counts as recurring and which does not.
2. **List the gaps and the assumptions** before any number: what is missing, what is assumed, who could supply it.
3. **Define, then compute.** For each metric, one sentence of meaning and the formula, then the value with its inputs and period:
   - monthly recurring revenue (MRR); annual run rate = MRR × 12 (a run rate, not the year's revenue);
   - customer churn per month = customers lost in the month ÷ customers at the start of the month;
   - average revenue per account = MRR ÷ paying accounts;
   - acquisition cost per new customer = sales and marketing spend in the period ÷ new customers in the period;
   - lifetime value = revenue per account × gross margin ÷ monthly customer churn (only when churn is steady enough to mean something);
   - months to earn back acquisition cost = acquisition cost ÷ (revenue per account × gross margin);
   - net revenue retention = (start MRR + expansion − contraction − lost) ÷ start MRR, for the same customers over the period; gross revenue retention = (start MRR − contraction − lost) ÷ start MRR.
4. **Walk recurring revenue** from start to end of the period: new, expansion, contraction, lost. The walk must end at the end figure.
5. **Group customers by start month,** in counts and indexed to 100, to see whether newer groups behave better or worse.
6. **Split by segment** (plan, size, channel, country) where the data allows; keep services revenue apart.
7. **Put gross and net side by side.** Net retention above 100 % can come from a few growing accounts while many others leave; always show gross retention and customer churn next to it.
8. **Name at most three weak points,** worst first, each with the number behind it and the data that would change the reading.

## Checks before hand-over

- Every metric has its formula, inputs, period and source.
- The revenue walk ends exactly at the end figure.
- Gross retention appears wherever net retention does.
- No benchmark or «healthy range» is stated as a fact; targets come from the founder.
- No valuation, no advice on investing or raising; nothing is called certain.

## Artefacts

- `unit-economics/<period>/metrics.csv`: metric, formula, inputs, value, period, source.
- `unit-economics/<period>/walk.csv` and `cohorts.csv`.
- `unit-economics/<period>/reading.md`: one page with gaps, assumptions and the three weak points.

## Hand-over

- **To the founder:** the reading and the sheets. The founder decides what to act on.
- **To the data analyst:** requests for raw customer or usage data; the analyst pulls, this skill defines and checks the metric.
- **To the accountant:** questions about revenue recognition or margins in the books.
- **To `scenario-model`:** the measured drivers, labelled with their period.

## Sources

Adapted from the saas-metrics-coach skill by Abbas Mir in github.com/alirezarezvani/claude-skills (MIT, © 2025 Alireza Rezvani) and from the unit-economics skill in github.com/anthropics/financial-services-plugins (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Metric formulas are standard definitions, retold. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
