---
name: complexity-check
description: Compare the growth an author states for an algorithm with the growth measured at three or more input sizes - expected growth written from the code first, operation counts or median timings collected, the script fits them to constant, log, linear, n log n, quadratic, cubic or exponential growth, and only then is the author's claim read. Worst-case, amortised and expected cost are tested separately. Use when reviewing an algorithm or a claim about its speed.
---

# Complexity check

A claim like «this is O(n log n)» is checkable. This skill writes down the growth the code should have, measures it at several sizes, fits the measurements to the usual growth classes, and only then reads the author's claim, so the claim cannot steer the result. One timing shows nothing; three or more sizes show growth.

**Route:** code from the author, after `algorithm-trace` → **complexity-check** → `property-tests` → verdict to the author; system-level slowness to the performance engineer.

## When to use

- A pull request, design note or comment states the cost of an algorithm.
- A function gets slow as data grows and the algorithm is suspected.
- Choosing between two algorithms for the same job.
- Not for a whole system under load, memory leaks or slow networks: those are profiling questions for the performance engineer.

## Inputs

- The code, and a way to run it on generated inputs (a test harness, a script, a REPL).
- What kind of input matters: random, sorted, reverse sorted, many duplicates, worst case.
- Do **not** read the author's complexity claim yet.

## Steps

1. **Expect first.** From the code, write the growth you expect and why: the dominant operation (a comparison, a loop body, a lookup) and how often it runs as n grows. Note whether this is the worst case, an amortised cost over a sequence, or an expected cost over random choices inside the algorithm.
2. **Choose what to measure.** Prefer counting the dominant operation (add a counter in a copy of the code); use median wall-clock timings only when counting is not possible, with several runs per size.
3. **Choose sizes.** At least three, each two or more times larger than the last (for example 1,000, 4,000, 16,000, 64,000), small enough to run quickly and large enough that constant costs fade.
4. **Choose inputs per cost.** Worst case: the input shape the code handles worst (sorted input for a naive quicksort, for example). Amortised: a long sequence of operations, total cost divided by the number of operations. Expected: several random seeds per size.
5. **Run and record** each size and value in a CSV with columns `n` and `value` (more columns are fine).
6. **Fit.** Run the script (see Tools). Read the table of medians, the local exponents and the closest class.
7. **Rough cost.** Multiply out what the fit means at the real data size (operations × size ÷ a machine's rough speed) to show whether it matters in practice.
8. **Now read the claim.** Compare the stated growth with the fit, for each kind of input measured, and write the verdict: for example «stated O(n log n); measured close to n^2 between 1k and 64k on sorted input; matches n log n on random input».

## Rules

- **Measure before reading the claim,** and say in the note that you did.
- **Name the cost.** Worst case unless stated; amortised and expected cost are named as such, with the inputs used.
- **No single timing.** Three sizes at least; medians of several runs for timings.
- **Fits are not proofs.** A fit holds for the sizes and inputs measured; say so.
- **No production data.** Inputs are generated; nothing runs against live systems.

## Checks before hand-over

- The expected growth and the reasoning were written before measuring.
- At least three sizes, growing by two or more times each.
- Each kind of cost measured has its own inputs.
- The script's table is attached, and the verdict names the sizes and inputs.
- The author's claim is quoted only after the fit.

## Artefacts

- `review/<algorithm>/growth.csv`: the measurements.
- `review/<algorithm>/growth.md`: expected growth, the script's report, the rough cost at real size, the verdict and the comparison with the claim.

## Hand-over

- **To the author:** the growth note and the CSV.
- **To the code reviewer:** the verdict for the commit under review.
- **To the performance engineer:** anything that is slow although the algorithm grows as stated.

## Tools

- `python3` 3.8 or newer, standard library only, no network.
- `python3 scripts/growth_fit.py growth.csv --unit comparisons` prints the measurements, the local exponent between sizes and the spread of value ÷ f(n) for each growth class; the smallest spread is the closest class.
- `--claim "n log n"` adds the author's stated growth, compared after the fit. `--size-col` and `--value-col` name other columns.
- The script exits with a message when fewer than three sizes are given, and notes steps that grow by less than two times.

## Sources

Built on «Open Data Structures» by Pat Morin, sections on the need for efficiency, asymptotic notation and correctness, time and space (contains text from the Open Data Structures Project, opendatastructures.org; CC BY 2.5 Canada), adapted. Built on «Algorithms» (1st edition, 2019) by Jeff Erickson, section on analysing algorithms (CC BY 4.0; algorithms.wtf), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
