---
name: spec-triage
description: Decide for every incoming engineering task whether it needs a spec, with one verdict line on the item - spec, no spec, spec later or ask first - after searching the code and the commit history for work already built; lists of when a spec pays off and when it does not, and where tasks that are not spec work go. Use on every new task, before any other work on it.
---

# Spec triage

A spec earns its keep when a wrong guess would be expensive to undo: a change on paper costs an edit, the same change after the build costs rework. For a typo or a one-file fix with a failing test, a spec is pure overhead. This skill sorts every task into one of four verdicts in minutes, writes the verdict on the item in one line, and sends the task on.

**Route:** a new task on the board → **spec-triage** → «spec» goes to **code-first-spec**; every other verdict goes back to the lead, the person or the role named below.
Before this skill: the task as written. After it: one verdict line on the item, and nothing else unless the verdict is «spec».

## When to use

- Every new engineering task, before any other work on it.
- A task comes back with a changed scope: triage it again.
- Not for content, research or design tasks without code; say so on the item and hand it back to the lead.

## Inputs

- The whole item: title, text, comments, links, who asked and why.
- Read access to the code and its commit history.

## Steps

0. **Search before judging.** Look for the task in the code and the commit history: its key words, the names of the screens, endpoints or tables it mentions, and any item reference in commit messages. A task is often already built, partly built or reverted; the search can turn «spec» into «no spec» in a minute.
1. **Read the item to the end,** including comments: a later comment often narrows or widens the ask.
2. **A short look at the code** where the change would land: which modules, whether a public interface, a data schema or a migration is involved. Minutes, not hours; the deep read belongs to code-first-spec.
3. **Check the «spec needed» list.** The first entry that fits is the reason:
   - the change crosses more than one code module, or touches a public interface, a data schema or a migration;
   - the behaviour is unclear, or people disagree about it;
   - there are two or more real ways to build it;
   - security, money, personal data or possible data loss is involved;
   - it is more than about a day of work;
   - the requester cannot judge the change from the code (they will judge the result only by what they see).
4. **If none fits, check the «no spec» list:**
   - copy, styles or a typo;
   - a bug in one file with a failing test that shows it;
   - a revert;
   - a patch-level dependency update;
   - the task already states acceptance criteria that a test can check;
   - the work is already built (from step 0).
5. **Apply the copy rules.** Count modules only for code: the same sentence in several language files is one change, not many. Legal or privacy wording is copy too, but its gate is the lawyer, not a spec: «no spec: copy; the lawyer reads it».
6. **Pick the verdict and write it on the item,** one line:
   - `spec: <trigger from the list>` and the files you looked at;
   - `no spec: <reason>`, for example `no spec: already built at <path:line>; what is left is a check`;
   - `spec later: blocked on <item>; write it when that lands` when the spec depends on an interface or decision that does not exist yet;
   - `ask first: <question>; spec if <answer>` when one answer decides between «spec» and «no spec».
7. **When torn between «spec» and «no spec»,** choose «spec» and name the doubt: a short spec is cheap, a wrong build is not.
8. **Route what is not spec work:** people disagree about what is wanted or for whom → requirements analyst; whether it is worth doing, or in which order → product manager or product owner; a design question with no task behind it yet → software architect.

## Rules

- One verdict line before anything else; no spec draft, no plan, no code in the same note.
- A «no spec» verdict names its reason from the list; «already built» names the file and line.
- Never re-prioritise or close a task: the verdict is advice for the lead.
- Triage is not a review of the request's value; that belongs to the product roles.

## Checks before hand-over

- The search of step 0 was done, and its result is in the note when it changed the verdict.
- The verdict is one of the four forms, with a reason taken from the lists.
- For «spec»: the files looked at are listed. For «ask first»: one question, with the answer that would mean «spec».

## Artefacts

- A one-line verdict note on the item, plus the list of files looked at for «spec».

## Hand-over

- **«spec»:** to code-first-spec, yourself.
- **«no spec»:** to the lead, who seats a developer, the copywriter or the lawyer.
- **«spec later»:** to the lead, with the blocking item named.
- **«ask first»:** the question to the person or the lead; triage again on the answer.

## Sources

No endorsement by these projects or their authors is implied.

Built on agent-skills, «spec-driven-development», the list of when not to write a spec (github.com/addyosmani/agent-skills, commit aeac41d; Addy Osmani, MIT), adapted. Built on mattpocock/skills, «triage» (github.com/mattpocock/skills, commit 5beb35b; Matt Pocock, MIT), adapted. Built on Code-With Engineering Playbook, «Definition of ready» and «Design reviews» (github.com/microsoft/code-with-engineering-playbook, commit 016770e; © Microsoft, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on Open Practice Library, «Definition of Ready» (openpracticelibrary.com/practice/definition-of-ready/, read 2026-10-20; Matt Takane, Ilaria Doria; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
