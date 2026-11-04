---
name: gate-rollout
description: Bring one module or service that is hard to change under the three quality gates and keep them running - a baseline measured on the main line, the module improved in small proven commits, a CI job that gates only the changed files, and a ratchet that only ever tightens. CI files are edited only with the owner's OK. Use when a team wants the gates to stay after the work is done, not only for one change.
---

# Gate rollout

quality-gates measures one change. This skill puts a whole module under the same three gates and leaves them in the project's CI, so the module does not slide back once the work is handed over. It starts from numbers measured on the main line, improves the module step by step, and then turns the gates on for every later change.

**Route:** pick the scope → baseline on the main line → bring the module under the gates → CI gate on changed files → ratchet → hand over.
Before this skill: the owner named the module and agreed to the tool setup in quality-gates. After it: a before/after table, the CI change (merged by the owner or left as a proposal), and the action log.

This skill uses quality-gates for the commands, the file list rules, the install rules and «not measured», and characterization-tests for pinning behaviour. It does not repeat them.

## When to use

- A module or service is hard to change: bugs come back, nobody wants to touch it, tests pass and still miss breakages.
- A team asks to keep the gates after a clean-up, so new changes cannot make the module worse.
- Not for one change ready for review (quality-gates alone), not for replacing a system piece by piece (that is the legacy modernizer's work), not for removing unused code at scale (the code deleter's).

## 1. Pick the scope

- One module or one service, named by the owner. Write its folder and its language. A language the tools do not cover gets all three gates «not measured», and the rollout stops at this step with that report.
- List its source files the same way quality-gates lists a branch, but from the tree instead of a diff, and without tests:

```sh
M=<module folder>
F=$(git ls-files "$M" \
  | grep -E '\.(py|go|ts|tsx|js|jsx|mjs|cjs|rs|java)$' \
  | grep -vE '(^|/)(test|tests|spec|__tests__)/|_test\.(go|py)$|\.(test|spec)\.[cm]?[jt]sx?$|(^|/)test_[^/]*\.py$|Tests?\.java$')
```

- Count the files and the functions (crapper's table has one row per function). Mutation over a whole module runs the test suite once per mutation site: tell the owner the size and the expected run time before the first mutation run, and agree on the order of files (worst CRAP first).

## 2. Baseline on the main line

Measure the module as it is on the main line before changing anything, so every later number has something to compare with.

- Work in a separate worktree at the main line's head, in a folder outside the project, so the person's working tree is not touched: `git worktree add <folder outside the project> <main branch>`. Remove it when the baseline is written.
- CRAP: `"$Q/crapper/crapper" $F` with no threshold. The table on stdout is sorted worst first; keep the ten worst rows (function, namespace, CC, coverage, CRAP) and the count of functions at 10 or more.
- Duplication: `"$Q/dryer/dryer" --threshold 0.8 $F`. Keep the count of `DUPLICATE score=` lines and each pair's two ranges.
- Mutation: `"$Q/mutator/mutator" <file>` file by file in the agreed order. Keep each file's `Total` row: killed, survived, uncovered, sites, score. The score is killed / (killed + survived); uncovered sites are not in it, so report them next to it.
- The gaps are part of the baseline: «not measured» rows (and why) go in with the numbers.
- Write the baseline as a short table with the main line's commit, the date and the tool commits. Keep it in the hand-over. A copy in the repository (for example `docs/quality-baseline.md`) only with the owner's OK.

## 3. Bring the module under the gates

Work in the order the baseline gives: the worst CRAP functions and the files with survivors first. Each step is one small commit on a branch, with the numbers before and after in its message.

1. **Pin before touching.** Before a refactor, the function's current behaviour is pinned with characterization-tests, oddities included. No behaviour change in the same commit.
2. **Cover, then split.** For a function at CRAP 10 or more, add behaviour tests first (the score falls as coverage rises); split it only if the complexity itself stays too high. A flat value map may stay with a one-line reason.
3. **Kill survivors.** Each `SURVIVED` line gets a test of visible behaviour that fails on that mutation. Each `UNCOVERED` line in a function the work touched gets a test, or is deleted as code no behaviour needs, or gets a reason.
4. **Merge duplicates.** Each `DUPLICATE` pair is merged into one place, the module's existing home for shared code (when it has none, propose one to the owner before creating it), or gets a one-line reason why the two must differ.
5. **Delete dead code** only when it is shown to be unused within the module. Removals that reach public interfaces, other services or feature flags go to the code deleter with the evidence.
6. Rerun the gates on the files the commit changed (quality-gates, branch file list). The step is done when they hold.

Stop and ask the owner when a step needs a behaviour change, when the tests are too slow for mutation to finish in an agreed time, or when a pinned oddity looks like a bug. A bug found here is reported, not fixed silently inside a refactor.

## 4. CI gate on changed files

The gate in CI checks only the files a pull request adds or modifies, so an old module can be gated before it is clean. The CI file belongs to the owner: write the change as a proposal first, and edit it only after the owner's OK.

The proposal says:

- which job is added and where, and which pull requests it runs on;
- what it installs on the CI runner (git, Python 3.11 or newer, the three tools at their pinned commits, and the coverage packages quality-gates lists for the language);
- how long it adds to a run, measured on one real pull request locally;
- what fails the job, and what only shows in its log;
- how to turn it off (remove the job, or one line that skips it).

The job's steps, as a plain shell script the CI calls (written from the tools' READMEs and the commands tried in quality-gates; the CI job itself is not tried, so run it once on a draft pull request before relying on it):

