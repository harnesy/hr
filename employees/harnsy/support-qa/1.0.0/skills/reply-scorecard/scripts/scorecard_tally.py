#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Tally reply scorecards: one line per reply, and criterion trends per team. Never per person.

scores.csv: one row per reply and criterion, columns reply_id, team, criterion,
level (and optionally evidence). Levels are the anchor names in order, given with
--levels (default: weak,acceptable,strong); «n/a» marks a criterion that does not
apply to the reply.

The script refuses any column that names a person (agent, author, employee,
person, staff, owner, assignee, name, email): scorecards judge replies, and
totals per person are not produced.

Prints Markdown: per reply, the count of each level and the weak criteria; per team,
for each criterion, the count and share of each level. Standard library only; no network.
"""
import argparse
import csv
import re
import sys
from collections import Counter, defaultdict

PERSON = re.compile(r"agent|author|employee|person|staff|owner|assignee|^name$|e-?mail|user_?name", re.I)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scores")
    ap.add_argument("--levels", default="weak,acceptable,strong", help="anchor levels, lowest first")
    a = ap.parse_args()
    levels = [x.strip().lower() for x in a.levels.split(",") if x.strip()]

    with open(a.scores, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        cols = rd.fieldnames or []
        bad = [c for c in cols if PERSON.search(c)]
        if bad:
            sys.exit("refused: column(s) " + ", ".join(bad) + " name a person. Remove them; scorecards judge replies, not people.")
        need = {"reply_id", "team", "criterion", "level"}
        if not need <= set(cols):
            sys.exit("missing columns: " + ", ".join(sorted(need - set(cols))))
        rows = list(rd)

    errors = []
    teams_of = defaultdict(set)
    for r in rows:
        teams_of[r["reply_id"]].add(r["team"])
    for rid, ts in sorted(teams_of.items()):
        if len(ts) > 1:
            errors.append(f"reply {rid} is filed under more than one team ({', '.join(sorted(ts))}); check the sheet")
    per_reply = defaultdict(Counter)
    weak_list = defaultdict(list)
    per_team = defaultdict(lambda: defaultdict(Counter))
    for i, r in enumerate(rows, start=2):
        lv = (r["level"] or "").strip().lower()
        if lv == "n/a":
            continue
        if lv not in levels:
            errors.append(f"line {i}: level «{r['level']}» is not one of {', '.join(levels)}")
            continue
        per_reply[r["reply_id"]][lv] += 1
        if lv == levels[0]:
            weak_list[r["reply_id"]].append(r["criterion"])
        per_team[r["team"]][r["criterion"]][lv] += 1

    print(f"# Scorecard tally: {a.scores}")
    print()
    print(f"{len(per_reply)} replies, {len(per_team)} team(s). Levels: {', '.join(levels)}. Totals per person are not produced.")
    if errors:
        print()
        print("## Problems in the sheet")
        print()
        for e in errors:
            print(f"- {e}")
    print()
    print("## Per reply")
    print()
    print("| reply | " + " | ".join(levels) + f" | {levels[0]} criteria |")
    print("|---|" + "---|" * len(levels) + "---|")
    for rid in sorted(per_reply):
        c = per_reply[rid]
        print(f"| {rid} | " + " | ".join(str(c[l]) for l in levels) + f" | {', '.join(weak_list[rid]) or '-'} |")
    print()
    for team in sorted(per_team):
        print(f"## Team {team}: criteria")
        print()
        print("| criterion | n | " + " | ".join(levels) + " |")
        print("|---|---|" + "---|" * len(levels))
        for crit in sorted(per_team[team]):
            c = per_team[team][crit]
            n = sum(c.values())
            print(f"| {crit} | {n} | " + " | ".join(f"{c[l]} ({c[l] / n:.0%})" for l in levels) + " |")
        print()
    print("Small samples swing: read shares together with n, and compare periods only on the same criteria and anchors.")


if __name__ == "__main__":
    main()
