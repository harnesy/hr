---
name: range-estimate
description: Estimate each piece of a work breakdown as a low, a likely and a high value with the assumptions behind them, mark what would widen the range, total the pieces with a small script (sums and a common weighting, optional team correction factor), and name the assumptions that move the total most - labelled «a range for planning; the owner sets any date». Use after a work breakdown, whenever someone asks how long or how much effort.
---

# Range estimate

A single number for a piece of work hides the most useful thing about it: how sure anyone can be. Three numbers per piece, a low, a likely and a high value, with the assumptions behind them, show both the size and the uncertainty. This skill estimates every piece that way, totals them, and tells the owner which assumptions matter most. It gives effort, never a date: the owner turns the range into a plan.

**Route:** a work breakdown → **range-estimate** → the owner and the project manager decide the date and the scope → after the work, `estimate-review`.

## When to use

- After `work-breakdown`, whenever someone asks how long or how much effort.
- When the scope or an assumption changes, to update the range.
- Not to commit a date, and not to compare the speed of people or teams.

## Inputs

- The breakdown, with its scope and investigation pieces.
- The team's correction factor from `estimate-review`, if there is one.
- Who will do the work, so they can check the numbers.

## Steps

1. **Form your own numbers first,** before reading anyone else's estimate, then compare and discuss differences.
2. **Give each piece three values:** low (if the assumptions hold and nothing surprises), likely, high (if the known risks happen). Same unit for all pieces, for example ideal days.
3. **Write the assumptions** behind each piece: what exists already, who reviews and how fast, which interface is stable.
4. **Mark what widens the range:** an unknown interface, technology new to the team, waiting on another team, an unclear requirement. A piece with a very wide range is a candidate for an investigation first.
5. **Total the pieces** with the script (see Tools): sum of lows, sum of likely values, sum of highs, and a weighted mean; apply the team's correction factor if one exists.
6. **Name the two or three assumptions** that move the total most, and what would settle each.
7. **For a fixed date set from outside,** estimate conservatively, show the high total next to the time available, keep a buffer for what nobody can foresee, and list pieces that could move out; the owner chooses.
8. **Label and hand over:** «a range for planning; the owner sets any date».

## Rules

- **Ranges, never a lone number;** every piece has three values and at least one assumption.
- **No dates.** A range is effort; the owner sets dates and tells other teams.
- **Assumptions are visible** and updated when they change.
- **About the work, never the people.** Numbers are never used to judge anyone's speed.

## Checks before hand-over

- Every piece has low, likely, high and at least one assumption.
- The total is given as a range, with the script's output attached.
- The assumptions that move the total most are named.
- The label «a range for planning; the owner sets any date» is on the result.

## Artefacts

- `estimate/<goal>-range.md`: pieces with three values and assumptions, what widens each, the totals, the key assumptions.
- `estimate/<goal>-pieces.csv`: the input for the script.

## Hand-over

- **To the owner and the project manager:** the range, to turn into a date and a scope.
- **To the program manager:** assumptions that are risks for the program.
- **To `estimate-review`:** the estimate, to compare with actuals later.

## Tools

- `python3` 3.8 or newer, standard library only, no network. The script reads one CSV file; it runs no other program.
- Input: one row per piece, `piece,low,likely,high,assumption` (a header row and lines starting with «#» are skipped). Example row: «export endpoint,2,3,6,interface unchanged».
- `python3 scripts/range_total.py pieces.csv` prints each piece with its spread, the sum of lows, of likely values and of highs, a weighted mean ((low + 4 × likely + high) / 6 per piece, a common weighting), the three widest pieces and the label.
- `--factor 1.3` scales every number by the team's correction factor from `estimate-review`; `--unit` names the unit in the report; `-` reads the CSV from standard input.
- Exit 2 on bad input: a missing column, a value that is not a number, a negative value, or values not in the order low ≤ likely ≤ high.

## Sources

Built on 18F Guides, «Release strategies» and «Agile lexicon» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: estimate a forced large release very conservatively with a generous buffer, velocity for planning and not as a productivity measure. Built on the GOV.UK Service Manual, «Planning in agile» (Government Digital Service, Crown copyright), adapted: planning that is visible and revisited. Contains public sector information licensed under the Open Government Licence v3.0. The three-point estimate (low, likely, high) and its weighting are general methods, described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
