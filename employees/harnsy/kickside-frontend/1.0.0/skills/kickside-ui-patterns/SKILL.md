---
name: kickside-ui-patterns
description: Decide what goes on a KickSide module's screen and build it from what the platform already gives before writing new UI - lists and tables, record cards, boards, forms through the shared JSON-schema form, pickers from kickside/widgets, the CSS vocabulary of kickside/ui-kit, the CRM module's own surfaces; real loading, empty and error states; confirmation before destructive actions; and the public lead form for a client's website (no secrets in the browser, a honeypot field, labels, a clear success and error message). Use when a spec names a screen, a form, a list, a board, an approval or a website form, or when a page grows its own copy of something the platform has.
---

# KickSide screens: reuse first, then build

Most screens a client asks for are a list, a record, a board or a form. KickSide already ships a lot of that: the CRM module has tables, boards, records, history and imports; `kickside/widgets` has a form generated from a JSON schema and several pickers; `kickside/ui-kit` has shared CSS classes for cards, headers, empty and loading states, controls and overlays. A module page that rebuilds these costs time now and drifts from the rest of the app later. This skill decides what to reuse and how to build what is left.

**Route:** the KickSide analyst's spec → **kickside-ui-patterns** (what is on the page) inside kickside-web-component (the frame) → kickside-ui-testing → the Reviewer.
Before this skill: the spec with its fields and actions, and the endpoint contract from the KickSide module developer. After it: a screen made of reused parts plus the smallest new code, every state drawn, every action labelled.

## When to use

- A spec names a list, a table, a record view, a board, a form, a settings screen or an approval step.
- Someone asks for a form on the client's website that sends leads into KickSide.
- A module page has grown its own date picker, schema form, card style or empty state.

## Inputs

- The spec: who uses the screen, which fields, which actions, which roles see it.
- The endpoint contract: paths, answer shapes, error codes, the realtime topic.
- The list of modules installed on the DEV copy (the KickSide specialist has it).

## Steps

1. **Ask «does CRM already do this?»** If the screen is records of a business object (leads, deals, companies, contacts) with a table, a board, a record card and history, it is CRM configuration, not a new page: the schema, fields and collections are set in CRM by the KickSide specialist. A module page links to CRM routes by the `navigate` event, or embeds a CRM surface such as the record picker where the module needs a record chosen.
   Check: the report says which part is CRM configuration and which part is new UI, and why.
