---
name: policy-draft
description: Draft an internal policy (for people, data, security, spending, conduct or any other area) with scope, owner, rules, exceptions and a review date, marking every point that needs a professional, for the owner to approve. Use when a company needs a new policy or a change to one.
---

# Policy draft

A policy is a decision the owner makes and the company follows. This skill prepares it: it writes the draft, shows where the rules of a country matter, and leaves the decision to the owner and, where needed, a professional.

**Route:** request → (country first) → **policy-draft** → a professional reviews the marked points → the owner approves → the page people read.
Before this skill: a work item naming the need and who asked. After it: the owner's approval; the page people read is written from the approved policy.

## When to use

- A company needs a new policy (remote work, leave, expenses, equipment, conduct, data handling, access, and so on).
- A policy must change: a new country, a new kind of contract, a rule that no longer works, a review date reached.

## Inputs

Ask first. Do not draft without these:

- **Country** (and region) of the people or activity the policy covers. Rules differ by country; when several apply, say so.
- **Company size** and the kinds of people covered (employees, contractors, part-time, volunteers).
- **The owner:** the person who approves the policy and decides exceptions.
- **The need:** what is going wrong or missing, in the requester's words, and what the owner wants to happen.
- **Existing policies** and pages it touches.

## Steps

1. **Write the need in one paragraph,** with the requester's words and the owner's intent. Confirm it if unsure.
2. **Collect dated sources.** For points that depend on the rules of the country, find the official source (government or regulator page), note its date and any «under review» or «draft» banner. A source that cannot be fetched is named, not quoted.
3. **Draft the policy:**
   - **Purpose:** one or two sentences.
   - **Scope:** who and what it covers, and what it does not.
   - **Owner:** who approves, who decides exceptions, who to ask.
   - **Rules:** short, numbered, each one something a person can follow and check.
   - **Exceptions:** how to ask and who decides.
   - **Related:** links to other policies and pages, not copies.
   - **Review:** version, date, next review date.
4. **Read it for fairness.** Rules about people use job-related reasons and must not treat a group less well; look for wording that would.
5. **Mark points for a professional.** Every point where the rules of the country decide the answer gets a marker and a question, with its dated source. The draft never says it meets the law or will hold up.
6. **Send to the owner** with the marked points listed at the end. Record the approved version and date. A change after approval is a new version.

## Checks before hand-over

- Country, scope, owner and review date are present.
- Every rule is short and checkable.
- Every country-dependent point is marked, with a dated source and a question for a professional.
- No claim that the draft meets any law; no promise of an outcome.
- No named person, case or private data in the policy.

## Artefacts

- `policy/<name>-v<N>.md`: the draft.
- `policy/<name>-questions.md`: the marked points for a professional, each with its source and date.

## Hand-over

- **To the owner:** the draft and the questions, for approval. The person signs off and publishes; the agent never does.
- **To a professional** (through the owner): the marked questions.
- **To whoever keeps the handbook:** the approved policy, so the page people read can be written or updated.

A specialist area (for example a privacy notice or a security policy) may add a short section of its own under this skill; the steps and checks above stay the same.

## Privacy notice

Use this section when the policy is a privacy notice: what people are told about their personal data.

- **Facts come from the record of processing** (`processing-record`; build it first if none exists). Each line of the notice points to a line of the record. A fact the record lacks becomes a question to the owner, never a typical answer.
- **What to cover (EU and UK GDPR).** Articles 13 (data collected from the person) and 14 (data obtained elsewhere) of Regulation (EU) 2016/679 (OJ L 119, 4.5.2016; read 8 October 2026) list it: who the organisation is and how to reach it, each purpose with the lawful basis the owner and the lawyer confirm, who receives the data, transfers abroad, how long it is kept, the person's rights, the right to complain, and, for data from elsewhere, what kinds of data and where they came from.
- **When to tell people.** At collection. For data obtained elsewhere: within a reasonable time and no later than one month, or at the first contact or first disclosure if that comes sooner. Tell people before the data is used for a new purpose.
- **How.** Plain words; a short first layer with the details one step away; a test with a few real readers; a review date.
- **Date the guidance.** The ICO pages on the right to be informed carry the banner «under review» after the Data (Use and Access) Act (checked 8 October 2026). Write that date and banner next to every point taken from them, and check again before each new version.
- **Other countries:** name the law that may apply as a question for the lawyer; state no rule or deadline.

Built on: Information Commission’s Office, The right to be informed guidance (under review, checked 8 October 2026), licensed under the Open Government Licence. Facts only, not text: Regulation (EU) 2016/679, Articles 13 and 14.

## Sources

Built on the hr-pro agent from github.com/wshobson/agents (MIT, © 2024 Seth Hobson), the Sourcegraph handbook content practices (Apache License 2.0, © 2021 Felix Frederick Becker) and the O*NET 31.0 Database, 11-3121.00 Human Resources Managers. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
