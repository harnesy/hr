---
name: handbook-section
description: Write or update one employee handbook page so people can find and follow it, with an owner and a review date, and remove the pages it replaces. Use when a company needs a new handbook topic, a page is out of date, or two pages give different answers.
---

# Handbook section

A handbook is useful only when people trust that each page is the current answer. One topic lives on one page, the rule comes first, and every page has an owner who approves it.

**Route:** request → (country first) → **handbook-section** → the page owner approves → published by the person.
Before this skill: a work item naming the topic and who asked. After it: the owner's approval; a policy behind the page goes through `policy-draft`.

## When to use

- A new topic is needed (for example, how leave is requested, how equipment is ordered, how someone raises a concern).
- A page is out of date, or two pages say different things.
- A new or changed policy needs a page people read, not only the policy text.

## Inputs

- **Country** and company size, if the page touches any rule about work (leave, hours, pay, contracts). Rules differ by country.
- **The page owner:** the person who approves it and answers questions on it.
- **The source of truth:** the approved policy, decision or process the page describes. If there is none, the page is a proposal and says so.
- **Existing pages** on the same topic.

## Steps

1. **Find what exists.** Search the handbook for pages on the topic and list them, with their dates and owners.
2. **Decide the one page.** Pick one page to keep (or a new one) and list the others to remove or point here.
3. **Write the page:**
   - a clear title, the way people would search for it;
   - the rule or the steps first, in a few short sentences;
   - exceptions, and who decides them;
   - who to ask, by role;
   - owner, last reviewed date, next review date;
   - links to the policy behind it, not a copy of it.
4. **Mark what needs a professional.** Any statement about what the law of a country requires is a question for a professional with its dated source, not a fact on the page.
5. **Check plain language.** Short sentences, everyday words, no internal jargon without a short explanation, steps numbered.
6. **Send for approval** to the page owner, with the list of pages to remove. The person publishes; the agent never does.

## Checks before hand-over

- One topic, one page; every older page on the topic is listed for removal or redirect.
- Owner, last reviewed date and next review date are on the page.
- Every rule points to its source; nothing says the page meets any law.
- Nothing about a named person, a case or private data is on the page.

## Artefacts

- `handbook/<topic>.md`: the page draft.
- `handbook/<topic>-changes.md`: what changed, which pages to remove, open points for a professional.

## Hand-over

- **To the page owner:** the page and change list for approval.
- **To `policy-draft`:** a rule that has no approved policy behind it yet.
- **To the onboarding specialist:** pages new people need in their first weeks.

## Sources

Built on the Sourcegraph handbook content practices and people-ops pages (Apache License 2.0, © 2021 Felix Frederick Becker), the PostHog handbook people pages (MIT, © 2020-2025 PostHog Inc.) and the O*NET 31.0 Database, 11-3121.00 Human Resources Managers. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
