---
name: wippy-processes
description: Build services in Lua on Wippy as processes that talk by messages - a pure library for the logic, a thin process with a registered name and an inbox loop, supervision declared as a service with restart and an actor, callers that check every send and never wait without a timer, errors read by their kind, and narrow per-entry security policies proven by a live call. Check your runtime build first. Use when writing or changing a process, a service, a handler that talks to one, or a policy.
---

# Wippy processes, services and policies

In Wippy, long-lived work runs as processes that own their state and talk only by messages. The runtime supervises them and checks every call they make against a policy. Two failures come back again and again, and neither shows up as an error: a call the policy refuses, read as «nothing happened», and a caller that waits for an answer that will never come. This skill builds a service so that both show up.

**Route:** a task for a service or a handler → wippy-modules (if a dependency or an entry is new) → **wippy-processes** → wippy-lua-testing for the test-first loop and the live check → reviewer.
Before this skill: the runtime build and the namespace known (wippy-modules, step 1). After it: a library with tests, a supervised process, callers that report refusals, and policies no wider than the live call needs.

## When to use

- A new process or service, or a change to how one answers, restarts or keeps state.
- A function or HTTP handler that sends to a process and waits for the answer.
- A policy to add or change.

## Inputs

- The index file of the namespace, its process host and its existing policies.
- The message contract: topics, payload fields, who answers whom.

## Steps

1. **Put the logic in a pure library.** A `library.lua` entry with no side effects holds everything a test should see: parsing, sums, decisions, formatting.
   Check: the library has its own test that needs no process.
2. **Keep the process thin.** A `process.lua` entry registers its name, loops over `process.inbox()`, calls the library, answers to the `reply_to` the sender gave, and logs and skips a topic it does not know.
   Check: a test sends a message and waits for the answer with a timer; an unknown topic leaves the process alive.
3. **Declare the supervision.** Wrap the process in a `process.service` entry on the app's process host: auto start, restart with back-off and a limit, a security actor, and the policies it needs.
   Check: in a stand, make the process fail on purpose; the service comes back with a new pid. Then check the state: a restarted process starts with empty memory, so anything that must survive lives in a store, not in a local table.
4. **Write callers that cannot hang or hide a refusal.** A function or handler reads both returns of `process.send`; on an error it reads `err:kind()` and answers with that kind. It waits for the reply with `channel.select` over the reply and a `time.after` timer, never forever, and turns a timeout into a clear error.
   Check: a refused send shows its kind in the answer; a stopped service gives a timeout error, not a hang.
5. **Grant narrow policies.** One policy per need, the actions listed by name, attached to the entry that needs them. A send to a registered name needs more than the send action: the name lookup is a separate action. Narrow the resources only as far as a live call proves; a narrowing that stops the call is not a fix.
   Check: a rule test that walks every process and function entry, takes the modules it declares and the actions its policies grant, and fails when a gated module has no action; then the live call through the real entry point (wippy-lua-testing, last step).
6. **Read errors once, in one place.** One helper per project turns a runtime error into kind and message; handlers and services call the helper.
   Check: no `tostring(err)` used to decide anything; the decision reads the kind.

## Rules (each with its check)

- **The second return is read on every runtime call** that can fail (`process.send`, `env.get`, registry and SQL calls). An unchecked send that the policy refuses looks exactly like a slow service. Check: search the change for calls whose error is dropped; none remain.
- **Decide by the kind, not the text.** A permission refusal has a stable kind, its message does not. Some modules report a refusal with a more general kind and a message that starts with the words «permission denied», so the helper checks both. Check: a test or a live call shows the kind your helper returns for a refusal.
- **Some modules refuse by leaving things out.** A listing call can return only what the policy allows, with no error at all. Check: when a listing is empty or short, prove the policy grants the action before you believe it.
- **The environment store is not the process environment.** A value set in the shell when starting the app is not what the runtime's environment module reads. Check: read the value through the project's own environment entries in a test.
- **Tests run with a wide scope; the app does not.** A missing policy passes every test. Check: the live call, every time a policy, an entry or a caller changes.
- **Events are broadcast and can race; control goes by direct message.** Check: anything that must happen once is sent to a name and answered.
- **One state, one owner.** Two copies of the same value, or two tables of the same settings, drift apart without a sound. Check: one source per fact; a test compares the full field set with what the real consumer reads.
- **Policies stay narrow; shared ones are not yours alone.** No wildcard actions in production entries. A change to a policy that many entries share, or to the app's user scope, goes to the reviewer and the owner before it lands. Check: the diff touches only the policies of your own entries, or names who approved the shared change.

## Checks before hand-over

- The library has unit tests; the process has a message test with a timeout.
- Every caller reads the error and its kind; no wait without a timer.
- The rule test for modules and permissions is green, and the live call through the real entry gave the expected body.
- A restart drill was done when the change touched a service, and state that must survive is in a store.

## Artefacts

- The library, the process, the service and policy entries, the tests.
- The live command and its answer, and the restart drill result.

## Hand-over

- **To the reviewer:** the change, the policies it adds, the test run and the live answer; a shared policy change with the owner named.
- **To the terminal UI developer:** what a window shows and how it looks; you give it the service and the message contract.
- **To the Go developer:** a runtime module that behaves against its documentation, with a small repeatable case.
- **To the software architect:** a service that wants to move to another module, or a new contract between modules.

## Sources

This employee is a harnsy product, not an official product of these projects.

Built on Chicago shell, «docs/traps.md» (github.com/chicago-desktop/shell, commit ceaebf5; © 2026 Wippy, MIT), adapted. Built on Chicago module-template, «AGENTS.md» (github.com/chicago-desktop/module-template, commit 4c86d76; © 2026 Wippy, MIT), adapted. Built on Chicago app, the skill «chicago-debug» (github.com/chicago-desktop/app, commit 225e926; © 2026 Wippy, MIT), adapted. Facts only, no text taken: Wippy documentation on processes, services, channels and security (github.com/wippyai/docs, commit b05b548; MPL-2.0) and the Wippy runtime (github.com/wippyai/runtime, commit 4137a00; MPL-2.0). Facts checked in our own trial in a running app, 2026-10-21.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
