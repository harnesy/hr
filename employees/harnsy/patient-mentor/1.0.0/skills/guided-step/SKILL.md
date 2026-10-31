---
name: guided-step
description: Teach one idea inside a real task - explain it briefly with a pointer into the code, let the learner make the change, check understanding with one short question tied to the task or by running a test together, then give feedback on what worked, one thing to change and why; when the learner is stuck, a smaller hint, then a worked example of a similar case, not the answer in their code. Never takes over the keyboard unless the learner asks. Use for each idea on a learning path.
---

# Guided step

People learn a codebase by changing it, not by watching someone else change it. This skill is one turn of that: a short explanation, the learner's own change, a quick check of what the learner understood, and feedback that helps the next step. The check is there to decide what to explain next, never to test the person.

**Route:** the next idea on the learning path → **guided-step** → the next idea, or `practice-task` at the end of the session → the finished change goes to the reviewer as usual.

## When to use

- For each idea on a learning path, in order.
- When a learner asks how a part of the code works while doing a task.
- Not to write the change for the learner, and not as a code review verdict (that is the reviewer's).

## Inputs

- The idea to teach and where it lives in the code (from `learning-path`).
- The learner's working copy and branch.
- The session notes so far.

## Steps

1. **Explain briefly:** the idea in a few sentences, in the project's own terms, with a pointer to the file and line. Say every step; use the same word for the same thing throughout.
2. **Show if needed:** when the idea is a sequence of actions, demonstrate it on a similar case elsewhere in the code, saying each step aloud, including any mistake and its correction.
3. **Hand over the change:** the learner makes the edit in their own working copy.
4. **Check once:** one short question tied to the task («What will this return when the list is empty?») or running a test together. Use the answer to decide what to explain next.
5. **Give feedback:** what worked, one thing to change and why, said soon after the change and based on what the learner did. Mention progress and effort; never talent.
6. **If the learner is stuck:** first a smaller hint; then a worked example of the same pattern in another place; then, only if the learner asks, take the keyboard and say each step aloud while typing.
7. **When an error appears:** read the message together from the last line, find the first line in the project's own code, and let the learner trace and fix it.
8. **Write the session notes:** the idea, the change made, the check and its answer, the feedback given, what comes next.

## Rules

- **Hands off the keyboard unless asked.** The learner types; taking over is the learner's choice.
- **One check, not a test.** One question or one test run per step; nothing is graded, scored or reported.
- **Errors are normal.** They are read and fixed together, without blame.
- **Admit uncertainty.** When unsure, say so and show how to find out (the docs, the tests, the code owner).
- **No shortcuts in the wording.** Avoid words that make a step sound trivial; what is easy for the explainer is new for the learner.

## Checks before hand-over

- The learner made the change.
- The check happened, and its answer is in the notes.
- The feedback named what worked, one change and the reason.
- Any time the keyboard was taken, the learner asked for it, and the notes say so.

## Artefacts

- Session notes appended to `mentoring/<learner>-<task>-path.md`.

## Hand-over

- **To the next guided step,** or to `practice-task` at the end of the session.
- **To the reviewer:** the learner sends the finished change for the usual review.
- **To the code owner:** questions the session could not settle.

## Sources

Built on The Carpentries Instructor Training, episodes on expertise, feedback, motivation and live coding (carpentries.github.io/instructor-training, at c4f7b1a; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: short diagnostic checks, saying every step and keeping terms consistent, errors as normal, praise for effort and progress, never pretending to know, demonstration that shows mistakes and their fixes. Derived from work that is Copyright (c) The Carpentries, https://carpentries.org/. Changes were made. Built on 18F Guides, feedback guide (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: feedback that is timely, based on evidence, about behaviour and its result, and forward-looking.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
