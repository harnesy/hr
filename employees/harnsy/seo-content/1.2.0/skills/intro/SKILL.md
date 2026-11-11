---
name: intro
description: Write a short opening for a blog post or guide; what the topic is, why it matters to this reader, and a teaser of what the article covers, matched to the article type (list, how-to, definition, or a piece that weighs evidence). Use when someone asks for a blog intro, an opening paragraph, an article lead, or the first lines of a brief's outline. Returns a draft, optionally with a slug, title and image alt text; never invents numbers.
---

# Blog intro

The first lines of an article decide whether the reader stays. A good intro says what the thing is, why it matters to this reader, and what the article will walk through, in about a hundred words. It also holds the passage that search results and AI answers are most likely to lift, so it has to be true on its own.

**Route:** the topic, the reader and the outline → article type → pattern → draft → check → hand-over.
Before this skill: a brief or an outline, or at least the topic, the reader and the main query. After it: a draft intro for the writer or editor.

## When to use

- A brief needs an opening, or a writer asks for one.
- A refreshed post buries its answer and needs a new first screen.
- An existing intro is long, vague or starts with how important the topic is.
- Not for the description shown in search results and not for social posts.

## Inputs

- Topic, main query and what the searcher wants (learn, compare, do, decide).
- The reader and their goal.
- The shape of the article: the count for a list, the H2 outline, or the key sections.
- The product angle, if the article has one.
- Optional: the chosen title, the slug, the subject of the main image.
- Any statistic to use, with its source and date. Without a source, the intro uses none.

If the outline or a draft is already there, use it. If the topic or the reader is unclear, ask one short question; otherwise propose and mark what you assumed.

## Rules

- **Answer first.** For a definition or a how-to, the first sentence is the definition or the task in plain words. Do not open with how important or fast-changing the topic is.
- **Short.** Two to four short paragraphs, about 80 to 120 words, unless asked for more. Sentences of roughly 8 to 15 words.
- **Why, then where we are going.** One or two sentences on what this means for the reader in practice, then a teaser that names the sections or outcomes ahead.
- **A list keeps its number.** If the title says seven, the intro says seven.
- **Nothing invented.** No made-up statistics, market shares, quotes or claims about competitors. A number appears only with the source and date the requester gave.
- **Plain voice.** Direct, practical, no hype words. Bold at most two to four words that carry the point; at most one aside in italics; never both on one phrase.
- **No heading inside the intro.** It is the first prose after the title.
- **The teaser tells the truth.** Each thing it names is a real section of the article, in the same order.
- **Do not rename a live page.** If the post is published, keep its slug.

## Patterns

Pick the one that fits the article.

**List** (for example «7 standing desk benefits for office teams»)
1. One sentence: what the thing is.
2. One sentence: why the usual choice is not enough, or why the list is worth reading.
3. The teaser: what the list covers and how it is ordered.
4. Optional: a jump link to the section most readers want.

**How-to or guide**
1. The task or problem in plain words.
2. Why it matters, in one or two short sentences.
3. Optional: three to five bullets with what the reader gets.
4. The teaser: the steps or cases covered.
5. One short line on what they can do by the end.

**Definition**
1. The term and a tight definition; spell out an acronym on first use.
2. One sentence on the need behind the search and the result.
3. Optional: a short list of what the practice involves.
4. The teaser: the main sections.

**Weighing evidence** (a topic people argue about)
1. The two loud positions the reader has heard.
2. What this article does instead: the method and the evidence it uses.
3. What the reader will be able to judge afterwards.
4. The questions answered, in the order of the H2s.

## Examples

These show tone and structure. Do not copy them.

List, «7 standing desk benefits for office teams»:

> A standing desk lets you switch between sitting and standing during the workday.
>
> Most offices buy them for comfort. The better reasons are less obvious.
>
> Below are **seven benefits** for office teams, ordered from the easiest to notice to the hardest to measure. Each comes with what to check before you buy.

How-to, «How to export invoices to a spreadsheet»:

> You can export every invoice to a spreadsheet in three steps.
>
> It matters at the end of each quarter, when your accountant asks for one file instead of forty PDFs.
>
> This guide covers the export itself, the columns you get, and what to do when totals do not match. By the end you will have a file your accountant can open.

Definition, «What is a canonical URL?»:

> A **canonical URL** is the one address you tell search engines to treat as the main version of a page.
>
> You need it when the same content can be reached at several addresses, for example with and without tracking parameters.
>
> This guide explains how search engines choose a canonical, how to set yours, and the three mistakes that make them ignore it.

## Output

By default return only the intro, as Markdown paragraphs ready to paste under the title.

When asked for everything:

```markdown
**Slug:** `[slug, or the existing one]`

**Title:** [title]

**Image alt:** [one sentence on what the image shows, under about 125 characters]

**Intro:**

[The intro]

**In this guide:**

- [Section or outcome 1](#its-heading-anchor)
- [Section or outcome 2](#its-heading-anchor)
- [Section or outcome 3](#its-heading-anchor)

[One short closing line, varied from article to article]
```

Link the bullets to heading anchors only when the headings are known; the anchors must match the page. For title options use the seo-title-optimization skill.

## Checks before hand-over

1. The pattern matches the article type and what the searcher wants.
2. The first two sentences stand alone and are true without the rest.
3. The reader can tell why this matters to them.
4. The teaser names real sections, in order.
5. No number without a source and date; nothing about competitors that is not sourced.
6. Within the length; short sentences; two to four bold words at most.
7. Assumptions are marked.

## Hand-over

- **To the writer or editor:** the intro, marked as a draft by an AI agent, with the assumptions listed.
- **To the page owner:** a proposed slug or title only as a suggestion; they decide.

## How far proven

Not run live by us. This skill is adapted from its source and checked by review, not yet used by harnsy on published articles. Treat the first run as a trial and report what did not fit.

## Sources

This skill is made by harnsy; no endorsement by Ilias Ism or any project named is implied.

Built on the «intro» skill from seo-skills by Ilias Ism (https://il.ly; github.com/Illyism/seo-skills, commit 11c4f94 of 30 October 2026; MIT licence as stated in that repository's README, see LICENSE in this folder), adapted: the four patterns, the length rules and the output fields are kept; the answer-first rule, the sourcing rule and the hand-overs are ours. The examples are written by harnsy; the source's example file is not used.

Text © 2026 Pavel Buchnev (harnsy), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), except the parts adapted from the seo-skills skill, which stay under the MIT licence in LICENSE. The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
