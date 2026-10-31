---
name: kickside-endpoints-access
description: Open exactly the doors a KickSide module needs - member endpoints on the authenticated router listed by exact id in the module access policy bound to the members scope, a public endpoint only on an intentional public router with its own signature or token check and a rate limit, outbound calls under a policy scoped to the provider address, secrets as secret settings the owner enters, and live checks as a member and as an outsider. Use when adding an endpoint, a webhook or callback, a public form, an outside API call, a secret or an access policy.
---

# Endpoints, access policies, callbacks and secrets

In KickSide a signed-in person reaches a module only through policies. The host's authenticated router signs the request in and then a firewall checks the `access` action against the endpoint's exact registry id. A module therefore ships its own access policy that an administrator can give to a group, and by default the platform's Members group gets it. This skill keeps one rule above the others: **a door is open only when a policy names it, and a public door is locked by its own check.** A route, a menu item or a page grants nothing.

**Route:** a surface from kickside-module-capabilities → **kickside-endpoints-access** → the Application security reviewer for public or widening changes → kickside-module-release.
Before this skill: the handler and its domain call exist and are tested. After it: each door declared, its policy in place, and live answers as a member and as an outsider.

Marks: «(read from Sx, not tried)» means the step was read in that source and not run by us; the Sources section at the end names each Sx. Steps 1-4 follow the template's own policy and wiring tests, which ran in our trial (S6).

## When to use

- A new endpoint for the module's page or for another system.
- A webhook from a payment provider, a public lead form, any callback from outside.
- A call from the module to an outside API.
- A key or password the module needs.
- A new or changed access policy.

## Inputs

- The handler, the endpoint path and method, and who may call it (members, admins, the public).
- For a callback: the provider's documented way to prove a request is genuine.
- A member account and an account outside the group on the development copy (made-up people).

## Steps

1. **Member endpoints go on the authenticated router.** Declare the `http.endpoint` with `method`, `path` relative to the router and `func`; its router comes from the module's `api_router` requirement (the host's router runs token authentication and the endpoint firewall). The handler still confirms an actor is present.
   Check: a wiring test asserts the endpoint's exact id, its handler and its router target.
2. **List the endpoint in the access policy.** The module has one public policy with `meta.intent: module_access`, a `title`, a `surface` and empty `groups`; it includes private policies for runtime calls and for endpoint `access`. Add the new `<namespace>.api:<name>.endpoint` id to the endpoint policy. Optional powers (tools, management actions) get their own public policy (`intent: tool_access` for tools) so an administrator grants them separately.
   Check: the policy names each member endpoint by exact id; no wildcard on endpoints.
3. **Bind the members scope.** The `user_security_scope` requirement has `meta.value_kind: security.scope`, the platform Members group as its default, and a `.groups +=` target on every policy of the capability. When you add a policy, keep the published requirement id and its existing targets and append the new target, so installed copies keep their binding.
   Check: a wiring test asserts every policy is a target of the requirement.
4. **Check component access too.** Module access lets a member use the module; it does not let them read another person's records. For every record or component id a request carries, check access in the current call.
   Check: a member asking for another member's record is refused.
