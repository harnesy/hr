---
name: work-breakdown
description: Break a goal, spec or ticket list into pieces of at most a few days that cover all the work once - deliverables first, then pieces, the usually forgotten work added (tests, review, migration, release, documentation, coordination), every unknown turned into a time-boxed investigation, in and out of scope written down, nothing counted twice. Use before any estimate, and again when the scope changes.
---

# Work breakdown

Most estimates go wrong before the first number: a piece of work is missing from the list, or one big vague item hides several smaller ones. This skill turns a goal into a list of small, clearly defined pieces that together cover all the work once, marks what is not known yet, and writes down what is in and out of scope, so that the estimate that follows is about something everyone can see.

**Route:** a goal, spec or ticket list → **work-breakdown** → scope questions to the owner → `range-estimate`.

## When to use

- Before any estimate of more than a few days of work.
- When the scope changes, to see what moved.
- Not for scheduling who does what and when: that is the project manager's plan.

## Inputs

- The goal, the spec or the ticket list.
- The codebase or system the work touches, and its current state.
- Who will do the work, if known, so they can check the breakdown.

## Steps

1. **List the deliverables:** what will exist when the work is done, in the owner's words.
2. **Break each deliverable into pieces** of at most a few days of work. A piece has a one-line definition of what is done when it is done.
3. **Detail only what is near:** pieces for the next few weeks are small; later work can stay as larger, coarser items with a note that it will be broken down later.
4. **Add the usually forgotten work:** tests, code review, data migration, release steps, documentation, coordination with other teams, environments and access, clean-up of temporary code.
5. **Turn unknowns into investigations:** anything nobody can estimate yet becomes a time-boxed investigation piece (for example one day) whose result is a decision or a smaller breakdown.
6. **Write the scope:** what is in, what is out, and what is assumed to exist already. Send open scope questions to the owner.
7. **Check coverage:** every deliverable is covered by pieces, and no piece appears twice under different names.
8. **Have it checked** by the people who will do the work.

## Rules

- **No number yet.** This skill produces the list; the numbers come in `range-estimate`.
- **Small pieces near, coarse pieces far.** Detail is spent where knowledge exists.
- **Unknowns are visible.** An unknown is never hidden inside a larger piece.
- **Scope in writing.** What is out of scope is written as clearly as what is in.

## Checks before hand-over

- Every near piece is at most a few days and has a one-line definition.
- The usually forgotten kinds of work were checked.
- Unknowns are investigation pieces with a time box.
- In and out of scope are written and open questions sent.
- Nothing is counted twice.

## Artefacts

- `estimate/<goal>-breakdown.md`: deliverables, pieces with definitions, investigation pieces, scope, open questions.

## Hand-over

- **To `range-estimate`:** the breakdown.
- **To the owner:** the scope questions.
- **To the developers who will do the work:** the breakdown, for a check.

## Sources

Built on the GOV.UK Service Manual, «Planning in agile» and «Agile tools and techniques» (Government Digital Service, Crown copyright), adapted: plan in detail only the work about to start, keep later work at a high level, make planning visible, revisit it regularly. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Guides, «Agile lexicon» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted. Breaking work into a list that covers it all once is a general planning method, described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
