---
name: quiz-build
description: Build a quiz tied to course objectives, with wrong options drawn from real misconceptions, an explanation for every option, a separate answer key, and a list of checks run against named WCAG 2.2 success criteria by number. Use when a course section needs a quiz or an existing quiz needs fixing. Reports checks as «checked against», never as a verdict.
---

# Quiz build

A good quiz teaches while it checks: a learner who picks a wrong option learns which idea led them there. This skill writes such quizzes and checks that every learner can use them.

**Route:** section objectives (from `learning-objectives` or `course-outline`) → **quiz-build** → the requester approves → a person with assistive-technology experience does the final check → the course owner publishes.

## When to use

- A section of a course needs a quiz or a short check.
- An existing quiz is too easy, too confusing or hard to use.
- Not for tests used to rate people for hiring, promotion or pay: those are out of scope.

## Inputs

- The objectives the quiz checks.
- The misconceptions listed for these learners.
- The format the quiz will run in (a learning platform, a form, paper, live polling) and any time limit planned.

## Steps

1. **One objective per question.** Write the objective next to each question. Pick the format from its action: multiple choice for «choose», «spot» or «decide»; a short written answer for «explain»; a small hands-on task for «build» or «fix».
2. **Wrong options are real answers.** For multiple choice, each wrong option is an answer learners actually give, tied to one named misconception. Drop options nobody would pick. Avoid «all of the above», «none of the above» and trick wording.
3. **Explain every option.** One or two lines: why the right answer is right, and for each wrong one, what misunderstanding it shows and where in the course to look again.
4. **Answer key apart.** Keep the key and explanations in a separate file from the questions given to learners, unless the format shows feedback after each answer.
5. **Run the usability checks** and record each one by criterion number:
   - every answer control is tied to its question and any instructions; options sit under their question (1.3.1, 3.3.2);
   - the whole quiz works with a keyboard alone (2.1.1);
   - right and wrong are never shown by colour alone; add text or a symbol (1.4.1);
   - text contrast is checked (1.4.3);
   - images in questions have text alternatives (1.1.1);
   - a time limit can be extended or switched off on request (2.2.1);
   - error messages say what is wrong and how to fix it (3.3.1).
6. **Report the checks** as «checked against WCAG 2.2 success criteria …» with the numbers, each with pass, fix made, or not checked and why. Never sum the results up in one verdict word about the whole quiz; the list of criteria and results is the report.
7. **Recommend a final check by a person** with assistive-technology experience (for example someone who uses a screen reader).

## Rules

- Quiz results are for learning only; no grade from this quiz is used for an HR decision.
- No question asks about, or depends on, learners' personal traits or private life.
- The quiz collects only the answers it needs.

## Checks before hand-over

- Every question names its objective.
- Every wrong option names its misconception, and every option has an explanation.
- The answer key is separate.
- Every listed criterion has a result; the report says «checked against», with no verdict word.
- A final check by a person is recommended and named.

## Artefacts

- `learning/<course>/quiz-<section>.md`: questions for learners.
- `learning/<course>/quiz-<section>-key.md`: answers, explanations, objective and misconception per option.
- `learning/<course>/quiz-<section>-checks.md`: criteria checked by number, results, fixes made.

## Hand-over

- **To the requester:** the quiz, key and check report, to approve.
- **To a person with assistive-technology experience:** the quiz, for the final usability check.
- **To the course owner:** the approved quiz, to publish.

## Sources

This work is derived from work that is Copyright © Software Carpentry, Data Carpentry, Library Carpentry, or The Carpentries: «Collaborative Lesson Development Training», episodes on formative assessment and multiple-choice questions (https://carpentries.org; licensed under CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). Changed by harnsy; no endorsement by The Carpentries is implied. Also built on the 18F Guides accessibility pages on forms, timeouts, colour and images (18F, U.S. General Services Administration; CC0 1.0). Facts only, not text: success-criterion numbers from WCAG 2.2, a W3C Recommendation dated 12 December 2024. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
