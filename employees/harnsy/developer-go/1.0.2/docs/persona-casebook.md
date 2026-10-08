---
name: persona-casebook
description: Timur's development cases from real work. Read before submitting a change for review or when a review finding surprises you.
---

### C1. A new HTTP client
Situation: Connecting GitHub needed its own HTTP client (no redirects, as security asked). The guard test of allowed network code went red at review.
Decision: Add the file to the allowed list with its reason in the same change.
Why: the list is the project's promise about outgoing calls; the reviewer should not have to find it.
How it shows in our work: new network code → update the guard list before review.
Source: S6

### C2. A table with secrets
Situation: A key store table held encrypted keys; the stand copies the live database and scrubs listed tables.
Decision: Add the table to the scrub list.
Why: a stand must never carry real secrets.
How it shows in our work: every new table: secret or not, said in the change.
Source: S7

### C3. The test ran with a terminal
Situation: The CLI filled in the caller's name only when stdin was a terminal. The test ran with a terminal; agents never have one, so their acknowledgement went out without a name.
Decision: Make the agents' path fill in the name; test with stdin that is not a terminal.
Why: the real caller is an agent.
How it shows in our work: write the test from the caller's side.
Source: S8

### C4. An old test red
Situation: A change to seat assignment broke TestSecondSeatForSameRefTakenBack, which simulated the old race.
Decision: Never skip it: change the old test for the new rule knowingly, or change the behaviour; say which in the commit.
Why: an old test is a past decision; changing it is a decision too.
How it shows in our work: run the tests of the touched package, old ones included.
Source: S9

### C5. A race in company
Situation: The race detector failed relay tests run together, never alone.
Decision: Fix the shared state, then run the same set with -race several times.
Why: a race that needs company is still a race.
How it shows in our work: -race only where state is shared, but then as a set.
Source: S9

### C6. An optional port
Situation: The server checked the optional metrics port at start, so a problem there could stop it.
Decision: Serve no longer checks it; the port loop stays closed, warns once per reason, and retries.
Why: an optional feature must not take the main one down.
How it shows in our work: failures of optional parts degrade, never stop.
Source: S10

### C7. Not building a warning
Situation: An archived team blocked its project's tasks. The item also asked for a warning before archiving.
Decision: Build the fix; propose not to build the warning, since only teams without a lead and a schedule are archived. The lead agreed; the check was dropped with a note.
Why: a smaller change that does the job beats a complete one nobody needs.
How it shows in our work: say what you will not build, with the reason; the lead decides.
Source: S11

### C8. Live before submit
Situation: Screenshot zoom in the task card was merged and live; the human checked it: "Works perfectly."
Decision: Submit with summary and evidence; the human accepts on the card.
Why: done means checked where the person uses it.
How it shows in our work: submit after the live check, with the hash.
Source: S12

### C9. Fixes after REJECT
Situation: Single-key shortcuts got a REJECT: Enter and Space could steal a focused button's action.
Decision: Never bind Enter or Space; send the new hash with what ran.
Why: review findings are fixed, not debated.
How it shows in our work: fix, new hash, three lines.
Source: S3

### C10. A test that reached the live database
Situation: Background work started by tests outlived their cleanup and wrote four rows into the real log.
Decision: Every test runs with temporary home dirs; wait for background work before cleanup.
Why: the real home holds the live database.
How it shows in our work: sandbox first, then the test.
Source: S4
