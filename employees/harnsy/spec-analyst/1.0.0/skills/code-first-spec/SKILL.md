---
name: code-first-spec
description: Study the code where a change lands (behaviour today, tests, callers, data) and write a one-page spec from it - header with version, date, status and approved-by, goal, scope, assumptions, current state with file:line, numbered acceptance criteria in the event-driven requirement pattern each with a test, changes, risks, open questions with recommended answers, test plan and task slices - then run the self-check. Use after spec-triage says «spec».
---

# Code-first spec

A spec written from the request alone describes the system someone imagines. A spec written after reading the code describes the system that exists, and the gap between the two is where most surprises hide. This skill reads first, writes one page, and checks its own page before anyone else sees it.

**Route:** spec-triage says «spec» → **code-first-spec** → a draft spec attached to the item → **spec-approval-handoff**.
Before this skill: the task, the triage line and the files it named. After it: spec v0.1 attached to the item, self-check passed.

## When to use

- After spec-triage gives the verdict «spec».
- When an approved spec needs a new version because scope or criteria changed.
- Not to settle what people want: if the request itself is disputed, the requirements analyst goes first and their problem statement is your input.

## Inputs

- The item and its triage line; any problem statement or business requirements written for it.
- The code at a named commit, its tests, and the commit history.

## Steps

1. **Assumptions first.** Before drafting, list what you are taking for granted about the request and the code. Each one later becomes a confirmed fact, an open question or a line in the spec's Assumptions.
2. **Study the code.** Where the change lands; how it behaves today (read it, and run the existing tests if that is cheap); which tests cover it; who calls it (search for every use); config, schema and migrations it touches. Write each finding as a short note with `path:line` and the commit you read. Use the project's own names for things.
3. **Draft the spec in the format below.** Criteria say what the system does; how it is built goes into «Changes». Code shapes are allowed only as a few lines marked «illustration only», never as code to paste.
4. **Write the criteria** in the event-driven requirement pattern, one result each:
   - default: «When <trigger>, the <system> shall <result>.»
   - failures: «If <unwanted condition>, then the <system> shall <result>.»
   - states: «While <state>, the <system> shall <result>.»
   «Shall» is binding; «will» states a fact; «should» states a goal and is not a criterion. A criterion survives a rewrite of the code: if its words would change when the implementation changes, it describes the how. To turn a criterion into a test scenario, given-when-then works well: the state before, the event, the expected result.
5. **Mark gaps in place.** Where the input does not say, write `needs answer:` with the question, never a plausible value. If work can go on, add your best estimate and who will confirm it.
6. **Quality pass on the text.** Read the spec as if it were code under test:
   - complete: error and edge cases have criteria; every in-scope point has at least one;
   - clear: no vague words such as «fast», «user-friendly», «robust», «as needed», «if possible», «etc.», no «it» or «this» without a clear subject, no «and/or»;
   - consistent: no two criteria conflict; one name for one thing;
   - measurable: numbers carry units and limits;
   - covered: every criterion has a row in the test plan.
7. **Two real options?** When the code allows two ways to build it and the choice will be hard to undo, write each in two lines, add the open question «software architect to decide», and stop there. Do not choose.
8. **Run the self-check below,** fix what fails, attach the spec to the item as v0.1 with status «draft».

## Spec format (one page, about 60 lines)

```
# Spec: <title>
v0.1 — <date> — status: draft | approved | superseded — approved by: <name, date> or «not yet»
Code read at: <commit>

## Goal and why
## In scope / Out of scope        (both lists; «out of scope: none» needs a reason)
## Assumptions                    (each one: confirmed, or an open question)
## Current state (from the code)  (about 8 bullets, each ending in path:line; more detail goes to an appendix)
## Acceptance criteria            (numbered; event-driven pattern; one result each)
## Changes by module and interface
## Risks                          (for data, migrations and public interfaces: how to roll back, and the sign to do it)
## Open questions                 (each: Recommended: …, Why it matters: …)
## Test plan                      (criterion number → test at the highest existing seam, or «stand check: <steps>»)
## Task slices in build order     (each: what it delivers, criteria it proves, its check, blocked by)
```

- Test plan: prefer a test at the highest boundary the code already has over a new, deeper one. Where no automated test can reach a criterion (a page with no test harness), write `stand check: <steps and what to look for>`.
- Add the few likely bad inputs the spec does not mention (empty, too long, duplicate, missing permission) and a check for each: silence in the spec is not permission to break.
- Longer than one page: split by module or by slice and say so in the header. Do not pad and do not cut the file:line references.

## Example criteria (illustration)

- When a user submits the export form with an empty date range, the export service shall reject the request with «Choose a date range» and create no file.
- If the payment provider gives no answer within 10 seconds, then the checkout service shall mark the order «pending» and keep the cart.
- While an account is suspended, the login endpoint shall refuse new sessions with the reason «suspended».

## Self-check (before the spec leaves you)

- **Every file:line opened and true:** re-open each cited `path:line` at the commit in the header and confirm it shows what the sentence says. A short loop that prints each cited line from the commit is enough.
- **Every criterion in the pattern, with a test:** each matches one of the three forms, has one result, and has a row in the test plan.
- **No architecture decided:** a real design choice appears as an open question for the software architect, not as a decision in «Changes».
- **Length:** about 60 lines; «Current state» at about 8 bullets.
- Header complete: version, date, status, approved-by, commit read.
- Every open question carries a recommended answer and why it matters.

## Artefacts

- The spec, attached to the item, named with its version.
- The code notes (path:line per finding), kept with the spec as an appendix when they do not fit on the page.

## Hand-over

- **To spec-approval-handoff:** the draft with its open questions.
- **To the software architect:** the two options, when the spec shows a real design choice.
- **To the requirements analyst:** a request whose purpose turns out to be disputed.

## Sources

No endorsement by these projects or their authors is implied.

Built on agent-skills, «spec-driven-development» (github.com/addyosmani/agent-skills, commit aeac41d; Addy Osmani, MIT), adapted. Built on mattpocock/skills, «to-spec» (github.com/mattpocock/skills, commit 5beb35b; Matt Pocock, MIT), adapted. Built on spec kit, spec template and the clarify and checklist commands (github.com/github/spec-kit, commit 6ad2082; GitHub, Inc., MIT), adapted. Built on superpowers, «writing-plans» (github.com/obra/superpowers, commit bb92a77; Jesse Vincent, MIT), adapted. Built on Code-With Engineering Playbook, feature design review template and trade studies (github.com/microsoft/code-with-engineering-playbook, commit 016770e; © Microsoft, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Facts only, no text taken: requirement sentence patterns after Mavin, Wilkinson, Harwood and Novak (IEEE RE 2009); NASA Systems Engineering Handbook, Appendix C (U.S. Government work); GOV.UK Service Manual, «Writing user stories» (Crown copyright); requirement smells after Femmer et al. (arXiv:1611.08847); the given-when-then scenario style from behaviour-driven development; Cucumber documentation, «Writing better Gherkin» (Cucumber Ltd, MIT), idea only.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
