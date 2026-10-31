---
name: async-update
description: Write one team's weekly update in four short parts - done (with links), next, blocked (by whom, since when, who can unblock it), decisions needed (links to decision docs and their dates) - plus risks and dependencies in one line each, written for someone who missed the week, with nothing that needs a reply buried; the team lead publishes it. Use weekly, instead of a status meeting.
---

# Async update

A status meeting asks everyone to stop working so that each person can say what they did. A short written update does the same job for readers in any time zone, keeps a record, and puts the one thing that needs an answer where nobody can miss it.

**Route:** the team's board, merged work and decision docs → **async-update** → the team lead publishes it → open decisions to `decision-doc`.

## When to use

- Every week, instead of a status meeting.
- When stakeholders ask «where are we?» more than once a week.
- Not for a programme's status against its plan (the program manager reports that), and not for a personal daily note.

## Inputs

- The team's board, merged or shipped work, open decision docs, blockers raised.
- The previous update, so nothing drops silently.

## Steps

1. **Done:** what was finished or shipped, each with a link to the evidence.
2. **Next:** what the team will work on, in a few items.
3. **Blocked:** each blocker with what or who it waits on, since when, and who can unblock it.
4. **Decisions needed:** each with a link to its decision doc and the reply-by date.
5. **Risks and dependencies:** one line each, with who is watching.
6. **Carry-overs:** anything from last week's update that is neither done nor still listed is named, so nothing disappears.
7. **Put what needs a reply first** if anything is urgent; never in the middle.
8. **Hand it to the team lead** to publish in the shared place.

## Rules

- **Short and linked.** Every item points to evidence.
- **Written for someone who missed the week.** No «as discussed».
- **Blockers name who can unblock.**
- **No extra work for the team.** The update comes from the board and the work already done, not from a round of questions.
- **Nothing published by the agent.**

## Checks before hand-over

- Every done item has a link.
- Every blocker names who can unblock it and since when.
- Every decision needed has a doc and a date.
- Last week's items are all accounted for.

## Artefacts

- `updates/<yyyy-ww>.md`: done, next, blocked, decisions needed, risks and dependencies, carry-overs.

## Hand-over

- **To the team lead:** the draft, to publish.
- **To `decision-doc`:** decisions needed that have no doc yet.
- **To the program manager:** the published update, if the team is part of a programme.

## Sources

Built on 18F Product Guide, «Build» and «Collaborate» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: a concise regular shipping update to the team and stakeholders with dependencies and risks, demos instead of status meetings. Built on GOV.UK Service Manual, «Agile tools and techniques», «Creating an agile working environment» and «Measuring and reporting progress» (GDS, Crown copyright), adapted: a shared visible board, show-and-tell instead of status meetings, reporting without extra work for the team. Contains public sector information licensed under the Open Government Licence v3.0. Built on the TTS Handbook, «Internal communications» (github.com/GSA-TTS/handbook at c220f93; Technology Transformation Services, GSA; CC0 1.0), adapted: make work visible, messages scheduled for working hours. Built on Open Source Guides, «Best practices for maintainers» (© Open Source Guides authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: keep communication public, document processes. Content based on github.com/github/opensource.guide used under the CC-BY-4.0 license.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
