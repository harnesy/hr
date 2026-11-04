#!/usr/bin/env python3
# Copyright (c) 2026 Pavel Buchnev (harnsy)
# SPDX-License-Identifier: MIT
"""Driver-based monthly scenario model for a young company. Standard library only; no network.

usage:
  model_template.py template OUT.json [--months 24] [--currency EUR] [--start 2026-11]
      Write a blank assumptions file: every driver with value, unit, source, date and owner to fill in,
      and three scenarios (base, downside, upside) with a trigger event each.

  model_template.py run ASSUMPTIONS.json --out DIR
      Build one monthly CSV per scenario, summary.csv and assumptions.md (assumptions with their
      sources, gaps, checks, the three drivers that move ending cash most, and the scenario label).

Every typed number lives in ASSUMPTIONS.json; the CSVs are calculated from it and nothing else.
Outputs are scenarios, not forecasts.

Exit codes: 0 = built, checks passed (gaps, if any, are listed); 2 = input missing or invalid;
3 = built, but a check failed (see assumptions.md and the printed lines).
"""
import argparse
import csv
import json
import math
import os
import sys

LABEL = "Scenario, not a forecast: every figure follows from the assumptions listed with it."

# driver key -> (unit, meaning)
DRIVERS = {
    "start_cash": ("money", "cash in the bank at the start of month 1"),
    "start_customers": ("count", "paying customers at the start of month 1"),
    "new_customers_per_month": ("count", "new paying customers in month 1"),
    "new_customers_growth": ("share per month", "growth of new customers per month, 0.03 = 3 %"),
    "monthly_churn": ("share per month", "customers lost in a month / customers at its start"),
    "price_per_customer_month": ("money", "recurring revenue per customer per month"),
    "gross_margin": ("share", "(revenue - cost of revenue) / revenue"),
    "headcount_start": ("people", "people paid at the start of month 1"),
    "hires_per_month": ("people per month", "net hires per month (an average; 0.5 = one every two months)"),
    "cost_per_head_month": ("money", "full monthly cost of one person"),
    "other_costs_month": ("money", "all other operating costs in month 1"),
    "other_costs_growth": ("share per month", "growth of other costs per month"),
    "funding_amount": ("money", "cash received from a planned raise or loan (0 = none)"),
    "funding_month": ("month number", "month in which that cash arrives (0 = none)"),
}

COLUMNS = ["month", "period", "customers_start", "new", "churned", "customers_end", "revenue",
           "cost_of_revenue", "gross_profit", "headcount", "payroll", "other_costs",
           "operating_cash_flow", "funding", "cash_end", "flag"]


def blank(months, currency, start):
    a = {k: {"value": None, "unit": u, "meaning": m, "source": "", "date": "", "owner": ""}
         for k, (u, m) in DRIVERS.items()}
    return {
        "title": "", "currency": currency, "start_month": start, "months": months, "label": LABEL,
        "assumptions": a,
        "scenarios": {
            "base": {"overrides": {}, "trigger": "what has to stay true for this case"},
            "downside": {"overrides": {}, "trigger": "the event that would move us here"},
            "upside": {"overrides": {}, "trigger": "the event that would move us here"},
        },
    }


def period_name(start, m):
    try:
        y, mo = (int(x) for x in start.split("-"))
    except (ValueError, AttributeError):
        return str(m)
    mo += m - 1
    y += (mo - 1) // 12
    mo = (mo - 1) % 12 + 1
    return f"{y:04d}-{mo:02d}"


def resolve(doc, scen):
    """Return {driver: value} and a list of gaps for one scenario."""
    vals, gaps, errors = {}, [], []
    over = doc["scenarios"][scen].get("overrides", {}) or {}
    for k in DRIVERS:
        item = doc["assumptions"].get(k)
        if item is None:
            errors.append(f"assumption {k} is missing")
            continue
        src = item
        if k in over:
            o = over[k]
            src = o if isinstance(o, dict) else {"value": o}
            for f in ("source", "date", "owner"):
                if not src.get(f):
                    gaps.append(f"{scen}: override {k} has no {f}")
        v = src.get("value")
        if not isinstance(v, (int, float)) or isinstance(v, bool) or math.isnan(v):
            errors.append(f"{scen}: {k} has no numeric value")
            continue
        vals[k] = float(v)
    for k, item in doc["assumptions"].items():
        if k in DRIVERS:
            for f in ("source", "date", "owner"):
                if not item.get(f):
                    gaps.append(f"assumption {k} has no {f}")
    if not errors:
        for k in ("monthly_churn", "gross_margin"):
            if not 0 <= vals[k] <= 1:
                errors.append(f"{scen}: {k} must be a share between 0 and 1")
    return vals, gaps, errors


