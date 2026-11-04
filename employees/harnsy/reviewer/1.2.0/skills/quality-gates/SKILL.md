---
name: quality-gates
description: After the last green slice and before submit, measure the changed code with three gates (CRAP score, structural duplication, mutation testing), fix or explain every finding, and put the numbers and an action log in the hand-over. A gate that cannot run for the language or the project is reported as «not measured», never as «passed». Tools run from a pinned clone outside the project; languages Go, Python, TypeScript and JavaScript, Rust, Java.
---

# Quality gates

A green test suite says the tests pass; it does not say they would notice a wrong answer, or that the code is easy to change. This skill adds three numbers that do: how risky each changed function is (complexity against coverage), whether the change repeats code that already exists, and whether the tests fail when the code is deliberately broken. Each finding is fixed or gets a one-line reason, and the numbers go into the hand-over so the reviewer does not have to trust words.

**Route:** tdd-slice, repeated per behaviour → code-structure compare → **quality-gates** on the branch's changed files → hand-over with the gate table and the action log.
Before this skill: the full test suite green and the work committed per slice. After it: every gate measured or marked «not measured» with the reason.

This skill does not repeat the other two. Test-first, the slice loop and the smallest passing change live in tdd-slice (when it is installed). File, function and folder sizes, and where shared code belongs, live in code-structure. Its scan's duplicate hint is a hint; here the duplication gate is dryer.

## When to use

- A change to source code is ready for review: after the last green slice, before submit.
- Reviewing someone else's change: run the gates on that change's files and report the numbers; the author fixes.
- Turning surviving mutants into behaviour tests, or checking that new characterization tests really pin the code.

## Make it work

These come on top of tdd-slice and apply while the code is being written. They keep the gate findings small.

- **Shape the data first.** Settle the types and structures the change works on before writing logic over them; most later complexity comes from a shape chosen in a hurry.
- **Take something out before adding something.** Look for a branch, a flag or a helper the change makes unnecessary, and remove it in the same piece of work.
- **Redesign instead of bolting on.** When a new requirement does not fit, sketch the design you would have made had it been known from the start, then reach that design in small proven steps. A special case glued to the side is how CRAP scores grow.
- **Drop the shared assumption.** If a second fix built on one belief has failed like the first, state that belief in one sentence and discard it before a third attempt.
- **Check outside data where it enters.** Parse it once, at the edge, into a type the rest of the code can trust; keep business rules in pure functions that take values and return values, so they are easy to test and to mutate.
- **Make illegal states impossible to write.** Prefer types that cannot hold a wrong value. Never silence the compiler or the type checker (`any`, `# type: ignore`, `//nolint`, `@SuppressWarnings`, `unsafe`) to make the build pass; when it is truly needed, write the reason on the same line.
- **Make operations idempotent.** Running an operation twice, or once more after it died midway, must end in the same state.
- **Do not share what does not need sharing.** Give each user of mutable state its own copy. When they must share it, allow one writer and make the structure enforce it (one owner goroutine or task, one type that holds the lock).

## Make it right

- **Fix the cause, not the symptom.** Reproduce the fault, then change what produces it. A catch that swallows the error or a nil check around the crash site is not a fix.
- **Tests check behaviour.** Each test drives the code through the entry point its caller uses and asserts on the result that caller gets. A test that would still pass if every function returned nothing, zero or an empty list is deleted or rewritten; the mutation gate is how you find them.
- **Refactor in three moves:** lock down today's behaviour with tests (characterization tests for old code), change the structure, show that the same tests pass. No behaviour change in the same commit.

## Gates

### Tool setup, once per machine

The gates use three open-source command-line tools (authors and licences in Sources below): crapper (CRAP score), dryer (duplication) and mutator (mutation testing). They are not carried in this bundle. Ask the owner once per machine before installing them, and keep them in one tools folder outside every project, side by side, because mutator loads crapper from the folder next to it.

```sh
Q=~/.local/share/quality-gate-tools      # any folder outside the project
git clone https://github.com/unclebob/crapper "$Q/crapper" && git -C "$Q/crapper" checkout 6fd92c4c9bcc56efb64a2f8743d5a2993bcfd42d
git clone https://github.com/unclebob/dryer   "$Q/dryer"   && git -C "$Q/dryer"   checkout 66ff6d21a42c04afcad89c78a80066176d1294b0
git clone https://github.com/unclebob/mutator "$Q/mutator" && git -C "$Q/mutator" checkout a5a0cb803b66e0cdb8bf471b3b08af701d424a41
```

- Needs git and Python 3.11 or newer. The first run of each tool creates a `.venv` inside its own clone and installs its parsers from the network.
- Those parser packages are not pinned by the tools. Record once per machine, in the connection note or the first hand-over: each tool's commit (`git -C "$Q/crapper" rev-parse HEAD`, and the same for dryer and mutator) and its packages (`"$Q/crapper/.venv/bin/pip" freeze`, and the same for the other two).
- On a shared machine, run each gate through the machine's wrapper for heavy jobs if it has one; mutation runs the test suite many times.

