---
name: persona-casebook
description: Mattis's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. The job that ran too early
Situation (teaching case): A typical queue bug: a job is dispatched inside a transaction and runs before the data it needs is committed.
Decision: Dispatch after commit and add a test.
Why: Workers can be faster than the request that queued them.
How it shows in our work: Jobs that read new data dispatch after commit.
Source: S2

### C2. One query per row
Situation (teaching case): A common list-page problem: a loop over records loads each one's relation separately.
Decision: Load the relation with the first query and check the query log.
Why: Round trips grow with the data; eager loading keeps them fixed.
How it shows in our work: List pages are checked in the query log.
Source: S2

### C3. Advice for the wrong version
Situation (teaching case): A typical mistake: a feature from a newer framework release is suggested for a project pinned to an older one.
Decision: Read the lock file first and use what that version offers.
Why: The project's versions, not memory, decide what works.
How it shows in our work: Every change states the framework version it targets.
Source: S4

### C4. The SDK everywhere
Situation (teaching case): A common maintenance trap: a payment or shipping SDK is called directly from many controllers.
Decision: Wrap it in one adapter and use that everywhere.
Why: One seam makes testing and replacing the provider simple.
How it shows in our work: Outside SDKs live behind adapters.
Source: S1
