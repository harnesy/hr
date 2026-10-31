---
name: repro-steps
description: Turn a bug report into the smallest reproduction that fails reliably - the symptom in one sentence, the environment as a table, the fewest steps and data that still fail, the failure rate over a stated number of runs, and the list of things that do not change it - on a copy, never on a live system. Use first on any hard, intermittent or environment-dependent bug, before forming a theory of the cause.
---

# Reproduction steps

A bug that cannot be made to fail on demand cannot be investigated or confirmed fixed. This skill turns «it breaks sometimes» into a short page that anyone can follow to see the failure: what goes wrong, in which environment, with which steps, and how often. It also records what was tried and left the failure unchanged, because that narrows the search as much as what makes it disappear.

**Route:** a bug report with logs → **repro-steps** → `bug-timeline` and the debugging of the cause → the QA engineer keeps the reproduction as a regression test.

## When to use

- First, on any bug that is hard to pin down: intermittent, only in one environment, only with some data, only under load.
- When a fix was made and nobody can say whether it worked.
- Not as a substitute for reading the error: the full message and stack trace come first.

## Inputs

- The report: what happened, what was expected, where and when, who saw it.
- Error messages, stack traces and logs, complete.
- A safe place to run it: a local setup, a test environment or a copy of the data. Not the live system.

## Steps

1. **Restate the symptom** in one sentence: «When X is done with Y, Z happens instead of W.» Confirm it with the person who reported it.
2. **Record the environment** as a table: runtime and its version, dependency versions (from the lock file), database and its version, operating system and browser, configuration and feature flag values, data set, time zone, locale, and anything else the report mentions.
3. **Reproduce it as reported** on the copy. If it does not fail, compare the environment table with where it failed and close the differences one at a time; ask the owner for missing details (an anonymised input, the exact time, a log extract) instead of fetching them from production.
4. **Make it small:** remove steps, inputs and data one at a time, keeping each removal only if the failure stays. Stop when every remaining step is needed.
5. **Measure the failure rate:** run the smallest reproduction a stated number of times (at least 20 for an intermittent bug) and write the count, for example «7 of 20». Do the same with the order of tests or requests fixed, and alone, if order may matter.
6. **List what does not change it:** every variation tried that left the rate the same (retries, a slower or faster machine, a clean cache, another browser). Write the rate for each.
7. **Automate it** where the reproduction can run as a script or a test, so the next person runs one command.
8. **Have it followed:** a second person, or a clean environment built from the instructions alone, runs it and sees the failure at a similar rate.

## Rules

- **Copies only.** Nothing is reproduced on a live system or with live customer data; production details are requests to the owner.
- **Rates, not adjectives.** «Sometimes», «often» and «rarely» are replaced by counts over a stated number of runs.
- **Facts and guesses apart.** The reproduction file holds what was observed; theories of the cause go to the debugging log as hypotheses.
- **Pin what can be pinned.** Runtime and database versions are fixed in the setup, and outside services are replaced by local stand-ins where possible, so the failure belongs to the code.

## Checks before hand-over

- The symptom sentence is confirmed by the reporter.
- The environment table is complete for the failing and the working environment.
- Every remaining step is needed; the failure rate and the number of runs are written.
- The «does not change it» list exists, with a rate for each entry.
- Someone else, or a clean setup, saw the failure from the instructions alone.
- No live system or live data was touched.

## Artefacts

- `debug/<date>-<short-name>/repro.md`: symptom, environment table, steps, failure rate, the «does not change it» list, open requests to the owner.
- A reproduction script or test, if it could be automated.

## Hand-over

- **To `bug-timeline`:** the first-seen time and the environment table.
- **To `debug-root-cause`:** the reproduction as its first two steps.
- **To the QA engineer:** the reproduction, to keep as a regression test once the cause is fixed.
- **To the code owner:** requests for production details, as questions.

## Sources

Built on the GOV.UK Service Manual, «Exploratory testing», «Working in pre-production environments» and «Quality assurance: testing your service regularly» (Government Digital Service, Crown copyright), adapted: a stated goal for each session, recording queries, observations, screenshots and logs so a finding can be replicated, differences between development and production as a common cause, a pre-production environment that mirrors production. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Guides, «Development environments» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: reproducible, documented setups, versions pinned, outside services mocked by default.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
