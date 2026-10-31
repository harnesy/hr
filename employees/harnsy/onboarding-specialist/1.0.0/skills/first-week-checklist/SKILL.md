---
name: first-week-checklist
description: Turn an approved onboarding plan into a dated checklist for the days before the start and the first week, with an access table (tool, level, owner, requested, confirmed) and a contacts table. Use about a week before a newcomer starts, and check it daily until the end of week one.
---

# First-week checklist

The plan says what should happen; the checklist makes sure it does. It is the list the newcomer, the buddy and the manager tick through, and the place where a missing laptop or account shows up while there is still time to fix it.

**Route:** approved plan (from `onboarding-plan`) → **first-week-checklist** → owners carry out their items → end-of-week check-in → `check-in-notes` at about 30 days.

## When to use

- About a week before the start date, once the plan is approved.
- Daily until the end of the newcomer's first week.
- When a team has no onboarding guide yet: the checklist becomes its first version.

## Inputs

- The approved onboarding plan.
- The tools and access the role needs, with each tool's owner and the access level.
- The team's onboarding guide, if one exists.
- The people the newcomer will work with, and what to ask each about.

## Steps

1. **Before the start.** One line per item, with owner and due date:
   - each access request, sent to the tool's owner;
   - equipment ordered and delivery confirmed;
   - calendar: recurring one-to-one, team meetings, buddy sessions;
   - buddy confirmed as willing and free;
   - welcome note with the time, place or link, and who meets the newcomer.
2. **Access table.** Columns: tool, level needed, owner, requested on, confirmed on, notes. Ask for the lowest level the work needs; raise it later if the work requires.
3. **Day one.** Setup, introductions, the conversation with the manager about expectations, a short tour of where things live (documents, chat channels, tracker).
4. **Rest of week one.** Reading for the role, meetings to sit in on, introductions with the reason for each, the first small task with its finish line and who reviews it, the end-of-week check-in.
5. **Contacts table.** Name or role, what to ask them about, how to reach them.
6. **Team guide links.** What the team works on and why, team agreements, setup steps, where things live. If a link is missing, note it for the manager.
7. **Daily check.** Mark done items, chase late ones, and flag to the manager anything not confirmed two working days before the start.

## Rules

- The agent requests and tracks; owners grant access. Any change to accounts or tools is a proposal (current state, change, expected effect, how to undo it) that the owner approves and carries out.
- The checklist holds work items only: nothing about health, family or other private matters.

## Checks before hand-over

- Every item has an owner and a date; every access line has an owner and a status.
- Access levels are the lowest the work needs.
- Anything unconfirmed two working days before the start is flagged to the manager.
- The first task has a clear finish and a named reviewer.

## Artefacts

- `onboarding/<newcomer-ref>/first-week.md`: the checklist with owners, dates and status.
- `onboarding/<newcomer-ref>/access.csv`: tool, level, owner, requested, confirmed, notes.
- `onboarding/<newcomer-ref>/contacts.md`: who to ask about what.

## Hand-over

- **To the newcomer and the buddy:** the checklist and contacts, on day one.
- **To tool owners:** access requests, one per tool.
- **To the manager:** anything late or unconfirmed, and the end-of-week check-in.
- **To the HR generalist:** policy questions the newcomer raises.

## Sources

Adapted from the onboarding skill in github.com/anthropics/knowledge-work-plugins, human-resources folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Also built on the onboarding guide template of the Code-With Engineering Playbook (© Microsoft; CC BY 4.0) and the Sourcegraph handbook (archived) onboarding page for hiring managers (© 2021 Felix Frederick Becker; Apache License 2.0; changed by harnsy). All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
