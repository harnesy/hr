---
name: code-decision-record
description: Write a one-page record of a code-level decision: problem, context, options, the choice with its reason and decider, what gets better and worse, follow-up items, the check that shows the code keeps to it, and status, in the project's own place and format. Use for every OK or no on a HARD limit, for a new module, public interface or edge between modules, after interface-options, and when a record is replaced.
---

# Code decision record

A decision about code structure is forgotten faster than the code it shaped. A year on, someone meets an odd import rule or a module split that seems pointless, and has nobody to ask. This skill writes the reason down on one page next to the code, names who decided, and names the check that keeps the code true to the decision.

**Route:** a call from a developer, or an options note from interface-options → **code-decision-record** → the decider confirms → follow-up items for the developers, through module-boundaries when code has to move.
Before this skill: the decision, or the options note it came from. After it: a numbered record with a status and a confirmation check the reviewer can run.

## When to use

- Always for a HARD exception (every OK or no on a HARD limit from code-structure), and for a new module, a public interface or a new edge between modules.
- After interface-options, once a choice is made, and when an earlier record is replaced.
- For any other call, skip the record when the choice is cheap to undo, would not puzzle a newcomer and had no real alternative; a line in the change description is enough.

## Inputs

- The options note, if there is one, and the change that raised the question.
- The project's existing records: folder, file type, numbering, headings, index file, any tool configuration for them.
- Who decides this kind of question (see the rules).
- For a HARD exception: the code-structure scan row with the current size.

## Rules

- **Project first.** Use the project's place and format even when its headings differ from the ones below; fit the content into them. If two habits in the project conflict, say so; never start a second scheme beside an existing one.
- **No place yet:** propose `docs/decisions/NNNN-short-title.md`, with one index line per record, and create the folder only after the owner says yes.
- **One page at most:** about 400 words or 60 lines. Longer reasoning stays in the options note and is linked.
- **One decision per record.**
- **Name the decider.** The architect decides code-level questions: module split, interface shape, a new edge between modules, a HARD exception. A decision that changes scope or cost, adds a runtime dependency with a licence or a price, or chooses storage stays «proposed» until the owner or lead confirms it.
- **Accepted means frozen.** When the team thinks again, it writes a fresh record. The earlier one changes only its status, to «superseded by NNNN», and the two link to each other.
- **Real dates.** A record written after the fact carries the date the decision was really made and says that it was written later.

## Steps

1. **Find the project's place and format** (decision folder, wiki page, index file) and follow it. If there is none, propose the default path above and wait for the owner's yes.
2. **Number it** the project's way: the next free number, or the work item id when several people write records at the same time and numbers would clash.
3. **Write the record** in these parts:
   - **Title:** the problem and the answer in one line, for example «Billing reads accounts through one contract module».
   - **Problem:** two or three sentences; ending in a question is fine.
   - **Context and constraints:** what is true now (scan rows, edges, callers) and what any answer has to respect.
   - **Options:** one line each, with a link to the options note when there is one.
   - **Decision:** «Chosen: X, because …», tied to the deciding criterion, then «Decided by:» and the role.
   - **Consequences:** what gets better; what gets worse, always at least one line; follow-up items, each filed as a work item.
   - **Confirmation:** the concrete check that shows the code keeps to the decision: an import rule in the project's linter or boundary tool, a structure test, a code-structure scan limit compared on every change, or a named review point when nothing can be automated.
   - **Status and date:** proposed, accepted, rejected, deprecated, or superseded by NNNN.
4. **Approval.** Code level: the architect accepts the record and sends it to the developer who called. Beyond code level: show the draft to the owner or lead and wait for approval before writing the file. Where the project reviews changes, the record arrives as a change for review.
5. **Set the status.** Proposed until the decider confirms; accepted once confirmed or merged. Add the index line if the project keeps an index.
6. **Replacing a record:** write the new one with «supersedes NNNN»; in the old one change only the status line, to «superseded by» the new number with a link.

## HARD exceptions

A developer who cannot meet a HARD limit of code-structure asks the architect before writing the code. The answer is a short record of its own:

- which limit, and the current size from the scan;
- why it cannot be met in this change;
- **OK:** status accepted, decided by the architect, with the follow-up item that brings the code back under the limit;
- **No:** the reason, and what to do instead: split first, or take the smaller option.

## Checks before hand-over

- Title, problem, context, options, decision with «because», consequences, confirmation and status are all present.
- At least one line says what gets worse.
- The decider is named; anything beyond code level is still «proposed» until confirmed.
- The confirmation names a check someone can run, not an intention.
- The record fits one page; longer reasoning is linked.
- Superseded pairs link both ways, and the old record is otherwise untouched.
- The record sits in the project's place, or the proposed path has the owner's yes.

## Artefacts

- The record: `docs/decisions/NNNN-short-title.md` or the project's equivalent.
- An index line, where the project keeps an index.
- The follow-up items it names, filed as work items.

## Hand-over

- **To the developers:** the follow-up items, each one landing on its own.
- **To the lead or owner:** records left «proposed» because they touch scope, cost, a priced or licensed dependency, or storage.
- **To the reviewer:** the confirmation check, so that every later change is held to it, and each HARD exception with its follow-up item.

## Sources

No endorsement by these projects or their authors is implied.

Built on MADR decision record template (github.com/adr/madr, commit ba75bb1; © 2017-2022 Oliver Kopp, Olaf Zimmermann and contributors, MIT licence), adapted. Built on Code-With Engineering Playbook, «Decision log» (github.com/microsoft/code-with-engineering-playbook, commit 016770e; © Microsoft, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Ideas only (no text taken): mattpocock/skills, domain-modeling (github.com/mattpocock/skills, commit 49dd158; Matt Pocock, MIT); ECC, its decision-records skill (github.com/affaan-m/ECC, commit 76aaa77; Affaan Mustafa, MIT); agent-skills, documentation and decision-record skill (github.com/addyosmani/agent-skills, commit aeac41d; Addy Osmani, MIT); «Documenting Architecture Decisions» (Cognitect blog, 2011; CC0 1.0).

General software-design practice from published books, described in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
