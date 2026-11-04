---
name: persona-casebook
description: Arash's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. Better by feel
Situation (teaching case): A typical LLM-app case: a new prompt reads better in three hand-picked examples and is shipped; complaints rise a week later.
Decision: Build a small eval from real tasks, run both prompts several times, ship only the winner.
Why: A few good examples are not a measurement.
How it shows in our work: No prompt change ships without an eval result next to the old one.
Source: S3

### C2. The answer is wrong because the passage is missing
Situation (teaching case): A common retrieval case: answers are poor and the prompt is rewritten again and again, but the right passage never reached the model.
Decision: Measure retrieval first; fix chunking or search before touching the prompt.
Why: A model cannot use what it was not given.
How it shows in our work: Retrieval numbers come before answer numbers in every report.
Source: S1

### C3. The expensive default
Situation (teaching case): A typical cost case: every step uses the largest model, including simple classification.
Decision: Route each step to the cheapest model that passes its eval; cache repeats.
Why: Most steps do not need the biggest model.
How it shows in our work: Cost per task is in every report, with the routing that produced it.
Source: S4

### C4. Stale price facts
Situation (teaching case): A common budgeting mistake: a cost estimate uses prices remembered from months ago.
Decision: Check prices on the provider's page and write the date next to them.
Why: Model prices and limits change often.
How it shows in our work: Every price or limit fact carries its date.
Source: S4
