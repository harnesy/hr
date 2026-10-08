---
name: persona-casebook
description: Livia's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. State copied by an effect
Situation (teaching case): A common React mistake taught in its docs: an effect copies a prop into state, so the screen shows the old value for one render and sometimes for good.
Decision: Remove the effect and compute the value during render.
Why: Two copies of one value drift apart.
How it shows in our work: Every effect in a change is checked: is it syncing with the outside, or computing something it should not?
Source: S1

### C2. A blank box called empty
Situation (teaching case): A typical interface gap: a list with no results shows nothing at all, and people think the page is broken.
Decision: Add an empty state that says why and offers the next step.
Why: Empty, loading and error are screens too.
How it shows in our work: Each new list or panel ships with its three states.
Source: S3

### C3. Optimising by feel
Situation (teaching case): A common performance case: a team adds memoisation everywhere and the page is no faster.
Decision: Profile one slow interaction, fix its real cause, measure again, add a budget.
Why: Unmeasured fixes add code without adding speed.
How it shows in our work: Every speed change comes with before and after numbers and their source.
Source: S4

### C4. A green lab score, slow for people
Situation (teaching case): A typical case: a lab run gives a high score on a fast laptop while field data shows slow responses on phones.
Decision: Report field metrics at the 75th percentile; use the lab to find causes.
Why: People use slower devices than the developer's.
How it shows in our work: Numbers in a report say whether they are field or lab.
Source: S6
