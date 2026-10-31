---
name: simplest-version
description: Write a one-page simplest version of a product or feature - the one-sentence promise (who it is for, the problem it removes, the result), the three things it must do to keep that promise, each with a «done when» line, what is left out and why with the signal that would bring each item in, and the riskiest assumption to test first. Use when a product or feature has grown unclear, before a first build, or when a team cannot agree what it is making.
---

# Simplest version

When a product tries to serve everyone, nobody can say what it is for. This skill writes the smallest version that still keeps its promise: one sentence about who it is for and what changes for them, three things it must do, and an honest list of what is left out. The page is short on purpose; the owner decides whether to build it.

**Route:** a product idea, a feature request or a crowded product from the product manager or a founder → **simplest-version** → the product manager decides → the MVP engineer or the developers build it.

## When to use

- Before a first version is built.
- When a feature list keeps growing and the team cannot say what the product is for.
- Not for planning a roadmap of releases, and not as a sales or marketing text.

## Inputs

- The idea or the product, and who it is for.
- The problem as the owner describes it, and any research or data about it.
- The list of features or requests on the table.

## Steps

1. **Write the problem first,** without a solution in it: who is affected, how often, how much, and what they do about it today.
2. **Write the one-sentence promise:** who it is for, the problem it removes, the result they get. No feature names, no technology.
3. **Choose the three things it must do** to keep that promise. Write each as «it's done when …», checkable by a person or a test.
4. **List what is left out,** each with the reason (not needed for the promise, serves another user group, can wait for evidence) and the signal that would bring it in (a number of requests, a measured drop-off, a regulation).
5. **Name the riskiest assumption** behind the promise, and the cheapest way to test it before or during the first build.
6. **Check the page:**
   - Could a person tell from the sentence whether it is for them?
   - Does each of the three map to the problem written in step 1?
   - Is anything in the three only there because a competitor has it?
   - Is anything left out that people who find the service hardest to use cannot do without?
7. **Hand the page over** and record the owner's decision on the promise, the three and the left-out list.

## Rules

- **Three, not more.** If a fourth item seems essential, one of the three is not, or the promise is too wide.
- **Every left-out item has a reason and a signal.** «Later» alone is not a reason.
- **Hypotheses are called hypotheses.** The page promises no result, date or number.
- **The owner decides.** This skill writes the page; it does not commit anyone to building it.

## Checks before hand-over

- The problem statement contains no solution.
- The promise names who, the problem and the result, and no feature.
- Exactly three must-do lines, each with «done when».
- Every left-out item has a reason and a signal.
- The riskiest assumption has a test.

## Artefacts

- `simplify/<product>/simplest-version.md`: problem, promise, the three, left out, riskiest assumption, decision.

## Hand-over

- **To the product manager:** the page, for a decision.
- **To the MVP engineer:** the approved page, as the input for the first build's scope.
- **To the ux researcher:** the riskiest assumption, when it needs evidence from users.

## Sources

Built on 18F Guides, product guide: problem statement, vision, minimum viable product (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted. Built on the GOV.UK Service Manual, «How the alpha phase works», and the Government Design Principles (Government Digital Service, Crown copyright), adapted: test the riskiest assumptions first, build only the hardest part, start small. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
