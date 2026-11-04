---
name: property-tests
description: Turn an algorithm's invariants into randomised property tests - a slow, obviously correct reference version, properties that must hold for every valid input, preconditions instead of silent filtering, edge-biased generators, many runs with a seed that is always reported, failures shrunk to a small counter-example and pinned as example tests. Use after tracing an algorithm, next to its example tests, never instead of them.
---

# Property tests

An example test checks one input someone thought of. A property test states something that must be true for every valid input («the output holds the same items as the input, in order») and checks it on many generated inputs, including the awkward ones. When it fails, it shrinks the input to a small counter-example and reports the seed so anyone can replay it.

**Route:** invariants from `algorithm-trace` → **property-tests** → counter-examples pinned as example tests → the author fixes the algorithm.

## When to use

- An algorithm has invariants that are easy to state but hard to cover with hand-picked examples: sorting, deduplication, merging, parsing and printing, encoding and decoding, scheduling.
- A slow but obviously correct version exists or is easy to write.
- Not as a replacement for example tests, and not for behaviour that depends on time, network or live data.

## Inputs

- The function under test and its contract (from the trace).
- The invariants found in the trace.
- The project's testing tools: most languages have a property-based testing library; use the one the project already has. For Python code without one, the script in `scripts/` runs a quick check.

## Steps

1. **Write the reference.** A slow, obviously correct version of the same function, short enough to check by eye (for example, deduplicate with a set and a list; sort with the language's built-in sort). If no reference is possible, use properties only.
2. **Write the properties.** Each one says «for every valid input x, the result has property P»: same items as the input, ordered, no duplicates, the length rule, a round trip that gives the input back. Take them from the invariants in the trace.
3. **State the preconditions.** Restrict inputs with a stated precondition (for example «no negative sizes»), and report how many inputs it rejected; do not quietly drop inputs inside the test.
4. **Use edge-biased generators.** Make sure the runs include 0, 1, -1, the bounds, empty and one-item collections, duplicates, already sorted and reversed inputs.
5. **Keep the inputs untouched.** The property code must not change its inputs, and the test checks that the function under test does not either, unless changing them is its contract.
6. **Run many cases with a seed.** 100 runs for a quick check, 1,000 or more before hand-over. Fix the seed in continuous integration; every failure prints the seed and the shrunk counter-example.
7. **Pin every counter-example.** Each one found becomes an explicit example test with a name that says what it covers, so it runs every time and is never lost.
8. **Report.** Properties, seed, runs, rejected inputs, counter-examples and the pinned tests.

## Rules

- **Next to example tests, never instead.**
- **Every run is repeatable:** a seed is always reported.
- **Passing runs are evidence, not proof;** say how many runs and which generators.
- **The author changes the algorithm.** This skill writes tests and reports; it does not edit the code under test.
- **Read before you run.** The helper imports and runs the files it is given; run only code you have read, on invented inputs, never against live systems.

## Checks before hand-over

- A reference or at least two properties per function, each traceable to an invariant.
- Preconditions stated, with the count of rejected inputs.
- Edge values included in the runs.
- The seed and the number of runs are in the report.
- Every counter-example is pinned as a named example test.

## Artefacts

- The property test file in the project's test folder, next to the example tests.
- `review/<algorithm>/properties.md`: properties, reference, seed, runs, counter-examples, pinned tests.
- For the helper: `review/<algorithm>/pins.json` with saved counter-examples.

## Hand-over

- **To the author:** the property file, the seed and the counter-examples, with the pinned example tests.
- **To the code reviewer:** the report for the commit under review.
- **To the test automation engineer:** the property file, if it should run in continuous integration.

## Tools

- `python3` 3.8 or newer, standard library only, no network.
- `python3 scripts/prop_check.py --target algo.py:dedupe --reference ref.py:dedupe_ref --gen "list[int]" --runs 1000 --seed 4242` compares the target with the reference on edge values and 1,000 random lists and checks that the input is not changed.
- `--property props.py:check` adds a property function called as check(input, result); `--pre file.py:valid` gives a precondition; `--min`, `--max`, `--max-len` set the generator's range.
- `--pins pins.json --save` replays saved counter-examples first and adds a new shrunk one. Exit 0 all passed, 1 counter-example found, 2 bad arguments.

## Sources

Built on the fast-check documentation, pages on property-based testing, properties, runners and model-based testing (MIT, Copyright (c) 2017 Nicolas Dubien), adapted. The practices of comparing with a slow reference and replaying failures first are widely shared among property-based testing tools; described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
