---
name: source-match
description: Check each listed claim against its original source and give one of four verdicts only - matches, differs (how), no source found, source unreachable - each with the source, the source's own date, the date read and the exact passage; note context that changes the meaning and whether a correctly copied figure fits the point it is used for; depth proportionate to the stakes; never rewrites a claim, never invents a source, never searches to make a claim come out right. Use after claim-extract.
---

# Source match

A claim is only as good as the source behind it, and a source is only useful if someone can go back to it. This skill takes each listed claim to its original source, quotes the passage, and gives a plain verdict with dates, so the author can fix the text and anyone can repeat the check.

**Route:** `claim-extract` → **source-match** (every search kept in `source-log`) → the author or the editor.

## When to use

- After the claims are listed, for every checkable claim in scope.
- When a single figure is questioned and needs its source traced.
- Not for rewriting the text, and not for finding support for a claim chosen in advance.

## Inputs

- The claims list.
- The sources the text cites, and search access.
- The stakes: which claims carry the main point or drive a decision.

## Steps

1. **Form the verdict from the source first,** before reading any justification the author gave.
2. **Go to the cited source.** If none is cited, look for the original publisher of that kind of figure; log every search in `source-log`.
3. **Prefer the original.** A secondary source that quotes the figure goes in the log as the route; the verdict rests on the original when it is reachable.
4. **Copy the exact passage** that supports or contradicts the claim, with the page, table or section.
5. **Give one verdict:** matches; differs (say how: number, date, unit, group counted, rounding, a forecast stated as a result); no source found (with the searches); source unreachable (paywall, login, broken link, with the date tried).
6. **Record three things with each verdict:** the source's address, the source's own date (or «undated»), and the date read.
7. **Note context** in the source that changes the meaning (definitions, caveats, ranges, what the figure does not cover), and whether the figure could be misread on its own.
8. **Note fitness for the point:** a figure that matches can still be the wrong year, the wrong group or a rate read as a count.
9. **State the depth** of each check, deeper for main-point claims, and list claims not checked and why.

## Rules

- **Four verdict words only:** matches, differs, no source found, source unreachable.
- **About claims, never people.** No word about the author's honesty or motives.
- **No invented or guessed sources.** A claim that cannot be traced is «no source found».
- **No hunting.** Never search for a source in order to make a claim come out right.
- **No rewriting.** A suggested fix, if offered, is labelled as a suggestion for the author.
- **Repeatable.** The log lets another person reach the same verdict.

## Checks before hand-over

- Every verdict has the source address, the source's own date, the date read and the passage.
- Every «no source found» has its searches in the log.
- Main-point claims had the deepest check, and the depth is stated.
- Claims not checked are listed with the reason.

## Artefacts

- `factcheck/<text>/verdicts.md`: claim, verdict, passage, source and dates, context note, fit for the point, depth; claims not checked; plus the source log.

## Hand-over

- **To the author or the editor:** the verdicts and the log; the author decides how to fix the text.
- **To the data analyst:** claims that need a recalculation from raw data.
- **To a lawyer:** questions about whether something may be said at all.

## Sources

Built on the Code of Practice for Statistics, «Standards for the Public Use of Statistics, Data and Wider Analysis» (Office for Statistics Regulation, UK Statistics Authority, Crown copyright), adapted: a public figure's source available to everyone and cited next to it, limitations and context that change the meaning, whether a figure could be misread out of context. Adapted from data from the UK Statistics Authority licenced under the Open Government Licence v.3.0. Built on The AQuA Book, 2025 edition (Government Analysis Function, Crown copyright), adapted: effort proportionate to the risk of the use, repeatable results, uncertainty stated rather than hidden, a statement of what was checked and what was not. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
