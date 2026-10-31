---
name: demo-plan
description: Plan a product demo around the problems the buyer named, in the buyer's words, on a stand filled with invented sample data; outcome first, setup second, a deeper path for technical attendees and a written follow-up. Use when a prospect or customer asks for a demo or a walkthrough. Never uses real customer or production data.
---

# Demo plan

A demo is a short story about the buyer's own problem: what hurts today, what it looks like solved, and how it gets solved. This skill plans that story, prepares a demo stand with invented data, and lists what the buyer receives in writing afterwards. The account executive owns the meeting and the deal.

**Route:** discovery notes from the account executive → **demo-plan** → the demo, run with the account executive → written follow-up → `trial-plan` if the buyer needs hands-on proof.

## When to use

- A prospect asks to see the product after a discovery call.
- An existing customer asks for a walkthrough of an area they do not use yet.
- Not for a trial in the buyer's own environment (that is `trial-plan`) and not for written questionnaires (`technical-questionnaire`).

## Inputs

Ask the account executive; do not plan without these:

- **Discovery notes:** the problems the buyer named, in their words, and what happens today without a fix.
- **Attendees:** names, roles and what each one cares about (people who build and integrate, people who pay, people who use it daily).
- **Time available** and whether the meeting is remote or in person.
- **Product facts:** which features exist today, from published documents. Nothing that is planned or unreleased goes into a demo.

## Steps

1. **Write the problems down.** Two or three, in the buyer's own words, each with the cost or pain they described. If discovery did not produce them, stop and ask the account executive for another call; a demo without a problem turns into a tour.
2. **Pick what to show.** For each problem, one outcome screen (what it looks like solved) and the shortest path to it. Leave out anything that answers no stated problem, however good it is.
3. **Order it.** Open by restating the problems and asking whether they are still right. Then, for each problem: the outcome first, then how it is set up. Close with what the buyer will receive in writing.
4. **Plan two depths.** A main path for everyone, and a deeper path (architecture, integration, data flow, security) for the moment a technical attendee asks how it works underneath. Note who is likely to ask what.
5. **Build the stand.** An invented company, invented people and invented numbers, shaped like the buyer's business (same kind of orders, tickets, users or devices), labelled «sample data» on screen. No customer, prospect or production data, not even a «quick export». Reset the stand after each demo.
6. **Prepare for hard questions.** For each likely objection, the honest answer from the documents, including «not supported today» with what exists instead. Questions about plans, dates or prices go to the account executive.
7. **For an existing customer:** agree topics in advance, ask about their goals before showing anything, let them drive on their own screen where possible, and read back what you heard before the call ends so they can correct it.
8. **Write the follow-up.** One line per problem: what was shown, what the buyer said, open questions with an owner and a date, and any documents promised.

## Rules

- **Invented data only** on the stand, labelled as sample data.
- **No promises.** No feature that does not exist today, no delivery date, no price or discount. Plans and money are the account executive's.
- **Fair comparisons.** Compare with other products only on facts the buyer can check; never run another product down.
- **The buyer's words.** Use the terms the buyer used, not internal names.

## Checks before hand-over

- Every planned screen maps to a named problem.
- The stand holds only invented data and shows the «sample data» label.
- Every answer prepared for an objection names its source document.
- Nothing in the plan or the follow-up mentions a future feature, date, price or discount.
- The follow-up lists each open question with an owner and a date.

## Artefacts

- `deals/<buyer>/demo-plan.md`: problems, screens in order, the deeper path, prepared answers, attendees.
- `deals/<buyer>/demo-stand.md`: what the invented data set contains and how to reset it.
- `deals/<buyer>/demo-follow-up.md`: the written follow-up, as a draft.

## Hand-over

- **To the account executive:** the plan before the meeting and the follow-up draft after it; the account executive sends it.
- **To `trial-plan`:** when the buyer asks for hands-on proof, the problems and open questions from the follow-up.
- **To the product owner, through the account executive:** gaps the buyer raised, with the buyer's use case.

## Sources

Built on the Sales Engineer agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors), adapted; third-party named methods left out. Built on the PostHog handbook, /contents/ folder, pages on sandboxes and reverse demo calls (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted. Built on the Sourcegraph handbook (archived), technical win process page (Apache License 2.0; Sourcegraph, Inc. and contributors). Changed by harnsy. Scope from the O*NET 31.0 Database, 41-9031.00 Sales Engineers. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
