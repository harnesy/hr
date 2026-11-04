---
name: module-boundaries
description: Map the modules of an existing codebase and plan the way to clean boundaries in small safe steps: a current modules table from the code-structure scan and the import graph, a target layout (feature modules, one shared home, entry wiring, edge rules) and ordered migration items that each keep behaviour unchanged and carry their own check. Use when modules must be moved, split, merged or untangled.
---

# Module boundaries

Moving code between folders looks harmless and is one of the easiest ways to break something nobody tested. This skill turns «the structure is a mess» into three things the team can check: a table of what exists now, a target layout with rules on which module may import which, and a list of moves that each land on their own, keep behaviour the same and can be undone by reverting one change. The architect writes the plan; the developers make the moves.

**Route:** a record from code-decision-record, or a call to move or split a module → **module-boundaries** → migration items for the developers → each item checked with the code-structure scan delta and the edge check.
Before this skill: the code-structure baseline and the import graph. After it: a modules table, a target layout and an ordered list of items.

## When to use

- A record says code has to move: a module split or merged, shared code gathered in one home, a cycle broken.
- Code grouped by kind (all handlers in one place, all models in another) has to become code grouped by feature.
- Not for a change that stays inside one module, and not for replacing a running service behind live traffic.

## Inputs

- **The scan baseline:** run code-structure's `scripts/structure_scan.py <repo> --json baseline.json` and keep the file. It gives sizes per file and folder; it does not read imports.
- **The import graph:** the edges between top-level modules, with the command that produced them. Per stack, as facts (a tool the project does not have yet is a proposal to the owner, never installed unasked):
  - Go: `go list -f '{{.ImportPath}}: {{join .Imports " "}}' ./...` prints each package with its direct imports.
  - JavaScript and TypeScript: a tool such as dependency-cruiser or madge.
  - Python: a tool such as import-linter or pydeps.
  - Java and Kotlin: `jdeps -summary` on compiled classes, or architecture tests with a library such as ArchUnit.
  - Rust: a tool such as cargo-modules. PHP: a tool such as deptrac. Ruby: a tool such as packwerk.
  - Any stack, always available: grep the import, use or require lines, for example `grep -rnE "^(import|from|use|require)" src/`, and count them per pair of top-level folders.
  - One flat package or folder: imports show nothing. Group the files by feature (a name prefix, or the project's own map). Count the references between groups instead: each group's exported names, searched for in the other groups' files (a language server's find-references, or grep), with the command shown. The counts are approximate; say so in the table.
- The project's records, layout notes and lint rules, and the decision record this plan carries out.

## Rules

- No single big move: one item, one landing.
- Structural items are never mixed with features or fixes, in either direction.
- The architect writes items and the developers make the moves; the architect moves code only when that is the task it was given.
- Installing a tool or adding it to CI is a proposal to the owner.
- After each item the edge check gets stricter; loosening it needs a record.

## Steps

1. **Current modules table.** One row per top-level module: its purpose in a few words; files and lines from the scan; its public entry (the file or package callers should import); edges out and in, with counts; the cycles it is part of; scan rows over code-structure's limits.
2. **Sort the dependencies** of each module that will move: plain code in the same process; code with a local stand-in for tests (a file store, an in-memory database); a service the team runs; a third-party service. The kind decides how the moved module is tested.
3. **Target layout:**
   - **feature modules**, one user-facing area or domain each, with one public entry and everything else internal;
   - **one shared home** for helpers, storage contracts and the UI kit, named once; code that many modules use goes there;
   - **entry wiring**: the start-up or app module is the only one that knows every feature, and it chooses which implementation of a contract runs (production, local, test);
   - **edge rules**: features do not import each other; when two must exchange something, the entry module or a shared module passes a plain id or value between them; nothing imports another module's internals; no cycles;
   - **size**: many tiny modules cost build time and boilerplate, a few huge ones bring the old tangle back. Two modules that keep reaching into each other are really one; two halves of a module that rarely talk can part. A codebase that will stay small may need no more modules than it has: say so and stop there.
4. **Migration items, in this order,** each one landing that keeps behaviour unchanged:
   1. **Safety net:** a structure test that finds every module from the repository root, so it survives the moves, and UI tests running in CI for UI code. Where tests do not pin behaviour, say so: the first follow-up is tests, plus a smoke run of the build, and no move starts before the owner accepts the risk in a record.
   2. **Edge check at today's state:** a rule in the project's boundary tool, or a test, that allows exactly the edges that exist now, so no new bad edge appears during the moves. Prove it fires once with a deliberate bad import, then remove that import. In a flat package the edge check begins with the first module moved out: from then on it allows only today's edges of that module.
   3. **Shared helpers and storage out** to the shared home, one group per item. They go before any feature because every feature leans on them: in a flat package the shared storage handle, the network and file helpers and the package-level state usually block every other move. Where many callers import the old path, leave a forwarding file there that only re-exports and holds no logic.
   4. **The least-coupled features**, fewest edges first.
   5. **The most-coupled features**, last.
   6. **Removal of each forwarding file** once nothing imports it, each as an item of its own, with the edge check tightened to match.
5. **Write each item** so a developer can do it without context: the files and modules moved; the edges it removes; its check (the build passes, the tests pass, code-structure's `--compare` against the baseline shows nothing worse except the move itself and any forwarding file not yet removed, the edge check passes); and how to undo it (revert this one landing).
6. **Record it.** The target layout and the edge rules go into a code-decision-record whose confirmation is the edge check; the item list is linked from it.

## Checks before hand-over

- The modules table covers every top-level module, with edges from a command that is shown.
- The target layout names the shared home and the entry module and states the edge rules.
- Items follow the order above; the safety net and the edge check come before any move.
- Every item names the files moved, the edges removed, its check and its undo.
- Every forwarding file has its own removal item.
- No item mixes structure with a feature or a fix.

## Artefacts

- A modules note, or the project's layout note: current table, target layout, edge rules.
- The migration items, one work item each, in order.
- The edge check (a tool rule or a test), proposed as the second item.
- The baseline file the plan was measured against, named in the plan.

## Hand-over

- **To the developers:** the items, in order, one at a time.
- **To the lead or owner:** the plan as a proposed record, any tool to install, and the risk where tests do not pin behaviour.
- **To the reviewer:** the edge check and the scan delta expected for each item; a landing that mixes in other work is sent back.

## Sources

No endorsement by these projects or their authors is implied.

Built on «Google Engineering Practices Documentation», «Small CLs» (github.com/google/eng-practices, commit 3bb3ec2; © Google, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), adapted.

Ideas only (no text taken): Android Developers docs: app modularization guide and common modularization patterns (Google LLC and the Android Open Source Project, Apache-2.0); mattpocock/skills, codebase-design (github.com/mattpocock/skills, commit 49dd158; Matt Pocock, MIT); agent-skills, deprecation and migration (github.com/addyosmani/agent-skills, commit aeac41d; Addy Osmani, MIT); superpowers, writing-plans (github.com/obra/superpowers, commit bb92a77; Jesse Vincent, MIT). Facts only (no text taken): command and tool names of go list, jdeps, dependency-cruiser, madge, import-linter, pydeps, ArchUnit, cargo-modules, deptrac and packwerk, as of October 2026.

General software-design practice from published books, described in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), except passages adapted from CC BY 3.0 sources, which stay under CC BY 3.0. The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
