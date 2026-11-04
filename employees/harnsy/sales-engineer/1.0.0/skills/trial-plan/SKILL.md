---
name: trial-plan
description: Plan a product trial or proof of concept that settles one buyer doubt: a one-sentence purpose, a few written success criteria with targets, measures and check dates agreed by both sides, scope in and out, the buyer's own environment connected first, a midpoint check and a readout for the buyer's go or no-go. Use when a buyer needs hands-on proof and has a decision process and a date.
---

# Trial plan

A trial is a structured test, not free access. It is worth running only when a demo cannot settle the buyer's doubt and the buyer has a way to decide. This skill writes the plan both sides sign up to, keeps it steady while it runs, and ends it with a readout against each criterion.

**Route:** demo follow-up or discovery notes from the account executive → **trial-plan** → kickoff → midpoint check → readout → the buyer decides → after signing, open risks to the customer success manager.

## When to use

- The buyer needs hands-on proof in their own environment, and a demo or workshop would not settle it.
- The buyer has a decision process, a decision maker and a date.
- Not when the buyer only wants to «have a look» (offer a demo with `demo-plan`), and not without a date for the decision.

## Inputs

- The buyer's problem and doubt, from discovery and the demo follow-up.
- Who decides at the buyer, and by when.
- The buyer's environment: what has to be connected, who on their side does it.
- The account executive's limits for the trial (length, who supports it).

## Steps

1. **One sentence of purpose:** what the trial will prove, about which problem.
2. **Draft the criteria.** Few, each naming a problem solved rather than a feature present. Group them (does it work, is it fast enough, does it connect, can the team use it). For each: a target, how it is measured, who measures it, and the date it is checked. Rewrite vague or unmeasurable criteria; drop the ones nobody will decide on.
3. **Draw the scope.** What is in, what is out, and what waits for later. Name who on each side does what.
4. **Agree it.** Both sides agree the criteria and the scope in writing at a kickoff; the agreement and its date go into the plan.
5. **Connect first.** The first step is the buyer connecting their own environment. Nothing else starts until real data flows on their side. The sales engineer never asks for credentials, passwords or data exports, and reads only what the buyer chooses to share.
6. **Watch engagement.** Questions, use, meetings attended. If it fades, ask the buyer directly whether the trial is still a priority.
7. **Midpoint check.** Status per criterion, blockers, what changes are needed. A change to criteria or scope needs both sides' written agreement and goes into the change record.
8. **Extensions.** Only for a stated reason, and in exchange for a concrete step from the buyer (a meeting with the decision maker, a date for the decision).
9. **Readout.** Each criterion: met, partly met or not met, with the evidence. The buyer decides go or no-go.

## Rules

- **Criteria first.** No trial starts without written, agreed criteria.
- **No moving goalposts.** Criteria do not change mid-trial without both sides agreeing in writing.
- **Buyer's environment, buyer's data.** The agent touches nothing it was not given and changes nothing in the buyer's systems; any change it suggests is a proposal with the current state, the change, the expected effect and the undo.
- **No promises.** A missing feature is «not supported today»; plans and dates go to the account executive.

## Checks before hand-over

- Each criterion has a target, a measure, an owner and a check date.
- The plan records the agreement of both sides with a date.
- The change record lists every change with both sides' agreement.
- The readout gives evidence for every criterion.

## Artefacts

- `deals/<buyer>/trial-plan.md`: purpose, criteria, scope, roles, dates, agreement.
- `deals/<buyer>/trial-log.md`: engagement notes, midpoint check, change record.
- `deals/<buyer>/trial-readout.md`: result per criterion with evidence.

## Hand-over

- **To the account executive:** the plan for agreement and the readout for the buyer's decision.
- **To the customer success manager, after signing:** the issues log, open technical risks and the agreed criteria, which become the starting point of `customer-onboarding-plan`.
- **To the product owner:** gaps found during the trial, with the buyer's use case.

## Sources

Built on the PostHog handbook, /contents/ folder, pages on running trials and trials (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted. Built on the sales-engineer skill references, POC practices, in github.com/alirezarezvani/claude-skills (MIT, © 2025 Alireza Rezvani), adapted; the goal acronym left out. Built on the Sales Engineer agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors), adapted. Built on the Sourcegraph handbook (archived), technical win process and implementation handoff pages (Apache License 2.0; Sourcegraph, Inc. and contributors). Changed by harnsy.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