### Before the first run in a project

The tools measure coverage with the project's own test runner, and may install what is missing into the project. Tell the owner what will land and get the OK first.

- **Python:** the project's `.venv` or `venv` gets `coverage`, and `pytest` when the project uses pytest. No project virtual environment: stop and ask. Never let the tools install into the system or user Python.
- **TypeScript with Vitest:** `@vitest/coverage-v8` at the project's Vitest version goes into `node_modules`; `package.json` and the lock file stay as they were. A `coverage` script in `package.json` is used as it is, and other test runners are wrapped in `npx c8` (read from the README, not tried).
- **Go:** nothing is installed; coverage comes from `go test`.
- **Rust:** with neither `cargo-llvm-cov` nor `cargo-tarpaulin` on the PATH, crapper installs `cargo-llvm-cov` and the `llvm-tools-preview` component into the user's toolchain, which changes the machine, not the project (read from the README, not tried). Only with the owner's explicit OK for that install.
- **Java:** needs Maven; coverage is the JaCoCo Maven plugin 0.8.12 and the mutation test command is `mvn -q test` (read from the README, not tried). Gradle projects: CRAP and mutation are «not measured».
- **Every language:** the run writes `.metrics/` and `target/coverage/` into the project root, and mutator leaves `target/mutation-workers/`. Save the output of `git status --short` before the first run and take it again after. A file that was clean before and changed after is put back with `git restore <file>`, and each one is named in the report. A file that already had changes before the run is never touched, even if the tools changed it too: name it to the owner. Do not edit `.gitignore` or `package.json` to hide the leftovers unless the owner asks.

### Which files

The tools' `--changed` flag reads `git status`: uncommitted and untracked files only. After per-slice commits it prints «No source files to analyze.» and exits 0, which looks like a pass and measured nothing. Use `--changed` only for work that is not committed yet. For a branch, list the files it added or modified against the main line, without tests:

```sh
BASE=$(git merge-base HEAD <main branch>)
F=$(git diff --name-only --diff-filter=AM "$BASE" HEAD \
  | grep -E '\.(py|go|ts|tsx|js|jsx|mjs|cjs|rs|java)$' \
  | grep -vE '(^|/)(test|tests|spec|__tests__)/|_test\.(go|py)$|\.(test|spec)\.[cm]?[jt]sx?$|(^|/)test_[^/]*\.py$|Tests?\.java$')
echo "$F"
```

- An empty list stops the gates with «nothing to measure». It is never a pass, and the tools are never run without paths: with no paths they walk the whole tree, and mutator then runs every mutant in it.
- Test files never go on the command line: a named test file is scored like production code.
- Show the list in the hand-over. Paths with spaces break the unquoted `$F` below; name such files one by one.

Run every gate from the project root.

### Gate 1: CRAP below 10

```sh
"$Q/crapper/crapper" --threshold 9.9 $F
```

- Exit 2 with `CRAP threshold exceeded: <worst> > 9.9` means a function scores 10 or more. Scores are decimals, so 9.9 is how «below 10» is written.
- For each such function: add behaviour tests, split it, or both. A flat `switch` or `match` that only maps values may stay, with a one-line reason.
- «Not measured», never «passed»: a run with `--no-coverage` (no score, exit 0 whatever the complexity), and a run where coverage is 0 % across the board because the coverage tool or the build is missing. Write which one and why.

### Gate 2: no duplicate at 0.8 or above

```sh
"$Q/dryer/dryer" --threshold 0.8 $F
```

- dryer exits 0 even when it finds duplicates. The gate reads the output: every line that starts with `DUPLICATE score=` is a finding, followed by the two `file:start-end` ranges.
- For each pair: merge the two into one place (code-structure says where shared code lives), or write a one-line reason why the two must stay different.
- Installs nothing into the project.

### Gate 3: mutation, no survivor

```sh
"$Q/mutator/mutator" $F
```

- Exit 3 means at least one `SURVIVED` line: the code was changed (`>=` to `>`, `and` to `or`, `0` to `1`) and every test still passed. Exit 0 means every mutant that ran was killed. Exit 2 means the tests fail before any mutation (read from the README, not tried).
- Exit 0 is not the whole answer. Lines that no test reaches are printed as `UNCOVERED` and are not run at all, and they do not change the exit code. The gate reads the output: no `SURVIVED` line, and every `UNCOVERED` line in a changed function has a test, is deleted as dead code, or has a one-line reason.
- Work in this order: cover what is uncovered; kill each survivor with a test of visible behaviour (for `>=` turned into `>`, a test exactly at the boundary value); delete code that no behaviour needs. Run again until the gate holds.
- On a large file start with that file alone. Later runs only repeat survivors and changed functions (read from the README, not tried).

### Per language

