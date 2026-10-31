---
name: decision-note
description: Write one page for the person who decides a disagreement - the question, both positions as confirmed by each side, the criteria both accept, the options with their scores, who decides and by when, and empty fields for the decider's decision, reason and review date; architectural decisions are handed to the software or cloud architect for their own record. Never fills in the decision. Use at the end of a mediation, after the criteria table.
---

# Decision note

A decider should not have to read a long thread to understand a disagreement. This skill puts everything on one page: the question, both sides' confirmed cases, what both agree matters, how each option scores, and who decides by when. The decision itself is left for the decider to write, with the reason and a date to look at it again.

**Route:** `position-summary` + `decision-criteria` → **decision-note** → the decider → the team's own decision log.

## When to use

- At the end of a mediation, once both summaries are confirmed and the criteria table is ready.
- When a decider asks for a short page to decide from.
- Not for recording decisions nobody disagreed about, and not for a team's running list of decisions (that stays in the team's own log).

## Inputs

- The confirmed position summaries and shared facts.
- The criteria table with both sides' weights and the option scores.
- The decider and the date.

## Steps

1. **Write the question** in one sentence that both sides accept.
2. **Add both positions** in a few lines each, as confirmed by each side, with a link to the full summaries.
3. **Add the shared facts and the criteria** both accept, with each side's weights.
4. **Add the options** with their scores and the evidence links; «keep things as they are» included.
5. **Name who decides** and the limits of that authority, who was consulted, and the date the decision is needed.
6. **Leave the decision fields empty** for the decider: the decision, the reason, what would make it worth revisiting, a review date.
7. **Keep it to one page;** detail stays in the linked files.
8. **After the decider fills it in,** propose where it is filed: architectural decisions to the software or cloud architect for their own record, others to the team's own decision log, and both sides informed.

## Rules

- **One page.** If it does not fit, the question is too broad: split it.
- **Confirmed words only.** Each position is the version its side confirmed.
- **The decider writes the decision.** The mediator never fills in the decision or the reason.
- **Nothing sent by the agent.** The decider or the requester shares the note.
- **About the work.** No judgement of either side.

## Checks before hand-over

- The question is one sentence both sides accept.
- Both positions match their confirmed summaries.
- Every option has its scores and evidence.
- The decider, the limits of authority and the date are named.
- The decision fields are empty.

## Artefacts

- `mediation/<topic>/decision-note.md`: question, positions, shared facts, criteria and weights, scored options, decider and date, empty decision fields, links.

## Hand-over

- **To the decider:** the note.
- **After the decision:** architectural decisions to the software architect or cloud architect; others to the decider and the team's own decision log; both sides informed by the decider.

## Sources

Built on the Architectural Decision Record Framework (Department for Science, Innovation and Technology and GDS, Crown copyright), adapted: a record with title, date, status, context, the decision, its consequences, who was consulted and links; shared with everyone affected; reviewed when the context changes. Built on «A guide to civil mediation» (Ministry of Justice, Crown copyright), adapted: the mediator does not decide and gives no advice on who is right. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
