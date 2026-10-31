---
name: load-test-plan
description: Plan, run and report a load test against a pre-production system the hirer owns, with the question, test shapes, rate, duration and data limits and a stop rule agreed in writing with the owner; record where and how the system broke so the owner can decide whether the risk is acceptable. Use before a launch or an expected traffic peak, after a large change, or when capacity is in doubt.
---

# Load test plan

A load test answers one question about capacity, and it can do real damage if it hits the wrong target. This skill writes the plan first: what is being asked, which system is tested, how hard and for how long, and when to stop. The owner signs the plan in writing. Only then does the test run, step by step, and the report says where the system gave way and how.

**Route:** a capacity question → **load-test-plan** → the owner agrees the plan in writing → the test runs in pre-production → a report → the owner decides whether the risk is acceptable.
Before this skill: a capacity question and a pre-production system the hirer owns. After it: a signed plan and a report; fixes and decisions belong to the owner.

## When to use

- Before a launch, a campaign or a known seasonal peak.
- After a change to architecture, infrastructure or a heavy code path.
- When nobody knows how much traffic the system can take.

## Inputs

- The question: for example «does it hold normal peak traffic», «what breaks first when traffic doubles», «does it stay healthy over a full day».
- A capacity picture from the owner: normal traffic, expected growth, known spikes, the user journeys that matter.
- A pre-production target the hirer owns, as close to production in size and settings as practical.
- Test data that looks like production but contains no personal data.
- The monitoring that shows health: errors, latency, resource use, queue lengths.

## Rules

- Only against a pre-production target the hirer owns. Never against production without the owner's written OK, and then only with the same written limits and stop rule.
- Never against third-party services or APIs the hirer does not own: payment providers, mail senders, maps, identity providers, partners. Replace them with stubs or exclude those paths.
- Limits agreed in writing before any run: maximum request rate, maximum duration, data volume, time window, and who may stop it.
- A stop rule agreed in writing: the error rate, latency, resource or side-effect level at which the test stops at once, plus «stop if anything outside the target shows impact».
- Production-like data with no personal data; synthetic accounts only.
- No promise of capacity, uptime or speed in the report; it states what was observed under the stated conditions.

## Steps

1. **Write the question** and how the answer will be read (which numbers, which threshold set by the owner).
2. **Build the traffic model** from the owner's figures: normal load, expected growth, known spikes, and the mix of user journeys. Note where each figure came from.
3. **Choose the test shapes** that answer the question:
   - a tiny smoke run to prove the script and the target work;
   - a run at normal load;
   - a stepped run that raises load until something gives way, to find the limit;
   - a sudden spike;
   - a long run at moderate load, to find leaks and slow drift.
   Use only the shapes the question needs.
4. **Fix the target and its dependencies:** name the environment and its owner; list every external dependency and how it is stubbed or excluded; confirm no production system shares the target's databases, queues or networks.
5. **Write the limits and the stop rule,** and who watches and who may stop.
6. **Get written agreement** from the owner of the target (and from any team whose shared component sits in the path). Record who agreed and when.
7. **Document the procedure** so the test can be repeated exactly: scripts, data set, settings, versions.
8. **Run the smoke test,** then the agreed shapes, raising load in steps and watching the stop rule at every step.
9. **Record what happened:** at which load errors or latency rose, what failed first (CPU, memory, connections, a database, a queue), how it failed (slowdown, errors, crash) and whether it recovered when load fell.
10. **Report** to the owner: question, conditions, observations, the weak point, and options to address it. The owner decides whether the risk is acceptable.

## Checks before hand-over

- The plan names a pre-production target the hirer owns, and the owner's written agreement is attached.
- No third-party service or API was put under load; stubs are listed.
- Limits and stop rule were written before the first run and were followed; any stop is recorded with its reason.
- The data had no personal data.
- The report states observed behaviour under stated conditions and promises nothing.

## Artefacts

- `load/<topic>-plan.md`: question, traffic model, shapes, target, stubs, limits, stop rule, agreement.
- `load/<topic>-<date>-report.md`: conditions, observations, weak point, options.
- `load/<topic>/`: scripts and data set definitions for repeat runs.

## Hand-over

- **To the owner:** the report and the risk decision.
- **To devops, the SRE or the Kubernetes platform engineer:** capacity findings, as change proposals.
- **To the database engineer:** database limits found.
- **To developers:** code paths that failed first, to be examined with profile-first.
- **To the QA engineer:** the repeatable scripts.

## Tools

An open-source load-testing tool that can script user journeys and raise load in stages, the target's monitoring dashboards, and a stub server for external dependencies. All runs started from a machine the hirer controls.

## Sources

Built on GOV.UK Service Manual «Test your service's performance» (Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
