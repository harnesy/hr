---
name: plugin-card-check
description: Check a harnsy plugin's catalog card against the plugin itself: run harnsy plugin check --json on the exact version, list the card's claims, match each to a line of the output in a claim → evidence → ok/fix table, and write what a person sees when enabling it (each right in plain words, the linked sentence, whether a consent tick is needed). Use for every plugin submission, and when a person asks whether to enable a plugin.
---

# Plugin card check

A plugin card is what a person reads before enabling code in their project. This skill makes sure the card says exactly what the plugin does and asks: no right left out, no right the code does not use, no promise the plugin does not keep. The plugin check's output is the evidence; the author's words are claims to test against it.

**Route:** the submission (plugin folder, card text, screenshots) → **plugin-card-check** → plugin-submission-report → the person's decision.

This skill does not review code and does not judge whether the plugin is safe. Looking up which operation a script calls for a need is a lookup, not a review; the code review is the catalog's code reviewer's step.

## 1. Run the check

```sh
harnsy plugin check /abs/path/to/<name>/<version> --json --publisher <publisher>
harnsy --version
```

- The folder path must be absolute; a relative one answers `plugin_not_found`.
- Use the harnsy the catalog uses (or the person's harnsy, when they ask whether to enable it) and write its version in the report.
- `--publisher` gives the real `id` and the `manifest_sha256`; without it the id reads `local/<name>`.
- Exit 0 is good, 1 refused, 2 usage. Keep the whole JSON with the report.

The answer: `ok`, `error {code, message}` when refused, `id`, `version`, `manifest_sha256`, `harnsy` (the plugin's own minimum), `needs`, `linked`, `entries [{kind, name, title}]`, `files [{name, sha256, size}]`.

**A refused check stops the table.** Quote the error line as it is (code and message) with the harnsy version; that is the finding for the author. `plugin_kind_unknown` or a need the check does not know means the plugin needs a newer harnsy («upgrade harnsy»): the people who would see it cannot install it yet.

## 2. List the card's claims

Collect every sentence that says what the plugin does, asks or does not do: the card text, the README, the comments at the top of `plugin.yaml`. One claim per row; «does not» claims count too («no network», «does not read your files»).

## 3. Match each claim to the output

| Claim (the card's words) | Evidence (output line, or the call in a script) | Result |
| --- | --- | --- |
| Adds a project page «Deals» | `entries`: `{kind: page, name: deals}` | ok |
| «No network» | `needs` has `http:stats.example.com` | fix |

Then the other direction: every line of the output must appear in the card.

- **Every need**, named in plain words:

  | Need | In plain words |
  | --- | --- |
  | `items.read` | reads the project's items |
  | `items.write` | writes to the project's items (notes, tags, check lines, new items, blocks) |
  | `send.role` | sends lines to roles of the project |
  | `agents.read` | sees which of the project's roles are online |
  | `files.read` | reads the project's files |
  | `files.write` | writes files into its own folder of the node's files |
  | `sql` | keeps its own database in this project |
  | `key:<name>` | uses a key you choose, for calls to the hosts that key allows |
  | `http:<host>` | sends https requests to `<host>` |
  | `mcp:<server>` | uses read-only tools of an MCP server you choose |
  | `chat:<name>` | writes to (and takes commands in) a bot chat you pick |
  | `feed:<name>` | reads mail from an Inbox feed you pick |
  | `sub:<publisher>/<plugin>/<channel>` | receives what another plugin publishes on that channel |

  A need not in this list is named as the check names it, with what harnsy's documentation says it opens.
- **Every host** from `http:` needs, by name.
- **Every entry**: a page, an action (and its schedule), an item hook (and its events), a check before a submit, a webhook hook, an http route, a feed hook, a background process, a chat command (and its commands), a chat reader.
- **Used, not just asked.** For each need, find the call that uses it in `lua/` or the page's `web/` (for example `harnsy.http.request` for `http:`, `harnsy.items.*` for `items.*`, `harnsy.sql.*` for `sql`). A need no script calls is a fix: the author removes it. Ask only for what is used.
- **No over-promise.** A «does not» claim that the output contradicts is a fix; so is a feature the entries do not have.

## 4. The enable view

Write what the person sees when enabling this version:

- **Rights in plain words**, one line each, from the table above, plus each page as «adds the page …». A page runs in the dashboard with the person's rights; the enable window says so for every plugin page.
- **The linked sentence.** When `linked` is true (it reads the project or a chat and sends out by key, host, MCP server or a second chat), one sentence as the person sees it: «Reads the project's items and sends them to api.github.com». When false, say «not linked».
- **Consent tick:** needed for a linked plugin that is not verified; not needed when it is not linked, or once the catalog has signed a code-reviewed version. Keys, hosts, chats and the enable itself stay the person's either way.

## Common misses

- An `http:` host left from an experiment, while the text says «no network»: unused, and it makes the plugin linked.
- `items.write` named as «reads items»: writing is a separate right; say what it writes.
- A chat command that answers in a second chat: that is linked; answering in the same chat alone is not.
- A schedule on an action not mentioned («every 1h»).
- A page's text that mentions a hook or action the plugin does not have.
- The card calls the plugin «safe» or «verified» before the code review.
- A version in the README that is not the checked one.
- Personal data stored and not said (an author's name from a chat message).
- Screenshots of another version, or with real names, emails or keys.

## Hand-over

The claim table, the enable view and the list of fixes go to plugin-submission-report. A claim you could not check is marked «not checked», with why.

## Sources

harnsy documentation 0.11.0: llms/plugins.txt, docs/plugin-v1.md, docs/plugin-page-v1.md, docs/plugin-catalog-v1.md (read 4 Nov 2026). Described in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. No scripts are carried with this skill.
