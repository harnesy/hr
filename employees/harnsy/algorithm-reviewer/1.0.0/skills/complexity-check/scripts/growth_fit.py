#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Fit measured growth to the usual growth classes.

measurements.csv: one row per run, a column with the input size and a column with
the measured value (an operation count, or a time in seconds). Several runs per size
are allowed; the median per size is used. At least three different sizes are needed,
each ideally two or more times larger than the one before.

For every class (1, log n, n, n log n, n^2, n^3, 2^n) the script divides the median
value by the class function at each size and reports how much that ratio spreads
(the largest ratio divided by the smallest). The class with the smallest spread is
the closest fit. It also prints the local exponent between neighbouring sizes
(the slope on a log-log scale): about 1 means linear, about 2 quadratic.

--claim names the growth the author states; it is compared only after the fit is
printed, so the measured result comes first.

Prints Markdown. Counts and a fit, not a proof. Standard library only; no network.
"""
import argparse
import csv
import math
import statistics
import sys

CLASSES = [
    ("1", lambda n: 0.0),
    ("log n", lambda n: math.log(math.log(n))),
    ("n", lambda n: math.log(n)),
    ("n log n", lambda n: math.log(n) + math.log(math.log(n))),
    ("n^2", lambda n: 2 * math.log(n)),
    ("n^3", lambda n: 3 * math.log(n)),
    ("2^n", lambda n: n * math.log(2)),
]  # each function returns ln f(n)

ALIASES = {"1": "1", "constant": "1", "logn": "log n", "log": "log n", "n": "n", "linear": "n",
           "nlogn": "n log n", "n*logn": "n log n", "n^2": "n^2", "n2": "n^2", "quadratic": "n^2",
           "n^3": "n^3", "n3": "n^3", "cubic": "n^3", "exponential": "2^n", "2^n": "2^n"}


def fmt(log_spread):
    return f"×{math.exp(log_spread):.2f}" if log_spread < 50 else "more than ×10^20"


def norm_claim(s):
    t = s.strip().lower().replace("**", "^").replace("o(", "").replace(")", "").replace("·", "*").replace(" ", "")
    return ALIASES.get(t)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("measurements", help="CSV file with a header row")
    ap.add_argument("--size-col", default="n", help="column with the input size (default n)")
    ap.add_argument("--value-col", default="value", help="column with the count or time (default value)")
    ap.add_argument("--unit", default="operations", help="what the value measures, for the report")
    ap.add_argument("--claim", help="the author's stated growth, e.g. «n log n» or «O(n^2)»; compared after the fit")
    a = ap.parse_args()

    runs = {}
    problems = []
    with open(a.measurements, newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        if not rd.fieldnames or a.size_col not in rd.fieldnames or a.value_col not in rd.fieldnames:
            sys.exit(f"growth_fit: columns «{a.size_col}» and «{a.value_col}» are needed; the file has {rd.fieldnames}")
        for i, row in enumerate(rd, start=2):
            try:
                n = float(row[a.size_col])
                v = float(row[a.value_col])
            except (TypeError, ValueError):
                problems.append(f"line {i}: not a number, skipped")
                continue
            if n < 3 or v <= 0:
                problems.append(f"line {i}: size below 3 or value not above 0, skipped")
                continue
            runs.setdefault(n, []).append(v)

    sizes = sorted(runs)
    if len(sizes) < 3:
        sys.exit(f"growth_fit: {len(sizes)} different sizes; at least 3 are needed to see growth")
    med = {n: statistics.median(runs[n]) for n in sizes}

    print(f"# Growth fit: {a.measurements}")
    print()
    print("Counts and a fit, not a proof. Read the table before any claim.")
    print()
    if problems:
        print("## Problems in the file")
        print()
        for p in problems:
            print(f"- {p}")
        print()
    print(f"## Measurements (median per size, {a.unit})")
    print()
    print("| n | runs | median | ratio to previous size | local exponent |")
    print("|---|---|---|---|---|")
    prev = None
    small_steps = 0
    for n in sizes:
        if prev is None:
            print(f"| {n:g} | {len(runs[n])} | {med[n]:g} | | |")
        else:
            r = med[n] / med[prev]
            k = math.log(med[n] / med[prev]) / math.log(n / prev)
            if n / prev < 2:
                small_steps += 1
            print(f"| {n:g} | {len(runs[n])} | {med[n]:g} | ×{r:.2f} (size ×{n / prev:.2f}) | {k:.2f} |")
        prev = n
    print()
    if small_steps:
        print(f"Note: {small_steps} step(s) grow the size by less than 2 times; the fit is weaker. Prefer sizes that double or more.")
        print()

    fits = []
    for name, lnf in CLASSES:
        try:
            lr = [math.log(med[n]) - lnf(n) for n in sizes]
        except (ValueError, OverflowError):
            continue
        trend = lr[-1] - lr[0]
        fits.append((max(lr) - min(lr), name, trend))  # log of the spread
    fits.sort()
    print("## Fit against growth classes")
    print()
    print("| class | spread of value ÷ f(n) | ratio drifts |")
    print("|---|---|---|")
    for spread, name, trend in fits:
        drift = "up (grows faster)" if trend > 0.1 else "down (grows slower)" if trend < -0.1 else "flat"
        print(f"| {name} | {fmt(spread)} | {drift} |")
    best = fits[0]
    print()
    print(f"**Closest class: {best[1]}** (spread {fmt(best[0])} between {sizes[0]:g} and {sizes[-1]:g}).")
    if len(fits) > 1 and fits[1][0] - best[0] < math.log(1.15):
        print(f"Close second: {fits[1][1]} (spread {fmt(fits[1][0])}); measure at larger sizes to separate them.")
    print()

    if a.claim:
        c = norm_claim(a.claim)
        print("## The stated growth (read after the fit)")
        print()
        if not c:
            print(f"Claim «{a.claim}» is not one of: {', '.join(n for n, _ in CLASSES)}; compare by hand.")
        else:
            cs = next(s for s, n, _ in fits if n == c)
            verdict = "matches the closest class" if c == best[1] else f"differs from the closest class ({best[1]})"
            print(f"Claim: {c}. Spread for the claim {fmt(cs)}; it {verdict} on these inputs and sizes.")
        print()
    print("These sizes and inputs only: worst-case, amortised and expected cost each need their own inputs.")


if __name__ == "__main__":
    main()
