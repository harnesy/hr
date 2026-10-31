---
name: patch-series-review
description: Review a series of commits (a pull request or a set of patches) commit by commit - the order, one logical change per commit, every commit building and passing tests, the content checks, the commit messages - and write findings as file:line, problem, exact ask and blocking or suggestion, ending in one verdict - ready to merge, changes requested (n blocking) or declined with the reason. Use on every incoming series in a long-lived codebase before anyone merges it.
---

# Patch series review

A series is read in order, one commit at a time, because that is how the history will be read later: by someone looking for the change that broke something, or for why a line exists. This skill checks that each step is one logical change, that each one builds and passes on its own, and that the series as a whole keeps the promises the codebase makes to its existing users. Every finding names the place and the exact change asked for; nothing in a review is about the person who wrote the code.

**Route:** a pull request or a series from a contributor → **patch-series-review** (with `commit-message-check` on the messages) → findings to the contributor → a new round as separate commits → ready series to the person who merges and to the release manager.

## When to use

- On every incoming series or pull request, before anyone merges it.
- On a new round of an earlier series: review what changed since the last round.
- Not for a single commit inside a product team's daily flow (the reviewer's work), and not for licence questions (the open source licence specialist's).

## Inputs

- The series (branch, pull request or patch files) and its description.
- The linked issue, if any, and the project's written contributing rules.
- The build and test commands, and CI results per commit if the project has them.

## Steps

1. **Read the description and the linked issue.** Write in one line what the series is for. Form your verdict before reading other reviewers' comments.
2. **Check the order:** each commit depends only on the ones before it. Would another order make each step smaller or safer? Say which.
3. **One logical change per commit:** flag commits that mix refactoring with behaviour changes, formatting with logic, or carry unrelated edits. Give the exact split, for example «move the rename in `api/client.py` into its own commit before this one».
4. **Every commit builds and passes:** check out each commit, build it and run the tests (or read the per-commit CI result). Record pass or fail per commit id. A series where only the last commit passes is not ready.
5. **Content checks,** per commit and for the whole:
   - one goal, no scope creep; merges cleanly on the current main line;
   - new code has tests next to it, and changed behaviour has changed tests;
   - documentation and changelog updated where users would notice;
   - placeholder or temporary code is flagged as such;
   - nothing duplicates what already exists in the codebase;
   - edge cases are covered: empty input, limits, errors;
   - the public interface is unchanged, or the change is declared with a migration path for existing users.
6. **Messages:** run `commit-message-check` on the series and add its flags to the findings.
7. **Write the findings,** one per point: `file:line` — the problem — the exact ask — **blocking** or **suggestion**. A style point that is not in the written rules is a suggestion.
8. **Give the verdict:** «ready to merge», «changes requested (n blocking)», or «declined» with the reason and a link to the written rule. Ask for the next round as separate commits on top, so each answer can be seen; they are squashed only when the series is ready.
9. **On a new round:** check each earlier finding against its answer, and review only what changed.

## Rules

- **About the change, never the person.** No sarcasm, no exaggeration, no capitals for emphasis. Thank the contributor for the work.
- **Every finding is exact.** File, line, the problem and the change asked for.
- **Existing users are protected.** A change that alters a public interface or behaviour without a migration path is blocking.
- **Same standard for everyone,** stated in the written rules; facts and data count more than preference.
- **No merge, no push, no rewritten history.** The merge is the person's; fixes are asked of the contributor.

## Checks before hand-over

- Every commit has a recorded build and test result.
- Every finding has file:line, problem, exact ask and blocking or suggestion.
- Public interface changes are found and marked.
- The verdict is one of the three, with the count of blocking findings.

## Artefacts

- The review on the pull request or series: the one-line purpose, the per-commit results table, the findings, the verdict.

## Hand-over

- **To the contributor:** the findings and the verdict.
- **To the person who merges:** a series marked ready, with its per-commit results.
- **To the release manager:** ready series that change public interfaces or need a changelog entry.

## Sources

Built on 18F Guides, code review and workflow (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: one goal per change, merges cleanly, tests and docs with new code, placeholders flagged, no duplicated functionality, feedback as separate commits until ready, CI before merge. Built on Open Source Guides, «Best practices for maintainers» (Open Source Guides authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: tests on every incoming contribution, written rules. Content based on github.com/github/opensource.guide used under the CC-BY-4.0 license.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
