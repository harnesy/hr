---
name: pipeline-report
description: Weekly sales pipeline report from a CRM export: a data-quality block first, the per-stage roll-up in the team's own stage names, risk flags, the win rate from each stage in the team's last quarters, and a range for open pipeline value instead of one number. Use for the weekly pipeline review or when the sales lead asks where the quarter stands. Reads only; changes go through crm-change-proposal.
---

# Pipeline report

A pipeline report should tell the sales lead what is real, what is at risk and what the numbers cannot show. This skill reads a CRM export, says first what is missing or stale, rolls the open deals up by stage, flags risk, and compares the pipeline with the team's own history as a range.

**Route:** CRM export (or read access) → **pipeline-report** → the sales lead → record fixes through `crm-change-proposal`; recurring dashboards through `dashboard-spec` / `chart-report`.

## When to use

- The weekly pipeline review.
- The sales lead asks where the quarter stands or why a number moved.
- Not for one-off metric questions (agree the metric with `metric-definition` first) and not for building a dashboard (`dashboard-spec`).

## Inputs

- A CRM export of open and closed deals with: id, stage, amount, created date, date the current stage was entered, close date, next step, last activity date, status (open, won, lost), and optionally a segment. For lost deals, the stage they had reached.
- The team's stage names in order, with their exit criteria.
- The owner's thresholds: days without activity that count as stale, how many past quarters to use (two by default).
- The metric definitions in use (from `metric-definition`), so «pipeline value» and «win rate» mean what the team agreed.

## Steps

1. **Data quality first.** Run the script (see Tools). Read its data-quality block: blank amounts, blank or past close dates, blank next steps, missing activity dates, stages not in the list. Write what each gap does to the numbers. Never fill a gap in silently.
2. **Stage roll-up.** Per stage: count, value, average age, how many have no next step, how many are stale, how many have a close date in the past. Say which age measure you used (days in the current stage or days since created).
3. **Risk flags.** Stale deals regardless of stage, slipping close dates, blank next steps, deals stuck far beyond the stage's usual age, deals with a single contact, late-stage deals missing steps the team requires (for example a security review). List the largest flagged deals with the reason.
4. **Next steps that mean something.** A good next step has a date, the person at the customer who acts, and the outcome expected. Count deals whose next step lacks one of these.
5. **History as the baseline.** Win rate from each stage per quarter, from the team's own closed deals. No industry rule of thumb.
6. **A range, not a number.** Open value times the lowest and the highest quarterly rate of each stage. If someone uses a stage-probability figure, compare it with the range and explain the gap as a risk; name the deals that drive it.
7. **Segment before concluding.** Repeat the roll-up per segment when segments behave differently; a total can hide a segment in trouble.
8. **Leading and lagging.** Separate signals that move first (new deals created, stage moves, activity) from results (won, lost).
9. **Loss reasons.** For deals lost in the period, list the recorded loss reasons and count deals lost without one.
10. **Write the report** with bad news in the same tone as good news, and recommendations specific enough to act on (which deals, which owner, by when).

## Rules

- **Read-only.** The report changes nothing; record fixes are proposals through `crm-change-proposal`.
- **Gaps are findings.** A missing value is reported, not estimated.
- **Ranges with assumptions.** Every forecast figure carries the quarters, rates and exclusions it came from.
- **No ranking of people.** The report is about deals and stages, not a league table of representatives.

## Checks before hand-over

- The data-quality block is the first section, with counts.
- The age measure, stale threshold and quarters used are stated.
- Every forecast figure is a range with its assumptions.
- Flagged deals are listed with reasons.
- No number in the report was filled in by hand.

## Artefacts

- `sales/reports/pipeline-<date>.md`: the report.
- The export file name and date, recorded in the report header.

## Hand-over

- **To the sales lead:** the report.
- **To `crm-change-proposal`:** record fixes found on the way (for the owners to approve).
- **To the BI dashboard developer through `dashboard-spec`:** a request when the team wants the report as a standing dashboard.

## Tools

`scripts/stage_report.py` reads a CSV export and prints the report sections in Markdown: data quality, the roll-up of open deals by stage, risk flags, the quarterly win rate from each stage and the range for open value. Python 3 standard library only, no network; it reads the file and writes to standard output.

- Arguments: the export file; `--stages` with the open stages in order, comma-separated.
- Options: `--today` (report date), `--stale-days` (default 30, the owner's threshold), `--age-from` (`stage_entered` or `created`), `--quarters` (default 2), `--by-segment`, `--top` (how many flagged deals to list), and `--col field=Header` when the export's column names differ.
- Lost deals must carry the stage they had reached; won deals count as having passed every stage.

## Sources

Adapted from the pipeline-review and crm-hygiene-check skills in github.com/anthropics/knowledge-work-plugins, sales folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Built on the Pipeline Analyst agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors), adapted; third-party named methods left out. Built on the revops skill in github.com/coreyhaines31/marketingskills (MIT, © 2025 Corey Haines), adapted. Built on the PostHog handbook, /contents/ folder, CRM page (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
