---
name: four-eyes-review
description: Second-person check on anything that moves the books or leaves the finance team (journal entries, reconciliations, reports). Prepares a review pack for a named human approver, or returns findings on an item a person prepared. Use before anything is posted or sent, and when someone asks «can you check this?». The agent is never the approver.
---

# Four-eyes review

No single person should control a whole transaction: whoever prepares an entry does not approve it, and whoever records it does not also hold the asset. This skill applies that rule to finance work. The agent checks and reports; a person approves.

**Route:** prepared item (from `month-end-close`, the bookkeeper or a colleague) → **four-eyes-review** → named human approver decides → posted by a person, or back to the preparer.

## The one rule

- **The agent is never the approver,** of its own work or of anyone else's.
- If the agent prepared the item, this skill produces a **review pack** for a named human approver: the checks already run, the evidence, and the points the approver must look at.
- If a person prepared the item, this skill returns **findings** to the preparer and the approver; the approver decides.
- An agent never acts as the second pair of eyes on work it prepared itself.

## When to use

- Before any journal entry, reconciliation adjustment or finance report is posted, sent or relied on.
- Whenever someone asks for a check.
- When duties are being set up or changed in a small team.

## Inputs

- **Jurisdiction and basis:** the country and accounting rules in force, and whether an outside accountant or auditor is involved.
- **The approver:** a named person, and that person's approval limits as the owner set them.
- **The item and its papers:** calculation, source documents, period, preparer and date.
- **The policies** the item must follow (chart of accounts, cost centres, accrual and reversal rules, closed periods).

## Steps

1. **Read the item and its papers first,** before anyone's summary or opinion of it. Form the view; then read the notes.
2. **Run the checklist:**
   - debits equal credits;
   - the period is right and not already closed;
   - the accounts exist and fit the transaction; cost centre and other coding present;
   - the arithmetic, done again from the source documents;
   - a description a stranger (or an auditor) could follow;
   - consistent with the same entry in earlier months and with the policies;
   - a reversal date where the entry should reverse;
   - the papers are complete;
   - the amount is within the preparer's limit;
   - not a duplicate of an entry already in the books;
   - large or unusual amounts carry an explanation.
3. **Compare with the usual errors:** wrong period, wrong sign, duplicate, a similar but wrong account code, an accrual that never reverses, an accrual repeated without checking it still holds, a round estimate with no calculation, a wrong exchange rate or rate date, a cut-off slip.
4. **Check who did what.** Authorising, recording, reviewing and holding the asset should sit with different people. Where the team is too small for that, write it down and propose a substitute control (for example, the owner reviews a monthly list of every manual entry with its papers). Note that splitting duties does not stop people who act together.
5. **Write the result:** pass, fail or cannot tell for each check, with the evidence and a suggested fix.

## Checks before hand-over

- Every failed or «cannot tell» check has evidence and a suggested fix.
- The pack names the approver; no line says «approved» on the agent's behalf.
- Nothing was changed in the item: findings only.

## Artefacts

- `review/<item-id>.md`: item, each check, pass / fail / cannot tell, the finding with its evidence, suggested fix, the approver's decision line left blank.
- `review/duties.md` (when duties are in question): who authorises, records, reviews and holds what, gaps, and the proposed substitute control.

## Hand-over

- **To the named approver:** the review pack. The person approves or rejects; the person, not the agent, posts.
- **To the preparer:** failed checks and suggested fixes.
- **To the owner:** gaps in the split of duties and the proposed substitute control, for a decision.

## Sources

Built on «Standards for Internal Control in the Federal Government», GAO-25-107721 (U.S. GAO, May 2025), Principle 10, paragraphs 10.21–10.23 (a work of the U.S. government). Adapted from the journal-entry-prep skill in github.com/anthropics/knowledge-work-plugins, finance folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Scope from the O*NET 31.0 Database, 13-2011.00 Accountants and Auditors. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
