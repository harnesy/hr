---
name: design-it-twice
description: Before committing to a design, sketch two or three genuinely different options, compare them on the same criteria (fit to the need, trade-offs, total cost, risk, how easy to change later) and give a recommendation the owner can accept or reject; the result feeds a decision record. Use for any choice that is expensive to reverse, such as a platform, a data store, a service boundary, a hosting model or a major library.
---

# Design it twice

The first design that comes to mind is rarely the best one, and a single option cannot be judged. This skill puts two or three really different options side by side, measured against the same criteria, so the owner chooses with the trade-offs in view. It recommends; the owner decides.

**Route:** a need or a problem → **design-it-twice** → options with a recommendation → the owner decides → **decision-record**.
Before this skill: the problem, its constraints and who decides. After it: an options paper; the decision itself is written down with the decision-record skill.

## When to use

- A choice that would be costly or slow to undo: hosting model, data store, messaging, service boundaries, identity, a major framework.
- When a team is about to build the first idea without having looked at another.
- When two people argue for different designs and nobody has written either down.

## Inputs

- The problem as a question, and what success looks like.
- Decision drivers: the qualities that matter (reliability, security, speed of change, cost, skills in the team, data location), and hard constraints.
- What exists today, and why earlier choices were made.
- Who decides, and at what level (team, programme, organisation).

## Rules

- Two or three options, and they must differ in kind, not only in settings. «Do nothing» or «keep the current system» counts as an option when it is real.
- Every option is judged on the same criteria and with the same depth.
- Each option shows trade-offs, cost (total cost of ownership, not just list price), risk, and how hard it would be to change course later.
- No price figures without a cost estimate behind them; no promised uptime, speed or saving.
- The recommendation names the driver that tips it. The owner makes the decision.
- No vendor or product is favoured by default; a product appears only as part of an option with its reasons.

## Steps

1. **Frame the problem** as one question and list the decision drivers in order of weight. Agree them with the owner before designing.
2. **Learn the landscape:** what runs now, what it costs to run, which teams depend on it, and why it was built that way. Read existing decision records.
3. **Sketch the options.** Make them really different: for example managed service versus self-run, one shared component versus one per team, buy versus build, event-driven versus request-driven. Write a short description and a simple diagram of each.
4. **Compare on the same criteria,** in one table:
   - fit to each decision driver (good, neutral or bad, with a reason);
   - total cost of ownership: usage or licence cost, the work to run it (patching, monitoring, scaling, upgrades) and indirect costs (outages, data loss, lock-in), using the cost-estimate skill for figures;
   - risks and how each would be reduced;
   - reversibility: what it would take to change course in a year;
   - skills and effort needed to build and run it.
5. **Test the riskiest assumption** when it matters: a small prototype, a spike or a quick measurement, and record what it showed.
6. **Watch the boundaries:** lines between components drawn too early are easy to get wrong; prefer options that keep a later change possible.
7. **Recommend** one option, saying which driver decides it and what would change the recommendation.
8. **Hand it to the owner** for decision. Escalate when the choice affects a shared platform, sets a precedent, or adds notable cost or technical debt.

## Checks before hand-over

- Two or three options that differ in kind, each on the same criteria.
- Each option has trade-offs, cost, risk and reversibility.
- Cost figures, if any, come from a dated cost estimate.
- The recommendation is tied to a named driver and the owner is named as decider.
- Assumptions and prototype results are written down.

## Artefacts

- `design/<topic>-options.md`: problem, drivers, options, comparison table, prototype notes, recommendation.
- Diagrams next to it, one per option.

## Hand-over

- **To the owner:** the options paper for decision.
- **To the cloud architect or software architect** (whichever does not hold this skill here): a review of the options.
- **To the security reviewer and the database engineer:** options that change data, access or storage.
- **To the decision-record skill:** the chosen option, once the owner decides.
- **To the product manager:** effects on scope or timing.

## Sources

Built on MADR, the Markdown Architectural Decision Records template (github.com/adr/madr, commit ba75bb1; © 2017-2022 Oliver Kopp, Olaf Zimmermann and contributors, MIT licence), adapted. Built on GOV.UK Service Manual «Choosing technology: an introduction» (Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on the Google Cloud Well-Architected Framework, cost optimization pillar and «Align cloud spending with business value» (Google LLC, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

The practice of comparing several designs before choosing is widely known as «design it twice» (John Ousterhout); described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