def build(v, months, start):
    rows = []
    cust = v["start_customers"]
    cash = v["start_cash"]
    for m in range(1, months + 1):
        new = v["new_customers_per_month"] * (1 + v["new_customers_growth"]) ** (m - 1)
        churned = cust * v["monthly_churn"]
        end = cust + new - churned
        revenue = end * v["price_per_customer_month"]
        cor = revenue * (1 - v["gross_margin"])
        gp = revenue - cor
        head = v["headcount_start"] + v["hires_per_month"] * m
        payroll = head * v["cost_per_head_month"]
        other = v["other_costs_month"] * (1 + v["other_costs_growth"]) ** (m - 1)
        ocf = gp - payroll - other
        funding = v["funding_amount"] if int(v["funding_month"]) == m else 0.0
        cash = cash + ocf + funding
        rows.append({
            "month": m, "period": period_name(start, m), "customers_start": cust, "new": new,
            "churned": churned, "customers_end": end, "revenue": revenue, "cost_of_revenue": cor,
            "gross_profit": gp, "headcount": head, "payroll": payroll, "other_costs": other,
            "operating_cash_flow": ocf, "funding": funding, "cash_end": cash,
            "flag": "CASH BELOW ZERO" if cash < 0 else "",
        })
        cust = end
    return rows


def checks(rows, v):
    out = []
    tol = 0.01 * max(1, len(rows))
    s = lambda c: sum(r[c] for r in rows)
    ok = abs(s("revenue") - s("cost_of_revenue") - s("gross_profit")) <= tol
    out.append(("revenue - cost of revenue = gross profit, all months", ok))
    ok = abs(v["start_customers"] + s("new") - s("churned") - rows[-1]["customers_end"]) <= tol
    out.append(("customers: start + new - churned = end", ok))
    ok = abs(v["start_cash"] + s("operating_cash_flow") + s("funding") - rows[-1]["cash_end"]) <= tol
    out.append(("cash: start + operating cash flow + funding = end", ok))
    ok = all(abs(r["gross_profit"] - r["payroll"] - r["other_costs"] - r["operating_cash_flow"]) <= 0.01 for r in rows)
    out.append(("operating cash flow = gross profit - payroll - other costs, each month", ok))
    return out


def summary(name, rows):
    low = min(rows, key=lambda r: r["cash_end"])
    neg = next((r for r in rows if r["cash_end"] < 0), None)
    return {
        "scenario": name, "cash_end": rows[-1]["cash_end"], "lowest_cash": low["cash_end"],
        "lowest_cash_period": low["period"], "first_month_below_zero": neg["period"] if neg else "none in range",
        "customers_end": rows[-1]["customers_end"], "monthly_revenue_end": rows[-1]["revenue"],
    }


def sensitivity(v, months, start):
    """Ending-cash effect of raising each driver by 10 %, largest first."""
    base = build(v, months, start)[-1]["cash_end"]
    eff = []
    for k in DRIVERS:
        if k == "funding_month" or v[k] == 0:
            continue
        w = dict(v)
        w[k] = v[k] * 1.1
        if k in ("monthly_churn", "gross_margin"):
            w[k] = min(1.0, w[k])
        eff.append((abs(build(w, months, start)[-1]["cash_end"] - base), k,
                    build(w, months, start)[-1]["cash_end"] - base))
    eff.sort(reverse=True)
    return [(k, d) for _, k, d in eff[:3]]


def fmt(x):
    return f"{x:.2f}" if isinstance(x, float) else str(x)


def write_csv(path, rows, cols):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([fmt(r[c]) for c in cols])


