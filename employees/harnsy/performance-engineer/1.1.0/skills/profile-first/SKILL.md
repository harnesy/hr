---
name: profile-first
description: Find out where time or memory actually goes before changing any code for speed; measure a baseline, profile to locate the bottleneck, change one thing, and measure again with the same method so the before/after difference is real. Use when something is slow or heavy, before any optimisation work, and when someone proposes a speed-up without numbers.
---

# Profile first

Guessing where a program is slow is usually wrong. This skill measures first, finds the part that really costs the time, changes only that, and measures again the same way. The result is a before/after comparison the owner can trust, or an honest «no measurable gain».

**Route:** a slow page, request, job or query → **profile-first** → a measured change, or a finding with no change → the owner decides → a regression check in the build.
Before this skill: a symptom someone can describe and repeat. After it: before/after numbers with their method, and a proposed change for review.

## When to use

- A request, page, job, query or build is slower or heavier than people want.
- Before anyone starts «optimising».
- When a change is claimed to be faster and nobody has measured it.

## Inputs

- The symptom, stated so it can be repeated: which action, what data, which environment.
- An environment where measuring does no harm: a local copy or a pre-production system, not production under live load unless the owner agrees to read-only sampling.
- The target, if the owner has one, and where it comes from. No target is invented.

## Rules

- Measure before changing. No code change without a baseline.
- One change at a time; each change gets its own measurement.
- The same method before and after: same environment, same data, same settings, same number of runs.
- Repeat runs and note the spread; a difference smaller than the run-to-run spread is not a result.
- No invented budgets or limits. Targets come from the owner, a written requirement or a published source with its date.
- Each number says where it came from: field data from real users, a lab run, or a profiler trace. Without data, the answer is «not measured».
- Read-only on live systems. Changes go through normal review.

## Steps

1. **Pin the question:** «action X with data Y takes Z, and should take less». Write down what is measured (time, memory, CPU, queries, bytes sent) and how.
2. **Prepare a clean measurement:** a fresh process or a clean browser profile without extensions, the same data set, and caching treated the same way each run. For browser work, slow the CPU and network to resemble a mid-range or low-end phone, and say which settings were used.
3. **Take a baseline:** several runs, record each value and the spread.
4. **Profile** to see where the cost sits: CPU samples or a flame graph, time spent waiting on the database or network, memory allocations, long tasks on the browser's main thread. Look at the biggest item first.
5. **Explain the bottleneck** in one sentence, with the evidence: «most of the time is spent in A because B».
6. **Make one change** that targets that bottleneck. Keep it small and reviewable.
7. **Measure again** with exactly the same method and number of runs.
8. **Compare:** if the gain is larger than the spread, record it; if it is within the spread, or other things got worse, recommend dropping the change and keeping the code simpler.
9. **Repeat** from step 4 for the next bottleneck, if the owner wants more.
10. **Guard against regressions:** propose a repeatable benchmark or check in the build, using the same method, so the gain does not quietly disappear.

## Checks before hand-over

- A baseline exists for every change, made with the same method as the after-measurement.
- Each change was measured on its own.
- The spread of runs is reported next to each number.
- Every number is labelled (field, lab or trace), and missing data says «not measured».
- No target or budget appears that the owner or a dated source did not give.

## Artefacts

- `perf/<topic>-<date>.md`: question, method, environment, baseline, profile findings, change, after-numbers, conclusion.
- Profiles or traces saved next to it.

## Hand-over

- **To the owner of the code** (developer or frontend developer): the measured change for review.
- **To the database engineer:** bottlenecks in queries or indexes.
- **To devops or the SRE:** bottlenecks in infrastructure, as change proposals.
- **To the QA engineer:** the regression check for the build.

## Tools

A profiler for the language in use (sampling CPU profiler, memory profiler), the database's query-plan output, and for web pages the browser's developer tools performance panel with CPU and network throttling. A small script to repeat a run several times and report the spread.

## Sources

Built on GOV.UK Service Manual «How to test frontend performance» and «Test your service's performance» (Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on Chrome DevTools «Analyze runtime performance» (Google LLC, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on agent-skills, «performance-optimization» and «web-performance-auditor» (github.com/addyosmani/agent-skills, commit 1401c8b; © 2025 Addy Osmani, MIT licence), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
