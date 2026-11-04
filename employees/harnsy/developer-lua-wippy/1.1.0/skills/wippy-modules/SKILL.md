---
name: wippy-modules
description: Lay out a Wippy app or module and manage what it depends on - index files and entries, dependency entries with a version range and the parameters that bind a module's requirements, the lock, local replacement while developing, and a module made ready for release without tagging it. Check the runtime build first, then follow the route the project uses - module registry plus lock, or git repository by tag plus lock. Use when adding, moving or replacing a dependency, creating a module, or when a change «did not land» in the app.
---

# Wippy modules and dependencies

A Wippy app is a set of registry entries plus the Lua files they point to. A module is the same thing packed for reuse: a manifest and a `src/` folder. Most module trouble is quiet: an edit that never reaches the app, a lock that moved under you, a requirement left without a value. This skill keeps one rule above the others: **check the runtime build first**, because what the resolver can do depends on it.

**Route:** a task that touches layout or dependencies → **wippy-modules** → wippy-processes or wippy-lua-testing for the code → reviewer.
Before this skill: the task, and read access to the repository. After it: the entries and the lock changed on purpose only, with the lock diff in the hand-over.

## When to use

- Adding a dependency, moving it to a newer version, or removing it.
- Developing a module against an app with a local replacement.
- Creating a module, or preparing one for release.
- A change that is in the files but not in the running app.

## Inputs

- The project's agent notes and readme, the manifest, every `_index.yaml`, `.wippy.yaml`, the lock.
- The runtime binary the project really uses (the Makefile, a variable, a script), not just the one on PATH.

## Steps

1. **Read before writing.** Note the namespace of each index file, the entry you will touch, and the version line of the runtime build the project uses. Find out where dependencies come from: a `component` of the form `org/module` is a module from the module registry; a `component` that names a repository host and path is a git source, and only some runtime builds resolve those.
   Check: you can say in one line «namespace X, build Y, dependencies from the registry / from git by tag / both». If the build does not resolve git sources, say so and stay on the registry route.
2. **Write the dependency entry.** One `ns.dependency` per module, a unique `name` in its namespace, `component`, a `version` range, and `parameters` that give a value to every `ns.requirement` the module declares (its database, its process host, its router, its user scope, as its own index file says).
   Check: the name appears once in the namespace; every requirement of the module has a value; the range is full semver (`^1.2.0`, `>=0.3.0`), never a fixed version taken over from the lock.
3. **Back up the lock, then resolve.** Copy the lock aside and run `wippy update`.
   Check: diff the lock against the copy. Only the rows you meant changed. A registry row carries a `hash`; a git row carries `source`, `commit` and `local_hash`, and its version matches the tag that points at that commit (`git tag --points-at <commit>` in the package's repository).
4. **Run tests and lint, then diff the lock again.** A run after a range change may resolve again and rewrite the lock.
   Check: the lock is byte-for-byte what step 3 left, or you know why it is not.
5. **Restart, then look.** A running instance keeps the code it started with; a new dependency loads at the next start.
   Check: the app answers with the new behaviour (wippy-lua-testing, last step), not only the files.
6. **Develop against a working copy, then take it out.** Point the module's name at the working copy (or at a repository plus branch or commit) under `workspace.replacements` in `.wippy.yaml`. Without the replacement, editing the working copy changes nothing in the app.
   Check while it is in: the app shows the working copy's behaviour. Before commit: the replacement is gone, `wippy update` ran, the lock diff is clean and each git row's version and commit agree.
7. **Prepare a release, do not make it.** Dependencies declare ranges; the manifest does not pin the next version; every folder the package must carry is listed for embedding; the project's verify target is green; `git status` shows only intended files.
   Check: hand the verify output and the lock diff to the release manager. You do not tag, push a tag or publish.

## Two ways to get modules

- **Module registry + lock.** `wippy update` picks the highest registry version inside the range and writes it with its hash to the lock. `wippy install` and the boot install what the lock says.
- **Git repository by tag + lock** (only on builds that resolve git sources; the output of `wippy update` shows whether yours does). The candidates are the repository's tags that read as semver, with or without a leading `v`; the highest match inside the range wins; a branch is never a version. The lock records the commit, so install and boot need no tags and work offline once the commit is cached. Packages often come from GitHub this way. A tag that moved upstream is picked up only by the next `wippy update`.

## Rules (each with its check)

- **Ranges in the source, exact versions only in the lock.** Check: no dependency entry holds a version that only the lock should hold; `wippy update` accepts every range.
- **A run can move the lock.** Back up and diff the lock around `update`, and around `test` or `run` after any range change. Check: the diff is in the hand-over.
- **Version and commit agree in every git row,** above all after a replacement was used. Check: the tag that points at the row's commit names the row's version; if not, remove the replacement and resolve again.
- **A working copy is not the app.** Check: the behaviour of the running app, the lock row and a clean `.wippy.yaml`, before saying a change landed.
- **No `file://` in a dependency source.** It can be taken for a file include and fail the resolve. Use the form the project's other entries use. Check: `wippy update` succeeds and the lock row shows the source you meant.
- **Entry names are unique in a namespace.** A duplicate is taken quietly and the other module's requirements go unbound. Check: search the index file for the name; read the start-up log for a duplicate warning.
- **Quote YAML comments that contain «: ».** One such comment can break the parse of the whole index file and the boot with it. Check: lint of the namespace passes and the app boots.
- **One instance per port.** A second instance on a busy port dies quietly. Check: the port is free before the start, and the old process is gone (wait for the pid and the port, not a fixed sleep; a stop can take about 20 seconds).

## Checks before hand-over

- The lock diff shows only intended rows; registry rows have hashes, git rows have source, commit and tree hash, and versions match commits.
- No replacement left in `.wippy.yaml`; no exact version in a dependency entry.
- Tests, lint and the running app checked after the last change.

## Artefacts

- The changed index files, `.wippy.yaml` if it changed for good, and the lock when the project commits it.
- The lock diff and the commands that ran.

## Hand-over

- **To the reviewer:** the change, the lock diff, the test and lint output, the live answer.
- **To the release manager:** a module ready for release, with the verify output; the owner decides on the tag.
- **To the software architect:** a question about which module should own a feature, or a split or merge of modules.
- **To the Go developer:** resolver or loader behaviour that looks wrong, with a small repeatable case and the lock diff.

## Sources

This employee is a harnsy product, not an official product of these projects.

Built on Chicago app, «CLAUDE.md» and the skill «chicago-add-module» (github.com/chicago-desktop/app, commit 225e926; © 2026 Wippy, MIT), adapted. Built on Chicago module-template, «AGENTS.md», «README.md» and the test harness (github.com/chicago-desktop/module-template, commit 4c86d76; © 2026 Wippy, MIT), adapted. Facts only, no text taken: Wippy documentation (github.com/wippyai/docs, commit b05b548; MPL-2.0) and the Wippy runtime and its git-sources fork (github.com/wippyai/runtime, commit 4137a00; github.com/chicago-desktop/runtime, commit 7bcb546; MPL-2.0). Facts checked in our own trial on two runtime builds, 2026-10-21.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
