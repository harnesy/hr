---
name: memory-safety-check
description: Look for memory and undefined-behaviour bugs in C and C++ code before they ship; build with a broad warning set treated as errors during development, run the test suite in separate sanitizer builds (memory errors, undefined behaviour, and data races or leaks where they fit), run static analysis with the project's configuration, trace each finding to its root cause with the stack trace, and fix it together with a regression test. Use after changes to C or C++ code, before a release, and when a crash or corruption cannot be explained.
---

# Memory safety check

In C and C++, an out-of-bounds write or a use after free may do nothing visible in a test and still corrupt memory in production. The compiler and its runtime checkers can find many of these bugs while the tests run, if the build asks for them. This skill sets up those builds next to the normal one, runs the test suite through them, and turns each report into an understood cause, a fix and a test that would catch it again.

**Route:** a change to C or C++ code, or an unexplained crash → **memory-safety-check** → findings with stack traces and causes → fixes with regression tests (tdd-slice, debug-root-cause for hard ones) → a clean run of all check builds → the reviewer.
Before this skill: a repository that builds and has tests. After it: a findings log, fixes with tests, and a record of which checks ran clean.

## When to use

- After a change to C or C++ code, especially code that handles buffers, pointers, lifetimes, threads or untrusted input.
- Before a release.
- When a crash, a corrupted value or a test that fails only sometimes has no clear cause.

## Inputs

- The repository and its build system, with the compilers it supports.
- The test suite, and how to run it.
- Any existing warning settings, static-analysis configuration and suppression lists.

## Rules

- Check builds are separate build configurations, off by default, so the normal build and its flags stay as the project has them.
- Treat all warnings as errors in development and CI builds. Do not put that blanket setting into build files that others use to build distributed source, because it ties them to one compiler version; promoting selected warnings to errors is fine everywhere.
- Warning flags cost nothing at run time; turning them on is never a performance trade-off.
- Sanitizers are for debug and test builds. They are too slow for release builds and must not be used to harden production binaries; the minimal undefined-behaviour runtime is the one exception the hardening guide names.
- A clean sanitizer run means these tests did not trigger these checks. It does not prove the code has no bugs, and the report says so.
- Every finding gets a root cause, not a workaround. Suppressions are a last resort, each with a written reason and the owner's OK.
- Every fix comes with a test that fails before the fix and passes after it.
- Run only the project's own code and tests; inputs from outside (crash files, fuzz cases) are run only in the sanitizer build, never on a live system.

## Steps

1. **Read the build:** compilers and versions, build types, current warning flags, existing sanitizer or analysis options, and how tests are registered and run.
2. **Raise the warning level** in a development configuration: the compiler's broad warning sets plus the format, conversion and fallthrough warnings, with warnings as errors. Build once without failing to record the baseline count if the project is not clean yet; agree with the owner whether to fix all at once or by area.
3. **Add a memory-error sanitizer build:** the sanitizer flag at both compile and link time, debug information, frame pointers kept, and modest optimisation so stack traces stay readable. Run the full test suite in it.
4. **Add an undefined-behaviour sanitizer build,** with findings made fatal so that the test run fails on the first report instead of printing and carrying on. Run the full test suite.
5. **Where it fits,** add a data-race build for code with threads (it cannot be combined with the memory-error build), and leak detection where the platform supports it.
6. **Run static analysis** with the project's configuration file and the compilation database from the build, on the changed files first and then on the whole tree if it is affordable. Agree with the owner which checks to promote to errors.
7. **Triage each finding:** read the full report and stack traces, reproduce it with the smallest test, and find where the bad pointer, index or value comes from. Hard cases go through debug-root-cause.
8. **Fix at the cause,** with a regression test written first (tdd-slice). Prefer fixes that make the error impossible: an owning object instead of manual release, a bounds-checked view instead of a pointer and a length, an initialised variable, no cast that hides a type mismatch.
9. **Run all check builds again** until they are clean, or until each remaining finding is recorded with a reason.
10. **Propose CI jobs** for the check builds to the owner and to devops, so the checks keep running.

