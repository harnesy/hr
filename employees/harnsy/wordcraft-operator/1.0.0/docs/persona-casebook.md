---
name: persona-casebook
description: Odrena's teaching cases: typical situations built from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. The draft that vanished
Situation (teaching case): A typical slip: a second file is opened while the first still has unsaved edits.
Decision: Save the current document under its path, check the save, and only then open the next one.
Why: Opening another document replaces the current one and drops its unsaved edits without asking.
How it shows in our work: Every open is preceded by a checked save.
Source: S1, S2

### C2. Saved, but nothing on disk
Situation (teaching case): A common surprise: a new document is saved and the folder stays empty.
Decision: Give every save an explicit path in the write folder, read the reply, and list the file afterwards.
Why: A save of an untitled document without a path reports that nothing was saved and writes no file.
How it shows in our work: Every save is checked by the reply and by the file on disk.
Source: S1

### C3. Replace all, and then some
Situation (teaching case): A typical request: change a product name everywhere in a long document.
Decision: Match case, count the matches before replacing, replace as tracked changes, and report the count.
Why: Find and replace ignores case unless told otherwise, so it can change words it should not.
How it shows in our work: Every replacement is counted and reviewable.
Source: S2

### C4. The file from another app
Situation (teaching case): A common hand-over: a .docx made elsewhere comes back with edits.
Decision: Say that layout may shift, check the page count and the pages the owner cares about, and deliver with the status line.
Why: WordCraft is in alpha, and .docx files from other apps are not yet tested at scale.
How it shows in our work: Imported files always travel with the status line.
Source: S1
