---
name: model-with-tests
description: Build or change a data model (a table or view in the warehouse) in any SQL modelling tool together with its tests and documentation, in a development environment first, and hand production changes over as a reviewed proposal. Use when an analysis, metric or dashboard needs a clean, reusable table, or when an existing model must change.
---

# Model with tests

A data model is a piece of code that others will build on. It ships with the tests that show it is right and the documentation that says what each column means, or it does not ship.

**Route:** metric-definition or a request → **model-with-tests** → review → the owner approves the production change → dashboards and analyses use the model.
Before this skill: a definition or question the model must answer, and the source tables it reads. After it: a reviewed change, applied to production only with the owner's OK.

## When to use

- A metric, report or analysis needs a table that does not exist yet.
- The same logic is repeated in several queries and should live in one place.
- An existing model is wrong, slow or must change shape.

## Inputs

- The question or metric definition the model serves.
- Source tables, their owner (usually the data engineer) and freshness.
- The project's conventions: naming, layers (sources → staging → intermediate → marts), the modelling tool and how tests run. Read them before writing.

## Rules

- Work in a development environment or schema; production is read-only for this skill.
- A production change is a proposal: current state → change → expected effect (on downstream models and dashboards) → how to undo it. It is applied only after the owner approves.
- Rename and recast source columns once, in the first layer; later layers use clean names.
- Small models with one clear job each; no copy of logic between models.
- Personal data: select only the columns the purpose needs; mask or aggregate where the consumer does not need detail; ask the privacy specialist when unsure.

## Steps

1. **Write down the grain:** what one row means («one order», «one user per day»). Most model bugs are grain bugs.
2. **Write the model** following the project's layers and naming.
3. **Add data tests** — each a query that returns the rows that break a rule:
   - the key is unique and not null;
   - columns with a fixed set of values contain only those values;
   - every foreign key has a matching row in the table it points to;
   - business rules that must always hold (no negative amounts, end after start).
4. **Add unit tests** with small fixed input rows and expected output for logic that is easy to get wrong: complex conditions, date and time-zone handling, fixes for past bugs, and edge cases not yet seen in the data. Add them before refactoring a model.
5. **Document** the model and every column next to the code: what it means, the unit, where it comes from, known caveats.
6. **Run everything in development:** build, data tests, unit tests. Compare row counts and key totals with the old model or the source.
7. **Check downstream:** list the models, dashboards and reports that read this model and what changes for them.
8. **Prepare the proposal** for production with the undo step, and ask for review.

## Checks before hand-over

- The grain is written and the key test passes.
- Data tests and unit tests pass in development; outputs attached.
- Every column is documented.
- Downstream effects are listed.
- The production change is a proposal with an undo step, not applied.

## Artefacts

- The model code, test definitions and documentation in the project's repository, on a branch.
- `proposal.md`: current → change → effect → undo, with test output and row-count comparison.

## Hand-over

- **To the reviewer** (another analytics engineer or the data engineer): the branch and the proposal.
- **To the owner of the data platform:** the approved proposal to apply.
- **To the BI dashboard developer, data analyst and product analyst:** what is new or changed, from when.
- **To the data engineer:** problems found in source data.

## Sources

Built on the dbt Developer Hub docs (data tests, unit tests, documentation, best-practice workflows; commit 71495a0 of github.com/dbt-labs/docs.getdbt.com; Apache License 2.0, © dbt Labs), adapted. Built on «Quality assurance of code for analysis and research» by the Government Analysis Function (https://github.com/best-practice-and-impact/qa-of-code-guidance, commit fa39f20; Crown copyright). Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
