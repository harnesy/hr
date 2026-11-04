---
name: detail-critique
description: Review a set of screens in task order and write findings with exactly one problem and one concrete fix each - screen, element, what goes wrong for the person, the exact change (wording, order or control) and how to check it worked - ranked from «blocks the task» to «polish», with the evidence behind each. Use on a design, a prototype or a live flow before it is built, changed or released.
---

# Detail critique

A screen can look tidy and still make people stop: a heading that could belong to any page, a toggle whose state is unclear, an error that says something is wrong but not how to fix it. This skill walks the screens the way a person doing the task would, and turns each problem it meets into one finding with one fix. A finding without a fix is a complaint; a fix without the problem it solves is a taste. Neither goes in.

**Route:** screens or a link from the ui designer, the product manager or a team → **detail-critique** → ranked findings → the ui designer specifies the fixes, the product manager sets the order.

## When to use

- A design, prototype or live flow is about to be built, changed or released.
- People are slow, make mistakes or ask for help on a known step.
- Not as an accessibility audit or a heuristic evaluation (the UX auditor does those), and not for choosing between whole concepts.

## Inputs

- The screens in task order (links, screenshots or a prototype), including error, empty and confirmation states.
- The task people come to do, and who they are.
- Research notes, usage data or support questions, if they exist.

## Steps

1. **Form your own view first.** Walk the screens in task order and capture each one (screenshot or link) before reading the designer's notes or other reviews.
2. **Name the single job of each screen** in one line. A screen with two jobs is itself a finding (split it, or say why it should stay together).
3. **Check each screen against these questions:**
   - Is the heading specific to this screen?
   - Can someone doing this for the first time finish without help?
   - Are questions closed where they can be, with «I'm not sure» where that is a valid answer?
   - Is input accepted in the forms people really type (spaces, dashes, upper or lower case)?
   - Does each error message say how to put the problem right?
   - Can the person undo the action or edit what was entered?
   - Does it work with a keyboard only and with a screen reader?
   - Are the main points clear at a glance, and is the wording plain?
   - Does any help text only explain the interface? Then the interface is the problem.
4. **Compare across screens:** the same thing named or styled two ways, buttons in different places, different words for one action. List each and pick one.
5. **Write each finding** with exactly one problem and one fix:
   - **where** — screen and element;
   - **problem** — what goes wrong for the person, in their terms;
   - **fix** — the exact change: new wording, new order, a different control;
   - **check** — how to tell it worked (a person finishes the step unaided, an error stops appearing);
   - **evidence** — how many people or sessions showed it, or «expert review only».
6. **Rank** the findings: blocks the task, then causes errors, then slows people down, then polish.
7. **Compare** with the designer's notes and other reviews after your own list is done; add what you missed and note where you disagree, with the reason.

## Rules

- **One problem, one fix, per finding.** Split findings that carry two.
- **Concrete fixes only.** «Make it clearer» is not a fix; «rename the button "Continue to payment"» is.
- **About the screen, never about the designer.** Hard verdicts name the screen, the element and the change.
- **Evidence is stated.** Expert review is allowed and labelled as such.
- **Propose, never edit.** The ui designer owns the spec; this skill does not change it.

## Checks before hand-over

- Every screen in the task, including error and empty states, was walked.
- Every finding has where, problem, fix, check and evidence.
- The list is ranked, and accessibility findings are marked for the UX auditor.
- Inconsistencies across screens are listed with the one form to keep.

## Artefacts

- `simplify/<flow>/critique.md`: screens in order with their job, the ranked findings, the inconsistency list.
- The captured screens, numbered as in the findings.

## Hand-over

- **To the ui designer:** the findings, to turn accepted fixes into specs.
- **To the product manager:** the ranking, to set the order of work.
- **To the UX auditor:** findings about keyboard, screen reader, contrast or plain wording.

## Sources

Built on the GOV.UK Service Manual, «Structuring forms», «Designing good questions» and «Make the service simple to use» (Government Digital Service, Crown copyright), adapted: one thing per page, closed questions, «I'm not sure», tolerant input, error messages that say how to fix the problem, help text as a sign of a design fault. Contains public sector information licensed under the Open Government Licence v3.0. Built on the U.S. Web Design System design principles (GSA Technology Transformation Services; CC0 1.0), adapted: keyboard and screen reader use, main points at a glance, undo and edit, plain language. Built on 18F Guides, code review and product guide (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
