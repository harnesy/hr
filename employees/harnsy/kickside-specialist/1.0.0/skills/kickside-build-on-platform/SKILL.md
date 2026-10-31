---
name: kickside-build-on-platform
description: Build on a running KickSide copy - agents with a prompt, a model and capabilities; model providers; automations and workflows with approval steps; connections to outside apps; AI tools connected into the platform over MCP with narrow, expiring credentials; users, groups and roles - and check each piece in the running platform, including as an ordinary member. Use when someone asks for an agent, an automation, a workflow, a connection, MCP access or a user setup on KickSide.
---

# Build on KickSide

Most of the work on a running KickSide copy happens in its own pages and its API, not in code. Each piece has a quiet way to look finished without working: an agent saved without a model, an MCP credential that lets the client in but shows it no tools, a role that looks right to the admin and is never tried as a member. This skill ends every piece with a check in the running platform.

**Route:** a request to build on the platform → **kickside-build-on-platform** → kickside-hub-modules when a needed module is missing → the owner.
Before this skill: a running copy (kickside-install-run), admin access the owner gave you, the owner's OK for what you will create. After it: each piece created, checked live and reported.

## When to use

- An agent, a model provider, an automation or a workflow.
- A connection to an outside app.
- An AI tool that should reach the platform over MCP.
- Users, groups, scopes and roles.

## Inputs

- What the owner wants, in one sentence per piece.
- The owner's model provider key, when an agent must answer; it is entered in the platform, never in chat or files.
- The port of the copy; local addresses are written as `127.0.0.1:<port>`.

## Steps

Our trial ran these steps through the calls each step names, as an admin signed in to the copy, not by clicking the pages; the pages are the same actions for a person.

1. **Agent.** Agents → new: a prompt, a model or a model class, capabilities (traits) and routing; share with it the resources it needs. An agent saved without a model gets the default class and answers nothing until a model is assigned to that class.
   Check: the agent is in the list; a short chat answer once a model is set, or the report says «waits for a model».
2. **Model provider.** System → Models: a provider profile with the owner's key, refresh the model list, assign a model to the default class. Not tried in our trial: it needs the owner's key.
   Check: the profile's test passes, and the agent from step 1 answers.
3. **Workflow.** Needs the workflows module (kickside-hub-modules). Create a workflow, then add its steps: a start with an input schema, the steps (for a person's decision, the Inbox review block with its prompt), a finish with an output schema, and edges between them; the review block has an approve and a reject exit, and both must lead somewhere. The same steps go through `POST /api/v1/workflows`, then `POST /api/v1/workflows/<id>/apply` with a batch of `node.add` and `edge.add` commands. Publish it; a published version cannot change: edit and publish a new one.
   Check: publishing returns a version number, and the workflow appears among the published ones (`GET /api/v1/workflows/published`).
4. **Automation, and the Inbox answer.** Automations → pick a kind; the kinds come from the installed modules (`GET /api/v1/automations/types`). «Manual task» runs a published workflow version on request and needs no outside key: set its target to the workflow and version from step 3 and its input, enable it, then run it now (`POST /api/v1/automations/<id>/control` with `run_now`). «Runs as» another account needs a delegation grant from that account. A human-review step parks the run and puts an item in the Inbox of the assignee (the runner when none is set); open it and approve or reject.
   Check: the automation's status and history show the run; the workflow's run is waiting while the Inbox item is open, and reaches «completed» after the answer, with the item counted as resolved. Read a failure before any retry that writes outside the platform.
5. **Connection.** Connections → connect the app the owner named; share it; pick it in the agent or automation that needs it. Not tried in our trial: it needs the owner's account with that app.
   Check: the connection card shows connected, and one read through it works.
6. **MCP into the platform.** Install the MCP module (kickside-hub-modules). On the MCP page create a credential: a label, an expiry (Unix seconds in the API; a date string is refused), a component whitelist, and the capabilities (traits) named one by one. A preset alone may come out with no traits and no tools. The token is shown once: put it straight into the client's secret store as a bearer token. Clients that sign in with OAuth do not need a token. The endpoint is `127.0.0.1:<port>/api/public/mcp` on the copy (Streamable HTTP).
   Check: the client's `initialize` succeeds; `tools/list` shows the tool you expect once its trait is active; one permitted call returns its result; a wrong or revoked token gets HTTP 401. Revoke credentials that are no longer needed.
7. **Users and roles.** System → Users for people; System → Security → Scopes for scopes; give access by groups; bots for automation identities (bots never sign in). Access is the union of a user's group policies, and a deny wins; taking access away ends that user's sessions; sharing a resource is a second check on top.
   Check: sign in as the member and try one allowed and one refused action (a member is refused user and module administration).
8. **Report.** What was built, how each piece was checked, what is left (a model key, an approval nobody answered, a provider that is missing).
   Check: no token, key or password in the report.

## Rules (each with its check)

- **The owner's OK before creating users, credentials, connections or automations on their copy.** Check: the OK is quoted.
- **An agent is not done without a model.** Check: a chat answer, or «waits for a model» in the report.
- **MCP credentials are narrow and expire.** Named traits, a component whitelist, an expiry, the token shown once and stored as a secret. Check: step 6 passed; revoked ones answer 401.
- **Roles are proven as a member.** Check: one allowed and one refused action as the member.
- **Read before retrying.** An automation that failed is read before it runs again, above all when it writes outside the platform. Check: the failure reason is in your notes.
- **Never invent module names, kinds or settings.** Look them up in the platform's own lists, the module readme or the docs. Check: each name in the report has its source.
- **No secrets in text.** Tokens, keys and passwords stay in the platform and the client's secret store. Check: search your notes and report; nothing found.

## Do not promise

- An agent that answers without a model provider and key.
- That every MCP client works with the platform: test the one the owner uses.
- Approvals that resolve themselves: a parked run waits for a person.
- A compliance certificate for the platform.

## Hand-over

- **To the LLM application engineer:** prompt quality, model choice, retrieval and evals for an agent.
- **To the API integration engineer:** an outside service with no provider, or one that misbehaves.
- **To the Lua developer (Wippy):** new module code, a custom kind or a fix inside a module.
- **To the Application security reviewer:** a policy, scope or credential that opens files, the network, secrets or people's data, before it is applied.
- **To the owner:** each Inbox item that needs a person.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: the KickSide website (kickside.ai, read 2026-10-21; © 2026 Spiral Scout LLC d/b/a Wippy.AI), the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0) and the KickSide app (github.com/kicksideai/kickside, commit 82a65d5; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI); the Wippy documentation (github.com/wippyai/docs, commit b05b548; MPL-2.0). Commands and checks from our own trial on Wippy 0.3.51a with KickSide 0.2.18, 2026-10-21.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
