---
name: characterization-tests
description: Before changing old or poorly understood code, record what it does today (including its oddities) as deterministic, reviewed tests, so any later change in behaviour shows up at once; no behaviour change is mixed into the same work. Use before refactoring, upgrading, porting or replacing legacy code that has few or no tests.
---

# Characterization tests

Old code often has no tests and no reliable description of what it should do. The safest description is what it does right now. This skill feeds the code a realistic set of inputs, records the outputs, and keeps those recordings as tests. Then any change, intended or not, shows up as a difference.

**Route:** legacy code about to change → **characterization-tests** → recorded behaviour, reviewed and committed → refactoring, upgrade or strangler-slice → the same tests run on every change.
Before this skill: the part of the code to be changed and a way to run it outside production. After it: a committed test suite and a list of surprises for the owner.

## When to use

- Before refactoring, upgrading a runtime or library, or porting code to a new platform.
- Before replacing a part of a system slice by slice, to compare old and new answers.
- When nobody can say for sure what a piece of code does in edge cases.

## Inputs

- The code to be changed and the seam where it can be called: a function, a class, an endpoint, a batch job with input and output files.
- Realistic inputs: typical cases, edge cases, and samples shaped like production traffic with personal data removed or replaced.
- A non-production environment where the code can run with its dependencies stubbed or copied.

## Rules

- Pin today's behaviour, not the desired behaviour. An output that looks wrong is recorded as it is and listed as a surprise for the owner; it is not fixed in this work.
- No behaviour change in the same change set as the tests. Fixes come later, each as its own change that updates a recording on purpose.
- Tests are deterministic: fixed clock, fixed random seeds, stable ids and ordering, fixed locale and time zone. Fields that cannot be fixed are matched by type or pattern, not by value.
- Recordings are reviewed like code before they are committed.
- The build only compares; it never writes new recordings. A recording changes only when someone updates it deliberately and states why.
- No personal data in inputs or recordings.
- Read-only on live systems; inputs come from copies or masked samples.

## Steps

1. **Pick the seam** where behaviour can be observed: what goes in, what comes out, and what side effects happen (files written, messages sent, rows changed).
2. **Collect inputs** that cover real use: common cases, boundaries (empty, zero, very large, unusual characters, dates around month and year ends), known error cases, and masked samples from logs.
3. **Isolate dependencies:** stub the network, the clock, random sources and external services; use a copy of any database the code reads, so side effects can be captured safely.
4. **Make runs repeatable:** run each input twice; anything that differs between runs is either fixed (seed, clock, order) or matched by type.
5. **Record the outputs** and side effects for every input, in a readable format, and save them next to the tests.
6. **Review the recordings** with someone who knows the domain. Mark each odd result as a surprise with a short note; leave the recording unchanged.
7. **Commit** the tests and recordings together, separate from any code change.
8. **Turn on the comparison** in the build, so every later change runs against the recordings and fails on any difference.
9. **When replacing code,** run the same inputs through old and new and compare the answers; differences are either accepted by the owner (and the recording updated with the reason) or fixed.
10. **Keep focused tests too:** recordings show that something changed; small targeted tests explain what each rule is meant to do. Add those as understanding grows.

## Checks before hand-over

- Every test passes twice in a row on unchanged code.
- No code behaviour was changed in this work.
- Recordings were reviewed, and surprises are listed for the owner.
- The build compares and never rewrites recordings.
- No personal data appears in inputs or recordings.

## Artefacts

- Test files and recordings in the code repository, next to the code under test.
- `legacy/<area>-surprises.md`: odd behaviours found, with input, output and a question for the owner.

## Hand-over

- **To the owner of the code:** the surprises list, to decide which behaviours are bugs.
- **To developers:** the suite to run before and after their changes.
- **To the QA engineer:** the recordings as part of regression testing.
- **To strangler-slice:** the inputs and recordings for comparing old and new.

## Tools

The project's own test runner, with a snapshot or «golden file» feature if it has one; a fake clock and seeded random source for the language in use; a diff tool to read changes in recordings.

## Sources

Built on Jest documentation, «Snapshot Testing» (github.com/jestjs/jest, commit 61050e9; © Meta Platforms, Inc. and affiliates and Jest contributors, MIT licence), adapted. Built on GOV.UK Service Manual «Moving away from legacy systems» (Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0.

The practice of pinning current behaviour before changing legacy code is widely known as characterization testing (Michael Feathers); described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
