---
name: chart-report
description: Turn analysis results into charts and a short report people can read correctly: the right chart for the relationship, a title that states the message, uncertainty shown, source, date and notes with every chart, and a text alternative. Use when results go to a decision owner, into a dashboard, or into a document.
---

# Chart report

A chart should make one point quickly and honestly. This skill picks the chart by what the data shows, writes the message in the title, shows how uncertain the numbers are, and attaches what a reader needs to check them.

**Route:** analysis results (analysis-notebook, funnel-analysis, experiment-readout) → **chart-report** → the reader (decision owner, dashboard, document).
Before this skill: numbers with their queries and dates. After it: a report or charts the reader can act on.

## When to use

- Results go to a person who will decide something.
- Charts are built for a dashboard (with `dashboard-spec`).
- A chart someone made looks misleading and needs fixing.

## Inputs

- The numbers, their queries or code, and the date they were produced.
- The message: the one thing the reader should take away.
- The reader: how much they know and where they will see the chart (screen, phone, printed page).

## Rules

- Every chart carries its source, the date of the data and notes on definitions or gaps.
- Uncertainty is shown when the numbers come from a sample or a model (intervals, ranges).
- A correlation is described as an association, not as a cause.
- Colour is never the only way to tell series apart; text has enough contrast; every chart has a text alternative.
- Aggregates only: no chart identifies a person; very small groups are suppressed or merged.

## Steps

1. **Write the message** in one sentence. If there is no message, a table may be better than a chart.
2. **Pick the chart by the relationship:**
   - change over time → line (or columns for a few periods);
   - comparison between categories → bars, sorted, starting at zero;
   - parts of a whole → stacked bar with few parts, or a simple table;
   - distribution → histogram or box plot;
   - relationship between two measures → scatter;
   - effect with uncertainty → point with interval.
3. **Build it plainly:** label lines directly instead of a legend where possible; light or no gridlines; bars never on a cut axis; a limited number of lines, stacks or groups; units on axes.
4. **Title and text:** the title states the message («Sign-ups rose 12% after the new form»), a subtitle says what is measured, where and when; notes give definitions, exclusions and caveats; the source line names the data and date.
5. **Show uncertainty** where it exists and say in words what it means for the message.
6. **Write a text alternative** that gives the message and the key numbers.
7. **Check with a reader:** show it to someone who has not seen the analysis and ask what they take from it; fix what they misread.
8. **Assemble the report:** a short summary in plain words, then the charts, then method and limits, with the downloadable data or the query.

## Checks before hand-over

- Each chart has a message title, source, date, notes and a text alternative.
- Chart type matches the relationship; bar axes start at zero.
- Uncertainty is shown where the numbers are estimates.
- No causal wording for associations; no identifiable small groups.
- Colours are not the only cue; contrast is sufficient.

## Artefacts

- `report/<name>-<date>.md` (or the format the reader uses) with charts and their source data or queries.

## Hand-over

- **To the decision owner** (product manager, marketing lead, owner): the report.
- **To the BI dashboard developer:** charts meant for a dashboard.
- **To the analyst who produced the numbers:** questions readers raised.

## Sources

Built on «Data visualisation: charts» by the Government Analysis Function (https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/; source acknowledged; Crown copyright; the page's images are not reused). Contains public sector information licensed under the Open Government Licence v3.0. Built on the Office of Evaluation Sciences (U.S. General Services Administration) paper «Reporting statistical results in text and in graphs» (https://oes.gsa.gov/methods/; US government work), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
