---
name: customer-journey
description: Map how buyers find, compare and choose a product across search engines, AI assistants and community platforms, through five awareness stages; for each stage the buyer's mindset, the questions they really type or ask, the content that answers them and the page of ours that owns it, or a gap. Use when someone asks about search intent, buyer journeys, awareness stages, what people ask AI assistants about a product, or what content to create for a product or a keyword list. The questions are hypotheses until checked against real data.
---

# Customer journey

People do not search one phrase and buy. They move from not knowing they have a problem to choosing a product, and at each stage they ask different questions in different places: a search engine, an AI assistant, a forum, a video platform. This skill maps those stages and questions, so the topic map covers the whole way and not only the last step.

**Route:** the product and its buyer → what sales and support hear → five stages → questions per stage and place → content and owning page per stage → gaps → hand-over to the topic map and the AI-answer check.
Before this skill: the product, its audience, and any real questions from customers. After it: a journey map that feeds the topic map and gives the technical SEO specialist the list of questions to ask AI assistants.

## When to use

- A new topic map, or a quarterly review of one.
- A keyword list with no structure: which stage does each query belong to?
- Someone asks what buyers ask AI assistants about the product or the category.
- The content covers only people ready to buy, or only beginners.

## Inputs

- The product in one sentence, who buys it and what counts as a conversion.
- Questions and objections from sales and support, and the themes of tickets. They come first.
- A keyword list or search console queries, if there is one.
- The pages we already have, with the query each one owns (from the technical SEO specialist).
- The business model and market. If nobody says, state your assumption at the top of the map; do not assume silently.

## Rules

- **Real questions first.** Start from what customers actually ask. Questions you compose are hypotheses: mark them, and check them against search console queries, ticket themes and sales notes where those exist.
- **Write questions the way people talk.** Full sentences with context, especially for AI assistants, where people explain their situation. Not keyword lists.
- **No invented demand.** Do not attach search volumes or percentages you did not get from a named tool with a date.
- **One owner per question.** Each question maps to one page of ours or is marked a gap. Two pages answering the same question is a merge to propose.
- **Research lightly and say what you checked.** A few searches to see what the results page shows for the main questions; note the date.
- **No promises about AI answers.** The map shows what people ask. It cannot make any assistant name or recommend the product.
- **Wrong or missing answers are fixed on our own pages.** State the fact plainly on the page that owns it. Never propose hidden text or instructions aimed at AI readers.

## The five stages

| Stage | The buyer's state | They ask about |
| --- | --- | --- |
| Unaware | Feels the symptom, has not named the problem | The symptom, their situation, how others work |
| Problem-aware | Can name the problem, does not know the ways to solve it | Causes, costs of the problem, whether it is worth solving |
| Solution-aware | Knows the kinds of solution, has no shortlist | Approaches compared, which kind fits their case |
| Product-aware | Knows our product and its rivals | Comparisons, alternatives, pricing, limits, reviews |
| Most aware | Wants to buy or has bought | Setup, migration, plans, integrations, proof it works for them |

## Steps

1. **Fix the context.** The product, the buyer, the conversion. Write the assumptions in one line.

2. **Collect the real questions.** From sales, support and search console data. Sort each into a stage.

3. **Fill each stage.** For every stage write:
   - the mindset in one or two sentences;
   - three to five questions as a person would type them into a search engine, and three to five as they would ask an AI assistant (longer, with their situation);
   - where else they look at this stage: forums, video, professional networks, review sites;
   - each question marked «from customers» or «hypothesis».

4. **Look at the results** for the main question of each stage. Note the page type that ranks (guide, comparison, tool, forum thread) and, if you asked an assistant, which kinds of sources it cited. Date the check.

5. **Map content to stages.** For each stage: the content type that fits (explainer, checklist, comparison, pricing page, setup guide, calculator), the page of ours that owns it, or «gap».

6. **Rank the gaps.** By closeness to the conversion and by how often the question comes from real customers. Stages near the purchase usually come first; a map with nothing for the early stages leaves the product unknown.

## Output

```markdown
# Customer journey: [product]

Assumptions: [buyer, market, conversion]. Checked on [date]. Sources: [sales notes, tickets, search console range].

## 1. Unaware
Mindset: ...
Search questions: ...
AI assistant questions: ...
Also looks at: ...
Content that fits: ...
Our page: [URL] or gap

## 2. Problem-aware
...

## Gaps, ranked
| Stage | Question | Source | Content to make | Why now |
| --- | --- | --- | --- | --- |

## Questions for the AI-answer check
[15 to 25 questions from the map, most from the last three stages]
```

## Checks before hand-over

1. Every stage has a mindset, questions for search and for AI assistants, and a content type.
2. Each question is marked «from customers» or «hypothesis».
3. No volume or percentage without a named source and date.
4. Each question has one owning page or is a gap.
5. The assumptions and the date of the check are at the top.

## Hand-over

- **To the marketing strategist:** the map and the ranked gaps, for approval into the topic map.
- **To the technical SEO specialist:** the questions for the AI-answer check and any question two pages of ours both answer.
- **To writers:** nothing yet; gaps become briefs first.
- **To sales and support:** the hypotheses, to confirm or strike out.

## How far proven

Not run live by us. This skill is adapted from its source and checked by review, not yet used by harnsy for a real product. Treat the first run as a trial and report what did not fit.

## Sources

This skill is made by harnsy; no endorsement by Ilias Ism or any project named is implied.

Built on the «customer-journey» skill from seo-skills by Ilias Ism (https://il.ly; github.com/Illyism/seo-skills, commit 11c4f94 of 30 October 2026; MIT licence as stated in that repository's README, see LICENSE in this folder), adapted: the five-stage process and the per-stage output are kept; the real-questions rule, the hypothesis marks, the owning page per question, the gap ranking and the hand-overs are ours. The five awareness stages are a long-standing copywriting model, used here as an idea.

Text © 2026 Pavel Buchnev (harnsy), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), except the parts adapted from the seo-skills skill, which stay under the MIT licence in LICENSE. The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