def cmd_template(a):
    doc = blank(a.months, a.currency, a.start)
    with open(a.out, "w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    print(f"wrote {a.out}: fill every value, source, date and owner, then run it")
    return 0


def cmd_run(a):
    try:
        with open(a.assumptions) as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read {a.assumptions}: {e}", file=sys.stderr)
        return 2
    months = int(doc.get("months") or 0)
    if not 1 <= months <= 120 or not doc.get("scenarios"):
        print("months must be 1..120 and at least one scenario is needed", file=sys.stderr)
        return 2
    start = doc.get("start_month", "")
    cur = doc.get("currency", "")
    os.makedirs(a.out, exist_ok=True)
    results, all_gaps, failed, sums = {}, set(), False, []
    for scen in doc["scenarios"]:
        v, gaps, errors = resolve(doc, scen)
        if errors:
            for e in errors:
                print("input:", e, file=sys.stderr)
            return 2
        all_gaps.update(gaps)
        rows = build(v, months, start)
        write_csv(os.path.join(a.out, f"scenario-{scen}.csv"), rows, COLUMNS)
        results[scen] = (v, rows, checks(rows, v))
        sums.append(summary(scen, rows))
    order = []
    names = list(results)
    if all(n in results for n in ("downside", "base", "upside")):
        e = {n: results[n][1][-1]["cash_end"] for n in ("downside", "base", "upside")}
        order.append(("ending cash: downside <= base <= upside", e["downside"] <= e["base"] <= e["upside"]))
    write_csv(os.path.join(a.out, "summary.csv"), sums, list(sums[0]))

    md = [f"# {doc.get('title') or 'Scenario model'}", "", f"**{LABEL}**", "",
          f"Currency: {cur or 'not stated'}. First month: {start or 'not stated'}. Months: {months}.", "",
          "## Assumptions", "", "| driver | value | unit | source | date | owner |", "|---|---|---|---|---|---|"]
    for k in DRIVERS:
        it = doc["assumptions"][k]
        md.append(f"| {k} | {it.get('value')} | {it.get('unit', DRIVERS[k][0])} | {it.get('source') or 'GAP'} | "
                  f"{it.get('date') or 'GAP'} | {it.get('owner') or 'GAP'} |")
    md += ["", "## Scenarios", ""]
    for scen, spec in doc["scenarios"].items():
        ov = ", ".join(f"{k} = {o['value'] if isinstance(o, dict) else o}" for k, o in (spec.get("overrides") or {}).items())
        md.append(f"- **{scen}**: {ov or 'the assumptions above'}. Trigger: {spec.get('trigger') or 'GAP'}.")
    md += ["", "## Results (scenarios, not forecasts)", "", "| scenario | cash at end | lowest cash | lowest in | first month below zero |",
           "|---|---|---|---|---|"]
    for s in sums:
        md.append(f"| {s['scenario']} | {s['cash_end']:.2f} | {s['lowest_cash']:.2f} | {s['lowest_cash_period']} | {s['first_month_below_zero']} |")
    md += ["", "## Checks", ""]
    for scen in names:
        for text, ok in results[scen][2]:
            md.append(f"- [{'x' if ok else ' '}] {scen}: {text}")
            failed |= not ok
    for text, ok in order:
        md.append(f"- [{'x' if ok else ' '}] {text}")
        failed |= not ok
    neg = [s["scenario"] for s in sums if s["first_month_below_zero"] != "none in range"]
    md.append(f"- cash below zero in: {', '.join(neg) if neg else 'no scenario'} (flagged month by month in the CSV)")
    if "base" in results:
        md += ["", "## What moves the base case most", "", "Ending cash after raising each driver by 10 %:", ""]
        for k, d in sensitivity(results["base"][0], months, start):
            md.append(f"- {k}: {d:+.2f}")
    md += ["", "## Gaps", ""] + ([f"- {g}" for g in sorted(all_gaps)] or ["- none"])
    md += ["", "Model rules: customers at month end pay the full monthly price; cost of revenue = revenue x (1 - gross margin);",
           "headcount grows by hires_per_month each month; funding arrives in funding_month. Change the rules here only with the owner.", ""]
    with open(os.path.join(a.out, "assumptions.md"), "w") as f:
        f.write("\n".join(md))

    for s in sums:
        print(f"{s['scenario']}: cash at end {s['cash_end']:.2f}, lowest {s['lowest_cash']:.2f} in {s['lowest_cash_period']}, "
              f"below zero from {s['first_month_below_zero']}")
    print(f"gaps: {len(all_gaps)}; checks: {'FAILED' if failed else 'passed'}; files in {a.out}")
    return 3 if failed else 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("template")
    t.add_argument("out")
    t.add_argument("--months", type=int, default=24)
    t.add_argument("--currency", default="")
    t.add_argument("--start", default="")
    r = sub.add_parser("run")
    r.add_argument("assumptions")
    r.add_argument("--out", required=True)
    a = p.parse_args()
    return cmd_template(a) if a.cmd == "template" else cmd_run(a)


if __name__ == "__main__":
    sys.exit(main())
