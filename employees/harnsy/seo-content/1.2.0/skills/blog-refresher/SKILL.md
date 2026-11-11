---
name: blog-refresher
description: Refresh an existing blog post or article that has slipped behind the pages above it; audit the post, read the pages that rank now with real search and fetch tools, build a gap table, agree a plan with the page owner, then draft the updated version in the original voice. Use when someone asks to update, refresh or improve an existing post, to recover lost positions, or asks why a post fell behind. Drafts only, no ranking or traffic promises.
---

# Blog refresher

An existing post already has a URL, some links and a position. A refresh keeps all three and closes the gap with the pages that rank above it. The work is an audit of the post, a reading of the current results, a gap table, a plan the page owner approves, and only then a new draft that still sounds like the original.

**Route:** the post and its query → who owns the query → audit of the post → the pages that rank now → gap table → plan → the owner's approval → draft → hand-over.
Before this skill: the post's URL or text, its main query, and search console data if the owner gave access. After it: a draft and a publisher's note; a person reviews and publishes.

## When to use

- A post that used to rank has slipped, or sits in positions eight to twenty.
- The facts, numbers, screenshots or examples in a post are out of date.
- Someone asks why a post fell behind the pages above it.
- Not for a new article (write a brief instead), and not when another page of ours already owns the query: then propose a merge.

## Inputs

- The post: URL and text, title, main query, the date of the last real update.
- Search console data for the page (queries, positions, clicks, the date range), if access was given. Without it, say «position not verified».
- The query ownership map from the technical SEO specialist.
- A search tool and a page fetcher. Without them this skill cannot read the current results; say so and stop at the audit of the post.

## Rules

- **Read, do not remember.** What ranks and what those pages say comes from a search and a fetch made today, never from memory. Write the date of the check.
- **Check ownership first.** If another page of ours gets the impressions for the query, the answer is a merge and a redirect proposal, not a refresh.
- **A refresh adds substance.** New data, a missing section, a corrected answer, a better example. A «Last updated» date changes only when the content did. A new date on old text is fake freshness.
- **Length is an observation, not a target.** Note how long the ranking pages are; never set a word count to reach.
- **Nothing invented.** No made-up statistics, quotes, customers, reviews or sources. Every number carries its source and its date. If the fact cannot be sourced, leave it out and list it as a question for the owner.
- **Read competitors for coverage, never for text.** Take what topics they cover, not their sentences, tables or images.
- **Keep the URL.** A change of URL, a merge or a redirect of a page that has traffic or links needs the owner's OK and goes through the technical SEO specialist.
- **Approval before writing.** Show the plan and wait for the page owner's yes.
- **No promises.** Never promise a position, a traffic figure or a date. Say what will be measured and when.
- **Drafts only.** A person reviews and publishes. The publisher's note says an AI agent drafted the refresh.

## Steps

1. **Check who owns the query.** Look at the ownership map or the search console data. One query, one page of ours. If this post is not the owner, stop and propose the merge.

2. **Audit the post.** Fill this in from the page itself:
   ```
   Title, URL, main query
   Last real update
   Position, clicks, impressions (source, date range) or «not verified»
   Headings: H2 and H3 list
   Lists, tables, images, internal and outgoing links
   Keep: sections that answer well, the angle only we have
   Fix: outdated facts, missing topics, a buried answer, broken links
   Quick wins: what a small edit would already improve
   ```

3. **Read the pages that rank now.** Search the main query. Record the titles of the first ten results, the format most of them share (list, guide, comparison, tool), and the questions the results page itself suggests. Pick up to five pages to read in full: the first three, plus any recently updated or close in audience to ours. For each note the position, the headings, what it has that others lack (own data, examples, visuals, a tool) and its visible update date.

4. **Build the gap table.** One row per topic or element, one column per page:

   | Element | Our post | Page 1 | Page 2 | Page 3 | Priority |
   | --- | --- | --- | --- | --- | --- |
   | Answer in the first screen | | | | | |
   | [Topic] | | | | | |
   | Data with a source and date | | | | | |
   | Worked example | | | | | |
   | Table or comparison | | | | | |
   | Questions answered | | | | | |

   Priority: high when most of the pages read cover it, medium when two or three do, low when one does. Add a last row, «nobody covers», for the angle that would make our post the one worth reading. A gap every page shares is not a reason to copy it: say in one sentence what our post adds.

5. **Write the plan.** Keep it short:
   ```
   Refresh plan: [post title]
   Where it stands: position and clicks with source and dates, or «not verified»
   Findings: the three main gaps, what is outdated, our angle
   Outline: each H2 marked keep, change or new, with the change in one line
   Title: keep, or up to three options (use the seo-title-optimization skill)
   New elements: table, example, questions section, diagram
   Needed from the owner: facts, numbers, screenshots only they have
   Measure: baseline today, judge three to four weeks after publishing
   ```

6. **Get the owner's approval.** Send the plan and the gap table. Ask which sections matter most. Do not draft before the yes.

7. **Draft the refresh.**
   - Keep the sections that work, the voice, the URL and the heading anchors other pages link to.
   - Put the answer to the main query in the first paragraph.
   - Add the high-priority gaps and the angle nobody covers.
   - Give each number its source and year; replace or remove what cannot be sourced.
   - Short paragraphs, descriptive H3s, lists and tables where they help the reader scan, jump links in a long post.
   - Use related terms the way a person who knows the subject would; never repeat the query to fill space.
   - Add a questions section only for questions the post really answers.

## Output

```markdown
# [Title]

_Last updated: [date of this real update]_

[Intro with the answer]

[Refreshed sections]

---

Publisher's note
- Drafted by an AI agent; review before publishing.
- Description: [new text]
- Internal links: [from which pages, to which pages]
- Images or screenshots needed: [list]
- Markup worth adding, only for visible content: [types] (for the technical SEO specialist)
- URL: keep
- Sections added, changed, removed: [list]
- Open questions and facts not verified: [list]
- Baseline: [position, clicks, impressions, date range, source]
```

## Checks before hand-over

1. The ownership check is written down, with its source.
2. Every row of the gap table is either addressed in the draft or marked as skipped with a reason.
3. Every number in the draft has a source and a date; nothing is invented.
4. The «Last updated» line matches a real change of content.
5. No sentence, table or image is lifted from a competitor's page.
6. The voice matches the original post; the URL and linked anchors are unchanged.
7. The note lists what was not verified and what the owner must supply.

## Hand-over

- **To the page owner or editor:** the draft, the gap table and the publisher's note, for review and publishing.
- **To the technical SEO specialist:** markup needs, a merge or redirect proposal, and the baseline to judge against.
- **To the marketing lead:** the list of posts where no gap could be named; the limit there is likely trust and links, not text.

## How far proven

Not run live by us. This skill is adapted from its source and checked by review, not yet used by harnsy on a real post. Treat the first run as a trial and report what did not fit.

## Sources

This skill is made by harnsy; no endorsement by Ilias Ism or any project named is implied.

Built on the «blog-refresher» skill from seo-skills by Ilias Ism (https://il.ly; github.com/Illyism/seo-skills, commit 11c4f94 of 30 October 2026; MIT licence as stated in that repository's README, see LICENSE in this folder), adapted: the six phases are kept; the ownership check, the rule that length is no target, the real-update rule, the sourcing rules and the hand-overs are ours.

Text © 2026 Pavel Buchnev (harnsy), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), except the parts adapted from the seo-skills skill, which stay under the MIT licence in LICENSE. The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
