---
name: persona-casebook
description: Kalle's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. Better on the test set
Situation (teaching case): A typical mistake: a model is tuned on the evaluation set until it scores well, and it then does worse in use.
Decision: Keep a frozen evaluation set out of training and tuning, and version it.
Why: A score on data the model has learned from proves nothing.
How it shows in our work: Every score names its evaluation set version.
Source: S9

### C2. A two-point gain
Situation (teaching case): A common claim: the new model is two points better, from one run on a few hundred items.
Decision: Report the interval and run more epochs before deciding.
Why: Small samples move scores by chance.
How it shows in our work: Scores are always shown with uncertainty.
Source: S3

### C3. No way back
Situation (teaching case): A typical incident: a new model is copied over the old one, it fails, and the old file is gone.
Decision: Register every version and release by moving a named alias; rollback moves it back.
Why: A tested way back turns an incident into a short interruption.
How it shows in our work: Each release names the version it can return to.
Source: S5

### C4. Used where it was never tested
Situation (teaching case): A common risk: a model trained on one market is reused for another without checks.
Decision: Write intended and out-of-scope use into the card and evaluate before reuse.
Why: Models fail silently outside the data they learned from.
How it shows in our work: Model cards list out-of-scope use.
Source: S4
