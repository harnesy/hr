#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""List every sentence of a text that contains a checkable element, so no claim is missed when the claims list is written.

Read-only: it reads one plain-text or Markdown file (or standard input) and prints one row per sentence with the line number
and what was spotted (number, percent, money, year or date, ranking or comparison word, change word, quotation).
It finds candidates only; it does not judge whether anything is right, and a person still reads the whole text.

Usage:
  find_figures.py text.md [--csv-out sentences.csv] [--min-kinds 1]
"""
import argparse, csv, re, sys

KINDS = [
    ("percent", re.compile(r"\d[\d.,]*\s?(%|per ?cent\b|percent\b|pp\b|percentage points?\b)", re.I)),
    ("money", re.compile(r"([$€£¥]\s?\d|\b\d[\d.,]*\s?(USD|EUR|GBP|JPY|CHF|dollars?|euros?|pounds?)\b)", re.I)),
    ("date", re.compile(r"\b(1[89]\d\d|20\d\d)\b|\b(January|February|March|April|May|June|July|August|September|October|November|December)\b|\bQ[1-4]\b", re.I)),
    ("number", re.compile(r"\b\d[\d.,]*\b|\b(one|two|three|four|five|six|seven|eight|nine|ten|dozen|hundred|thousand|million|billion|half|third|quarter)\b", re.I)),
    ("ranking", re.compile(r"\b(first|only|largest|biggest|smallest|fastest|highest|lowest|most|least|leading|top|record|best|worst|more than|less than|fewer than|compared with|than)\b", re.I)),
    ("change", re.compile(r"\b(doubled|tripled|halved|rose|risen|fell|fallen|grew|grown|increased?|decreased?|dropped|cut|up|down|growth|decline)\b", re.I)),
    ("quote", re.compile(r"[\"“”«»]|\b(said|says|told|according to)\b", re.I)),
]
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"“«(])")


def die(msg):
    print(f"find_figures: {msg}", file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="Sentences with checkable elements (read-only).")
    ap.add_argument("file", help="plain-text or Markdown file, or - for standard input")
    ap.add_argument("--csv-out", default="", help="also write the rows as CSV")
    ap.add_argument("--min-kinds", type=int, default=1, help="list a sentence only if it has at least this many kinds (default 1)")
    a = ap.parse_args()
    if a.min_kinds < 1:
        die("--min-kinds must be 1 or more")
    try:
        fh = sys.stdin if a.file == "-" else open(a.file, encoding="utf-8")
    except OSError as e:
        die(f"cannot read {a.file}: {e.strerror}")
    with fh:
        lines = fh.read().splitlines()
    if not any(l.strip() for l in lines):
        die("empty text")
    rows, total = [], 0
    for ln, line in enumerate(lines, start=1):
        text = re.sub(r"^\s*([#>*-]+|\d+[.)])\s+", "", line).strip()
        if not text:
            continue
        for s in SENT.split(text):
            total += 1
            kinds = [k for k, rx in KINDS if rx.search(s)]
            if "number" in kinds and ({"percent", "money"} & set(kinds)):
                kinds.remove("number")
            if len(kinds) >= a.min_kinds:
                rows.append((ln, ",".join(kinds), s))
    print(f"# {len(rows)} of {total} sentences have a checkable element. Candidates only: every claim still goes into the claims list "
          "with its exact wording, and opinions and forecasts are marked as not checkable.")
    print("| row | line | spotted | sentence |")
    print("|---|---|---|---|")
    for i, (ln, k, s) in enumerate(rows, start=1):
        print(f"| s{i} | {ln} | {k} | {s.replace('|', '/')} |")
    if a.csv_out:
        with open(a.csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["row", "line", "spotted", "sentence"])
            for i, (ln, k, s) in enumerate(rows, start=1):
                w.writerow([f"s{i}", ln, k, s])


if __name__ == "__main__":
    main()
