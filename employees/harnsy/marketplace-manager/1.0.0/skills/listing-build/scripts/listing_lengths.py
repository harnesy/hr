#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Check a listing draft against the field limits recorded in a rules check, and flag claim words.

listing.json: {"title": "...", "key_points": ["...", "..."], "description": "...", ...}
limits.json:  {"page": "<address of the rule page>", "read_on": "YYYY-MM-DD",
               "fields": {"title": {"max_chars": 150},
                          "key_points": {"max_items": 5, "max_chars_each": 250},
                          "description": {"min_chars": 200, "max_chars": 2000, "max_bytes": 2000}}}
terms.txt (optional, --terms): one word or phrase per line that needs a document
behind it (for example a material, a certification or a health claim).

The limits are not built in: they come from the platform's live page, read and dated
by the person or the agent before each job. Characters are counted as Unicode code
points; bytes as UTF-8. Prints a table; exits 1 when any field breaks a limit.
Standard library only; no network.
"""
import argparse
import json
import re
import sys


def check(name, value, rule, out):
    def row(what, got, limit, ok):
        out.append((name, what, str(got), str(limit), "ok" if ok else "OVER" if "max" in what else "UNDER"))
    if isinstance(value, list):
        if "max_items" in rule:
            row("max_items", len(value), rule["max_items"], len(value) <= rule["max_items"])
        for i, v in enumerate(value, start=1):
            if "max_chars_each" in rule:
                row(f"max_chars_each[{i}]", len(v), rule["max_chars_each"], len(v) <= rule["max_chars_each"])
            if "max_bytes_each" in rule:
                b = len(v.encode("utf-8"))
                row(f"max_bytes_each[{i}]", b, rule["max_bytes_each"], b <= rule["max_bytes_each"])
        return
    v = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    if "max_chars" in rule:
        row("max_chars", len(v), rule["max_chars"], len(v) <= rule["max_chars"])
    if "min_chars" in rule:
        row("min_chars", len(v), rule["min_chars"], len(v) >= rule["min_chars"])
    if "max_bytes" in rule:
        b = len(v.encode("utf-8"))
        row("max_bytes", b, rule["max_bytes"], b <= rule["max_bytes"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("listing")
    ap.add_argument("limits")
    ap.add_argument("--terms", help="file with claim words that need a document, one per line")
    a = ap.parse_args()
    listing = json.load(open(a.listing, encoding="utf-8"))
    limits = json.load(open(a.limits, encoding="utf-8"))
    fields = limits.get("fields", {})
    print(f"Limits from: {limits.get('page', '(no page recorded)')}, read on {limits.get('read_on', '(no date recorded)')}")
    if not limits.get("page") or not limits.get("read_on"):
        print("WARNING: limits without a page and a read date; record them from the live page before relying on this check.")
    out = []
    for name, rule in fields.items():
        if name not in listing:
            out.append((name, "present", "missing", "required by limits file", "MISSING"))
            continue
        check(name, listing[name], rule, out)
    unchecked = [k for k in listing if k not in fields]
    print()
    print(f"{'field':<16} {'check':<20} {'value':>7} {'limit':>7}  result")
    for r in out:
        print(f"{r[0]:<16} {r[1]:<20} {r[2]:>7} {r[3]:>7}  {r[4]}")
    if unchecked:
        print(f"\nFields with no recorded limit (not checked): {', '.join(unchecked)}")
    if a.terms:
        terms = [t.strip() for t in open(a.terms, encoding="utf-8") if t.strip() and not t.startswith("#")]
        text = json.dumps(listing, ensure_ascii=False)
        hits = []
        for t in terms:
            n = len(re.findall(r"(?<!\w)" + re.escape(t) + r"(?!\w)", text, re.I))
            if n:
                hits.append((t, n))
        print("\nClaim words found (each needs a document from the product owner):")
        for t, n in hits:
            print(f"  {t}: {n}")
        if not hits:
            print("  none")
    bad = [r for r in out if r[4] != "ok"]
    print(f"\n{len(bad)} problem(s).")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
