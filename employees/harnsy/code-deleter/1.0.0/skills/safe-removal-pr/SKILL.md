---
name: safe-removal-pr
description: Remove one unused item in one pull request - the item and everything only it used, proof that nothing uses it, the full test suite and build green at the pull request's commit, the risk stated, and a one-line revert in the description - opened for review, never pushed to the main branch, public interfaces only with the owner's deprecation decision linked. Use for each candidate the owner agreed to remove after a scan or a flag review.
---

# Safe removal pull request

Removing code is a change like any other, and it should be as easy to review and as easy to undo. This skill turns one agreed candidate into one small pull request: the item goes, along with the helpers, types, tests and configuration that only it used; the description shows why it is safe, what was run, and how to bring it back with a single command.

**Route:** one agreed candidate with its proof → **safe-removal-pr** → the reviewer → the code owner merges → the release manager, if users could notice.

## When to use

- For each high-confidence candidate from `dead-code-scan` that the owner agreed to remove.
- For each flag the owner agreed to retire after `flag-retirement`.
- Not for replacing code that is still used: that is a migration, owned by whoever runs it.
- Not for public interfaces without the owner's deprecation decision and the end of its notice period.

## Inputs

- One candidate, its proof (the scan row or the flag row) and the owner's OK.
- The repository, its build and test commands.
- For a public interface: the deprecation decision and the notice end date.

## Steps

1. **Branch** from the current main branch; name the branch after the item.
2. **Remove the item** and everything only it used: helpers, types, tests of it, configuration keys, documentation lines, dependencies that only it imported. Search again for each of these before removing it.
3. **Keep the change to one logical item.** Anything else noticed on the way goes into a note, not into this pull request.
4. **Run the full test suite and the build** at the pull request's commit, and the linters the project uses. Record the command and the result.
5. **Write the description:**
   - **what is removed** — the item and the files touched;
   - **why it is safe** — the proof, with a link to the scan or flag row and the usage data window;
   - **tests** — the command, the result (passed, failed, skipped counts) and the commit;
   - **risk** — what could still depend on it and how that would show (an error in the logs, a failing outside call);
   - **revert** — one line: `git revert <commit>` once merged.
6. **Open the pull request** and request review from the code owner or the reviewer. Do not merge it.
7. **Answer review comments** with new commits on the same branch.

## Rules

- **One removal per pull request**, so each can be reviewed and reverted alone.
- **Never push to the main branch** and never merge; the code owner merges.
- **Tests green before review.** A red run is fixed or the pull request is closed with the reason.
- **Public interfaces only with a decision.** The deprecation decision and the end of the notice period are linked in the description, or the pull request is not opened.
- **No surprises in the diff.** Formatting, renames and unrelated fixes stay out.

## Checks before hand-over

- The diff touches one logical item and what only it used.
- Tests, build and linters pass at the pull request's commit; the command and result are in the description.
- The proof, the risk and the one-line revert are in the description.
- Public interfaces untouched, or the deprecation decision is linked.

## Artefacts

- The pull request, with its description.

## Hand-over

- **To the reviewer or the code owner:** the pull request for review; the owner merges.
- **To the release manager:** removals that users could notice, for the changelog.
- **To `dead-code-scan`:** anything the removal made unreachable, for the next scan.

## Sources

Built on the GOV.UK Service Manual, «Maintaining version control in coding» and «Retiring your service» (Government Digital Service, Crown copyright), adapted: small commits grouped by purpose, messages that say what changed and why, review by someone else, going back to any earlier version, telling users of an interface early and giving them lead time. Contains public sector information licensed under the Open Government Licence v3.0. Built on The Go Blog, «Finding unreachable functions with deadcode» (The Go Authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: removing a dead function together with the types only it used.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
