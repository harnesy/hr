---
name: interviewer-briefing
description: Write a one-page briefing for each interviewer from the approved kit (the competencies they own, questions, probes, scale, how to take notes, topics never to raise, what not to promise) plus the debrief order. Use before each hiring round and whenever a new interviewer joins a panel.
---

# Interviewer briefing

A kit only works if every interviewer uses it the same way. The briefing puts each person's part of the kit on one page, with the rules that keep notes factual and decisions fair.

**Route:** approved kit (from `interview-kit`) and review guide (from `work-sample-task`) → **interviewer-briefing** → interviewers re-read it before each round → independent ratings → debrief → the hiring manager decides.

## When to use

- Before a hiring round opens.
- When someone joins a panel, or swaps in for a colleague.
- After a round where something went wrong in an interview (a question off the kit, a topic that should not have come up): the lesson goes into the next briefing.

## Inputs

- The approved, frozen kit and its panel split.
- The work-sample review guide, if a task is used.
- Who sits on each panel, and the date of the debrief.
- How ratings are submitted (form, file, tool) and the deadline.

## Steps

1. **One page per interviewer.** Contents:
   - a short summary of the role and what the job needs on day one;
   - the competencies this interviewer owns, each with its definition and the description of each level;
   - the questions and fixed probes, in order;
   - the scale and its length;
   - what to hand to the next interviewer (gaps to cover).
2. **How to take notes.** Write what the candidate said or did («ran the release for two years, wrote the rollback steps»), not impressions («strong», «nervous», «not a fit»). Notes never mention or guess a protected trait; a gap in a CV or a change of career is not evidence against anyone. Notes hold facts only and stay inside the hiring project.
3. **Topics never to raise.** Age, family and children, pregnancy, health and disability, religion, origin, sexuality, politics, pay history, and anything similar. If a candidate brings one up, thank them, do not follow it, steer back to the question, and write nothing about it.
4. **What not to promise.** No pay figures, start dates, offers or projects; such questions go to the recruiter.
5. **A quick verdict is a hypothesis.** If a view forms in the first minutes, use the rest of the time to look for evidence against it.
6. **No outside digging.** Do not search the web or social media for candidates beyond links they chose to share.
7. **Independent rating.** Each interviewer writes a rating and its evidence before reading anyone else's, by the stated deadline. Any rating below the top says what was missing.
8. **Debrief order** (one page for the hiring manager): evidence first, in the candidate's words; then each rating; then what would have raised it. Ratings open the discussion; they are never averaged into a decision. Nobody changes a rating only because it differs from the others. The disagreement is written down and the hiring manager decides.
9. **Remind the panel** that candidates were told whether an AI tool takes part, and how adjustments are handled; any adjustment request goes to the recruiter.

## Checks before hand-over

- Each briefing covers only that interviewer's competencies, and all competencies are covered across the panel.
- Questions, probes and levels match the frozen kit word for word.
- The never-raise list and the steer-back line are on every page.
- The debrief guide says evidence first, ratings before discussion, no averaging, and who decides.

## Artefacts

- `hiring/<role>/briefings/<interviewer>.md`: one page per interviewer.
- `hiring/<role>/debrief-guide.md`: the debrief order and the decision line, left for the hiring manager.

## Hand-over

- **To each interviewer:** their briefing, to re-read before each interview day.
- **To the hiring manager:** the debrief guide. The manager runs or chairs the debrief and decides.
- **To the recruiter:** the list of what interviewers must not promise, so candidate questions about pay and dates reach the recruiter.

## Sources

Built on «Structured Interviews: A Practical Guide» (U.S. Office of Personnel Management, September 2008; a work of the U.S. government; used for method, US). Also built on the 18F Guides, engineering hiring interviews and debrief pages (18F, U.S. General Services Administration; CC0 1.0), the TTS Handbook fair and equitable hiring practices page (Technology Transformation Services, GSA; CC0 1.0), the Sourcegraph handbook (archived) interview training page (© 2021 Felix Frederick Becker; Apache License 2.0; changed by harnsy) and the PostHog handbook, how to interview (© 2020-2025 PostHog Inc.; MIT for the /contents/ folder). All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