2. **Look for a widget.** For a settings form whose fields a JSON schema can describe, use `wc-schema-form` (props: the schema and the current values). For choosing many items from a paged source use `wc-multiselect`; there are also pickers for models, icons, channels, connections and components. Read each widget's props in its `view.component` entry on the DEV copy before using it; never guess a prop. Load a peer element with `loadByTagName` from the proxy if it is not yet defined, and keep the build from compiling `wc-` tags as Vue components (read from S2, not tried).
   Check: every widget prop you set is in its registry entry; the owning endpoint validates the submitted values again (the widget's checks are a convenience, not security).
3. **Use the shared CSS vocabulary.** When the module consumes `kickside/ui-kit`, import its token sheet first and then only the sheets the page uses (cards, headers, states, controls, overlays, tags). Adopting a shared class means deleting the local rule it replaces; an override states only what differs (read from S2, not tried).
   Check: no local rule duplicates a ui-kit class you import; the module's own check and tests still pass.
4. **Build the rest from PrimeVue.** Tables, inputs, selects, dialogs, tags, toasts and menus come from PrimeVue, styled by the host theme. A hand-made control where PrimeVue has one is a defect, and so is an invented prop.
   Check: no raw `<input>` or clickable `<div>` acting as a standard control.
5. **Draw every state.** Loading (with a stable layout, not a jump), empty (what this list will hold and the one action that fills it), error (the message in plain words and a retry), and the data. A list that pages shows where it is and loads the next page on request. Keep the old rows visible while a refresh runs.
   Check: each state has a test in kickside-ui-testing and a screenshot for the KickSide QA tester.
6. **Make actions safe.** Real buttons for actions; every icon-only button has an accessible label. A destructive action (delete, cancel, send to a client) asks through `host.confirm` with the action named on the accept button. After a write, show a toast with `host.toast` and reload from the endpoint; never patch the list from the request you sent. Disable the button while the write runs so a double click does not send twice (read from S2, S5, not tried).
   Check: a test clicks the action, sees the confirm, and sees one request.
7. **Approvals are platform first.** A step where a person must approve (a refund, a discount, a sent quote) is usually a workflow with an approval step built by the KickSide specialist; the module page shows the item's state and links to it. A page builds its own approve button only when the spec says so and the endpoint enforces who may approve.
   Check: the endpoint, not the page, refuses an approval by someone without the right; the page only hides what the person cannot do.
8. **Respect access.** Hide or disable what the person's role cannot do, from what the endpoint tells you, and still expect a refusal. Show a refused call as «you do not have access» with no technical detail.
   Check: tried as a member without the right on the DEV copy; the page shows the refusal cleanly.

## A public website form, such as a lead form

This form lives outside the KickSide shell, on the client's own site, so none of the shell's tools (proxy, session, theme) are there. The backend half (the public endpoint on a public router, spam and rate limits, writing the lead into CRM, the event for automations, the allowed origins) belongs to the KickSide module developer; hosting, HTTPS through your reverse proxy and the origin headers to the KickSide DevOps engineer. You build the form, its snippet and the module's settings screen.

The public endpoint such a form posts to does not come with the platform or the module template (read from S1, S3): the KickSide module developer builds it first. Until it exists, the steps below are a design and not tried; say so in every report about the form.

1. **Settings screen in the shell.** The owner chooses fields, labels, the thank-you text and the allowed site address on a page of the module (use `wc-schema-form` if a schema describes it). The page shows the ready snippet with a copy button (not tried).
2. **The snippet holds no secret.** No API key, no Hub or provider token, no admin password, no webhook secret: anything in the snippet is public. KickSide's generic webhook checks a shared secret and therefore does not fit a browser form; the form posts to the module's own public endpoint, which checks the origin and limits by itself (read from S1, S12, not tried). HTTPS address only.
3. **Small and self-contained.** Plain HTML form and a short script, no framework, no third-party loads, no cookies. It works without the script where the endpoint allows a plain form post; where the client's site forbids inline scripts, offer the script as a file (not tried).
4. **Honeypot.** One extra text field that people never see: moved off-screen (not `display: none`, which some bots skip), `tabindex="-1"`, `autocomplete="off"`, hidden from screen readers. The endpoint drops any submission where it is filled. Never the only defence: the endpoint's rate limit stays (not tried).
5. **Accessible.** Every field has a visible `<label>` tied to it, required fields say so in text, errors are shown next to the field and announced through a polite live region, the submit button says what it does, and focus moves to the success or error message (not tried). A question these checks do not settle goes to the Accessibility engineer.
6. **Honest messages.** On success, the owner's thank-you text; on failure, «could not send, please try again or contact us» and the form keeps what was typed. Never echo server internals (not tried).
7. **Personal data.** The form collects only the fields the owner chose, says what happens with the data in the owner's own words (the owner provides the text), and the data goes to the client's copy only (not tried).

Check for the form, once the endpoint exists: a test page with the snippet sends a lead that appears in CRM on the DEV copy; a filled honeypot creates nothing; keyboard-only and screen-reader runs pass; the snippet's text contains no key-like string. Then the Application security reviewer sees the form and its endpoint before it goes on a client's site.

## Rules (each with its check)

- **Reuse before build.** Check: the report names what was reused and why anything new was needed.
- **Every state drawn.** Check: loading, empty, error and data each have a test.
- **The server decides access and validity.** Check: a refused call is shown cleanly, and no rule exists only in the page.
- **No secrets in any browser code, the public snippet above all.** Check: search of the snippet and `static/` for key-like strings is empty.

## Hand-over

- **To the KickSide specialist:** CRM schema, fields, collections, workflows with approval steps, roles to test with.
- **To the KickSide module developer:** endpoints, the public lead endpoint, spam and rate limits, allowed origins in code, realtime topics.
- **To the KickSide analyst:** a spec that conflicts with what CRM or the widgets already do, with a proposal.
- **To the UI designer:** a look or layout that no screen in the platform has yet.
- **To the Accessibility engineer:** a form or screen where keyboard or screen-reader use is still in doubt after your checks.
- **To the Application security reviewer:** a public website form and its endpoint, before it reaches a client's site.
- **To the Reviewer:** the commit hash and what to check.
- **To the KickSide QA tester:** the states to try and the form's test page.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: S1 the KickSide documentation's module list (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0), S3 the official module template (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy), S2 the KickSide app (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI) with its ui-kit and widgets modules and the handbook's security chapter, S4 the KickSide CRM module (github.com/kicksideai/crm, commit 3cdb074; same licence), S12 our reading of that module list (the webhook module checks a shared secret), and S5 the Wippy proxy page (en/frontend/micro-frontends/proxy-api; MPL-2.0), read 2026-10-23.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