5. **A public endpoint is a separate, reviewed door.** (Read from S1 and S5, not tried.) Only when the task needs it (a payment provider's webhook, a public lead form): a separate requirement for the host's public router, its own `security.actor` and a short list of narrow policies for that function (open its database, read its config, dispatch one internal function), never the members scope and never a broad allow. Write the plan (path, what is checked, what it may do) and send it to the Application security reviewer before you build it.
   Check: the Application security reviewer's answer is on the item before the endpoint is merged.
6. **Prove the caller before acting.** (Read from S1, not tried.) Read the secret from a header (never from the URL or the body), or verify the provider's signature over the exact raw body, or fetch the object back from the provider by its id, as the provider documents; compare secrets without leaking timing. Never take a user identity, a group or a scope from a request field. Refuse with a plain 401 or 403 and no detail on failure; accept a retried delivery idempotently by its event id.
   Check: tests send a missing secret, a wrong one, a tampered body and a replayed event, and each is refused or ignored without a second effect.
7. **Limit the rate.** (Read from S1 and S4, not tried.) Do not rely on the host's public router to limit the rate: check on your copy which middleware it runs, and give a public endpoint its own limit. Wippy offers a `ratelimit` middleware on a router (requests per window, burst, key by IP or by a header). Behind your reverse proxy every request comes from the proxy's address, so key on the client-address header the proxy sets, or have the KickSide DevOps engineer limit at the proxy as well; the proxy side is theirs.
   Check: on the development copy a burst above the limit is refused with the code the middleware documents, and a normal pace is not.
8. **Outbound calls under a narrow policy.** (Read from S5, not tried.) Code that runs under its own actor (a callback, a job) needs an explicit policy for `http_client.request` whose resource is the provider's address (`https://api.<provider>/*`), never `*` and never `http_client.private_ip`. Do not rely on what ordinary users' policies allow on a copy for module code, and do not widen them.
   Check: a call to the provider succeeds and a call to another host from the same actor is refused.
9. **Secrets as secret settings.** (Read from S1 and S5, not tried.) Declare a settings definition with `value_type: secret` (usually `visible: false`, with the module's own panel to set it); the handbook says values are stored encrypted, masked in lists and returned in plain only to server code that asks for the one key. The owner enters the value on their own copy. Never return a secret to the page, never log it, never put it in a default, a test or a fixture.
   Check: the settings list shows the secret as set without its value, and a search of the repository and logs finds no key-like string.
10. **Check live as a member and an outsider.** (Not tried in our trial: it needs a running copy with the module loaded.) On the development copy call each endpoint as a member of the bound group and as a user outside it; call a public endpoint with and without its proof.
   Check: the four answers (allowed, refused, proved, unproved) with their status codes are in the report.

## Rules (each with its check)

- **Exact ids, no wildcards on endpoints.** Check: the endpoint policy lists ids, not `*.endpoint` patterns.
- **Published requirement ids and targets stay.** Check: the diff appends targets, it removes none.
- **Public doors only with review, proof and a rate limit.** Check: the Application security reviewer's answer, the proof tests and the rate-limit probe are in the report.
- **No identity from a request field.** Check: no handler builds an actor or a scope from input.
- **Secrets stay in the platform.** Check: none in source, tests, chat, files or reports.
- **Treat every copy as untrusted toward its host.** Extra accounts only after the Application security reviewer clears that copy; check on your copy what ordinary users' policies allow and tell the owner before anyone else gets an account. Check: the report says who has accounts and what ordinary users' policies allow on that copy.

## Do not promise

- That a member policy hides other people's records: that is component access, checked separately.
- That a rate limit by IP works behind a proxy without the right key.
- That a secret setting protects a value from everyone who can sign in: what ordinary users may do depends on the copy's policies, checked on that copy.

## Hand-over

- **To the Application security reviewer:** every public endpoint, every policy that widens access, every outbound or secret change, before it is applied.
- **To the KickSide QA tester:** the role checks in the browser and after a restart.
- **To the KickSide DevOps engineer:** rate limits at your reverse proxy, the client-address header, TLS and network isolation.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken. S1: the KickSide app at commit b7e0106 (github.com/kicksideai/kickside; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI): the handbook pages on security and module access, conventions and settings, the webhooks module's public endpoint and the host routers. S2: the KickSide module template (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy): its access policy, members-scope requirement and wiring tests. S4: the Wippy documentation page http/middleware (wippy.ai, read 2026-10-23; MPL-2.0). S5: KickSide components at commit bc5e866 (github.com/kicksideai/components; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI): an outbound policy scoped by address and secret settings. S6: our own trial with Wippy 0.3.52a, 2026-10-23: the template's own tests ran green on SQLite. No public endpoint, rate limit, outbound policy or secret setting was tried on a running copy.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
