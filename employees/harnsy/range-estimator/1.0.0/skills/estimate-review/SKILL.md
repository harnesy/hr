---
name: estimate-review
description: Compare a team's past estimates with what actually happened - pair each piece's estimate with its actual, compute the ratio of actual to likely, the median and spread by kind of work, and the kinds of work that were missing from breakdowns - and turn that into the team's own correction factor for future estimates; about the estimates, never a ranking of people. Use when a batch of estimated work is finished and before a large new estimate.
---

# Estimate review

Every team misjudges some kinds of work in its own way: integrations take longer than they look, small screens take less. The best correction for an estimate is the team's own history. This skill puts past estimates next to what really happened, finds the patterns by kind of work, and turns them into a correction factor for the next range. It describes estimates, not people.

**Route:** finished work with estimates and actuals → **estimate-review** → the correction factor back into `range-estimate` → patterns to the team lead and the project manager.

## When to use

- When a batch of estimated work is finished, for example at the end of a release.
- Before a large new estimate, if the team has history.
- Not to measure anyone's productivity or to compare people or teams.

## Inputs

- Past estimates (low, likely, high where they exist) and actuals, per piece: from tickets, the tracking tool or cycle times the team shares.
- The kind of each piece (for example interface, integration, migration, screen, investigation), or enough description to assign one.

## Steps

1. **Pair estimate and actual** for each finished piece, in the same unit. Leave out pieces whose scope changed a lot, and say how many.
2. **Compute the ratio** of actual to likely for each piece, and whether the actual fell inside the low-to-high range.
3. **Group by kind of work:** median ratio and spread per kind, and how often the actual landed inside the range.
4. **Find the missing work:** pieces that appeared during the work but were not in the breakdown (migrations, review rounds, environment set-up), by kind and how often.
5. **Set the correction factor:** the team's median ratio overall, and per kind of work where there is enough data (say how many pieces each number rests on).
6. **Write the patterns** in plain words, for example «integrations ran at 1.8 times the likely value in 7 of 9 pieces».
7. **Feed it back:** the factor goes into the next `range-estimate` (`--factor`), and the missing kinds into the next `work-breakdown` checklist.

## Rules

- **Estimates, never people.** No per-person numbers, rankings or speed comparisons; data is grouped by kind of work.
- **Planning, not productivity.** The ratios and velocity help the next estimate; they are not a score.
- **Say how much data each number rests on;** a factor from four pieces is a hint, not a rule.
- **Read-only.** Tickets and tracking tools are read, not edited.

## Checks before hand-over

- Every finished piece is paired or listed as left out, with the reason.
- Ratios and medians are given per kind of work, with the count of pieces.
- Missing kinds of work are listed.
- No number refers to an individual.

## Artefacts

- `estimate/review-<period>.md`: the paired table, ratios by kind of work, the correction factor, the missing work kinds, the patterns.

## Hand-over

- **To `range-estimate`:** the correction factor.
- **To `work-breakdown`:** the kinds of work that were missing.
- **To the team lead and the project manager:** the patterns, for planning.

## Sources

Built on 18F Guides, «Agile lexicon» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: velocity is for planning and tracking, not a measure of productivity. Built on the GOV.UK Service Manual, «Measuring and reporting progress» (Government Digital Service, Crown copyright), adapted: reporting that shows progress without extra work for the team. Contains public sector information licensed under the Open Government Licence v3.0. Comparing estimates with actuals to correct the next estimate is a general method, described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
