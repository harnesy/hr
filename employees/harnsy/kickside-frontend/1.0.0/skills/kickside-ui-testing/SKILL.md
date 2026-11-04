---
name: kickside-ui-testing
description: Prove a KickSide module page before hand-over - vitest with jsdom and a mocked @wippy-fe/proxy through make test-ui (refresh on a realtime wake-up, refresh on host reveal without a second subscription, a late older answer ignored, the subscription released on unmount, every state and action), then make typecheck, make build and the module's own check, then the page in the DEV copy - console clean, light and dark, a member's view - with screenshots, then the commit hash and what to check for the Reviewer and the hand-over to the KickSide QA tester; Keeper's screenshot tool only on the DEV copy. Use before saying a page is done, when a page test is flaky, or when a page works in tests but not in the app.
---

# Proving a KickSide page

A page is done when three things agree: its unit tests, the module's build and checks, and the running DEV copy. Unit tests run fast in jsdom with the proxy replaced by a fake, so they can play out the hard timing cases (a wake-up during a load, a return visit, an answer that arrives late). The build and the module's check script catch contract breaks the tests cannot see (a stale `static/`, a missing scroll owner, a wrong token name). Only the running copy shows the shell, the theme, overlays and real access.

**Route:** kickside-web-component and kickside-ui-patterns → **kickside-ui-testing** → the Reviewer → the KickSide QA tester for end-to-end checks.
Before this skill: the page and its endpoint on the DEV copy. After it: green `make test-ui`, `make typecheck`, `make build` and the module's check, a live check with screenshots, and a short report.

## When to use

- Before you say a page or a change to it is done.
- When a page test fails now and then.
- When tests pass but the page misbehaves in the app.

## Inputs

- The module repository and its `Makefile` targets: `test-ui`, `typecheck`, `build`, `check` or `verify`.
- The DEV copy's address and two test accounts from the KickSide specialist: one with the module's access, one without, made only after the Application security reviewer cleared that copy. Fake data only.

## Steps

1. **Mock the proxy, not Vue.** In the spec, replace `@wippy-fe/proxy` with a small fake: `api.get` (and `post` where used) as mock functions, and `on` storing each topic's handler in a map and returning a disposer that removes it. Provide the host-visibility value from `@wippy-fe/webcomponent-vue` as a ref you control. Stub icons. Keep the template's vitest settings (jsdom, specs next to the source, the Wippy packages inlined) (read from S3, not tried).
   Check: the spec imports the real page component, not a copy of its logic.
2. **Test the refresh contract.** Three tests every data page needs:
   - a wake-up on the topic makes the page reload from the endpoint and show the new value, whatever the wake-up payload said;
   - hiding and showing the page through the visibility ref reloads once, without a second subscription;
   - when the first answer arrives after a later one, the page keeps the later one.
   Add: after unmount the topic map is empty.
   Check: each test was seen failing once (break the code on purpose, run, restore) before it counts.
3. **Test states and actions.** Loading, empty, error with a working retry, data. Every action: the click, the confirm where it is destructive, exactly one request, the toast, the reload. A refused call (403 from the mock) shows the access message.
   Check: one test per state and per action, with names that say what should happen.
4. **Run the module's gates.** `make test-ui`, `make typecheck`, `make build`, then the module's own check (`make check`, or `make verify` for the whole set when the machine has room; it also runs the Lua suites). Read failures; do not retry blindly (read from S3, not tried).
   Check: each command's last lines are in the report; `static/` was rebuilt by `make build` and committed.
5. **Open it in the DEV copy.** Start from the app shell and reach the page through its menu item, not by a typed asset URL. After the page loads and after each material action, read the browser console and the failed network calls. Try the long list (scrolls to the end), the empty state, the error state (the KickSide module developer can tell you how to cause one on the DEV copy), dark mode, and every overlay. When you drive the browser yourself, run it headed where the machine has a display, else headless with screenshots.
   Check: no console error, no failed call you did not expect; the data shown matches the endpoint's answer.
6. **Sign in as a member.** With the test account that has the module's access, then with the one that has not. An admin sees everything and proves nothing about a member.
   Check: allowed actions work for the member; the other account is refused by the endpoint and sees the access message.
7. **Screenshots for QA.** Take one screenshot per state and theme (light and dark, data, empty, error, an open dialog) at the desktop width the product supports. On the DEV copy, Keeper (the KickSide module that gives agents tools over MCP to edit, test and screenshot a running copy) has a screenshot tool (read from S2, not tried); how to call it depends on the Keeper version on that copy, so check it there first. Never use Keeper or its MCP access on a client's production copy, and never take screenshots of real client data.
   Check: screenshots are named by page, state and theme, and attached to the item.
8. **Report.** Done, how it was checked (commands and their last lines, the live checks, the screenshots), and what is left or was not checked, with the reason.
   Check: the report names the commit hash and the DEV copy it was checked on.
9. **Hand to the Reviewer.** Give the Reviewer the commit hash and what to check: the files changed, the tests that cover each change, the states seen live, and what was not checked. The KickSide QA tester gets the page with the same commit.
   Check: the item holds the hash and the list of what to check.

## Rules (each with its check)

- **A test that never failed proves nothing.** Check: each new test was seen red once.
- **The whole UI suite, not one file.** Check: the report shows `make test-ui` output.
- **Done is checked in the running copy.** Check: step 5 and 6 results are in the report.
- **DEV copy only for trials, Keeper and screenshots; fake data only.** Check: the copy's address in the report is the DEV copy's.
- **No secrets in tests, fixtures or screenshots.** Check: fixtures hold made-up values; no token in a screenshot or a log you attach.

## Pitfalls

- jsdom has no shadow-root layout and no real overlays: scrolling and dialog placement are proven only in the app.
- A live Keeper edit to a page or entry is not in the module's files: port it into `ui/src` or `src/`, rebuild and rerun the tests, or it is lost at the next release (read from S2, not tried).
- `make test` (the Lua runner) can pass with zero tests found; the template's Makefile guards against it, and a hand-run command may not (read from S3, not tried).
- The DEV copy may still serve the old bundle: reload hard after `make build` or keep `make dev` running.

## Hand-over

- **To the Reviewer:** the commit hash and what to check.
- **To the KickSide QA tester:** the commit, the routes, the accounts to use, the screenshots and the list of states, for end-to-end checks across modules.
- **To the KickSide module developer:** a failing endpoint call with the request, the answer and the time.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: S3 the official module template's Makefile, vitest setup and starter page spec (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy), S2 the KickSide developer handbook's frontend, testing and dev-loop chapters, including its Keeper tool list (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI), and S5 the Wippy proxy page (en/frontend/micro-frontends/proxy-api; MPL-2.0), read 2026-10-23.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
