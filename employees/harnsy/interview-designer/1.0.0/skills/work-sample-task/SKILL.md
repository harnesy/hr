---
name: work-sample-task
description: Design a fair work sample for a hiring stage: a small, job-related version of real work with a stated time cap, paid or unpaid terms, what it measures, and a promise that the result is never used in production. Use when an interview stage needs a task, take-home or exercise. The hiring manager decides on pay and use.
---

# Work sample task

A good work sample shows a skill the job needs from day one, in a short time, on a problem the candidate can understand without inside knowledge. A bad one is free labour or a test of how many evenings someone can give up. This skill writes the good kind and flags the bad kind.

**Route:** approved kit (from `interview-kit`) → **work-sample-task** → the hiring manager approves the task and its terms → the recruiter sends the brief → one interviewer reviews the result before the interview.

## When to use

- A stage in the kit calls for a task, take-home, exercise or live problem.
- Someone proposes a task and wants it checked before candidates see it.
- The job has changed and an old task may no longer match it.
- Not for scoring the results: interviewers rate against the kit, and the hiring manager decides.

## Inputs

- The approved kit: which competencies the task must show.
- The job notes: which skill is critical on day one.
- The hiring manager's answers on **pay** (paid or unpaid; any amount is the manager's, never suggested by the agent) and the **time cap**.
- Who reviews the result, and when.
- The country (rules on unpaid work and candidate data differ; questions go to an employment professional through the HR generalist).

## Steps

1. **Pick the skill.** Name the one or two competencies from the kit the task shows. If a conversation could show them just as well, say so and propose no task.
2. **Invent the problem.** Draw on the kind of work the job does, but make the problem up. Never use a ticket, document, dataset or design from the live backlog or from a client. Give all context in the brief.
3. **Size it.** The task fits inside the time cap with room to spare. Write the cap in the brief («stop at two hours and tell us where you got to»).
4. **Offer an equal alternative** where possible: for example, an existing piece of work the candidate is free to share and discuss instead.
5. **Write the candidate brief:**
   - what the task is and which competencies it shows;
   - the time cap and that stopping at it is expected;
   - **paid or unpaid**, as the hiring manager decided;
   - that the work stays the candidate's and is **never used in production**;
   - how it will be discussed (who reads it, what the follow-up conversation covers);
   - how to ask for an adjustment (more time, another format) or the alternative;
   - whether any AI tool takes part in reviewing it, and how.
6. **Write the review guide** for the interviewer: what to look at, how each competency's levels from the kit apply, and three or four questions about the candidate's choices.
7. **Check against live work.** If the draft looks like real work for the company, or would take longer than a short session, stop and propose either cutting it down or paying for it. The hiring manager decides.

## Rules

- Every brief states paid or unpaid, the time cap and «not used in production». No exceptions.
- No task asks for, or depends on, anything about protected traits, and none requires paid tools or equipment the candidate may not have.
- The agent never rates the submitted work.
- Submissions stay inside the hiring project and are kept only as long as the owner's rule says.

## Checks before hand-over

- The task maps to named competencies in the kit.
- The problem is invented; nothing comes from live work or a client.
- The brief states pay terms, time cap, «not used in production», how it is discussed, adjustments and any AI use.
- A reviewer is named and has the review guide.
- The same task and brief go to every candidate at this stage in the round.

## Artefacts

- `hiring/<role>/work-sample/brief.md`: the candidate brief.
- `hiring/<role>/work-sample/review-guide.md`: what the reviewer looks for and the questions to ask.
- `hiring/<role>/work-sample/decisions.md`: pay, time cap and use as the hiring manager decided, with the date.

## Hand-over

- **To the hiring manager:** the task, the brief and the open points on pay and size, for a decision.
- **To the recruiter:** the approved brief to send to candidates.
- **To the reviewing interviewer:** the review guide, before the interview.

## Sources

Built on the «Work Samples and Simulations» page of the U.S. Office of Personnel Management (a work of the U.S. government; used for method, US). Also built on the 18F Guides, engineering hiring pre-work page (18F, U.S. General Services Administration; CC0 1.0) and the Sourcegraph handbook (archived) work-sample project page (© 2021 Felix Frederick Becker; Apache License 2.0). Changed by harnsy. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
