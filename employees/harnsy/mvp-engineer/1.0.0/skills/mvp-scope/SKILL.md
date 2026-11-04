---
name: mvp-scope
description: Scope the first real, working version of a product on one page - one user, one job, a «done when» list, what is in and out, every step done by hand for now with how and when it will be replaced, every shortcut with its risk, the release path with a way back, and the riskiest assumption it tests - for the owner to approve before building. Use before building a first version, or when a first version keeps growing.
---

# MVP scope

A first version is small enough to finish and real enough to keep. This skill pins it down on one page: one user, one job, a list that says when it is done, and an honest record of everything faked, skipped or done by hand, so nothing is hidden from the owner or from the developers who take it over later.

**Route:** an approved simplest version or a founder's idea → **mvp-scope** → the owner approves → the build in test-first slices → releases with a tested way back → hand-over to the developers with the shortcuts and done-by-hand lists.

## When to use

- Before building the first working version of a product or a large new part of one.
- When a first version keeps growing and nobody can say when it is done.
- Not for a throwaway prototype that answers one question (that is the prototype designer's work), and not for features in a product that already runs (the developers' work).

## Inputs

- The idea, the promise or the simplest-version page.
- Who the first users are and how many.
- What exists already: tools, data, accounts, an old way of doing the job.

## Steps

1. **One user:** who exactly, in a sentence (role and situation), in their own words where possible.
2. **One job:** the task they need done and why it matters to them.
3. **Done-when list:** three to seven lines «it's done when …», each checkable by a person or a test. These lines decide when building stops.
4. **In and out:** what this version does; what it deliberately does not do, each with the signal that would add it later.
5. **Done by hand for now:** every step a person does instead of the software (approving sign-ups, sending a weekly export, billing the first customers). For each: who does it, how often, how long it takes, the trigger for automating it, and the replacement plan. If a step would handle personal data, name the data, who sees it and when it is deleted, and get the owner's written OK before it starts.
6. **Shortcuts list:** hard-coded values, missing tests, a single server, no admin screen, a manual backup. For each: why it was taken, the risk, and how and when it is replaced.
7. **Release path:** who sees it first (an invited group), how the old way of doing the job keeps working meanwhile, who supports the first users, how a release is rolled back, and where the owner's approval comes in.
8. **Riskiest assumption:** the belief that would sink the product if false, and how the first release tests it.
9. **Get approval:** send the page to the owner; build nothing before the OK.

## Rules

- **Shortcuts are listed, never hidden.** A shortcut that is not on the list is a defect.
- **Nothing live without the owner's OK.** Every production change is a proposal with current state, change, expected effect and undo.
- **No personal data in a manual step without the owner's written OK.**
- **Small and reversible.** Each release can be rolled back, and the first one goes to an invited group.
- **Prototype code is not a starting point.** If a prototype exists, its findings are used, not its code.

## Checks before hand-over

- One user and one job, each in one sentence.
- Every done-when line is checkable.
- Every manual step has an owner, a frequency, a trigger and a replacement plan; personal data is named or absent.
- Every shortcut has a risk and a replacement.
- The release path names the first group, the old way, support and rollback.

## Artefacts

- `mvp/<product>/scope.md`: the one-page scope with the owner's approval and its date.
- `mvp/<product>/shortcuts.md` and `mvp/<product>/done-by-hand.md`: kept up to date during the build, handed over at the end.

## Hand-over

- **To the product owner or founder:** the scope page, for approval.
- **To the developers who take the product over:** the code, the shortcuts list and the done-by-hand list, each item with its replacement plan.
- **To the person doing a manual step:** what to do, how often, and when it ends.

## Sources

Built on 18F Guides, product guide (build, release strategies, measuring) (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: must-haves only, small prioritised features with acceptance criteria, a go-live plan with a way to revert, release to one user group at a time. Built on the GOV.UK Service Manual, «How the alpha phase works», «How the beta phase works» and «Writing user stories», and on the Government Design Principles (Government Digital Service, Crown copyright), adapted: riskiest assumptions first, an invited group first, keep the old service running, «it's done when» lines. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
