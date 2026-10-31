---
name: algorithm-trace
description: Check one algorithm's correctness by hand - restate the problem with its inputs, outputs and hidden assumptions, trace three to five small inputs (edge cases included) in a step table of operations and the values they change, and check a stated invariant at every step. Verdicts are «holds on the traced inputs», «fails at step n for input x» or «not shown», never «proven». Use before reading the author's own claims about correctness.
---

# Algorithm trace

A trace writes out what an algorithm actually does on small inputs, one operation at a time, and checks a stated invariant after each step. It finds the case nobody tried and makes hidden assumptions visible. It is not a proof: it shows the algorithm on the inputs traced, and an invariant that holds there is a strong argument, not a certainty.

**Route:** code or pseudocode from the author → **algorithm-trace** → `complexity-check` → `property-tests` → findings to the author and the code reviewer.

## When to use

- Reviewing a new or changed algorithm: a sort, a search, a merge, a dedupe, a scheduler, a parser loop.
- An author says the code is obviously correct.
- A bug report names an input where the result is wrong.
- Not for whole-system behaviour or speed under load: that is profiling, for the performance engineer.

## Inputs

- The algorithm (code or pseudocode) and where it is used.
- What it is supposed to compute, if written down anywhere.
- Do **not** read the author's claims about correctness or complexity yet; form your own result first.

## Steps

1. **Restate the problem.** In abstract terms: the inputs, the outputs and the relation between them, so the algorithm could be used as a black box. List every assumption the code makes but does not say: empty input, one element, duplicates, negative numbers, very large values, already sorted input, unicode, overflow.
2. **Choose 3 to 5 small inputs.** At least one ordinary case and the edge cases from step 1 that the problem allows.
3. **State the invariant.** For each loop, write what must be true at the end of every iteration (for example «out holds every distinct value of items[0..i], in first-seen order»). For a recursive algorithm, write what each call returns for a smaller input.
4. **Write the step table.** One row per operation: step number, operation, variables read, variables written, the values after the step, and whether the invariant holds. Keep going until the algorithm stops.
5. **Check the three moments.** The invariant holds before the loop starts; it stays true after every step; at exit, together with the stopping condition, it gives the required output.
6. **Record each difference** between the trace and the expected output: the input, the step number, the expected and the actual values.
7. **Write the verdict** per input: «holds on the traced inputs», «fails at step n for input x», or «not shown» (for example when the invariant cannot be stated).
8. **Only now** read the author's claims and note where they agree or differ with the trace.

## Rules

- **Verdict before claims.** The author's description is read after the trace, never before.
- **A trace is not a proof,** and a few passing tests are not proof either. Never write «proven correct».
- **Literal reading.** Read the code as a sceptical reader who takes every word literally; «obviously» is not a step.
- **Hands off the code.** Suggest a fix in the trace file; the author changes the algorithm.

## Checks before hand-over

- The problem restatement lists inputs, outputs and every assumption found.
- Edge cases are among the traced inputs.
- The invariant is written down and checked before, during and at exit.
- Every finding has an input, a step and expected versus actual values.
- The verdict uses only the three allowed phrases.

## Artefacts

- `review/<algorithm>/trace.md`: restatement, assumptions, invariant, step tables, findings, verdict, then the comparison with the author's claims.

## Hand-over

- **To the author:** the trace and findings, with any suggested fix.
- **To the code reviewer** checking the commit: the verdict and the inputs traced.
- **To `property-tests`:** the invariants, ready to become properties.

## Sources

Built on «Algorithms» (1st edition, 2019) by Jeff Erickson, sections on describing and analysing algorithms and on loop invariants (CC BY 4.0; algorithms.wtf), adapted. Built on «Open Data Structures» by Pat Morin, section on correctness, time and space (contains text from the Open Data Structures Project, opendatastructures.org; CC BY 2.5 Canada), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
