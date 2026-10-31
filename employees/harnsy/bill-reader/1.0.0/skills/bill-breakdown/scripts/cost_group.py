#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Group a cloud cost-and-usage export (CSV) by chosen columns, using exactly one cost column.

Reads one CSV file (or standard input), adds up ONE named cost column, and prints a grouped table:
totals per group, untagged rows as their own line, the top N groups, optional month-over-month change
by a date column, and charge categories (usage, purchase, tax, credit, adjustment...) kept apart if a
category column is named. Standard library only; no network; runs no other program. Numbers come only
from the rows of the file: the script never looks up a price.

Exit codes: 0 done, 2 bad input (missing file or column, more than one cost column, non-numeric cost).
"""
import argparse
import csv
import io
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation

UNTAGGED = "(untagged)"


def die(msg):
    print(f"cost_group: {msg}", file=sys.stderr)
    sys.exit(2)


def parse_args(argv):
    p = argparse.ArgumentParser(description="Group a cost-and-usage CSV export by columns, with one cost column.")
    p.add_argument("file", help="CSV export, or - for standard input")
    p.add_argument("--cost", required=True, action="append",
                   help="the ONE cost column to add up (for example the billed or the effective cost column)")
    p.add_argument("--by", required=True, help="comma-separated columns to group by, e.g. service,team_tag")
    p.add_argument("--untagged", default="",
                   help="comma-separated --by columns where an empty value means untagged (shown as its own line)")
    p.add_argument("--category", default="", help="charge category column; groups are kept apart per category")
    p.add_argument("--date", default="", help="date column (ISO, YYYY-MM...) for a month-over-month view")
    p.add_argument("--currency", default="", help="currency column; the script refuses to add rows in different currencies")
    p.add_argument("--top", type=int, default=20, help="show the top N groups (default 20)")
    p.add_argument("--csv-out", default="", help="also write the grouped table to this CSV file")
    p.add_argument("--delimiter", default=",", help="field delimiter (default ,)")
    return p.parse_args(argv)


def money(text, rowno, col):
    t = (text or "").strip().replace(" ", "")
    if t == "":
        return Decimal(0)
    try:
        return Decimal(t)
    except InvalidOperation:
        die(f"row {rowno}: column «{col}» is not a number: {text!r}")


def main(argv=None):
    a = parse_args(sys.argv[1:] if argv is None else argv)
    if len(a.cost) != 1 or "," in a.cost[0]:
        die("name exactly one cost column with --cost; billed, effective and list cost are never added together")
    cost = a.cost[0]
    by = [c.strip() for c in a.by.split(",") if c.strip()]
    untagged = {c.strip() for c in a.untagged.split(",") if c.strip()}
    if not by:
        die("--by needs at least one column")
    if untagged - set(by):
        die("--untagged columns must also be in --by: " + ", ".join(sorted(untagged - set(by))))
    try:
        fh = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8-sig") if a.file == "-" else open(a.file, encoding="utf-8-sig", newline="")
    except OSError as e:
        die(f"cannot read {a.file}: {e.strerror}")
    with fh:
        reader = csv.DictReader(fh, delimiter=a.delimiter)
        cols = reader.fieldnames or []
        need = [cost] + by + [c for c in (a.category, a.date, a.currency) if c]
        missing = [c for c in need if c not in cols]
        if missing:
            die("column(s) not in the file: " + ", ".join(missing) + ". Columns found: " + ", ".join(cols))
        totals = defaultdict(Decimal)
        months = defaultdict(lambda: defaultdict(Decimal))
        cats = defaultdict(Decimal)
        currencies = set()
        rows = 0
        grand = Decimal(0)
        for i, row in enumerate(reader, start=2):
            rows += 1
            v = money(row.get(cost), i, cost)
            if a.currency:
                currencies.add((row.get(a.currency) or "").strip())
            key = tuple(((row.get(c) or "").strip() or (UNTAGGED if c in untagged else "(empty)")) for c in by)
            cat = (row.get(a.category) or "").strip() or "(empty)" if a.category else ""
            gkey = (cat,) + key if a.category else key
            totals[gkey] += v
            cats[cat] += v
            grand += v
            if a.date:
                months[(row.get(a.date) or "").strip()[:7] or "(no date)"][gkey] += v
    if rows == 0:
        die("the file has a header but no rows")
    if len(currencies) > 1:
        die("rows in more than one currency (" + ", ".join(sorted(currencies)) + "); split the file by currency first")

    head = (["category"] if a.category else []) + by
    print(f"# cost_group: {rows} rows, cost column «{cost}», grouped by {', '.join(by)}.")
    cur = next(iter(currencies)) if currencies else "not stated in the file: check the export's currency"
    print(f"# Currency: {cur}. Numbers come only from the file's rows; no prices were looked up.")
    print(f"# Total of «{cost}»: {grand:.2f}")
    if a.category:
        print("# By charge category (purchases, taxes, credits and adjustments are not usage):")
        for c, v in sorted(cats.items(), key=lambda x: -x[1]):
            print(f"#   {c}: {v:.2f}")
    ranked = sorted(totals.items(), key=lambda x: -x[1])
    print("\t".join(head + [cost, "share %"]))
    for k, v in ranked[: a.top]:
        share = (v / grand * 100) if grand else Decimal(0)
        print("\t".join(list(k) + [f"{v:.2f}", f"{share:.1f}"]))
    if len(ranked) > a.top:
        rest = sum((v for _, v in ranked[a.top:]), Decimal(0))
        print(f"(other {len(ranked) - a.top} groups)\t" + "\t" * (len(head) - 1) + f"{rest:.2f}")
    unt = [(k, v) for k, v in ranked if UNTAGGED in k]
    if untagged:
        s = sum((v for _, v in unt), Decimal(0))
        share = (s / grand * 100) if grand else Decimal(0)
        print(f"# Untagged ({', '.join(sorted(untagged))} empty): {s:.2f} ({share:.1f} % of the total) in {len(unt)} group(s)")
    if a.date:
        ms = sorted(m for m in months if m != "(no date)")
        print("# Month over month (top groups):")
        print("\t".join(head + ms + (["change last two %"] if len(ms) >= 2 else [])))
        for k, _ in ranked[: a.top]:
            vals = [months[m].get(k, Decimal(0)) for m in ms]
            line = list(k) + [f"{x:.2f}" for x in vals]
            if len(ms) >= 2:
                line.append(f"{(vals[-1] - vals[-2]) / vals[-2] * 100:.1f}" if vals[-2] else "new")
            print("\t".join(line))
        if "(no date)" in months:
            print("# Some rows have no date; they are in the totals but not in the monthly view.")
    if a.csv_out:
        with open(a.csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(head + [cost])
            for k, v in ranked:
                w.writerow(list(k) + [f"{v:.2f}"])
        print(f"# Grouped table written to {a.csv_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
