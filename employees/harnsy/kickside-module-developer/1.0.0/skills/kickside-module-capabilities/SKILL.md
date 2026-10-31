---
name: kickside-module-capabilities
description: Give a KickSide module its data and working parts - tables with migrations for SQLite and Postgres, one repository for the SQL, a status endpoint, automation ports, Blocks and agent tools that all call the same domain code, and tests in the harness that really run on both databases. Use when a module needs a table, a migration, a status API, a workflow step, an automation destination or a tool for agents and MCP.
---

# Tables, status, Blocks, ports and agent tools

A module earns its place by what it stores and what it lets people, automations and agents do. KickSide has a separate surface for each caller: an HTTP endpoint for the page, an automation port for ongoing automations, a Block for a step in a workflow, a tool for an agent or an MCP client. This skill keeps one rule above the others: **one capability, one implementation.** Every surface calls the same domain code in `persist/` or a service, so access checks, events and data stay the same whoever calls.

**Route:** the task's acceptance criteria → kickside-module-template (a module that loads) → **kickside-module-capabilities** → kickside-endpoints-access for the doors → kickside-module-release.
Before this skill: an initialized module that lints and tests green. After it: the new tables and surfaces, each with tests that ran on SQLite and Postgres.

Marks: «(read from Sx, not tried)» means the step was read in that source and not run by us; the Sources section at the end names each Sx. Only the template's own SQLite suite was run in our trial (S6).

## When to use

- A module needs to store something: a table, a column, a changed shape.
- A page needs a status or read endpoint.
- An automation must write into the module, a workflow needs a step, or an agent needs a tool.

## Inputs

- The task and its acceptance criteria (from the KickSide analyst when there is one).
- The template's own examples: its migration, repository, status endpoint, sink with its port, Block and tests.
- Docker on the machine for the Postgres suite.

## Steps

1. **Reuse before you build.** KickSide already owns knowledge bases, threads and events, components and sharing, connections, uploads, automations, the inbox, agents and models, settings, webhooks, MCP and workflows. Find the owner of a capability (the Hub module page, the installed registry, the handbook) and bind to it; build only what is specific to this module's domain.
   Check: your notes name the existing module you checked and why it does not cover the need.
2. **Write the migration twice.** Each migration lives in its own `function.lua`; set `meta.type: migration`, give it a `meta.timestamp` in UTC (ISO-8601 form), and let the module's `target_db` requirement pick the database. Inside, one block for `sqlite` and one for `postgres`, each with `up` and `down`, each in its own SQL dialect (a Postgres type such as `UUID` or `TIMESTAMPTZ` fails in the SQLite block; read from S1, the Postgres side not tried). Order comes from the timestamp, not from `depends_on`. Prefix table names with the module's namespace.
   Check: both blocks exist; a changed shape gets a new forward-only, idempotent migration that keeps existing rows, never an edit of a published one.
3. **Keep SQL in one repository.** One `library.lua` in `persist/` owns every query, with values passed as parameters and the database handle released on every path, errors included. Endpoints, sinks, Blocks and tools import it; none of them write SQL.
   Check: a search for SQL keywords outside `persist/` and `migrations/` finds nothing.
4. **A status endpoint.** The template's status handler is the pattern: it confirms an actor is present, reads one number through the repository and answers JSON; on a repository error it answers 500 with a message that carries no secret. Attach it to the authenticated router (kickside-endpoints-access).
   Check: as a member it answers 200 with the module's numbers; without a session the router refuses it.
5. **An automation port when an automation writes in.** A `registry.entry` with `meta.type: kickside.automation.port` names its `binding`, its `config_schema`, `input_schema` and `operations` as top-level fields; the `contract.binding` behind it implements the writable contract with `meta.delivery` and `meta.input_shape`. A writable sink must handle a redelivery: same idempotency key, same result, no second row.
   Check: tests cover one write, a duplicate key, a changed payload under the same key and a redelivery.