## Checks before hand-over

- Each check build ran the full test suite; the commands and results are recorded.
- Warnings-as-errors is set for development builds only, not forced on distributed source.
- No sanitizer flag reached a release or production build.
- Every finding has a cause, a fix and a regression test, or a recorded reason with the owner's OK.
- The report says what the checks cannot prove.

## Artefacts

- `memcheck/<date>.md`: build configurations used, commands, results per build, findings with stack traces, causes, fixes and tests, open items.
- Build-system changes adding the check configurations, off by default.
- The fixes and regression tests, as reviewable changes.

## Hand-over

- **To the reviewer:** the fixes with their tests, and the findings log.
- **To the security reviewer:** findings that touch untrusted input, memory corruption or privilege boundaries.
- **To devops:** the proposed CI jobs for the check builds.
- **To the repository owner:** suppressions proposed, and warnings that need a decision.

## Tools

- **AddressSanitizer** (Clang and GCC, `-fsanitize=address`): reports reads and writes past the bounds of heap, stack or global buffers, access to memory already freed, to locals whose function has returned or whose scope has ended, freeing twice, and leaks where the platform supports leak detection. The Clang documentation gives a typical slowdown of 2x (commit 93c9c6b, page last changed 8 September 2026). Build with `-g`, `-fno-omit-frame-pointer` and `-O1` or higher; runtime options go through the `ASAN_OPTIONS` environment variable.
- **UndefinedBehaviorSanitizer** (`-fsanitize=undefined`, a check group; single checks can be added or removed): add `-fno-sanitize-recover=` for the checks that must stop the run. Some checks, such as implicit conversions and local bounds, are outside the default group and must be named.
- **ThreadSanitizer** (`-fsanitize=thread`) and **LeakSanitizer** (`-fsanitize=leak`), where they fit. The OpenSSF guide notes that ThreadSanitizer cannot be used together with AddressSanitizer or LeakSanitizer, and that GCC and Clang sanitizer builds cannot be mixed.
- **clang-tidy:** reads the compilation database (`-p <build dir>`; CMake writes one with `CMAKE_EXPORT_COMPILE_COMMANDS=ON`), a checked-in `.clang-tidy` file, and `--warnings-as-errors=` to promote chosen checks. Its `cppcoreguidelines-` checks relate to the C++ Core Guidelines; the fix patterns in step 8 correspond to rules R.1, R.11, I.13, ES.20 and ES.48 there.
- **Warning flags:** `-Wall`, `-Wformat`, `-Wformat=2`, `-Wconversion`, `-Wimplicit-fallthrough` and `-Werror=format-security` from the guide's short list, plus blanket `-Werror` for development builds only; the OpenSSF guide (dated 20 August 2026) lists the run-time hardening flags for production builds as a reference to read, not as a fixed rule set.
- **Test runner:** CTest or the project's own; put each sanitizer behind its own CMake option, off by default.

## Sources

Built on Clang documentation, «AddressSanitizer», «UndefinedBehaviorSanitizer» and «clang-tidy» (github.com/llvm/llvm-project, commit 93c9c6b; LLVM Project contributors, Apache License 2.0 with LLVM Exceptions), adapted; changes were made. Built on «Compiler Options Hardening Guide for C and C++» (github.com/ossf/wg-best-practices-os-developers, commit 8259081, https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html; © OpenSSF contributors, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on the «cpp-testing» skill from ECC (github.com/affaan-m/ECC, commit ef648e0; © 2026 Affaan Mustafa and contributors, MIT licence), adapted.

Ideas only (no text taken; rule ids named as facts): C++ Core Guidelines (github.com/isocpp/CppCoreGuidelines, commit 33bcd01; Standard C++ Foundation and contributors).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
