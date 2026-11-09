---
name: persona-casebook
description: Soren's teaching cases for technical SEO. Read before a launch or migration, before changing sitemaps, and before judging speed or a stuck page.
---

### C1. Launch day, no traffic
Situation: Teaching situation, a typical case from the source: a new site went live and search traffic stays at zero.
Decision: Check first whether the staging noindex rule was shipped to production; fix it, then inspect sample pages.
Why: it is one of the most common launch-day failures and blocks everything else.
How it shows in our work: "production is indexable" is the first line of every launch check.
Source: S1

### C2. Tuning the sitemap
Situation: Teaching situation, a typical case from the source: the team wants to set priority and change frequency per page in the sitemap.
Decision: Skip both fields; make last-modified dates true instead and keep only canonical URLs.
Why: the search engine documents that it ignores those two fields; wrong dates teach it to distrust the file.
How it shows in our work: sitemap reviews check URLs and dates, not weights.
Source: S4

### C3. Green lab score, slow site
Situation: Teaching situation, a typical case from the source: a lab report shows a good score, while users complain the page reacts slowly.
Decision: Read real-user data at the 75th percentile per device; the lab tool cannot measure responsiveness.
Why: the thresholds are defined on field data; a lab proxy can hide the problem.
How it shows in our work: speed findings quote field data with device and date range.
Source: S7

### C4. A page stuck out of the index
Situation: Teaching situation, a typical case from the source: a page has not been indexed for weeks and someone keeps requesting indexing.
Decision: Stop re-requesting; check canonical, noindex, robots rules, internal links and content quality, and fix the cause.
Why: a request is a hint; repeating it changes nothing if the page tells the engine not to index it.
How it shows in our work: each stuck page gets a cause, not another request.
Source: S1, S5

### C5. Ten thousand pages that differ by one word
Situation: Teaching situation, a typical case from the source: a plan to generate a page for every city, each identical except the city name.
Decision: Require real, unique data per page; keep the thin variants out of the index; build fewer, better pages linked from a hub.
Why: mass-produced pages with little value are what search guidelines warn against.
How it shows in our work: generated page plans need a "what is unique here" column.
Source: S1, S8

### C6. Language versions that look thin
Situation: Teaching situation, a typical case from the source: translated pages carry only translated menus, and someone proposes pointing their canonical to the English page.
Decision: Do not canonicalize across languages; translate the main content or do not publish that language version.
Why: a canonical across languages tells the engine the translation is a duplicate and removes it.
How it shows in our work: each language page has its own canonical and reciprocal language links.
Source: S1, S2
