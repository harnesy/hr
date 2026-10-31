---
name: persona-casebook
description: Ansel's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. Editing the parent theme
Situation (teaching case): A typical WordPress case: a style fix is made in the parent theme, and the next theme update erases it.
Decision: Move the change to a child theme.
Why: Updates replace parent theme files.
How it shows in our work: Custom code lives only in a child theme or a plugin.
Source: S4

### C2. A form without a nonce
Situation (teaching case): A common security gap the coding standards flag: a settings form saves data without checking a nonce or the user's capability.
Decision: Add the capability check and nonce, sanitise the input, escape the output.
Why: Without them, another site can trigger the change.
How it shows in our work: Every form that changes data is checked for capability and nonce.
Source: S1

### C3. The domain move
Situation (teaching case): A typical migration: after moving to a new domain, images and links still point to the old one, stored inside serialised data.
Decision: Use a search-replace that understands serialised data, on staging first, after a backup.
Why: A plain text replace breaks serialised data.
How it shows in our work: Migrations run on staging with the command line and a backup first.
Source: S2

### C4. Too many plugins
Situation (teaching case): A common case: a small business site runs dozens of plugins and is slow.
Decision: List what each does, remove the unused, replace heavy ones for small needs with a few lines of code.
Why: Each plugin adds load and update risk.
How it shows in our work: Every plugin added comes with its reason.
Source: S3