6. **A Block when a workflow needs a step.** Declare it as a `registry.entry`; its `meta.type` is `kickside.block` and its `data.block.api_version` is `kickside.block/v1`. Give `input`, `config` and `output` each an object schema, pair the `error` schema with a `failed` port, list the `out` ports yourself, presentation fields and exactly one execution target. The function receives `{input, config}` and calls the same repository or service as the endpoint. Blocks run under the caller's identity.
   Check: a test executes the Block's function and reads the persisted result; the `failed` port and the `error` schema are declared together.
7. **A tool when an agent or an MCP client needs it.** (Read from S1, not tried.) Write the tool as its own `function.lua` and set `meta.type: tool` there, plus `meta.llm_alias`, `meta.llm_description`, `meta.input_schema` and `meta.output_schema` as JSON strings, and `meta.mcp.required_scopes`. Put it on agents through a trait (`registry.entry`, `meta.type: agent.trait`, under `src/traits/`) whose `tools` list names it. The tool returns `(result, err)` with typed errors, checks the actor, and checks component access for any id it is given: an id in the prompt is not authorization. Give tools their own access policy (kickside-endpoints-access) rather than folding them into member access.
   Check: a test calls the tool as an actor and gets the result, and a call without an actor or with someone else's component id is refused.
8. **Errors carry a kind.** Return errors only as Wippy's own error values, each with the kind that fits, and, after a side effect that must not repeat, an explicit `retryable = false`. Callers branch on the kind or a code in the details, never on message text.
   Check: tests assert the kind of each refusal, not its words.
9. **Tests that really run.** Each test entry has `meta.type: test`, `method: run` and imports the test runner; the file must hand its cases to the runner's wrapper, or nothing executes. Add wiring tests for exact ids and references, behaviour tests for each surface, and a test for refused paths. Then run the SQLite suite with `make test`, and for Postgres start the database (`make postgres-up`), run `make test-pg` and stop it again (`make postgres-down`). The SQLite run (`make test`) was tried; the Postgres targets were read from S2 and never run by us, so the first Postgres run on a module is itself a check to report.
   Check: the run prints the case count you expect on both databases; break one new test on purpose once and see it fail.
10. **Check it live.** Restart the development copy from the checkout (kickside-module-template), call the endpoint, run the Block in a workflow or the tool from an agent, and read the stored row through the status endpoint (read from S1, not tried).
   Check: the live answers are in the report. The template's test harness gives its actor a permissive scope (read from S2), so a green suite says nothing about member access: that check is in kickside-endpoints-access.

## Rules (each with its check)

- **Both engines, every data change.** Check: SQLite and Postgres runs, with counts, are in the report.
- **Published migrations never change.** Check: the diff adds migrations, it does not edit released ones.
- **Product defaults are registry entries, not seed SQL.** Check: no `INSERT` of catalog data in a migration.
- **One implementation per capability.** Check: the endpoint, port, Block and tool import the same domain call.
- **No secret in a test, fixture or log line.** Check: a search of `test/` and the logs for key-like strings finds nothing.
- **Never weaken a test to land a change.** Check: no test deleted or loosened without a reason in the report.

## Do not promise

- That a green harness proves access: its actor has a permissive scope.
- That a Block appears in the visual editor: the visual Workflows module is optional; the Block works headless.
- That a migration's `down` restores data: it restores shape where it can.

## Hand-over

- **To the Lua developer (Wippy):** a supervised process or long-running service, a message protocol between processes, a Lua dialect question, a runtime fault, a Wippy app that is not a KickSide module. Lua handlers inside the module's own entry kinds (api, persist, migrations, security, sink, blocks, traits) stay with you.
- **To the KickSide frontend developer:** the page that shows the data, with the endpoint contracts.
- **To the KickSide QA tester:** the acceptance check under each role, in the browser and after a restart.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no code or text taken. S1: the KickSide developer handbook, pages on testing and migrations, conventions, Blocks and ports, agents and tools, module layout (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI). S2: the KickSide module template, its Makefile, migration, repository, status endpoint, sink, Block and test harness (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy). S4: the Wippy documentation pages framework/testing and framework/migration (wippy.ai, read 2026-10-23; MPL-2.0). S6: our own trial with Wippy 0.3.52a, 2026-10-23: the template's SQLite suite ran green; the Postgres suite was not run.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
