---
name: interface-options
description: Put two real options for a code-level change side by side (a different module split or a different interface, not two names for one idea), compare them on interface size, callers touched, migration cost and reversibility, then choose, name the deciding criterion and the observable sign that would make us switch. Use when a new module, interface, edge or move has more than one sensible shape.
---

# Interface options

When code takes a new shape, the first shape that comes to mind tends to stay, because callers start to rely on it the day it lands. This skill draws a second, really different shape before anything is built and compares the two on four questions the code itself can answer: how much a caller has to learn, how many places change, how many landings the move needs, and what undoing it would take. It ends in a choice with a stated reason and a stated condition for changing course.

**Route:** a call from a developer, the lead or the owner → **interface-options** → an options note with a choice → **code-decision-record** → **module-boundaries** when code has to move.
Before this skill: the change asked for and the code-structure baseline. After it: an options note of one page at most, linked from the record.

## When to use

- One of the cases where developers call the architect before writing code, when more than one sensible shape exists: a new module or top-level folder; a new or changed public interface; a new edge between modules or a cycle; moving or splitting a module; a new runtime dependency or storage choice.
- Two developers would build it differently, or a reviewer asks «why not the other way round?».
- Not when the answer is obvious: write the record straight away with code-decision-record and say that no comparison was needed.
- Not for platform, vendor or hosting choices; they are outside code level.

## Inputs

- The change asked for, in one or two sentences, and who asked.
- The code-structure baseline of the repository (the `--json` file of its scan).
- The callers of the code in question: a search over the repository or the import graph, with the command that produced the list.
- The project's existing decision records and layout notes, especially any record this change would contradict.

## Rules

- Exactly two options are compared in full. Leaving the code as it is counts only when it is really viable. Every other idea gets one line: «dropped, because …».
- The two must differ in where code lives or in what callers see. If both turn out to be the same idea under two names, stop and find a real second one.
- Both options are judged on the same four criteria at the same depth, with numbers wherever they can be counted.
- An option that adds an interface (a contract with an implementation behind it) names its second implementation, or the test that needs the contract. Without one, a plain call is the default.
- Adding beats changing: a new function or an optional parameter keeps today's callers working, so it usually costs less to migrate and to undo.
- The architect chooses code-level questions: the module split, the interface shape, a new edge. A choice that changes scope or cost, adds a runtime dependency with a licence or a price, or picks storage stays a proposal until the owner or lead confirms it.

## Steps

1. **Write the constraints** any answer must meet: the callers and what each one needs, what must stay hidden behind the interface, compatibility or speed limits, the project's own rules. List the callers together with the search command.
2. **Draft wide, keep two.** Sketch several shapes quickly, each pushed a different way: the smallest surface a caller can use; the easiest call for the most frequent caller; room for the variant that is most likely to come next. Keep the two strongest that really differ; the rest become «dropped» lines.
3. **Describe each option** in a few lines: what it exposes (public names, types, endpoints, events), where it lives (module and folder), what it hides, and which existing code it replaces. A short signature sketch says more than prose.
4. **Compare in one table** on the four criteria:
   - **interface size**: public names and parameters a caller has to learn;
   - **callers touched**: files or modules that must change, counted from the search in step 1;
   - **migration cost**: how many separate landings, and how many temporary forwarding files while callers move;
   - **reversibility**: what undoing it would take six months from now, once more code depends on it.
   Under the table, one good and one bad point per option that the numbers do not show.
5. **Choose.** Name the option, the criterion that tipped it, and **what would make us switch**: a condition anyone can observe later, for example «a third caller needs the batch form» or «the storage contract gets a second implementation». Say whether a part of the other option is worth keeping.
6. **Pass it on** to code-decision-record with the note linked. If code has to move, module-boundaries plans the moves.

## Checks before hand-over

- Two options that differ in split or in interface, plus one line for each dropped idea.
- The same four criteria for both, with counts where countable; the caller count shows its search command.
- Each added interface names its second implementation or its test need.
- The deciding criterion and an observable switch condition are written down.
- The decider is named: the architect for code-level choices, the owner or lead for scope, cost, a priced or licensed dependency, or storage.

## Artefacts

- An options note of one page at most: constraints, callers with the search, the two options, the table, the dropped ideas, the choice and the switch condition. It lives where the project keeps design notes; with no such place, next to the decision record it feeds, under the same number.

## Hand-over

- **To code-decision-record:** the chosen option and the note.
- **To the lead or owner:** choices that change scope or cost, add a priced or licensed dependency, or pick storage, marked as proposed.
- **To the developers:** the signature sketch of the chosen option, once its record is accepted, so the items built from it match.
- **To the reviewer:** the switch condition, so that a later change meeting it comes back to the architect.

## Sources

No endorsement by these projects or their authors is implied.

Built on Code-With Engineering Playbook, «Trade studies» (github.com/microsoft/code-with-engineering-playbook, commit 016770e; © Microsoft, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Ideas only (no text taken): MADR decision record template, good and bad points per option (github.com/adr/madr, commit ba75bb1; Oliver Kopp, Olaf Zimmermann and contributors, MIT); mattpocock/skills, codebase-design (github.com/mattpocock/skills, commit 49dd158; Matt Pocock, MIT); agent-skills, interface design and migration (github.com/addyosmani/agent-skills, commit aeac41d; Addy Osmani, MIT); superpowers, brainstorming (github.com/obra/superpowers, commit bb92a77; Jesse Vincent, MIT); Google Style Guides, Go guidance on interfaces (github.com/google/styleguide, commit f43b95b; Google, CC BY 3.0).

General software-design practice from published books, described in our own words; comparing two designs before settling on one is widely known as «design it twice».

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
