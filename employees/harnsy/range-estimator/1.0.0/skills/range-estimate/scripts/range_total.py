# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Total a three-point estimate from a CSV of pieces: piece,low,likely,high[,assumption].

Prints each piece with its spread, then the sum of lows, the sum of likely values, the sum of highs and a weighted mean
(low + 4 x likely + high) / 6, a common weighting. --factor scales every number by the team's own correction factor from
an estimate review. Standard library only; reads one file (or standard input with "-"); no network. Exit 2 on bad input.
"""
import argparse
import csv
import math
import sys

LABEL = "a range for planning; the owner sets any date"


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def num(value, piece, column):
    try:
        x = float(value)
    except (TypeError, ValueError):
        fail(f"piece {piece!r}: {column} is not a number: {value!r}")
    if x < 0:
        fail(f"piece {piece!r}: {column} is negative")
    return x


def read(path):
    try:
        f = sys.stdin if path == "-" else open(path, newline="", encoding="utf-8")
    except OSError as e:
        fail(f"cannot read {path}: {e.strerror}")
    rows = list(csv.reader(f))
    if f is not sys.stdin:
        f.close()
    rows = [r for r in rows if r and any(c.strip() for c in r) and not r[0].lstrip().startswith("#")]
    if rows and [c.strip().lower() for c in rows[0][:4]] == ["piece", "low", "likely", "high"]:
        rows = rows[1:]
    if not rows:
        fail("no pieces found (expected piece,low,likely,high[,assumption])")
    out = []
    for r in rows:
        if len(r) < 4:
            fail(f"row {r!r}: need at least piece,low,likely,high")
        piece = r[0].strip()
        low, likely, high = (num(r[i], piece, c) for i, c in ((1, "low"), (2, "likely"), (3, "high")))
        if not low <= likely <= high:
            fail(f"piece {piece!r}: need low <= likely <= high, got {low:g}, {likely:g}, {high:g}")
        out.append((piece, low, likely, high, ",".join(r[4:]).strip()))
    return out


def main():
    ap = argparse.ArgumentParser(description="Total a three-point estimate (" + LABEL + ").")
    ap.add_argument("csv", help="CSV file of pieces (piece,low,likely,high[,assumption]), or - for standard input")
    ap.add_argument("--factor", type=float, default=1.0, help="team correction factor from an estimate review (default 1.0)")
    ap.add_argument("--unit", default="days", help="unit of the numbers, for the report (default days)")
    a = ap.parse_args()
    if not 0 < a.factor <= 10:
        fail("--factor must be above 0 and at most 10")
    pieces = read(a.csv)
    f = a.factor
    print(f"# Range estimate: {len(pieces)} piece(s), unit {a.unit}" + (f", correction factor {f:g}" if f != 1 else ""))
    print(f"# {LABEL}")
    w = max(len(p[0]) for p in pieces)
    for piece, low, likely, high, why in pieces:
        line = f"{piece:<{w}}  {low * f:7.1f} {likely * f:7.1f} {high * f:7.1f}   spread {(high - low) * f:5.1f}"
        print(line + (f"   assumes: {why}" if why else ""))
    lo = sum(p[1] for p in pieces) * f
    li = sum(p[2] for p in pieces) * f
    hi = sum(p[3] for p in pieces) * f
    wm = sum((p[1] + 4 * p[2] + p[3]) / 6 for p in pieces) * f
    wide = sorted(pieces, key=lambda p: p[3] - p[1], reverse=True)[:3]
    print()
    print(f"sum of lows    {lo:.1f} {a.unit}")
    print(f"sum of likely  {li:.1f} {a.unit}")
    print(f"sum of highs   {hi:.1f} {a.unit}")
    print(f"weighted mean  {wm:.1f} {a.unit}  (low + 4 x likely + high) / 6 per piece, a common weighting")
    print("widest pieces  " + "; ".join(f"{p[0]} ({(p[3] - p[1]) * f:.1f})" for p in wide))
    print(f"Report as a range, for example {math.floor(lo)} to {math.ceil(hi)} {a.unit}, likely about {li:.0f}; {LABEL}.")


if __name__ == "__main__":
    main()