```sh
set -u
Q=<folder where the three tools were cloned at their pinned commits, as in quality-gates>
BASE=$(git merge-base HEAD origin/<main branch>)   # the CI checkout needs the main line's history, not a shallow clone
F=$(git diff --name-only --diff-filter=AM "$BASE" HEAD -- <module folder> \
  | grep -E '\.(py|go|ts|tsx|js|jsx|mjs|cjs|rs|java)$' \
  | grep -vE '(^|/)(test|tests|spec|__tests__)/|_test\.(go|py)$|\.(test|spec)\.[cm]?[jt]sx?$|(^|/)test_[^/]*\.py$|Tests?\.java$')
if [ -z "$F" ]; then echo "quality gates: nothing to measure (skipped, not passed)"; exit 0; fi
fail=0
"$Q/crapper/crapper" --threshold 9.9 $F || fail=1
"$Q/dryer/dryer" --threshold 0.8 $F | tee dryer.out
grep -q '^DUPLICATE score=' dryer.out && fail=1
"$Q/mutator/mutator" $F | tee mutator.out
grep -q '^SURVIVED' mutator.out && fail=1
grep -c '^UNCOVERED' mutator.out || true
exit $fail
```

- A pull request with no source files in the module prints «nothing to measure» and does not run the gates. The log says skipped; the job's green mark there means «nothing to check», and the hand-over says so.
- dryer's and mutator's exit codes do not decide alone: the script reads their output, as quality-gates does by hand.
- Exceptions (a flat value map over 10, two pieces that must stay different) are listed in a file in the repository, one line each with the function or range and the reason, and changed only through a reviewed pull request. Until the job reads that file, an exception is approved in the pull request by the owner. (Not tried.)
- `UNCOVERED` lines are counted in the log but do not fail the job at first. Making them fail is a ratchet step.

## 5. Ratchet

The gates only get stricter. Each step is the owner's decision, written down with its date.

- **Wider scope:** from the changed files of one module, to the whole module once its baseline is clean, to the next module.
- **Stricter rules:** `UNCOVERED` lines in changed functions fail the job; the exception list only shrinks.
- **Never looser:** a threshold is not raised and a gate is not switched off to let one pull request through. The way out of a red job is a fix, an exception the owner approved, or the owner's written decision to pause the job.
- Rerun the baseline after each step and keep the old one next to the new one, so the trend shows.

## 6. Hand the gates to the team

- A short practice session on the team's own code: one survivor from the report, the team writes the test that kills it, the gate turns green. Twenty to thirty minutes, one example, no slides.
- A one-page note in the hand-over: what each gate measures, what fails the job, where the exceptions live, how to run the gates locally (quality-gates), and who decides on the ratchet.

## Checks before hand-over

- The scope, its file list and the language are written down; uncovered languages are «not measured».
- The baseline was measured on the main line in a separate worktree, with the commit, the date and the tool commits; the worktree is removed.
- Every improvement commit is small, has characterization tests before the refactor, and gives the numbers before and after.
- The before/after table has the same rows as the baseline.
- The CI change was shown to the owner before any edit; the CI file was changed only after the OK, and the job ran once on a draft pull request, or the change is handed over as a proposal marked not tried.
- Nothing was loosened to make a run pass.

## Artefacts

- The baseline table and the after table: the ten worst CRAP functions, functions at 10 or more, `DUPLICATE` pairs, mutation killed / survived / uncovered / score per file, «not measured» rows.
- The CI proposal, and the CI change with its first run's result when the owner agreed.
- The exception list, each line with its reason.
- The action log: one line per action, what and why.
- The ratchet plan: the next steps and who decides them.

## Hand-over

- **To the owner:** the before/after table, the CI change or proposal, the exception list, the ratchet plan, and the gates' leftovers and installs from quality-gates.
- **To the reviewer:** each improvement commit with its numbers.
- **To the code deleter:** removals beyond the module, with the evidence.
- **To the legacy modernizer:** a module the gates show is cheaper to replace than to repair, with the numbers.

## Sources

No endorsement by these projects or their authors is implied. This employee is a harnsy product, not an official product of these projects.

Run, not carried (no code or text in this bundle; the commands, output lines and exit codes are facts about the tools): crapper (https://github.com/unclebob/crapper/tree/6fd92c4c9bcc56efb64a2f8743d5a2993bcfd42d), dryer (https://github.com/unclebob/dryer/tree/66ff6d21a42c04afcad89c78a80066176d1294b0) and mutator (https://github.com/unclebob/mutator/tree/a5a0cb803b66e0cdb8bf471b3b08af701d424a41); © 2026 Robert C. Martin, 0BSD.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. No scripts are carried with this skill.
