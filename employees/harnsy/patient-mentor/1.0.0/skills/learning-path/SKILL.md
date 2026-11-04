---
name: learning-path
description: Plan what one learner needs to understand to do one real task in this codebase - find what the learner already knows with two or three questions, list the ideas the task needs from the closest to the furthest, tie each to the file or function where it lives with something small to look at there, mark new versus refreshed, and keep three to five new ideas per session. Use at the start of a mentoring task, before any explaining.
---

# Learning path

A task in an unfamiliar codebase asks for many things at once: how requests flow, where data lives, the project's own patterns, the tools. Explaining all of it up front buries the learner. This skill finds where the learner stands, picks out only the ideas this task needs, and puts them in an order that starts from what the learner already knows, each one tied to a real place in the code.

**Route:** one real task and one learner → **learning-path** → `guided-step` for each idea → `practice-task` at the end of the session.

## When to use

- At the start of mentoring on a real task, before explaining anything.
- When a learner returns to the same codebase after a gap, to refresh the path.
- Not for designing a course for many people (that is the learning designer's work), and not for the people side of joining a team (the onboarding specialist's).

## Inputs

- The task: the work item, the expected result, the branch.
- The codebase: readme, contributing guide, licence, conduct rules, the parts of the code the task touches.
- The learner's own description of their experience.

## Steps

1. **Orient in the project first:** read the readme, the contributing guide, the licence and the conduct rules; note who owns the parts the task touches; search earlier issues and discussions on the same area.
2. **Ask two or three short questions** to find what the learner knows and how they picture the part of the system involved, for example «What do you think happens between the request arriving and the row being saved?». Record the answers as they are.
3. **List what the task needs:** each idea, pattern or tool the learner must understand to finish it. Leave out anything the task does not need.
4. **Order the list** from the idea closest to what the learner knows to the furthest, so each step builds on the last.
5. **Tie each idea to the code:** the file and function where it lives, and one small thing to look at there (a call, a test, a log line).
6. **Mark each idea** «new» or «refresh».
7. **Cut it into sessions** of three to five new ideas each; start with a small, clearly scoped piece the learner can finish early.
8. **Show the path to the learner** and adjust the order with them.

## Rules

- **The learner's task, the learner's code.** Ideas are explained where they live in the real codebase, not with invented examples.
- **Few new ideas per session.** Three to five; the rest wait for the next session.
- **Answers are information.** A wrong answer to a starting question shows how the learner pictures the system; it is recorded, never graded.
- **Private to the learner.** The path and the answers are not an assessment and are not shared without the learner's agreement.

## Checks before hand-over

- Every idea on the path is needed for the task.
- Every idea points to a file or function and to something to look at there.
- No session holds more than five new ideas.
- The learner has seen the path and agreed the order.

## Artefacts

- `mentoring/<learner>-<task>-path.md`: the learner's starting answers, the ordered ideas with their code locations and «new» or «refresh», and the session cut.

## Hand-over

- **To `guided-step`:** the first idea of the first session.
- **To the learning designer:** gaps that need a course rather than a session, with the learner's agreement.
- **To the code owner:** questions about the code that the documentation does not answer.

## Sources

Built on The Carpentries Instructor Training, episodes on practice and learning, expertise, and memory (carpentries.github.io/instructor-training, at c4f7b1a; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: find the learner's current picture of the system first, a wrong answer shows a specific misunderstanding, limit new ideas per step, authentic tasks. Derived from work that is Copyright (c) The Carpentries, https://carpentries.org/. Changes were made. Built on Open Source Guides, «How to contribute» (Open Source Guides authors; CC BY 4.0), adapted: read the readme, contributing guide, licence and code of conduct first, learn who does what, gather context before asking, start small. Content based on github.com/github/opensource.guide used under the CC-BY-4.0 license.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
