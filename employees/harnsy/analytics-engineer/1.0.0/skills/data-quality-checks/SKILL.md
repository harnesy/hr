---
name: data-quality-checks
description: Write and run read-only checks that find bad rows in data (duplicates, missing values, unexpected values, broken links between tables, late or missing loads) and report them with counts and examples. Use before an analysis or release that depends on a table, after a pipeline change, or when a number looks wrong.
---

# Data quality checks

A check is a query that returns the rows that break a rule. Zero rows means the rule holds. This skill writes such checks, runs them without changing anything, and reports what failed so the owner of the data can fix it.

**Route:** a table or pipeline to trust → **data-quality-checks** → a report → the data owner fixes → checks run again.
Before this skill: the table(s), what they should contain, and who owns them. After it: a report for the owner; fixes are theirs.

## When to use

- Before an analysis, a dashboard release or an experiment readout that depends on a table.
- After a change to a pipeline or a model.
- When a number looks wrong and the data is the first suspect.
- On a schedule, for tables many people depend on.

## Inputs

- The table(s) and the grain of each (what one row means).
- The rules the data must follow: keys, allowed values, links to other tables, ranges, freshness.
- A read-only way in: a read-only database user, a read-only file, or an exported snapshot.

## Rules

- Read-only. Checks only select. The skill never deletes, updates or «cleans» rows; a fix is a proposal for the data owner (current → change → effect → undo).
- Reports show counts and a few example keys, never full personal records. Mask personal fields in examples.
- Each check has a name, a reason and an owner who is told when it fails.

## Steps

1. **List the rules** per table, starting with the ones that would silently break results:
   - key unique and not null;
   - required columns not null;
   - columns with a fixed set of values contain only those;
   - every foreign key has a matching row;
   - values in a sensible range (no negative amounts, dates not in the future);
   - freshness: the newest row is recent enough; row count per day within the usual band.
2. **Write each rule as a query returning failing rows.** Put them in one checks file, each with a `-- check: <name>` header (see `scripts/checks.example.sql`).
3. **Run the checks** on a read-only connection. For SQLite files use `scripts/run_checks.py`. For other databases, connect with a read-only user using your own driver or client, or export a snapshot to SQLite, and run the same queries.
4. **Read the failures:** how many rows, since when, which source. Look at a few examples (masked).
5. **Write the report:** per check pass or fail, count, examples, likely cause, effect on results that depend on it, owner.
6. **Propose fixes** to the owner as proposals; do not apply them. Re-run the checks after the owner's fix.

## Checks before hand-over

- Every check is a single read-only query; nothing was written.
- Each failure has a count, examples with personal fields masked, and an owner.
- The report says which analyses or dashboards are affected.
- The check file is saved so the same checks can run again.

## Artefacts

- `checks/<table>.sql`: the checks.
- `checks/report-<date>.md`: results, causes, effects, owners.

## Hand-over

- **To the data engineer** (pipelines and sources) or **the analytics engineer** (models): failures they own, with proposed fixes.
- **To the product analyst, data analyst or BI dashboard developer:** which results are affected until it is fixed.
- **To the privacy specialist:** personal data found where it should not be.

## Scripts

`scripts/run_checks.py` — runs the checks from a `.sql` file against a SQLite file opened read-only. It refuses any check that is not a single `SELECT` or `WITH` query. Prints pass or fail, the count and up to five failing rows; `--json` for machine output. Exit code 0 all passed, 1 some failed, 2 error. Standard library only, no network. SQLite only; for other databases see step 3.

```
python3 scripts/run_checks.py --db warehouse-snapshot.sqlite scripts/checks.example.sql
python3 scripts/run_checks.py --db warehouse-snapshot.sqlite checks/orders.sql --json
```

## Sources

Built on the dbt Developer Hub docs (data tests; commit 71495a0 of github.com/dbt-labs/docs.getdbt.com; Apache License 2.0, © dbt Labs), adapted. Built on «Quality assurance of code for analysis and research» by the Government Analysis Function (https://github.com/best-practice-and-impact/qa-of-code-guidance, commit fa39f20; Crown copyright). Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
