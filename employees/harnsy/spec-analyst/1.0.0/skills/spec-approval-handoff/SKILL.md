---
name: spec-approval-handoff
description: Put a spec to the person with its open questions, record their explicit approval (their words and the date) on the item, hand the work to the lead or developers as small slices in build order, keep the spec true during the build (scope or criteria change means a new approval), and at the end check the result against every criterion, met or not met. Use once a spec draft is ready, and again at the end of the build.
---

# Spec approval and hand-off

A spec nobody approved is an opinion, and a spec that drifts from the code during the build is a trap. This skill runs the gate between writing and building: the person who owns the work says yes in their own words, the yes is written down, the work goes out in small slices, the spec is kept true while the code is written, and the result is checked against every criterion at the end.

**Route:** code-first-spec → **spec-approval-handoff** (gate → hand-off → build → final check) → the lead closes the item.
Before this skill: spec v0.1 attached to the item, self-check passed. After it: an approval note, a hand-off note, and a final met / not met table on the item.

## When to use

- A draft spec is ready for the person.
- A developer asks a question during the build, or the code shows the spec is wrong.
- The build is done and the result needs checking against the criteria.

## Inputs

- The spec attached to the item, with its open questions.
- Who the person is: the one who owns the work and approves it (named on the item or by the lead).

## The approval gate

- Development starts only on the person's explicit approval. The words must say yes to this spec and this version: «approved», «go ahead with v0.2».
- The approval is recorded on the item in a note: the person's own words, quoted; their name; the date; the spec version. The spec header then says «approved by: <name, date>».
- The lead may relay the person's words, quoted and dated. The lead never approves for the person, and «they're fine with it» without their words is not a record.
- Silence is not approval, however long it lasts. Ask again, or report on the item that the spec is waiting.
- «OK, but …» is a change request, not approval: work the «but» into the spec, raise the version, ask again.
- Any later change to scope or criteria goes back to the person as a new version for a new approval.

## Steps

1. **Put it to the person:** a summary of five lines at most, the link to the spec, and the open questions. At most five questions per round, most important first; each with «Recommended: …» and «Why it matters: …». Then stop and wait; do not start slicing in the same turn.
2. **Write the answers back** into the spec (question → answer, who answered, date) and raise the version.
3. **Ask for approval** of the named version in one plain question. When the answer is a yes, record it as above. When it is anything else, go back to step 2.
4. **Hand off.** Give the lead or the developers the slices in build order. Each slice:
   - delivers something end to end through every layer it touches, and can be checked on its own;
   - names the criteria it proves and the check to run;
   - names the files and names involved, so a developer who never saw the code can start;
   - says «blocked by: <slice>» or «blocked by: none».
   A wide mechanical change goes in three steps: add the new beside the old, move the callers in batches, remove the old.
5. **During the build:** answer questions from the spec. When the code shows the spec is wrong, correct the spec first, then tell the developer.
   - A wording fix that changes no result: an amendment line in the spec with the date.
   - A change of scope or of any criterion: a new version, back to step 1. The developers keep building only the slices the change does not touch.
6. **Final check.** When the lead says the build is done, check every criterion against the result: met or not met, with the evidence (test name and result, `path:line`, or the observed output from a stand check). Write the table on the item. A not-met criterion goes to the lead with what was seen; you do not fix code.

## If you are not on the team at the end

The spec's criteria table is enough to run the final check without you: the reviewer or the lead takes each criterion number, runs its row of the test plan, and writes met or not met with the evidence.

## Rules

- No hand-off without a recorded approval of the current version.
- Never edit an approved version in place for a change of scope or criteria; write the next version and say what changed.
- No production code, no merges; questions of priority go to the product owner, design choices to the software architect.

## Checks before hand-over

- The approval note has the person's words, name, date and the spec version.
- The hand-off note lists every slice with its criteria, check and blockers.
- The final table covers every criterion number, each with evidence.

## Artefacts

- On the item: the spec versions as attachments; the approval note; the hand-off note; amendment and version notes; the final met / not met table.

## Hand-over

- **To the lead or the developers:** the slices in build order.
- **To the lead:** not-met criteria, and any spec waiting for approval.
- **To the person:** every new version after a change of scope or criteria.

## Sources

No endorsement by these projects or their authors is implied.

Built on agent-skills, «spec-driven-development» and «planning-and-task-breakdown» (github.com/addyosmani/agent-skills, commit aeac41d; Addy Osmani, MIT), adapted. Built on mattpocock/skills, «to-tickets» (github.com/mattpocock/skills, commit 5beb35b; Matt Pocock, MIT), adapted. Built on superpowers, «writing-plans» (github.com/obra/superpowers, commit bb92a77; Jesse Vincent, MIT), adapted. Built on spec kit, the clarify command (github.com/github/spec-kit, commit 6ad2082; GitHub, Inc., MIT), adapted. Built on Code-With Engineering Playbook, «Minimal slices» (github.com/microsoft/code-with-engineering-playbook, commit 016770e; © Microsoft, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Ideas only, no text taken: PEP 1, statuses and a new document that supersedes an accepted one (Barry Warsaw, Jeremy Hylton, David Goodger, Alyssa Coghlan; public domain or CC0 1.0); GOV.UK Service Manual, «Writing user stories», acceptance criteria as a checklist (Crown copyright).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
