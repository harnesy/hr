---
name: bill-breakdown
description: Break a cloud bill or cost-and-usage export for one period down by service, owner, sub-account and resource - with one stated cost column (billed or spread-out effective cost, never both added), purchases, taxes, credits and adjustments kept apart from usage, the month-over-month trend of the top lines, untagged spend as its own line, and a reconciliation with the invoice - using a small grouping script so every figure traces back to rows. Read-only. Use on any question about where cloud money goes or why it changed.
---

# Bill breakdown

A cloud bill is thousands of lines. Before anyone can say what to save, they need to know where the money goes, who owns it, and whether a rise is more usage or something else: a prepayment, a tax, a credit that ran out. This skill reads the export for one period, decides which cost number answers the question, groups the lines by service, owner and resource, and makes every figure traceable to the rows behind it.

**Route:** a bill or cost-and-usage export and the question behind it → **bill-breakdown** → `waste-finder` → budget questions to the financial analyst or the startup finance analyst.

## When to use

- Any question about cloud spend: where it goes, who owns it, why it rose or fell.
- Before looking for waste or proposing savings.
- Not for estimating a design that is not built yet (the cloud architect's cost estimate), and not for budgets or forecasts (finance).

## Inputs

- A bill or a cost-and-usage export (CSV, or another tabular format converted to CSV) for a stated period, from the account owner.
- The invoice total for the same period, if available.
- The owner map: which accounts, sub-accounts, tags, labels or name patterns belong to which team, if one exists.
- The question behind the request, in one sentence.

## Steps

1. **Confirm the frame:** period, currency, and the question. Check the export covers the whole period and all accounts asked about.
2. **Choose the cost column.** Billed cost (as invoiced) answers «what did we pay this month»; effective cost (prepayments and commitments spread over the usage they cover) answers «what did this service really cost»; list cost shows the discount received. Choose one per table and say which. Never add two of them together.
3. **Separate charge categories:** usage, purchases (prepayments, commitments), taxes, credits, adjustments. A rise in purchases or a credit that ended is not a rise in usage.
4. **Group the rows** with the script (see Tools): by service, by owner (tag or sub-account), and by resource for the top lines. Ask for untagged rows to be shown as their own line.
5. **Show the trend** of the top services and owners month over month, with the change in percent and in money.
6. **List untagged and unowned spend** with its top resources and the sub-accounts it sits in.
7. **Split shared costs** (support plans, shared networks, central tools) only by a rule the owner has written down; otherwise show them as shared.
8. **Reconcile** the export's total with the invoice where possible; name any gap and its likely reason (taxes, credits, rounding, a missing account).
9. **Write the page** and attach the grouped table.

## Rules

- **Read-only.** The breakdown is made from exports; nothing in the account is changed, tagged or reconfigured.
- **One cost column per table,** named in its heading; billed and effective cost are never mixed.
- **Every figure traces to rows:** the filter and grouping that produced it are stated.
- **No price looked up here.** The breakdown uses only the export's own figures; prices belong to the savings proposal, dated.
- **Owners or «owner unknown».** No line is assigned to a team by guesswork.

## Checks before hand-over

- Period, currency and cost column are stated at the top.
- Charge categories are separated, and purchases, taxes and credits are not counted as usage.
- Every figure can be reproduced from the export with the stated grouping.
- Untagged spend has its own line.
- The reconciliation with the invoice is done or the reason it could not be is given.

## Artefacts

- `cost/<period>-breakdown.md`: frame, cost column, charge categories, totals by service, owner and resource, trend, untagged spend, reconciliation.
- `cost/<period>-grouped.csv`: the grouped table from the script.

## Hand-over

- **To `waste-finder`:** the breakdown and the top resources.
- **To the financial analyst or the startup finance analyst:** the breakdown, for budget and plan-versus-actual questions.
- **To the account owner:** the untagged and unowned lines, as questions.

## Tools

- `python3` 3.8 or newer, standard library only, no network; the script reads one CSV file and runs no other program.
- `python3 scripts/cost_group.py export.csv --cost <cost column> --by <col1,col2>` groups the rows and prints a tab-separated table with each group's total and share. The column names are the export's own; read the header first.
- `--cost` takes exactly one column; naming two stops the script, because billed, effective and list cost are never added together.
- `--category <column>` keeps charge categories apart and prints a total per category; `--untagged <col>` shows rows with an empty owner column as «(untagged)» and prints their total and share; that column must also be listed in `--by`, or the script stops.
- `--date <column>` adds a month-over-month view of the top groups (the first seven characters of an ISO date); `--currency <column>` refuses to add rows in different currencies.
- `--top 20` limits the printed groups; `--csv-out grouped.csv` writes the full grouped table; `--delimiter ";"` for other separators; `-` reads standard input.
- Exit 0 when done, 2 on bad input (missing file or column, two cost columns, a non-numeric cost, mixed currencies).

## Sources

Built on the FOCUS Specification v1.4, cost and usage columns (Joint Development Foundation Projects, LLC, FinOps Open Cost and Usage Specification (FOCUS) Series and its contributors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), modified: billed, effective and list cost, charge categories, service, sub-account, resource, tags and charge period, retold in own words. Built on FinOps Framework: “Allocation” by FinOps Foundation (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: owners through accounts, tags, labels and naming, shared-cost rules, untagged spend.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
