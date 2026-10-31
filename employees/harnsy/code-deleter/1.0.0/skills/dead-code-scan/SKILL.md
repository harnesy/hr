---
name: dead-code-scan
description: Find code, files, exports, routes and dependencies that nothing uses, read-only - list every entry point (tests included), run the project's own unused-code tools, search each candidate by name and string, check declared dependencies nothing imports, check usage data if the owner provides it - and give each candidate its proof, a confidence level and the risk of removing it. Candidates, not verdicts. Use before any clean-up, after a large refactoring, or when a codebase feels heavier than its features.
---

# Dead code scan

Code that nothing runs still has to be read, built, upgraded and kept secure. But code that looks unused is not always unused: it may be called by name from configuration, from a template, from another language, or from outside the repository. This skill finds the candidates and gives each the evidence a reviewer needs, with an honest confidence level. It changes nothing.

**Route:** a repository at a commit → **dead-code-scan** → high-confidence candidates go to `safe-removal-pr` after the owner's OK → public interfaces to the owner for a deprecation decision → test-only code to the team as a coverage note.

## When to use

- Before a clean-up, or when a team asks «what here is still used?».
- After a large refactoring or a feature removal, when leftovers are likely.
- Periodically, on a rhythm the team agrees.
- Not to judge whether a feature that is used should be kept: that is the product owner's question.

## Inputs

- The repository at a stated commit, its build and test commands.
- The project's own analysis tools for unused code, if it has them.
- Usage data the owner can share: access logs for routes, analytics for pages, download counts for files, with the window they cover.

## Steps

1. **List the entry points:** main programs, initialisers, test entry points, scheduled jobs, command-line commands, plugins, handlers registered in configuration, templates, anything other languages call. Without the tests, library code looks dead.
2. **Run the project's own unused-code tool** if it has one, at the stated commit, and keep its output.
3. **Search each candidate by text:** its name, its string forms (as used in configuration, templates, reflection, routes and documentation), across the whole repository and any repositories the owner names.
4. **Ask why it is alive:** where a tool shows a call chain, read it before deciding; where an item has callers only from other candidates, mark the group together.
5. **Check dependencies:** packages declared in the manifest that no file imports; packages imported only by candidates.
6. **Check usage data** for routes, pages and files when the owner provides it, and state the window («no hits in the 90 days from 1 July to 28 September»).
7. **Rate each candidate:**
   - **high** — unreachable by the tool and no text hits outside its own file, and no usage in the data window where data exists;
   - **medium** — no static caller, but a dynamic call is possible (reflection, names built from strings, plugins, configuration);
   - **low** — only «looks unused», or reached only by tests.
8. **Name the removal risk** for each: public interface (others may call it), data it writes or reads, security or billing code, unknown owner.
9. **Write the report** and hand it over.

## Rules

- **Read-only.** No file, branch, configuration or flag is changed by this skill.
- **Candidates, not verdicts.** Every row is a candidate with proof; «unused» is never stated without evidence.
- **Test-only code is a coverage question.** It gets its own row and next step, not a removal.
- **Public interfaces wait for the owner.** They are listed with the risk, never proposed for removal on this skill's word.
- **The tools' blind spots are named** in the report: code called from outside the language, from configuration or from other repositories.

## Checks before hand-over

- The commit, the entry points and the tools used are stated.
- Every candidate has proof, a confidence level, a removal risk and an owner (or «unknown — ask»).
- The usage data window is stated wherever usage data was used.
- No file changed.

## Artefacts

- `cleanup/<date>-scan.md`: table of item, kind (file, function, export, route, dependency), proof, confidence, removal risk, owner, next step; the tools' blind spots.

## Hand-over

- **To `safe-removal-pr`:** high-confidence candidates the owner agrees to remove.
- **To the code owner:** public interfaces, for a deprecation decision; medium candidates that need the owner's knowledge.
- **To the team:** test-only code, as a coverage note.

## Sources

Built on The Go Blog, «Finding unreachable functions with deadcode» (The Go Authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: dead code as code no execution reaches, reachability from every entry point including tests, dynamic calls and code called from outside the language as blind spots, asking the tool why a function is alive, running the scan after refactoring. The reasoning is retold for any language; no tool's flags or output are reproduced.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
