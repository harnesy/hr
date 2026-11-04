---
name: scenario-model
description: Build «what if» scenarios for a young company (runway, hiring, pricing, timing of a raise) from one dated assumptions sheet: base, downside and upside switched in one place, each with the event that would move you to it, checks in every scenario, an optional dilution line marked as an estimate, and every output labelled as a scenario, not a forecast. Ships a standard-library Python template that writes the model as CSV and Markdown.
---

# Scenario model

Nobody knows next year's numbers. A scenario model says what follows from a stated set of assumptions, and which assumptions matter most. This skill keeps every assumption visible, dated and owned, and never presents a scenario as a promise.

**Route:** measured drivers from `unit-economics` + the founder's plans → **scenario-model** → the founder decides → scenario pages for `investor-pack-draft`.

## When to use

- Runway: how many months of cash under different cases.
- A hiring plan, a price change, a new channel, the timing of a raise.
- Any «what happens if…» question about money.

## Inputs

- **Jurisdiction and currency:** the company's country and currency; the accountant and the lawyer, if any.
- **Each assumption** with value, unit, source, date and owner: cash, customers, new customers, churn, price, gross margin, headcount and hires, cost per person, other costs, any planned funding.
- **Each scenario's trigger:** the event that would make it the likely case.
- For a dilution line: the ownership estimate inputs (see step 5).

## Steps

1. **Write the assumptions sheet.** Run `python3 scripts/model_template.py template work/assumptions.json` and fill every value, source, date and owner. Measured values come from `unit-economics`; plans come from the founder and are labelled as plans.
2. **Define the scenarios** in the same file: base, downside, upside, each as a few changed drivers plus its trigger event. One place switches them; nothing is typed anywhere else.
3. **Run the model:** `python3 scripts/model_template.py run work/assumptions.json --out work/out`. It writes one monthly CSV per scenario, `summary.csv` and `assumptions.md`.
4. **Read the checks:** totals add in every month; customer and cash walks end at their end figures; downside sits below base and base below upside; months with cash below zero are flagged, never hidden. A failed check is fixed or reported before anything else.
5. **Dilution line (optional).** Ownership after a raise needs the share register, each instrument's amount and terms (caps, discounts, how the price is measured), side letters, the planned round and the planned option pool. Until a price is agreed the result is an estimate and is labelled so; anything the model cannot handle is reported, not guessed. Instrument terms and the option pool are questions for the founder's lawyer.
6. **Write the note:** months of cash per scenario, the first month below zero if any, and the three assumptions that move the result most (the tool lists them from a 10 % change in each).

## Checks before hand-over

- No typed number outside the assumptions file.
- All checks pass, or the failure is reported first.
- Every assumption has a source, a date and an owner, or appears under «Gaps».
- Every output says «scenario, not a forecast»; no growth, return or valuation is promised.
- Any tax, grant or legal assumption names its official source and the date checked, and is marked for the tax professional or lawyer.

## Artefacts

- `work/assumptions.json`: the only place with typed numbers.
- `work/out/scenario-<name>.csv`, `work/out/summary.csv`, `work/out/assumptions.md`.
- `work/note.md`: one page for the founder.

## Hand-over

- **To the founder:** the note and the files; the founder decides what to do.
- **To the founder's lawyer:** questions on instruments, ownership and the option pool.
- **To `investor-pack-draft`:** the scenario pages, with their labels and assumptions.
- **To the accountant:** any question about the starting figures in the books.

## Tools

`scripts/model_template.py` writes a blank driver-based monthly model and runs it for each scenario. It reads one assumptions file and writes CSV and Markdown; it uses the Python standard library only and makes no network calls.

### Requirements

```sh
python3 --version   # Python 3.8 or later, standard library only
```

The CSV files open in any spreadsheet program.

### Example

```sh
# 1. a blank assumptions file to fill in (value, unit, source, date and owner for every driver)
python3 scripts/model_template.py template work/assumptions.json --months 24 --currency EUR --start 2027-01

# 2. after filling it in: one CSV per scenario, summary.csv and assumptions.md
python3 scripts/model_template.py run work/assumptions.json --out work/out

# a filled-in example with made-up values
python3 scripts/model_template.py run scripts/assumptions.example.json --out work/example
```

`assumptions.md` lists every assumption with its source, date and owner, the gaps, each scenario's trigger event, the results, the checks, and the three drivers that move ending cash most in the base case. Every output carries the label «scenario, not a forecast».

Exit codes: 0 = built and checks passed (gaps are listed, not fatal); 2 = a value is missing or invalid; 3 = built, but a check failed.

### Model rules

- Customers: start of month + new − lost = end of month; lost = customers at the start × monthly churn.
- Revenue = customers at month end × price; cost of revenue = revenue × (1 − gross margin).
- Payroll = headcount × cost per head; headcount grows by `hires_per_month`.
- Cash at month end = cash at the start + gross profit − payroll − other costs + funding in its month.
- A month with cash below zero is flagged in the CSV.

Change the rules only with the owner of the model, and note the change in `assumptions.md`.

## Sources

Adapted from the 3-statement-model (scenario section) and audit-xls skills in github.com/anthropics/financial-services-plugins (© Anthropic, PBC; Apache License 2.0), changed by harnsy; from the finance-fpa-analyst agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors); and from the cap-table skill in github.com/1984vc/cap-table (MIT, © 2024 1984 Ventures). All adapted. The script is our own code; no source code was copied.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
