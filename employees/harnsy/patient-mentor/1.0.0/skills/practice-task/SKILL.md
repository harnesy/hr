---
name: practice-task
description: Write one small follow-up exercise in the same codebase that uses what the learner met in the session in a slightly new place, with a way to check it (a test to make pass, or a command and its expected output) and two hints written in advance, for the learner to try alone and look at together next time. Use at the end of a mentoring session.
---

# Practice task

An idea understood once in a session fades unless it is used again. This skill leaves the learner one small, real piece of work that uses the same idea in a slightly different place, with a clear way to tell when it is done and two hints ready for when it gets hard.

**Route:** the session notes → **practice-task** → the learner tries it alone → the result is looked at together in the next session (`guided-step`).

## When to use

- At the end of a mentoring session.
- When a learner asks for something to try on their own.
- Not as a test or an assessment, and not as a course exercise for many people (that is the learning designer's work).

## Inputs

- The session notes: the ideas met and how the learner got on with each.
- The codebase: a place where the same idea is used, or could be, in a slightly new form.

## Steps

1. **Pick one idea** from the session, preferably the one the learner found hardest.
2. **Find a real place** in the same codebase where it applies a little differently: another endpoint, another parser, an edge case not yet covered. Prefer an easy, non-critical piece of real work over an invented one.
3. **Write the task** in three or four sentences: what to change, where, and what done looks like.
4. **Write the check:** a test to make pass (existing or written in advance), or a command and its expected output.
5. **Write two hints** in advance: the first points to where to look, the second shows the shape of the change on a similar case.
6. **Size it:** small enough to finish in under an hour alone; if not, cut it.
7. **Hand it to the learner** with the check and the hints, and agree when to look at it together.

## Rules

- **Small and real.** One idea, one place, in the learner's own codebase.
- **A clear check.** The learner can tell alone whether it works.
- **Not graded.** The result is looked at together and talked through, never scored or reported.
- **Safe to try.** The exercise runs in the learner's working copy; nothing touches shared or live systems.

## Checks before hand-over

- The task uses one idea from the session.
- The check exists and runs.
- Two hints are written.
- It fits in under an hour.

## Artefacts

- `mentoring/<learner>-practice-<n>.md`: the task, the check, the two hints, the agreed time to look at it.

## Hand-over

- **To the learner:** the exercise.
- **To the next session:** the result, looked at together with `guided-step`.
- **To the team lead:** only with the learner's agreement, a note that learning time is needed when the same gap keeps coming back.

## Sources

Built on The Carpentries Instructor Training, episodes on practice and learning, memory, and motivation (carpentries.github.io/instructor-training, at c4f7b1a; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: practice and reflection help an idea stay, authentic tasks motivate. Derived from work that is Copyright (c) The Carpentries, https://carpentries.org/. Changes were made. Built on Open Source Guides, «How to contribute» and «Building welcoming communities» (Open Source Guides authors; CC BY 4.0), adapted: small, clearly scoped first tasks, easy non-critical work kept for people who are learning. Content based on github.com/github/opensource.guide used under the CC-BY-4.0 license.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
