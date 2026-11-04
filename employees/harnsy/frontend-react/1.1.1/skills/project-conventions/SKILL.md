---
name: project-conventions
description: Before the first change in a repository, learn its own rules and tools; read the readme, contributing notes, lint and format settings, CI setup, existing tests and commit history, detect the toolchain and its version, run the project's own format, lint and test commands once for a baseline, and write down what was found. Follow the existing patterns over personal taste. Use when starting work in any repository that is new to you, or after a long gap.
---

# Project conventions

Every repository already has answers to most style questions: how code is laid out, which checks must pass, how commits are written. Those answers live in files, in the CI setup and in the code itself. This skill finds them before anything is changed, records a baseline of what passes today, and makes the new work look like it was always part of the project.

**Route:** a task in a repository → **project-conventions** → a conventions note and a baseline check run → the change itself (often with tdd-slice) → the same checks again before hand-over.
Before this skill: access to the repository and the task. After it: a short note that the rest of the work follows, and a record of which checks were already failing.

## When to use

- The first task in a repository, or the first after a long break.
- When a build, lint or test failure looks unrelated to your change.
- Before proposing a new tool, dependency or pattern: check whether the project already has one.

## Inputs

- The repository, checked out at the branch the work starts from.
- The task, with any requirements, limits and interfaces it names.
- Any team rules the owner points to outside the repository (a wiki page, a style document).

## Rules

- The project's rules win over personal preference and over general style guides. Where a public style guide and the project disagree, follow the project and note the difference.
- Read before writing. No change, refactor or reformat happens before the conventions note exists.
- Do not install, upgrade or remove dependencies or tools to make checks run. If something is missing, say so and ask the owner.
- Do not reformat files you were not asked to touch. A formatter run limited to changed files is fine when the project does that itself.
- Use the toolchain version the project pins (version files, lock files, wrapper scripts, CI images). Advice that depends on a version starts by naming that version.
- A failure that exists before your change is recorded as baseline, not fixed silently and not hidden.

## Steps

1. **Read the top-level documents:** readme, contributing guide, review rules, architecture notes, changelog format, licence headers if the project uses them.
2. **Find the toolchain:** build files, lock files, version pins, wrapper scripts. Run `scripts/run_checks.py <repo>` to list what it detects and the commands it would use; compare that with what the readme and CI actually run, and trust the project's own files where they differ.
3. **Read the CI configuration:** which jobs run, in which order, with which flags. These are the checks a reviewer will expect to pass.
4. **Read the lint, format and compiler settings:** rule files, ignore lists, warning levels, editor settings. Note which rules are errors and which are warnings.
5. **Read existing tests:** where they live, how they are named, which helpers and fixtures exist, how slow and fast tests are split, how one test is run on its own.
6. **Read recent history:** commit message style, branch naming, how big a typical change is, whether changelog entries go with code.
7. **Read the neighbourhood of the change:** two or three files close to the one you will edit. Note naming, file layout, error handling, logging and dependency style. New code copies these.
8. **Get a baseline:** run the project's format check, lint and tests once, before any change (`scripts/run_checks.py <repo> --run`, or the commands the readme gives). Record each command and its result.
9. **Write the conventions note** (see Artefacts). Keep it short; it is a working reference, not documentation.
10. **Work, then check again:** after the change, run the same commands. Compare with the baseline; anything newly failing is yours to fix.

## Checks before hand-over

- The conventions note exists and names its sources (file paths).
- The toolchain version used matches the project's pin, or the difference is written down.
- Baseline and final check results are both recorded, command by command.
- No dependency or tool was installed or upgraded without the owner's OK.
- New code follows the patterns of its neighbours; any deliberate departure is explained.

## Artefacts

- `notes/conventions.md` (or the place the team keeps such notes): toolchain and version, commands for format, lint, test and build, rules that matter, test layout, commit style, open questions.
- The baseline run: each command, exit code, and the first lines of any failure.

## Hand-over

