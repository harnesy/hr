---
name: debug-root-cause
description: Find the cause of a bug before fixing it, in any language or stack; reproduce it, check what changed, compare with a working case, test one written hypothesis at a time and record each result; fix at the source with a failing test first, and stop after three failed hypotheses to hand over everything tried. Use for any bug, failing test, crash, wrong result or flaky behaviour.
---

# Debug to the root cause

A fix without a known cause often moves the problem somewhere else. This skill works like a careful experiment: make the failure happen on demand, gather evidence, write down one guess about the cause, test only that guess, and keep a log. When three guesses in a row are wrong, it stops and brings in the owner instead of piling on more fixes.

**Route:** a bug report, failing test or alert → **debug-root-cause** → a confirmed cause with a failing test and a fix for review, or a hand-over after three failed hypotheses.
Before this skill: a symptom someone has seen. After it: a debug log, and either a reviewed fix or a clear hand-over.

## When to use

- Any bug, crash, wrong result, failing or flaky test, build failure or integration error.
- Especially under time pressure, and especially after a first quick fix did not work.

## Inputs

- The symptom: what happened, what was expected, where and when.
- Error messages, stack traces and logs, complete.
- A place to reproduce safely: a local setup, a test environment or a copy of the data. Not the live system.
- Recent changes: code, dependencies, configuration, infrastructure, data.

## Rules

- No fix before a cause. A change made only to see whether the symptom goes away is an experiment, and it is recorded as one.
- Read-only on live systems. Reproduce and experiment on copies; extra logging in production is a change proposal for the owner.
- One hypothesis at a time, written down before testing; one variable changed per test.
- Every result is recorded, including the ones that prove a guess wrong.
- Do not stack fixes. Undo an experiment that did not confirm its hypothesis before trying the next.
- After three failed hypotheses, stop and hand over with the log. Repeated misses usually mean a wrong assumption about how the system works, which needs the owner.

## Steps

1. **Read the error fully:** the whole message, the whole stack trace, codes, file names and line numbers. Note any earlier warnings.
2. **Reproduce it** with exact steps. Note how often it happens. If it will not reproduce, gather more evidence (logs, inputs, timing, environment) rather than guessing.
3. **Check what changed** shortly before it started: commits, dependency updates, configuration, environment, data, traffic.
4. **Compare with a working case:** a similar feature that works, the previous version, another environment. List every difference, even small ones.
5. **Find the failing layer** when several components are involved: in a test or copied environment, log what goes in and what comes out at each boundary, run once, and see where good input turns into bad output.
6. **Trace the bad value back** from where it shows up to where it is first produced. The cause is at the source, not where it crashes.
7. **Write one hypothesis:** «the failure happens because X, as shown by Y».
8. **Test it** with the smallest possible experiment that changes only one thing. Record the hypothesis, the experiment and the result in the debug log.
9. **If it is wrong,** undo the experiment, update what you know, and form the next hypothesis. Count failed hypotheses.
10. **If three have failed,** stop. Hand over the log, the reproduction steps and the open questions to the owner, and question the design together before going further.
11. **If it is confirmed,** write a test that fails because of the bug, then fix the cause at its source, run the new test and the existing suite, and send the change for review.
12. **Close the log:** cause, evidence, fix, test, and anything that should be checked elsewhere for the same mistake.

## Checks before hand-over

- The bug was reproduced, or the log says why it could not be.
- Every hypothesis and its result is in the log.
- A failing test existed before the fix and passes after it.
- No live system was changed during the investigation.
- After three failed hypotheses, work stopped and was handed over.

## Artefacts

- `debug/<date>-<short-name>.md`: symptom, reproduction, changes checked, differences, hypotheses with results, cause, fix, test.
- The failing test and the fix, in the code repository, as one reviewable change.

## Hand-over

- **To the owner of the code:** the fix for review, or the log after three failed hypotheses.
- **To the QA engineer:** the reproduction steps and the new test.
- **To devops or the SRE:** causes in infrastructure or configuration, as change proposals.
- **To the database engineer:** causes in data, queries or migrations.
- **To the security reviewer:** any cause with a security effect.

## Tools

The language's debugger and test runner, the version control history (log, blame, bisect between a good and a bad version), and the logs and traces of a non-production copy.

## Sources

Built on the «systematic-debugging» skill from Superpowers (github.com/obra/superpowers, commit 8ca22db; © 2025 Jesse Vincent, MIT licence), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
