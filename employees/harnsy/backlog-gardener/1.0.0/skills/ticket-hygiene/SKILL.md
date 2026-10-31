---
name: ticket-hygiene
description: Check each open backlog item for a specific title, an owner of the next step, a done-when line or acceptance criteria, labels and a priority, and for every gap write the exact question to the one person who can answer it - grouped into one message per person, priority questions only to the product owner, never a guessed value; summarise long threads at the top when asked. Use during a backlog sweep or before a planning session.
---

# Ticket hygiene

An item without an owner, a clear title or a way to tell when it is done gets skipped in every planning session. Filling those fields by guessing makes it worse, because a guessed owner looks real. This skill finds the gaps and turns each one into one precise question for the person who actually knows.

**Route:** a backlog → **ticket-hygiene** → questions to owners → the answers filled in by the owners (or by the gardener, if an owner asks).

## When to use

- During a backlog sweep, or before a planning or refinement session.
- When a team says items are «unclear» without saying which.
- Not for writing requirements or acceptance criteria yourself: the owner or the product owner writes them.

## Inputs

- Read access to the tracker or an export.
- The team's definition of done, label set and priority scale.
- Who owns which part of the backlog.

## Steps

1. **Check each open item** for: a title specific enough to find and understand; an owner of the next step; a done-when line or acceptance criteria; the relevant labels; a priority from the product owner; for a user need, who needs it, what and why.
2. **For each gap, write the exact question** to the one person who can answer it, naming the item: «Who owns the next step on the search item, design or backend?».
3. **Never fill a field by guessing.** A suggested value, if any, is labelled as a suggestion inside the question.
4. **Group the questions:** one message per person, items in order.
5. **Send priority questions only to the product owner.**
6. **Summarise long threads** in three lines at the top of the item, when the owner asks: what is asked, what is known, what is open.
7. **Record the answers** as they come back, and list items still open.

## Rules

- **Questions, not guesses.** No field is filled without the owner's answer.
- **One person per question,** named.
- **Priority belongs to the product owner.**
- **Nothing edited in the tracker** without the owner's yes.

## Checks before hand-over

- Every gap has one question naming its item and its addressee.
- No field was filled by guessing.
- Priority questions went only to the product owner.
- Nothing was changed in the tracker.

## Artefacts

- `backlog/hygiene-<date>.md`: gaps by item, questions grouped by person, answers received, items still open.

## Hand-over

- **To the named owners:** their grouped questions.
- **To the product owner:** priority questions and the summary of gaps.
- **To the scrum master:** the list of items still unclear before a refinement session.

## Sources

Built on the Python Developer's Guide, triage pages «Triaging an issue», «Issue tracker» and «Labels» (python/devguide at 734d750; Python Software Foundation; CC0 1.0), adapted: a concise and specific title, every relevant label, the assignee as whoever takes the next step, a short comment with the next action, a summary when a thread is long. Built on GOV.UK Service Manual, «Writing user stories» (GDS, Crown copyright), adapted: who, what and why; acceptance criteria; a story as a placeholder for a conversation. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Agile Lexicon (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: definition of done as a working agreement, time-boxed spikes for uncertain items.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