| Language | CRAP | Duplication | Mutation |
| --- | --- | --- | --- |
| Python, project virtual environment, pytest | as above | as above | as above |
| TypeScript, Vitest | as above | as above | as above |
| Go | as above | as above | as above, with the folder condition below |
| Rust | only after the owner's OK for the coverage install (read from the README, not tried); else «not measured» | as above | only after the same OK (read from the README, not tried); else «not measured» |
| Java, Maven | as above (read from the README, not tried) | as above | as above (read from the README, not tried) |
| Java, Gradle | «not measured» | as above | «not measured» |
| JavaScript, other TypeScript test runners | as above (read from the README, not tried) | as above | as above (read from the README, not tried) |

- **Go:** mutator joins coverage to files only when the project folder's path ends with the module path from `go.mod` (for `module example.com/shop`, a folder named `…/example.com/shop`). Otherwise it prints «No coverage data for <file>», marks every site `UNCOVERED` and exits 0. Then run `"$Q/mutator/mutator" --no-coverage <file>` on the changed files and say so in the hand-over (it also mutates functions no test reaches, so expect survivors there), or report mutation as «not measured». Never move or rename the person's repository to satisfy the tool.
- **Rust without the OK:** dryer still runs. A `mutator --no-coverage` run may be shown as extra information, labelled as such; the CRAP and mutation gates stay «not measured».
- A language the tools do not cover is «not measured» for all three gates.

### Reading and reporting

Put a table in the hand-over, one row per gate:

| Gate | Command | Exit | Result |
| --- | --- | --- | --- |
| CRAP | the command with its file list | 0 or 2 | worst score and function; each function at 10 or more with its fix or reason |
| Duplication | … | 0 | number of `DUPLICATE` pairs; each one merged or with its reason |
| Mutation | … | 0, 2 or 3 | killed, survived and uncovered for the changed functions; each survivor and uncovered line handled |

- A gate that could not run is a row too: «not measured: <why>» (no tool for the language, no Maven, no OK for the Rust install, the Go folder condition, an empty file list reported as «nothing to measure»). Never «passed», never left out.
- Exit codes alone decide nothing: dryer's exit 0 and mutator's exit 0 both allow findings in the output.

## Practice

- **Keep an action log.** One line per action: what was done, for which finding, and why. It goes into the hand-over with the gate table.
- **Commit small and in order.** Each message gives the reason, the change and the proof; for gate work, the numbers before and after.
- **Clean up only what is shown to be unused:** worktrees, branches, build output, and the gates' own leftovers. Uncommitted work is left for the owner to decide.
- **Leave the project as you found it,** apart from the change. List what the gates left (`.metrics/`, `target/coverage/`, `target/mutation-workers/`, `target/site/jacoco/` for Java, coverage packages installed into the project's environment or `node_modules`) and offer to remove it.

## Checks before hand-over

- The file list came from the branch diff against the merge base (or `--changed` for uncommitted work only), without tests, and it is shown. An empty list is reported as «nothing to measure».
- CRAP: every changed function below 10, or each exception with its reason.
- Duplication: no `DUPLICATE` line without a merge or a reason.
- Mutation: no `SURVIVED` line; every `UNCOVERED` line in a changed function handled.
- Every gate that did not run says «not measured» and why; `--no-coverage` and 0 % coverage are counted as «not measured» for CRAP.
- Installs into the project were agreed, and they are listed with the leftovers.
- `git status --short` was taken before and after the first run: files clean before and changed after were restored and named; files already dirty before were left alone and named to the owner.
- The tool commits and packages are recorded for this machine.

## Artefacts

- The gate table, with the commands and their file list.
- The action log.
- The list of installs and leftovers, with the offer to remove them.
- Once per machine: the tool commits and their package lists.

## Hand-over

- **To the reviewer or the requester:** the change with the gate table and the action log.
- **When this skill is used in a review:** the gate table goes to the author as findings; the reviewer does not fix them.
- **To the owner:** the leftovers and the installs, the Rust coverage install or a Gradle project when a gate stays «not measured», and any change the tools made to a tracked file.

## Sources

No endorsement by these projects or their authors is implied. This employee is a harnsy product, not an official product of these projects.

Ideas only (no text taken): «ub-mode» by Robert C. Martin (https://github.com/unclebob/ub-mode/tree/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f; no licence), which names rules by poteto as its loose basis (no licence found; https://github.com/poteto). Described in our own words.

Run, not carried (no code or text in this bundle; the commands and exit codes are facts about the tools): crapper (https://github.com/unclebob/crapper/tree/6fd92c4c9bcc56efb64a2f8743d5a2993bcfd42d), dryer (https://github.com/unclebob/dryer/tree/66ff6d21a42c04afcad89c78a80066176d1294b0) and mutator (https://github.com/unclebob/mutator/tree/a5a0cb803b66e0cdb8bf471b3b08af701d424a41); © 2026 Robert C. Martin, 0BSD.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. No scripts are carried with this skill.
