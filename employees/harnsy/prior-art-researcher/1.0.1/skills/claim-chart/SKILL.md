---
name: claim-chart
description: Chart an invention's features (or a published patent's claim elements) against references - one row per feature, one column per reference, each cell with the exact quoted passage and its page, column, line or paragraph and figure, and «found», «partly» or «not found»; references never combined in one cell; no conclusion column. Use after a prior-art search, to hand a patent attorney the evidence in a form that can be checked.
---

# Claim chart

A chart puts the evidence where a reader can check it: each feature of an invention against each reference, with the exact passage that shows it and where it is. It does not say what the evidence means in law; that is the patent attorney's job.

**Route:** `prior-art-search` shortlist → **claim-chart** → the patent attorney (a person).

## When to use

- After a search, to present the best references feature by feature.
- To compare a published patent's claim elements with a product description or with other documents, as evidence for an attorney.
- Not to reach a conclusion about novelty, obviousness, validity or infringement.

## Inputs

- The feature list from the search (or, for a published patent, its claim elements, one per row, in the claim's own order).
- The shortlisted references, read in full.

## Steps

1. **Rows:** one per feature or claim element, worded exactly as in the feature list or the claim. Split an element that contains several parts.
2. **Columns:** one per reference, headed with its number, title, publication date (or «undated») and link.
3. **Cells:** for each feature and reference, quote the exact passage that shows the feature, with its location: page, column and line, or paragraph number, and figure and reference numerals. Then mark it «found», «partly» (say which part is missing) or «not found».
4. **One reference per cell.** Never combine two references in one cell; if a feature is shown only by putting two documents together, leave both cells as they are and note it in a comment for the attorney.
5. **Check every quote** against the document itself, not against an abstract or a machine summary; translations are marked as such.
6. **No conclusion column.** Add a note at the top: «This chart shows where features appear in the references searched. Novelty, obviousness, validity and infringement are for the patent attorney.»
7. **Link the log:** every reference in the chart appears in the search log with its date.

## Rules

- **Exact quotes with locations,** never paraphrase in a cell.
- **No legal conclusions** in the chart or in the hand-over.
- **References stay separate.**
- **Dates matter:** a reference without a publication date is marked «undated».

## Checks before hand-over

- Every row has a cell for every reference.
- Every «found» or «partly» cell has a quote and a location.
- No cell combines references.
- The top note is present; there is no conclusion column.
- Every reference is in the search log.

## Artefacts

- `prior-art/<invention>/chart.md` (or a spreadsheet): rows, columns, quoted cells, marks, top note.

## Hand-over

- **To the patent attorney (a person):** the chart with the search log and the shortlist.
- **To the owner:** a plain note of how many features were found where, without any legal conclusion.

## Sources

Built on the Manual of Patent Examining Procedure, section 2217 (Source: United States Patent and Trademark Office, www.uspto.gov), adapted from examiners' practice to a researcher's chart. Built on the WIPO Guide to Using Patent Information (© WIPO 2021, CC BY 3.0 IGO, https://doi.org/10.34667/tind.46546); changes made by harnsy.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
