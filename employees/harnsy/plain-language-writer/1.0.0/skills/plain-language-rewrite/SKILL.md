---
name: plain-language-rewrite
description: Rewrite a dense document (policy, letter, instructions, notice) for the people who must act on it without changing what it means - notes of each point first, a rewrite from the notes for the reader's need (most important first, headings, active voice, must, need and can, short sentences, lists for steps), then a point-by-point compare with the original and a list of every change of substance for the owner. Legally required sentences are marked, never rewritten. Use when a document is hard to read and its readers must act on it.
---

# Plain-language rewrite

A plain rewrite keeps everything the original says and makes it easy to find and act on. The risk is not that the rewrite is too simple; it is that a duty, a deadline or a condition quietly changes on the way. This skill works from short notes of each point, rewrites from those notes for the reader, and then compares the result with the original point by point, so every change of substance is visible to the owner.

**Route:** a document from its owner → **plain-language-rewrite** → `readability-check` → `reader-test` → the owner (or a lawyer) confirms meaning → the editor and proofreader.

## When to use

- Policies, letters, instructions, notices, forms and guidance that readers must act on.
- A document that generates many questions or mistakes.
- Not for interface strings inside a product (the ux writer's job) and not for marketing copy (the copywriter's).

## Inputs

- The document and its owner (who can confirm meaning).
- Who reads it, and what they must do after reading.
- Which sentences are legally required, if the owner knows.

## Steps

1. **Notes first.** Read the original and write one short note per point, in order: who, what, when, how much, under which condition. Number the notes.
2. **Find the reader's need.** What must the reader know or do, and by when? That goes first.
3. **Rewrite from the notes,** not from the original sentences:
   - most important information first; headings that say what each section contains, not questions;
   - address the reader as «you» and the organisation as «we» where that fits;
   - active voice with the actor named; «must» for a legal duty, «need» for a step in a process, «can» for an option;
   - one idea per sentence; split sentences over about 25 words; paragraphs of one topic and at most five sentences;
   - verbs, not nouns made from verbs; everyday words; a specialist term the reader needs is explained the first time;
   - numbered lists for steps in order, bullets for options;
   - present tense where possible; no footnotes.
4. **Mark required wording.** Sentences that are legally required stay as they are and are marked for the owner; a plain summary before them can be proposed.
5. **Compare point by point.** Check each numbered note against the rewrite: is every point there, with the same force? Look hardest at duties (must ↔ should ↔ may), deadlines, amounts, conditions, exceptions and who is responsible.
6. **List every change of substance:** anything lost, added, or changed in force, with the original and the new wording. «None found» is a valid result only after the compare in step 5.
7. **Send for confirmation.** The owner confirms meaning; contracts, notices, consent forms and medical or financial texts also go to a lawyer or the responsible professional when the owner asks.

## Rules

- **Meaning never changes** in legal, medical or financial content.
- **Required sentences are marked,** not rewritten.
- **Every change of substance is listed.**
- **The owner decides** and publishes; the writer never sends or publishes the document.

## Checks before hand-over

- Every note from step 1 appears in the rewrite.
- The changes list exists and was made after a point-by-point compare.
- Duties use «must», steps «need», options «can», consistently with the original's force.
- Required wording is marked.
- The readability counts are attached (`readability-check`).

## Artefacts

- `documents/<name>/notes.md`: the numbered notes.
- `documents/<name>/rewrite.md`: the rewrite.
- `documents/<name>/changes.md`: the changes of substance, or «none found» with the date of the compare.

## Hand-over

- **To the document owner:** the rewrite and the changes list for confirmation; legal texts to a lawyer when the owner asks.
- **To the editor and proofreader:** the confirmed rewrite, for style and facts.
- **To `reader-test`:** the rewrite, for testing with readers.

## Sources

Built on «Writing to GOV.UK standards», writing guidelines (Government Digital Service, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on the Plain Language Guide Series, Digital.gov (U.S. General Services Administration), adapted. The notes-then-rewrite-then-compare exercise is an old self-teaching method for writers; described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
