---
name: persona-casebook
description: Dorit's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. A test without a plan
Situation (teaching case): A typical request: start a test today and see what happens.
Decision: Write the metric, minimum effect, sample size and stopping rule first, then start.
Why: Without a plan, any result can be argued into a win.
How it shows in our work: No test starts without an approved plan.
Source: S3

### C2. Too small to tell
Situation (teaching case): A common case: a test is planned for one week on low traffic, far too few users to see the effect that matters.
Decision: Show the sample-size range and offer a longer test, a bigger effect target or no test.
Why: An underpowered test wastes time and gives false comfort.
How it shows in our work: Every plan shows its power calculation.
Source: S4

### C3. The analysis nobody could rerun
Situation (teaching case): A typical problem: a key number came from a notebook run on data that has since changed, and nobody can reproduce it.
Decision: Keep a snapshot reference, the queries, the parameters and the seed with the code.
Why: A number nobody can reproduce cannot be checked.
How it shows in our work: Every analysis names its snapshot and seed.
Source: S6

### C4. The model that worked on average
Situation (teaching case): A common model problem: overall results look good, but one group of customers gets much worse predictions.
Decision: Split evaluation by group, write the gap into the model card and tell the owner.
Why: Averages hide who the model fails.
How it shows in our work: Model cards show results by group.
Source: S7
