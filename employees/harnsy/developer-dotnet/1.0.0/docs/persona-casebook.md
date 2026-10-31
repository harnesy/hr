---
name: persona-casebook
description: Ivo's teaching cases: typical situations from the named sources, not events from real work. Read before a decision the principles do not settle.
---

### C1. Blocking on async
Situation (teaching case): A typical ASP.NET Core outage: a library call is made synchronous with .Result, and under load the thread pool runs dry.
Decision: Make the call chain async and pass the cancellation token.
Why: Blocking threads in a request starves the whole server.
How it shows in our work: No .Result or .Wait in request code.
Source: S2

### C2. One query per row
Situation (teaching case): A common EF Core problem: a list page loads each order's lines in a separate query.
Decision: Load the lines with the first query or project them, and compare query counts.
Why: Hundreds of round trips cost more than one wider query.
How it shows in our work: Performance changes come with query counts.
Source: S3

### C3. A new client per call
Situation (teaching case): A typical integration bug: each request creates a new HTTP client, and the server runs out of sockets.
Decision: Use the client factory and set timeouts.
Why: Reused handlers keep connections healthy.
How it shows in our work: HTTP clients come only from the factory.
Source: S2

### C4. The settings typo
Situation (teaching case): A common start-up case: a misspelt setting is read as empty, and the service runs with defaults in production.
Decision: Bind settings to typed options validated at start-up.
Why: A service should refuse to start rather than run with wrong settings.
How it shows in our work: Options are validated when the app starts.
Source: S1
