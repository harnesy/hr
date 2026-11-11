---
name: seo-title-optimization
description: Audit and rewrite page titles for search; title tags, frontmatter titles, their fit with the H1, and bulk title reviews across many pages, with the query ownership checked first and a baseline recorded. Use when someone mentions titles, title tags, titles in search results, click rate, truncation, or asks to improve titles across pages. Proposals for the page owner to approve; no ranking or click promises.
---

# SEO title optimization

A title has two jobs: tell the search engine which query the page answers, and give the searcher a reason to choose it. This skill reviews one title or many, and returns options the page owner can approve quickly.

**Route:** the page and its query → who owns the query → what the results page shows → pattern → three to five options → pick → table for the owner → baseline → check after three to four weeks.
Before this skill: the page, its current title and H1, and the query ownership map. After it: approved titles go to whoever edits the pages; the baseline goes to the technical SEO specialist.

## When to use

- A page ranks but few people click it.
- Titles are vague («Home», «Products»), duplicated, bloated or cut off in the results.
- A bulk review of titles across a section or a whole blog.
- A brief or a refresh needs title options.
- Not a fix for a page that does not answer the query: that is a content problem.

## Inputs

- The page URL, its current title, H1, description and URL slug.
- The main query, or enough of the page to infer it (say that it was inferred).
- The query ownership map from the technical SEO specialist.
- Search console data for the page (position, impressions, click rate, date range), if access was given.
- A search tool to read the current results. Without it, say the options were not compared with the results page.

## Rules

- **The results page is the brief.** Do not write titles from taste. Read what ranks for the query today and what those titles have in common.
- **Ownership before any change.** Check which of our pages gets the impressions for the query. Never give two pages titles that chase the same query; the technical SEO specialist keeps the map and settles conflicts.
- **The title describes this page.** A number, a year, «free», «complete» or «best» appears only if the page delivers it. A year goes in the title only when the page was really updated for that year.
- **Clarity over keywords.** The query once, near the front, in natural word order. No lists of keywords, no repeats.
- **Every title unique** across the pages we own.
- **Leave the slug alone.** Do not change a live URL to match a title. Change the H1 or description only when asked or when the mismatch clearly confuses the reader, and say so in the table.
- **One change, one baseline.** Record position, impressions and click rate before the change. Do not edit the body in the same round. Judge after three to four weeks.
- **No promises.** A title can earn more clicks; nobody can promise a click rate or a position.
- **Proposals only.** The page owner approves; a person or engineering publishes.

## Steps

1. **Find the main query.** Take it from the brief or the ownership map. If you infer it from the title, slug, H1 and content, mark it «inferred».

2. **Name the intent and the page type.** Informational, commercial, transactional, local or navigational; and the type: product, pricing, comparison, docs, support, guide, definition, how-to, list, checklist.

3. **Read the results page**, if a search tool is there. Note repeated structures, modifiers, the usual length, and what none of the titles say. If most results are a different page type from ours, report that first: a title will not fix a mismatch of intent.

4. **Choose one pattern** that fits the intent:

   | Page | Pattern |
   | --- | --- |
   | Product or category | [What it is] for [audience] |
   | Pricing | [Product] pricing |
   | Comparison | [A] vs [B]: [what the reader decides] |
   | Definition | What is [term]? [and what the page adds] |
   | How-to | How to [task], optionally [without the usual obstacle] |
   | Guide | [Topic]: a guide for [audience or level] |
   | List | [Number] [things] for [audience or use] |
   | Checklist | [Topic] checklist: [number] checks for [outcome] |
   | Problem | How to fix [problem], or what [error] means |

   One pattern per title. The base formula is the query first, then the reason to click, then the brand if there is room.

5. **Draft three to five options.** Keep the words that matter in roughly the first 50 characters: search engines cut long titles by width, so a strict character limit does not exist, and 40 to 60 characters is a working range, not a rule. Avoid hype words such as «shocking» or «guaranteed».

6. **Pick one** that is accurate, clear and different from what already ranks. Check it against the H1 and the description: all three speak about the same topic, not necessarily in the same words.

7. **Return the table and record the baseline.**

## Common fixes

| Problem | Before | After |
| --- | --- | --- |
| Too vague | Home | Appointment booking software for dental clinics |
| Bloated | The ultimate complete guide to all the many benefits of standing desks for offices | 7 standing desk benefits for office teams |
| Wrong intent | Plans for growing teams | Booking software pricing |
| Promise the page does not keep | 25 free invoice templates (the page has 9, two of them free) | 9 invoice templates, 2 free |

## Output

One title: the options, the pick and one line of reasoning.

Many pages:

```markdown
| Page | Query (owner checked) | Current title | Proposed title | Why | Other fields to change |
| --- | --- | --- | --- | --- | --- |
| /pricing | booking software pricing (yes) | Plans for growing teams | Booking software pricing | Matches the query and the page type | none |
```

Below the table: the pattern used, the pages left alone and why, conflicts where two pages want one query, and the baseline with its date range and source.

## Checks before hand-over

1. Each proposed title names something the page really contains.
2. No two pages of ours share a title or chase the same query.
3. The main query appears once, near the front, in natural order.
4. Years, numbers and «free» are true for the page today.
5. No slug changed; any H1 or description change is listed and explained.
6. The baseline is recorded, or marked «not verified» with the reason.

## Hand-over

- **To the page owner:** the table to approve or edit.
- **To the technical SEO specialist:** ownership conflicts and the baseline; they judge the change after three to four weeks.
- **To the writer or engineering:** approved titles, with the exact field to edit.

## How far proven

Not run live by us. This skill is adapted from its source and checked by review, not yet used by harnsy on a real set of pages. Treat the first run as a trial and report what did not fit.

## Sources

This skill is made by harnsy; no endorsement by Ilias Ism or any project named is implied.

Built on the «seo-title-optimization» skill from seo-skills by Ilias Ism (https://il.ly; github.com/Illyism/seo-skills, commit 11c4f94 of 30 October 2026; MIT licence as stated in that repository's README, see LICENSE in this folder), adapted: the workflow and the idea of one pattern per intent are kept; the ownership check, the truth rule for years and numbers, the baseline, the examples and the hand-overs are ours.

Text © 2026 Pavel Buchnev (harnsy), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), except the parts adapted from the seo-skills skill, which stay under the MIT licence in LICENSE. The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
