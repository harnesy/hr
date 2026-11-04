#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Pipeline stage report from a CRM deal export (CSV). Reads only; writes Markdown to stdout.

Columns expected (rename with --col field=Header): id, stage, amount, created,
stage_entered, close_date, next_step, last_activity, status (open, won or lost),
and optionally segment. For lost deals, «stage» must be the stage the deal had
reached when it was lost. Dates are YYYY-MM-DD.

Prints: a data-quality block first, the per-stage roll-up of open deals, risk
flags, the historical win rate from each stage per quarter, and a range for open
pipeline value built from the lowest and highest quarterly rates. The range is
a reading of history, not a forecast anyone promises.

Standard library only; no network.
"""
import argparse
import csv
import datetime as dt
import sys
from collections import defaultdict

FIELDS = ["id", "stage", "amount", "created", "stage_entered", "close_date",
          "next_step", "last_activity", "status", "segment"]


def parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s[:10])
    except ValueError:
        return None


def parse_amount(s):
    s = (s or "").strip().replace(",", "").replace(" ", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def quarter(d):
    return f"{d.year}-Q{(d.month - 1) // 3 + 1}"


def money(x):
    return f"{x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", help="CSV export of deals")
    ap.add_argument("--stages", required=True, help="open stages in order, comma-separated, as the team names them")
    ap.add_argument("--today", help="report date YYYY-MM-DD (default: today)")
    ap.add_argument("--stale-days", type=int, default=30, help="no activity for more than N days counts as stale (the owner's threshold)")
    ap.add_argument("--age-from", choices=["stage_entered", "created"], default="stage_entered", help="which date age is measured from")
    ap.add_argument("--quarters", type=int, default=2, help="closed quarters of history used for the baseline (default 2)")
    ap.add_argument("--by-segment", action="store_true", help="repeat the roll-up per segment")
    ap.add_argument("--col", action="append", default=[], help="column mapping field=Header, e.g. amount=Amount (EUR)")
    ap.add_argument("--top", type=int, default=10, help="how many flagged deals to list")
    a = ap.parse_args()

    today = parse_date(a.today) if a.today else dt.date.today()
    stages = [s.strip() for s in a.stages.split(",") if s.strip()]
    rank = {s.lower(): i for i, s in enumerate(stages)}
    cols = {f: f for f in FIELDS}
    for m in a.col:
        k, _, v = m.partition("=")
        if k not in cols:
            sys.exit(f"unknown field in --col: {k}")
        cols[k] = v

    with open(a.export, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [f for f in FIELDS if f != "segment" and cols[f] not in (reader.fieldnames or [])]
        if missing:
            sys.exit("missing columns: " + ", ".join(cols[m] for m in missing))
        rows = [{k: (r.get(cols[k]) or "").strip() for k in FIELDS} for r in reader]

    open_d, closed = [], []
    dq = defaultdict(list)
    for r in rows:
        st = r["status"].lower()
        r["_amount"] = parse_amount(r["amount"])
        r["_close"] = parse_date(r["close_date"])
        r["_act"] = parse_date(r["last_activity"])
        r["_age0"] = parse_date(r[a.age_from])
        r["_rank"] = rank.get(r["stage"].lower())
        if st == "open":
            open_d.append(r)
            if r["_amount"] is None:
                dq["blank or unreadable amount"].append(r["id"])
            if r["_close"] is None:
                dq["blank close date"].append(r["id"])
            elif r["_close"] < today:
                dq["close date in the past"].append(r["id"])
            if not r["next_step"]:
                dq["blank next step"].append(r["id"])
            if r["_act"] is None:
                dq["no activity date"].append(r["id"])
            if r["_age0"] is None:
                dq[f"blank {a.age_from} (age unknown)"].append(r["id"])
            if r["_rank"] is None:
                dq["stage not in --stages"].append(r["id"])
        elif st in ("won", "lost"):
            closed.append(r)
            if r["_close"] is None:
                dq["closed deal without close date (left out of history)"].append(r["id"])
            if st == "lost" and r["_rank"] is None:
                dq["lost deal with a stage not in --stages (left out of history)"].append(r["id"])
        else:
            dq["unknown status"].append(r["id"])

    print(f"# Pipeline report, {today.isoformat()}")
    print()
    print(f"Export: `{a.export}`, {len(rows)} rows ({len(open_d)} open, {len(closed)} closed). "
          f"Age measured from **{a.age_from}**. Stale = no activity for more than {a.stale_days} days (owner's threshold). "
          "This report only reads the export.")
    print()
    print("## Data quality (read first)")
    print()
    if not dq:
        print("No gaps found in the checked fields.")
    for k, ids in dq.items():
        shown = ", ".join(ids[:15]) + (" …" if len(ids) > 15 else "")
        print(f"- {k}: {len(ids)} ({shown})")
    print()

    def rollup(deals, title):
        print(f"## {title}")
        print()
        print("| stage | deals | value | avg age (days) | no next step | stale | close date passed |")
        print("|---|---|---|---|---|---|---|")
        for i, s in enumerate(stages + ["(stage not listed)"]):
            ds = [d for d in deals if (d["_rank"] == i if i < len(stages) else d["_rank"] is None)]
            if not ds and i == len(stages):
                continue
            val = sum(d["_amount"] or 0 for d in ds)
            ages = [(today - d["_age0"]).days for d in ds if d["_age0"]]
            avg = f"{sum(ages) / len(ages):.0f}" if ages else "unknown"
            nn = sum(1 for d in ds if not d["next_step"])
            stale = sum(1 for d in ds if d["_act"] is None or (today - d["_act"]).days > a.stale_days)
            past = sum(1 for d in ds if d["_close"] and d["_close"] < today)
            print(f"| {s} | {len(ds)} | {money(val)} | {avg} | {nn} | {stale} | {past} |")
        print()

    rollup(open_d, "Open pipeline by stage")
    if a.by_segment:
        for seg in sorted({d["segment"] or "(no segment)" for d in open_d}):
            rollup([d for d in open_d if (d["segment"] or "(no segment)") == seg], f"Open pipeline by stage, segment {seg}")

    print("## Risk flags")
    print()
    flagged = []
    for d in open_d:
        why = []
        if not d["next_step"]:
            why.append("no next step")
        if d["_act"] is None or (today - d["_act"]).days > a.stale_days:
            why.append("stale")
        if d["_close"] and d["_close"] < today:
            why.append("close date passed")
        if why:
            flagged.append((d["_amount"] or 0, d["id"], d["stage"], ", ".join(why)))
    flagged.sort(reverse=True)
    print(f"{len(flagged)} open deals carry at least one flag; the {min(a.top, len(flagged))} largest:")
    print()
    for amt, i, s, w in flagged[:a.top]:
        print(f"- {i} ({s}, {money(amt)}): {w}")
    print()

    print("## History: win rate from each stage, by quarter of close")
    print()
    hist = [d for d in closed if d["_close"] and (d["status"].lower() == "won" or d["_rank"] is not None)]
    qs = sorted({quarter(d["_close"]) for d in hist if quarter(d["_close"]) < quarter(today)})[-a.quarters:]
    if not qs:
        print("No closed quarters in the export: no baseline, no range.")
        return
    rates = {}
    print("| stage | " + " | ".join(qs) + " |")
    print("|---|" + "---|" * len(qs))
    for i, s in enumerate(stages):
        cells = []
        for q in qs:
            reached = [d for d in hist if quarter(d["_close"]) == q and (d["status"].lower() == "won" or d["_rank"] >= i)]
            won = sum(1 for d in reached if d["status"].lower() == "won")
            r = won / len(reached) if reached else None
            rates[(s, q)] = r
            cells.append(f"{r:.0%} ({won}/{len(reached)})" if r is not None else "no data")
        print(f"| {s} | " + " | ".join(cells) + " |")
    print()
    lo = hi = 0.0
    gaps = []
    for d in open_d:
        if d["_rank"] is None or d["_amount"] is None:
            continue
        rs = [rates[(stages[d["_rank"]], q)] for q in qs if rates[(stages[d["_rank"]], q)] is not None]
        if not rs:
            gaps.append(d["id"])
            continue
        lo += d["_amount"] * min(rs)
        hi += d["_amount"] * max(rs)
    print(f"Range for open pipeline value from the quarters {', '.join(qs)}: **{money(lo)} to {money(hi)}** "
          "(each open deal times the lowest and the highest win rate of its stage). "
          "Deals without amount, without a listed stage or without history are left out"
          + (f" ({len(gaps)} without history)." if gaps else "."))
    print("Compare this range with any stage-probability figure; explain the gap as a risk, do not average it away.")


if __name__ == "__main__":
    main()
