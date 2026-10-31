---
name: cut-list
description: Propose what a product, flow or page can do without - one row per feature, setting, step, field or sentence with why to cut it, who loses what, the expected effect as a hypothesis, how to undo the cut and the evidence - ranked by gain against loss, for the product owner to decide row by row. Use when a product, form or settings page has grown, before adding anything new to it, or when people get stuck or give up.
---

# Cut list

Products grow by addition: a field for one team, a setting for one customer, a sentence for one complaint. Each makes sense alone; together they make the task slower and harder. This skill goes through everything on the table, asks what each item is for, and proposes the ones that can go, each with the people who would miss it and the way to bring it back. It proposes; the product owner decides.

**Route:** a product, flow or page with its users and their task → **cut-list** → the product manager decides each row → the ui designer changes the screens for accepted rows.

## When to use

- A form, settings page, onboarding flow or feature set has grown and people are slow, make mistakes or give up.
- Before adding something new to a crowded screen.
- Not for deciding priorities between new features (that is the product manager's roadmap), and not for legal text or steps required by law or contract.

## Inputs

- The product, flow or page: screenshots or links, in the order people use them.
- Who uses it and for which task.
- Usage data, research notes, support questions, if they exist. Without them every row is marked as an opinion to check.

## Steps

1. **List every item** on the table: features, settings, options, steps, fields, help texts and sentences. Number them in task order.
2. **Ask what each item is for:** who uses the answer or the setting, what happens with it, how it is checked and kept up to date. Write the answer next to the item, or «nobody could say».
3. **Pick the candidates.** An item is a candidate when it has no known purpose, is rarely used, repeats another item, collects information nobody uses, or only explains a confusing part of the interface (fix the interface instead).
4. **Write one row per candidate:**
   - **item** — the number and name;
   - **why cut** — the reason from step 3, in one sentence;
   - **who loses what** — which user group or team, which task gets harder, which data is no longer collected;
   - **expected effect** — fewer steps, fewer errors, less to maintain, written as a hypothesis, never as a promise;
   - **how to undo** — switch it back on with a flag or a setting, restore it from version history, re-enable the field (say whether earlier data is kept);
   - **evidence** — the data, the research note or the support count, or «none: opinion, to check».
5. **Check each row against the people who find the service hardest to use** (people using a screen reader or a keyboard only, people with little time or a poor connection, people new to the subject). A cut that harms them is marked «do not cut» or comes with an alternative.
6. **Flag what must stay:** steps and texts required by law, a contract or security are not cut; mark them for the owner with the reason they look removable.
7. **Rank the rows:** largest expected gain for the smallest loss first. Rows without evidence go below the rows with evidence, with a note on how to check them cheaply.
8. **Hand the list over** and record the product manager's decision on each row (cut, keep with the reason, check first).

## Rules

- **Propose, never remove.** Nothing is switched off, deleted or hidden by this skill; the owners apply accepted rows.
- **Every row has a way back.** A row without «how to undo» is not finished.
- **Evidence and opinion are labelled.** An opinion is allowed, but it is called one.
- **Talk about the item, never about who added it.**
- **«Keep» is a valid answer.** When the owner keeps an item with a reason, the reason is recorded and the row is closed.

## Checks before hand-over

- Every row has item, why cut, who loses what, expected effect, how to undo and evidence.
- Every row was checked against the people who find the service hardest to use.
- No legally or contractually required item is proposed for removal.
- The list is ranked, and rows without evidence are marked.

## Artefacts

- `simplify/<product-or-page>/cut-list.md`: the numbered item list, the rows, the ranking and a decision column.

## Hand-over

- **To the product manager:** the ranked list, for a decision on each row.
- **To the ui designer:** the accepted rows that change screens.
- **To the team that owns the data:** rows that stop collecting a field, so reports and integrations are checked first.

## Sources

Built on the GOV.UK Service Manual, «Structuring forms», «Designing good questions» and «Make the service simple to use», and on the Government Design Principles (Government Digital Service, Crown copyright), adapted: know why each question is asked, do less, remove what does not work, make the service easy to use. Contains public sector information licensed under the Open Government Licence v3.0. Built on the U.S. Web Design System design principles (GSA Technology Transformation Services; CC0 1.0), adapted: who has the most difficulty, can people undo. Built on 18F Guides, product guide (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
