---
name: wippy-lua-testing
description: Test-first work in Lua on Wippy with the runtime's own test runner - a failing test in the form the runner really executes, the smallest change, a deliberate break to prove the test bites, a late-locals scan and lint with the project's own runtime build, probe tests for the runtime's Lua dialect quirks (number formatting, integer or float, empty ranges, tail calls that yield, closures after pcall), and a final check in the running app. Check your runtime build first. Use for every code change in a Wippy project.
---

# Test first on Wippy, then the running app

The runtime's test runner boots the app and runs test entries inside it. It is fast and honest about what it runs, but three things slip past it: a test file in a form the runner counts but never executes, Lua that behaves differently from the reference manual on this runtime, and anything that depends on policies, because tests run with a wide scope. This skill covers all three and ends in the running app.

**Route:** a task → wippy-modules and wippy-processes as needed → **wippy-lua-testing** for every behaviour → reviewer.
Before this skill: the runtime build the project uses, and the namespace. After it: tests seen red then green, lint clean with the right build, and a live answer from the app.

## When to use

- Every new behaviour or bug fix in Lua on Wippy.
- A test that is green for no visible reason, or a change that «does nothing» in the app.
- A new runtime build in the project: run the probes again.

## Inputs

- The project's test command and host (the agent notes or the Makefile), and the runtime binary it uses.
- The behaviour to build as one sentence: given, when, then.

## Steps

1. **Write the failing test.** A test is a `function.lua` entry marked as a test in its `meta`, beside the module in the project's test harness. Build the cases with the test library's case runner and export `run` as a function that passes its options on to the cases, for example `local cases = test.run_cases(define)` and `return { run = function(opts) return cases(opts) end }`. Run it with the project's command; when the app has more than one terminal host, name one with `wippy test --host <entry id>`.
   Check: red, and red for the reason the sentence names. A failure to boot (a missing import stops every test) is not that reason: fix it and run again.
2. **Make it pass** with the smallest change. Logic goes in the pure library (wippy-processes, step 1).
   Check: green; the timing looks real. Many cases in under a millisecond, or «no tests found», is a failure.
3. **Break it once.** Change the code so the behaviour is wrong, run, restore.
   Check: red with the expected message, then green again. Keep the two lines of output for the hand-over.
4. **Scan for late locals, then lint with the project's build.** A local that a function reads before the line declaring it is seen as an unset global, nil at run time, with no error raised. Run the project's scan if it has one; if not, read each touched file for it. Then run `wippy lint --ns <namespace>` for every namespace you touched, with the runtime binary the project uses. A build that lacks a module's types can answer «clean» on code it cannot see.
   Check: no late locals; lint clean; an arithmetic warning on a value that may be nil is fixed at its source, not silenced.
5. **Run the dialect probes** below on the project's build, once per build, and keep the result in the project notes.
   Check: you know which workarounds apply. Where a probe answers as the reference manual does, drop that workaround.
6. **Check in the running app.** Make sure the port is free, start the app, call the changed path through its real entry point (an endpoint, a command, a message), read the answer body and the log, stop, and wait for the pid and the port. An edit does not reach an instance that is already running: restart it.
   Check: the answer body is the one the test expects, not only a good status code; the command and the answer go into the hand-over.

## Dialect probes

Each quirk is a rule only while its probe says so. A probe is a tiny test that asserts what the Lua reference manual says; red means the quirk is present on this build and its workaround applies.

| probe asserts | if red | workaround and its check |
|---|---|---|
| `string.format("%.1f", 3) == "3.0"` | float verbs garble integers | add `0.0` to a value before `%f`, `%e` or `%g`; a test formats an integer input and compares the string |
| `string.format("%02x", 255) == "ff"` | hex verbs print the hex of the digits | build hex from a digit table; a test checks 255 gives «ff» |
| `math.type(tonumber("5")) == "integer"` | parsed numbers come back as floats | decide at the edge whether a value is an integer and convert, refusing what does not fit (`math.tointeger` gives nil for 2.5); a test checks `math.type` |
| `table.concat({"a", "b"}, "", 3, 2) == ""` | an empty range at the end returns the last item | join ranges through a helper that returns `""` when the start is past the end; a test with a range at the end of a table |
| a helper that ends in a bare `return` of a yielding call (a send, a receive, a select, a query) still has its effect | the tail call is skipped with no error | assign the result to locals, then return them; search the change for a bare return of a yielding call |
| a local shared by a function and its closure stays shared after an error caught by `pcall` | the closure loses the shared local | keep such state in a table field; review closures in code that uses `pcall` |

## Rules (each with its check)

- **The test form is the one that runs.** A file that exports its cases in another shape can be counted and shown green without running. Check: step 3, the deliberate break, on every new test.
- **Read the runtime build before trusting a tool.** The lint, the probes and the dependency route all depend on it. Check: the build's version line is in your notes for the task.
- **Green is not the end.** Tests run with a wide scope and an edit does not reach a running instance. Check: step 6 after the last change.
- **Name what ran.** Report the commands, the numbers of passed and failed tests and the live answer; say what you did not check and why.

## Checks before hand-over

- Every new test was seen red for the right reason, then green, then red again on a deliberate break.
- Late-locals scan and lint of every touched namespace with the project's build are clean.
- The dialect probes have been run on this build, and only the workarounds they call for are in the code.
- The running app gave the expected answer; the instance is stopped and the port is free.

## Artefacts

- The tests, the probe results for the build, the lint output, the live command and its answer.

## Hand-over

- **To the reviewer:** the change, the red-green-red lines, lint, and the live answer.
- **To the Go developer:** a probe that shows a runtime fault, as a small repeatable test; you keep the workaround until the fix lands and the probe turns green.
- **To the terminal UI developer:** a window that should show the result; you give it the data and the contract, it owns the screen.
- **To the accessibility engineer, ui designer or design system keeper:** questions about what users see or read.

## Sources

This employee is a harnsy product, not an official product of these projects.

Built on Chicago shell, «docs/traps.md» (github.com/chicago-desktop/shell, commit ceaebf5; © 2026 Wippy, MIT), adapted. Built on Chicago module-template, «AGENTS.md», the Makefile and the test harness (github.com/chicago-desktop/module-template, commit 4c86d76; © 2026 Wippy, MIT), adapted. Built on Chicago app, «CLAUDE.md» and the skill «chicago-debug» (github.com/chicago-desktop/app, commit 225e926; © 2026 Wippy, MIT), adapted. Facts only, no text taken: Lua 5.4 Reference Manual (lua.org/manual/5.4/; Lua.org, PUC-Rio, MIT) for the standard behaviour the probes assert, and the Wippy documentation on testing and lint (github.com/wippyai/docs, commit b05b548; MPL-2.0). Probe results checked in our own trial on two runtime builds, 2026-10-21.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
