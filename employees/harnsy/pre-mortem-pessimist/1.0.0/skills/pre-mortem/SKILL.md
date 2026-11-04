---
name: pre-mortem
description: Run a failure-first session on a plan before it starts - recap the plan with its owner, set a date about six months on when the plan has clearly failed, collect every participant's reasons privately before anyone reads the others, group them into themes, score them on the owner's scale with avoidability, detectability and recovery, and give each top item a prevention, a fallback and a proposed owner. Use once before the start of a plan, and again at a milestone when things look good.
---

# Pre-mortem

Plans are usually reviewed by asking what might go wrong, and the answers come out polite and few. A pre-mortem turns the question round: the plan has already failed, and everyone explains why. Written alone and opened together, the reasons are more numerous, more specific and less shaped by the loudest voice. The session ends with actions, not with worry.

**Route:** a plan and its owner → **pre-mortem** → `early-warning-signs` for the top items → `risk-handoff` to the plan's owner.

## When to use

- Before a plan starts: a launch, a migration, a reorganisation, a contract, a new product bet.
- Again at a milestone when things are going well, to catch confidence that has grown faster than evidence.
- Not for keeping the risk register during the work (that stays with whoever runs the work), and not for reviewing an investor pitch.

## Inputs

- The plan: goal, date, scope, main assumptions, dependencies.
- The plan's owner, who accepts or changes the results.
- The participants, people or agents, including a few with a stake who are likely to be critical.
- The owner's scale for likelihood and impact and the level of risk the owner accepts; ask for both if missing, never assume them.

## Steps

1. **Recap the plan** in five lines or fewer and have the owner confirm it.
2. **Set the scene:** a date about six months after launch, or at the plan's end, on which the plan has clearly failed, and one sentence on what that failure looks like.
3. **Collect reasons privately.** Each participant writes every reason they can think of, one per item: what went wrong, why, and what warning signs there might have been. Nobody sees another's answers until everyone has written. With agents or remote people, collect the answers separately and open them together.
4. **Group into themes,** keeping each original reason visible under its theme; nothing is dropped as a duplicate without saying so.
5. **Score each theme** for likelihood and impact on the owner's scale, and note how easily it could be avoided, how hard it would be to notice while it is happening, and how well the team could recover.
6. **Pick the top items,** usually five to ten; the owner may move the cut.
7. **For each top item** write a prevention (what to start now), a fallback (what to do if it happens anyway) and a proposed owner with a date.
8. **Mark shared assumptions:** a belief that, if wrong, would cause several failures at once.
9. **Show the result to the owner,** record what the owner accepts, changes or rejects, and change nothing in the plan itself.

## Rules

- **Alone first, together second.** No discussion before every participant has written.
- **Causes, not moods.** Each item names a cause and an effect; «quality issues» is not an item until it says which quality and what follows.
- **Outside causes count.** Risks beyond the team's control are scored like the rest and get a response the team can act on.
- **Every top item gets a prevention.** If none can be found in the session, the item is marked open and a person is asked to propose one by a date.
- **The owner decides.** Scores and responses are proposals; the accepted level of risk is the owner's.
- **About the work, never a person.** A reason that blames one named person is reworded to the process or handed privately to the owner.

## Checks before hand-over

- Every participant wrote before seeing the others' answers.
- Every original reason appears under a theme.
- Every top item has a prevention, a fallback and a proposed owner with a date, or is marked open with a person asked.
- Scores use the owner's scale, and the accepted level is written at the top.
- Nothing in the plan was changed.

## Artefacts

- `risks/pre-mortem-<date>.md`: the recap, the scene, the participants, all reasons by theme, the ranked table, the top items with prevention, fallback and proposed owner, the shared assumptions.

## Hand-over

- **To `early-warning-signs`:** the top items.
- **To the plan's owner:** the whole file.
- **To the estimator:** items that are really questions of effort or duration.

## Sources

Built on «Pre-mortem – risk planning», Digital Service Toolkit (© State of New South Wales; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: invite critical stakeholders, recap the project, imagine a future failure, write reasons alone one per note, group into themes, rank, assign owners and actions, run it again when things go well. © State of New South Wales. For current information go to www.nsw.gov.au. Built on The Orange Book: Management of Risk – Principles and Concepts (HM Treasury, Crown copyright), adapted: risks from sources outside your control, small risks that combine, the beliefs of the people involved as a source of risk, a common scale. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Methods, «Hopes and fears» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: write individually, one per note, then share and group.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
