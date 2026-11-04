---
name: coaching-notes
description: Turn patterns from reviewed support replies into coaching notes for the support team lead only: ticket ids, what the replies did against the anchor, the likely cause (skill, process, tool, product, missing help article), what to keep doing and a suggested practice topic, each note marked «not a performance rating». Use after each review cycle. Never rates people or recommends action about them.
---

# Coaching notes

Review only helps if it changes the next reply. This skill groups what the scorecards found into short notes the support team lead can use in one-to-ones and team sessions. It separates what training can fix from what a process, a tool, the product or the help content must fix, and sends each part to the person who can act.

**Route:** scorecards and tallies from `reply-scorecard`, records from `calibration-session` → **coaching-notes** → the support team lead (only) → process, product and help-content causes to their owners.

## When to use

- After each review cycle.
- When a single reply caused or nearly caused harm (the lead needs it quickly).
- Not for performance reviews, ratings, rankings or decisions about people: those belong to the support team lead and are never drafted by the agent.

## Inputs

- Scorecards and the tally for the period.
- The calibration record, if any.
- The current anchors and the team's help articles and procedures.

## Steps

1. **Find patterns.** The same criterion scored weak in several replies, or a strength that repeats. One weak reply is a data point, not a pattern; say so.
2. **Sort the cause** for each pattern:
   - **skill or knowledge:** the writer did not know or did not apply something;
   - **process:** the procedure is unclear, missing or contradicts another;
   - **tool:** the help desk made the right step hard;
   - **product:** a product limit or bug drives the problem;
   - **help content:** an article is missing or wrong.
3. **Write each note:** the ticket ids, what the replies did (quoted, short), what the anchor expects, the likely cause, and one suggested practice or training topic. Add what to keep doing.
4. **Mark every note «not a performance rating».**
5. **Split by owner.** Skill notes go to the support team lead. Process notes go to the support team lead as a procedure question. Product causes go to the product owner, through the team lead. Missing or wrong articles go to the knowledge base writer.
6. **When a case should have gone up:** note which escalation criteria it met (impact, what was tried, steps to reproduce, what is needed) and propose a clearer escalation rule if the rule was the problem.

## Rules

- **To the team lead only.** Notes never go to a public channel, to the whole team, or to the reply's writer directly; the lead decides how to use them.
- **Facts only.** Ticket ids and observable reply facts; no guesses about motives, character or private circumstances.
- **No ratings.** No score per person, no ranking, no recommendation about pay, discipline, schedules or employment.
- **Strengths count.** Every note set includes what works.

## Checks before hand-over

- Every note carries ticket ids, the anchor, the cause category and «not a performance rating».
- Process, product and help-content causes are routed to their owners.
- No note names a person's character or private life.
- Nothing is addressed to anyone but the support team lead and the named owners of process, product and help content.

## Artefacts

- `support-quality/<period>/coaching-notes.md`: for the support team lead.
- `support-quality/<period>/routed-causes.md`: process, product and help-content items with their owners.

## Hand-over

- **To the support team lead:** the coaching notes, only.
- **To the knowledge base writer:** missing or wrong help articles, with ticket ids.
- **To the product owner, through the support team lead:** product causes with the customer impact.

## Sources

Scope from the O*NET 31.0 Database, 43-1011.00 First-Line Supervisors of Office and Administrative Support Workers (nearest occupation): guiding staff on difficult cases, training and procedure tasks only; evaluating people excluded. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. Adapted from the customer-escalation skill in github.com/anthropics/knowledge-work-plugins, customer-support folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Built on the PostHog handbook, /contents/ folder, customer support pages (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
