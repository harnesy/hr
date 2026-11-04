#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Find candidate duplicate backlog items by title similarity, from a CSV export of the tracker.

Read-only: it reads one CSV file (or standard input) and prints candidate groups; it merges or closes nothing.
Similar titles are only a lead: a person reads both items before anything is proposed.

Usage:
  similar_titles.py export.csv [--id id] [--title title] [--min 0.8] [--csv-out out.csv]
"""
import argparse, csv, difflib, re, sys


def die(msg):
    print(f"similar_titles: {msg}", file=sys.stderr)
    sys.exit(2)


def norm(t):
    return " ".join(re.findall(r"[a-z0-9]+", t.lower()))


def main():
    ap = argparse.ArgumentParser(description="Candidate duplicates by title similarity (read-only).")
    ap.add_argument("file", help="CSV export, or - for standard input")
    ap.add_argument("--id", default="id")
    ap.add_argument("--title", default="title")
    ap.add_argument("--min", type=float, default=0.8, help="similarity from 0 to 1 (default 0.8)")
    ap.add_argument("--csv-out", default="", help="also write the pairs as CSV")
    a = ap.parse_args()
    if not 0 < a.min <= 1:
        die("--min must be above 0 and at most 1")
    try:
        fh = sys.stdin if a.file == "-" else open(a.file, newline="", encoding="utf-8")
    except OSError as e:
        die(f"cannot read {a.file}: {e.strerror}")
    with fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        die("no rows")
    missing = [c for c in (a.id, a.title) if c not in rows[0]]
    if missing:
        die(f"missing column(s): {', '.join(missing)}; columns are: {', '.join(rows[0])}")
    items = [(r[a.id].strip(), r[a.title].strip(), norm(r[a.title])) for r in rows if r[a.title].strip()]
    if len(items) > 5000:
        die(f"{len(items)} items: split the export (at most 5000 per run)")
    pairs = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if not items[i][2] or not items[j][2]:
                continue
            s = difflib.SequenceMatcher(None, items[i][2], items[j][2]).ratio()
            if s >= a.min:
                pairs.append((s, items[i], items[j]))
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x
    for _, x, y in pairs:
        parent[find(x[0])] = find(y[0])
    members = {p[1][0] for p in pairs} | {p[2][0] for p in pairs}
    groups = {}
    for x in items:
        if x[0] in members:
            groups.setdefault(find(x[0]), []).append(x)
    groups = [g for g in groups.values() if len(g) > 1]
    print(f"# {len(pairs)} similar pair(s) at {a.min:.2f}+ among {len(items)} items, {len(groups)} candidate group(s). "
          "Candidates only: read both items; the owner decides what is a duplicate and which one survives.")
    for k, g in enumerate(sorted(groups, key=lambda g: g[0][0]), start=1):
        print(f"\n## group {k}")
        for i, t, _ in g:
            print(f"- {i}: {t}")
    if pairs:
        print("\n## pairs")
        for s, x, y in sorted(pairs, key=lambda p: -p[0]):
            print(f"- {s:.2f} {x[0]} ~ {y[0]}")
    if a.csv_out:
        with open(a.csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["similarity", "item_a", "title_a", "item_b", "title_b"])
            for s, x, y in sorted(pairs, key=lambda p: -p[0]):
                w.writerow([f"{s:.2f}", x[0], x[1], y[0], y[1]])


if __name__ == "__main__":
    main()
