---
name: calibration-session
description: Run a calibration session so support quality reviewers score the same reply the same way: each reviewer scores a shared set of replies alone with reasons, then the group compares, discusses every gap from the evidence, records the agreed score, checks for common rater errors and proposes clearer anchor text for the team lead to approve. Use on a fixed rhythm and whenever reviewers disagree. Scores replies, never people.
---

# Calibration session

Scores mean something only when reviewers agree on what each level looks like. Calibration finds where they differ and fixes the cause: usually an anchor that reads two ways. Everyone scores alone first, so the discussion starts from independent views. It is the same independence rule an interview debrief uses (see `interview-kit`), applied to replies instead of candidates.

**Route:** the support team lead sets a date or `reply-scorecard` shows disagreement → **calibration-session** → agreed scores and proposed anchor changes → the team lead approves → `reply-scorecard` uses the new anchors from the next period.

## When to use

- On the rhythm the support team lead sets (for example monthly).
- When two reviewers differ by two levels or more on the same reply.
- When anchors change, or a new reviewer joins.
- Not to judge reviewers or support staff: the session record holds reply ids and scores, never names.

## Inputs

- A set of replies (six to twelve is usually enough), chosen to include clear cases and hard ones.
- The current criteria and anchors, with version and date.
- The reviewers taking part (people and this agent).

## Steps

1. **Prepare the set.** Pick the replies, remove customer details that the scoring does not need, and share the full threads.
2. **Score alone.** Every reviewer scores every reply against the anchors, with the quoted line and a reason, and submits before seeing anyone else's scores. This agent scores too, under the same rule.
3. **Put scores side by side.** Per reply and criterion, show each reviewer's level. Mark gaps of one level and of two or more.
4. **Discuss every gap from the evidence.** Each reviewer reads out the quoted line and the reason. The question is which anchor the line meets, not who is right.
5. **Agree and record.** The agreed level for each reply and criterion, with the reason. Where the group cannot agree, record both views; the support team lead decides.
6. **Check for rater errors:**
   - **halo:** one strong point lifting every other criterion;
   - **middle:** everything scored acceptable;
   - **generous or harsh:** one reviewer always above or below the others;
   - **like me:** preferring replies written in one's own style;
   - **bias about the writer:** a score moved by who wrote the reply rather than what it says.
   Report patterns for the group, without naming a reviewer as «the harsh one».
7. **Fix the anchors.** Where gaps repeat on a criterion, the anchor text is unclear: propose new wording with one short example per level.
8. **Record the session**: date, reply ids, scores before and after, agreed reasons, proposed anchor changes.

## Rules

- **Independent first.** No reviewer sees another's scores before submitting.
- **Evidence decides.** Disagreements are settled by the reply's text and the anchors.
- **No names in the record**: reply ids and reviewer letters (A, B, C) only.
- **The team lead approves** anchor changes; until then the old anchors apply.

## Checks before hand-over

- All reviewers submitted before the comparison (the record shows submission times).
- Every gap of two levels or more has a recorded reason.
- Proposed anchor changes include an example per level.
- The record contains no personal names of support staff or customers.

## Artefacts

- `support-quality/calibration/<date>.md`: the session record.
- `support-quality/anchors-proposed-<date>.md`: anchor changes for approval.

## Hand-over

- **To the support team lead:** the session record and proposed anchor changes, for approval.
- **To `reply-scorecard`:** the approved anchors, with a new version and date.

## Sources

Built on «Structured Interviews: A Practical Guide» (U.S. Office of Personnel Management, September 2008; a work of the U.S. government), «Making Candidate Ratings» and Appendix F «Common Rating Errors»; method only, adapted from rating interview answers to rating replies. Built on the PostHog handbook, /contents/ folder, the «Don't bias yourself» section of how to interview (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted. Adapted from the draft-response skill in github.com/anthropics/knowledge-work-plugins, customer-support folder (© Anthropic, PBC; Apache License 2.0), as the shared anchor set. Changed by harnsy.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
