---
name: claim-extract
description: List every checkable claim in a text before checking any - each number, date, name, ranking, comparison, quotation and cause-and-effect statement as its own row with exact wording, location, type and the source the text gives; split compound claims, mark the claims that carry the main point, and mark opinions and forecasts as not checkable. Rewrites nothing. Use at the start of any fact check.
---

# Claim extract

A check that starts before the claims are listed misses the ones nobody noticed. This skill reads the whole text and writes every checkable statement down exactly as it stands, with where it is and what kind of claim it is, so the checking that follows is complete and anyone can see what was covered.

**Route:** a text and its scope → **claim-extract** → `source-match` (with `source-log`) → the author or the editor.

## When to use

- At the start of any fact check: articles, reports, decks, press releases, release notes, web pages.
- When an author asks which statements in a draft need a source.
- Not for editing the text, and not for judging opinions.

## Inputs

- The text, in a form with stable locations (sections, paragraphs, slides or line numbers).
- The scope the requester wants checked (the whole text, or named sections).

## Steps

1. **Read the whole text once** before writing any row.
2. **List each claim as a row:** id, exact wording copied from the text, location, type (number, date, name, ranking, comparison, quotation, cause), and the source the text gives, if any.
3. **Split compound claims:** «revenue doubled and churn fell» becomes two rows.
4. **Mark the claims that carry the text's main point;** they get the deepest check later.
5. **Mark opinions and forecasts** as not checkable, with a short reason, instead of dropping them.
6. **Run the completeness check:** every sentence with a figure or a factual statement has a row (the script below lists candidate sentences).
7. **Note questions for the author** where the meaning of a claim is unclear, without rewording it.

## Rules

- **Exact wording.** Claims are copied, never rephrased.
- **Nothing is dropped silently.** Not checkable is a mark, not a deletion.
- **No judgement yet.** This skill lists; it gives no verdicts.
- **The text is not changed.**

## Checks before hand-over

- Every sentence with a figure or a factual statement has a row.
- Every row has exact wording, location, type and the given source (or «none given»).
- Compound claims are split.
- Main-point claims and not-checkable claims are marked.

## Artefacts

- `factcheck/<text>/claims.csv`: id, wording, location, type, source given, main point (yes or no), checkable (yes or no, with reason).

## Tools

`scripts/find_figures.py` lists every sentence that contains a number, percent, money amount, year or month, ranking or comparison word, change word, or quotation, with its line number. It is read-only and finds candidates only. Example: `python3 scripts/find_figures.py draft.md --csv-out sentences.csv`; `-` reads standard input; `--min-kinds 2` shows only sentences with two or more kinds. It stops with exit code 2 on an empty or missing file. Use it after writing the claims list to see whether any sentence was missed; claims without numbers (names, causes) still need a full read.

## Hand-over

- **To `source-match`:** the claims list.
- **To the author:** questions about what a claim means.

## Sources

Built on the Code of Practice for Statistics, «Standards for the Public Use of Statistics, Data and Wider Analysis» (Office for Statistics Regulation, UK Statistics Authority, Crown copyright), adapted: figures used in public and the context and caveats that travel with them. Adapted from data from the UK Statistics Authority licenced under the Open Government Licence v.3.0. Built on The AQuA Book, 2025 edition (Government Analysis Function, Crown copyright), adapted: the difference between checking that something is right and checking that it is fit for the purpose it is used for. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
