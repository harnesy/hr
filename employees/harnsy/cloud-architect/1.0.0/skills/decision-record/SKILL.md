---
name: decision-record
description: Write down an architectural decision the owner has made, with its context, the options considered, the decision and why, its good and bad consequences, status, owner and a review date, so later readers know what was decided and when to look again. Use after design-it-twice, when an important technical choice is made in a meeting, or when an old decision is replaced.
---

# Decision record

A decision record is a short page that explains one decision to someone who arrives a year later. It says what problem was faced, which options were on the table, what was chosen and why, and what that costs. This skill writes the record; it does not make the decision.

**Route:** an options paper or a meeting outcome → the owner decides → **decision-record** → shared with everyone affected → reviewed on its date or when the context changes.
Before this skill: a decision taken by the person who owns it. After it: a numbered record in the decision log.

## When to use

- A decision changes the structure of a system, one of its qualities (security, reliability, cost, speed of change) or its behaviour in a way other teams will notice.
- After design-it-twice, once the owner has chosen.
- When a decision made earlier is replaced or withdrawn.
- Not for a running register of many decisions across topics: that is `decision-log`. This skill writes one full record, which a log entry can link to.

## Inputs

- The problem and its context; the options paper, if one exists.
- The owner's decision, in the owner's words, and the reason given.
- Who was consulted and who must be told.
- The existing decision log, to number the record and link related ones.

## Rules

- Records the owner's decision; never makes it. Until the owner confirms, the status is «proposed».
- At least two options are listed, even if one is «keep things as they are».
- Consequences include the bad ones: new costs, new risks, technical debt, things that become harder.
- Accepted records are not rewritten. A change of mind is a new record that marks the old one «superseded by <number>».
- Plain words; one decision per record.

## Steps

1. **Check it is worth a record:** does it change structure, a quality or behaviour that others rely on? If not, a note in the team's normal place is enough.
2. **Set the level and the decider:** team, programme or organisation. Escalate when the decision touches a shared platform, sets a precedent for other teams, or adds notable cost or technical debt.
3. **Write the context** in a few sentences, ending with the problem as a question.
4. **List the decision drivers:** the qualities and constraints that matter most.
5. **List the options,** each with its good, neutral and bad points. Reuse the options paper if there is one.
6. **Record the decision:** the chosen option and «because …», linked to a driver. Use the owner's reasoning, not a new one.
7. **Write the consequences:** what gets better, what gets worse, what follow-up work is now needed.
8. **Say how it will be confirmed:** a review, a test, a check in the build that shows the system follows the decision.
9. **Fill in the metadata:** number, title, date, status (proposed, accepted, rejected, deprecated, superseded by …), owner, consulted, informed, links to related records and tickets.
10. **Set a review date** and the triggers that bring it forward (a new requirement, a price or licence change, a failed assumption).
11. **Share it** with everyone listed as informed and store it in the decision log.

## Checks before hand-over

- Context, drivers, at least two options, decision with reason, consequences good and bad.
- Status, owner, date, review date and consulted/informed are filled in.
- The decision and reason are the owner's, confirmed by the owner.
- A replaced record links to its successor and the other way round.

## Artefacts

- `decisions/NNNN-<short-title>.md`: one record per decision.
- `decisions/index.md`: number, title, status, date, owner.

## Hand-over

- **To the owner:** the draft for confirmation before the status becomes «accepted».
- **To the software architect or cloud architect:** the record for the architecture log.
- **To the teams informed** (developers, devops, SRE, database engineer, security reviewer as relevant): what changes for them.
- **To the product manager:** consequences that affect scope, cost or timing.

## Sources

Built on GOV.UK «Architectural Decision Record Framework» (DSIT and GDS, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on MADR, the Markdown Architectural Decision Records template (github.com/adr/madr, commit ba75bb1; © 2017-2022 Oliver Kopp, Olaf Zimmermann and contributors, MIT licence), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
