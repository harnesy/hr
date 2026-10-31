---
name: analysis-notebook
description: Run an analysis so anyone can re-run it and get the same numbers: a frozen data snapshot, the queries, the code, parameters and random seed in one place, assumptions written down, and a short result for the person who asked. Use for any analysis whose result will inform a decision or be repeated.
---

# Analysis notebook

An analysis that cannot be re-run cannot be checked. This skill keeps the data version, the queries, the code, the settings and the seed together, so a colleague can rebuild every number months later, and writes the result in plain words.

**Route:** question → **analysis-notebook** → review by a second analyst (for important work) → result to the person who asked.
Before this skill: a question and the decision it informs. After it: the result, and a folder anyone can re-run.

## When to use

- A question whose answer will inform a decision.
- Any analysis likely to be repeated (monthly, after the next release).
- Modelling work (forecasts, classifiers) before it becomes a model with a `model-card`.

## Inputs

- The question, the decision it serves, the decision owner and the deadline.
- The data sources, their owner and a read-only way to them.
- How much assurance the work needs: a quick look for an internal question needs less checking than a number going to the board.

## Rules

- Read-only on production data; analyse a snapshot.
- Outputs (tables, charts, files) are produced by the code and can be thrown away and rebuilt; nothing is edited by hand.
- Personal data: take only the columns the question needs; aggregate as early as possible; drop direct identifiers; ask the privacy specialist when unsure.
- Correlation is reported as association; a causal claim needs a design that supports it (an experiment or a stated method with its assumptions).
- Every number in the result points to the step that produced it and the date of the snapshot.

## Steps

1. **Write the question** and how the answer will be used, in a few lines at the top of the notebook or README.
2. **Freeze the data:** export a snapshot (or record the exact table versions and query time) and record where it is stored and when it was taken.
3. **Keep settings in one place:** paths, dates, filters and the random seed in a configuration file or one cell at the top, not scattered in the code.
4. **Record the environment:** language and library versions.
5. **Work in order:** load → check (row counts, missing values, ranges; use `data-quality-checks` where needed) → transform → analyse → output. The notebook must run top to bottom without manual steps.
6. **Write assumptions and limits** as you go: what was excluded and why, what the data cannot show, where uncertainty is large.
7. **Test the parts that matter:** small checks on functions that compute key numbers; compare totals with a known figure.
8. **Re-run from a clean start** and confirm the numbers match.
9. **Write the result:** the answer in plain words first, then the key numbers with their uncertainty, then the limits. For important work, ask a second analyst to review before sending.

## Checks before hand-over

- The notebook runs from a clean start and gives the same numbers.
- Snapshot location and date, versions and seed are recorded.
- Assumptions, exclusions and limits are written.
- No personal data in outputs; identifiers dropped.
- No causal claim without a design that supports it.

## Artefacts

- `analysis/<name>/`: README (question, decision, how to run), configuration, code or notebook, environment file, link to the snapshot.
- `analysis/<name>/result.md`: the answer for the person who asked.

## Hand-over

- **To the person who asked** (often the product manager): the result.
- **To a second analyst** (data analyst or another data scientist): the folder for review, for important work.
- **To the ML engineer:** a model worth taking further, with its notebook and a draft `model-card`.
- **To the data engineer:** data problems found.

## Sources

Built on «Quality assurance of code for analysis and research» by the Government Analysis Function (https://github.com/best-practice-and-impact/qa-of-code-guidance, commit fa39f20; Crown copyright) and «The AQuA Book» (2025, https://www.gov.uk/guidance/the-aqua-book). Contains public sector information licensed under the Open Government Licence v3.0. Built on the Inspect AI documentation on eval logs (github.com/UKGovernmentBEIS/inspect_ai, commit 4acfd20; MIT, © 2024 UK AI Security Institute), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
