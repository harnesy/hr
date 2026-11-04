#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""List backlog items with no activity for at least N days, from a CSV export of the tracker.

Read-only: it reads one CSV file (or standard input) and prints a table; it changes nothing in any tracker.
The number of days is the backlog owner's rule and must be given; there is no default.

Usage:
  stale_list.py export.csv --days 90 [--id id] [--title title] [--updated updated] [--status status]
                [--open-status open,new] [--skip-label-col labels --skip-label keep,pinned] [--today 2026-10-11] [--csv-out out.csv]
"""
import argparse, csv, datetime, sys


def die(msg):
    print(f"stale_list: {msg}", file=sys.stderr)
    sys.exit(2)


def parse_day(value, where):
    v = (value or "").strip()
    if not v:
        die(f"empty date in {where}")
    try:
        return datetime.date.fromisoformat(v[:10])
    except ValueError:
        die(f"not a date (expected YYYY-MM-DD or an ISO timestamp) in {where}: {v!r}")


def main():
    ap = argparse.ArgumentParser(description="List items with no activity for at least N days (read-only).")
    ap.add_argument("file", help="CSV export, or - for standard input")
    ap.add_argument("--days", type=int, required=True, help="the owner's rule: days without activity")
    ap.add_argument("--id", default="id")
    ap.add_argument("--title", default="title")
    ap.add_argument("--updated", default="updated", help="column with the last activity date")
    ap.add_argument("--status", default="", help="status column (optional)")
    ap.add_argument("--open-status", default="", help="comma-separated status values that count as open")
    ap.add_argument("--skip-label-col", default="", help="column holding labels (optional)")
    ap.add_argument("--skip-label", default="", help="comma-separated labels the owner never wants proposed")
    ap.add_argument("--today", default="", help="reference date YYYY-MM-DD (default: today)")
    ap.add_argument("--csv-out", default="", help="also write the result as CSV")
    a = ap.parse_args()
    if a.days < 1:
        die("--days must be 1 or more")
    today = parse_day(a.today, "--today") if a.today else datetime.date.today()
    try:
        fh = sys.stdin if a.file == "-" else open(a.file, newline="", encoding="utf-8")
    except OSError as e:
        die(f"cannot read {a.file}: {e.strerror}")
    with fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        die("no rows")
    need = [a.id, a.title, a.updated] + ([a.status] if a.status else []) + ([a.skip_label_col] if a.skip_label_col else [])
    missing = [c for c in need if c not in rows[0]]
    if missing:
        die(f"missing column(s): {', '.join(missing)}; columns are: {', '.join(rows[0])}")
    open_set = {s.strip().lower() for s in a.open_status.split(",") if s.strip()}
    skip = {s.strip().lower() for s in a.skip_label.split(",") if s.strip()}
    out, skipped, closed = [], 0, 0
    for n, r in enumerate(rows, start=2):
        if a.status and open_set and r[a.status].strip().lower() not in open_set:
            closed += 1
            continue
        if skip and a.skip_label_col:
            labels = {x.strip().lower() for x in r[a.skip_label_col].replace(";", ",").split(",")}
            if labels & skip:
                skipped += 1
                continue
        last = parse_day(r[a.updated], f"row {n}, column {a.updated}")
        age = (today - last).days
        if age >= a.days:
            out.append((age, r[a.id], last.isoformat(), r[a.title].strip()))
    out.sort(key=lambda x: (-x[0], x[1]))
    print(f"# {len(out)} of {len(rows)} items with no activity for {a.days}+ days (reference date {today.isoformat()}); "
          f"not open: {closed}; skipped by label: {skipped}. Candidates only: the owner decides close, refresh or keep.")
    print("| item | last activity | days quiet | title |")
    print("|---|---|---|---|")
    for age, i, last, t in out:
        print(f"| {i} | {last} | {age} | {t.replace('|', '/')} |")
    if a.csv_out:
        with open(a.csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["item", "last_activity", "days_quiet", "title", "proposal", "reason", "evidence"])
            for age, i, last, t in out:
                w.writerow([i, last, age, t, "", "", ""])


if __name__ == "__main__":
    main()
