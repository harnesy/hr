---
name: problem-statement
description: Write a problem statement before work is planned - who has the problem in their own words, the need and why, how success will be measured, what is out of scope, acceptance examples («it's done when …») and links to open assumptions - checked to be about a problem rather than a feature, based on evidence and small enough for one piece of work. Use after questioning a request, before a spec or a plan is written.
---

# Problem statement

A good problem statement lets a team agree what they are solving before they argue about how. It names who has the problem, what they need and why, how everyone will know it is solved, and what is deliberately left out. It describes a problem, never a screen or a feature.

**Route:** `question-ladder` record + `assumption-log` → **problem-statement** → the business analyst writes the spec; the product manager decides.

## When to use

- After a request has been questioned and before it is planned.
- When a team keeps debating solutions and nobody can say what problem they solve.
- Not for writing the full specification (the business analyst's job) or for recording a decision once made (use a decision record).

## Inputs

- The question record and the assumption log.
- Any evidence: research notes, data, support tickets, the users' own words.

## Steps

1. **Who.** The user type in the words users would use about themselves, not the team's internal labels.
2. **Need and why.** One sentence in the shape «I need … so that …». The «so that» part is the goal and matters most. It describes the problem («a reminder before a payment is due»), not a solution («an email»).
3. **Evidence.** Where the need comes from. If the only source is an opinion, link the assumption ID instead of presenting it as fact.
4. **Measure.** How we will know the problem is solved: a signal or a number that can be observed (if a metric needs a precise definition, write it with a metric definition and link it).
5. **Out of scope.** What this work will not do, written down so it is not assumed.
6. **Acceptance examples.** A list of «it's done when …» lines, each one checkable by someone outside the team.
7. **Open assumptions.** The IDs from the assumption log this statement depends on.
8. **Size.** If the statement covers several needs, split it into several statements.
9. **Read it back** to the person who asked; change it only with their agreement, and record what changed.

## Rules

- **Problem, not feature.**
- **Users' words, not the team's.**
- **Evidence or a marked assumption** behind every claim.
- **The requester and the product manager own the statement;** the analyst drafts it.

## Checks before hand-over

- It sounds like something a real user would say.
- The need has a «so that».
- The measure can be observed by someone else.
- Out of scope is not empty.
- Each acceptance example is checkable.
- Every unproven claim links to an assumption ID.

## Artefacts

- `requirements/<request>/problem.md`: who, need and why, evidence, measure, out of scope, acceptance examples, open assumptions, change history.

## Hand-over

- **To the business analyst:** the statement, as the starting point for the specification.
- **To the product manager:** the statement and its open assumptions, for the decision on scope and priority.

## Sources

Built on the GOV.UK Service Manual, «Learning about users and their needs» and «Writing user stories» (Government Digital Service, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Methods, «Stakeholder and user interviews» (18F, U.S. General Services Administration; CC0 1.0), adapted. Built on «Algorithms» (1st edition, 2019) by Jeff Erickson, section on specifying the problem (CC BY 4.0; algorithms.wtf), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
