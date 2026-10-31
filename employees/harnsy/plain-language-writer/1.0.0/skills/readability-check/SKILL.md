---
name: readability-check
description: Count the usual suspects in an English text with a small script - sentences over 25 words, paragraphs over five sentences or 150 words, likely passives, hidden verbs (nouns ending in -tion, -sion, -ment, -ance), negative contractions and long words - then review every flag by hand. Counts, not a verdict - no grade, no named formula, never «this text is plain». Use on a draft or a rewrite before readers test it.
---

# Readability check

Some patterns make texts harder to read: long sentences, long paragraphs, passive sentences that hide who must act, verbs turned into nouns. A script can find them quickly; only a person can decide whether each one is a problem. This skill runs the counts, reviews each flag, and keeps the report next to the text. It gives counts, not a verdict.

**Route:** a draft or a rewrite (`plain-language-rewrite`) → **readability-check** → fixes → `reader-test` → the document owner and the editor.

## When to use

- After rewriting a document, before testing it with readers.
- To find where to start on a long, dense document.
- Not to score or grade a text, and not as evidence that a text meets any rule or standard.

## Inputs

- The text as plain text or Markdown (one file).
- Who reads it, and what they must do after reading.

## Steps

1. **Run the script** (see Tools) on the file.
2. **Read the totals,** then each list of flags.
3. **Long sentences** (over 25 words): split where a sentence carries more than one idea; long conditions become «if …, then …» in two sentences, or a list.
4. **Long paragraphs** (over five sentences, or over about 150 words; never over 250): one topic per paragraph, with a first sentence that says what it is about.
5. **Likely passives:** where it matters who acts, name the actor in active voice («you must send», «we will pay»). Keep the passive where the actor is unknown, unimportant, or the law itself.
6. **Hidden verbs:** where a verb says it shorter, use it («carry out an assessment of» → «assess»). Many such nouns are fine; leave those.
7. **Negative contractions:** spell them out («do not») where a misread would matter, such as a duty or a prohibition.
8. **Long words:** replace with an everyday word where one exists; keep a specialist term the reader needs, and explain it the first time.
9. **Record your decisions:** for each flag, changed or kept, with the reason in a few words. False alarms are recorded as such.
10. **Run again** on the changed text and keep both reports.

## Rules

- **Counts, not a verdict.** Never write that a text is plain, clear or meets a standard because of a count.
- **No grade or formula score.** The script reports counts only.
- **Meaning first.** A change made to clear a flag must not change a duty, deadline, amount or condition; such sentences go to the document owner.
- **People decide.** Readers, not counts, show whether a text is understood.

## Checks before hand-over

- Every flag has a decision: changed, kept (with reason), or false alarm.
- The second run is attached.
- No sentence with legal meaning was changed without being listed for the owner.

## Artefacts

- `documents/<name>/readability-1.md` and `readability-2.md`: the script's reports before and after.
- `documents/<name>/readability-decisions.md`: one line per flag.

## Hand-over

- **To the document owner and the editor and proofreader:** the reports and the decisions, next to the rewrite.
- **To `reader-test`:** the changed text, ready for readers.

## Tools

- `python3` 3.8 or newer, standard library only, no network.
- `python3 scripts/readability_counts.py rewrite.md` prints totals and lists every flag with its place (paragraph.sentence).
- `--max-sentence 25`, `--max-par-sentences 5` and `--max-par-words 150` set the thresholds; the defaults come from the sources below.
- Headings and code blocks are skipped; each list item counts as a paragraph. The passive and syllable counts are rough by design: expect false alarms and some misses.

## Sources

Built on «Writing to GOV.UK standards», writing guidelines (Government Digital Service, Crown copyright), adapted: sentences over 25 words, paragraphs of at most five sentences, active voice by default, negative contractions. Contains public sector information licensed under the Open Government Licence v3.0. Built on the Plain Language Guide Series, Digital.gov (U.S. General Services Administration), adapted: spotting passives, hidden verbs, paragraph length.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
