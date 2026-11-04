---
name: savings-proposal
description: Write one proposal per confirmed cloud savings candidate - current state, action, estimated monthly saving from the export's own usage and a dated published list price (read date, region, SKU or meter, unit, currency, link, «list price before discounts and tax»), effort, risk, how to undo it, who applies it, and how the next bill will show whether it worked. Proposes only; a person applies every change. Use on candidates the owners have confirmed.
---

# Savings proposal

A finding is only useful when someone can act on it safely. This skill turns each confirmed candidate into a proposal an owner can approve in a minute: what to change, how much it should save and on which price, what could go wrong, how to undo it, and who does it. The saving is an estimate; next month's bill shows whether it happened.

**Route:** confirmed candidates → **savings-proposal** → the account or service owner decides and applies → finance gets the summary → next month's breakdown checks the result.

## When to use

- On candidates from `waste-finder` that their owners have confirmed.
- When a change of purchase model (on demand, commitment, prepayment) is worth considering for steady usage.
- Not to apply anything, and not for budget decisions (finance).

## Inputs

- The confirmed candidates with their evidence and the export's usage for each.
- The provider's own published price list or price interface, read on the day.
- The owner's constraints: maintenance windows, recovery rules, contracts.

## Steps

1. **Write the current state** of each candidate: size, state, schedule, monthly cost from the export.
2. **Choose the action:** remove after a final copy, schedule off outside working hours, move to a smaller size, release unused capacity, change the purchase model.
3. **Estimate the monthly saving** from the export's own usage and the dated list price. Cite the price with the read date, region, SKU or meter, unit, currency and link, labelled «list price before discounts and tax». Where the export already shows the cost, use it and say so.
4. **State the effort:** who does what, and how long it takes.
5. **State the risk:** data loss, slower response, a peak the new size cannot take, a contract term, an unknown dependency.
6. **Write the undo:** restore from the final copy, size back up, switch the schedule off; or «no undo» stated plainly, with a final copy offered.
7. **Name who applies it:** the service owner or the team the owner names. Never the reader.
8. **Say how the result will be checked:** which line of next month's breakdown should change, and by about how much.
9. **Rank** the proposals by estimated saving against risk, and add a one-paragraph summary for finance.

## Rules

- **Propose, never apply.** No resource is changed, no purchase is made by this skill.
- **Estimates, not promises.** Every saving is labelled «estimated», with the price and its date.
- **Prices are dated facts** from the provider's own published list or price interface; no price from memory, no price older than the read date stated.
- **Every row has an undo,** or says plainly that there is none.
- **Compare later:** proposals stay open until the next bill shows the actual effect.

## Checks before hand-over

- Every proposal has current state, action, estimated saving with a cited dated price, effort, risk, undo, who applies it, and how it will be checked.
- No saving is presented as certain.
- No proposal is applied by the reader.

## Artefacts

- `cost/<period>-proposals.md`: one row per proposal, the ranking, the summary for finance, and a column for the owner's decision and the actual saving next month.

## Hand-over

- **To the account or service owner:** the proposals, for a decision and for applying them.
- **To the financial analyst or the startup finance analyst:** the summary of estimated savings.
- **To the cloud architect:** recurring patterns worth reflecting in future cost estimates.

## Sources

Built on FinOps Framework: “Workload Optimization” by FinOps Foundation (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: estimate both the saving and the effort and risk of each change, track recommendations and compare actual with estimated impact, the owners of the usage act. Built on «Managing technical lock-in in the cloud» (Government Digital Service / Central Digital and Data Office, Crown copyright), adapted: exit costs and duplicate contracts seen early, reviews continue after purchase. Contains public sector information licensed under the Open Government Licence v3.0. Price citation (official list or price interface, read date, region, unit, currency, list price before discounts and tax) is common practice for dated price facts.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
