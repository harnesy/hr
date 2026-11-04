#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Sample size per group for a two-group experiment (two-sided, normal approximation).

  sample_size.py proportions --baseline 0.10 --mde-abs 0.01
  sample_size.py proportions --baseline 0.10 --mde-rel 0.05 --metrics 2 --dropout 0.1
  sample_size.py proportions --baseline 0.10 --range 0.005,0.01,0.02
  sample_size.py means --sd 12.5 --mde 1.0 --power 0.9

Standard library only; no network. A first estimate for simple comparisons:
for clustered units, ratio metrics or many variants, simulate or ask a statistician.
"""
import argparse
import math
import sys
from statistics import NormalDist

Z = NormalDist()


def z_values(alpha, power, metrics):
    a = alpha / metrics  # Bonferroni split across primary comparisons
    return Z.inv_cdf(1 - a / 2), Z.inv_cdf(power), a


def n_proportions(p1, delta, alpha, power, metrics):
    p2 = p1 + delta
    if not 0 < p2 < 1:
        raise ValueError(f"baseline + effect = {p2:.4f} is outside (0, 1)")
    za, zb, _ = z_values(alpha, power, metrics)
    pbar = (p1 + p2) / 2
    num = za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(num ** 2 / delta ** 2)


def n_means(sd, delta, alpha, power, metrics):
    za, zb, _ = z_values(alpha, power, metrics)
    return math.ceil(2 * (za + zb) ** 2 * sd ** 2 / delta ** 2)


def inflate(n, dropout):
    return math.ceil(n / (1 - dropout))


def check_common(a):
    if not 0 < a.alpha < 1:
        sys.exit("error: --alpha must be between 0 and 1")
    if not 0 < a.power < 1:
        sys.exit("error: --power must be between 0 and 1")
    if a.metrics < 1:
        sys.exit("error: --metrics must be 1 or more")
    if not 0 <= a.dropout < 1:
        sys.exit("error: --dropout must be in [0, 1)")


def parse_range(text):
    try:
        vals = [float(x) for x in text.split(",") if x.strip()]
    except ValueError:
        sys.exit("error: --range takes numbers separated by commas")
    if not vals or any(v == 0 for v in vals):
        sys.exit("error: --range needs non-zero effects")
    return vals


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="kind", required=True)
    for name in ("proportions", "means"):
        s = sub.add_parser(name)
        s.add_argument("--alpha", type=float, default=0.05, help="two-sided significance level (default 0.05)")
        s.add_argument("--power", type=float, default=0.8, help="power (default 0.8)")
        s.add_argument("--metrics", type=int, default=1, help="number of primary comparisons; alpha is split equally")
        s.add_argument("--dropout", type=float, default=0.0, help="share of units expected to be lost (0-1)")
        s.add_argument("--range", help="comma-separated effects for a sensitivity table (absolute)")
    sp = sub.choices["proportions"]
    sp.add_argument("--baseline", type=float, required=True, help="control rate, e.g. 0.10")
    sp.add_argument("--mde-abs", type=float, help="smallest effect worth acting on, absolute (0.01 = 1 point)")
    sp.add_argument("--mde-rel", type=float, help="smallest effect worth acting on, relative (0.05 = +5%)")
    sm = sub.choices["means"]
    sm.add_argument("--sd", type=float, required=True, help="standard deviation of the metric")
    sm.add_argument("--mde", type=float, help="smallest difference in means worth acting on")
    a = ap.parse_args()
    check_common(a)

    effects = []
    if a.kind == "proportions":
        if not 0 < a.baseline < 1:
            sys.exit("error: --baseline must be between 0 and 1")
        if a.mde_abs is not None:
            effects.append(a.mde_abs)
        if a.mde_rel is not None:
            effects.append(a.baseline * a.mde_rel)
        calc = lambda d: n_proportions(a.baseline, d, a.alpha, a.power, a.metrics)
    else:
        if a.sd <= 0:
            sys.exit("error: --sd must be positive")
        if a.mde is not None:
            effects.append(a.mde)
        calc = lambda d: n_means(a.sd, d, a.alpha, a.power, a.metrics)
    if a.range:
        effects += parse_range(a.range)
    if not effects:
        sys.exit("error: give an effect (--mde-abs/--mde-rel, --mde) or --range")
    if any(e == 0 for e in effects):
        sys.exit("error: the effect must not be zero")

    _, _, a_each = z_values(a.alpha, a.power, a.metrics)
    print("Assumptions: two-sided test, normal approximation, equal groups,"
          f" alpha {a.alpha} split over {a.metrics} comparison(s) = {a_each:.4g} each,"
          f" power {a.power}, drop-out {a.dropout:.0%}.")
    if a.kind == "proportions":
        print(f"Baseline rate {a.baseline}.")
        print(f"{'effect (abs)':>13} {'target rate':>12} {'n per group':>12} {'total':>10}")
        for d in effects:
            try:
                n = inflate(calc(d), a.dropout)
            except ValueError as e:
                sys.exit(f"error: {e}")
            print(f"{d:>13.4g} {a.baseline + d:>12.4g} {n:>12,} {2 * n:>10,}")
    else:
        print(f"Standard deviation {a.sd}.")
        print(f"{'difference':>13} {'n per group':>12} {'total':>10}")
        for d in effects:
            n = inflate(calc(d), a.dropout)
            print(f"{d:>13.4g} {n:>12,} {2 * n:>10,}")


if __name__ == "__main__":
    main()
