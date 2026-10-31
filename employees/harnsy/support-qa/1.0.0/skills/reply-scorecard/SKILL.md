---
name: reply-scorecard
description: Score one sampled customer support reply at a time against written anchors (weak, acceptable, strong) for each criterion, quoting the reply line behind every score, and write the verdict before opening the agent's self-assessment or the customer's rating. Use for every reply in a quality review sample. Judges replies, never people; no per-person totals.
---

# Reply scorecard

A scorecard tells a support team which parts of its replies work and which do not. It works only if every reviewer scores against the same written anchors, quotes the evidence, and forms the verdict before reading anyone else's view. It is never a rating of the person who wrote the reply.

**Route:** review sample from the support team lead → **reply-scorecard** (one reply at a time) → tally per team → `calibration-session` when reviewers differ → `coaching-notes` to the support team lead.

## When to use

- Every reply in the review sample the support team lead sets.
- A reply that a customer rated low, before anyone draws a conclusion.
- Not to rate, rank or compare people, and not for performance reviews.

## Inputs

- The sample: ticket ids chosen by the support team lead (a random draw, plus any the lead adds for a reason that is written down).
- The criteria and their anchors, with the version and date. If anchors are missing, draft them for the lead to approve before scoring.
- Read access to the full ticket thread.

## Criteria

Each criterion has three anchors: what a weak, an acceptable and a strong reply looks like. The usual set:

1. **Right answer:** correct and complete for what the customer actually asked.
2. **Authorised commitments only:** no refund, credit, discount, feature or date promised beyond what the reply's writer may promise.
3. **No unreleased plans** shared.
4. **History right:** accurate about earlier messages in the thread; nothing asked again that was already answered.
5. **Clear next step:** who does what, by which exact date.
6. **We checked first:** the customer was not asked for something support could look up itself.
7. **Fit for the reader:** depth and length suit the reader and the channel; the customer's words, not internal jargon; active voice.
8. **Tone** suits the situation.
9. **Suggested text checked:** where the help desk shows an AI-suggested answer, the reply shows it was read and corrected, not pasted.
10. **Billing replies:** the issue classified first (likely duplicate charge, real extra seats, failed payment, missing self-service, product failure), least personal data shown, the decision left to the billing owner.
11. **Escalated when needed:** the reply went up when the case met the team's escalation criteria (impact, what was tried, steps to reproduce, what is needed).

Mark a criterion «n/a» when it does not apply.

## Steps

1. **Read the whole ticket**, then the reply under review.
2. **Score each criterion** against its anchors. Quote the line of the reply that earned the score. No quote, no score.
3. **Write the verdict**: the two or three things that matter most, strengths included.
4. **Only now open** the writer's self-assessment, the customer's satisfaction rating and any other reviewer's score. Note differences; do not change your scores because of them. Differences go to `calibration-session`.
5. **Low rating?** Sort the likely cause before concluding: the reply, a process or tool, a product limit, the customer's expectations, or a hard problem that took time.
6. **Record the scorecard** in the team's sheet: reply id, team, criterion, level, evidence. No column for the person.
7. **Tally the batch** with the script (see Tools): per reply and per team, never per person.

## Rules

- **Replies, not people.** No per-person totals, averages, rankings or league tables, ever. A request for them goes to the support team lead with this reason.
- **Verdict first.** Self-assessments, ratings and other reviewers' scores are read after the verdict is written.
- **Evidence for every score.** Quoted from the reply.
- **Customer data minimum.** Scorecards hold ticket ids and the quoted lines needed, not customer details.
- **Read-only.** The reviewer never edits tickets or replies to customers.

## Checks before hand-over

- Every scored criterion has a quoted line.
- The verdict was written before other opinions were opened (the order is noted in the record).
- The sheet has no column naming a person.
- Low ratings carry a cause category.

## Artefacts

- `support-quality/<period>/scores.csv`: one row per reply and criterion.
- `support-quality/<period>/scorecards.md`: verdicts per reply.
- `support-quality/<period>/tally.md`: the script's output.

## Hand-over

- **To the support team lead:** scorecards, the tally and team trends.
- **To `calibration-session`:** replies where reviewers differ, or where a score differs from the self-assessment by two levels or more.
- **To `coaching-notes`:** patterns across replies.

## Tools

`scripts/scorecard_tally.py` reads the scores sheet (CSV with reply_id, team, criterion, level) and prints, in Markdown, the count of each level per reply and, per team, the count and share of each level for every criterion. Python 3 standard library only, no network.

- Option: `--levels` with the anchor names, lowest first (default weak, acceptable, strong). «n/a» rows are skipped.
- It refuses a sheet with any column that names a person (agent, author, employee, owner, name, email and similar).

## Sources

Adapted from the draft-response and customer-escalation skills in github.com/anthropics/knowledge-work-plugins, customer-support folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Built on the PostHog handbook, /contents/ folder, customer support pages and the «Don't bias yourself» section of how to interview (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted. Built on «Structured Interviews: A Practical Guide» (U.S. Office of Personnel Management, September 2008; a work of the U.S. government; method only, adapted from rating interview answers to rating replies). Built on the customer-billing-ops skill in github.com/affaan-m/ECC (MIT, © 2026 Affaan Mustafa), adapted: classification only.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
