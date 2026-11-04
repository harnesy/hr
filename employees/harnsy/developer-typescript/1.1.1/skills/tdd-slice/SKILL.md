---
name: tdd-slice
description: Build or fix one small behaviour at a time with test-driven development; write a test for it, run it and see it fail for the expected reason, write the least code that makes it pass, tidy up while every test stays green, commit, and take the next slice. A bug fix starts with a test that reproduces the bug. Never report work as done without a passing run of the project's whole test command shown. Use for new features, bug fixes and behaviour changes in any language.
---

# Test-driven slice

A test that has never failed has not shown that it can catch anything. This skill works in thin slices: pick one behaviour, prove with a failing test that it is missing, add just enough code to make it present, clean up, and only then move on. Each slice ends with a green run and a small commit, so the work can stop or be reviewed at any point.

**Route:** a task or a bug → project-conventions (if the repository is new) → **tdd-slice**, repeated per behaviour → the whole test suite green → hand-over to the reviewer.
Before this skill: the task broken into behaviours, and the project's test command known. After it: small commits, each with its test, and a recorded passing run.

## When to use

- New features, bug fixes, refactoring that changes behaviour, and any change where a wrong result would matter.
- Exceptions only with the person's OK, recorded in the hand-over: a prototype that will be thrown away, generated code, pure configuration.

## Inputs

- The behaviours to build, as a short list, smallest and most certain first.
- The project's test command, and how to run a single test (from the project-conventions note; that skill's `run_checks.py` finds the command).
- For a bug: the report and the steps to reproduce it.

## Rules

- Production code comes after a failing test for it, never before. Code written ahead of its test is discarded and rewritten from the test, not patched up to fit.
- Watch every new test fail, and read the failure. It must fail because the behaviour is missing, not because of a typo, a missing import or a broken fixture.
- In the passing step write only what this test needs. No extra options, no speculative generality, no unrelated clean-up.
- Tidy up only while everything is green, and run the tests after each tidy-up step. Tidying never adds behaviour.
- One behaviour per test, with a name that says what should happen. Prefer real code to mocks; mock only what is slow, external or nondeterministic.
- A bug fix begins with a test that reproduces the bug and fails.
- «Done» needs evidence: a run of the project's full test command after the last change, with its output. A green single file is not a green suite. Any failure in that run, even one you did not cause, is named in the report.

## Steps

1. **Pick the next slice:** the smallest behaviour on the list that moves the task forward. Write it as one sentence: «given …, when …, then …».
2. **Write the test** for that sentence only, in the project's test layout and naming style.
3. **Run it and watch it fail.** Read the message. If it passes, the behaviour already exists or the test is wrong: find out which. If it errors for an unrelated reason, fix the test setup and run again until it fails for the right reason.
4. **Make it pass** with the simplest code that does so.
5. **Run the test, then the related tests,** and confirm they pass with no new warnings or errors in the output.
6. **Tidy up:** remove duplication, improve names, extract a helper if it makes the code clearer. Run the tests after each step; if one turns red, undo the last step.
7. **Commit** the test and the code together, in the project's commit style, with a message that names the behaviour.
8. **Repeat** from step 1 until the list is done. Add new behaviours to the list as you discover them; do not slip them into the current slice.
9. **Run the full suite** with the project's test command, and keep the output for the hand-over.

## Checks before hand-over

- Every new or changed behaviour has a test that was seen failing before the code existed.
- Each failure was for the expected reason.
- The full test command passed after the last change; the output is attached.
- Commits are small and each contains its test.
- Any exception to test-first was agreed with the person and is written down.

## Artefacts

- Commits, one per slice, each with its test.
- The last full test run: command, exit code, summary line, and names of any failing tests.
- The slice list, with done and open items.

## Hand-over

- **To the reviewer:** the commits, the slice list and the full test run.
- **To the QA tester:** behaviours that need checks beyond unit level (devices, browsers, end-to-end flows).
- **To the repository owner:** tests that were already failing before the work began.

## Per stack

- **Swift / iOS:** Swift Testing marks test functions with `@Test`, can give them a readable display name, supports `async` and `throws` tests, and can limit a test to the OS versions where it applies; XCTest is the older framework and many projects still use it. Run tests from the package or through the app scheme on a simulator.
- **Android / Kotlin:** local unit tests run on the computer and are fast; instrumented tests run on a device or emulator and are for code that needs the platform. Test view models, the data layer and edge cases first, including configuration changes such as rotation. JUnit is the usual framework.
- **Flutter:** unit tests for single functions and classes, widget tests for one widget in a test environment, and integration tests for the whole app on a device or emulator; they get slower and more realistic in that order. Run with `flutter test`.
- **React Native:** static checks (lint, type check) first, then unit tests, then component tests that render and interact the way a user does and check what is shown, then end-to-end tests. Jest is the usual runner.
- **Ruby / Rails:** RSpec or Minitest, whichever the project uses; run one file or one example by line number for the fast loop, the whole suite at the end.
- **C and C++:** GoogleTest with CTest is common. Keep unit and integration tests apart by directory or label, let the build register tests, run a small subset first and then the full suite with output shown on failure. Re-run a failing test with sanitizers on (see memory-safety-check). Guard against flaky tests: no sleeps used for synchronisation, a unique temporary directory per test that is cleaned up, no real clock or network in unit tests, fixed seeds for random inputs; use fakes for state and mocks for interactions.
- **Angular / TypeScript:** component tests use the test bed and a component fixture; test harnesses help with interaction. Run the project's test command in single-run mode, not watch mode.

## Sources

Built on the «test-driven-development» skill from Superpowers (github.com/obra/superpowers, commit 8ca22db; © 2025 Jesse Vincent, MIT licence), adapted. Built on the «cpp-testing» skill from ECC (github.com/affaan-m/ECC, commit ef648e0; © 2026 Affaan Mustafa and contributors, MIT licence), adapted. Built on Android Developers documentation, «Fundamentals of testing Android apps» and «What to test in Android» (https://developer.android.com/training/testing/fundamentals; Google LLC and the Android Open Source Project, Apache License 2.0), adapted. Portions of this page are modifications based on work created and shared by the Android Open Source Project and used according to terms described in the Creative Commons 2.5 Attribution License. Built on Flutter documentation, «Testing Flutter apps» (github.com/flutter/website, commit 898d84d; © The Flutter Authors, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), adapted. Built on React Native documentation, «Testing» (github.com/facebook/react-native-website, commit b477b73; © Meta Platforms, Inc. and affiliates, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on Swift Testing documentation, «Defining test functions» (github.com/swiftlang/swift-testing, commit f3cbdec; © 2023 Apple Inc. and the Swift project authors, Apache License 2.0), adapted. Built on Angular documentation, «Unit testing» and «Basics of testing components» (angular/angular, commit 97e6aa4; © Google LLC, CC BY 4.0), adapted.

Ideas only (no text taken): Kent Beck, «Test-Driven Development: By Example» (Addison-Wesley, 2002).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