- **To the reviewer:** the conventions note with the change, and the before/after check results.
- **To the repository owner:** missing tools or dependencies, failing baseline checks, and gaps between the readme and CI.
- **To devops:** CI jobs that cannot run locally, or differ from the documented commands.

## Tools

`scripts/run_checks.py <dir>` (Python 3, standard library only) prints the detected toolchains, the evidence files, and the format, lint and test commands it would use. `--run` runs them one by one and reports each exit code with a summary; `--only format`, `--only lint` or `--only test` limits the run. It never installs anything and never uses the network on its own: when dependencies are missing (no installed packages, an unresolved bundle, an unconfigured build directory), it stops and says what is missing. The commands it runs are the project's own; read them before using `--run`.

## Per stack

- **iOS / Swift:** Swift packages run tests from the package; app projects test through a scheme and a simulator destination, listed by the build tool. Look for a SwiftLint or swift-format config, and for the minimum OS version and Swift language version in the project settings.
- **Android / Kotlin:** use the Gradle wrapper the project ships, never a system Gradle. Typical tasks: `lint` for Android Lint, `test` for local unit tests, `connectedAndroidTest` for tests on a device or emulator; ktlint, detekt or Spotless only if the build applies them. Check minimum and target SDK in the module build files.
- **Flutter / Dart:** `dart format`, `flutter analyze` with the rules in `analysis_options.yaml`, and `flutter test`. Note the Flutter channel and version the project pins.
- **React Native:** the package scripts are the source of truth (lint, type check, test). Native parts follow the iOS and Android notes above. Note the package manager from the lock file.
- **Ruby on Rails:** `bundle check` tells whether the bundle is installed; then the linter the Gemfile includes (RuboCop or Standard), and RSpec or Minitest, whichever the project uses. Migrations are versioned files run in order, and the schema file is the record of the current database shape; read it before touching models.
- **C and C++ (CMake, Make):** find the build directory and its options; tests usually run through CTest from a configured build. Note the compiler warning level and whether warnings fail the build. Note the C++ standard in use. Resource ownership through objects that release what they hold, and initialised variables, are common house rules; follow what the code already does.
- **Angular / TypeScript:** check the Angular version first (in the package file), because features and recommended patterns differ by version. Use the CLI generators the project already uses. The Angular style guide asks for one concept per file, names that say what a file holds, folders by feature, and simple templates, and it also says to keep a project's existing style when it differs.

## Sources

Built on Angular documentation, «Style guide» (angular/angular, commit 97e6aa4, adev/src/content/best-practices/style-guide.md; https://angular.dev/style-guide; © Google LLC, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on the «angular-developer» skill (github.com/angular/angular, commit 97e6aa4, skills/dev-skills/angular-developer; © 2026 Google LLC, MIT licence), adapted. Built on «Compiler Options Hardening Guide for C and C++» (github.com/ossf/wg-best-practices-os-developers, commit 8259081; © OpenSSF contributors, CC BY 4.0), adapted. Command names from the Android Developers documentation (Google LLC and the Android Open Source Project, Apache License 2.0), the Flutter documentation (github.com/flutter/website, commit 898d84d; © The Flutter Authors, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), the React Native documentation (github.com/facebook/react-native-website, commit b477b73; © Meta Platforms, Inc. and affiliates, CC BY 4.0), the Swift Testing documentation (github.com/swiftlang/swift-testing, commit f3cbdec; © Apple Inc. and the Swift project authors, Apache License 2.0) and the Clang documentation (github.com/llvm/llvm-project, commit 93c9c6b; LLVM Project contributors, Apache License 2.0 with LLVM Exceptions); changes were made. Portions of this page are modifications based on work created and shared by the Android Open Source Project and used according to terms described in the Creative Commons 2.5 Attribution License. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Ideas only (no text taken): Ruby on Rails Guides, «Active Record Migrations» (github.com/rails/rails, commit 736156e; Rails Core Team and contributors, CC BY-SA 4.0); C++ Core Guidelines (github.com/isocpp/CppCoreGuidelines, commit 33bcd01; Standard C++ Foundation and contributors).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
