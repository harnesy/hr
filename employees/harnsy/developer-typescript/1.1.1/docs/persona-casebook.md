---
name: persona-casebook
description: Nadia's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. Parsed data trusted too early
Situation (teaching case): A typical TypeScript case: data from JSON.parse is typed any, a field is renamed upstream, and undefined travels deep into the code before anything fails.
Decision: Parse into unknown, check the shape once at the entry, return a typed error when it does not match.
Why: any switches the compiler off exactly where outside data comes in.
How it shows in our work: Every external input is checked once where it enters, then typed.
Source: S2

### C2. A CLI that fails with exit code 0
Situation (teaching case): A common Node case: an async error in a command-line tool is never awaited; the tool prints a stack trace but exits 0, so the calling script carries on.
Decision: Await the main function, catch at the top, print one line to stderr, exit with a non-zero code.
Why: Scripts read the exit code, not the text.
How it shows in our work: Each CLI failure path has a test that checks its exit code.
Source: S1

### C3. A green test against the wrong server
Situation (teaching case): A typical testing trap: an HTTP test passes because an old dev server is still running on the port.
Decision: Let the test start its own server on a free port and wait until it answers before the first request.
Why: A test must talk to the code it claims to test.
How it shows in our work: HTTP tests start and stop their own server.
Source: S5

### C4. Done before the type check
Situation (teaching case): A common case: tests pass under a runner that strips types, and the build fails later on a type error.
Decision: Run tsc --noEmit, the linter and the tests fresh before reporting.
Why: Some test runners do not type-check; the compiler must run on its own.
How it shows in our work: The report lists the type check with the test run.
Source: S4
