---
name: reader-test
description: Test a document with real readers by paraphrase - each reader reads one section and says in their own words what it means and what they would do, notes kept in their words, never corrected; open questions only; consent and no names in notes. At least three readers (or the document owner when no readers are available) for a quick check, six to nine for public documents; the number of readers and the limits are always reported. Use after a rewrite, then revise and test again.
---

# Reader test

A document works when its readers understand it and do the right thing. Asking them «is this clear?» tells you little; asking them to say in their own words what a section means, and what they would do next, shows exactly where they go wrong. This skill runs a small paraphrase test, reports the number of readers honestly, and feeds the misreadings back into the text.

**Route:** `plain-language-rewrite` + `readability-check` → **reader-test** → revise → test again → the document owner and the editor.

## When to use

- After a rewrite, before a document goes to the public.
- When a document generates calls, complaints or mistakes.
- For short documents and sections. Long documents and forms are better tested with a usability session (the ux researcher's work); focus groups are for learning about readers, not for testing text.

## Inputs

- The text, split into sections.
- Who reads it, and what they must do after reading.
- Readers like the real ones, who agreed to take part; or the document owner when no readers are available (say so in the report).

## Steps

1. **Plan the round.** Number of readers: at least three for a quick check, six to nine for a document going to the public. Fewer than six finds the big problems only; say so in the report.
2. **Consent.** Each reader agrees before the test and hears that the text is being tested, not them. Notes use R1, R2 … and no names or contact details.
3. **Write the questions** per section, open and neutral: «In your own words, what does this section say?», «What would you do if you got this?», «Is there anything here that might confuse other people?». No yes or no questions; nothing that hints at the answer.
4. **Run each test one-on-one.** The reader reads one section, then answers. Write their words as said. Never correct them or explain the text during the test.
5. **Mark misreadings.** For each section, compare the paraphrase and the intended action with what the text should lead to. A reader who «understood every word» but would do the wrong thing is a misreading.
6. **Tally** misreadings per section: n of N readers.
7. **Revise** the sections with misreadings, listing what changed and why. Changes of substance go to the owner, as in a rewrite.
8. **Test again** with new readers, at least once, until no section is misread by more than one reader, or the remaining problems are listed for the owner.

## Rules

- **The text is tested, not the reader.**
- **Report n.** Every result says how many readers took part and what that number can and cannot show.
- **Readers' words, not yours.**
- **No names in notes;** consent from everyone; a reader who wants to stop, stops.
- **Meaning first.** A revision that changes a duty, deadline or amount goes to the owner before use.

## Checks before hand-over

- Questions are open and neutral.
- Every reader's consent is recorded without their name.
- Each section has a tally of misreadings, n of N.
- The report states the number of readers and its limits.
- Revisions are listed, and the second round's results are attached.

## Artefacts

- `documents/<name>/reader-test-plan.md`: sections, questions, number of readers.
- `documents/<name>/reader-notes/R1.md` … : notes in readers' words, no names.
- `documents/<name>/reader-test-report.md`: misreadings per section (n of N), changes made, second-round results, limits.

## Hand-over

- **To the document owner:** the report and the revised text for confirmation.
- **To the editor and proofreader:** the confirmed text.
- **To the ux researcher, where there is one:** the notes, if the document is part of a larger service under study.

## Sources

Built on the Plain Language Guide Series, Digital.gov (U.S. General Services Administration), pages on testing and paraphrase testing, adapted. Built on the GOV.UK Service Manual, «Using moderated usability testing» (Government Digital Service, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Methods, «Usability testing» and «Privacy» (18F, U.S. General Services Administration; CC0 1.0), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
