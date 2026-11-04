---
name: prototype-test-plan
description: Plan, run and read out a small round of sessions on a prototype - one research question, pass and fail signals written before the first session, recruiting criteria, tasks and a discussion guide, five sessions by default (four to eight per round), consent, silent observers, a debrief after each session and a tally of each problem by participant. Use before building a prototype and again after the round to write the findings.
---

# Prototype test plan

A small round of sessions tells you whether an idea works, if you decided in advance what «works» means. This skill writes the plan before anything is built, keeps the sessions consistent and fair to participants, and turns the notes into a findings note with each problem counted.

**Route:** an idea and its chosen variant → **prototype-test-plan** (plan) → `prototype-build` → sessions → **prototype-test-plan** (tally and findings) → the ui designer and the product manager.

## When to use

- Before building a prototype: to fix the question, the signals and the tasks the prototype must support.
- After a round of sessions: to count problems and write the findings.
- Not for a large research study across many questions or products: that belongs to the ux researcher, who owns research plans and synthesis across studies.

## Inputs

- The idea, the chosen variant and the decision waiting on the result.
- Who the idea is for.
- The time available, and who can moderate, observe and take notes.

## Steps

1. **One research question.** Write it as a question a session can answer, for example «can a first-time buyer find the delivery date before paying?».
2. **Signals before sessions.** Write what result means pass and what means fail, as counts of participants (for example «pass: 4 of 5 find it unaided within a minute; fail: 2 of 5 or fewer»). Agree them with the product manager. They do not change after the first session.
3. **Who to recruit.** People who use the service now, used it recently, used it long ago, or use something similar. Five sessions by default, four to eight per round. More rounds of a few people each beat one large round.
4. **Write the tasks.** Each task has a clear goal, is believable, is hard enough to show problems, and never hints at the answer or uses the words on the button it tests. Put them in a sensible order.
5. **Write the discussion guide.** Introduction (who we are; the prototype is being tested, not the participant; they may stop at any time; recording only with their spoken consent), the tasks, open follow-ups such as «what makes you say that?», and a short wrap-up.
6. **Consent and privacy.** Every participant agrees before the session; recording is confirmed aloud at the start. Notes keep no names or contact details; participants are numbered P1 to P5. Nobody is asked to bring or show their own documents; where a task needs data, give them an invented character and invented documents.
7. **Roles.** One moderator who mostly stays quiet and lets the participant work; observers write down problems and do not interrupt.
8. **Debrief after each session** (ten minutes): what stood out, the participant's own words, what went well or badly in the session itself, and whether anything must change before the next one (only the session, never the signals).
9. **Tally after the round.** One row per problem, one column per participant, a mark where the problem occurred. Count n of N for each problem.
10. **Read out against the signals.** Compare the counts with the pass and fail signals written in step 2. Write the findings note and recommend keep, change or drop.

## Rules

- **Signals first.** No session before the signals are written and agreed.
- **The prototype is tested, not the person.** Participants hear this before the first task.
- **Small numbers stay small.** Report «3 of 5», never «60 %», and do not generalise beyond what a round of five can show.
- **No real data.** No real personal documents, no production data, no names in notes.
- **Stop when asked.** A participant who wants to stop, stops, and their notes are kept only if they agree.

## Checks before hand-over

- The question and the signals are dated and were written before session 1.
- Every task has a goal and no hint.
- Every participant's consent is recorded (without their name in the notes).
- The tally covers every problem seen, with n of N.
- The findings compare counts with the signals and recommend keep, change or drop.

## Artefacts

- `research/<idea>/test-plan.md`: question, signals, recruiting criteria, tasks, discussion guide, roles, dates.
- `research/<idea>/notes/P1.md` … : session notes without names, and the debrief.
- `research/<idea>/findings.md`: tally table, counts against signals, participants' words without names, recommendation.

## Hand-over

- **To the product manager:** the plan for agreement before the round, and the findings with the keep, change or drop recommendation after it.
- **To the ui designer:** the findings, so the real screens are specified from what people did.
- **To the ux researcher, where there is one:** the raw notes and the tally, for synthesis across studies.

## Sources

Built on the GOV.UK Service Manual, «Using moderated usability testing» and «Plan user research for your service» (Government Digital Service, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Methods, «Usability testing», «Recruiting» and «Privacy» (18F, U.S. General Services Administration; CC0 1.0), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
