#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Replay written lead routing rules on past leads and show what would change. Reads only.

rules.json:
  {"rules": [
     {"name": "existing account owner", "assign_from": "account_owner"},
     {"name": "named accounts", "match": {"company": ["Northwind Ltd"]}, "owner": "dana"},
     {"name": "EU mid-size", "match": {"region": ["EU"], "size_band": ["50-249"]}, "pool": "eu-mid"}],
   "pools": {"eu-mid": {"members": {"ari": 1, "kim": 2}, "away": ["kim"]}},
   "fallback": {"name": "fallback queue", "owner": "queue-owner"}}

A rule fires when every key in «match» holds one of the listed values (case
folded); {"present": true} means the field is not blank. «assign_from» takes
the owner from a lead column and fires only when that column is filled. A pool
rotates by weight (smooth weighted round-robin) and skips members marked away.
With --account-col, every later lead of an account already assigned in this
run goes to the same owner (rule «same account in this run»), unless an
«assign_from» rule names an owner on the lead itself.

leads.csv: one row per lead, in arrival order, with an id column, the fields the
rules use, and the owner it actually got (--current-col).

Prints a summary to stdout; with --out writes one row per lead:
id, rule, proposed_owner, current_owner, changed. Standard library only; no network.
"""
import argparse
import csv
import json
import sys
from collections import Counter


def norm(v):
    return (v or "").strip().casefold()


def matches(rule, lead):
    for k, want in (rule.get("match") or {}).items():
        v = norm(lead.get(k))
        if isinstance(want, dict):
            if want.get("present") and not v:
                return False
        elif v not in {norm(x) for x in want}:
            return False
    if "assign_from" in rule and not norm(lead.get(rule["assign_from"])):
        return False
    return True


class Pool:
    def __init__(self, cfg):
        away = {norm(x) for x in cfg.get("away", [])}
        self.w = {m: float(w) for m, w in cfg["members"].items() if norm(m) not in away and float(w) > 0}
        self.cur = {m: 0.0 for m in self.w}

    def next(self):
        if not self.w:
            return None
        total = sum(self.w.values())
        for m in self.w:
            self.cur[m] += self.w[m]
        pick = max(self.w, key=lambda m: (self.cur[m], m))
        self.cur[pick] -= total
        return pick


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rules")
    ap.add_argument("leads")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--current-col", default="owner", help="column with the owner the lead actually got")
    ap.add_argument("--account-col", help="column that identifies the account (company domain, account id)")
    ap.add_argument("--out", help="write per-lead results to this CSV")
    a = ap.parse_args()

    cfg = json.load(open(a.rules, encoding="utf-8"))
    rules = cfg.get("rules", [])
    pools = {k: Pool(v) for k, v in cfg.get("pools", {}).items()}
    fb = cfg.get("fallback")
    if not fb or not fb.get("owner"):
        sys.exit("rules.json needs a fallback with an owner, so no lead waits unassigned")
    for r in rules:
        if "pool" in r and r["pool"] not in pools:
            sys.exit(f"rule «{r.get('name')}» names an unknown pool {r['pool']}")
        if not any(k in r for k in ("owner", "pool", "assign_from")):
            sys.exit(f"rule «{r.get('name')}» assigns nobody")

    with open(a.leads, newline="", encoding="utf-8-sig") as f:
        leads = list(csv.DictReader(f))

    seen_account = {}
    out, per_rule, per_owner = [], Counter(), Counter()
    for lead in leads:
        rule_name, owner = None, None
        acct = norm(lead.get(a.account_col)) if a.account_col else ""
        for r in rules:
            if acct and acct in seen_account and "assign_from" not in r:
                # an owner named on the lead itself still wins; otherwise keep the account together
                rule_name, owner = "same account in this run", seen_account[acct]
                break
            if not matches(r, lead):
                continue
            if "owner" in r:
                owner = r["owner"]
            elif "assign_from" in r:
                owner = lead.get(r["assign_from"]).strip()
            else:
                owner = pools[r["pool"]].next()
                if owner is None:
                    continue  # everyone in the pool is away: try the next rule
            rule_name = r.get("name", "unnamed rule")
            break
        if owner is None:
            if acct and acct in seen_account:
                rule_name, owner = "same account in this run", seen_account[acct]
            else:
                rule_name, owner = fb.get("name", "fallback"), fb["owner"]
        if acct and acct not in seen_account:
            seen_account[acct] = owner
        cur = (lead.get(a.current_col) or "").strip()
        changed = norm(cur) != norm(owner)
        out.append({"id": lead.get(a.id_col, ""), "rule": rule_name, "proposed_owner": owner,
                    "current_owner": cur, "changed": "yes" if changed else "no"})
        per_rule[rule_name] += 1
        per_owner[owner] += 1

    n_changed = sum(1 for r in out if r["changed"] == "yes")
    print(f"Replayed {len(out)} leads from {a.leads} with {a.rules}.")
    print(f"Assignments that would change: {n_changed}.")
    print("By rule:")
    for k, v in per_rule.most_common():
        print(f"  {v:5d}  {k}")
    print("By proposed owner:")
    for k, v in per_owner.most_common():
        print(f"  {v:5d}  {k}")
    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["id", "rule", "proposed_owner", "current_owner", "changed"])
            w.writeheader()
            w.writerows(out)
        print(f"Per-lead results: {a.out}")
    print("This is a replay: nothing was reassigned. A change goes to the owner as a proposal with undo.")


if __name__ == "__main__":
    main()
