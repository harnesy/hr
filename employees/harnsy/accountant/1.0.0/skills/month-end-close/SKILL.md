---
name: month-end-close
description: Run a company's month-end close as a dated calendar with owners: cut-off, proposed accruals and adjusting entries with their papers, every balance-sheet account reconciled, movements explained, and a close pack for the owner or controller to approve and lock. Use when a month needs closing or someone asks where the close stands. Never posts, locks or files.
---

# Month-end close

The close turns a month of bookkeeping into numbers an owner can sign off. This skill plans the close, prepares every proposed entry and reconciliation, explains what moved, and hands a pack to the person who approves. It never posts to the ledger, locks a period or files anything.

**Route:** bookkeeper's month (matched transactions, bank and card reconciliations, trial balance) → **month-end-close** → `four-eyes-review` on the entry list → owner or controller approves, posts and locks → closed actuals to the financial analyst.

## When to use

- A month has ended (or is about to) and needs closing.
- Someone asks «where are we with the close?» or «why is this balance different?».
- Not for preparing or filing tax returns, or for an audit: those belong to a tax professional and an auditor.

## Inputs

Ask first; do not start without these:

- **Jurisdiction:** the country, the accounting basis or reporting standard in use, and the outside accountant, auditor or tax adviser (if any).
- **The people:** who approves entries, who locks the period, who prepares (often the bookkeeper).
- **The owner's numbers:** the materiality level and the size of movement that needs a written explanation, and the approval limits. Asked, written into the pack, then used. No default is assumed.
- The bookkeeper's hand-over: categorised transactions with documents, bank and card reconciliations, the trial balance.
- The chart of accounts, last month's close pack and list, and the working-day calendar.

## Steps

1. **Write the calendar before month end.** List each task with one owner, a due working day after month end, and a status: not started, in progress, done and reviewed, blocked (with the blocker) or at risk.
2. **Order the tasks by what they depend on.** First entries that need nothing else (cash, payroll, depreciation, release of prepayments, supplier accruals); then sub-ledger reconciliations; then every balance-sheet reconciliation; then tax lines and draft statements; then review; then «ready to lock». The longest chain decides the earliest finish; say which chain it is.
3. **Agree the cut-off.** With whoever handles payables, receivables, payroll and the bank, settle what belongs to this month. List unusual transactions known in advance. Read open purchase orders for missing accruals.
4. **Collect inputs and mark gaps.** Anything missing is a blocker with an owner and a date, not a guess.
5. **Prepare proposed entries with their papers.** Each one carries: what and why, the calculation, the source documents, the period, who prepared it and when, whether and when it reverses, and an empty line for the approver.
6. **Reconcile every balance-sheet account.** Give each open item a type: timing (clears by itself, say when), needs an adjustment (propose the entry), or unexplained (investigate). Age the open items; send old ones to the owner; report an item that repeats month after month as a process problem.
7. **Draft results and explain movements.** Compare with last month and with plan. Every movement above the owner's threshold gets its cause in plain words, not the number restated.
8. **Run `four-eyes-review` on the entry list** and on any reconciliation with an adjustment. The preparer is never the approver.
9. **Assemble the pack and propose «ready to lock»** with the evidence. Posting, locking and anything sent outside the company are done by a person.
10. **Look back.** Note what was late, what surprised, and one change for next month. Keep the close length and the count of late tasks from month to month.

## Checks before hand-over

- Every balance-sheet account has a reconciliation or a written reason why not.
- The trial balance balances; draft statements tie to it.
- Every open item has a type and an age; nothing unexplained is hidden in a suspense or plug entry.
- Every proposed entry has its papers and a blank approval line; nothing is marked posted by the agent.
- Every figure names its source (ledger export, bank statement, owner's statement, assumption).
- Every rate or rule used (exchange rates, depreciation lives, tax lines) names its official source and the date it was checked; tax treatment is written as a question for the tax adviser.

## Artefacts

- `close/<YYYY-MM>/status.md`: the calendar and status board.
- `close/<YYYY-MM>/reconciliations.csv`: account, balance per books, balance per support, open items with type and age.
- `close/<YYYY-MM>/proposed-entries.md`: each entry with its papers and approval line.
- `close/<YYYY-MM>/movements.md`: draft results and the explanations.
- `close/<YYYY-MM>/questions.md`: questions for the outside accountant, auditor or tax adviser.
- `close/<YYYY-MM>/look-back.md`.

## Hand-over

- **To the owner or controller:** the pack and the «ready to lock» proposal. That person approves, posts and locks.
- **To the bookkeeper:** missing documents and corrections to the month's transactions, as a list.
- **To the financial analyst:** the closed actuals, once a person has locked the period.
- **To the tax adviser or outside accountant** (through the owner): the questions file.

## Sources

Adapted from the close-management, reconciliation and journal-entry-prep skills in github.com/anthropics/knowledge-work-plugins, finance folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Also built on «Standards for Internal Control in the Federal Government», GAO-25-107721 (U.S. GAO, May 2025; a work of the U.S. government): reconciliations as a control, and duties kept apart. Scope from the O*NET 31.0 Database, 13-2011.00 Accountants and Auditors. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
