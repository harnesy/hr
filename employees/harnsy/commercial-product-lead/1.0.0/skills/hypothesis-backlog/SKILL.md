---
name: hypothesis-backlog
description: Keep one ranked list of hypotheses about getting new paying clients - a card per hypothesis (problem, and with very few visits which of two lines it serves, evidence marked fact or assumption and graded, one change, the reason buyers would act differently, expected result, the test with a verdict rule of pass, fail or undetermined set before release, what implementing it would need, harm check), ranking criteria agreed with the owner before ranking, one hypothesis live at a time, and a route for small traffic without a split test (before and after, each request followed to payment, buyer conversations). Use once the problem statement is agreed.
---

# Hypothesis backlog

One ranked list of hypotheses about getting new paying clients, one live at a time. Each card names one change, the reason buyers would act differently because of it, the effect we expect, and how the result will be judged, with the rule written before the change goes live. Nothing on the card is built here; the card lists what building it would need.

**Route:** the agreed page from `commercial-problem` + proposals accepted in `proposal-review` → **hypothesis-backlog** → the owner picks → the right roles build and measure.

## When to use

- Once the problem page is agreed and there are ideas to test.
- When a list of ideas has no order, or everything in it is marked top priority.
- When the verdict on a live change is due.

## The card

- **Problem:** the line of the problem page it addresses, with the audience and market. When visits are close to none, also which of the two lines it belongs to: selling to the buyers who reach the site, or bringing buyers to it at all.
- **Evidence:** the facts and guesses behind the idea, each item marked fact (source, date) or assumption and given a grade (below).
- **Change:** one change, described in words; nothing is built at this stage.
- **Why it should work:** in the shape «changing <what> for <which buyer> should lead to <benefit>, because <belief>».
- **Expected result:** what we expect to see and in which direction; an expectation, never a promise.
- **Test:** the measure, its starting value, the window or date, and the verdict rule set before release: pass, fail or undetermined.
- **What it would take:** a list (copy, page, form, tracking, sales script, data) with the role that would do each part.
- **Harm check:** who could this hurt, and how.
- **Ranking:** expected effect on sales, confidence, cost.

## Evidence grades

Strongest first:

1. What buyers did: orders, payments, requests followed to payment.
2. What buyers told us in conversations.
3. Published data, with its source and date.
4. A rival's practice: it shows that a pattern exists, not that its wording works.
5. The team's own view, the owner's included.
6. Simulated buyers (an AI playing a buyer): useful for drafting questions, never a stand-in for buyers.

## Steps

1. **Write the cards** from the problem page and the accepted proposals; one change per card. When visits are close to none, keep the two lines apart: a change to the site does not answer whether buyers arrive, and channel work on that line goes to the marketing strategist.
2. **Agree the ranking criteria before ranking.** Each person proposes criteria alone first; the owner picks, usually expected effect on paying clients and cost, with confidence as a third. Every criterion traces back to the goal.
3. **Rank.** Place each card on the criteria. Note dependencies, timing and capacity that change the order. The far end of the list is less certain and is reviewed later, not polished now.
4. **Doubtful beliefs first.** Among close cards, prefer the one that tests the belief most likely to be wrong with the least work.
5. **One live at a time.** The owner picks one card; the others wait. Two changes running together make neither readable.
6. **Choose the validation route.**
   - Enough visitors for a split test: hand sizing, length and stopping rule to the conversion optimization specialist.
   - Few visitors: no split test. A before-and-after comparison over a window fixed in advance, outcomes written down before release, each request followed through the pipeline to payment (the revenue operations specialist's data, read-only), and short conversations with buyers to learn why. Expect some drift anyway; say that this route cannot prove cause.
7. **Verdict on the date.** Apply the rule as written: pass, fail or undetermined. An unclear result sends you back to the card, not to a new rule.
8. **Update the list** with what was learned and hand the next pick to the owner.

## Rules

- The verdict rule is written before release and never changed afterwards; «undetermined» is an honest result, not a failure to hide.
- No numeric threshold is stated as a general fact; each rule is the owner's choice for this card.
- Early steps (sign-ups, demo views, pilot requests, clicks) never decide a verdict on their own.
- Numbers are split by audience, market and source, and set against the starting point.
- A card whose evidence sits only in the two weakest grades is ranked low on confidence.
- You build nothing and set up no tracking or test; the card lists what others would do once the owner says yes.

## Checks before hand-over

- Every card has all fields; evidence is marked fact or assumption and graded.
- When visits are close to none, every card names its line.
- The ranking criteria are written at the top, with the owner's agreement and date.
- Exactly one card is marked live, and its verdict rule and date were written before release.
- Small-traffic cards use the before-and-after route and say what it cannot prove.
- No card promises a sales figure.

## Artefacts

- `commercial/hypotheses-<date>.md`: the criteria, the ranked cards (with evidence grades and, when visits are close to none, their line), the live card, the verdicts with their dates, and what was learned.

## Hand-over

- **To the owner:** the ranked list and the pick to make.
- **To the product owner:** the chosen card's «what it would take», for tickets.
- **To the conversion optimization specialist:** test sizing and the stopping rule when traffic allows a split test.
- **To the marketing strategist:** cards on bringing buyers to the site, for their plan.
- **To the product analyst:** the measure, its definition and the starting value to read.
- **To the pre-mortem facilitator, through the owner:** a chosen card with a large expected effect, before it goes live.

## Sources

Built on the GOV.UK Service Manual, «How to set performance metrics for your service», «Measuring the success of your service», «Measuring the benefits of your service» and «How the alpha phase works» (GDS, Crown copyright), adapted: a hypothesis as a change, the benefit it should bring and the belief behind it, measures that follow from the hypothesis, a starting point, numbers split by segment and set against time, testing the most doubtful belief first with the least work. Built on «Evaluating digital health products»: «A/B testing» and «Before-and-after study» (OHID, Crown copyright), adapted: split tests need many users and their length follows from visitors and the expected change; a before-and-after comparison suits small samples, needs outcomes fixed in advance and cannot prove cause. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Methods, «Success metrics», «Design hypothesis» and «Multivariate testing» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: outcomes before measures, who collects them and how often, a benchmark, what is optimised for named in advance, a harm check; the template sentence and named tools are not used. Built on «Prioritise customer opportunities», Digital Service Toolkit (© State of New South Wales; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: criteria agreed before ranking and tied to the goal, proposed alone first, dependencies and capacity that change the order, the far end of the list less certain. © State of New South Wales. For current information go to www.nsw.gov.au. Built on «Market research and competitive analysis», U.S. Small Business Administration (Source: U.S. Small Business Administration, www.sba.gov), adapted: competitors read per segment, including indirect ones.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
