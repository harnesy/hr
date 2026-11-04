---
name: decision-log
description: Keep a running register of decisions across topics for any leader or team (date, who decided, the decision, the reason, owner, review date, what it supersedes), each entry linked to its full record when one exists; append-only, with clashes sent back to the decider. Use whenever a named person makes a decision worth remembering.
---

# Decision log

A decision log answers «what did we decide, who decided, and why?» months later, after people have changed. It is one running register across all topics, short enough to scan. Each entry points to its full record where one exists.

**Route:** a decision made by a named person (in a meeting, a thread, a review) → **decision-log** → owners carry out follow-up actions → review on date → a changed decision gets a new entry that supersedes the old one.

## When to use

- A leader, a team lead or another named decider has made a decision others will rely on.
- Someone asks «did we decide this already?» or «why did we do it this way?».
- A plan or document is being changed because of a decision.
- A single architectural decision with options → `decision-record`. Log only its outcome here, in one line, and link to that record.

## Inputs

- Who the deciders are for which topics.
- Where full records live (decision records, meeting notes, documents).
- The existing log, if any.

## The entry

One row per decision:

- **id** and **date** decided;
- **decided by:** the named person (or people);
- **decision:** one sentence;
- **reason:** one or two lines;
- **options not chosen:** each with why it was rejected (short);
- **recommendation overridden:** if the decider chose against a recommendation, say so plainly;
- **owner** of carrying it out, and follow-up actions with owners and dates;
- **review date:** when to check it still holds;
- **supersedes / superseded by:** links to other entries;
- **status:** active, superseded, withdrawn;
- **link** to the full record, when one exists.

## Steps

1. **Log only decisions.** Raw discussion, opinions and proposals stay in meeting notes. An entry exists only once a named person has decided.
2. **Check before adding.** Read the active entries on the same topic. If the new decision contradicts one, or brings back an option that was rejected, stop and ask the decider which stands. Do not choose.
3. **Write the entry** with every field above. Unknown fields say «unknown, ask <name>».
4. **Never delete or rewrite an old entry.** A changed decision gets a new entry; the old one is marked superseded and both link to each other. Mark the old one only after the decider confirms.
5. **Follow through.** List every plan, document and message that depends on the decision, and update or flag each one. Note the dependent documents in the entry.
6. **Review on date.** When a review date arrives, ask the owner whether the decision still holds; record the answer as a new entry if anything changed.

## Rules

- The agent never decides, and never logs its own recommendation as a decision.
- The log is a record, not an announcement: nothing is sent from it unless the decider says so.

## Checks before hand-over

- Every entry names who decided and when.
- No active entries contradict each other.
- Superseded entries are linked both ways.
- Every follow-up action has an owner and a date.
- Every entry with a full record links to it.

## Artefacts

- `decisions/log.md` (or a table in the team's tracker): the running register.
- `decisions/clashes.md`: open questions sent to deciders, with dates.

## Hand-over

- **To the decider:** clashes and reopened options, for a decision.
- **To owners:** follow-up actions with dates.
- **To readers of dependent documents:** the list of documents updated or flagged.

## Sources

Adapted from the decision-logger skill in github.com/alirezarezvani/claude-skills, c-level-advisor folder (MIT, © 2025 Alireza Rezvani). Also built on the decision log pages of the Code-With Engineering Playbook (© Microsoft; CC BY 4.0) and the specialized-chief-of-staff agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors). All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
