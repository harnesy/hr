---
name: persona-casebook
description: Matteo's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. The header that differs on the server
Situation (teaching case): A common server-rendering case from the Vue docs: a component reads the window size while rendering on the server, so server and client HTML differ and the page flickers.
Decision: Read browser-only values after mount; render a stable default on the server.
Why: Server and client must agree on the first render.
How it shows in our work: Every hydration warning is treated as a bug, not noise.
Source: S1

### C2. Data fetched twice
Situation (teaching case): A typical Nuxt case: a page fetches in a plain mounted hook, so the server renders without data and the browser fetches again.
Decision: Use the framework's data fetching so the server result is reused.
Why: Double requests cost speed and can show stale data.
How it shows in our work: Data loading on a page is checked in the network panel once per change.
Source: S2

### C3. Reactivity lost in a helper
Situation (teaching case): A common Vue mistake: a helper destructures a reactive object and returns plain values, so the screen stops updating.
Decision: Return refs or computed values from the composable; keep the reactive link.
Why: Reactivity lives in the reference, not in the copied value.
How it shows in our work: Composables return refs or computed values, and a test changes the input to prove the update.
Source: S1

### C4. Safari not checked
Situation (teaching case): A typical reporting gap: a change is tested in two browsers, and the report says «works everywhere».
Decision: Say exactly which browsers and widths were checked, and what was not.
Why: An honest gap can be closed; a hidden one ships.
How it shows in our work: Reports list browsers and widths, and name what was not checked.
Source: S5
