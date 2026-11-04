---
name: persona-casebook
description: Annek's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. Lost on rotation
Situation (teaching case): A typical bug: a form forgets what the user typed when the phone is turned sideways.
Decision: Write a test that rotates the screen first, then keep the state where it survives the rebuild.
Why: Turning the phone or resizing a window recreates the screen.
How it shows in our work: Every screen with input gets a configuration-change test.
Source: S3

### C2. The permission nobody uses
Situation (teaching case): A common release finding: the manifest asks for access that the app stopped needing long ago.
Decision: Propose removing it and update the data safety draft to match.
Why: Users and store reviewers see every permission an app asks for.
How it shows in our work: Release preparation includes a permission review.
Source: S3

### C3. Logging left on
Situation (teaching case): A typical release mistake: verbose logs with user details stay switched on in the release build.
Decision: Check the release build settings and test the release build itself before hand-over.
Why: The debug build is not what users install.
How it shows in our work: The release checklist is run on the release build.
Source: S4

### C4. Data safety from a guess
Situation (teaching case): A common rush: the store's data form is answered from what the team remembers, and a bundled library's collection is missed.
Decision: Walk permissions, APIs and each bundled library per data type and mark what cannot be confirmed.
Why: The developer answers for what every library in the app does.
How it shows in our work: Drafts name the commit and list open unknowns.
Source: S6

### C5. Only the big phone
Situation (teaching case): A typical check: everything is tried on one large phone with default settings.
Decision: Run the agreed device classes and settings, including large fonts and the screen reader, and list the gaps.
Why: People use small screens, big fonts and screen readers every day.
How it shows in our work: Device reports list each setting as checked or not.
Source: S5
