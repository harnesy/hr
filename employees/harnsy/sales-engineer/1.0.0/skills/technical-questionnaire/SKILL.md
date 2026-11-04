---
name: technical-questionnaire
description: Answer a buyer's security or technical questionnaire (or the technical part of a request for proposal) only from published product documents, the existing answer library and written confirmations; four answer classes, unknowns left blank and sent to a named owner, every date logged. Use when such a file arrives. Never writes a future feature or date and never signs attestations.
---

# Technical questionnaire

Buyers send long questionnaires about security, data handling, integration and operations. A wrong «yes» costs more than an honest «unknown, asked». This skill answers from documents only, routes every unknown to the person who knows, and keeps a record so the next questionnaire is faster.

**Route:** questionnaire from the account executive (or a tender section from the proposal and RFP writer) → **technical-questionnaire** → owners answer the unknowns → the finished file back to the account executive, who sends it.

## When to use

- A security, privacy, architecture or vendor questionnaire arrives during a sale.
- The proposal and RFP writer needs the technical answers for a formal tender.
- Not for promises about the future, prices or contract terms: those go to the account executive.

## Inputs

- The questionnaire file and its deadline.
- The **answer library**: earlier approved answers with their dates.
- The product's **published documents** (security pages, setup guides, data handling notes) and their dates.
- **Owners** for each area: product owner, security owner, legal contact. Ask the account executive who they are before starting.

## Steps

1. **Log the arrival.** Date received, deadline, who sent it, number of questions.
2. **Read every question first.** Group them by area. Note duplicates and questions that depend on each other, so answers stay consistent across sections.
3. **Answer what the documents cover.** For each question, answer what was asked, first and in the buyer's terms; then the detail. Pick one class:
   - **Supported**: with the link to the document or library answer.
   - **Supported with configuration or a workaround**: describe it and link it.
   - **Not supported**: say so plainly. Add what exists today, if anything.
   - **Unknown**: leave the answer blank in the buyer's file.
4. **Route the unknowns.** Send all unknowns of one area as one tracked request to the named owner, with the questions, the context and the date you need the answers by. Log the date sent.
5. **Merge the answers.** Owners' written answers go into the file with their date and name in your log (not in the buyer's file unless the buyer asks for contacts).
6. **Check consistency.** The same fact gets the same answer everywhere; no section contradicts another.
7. **Log the return and file the set.** Date answered, date returned to the account executive. Add new approved answers to the library with their source and date.

## Rules

- **Four classes only.** There is no «planned» class. No future feature, release or date is written, even if someone mentions one in a chat. «Ask your account executive about plans» is the most that is said.
- **Never mark a gap as covered** to raise a score.
- **No signatures.** Attestations, certifications of truth and signed forms are for the person the company names; the agent never signs or submits.
- **Documents over memory.** An answer without a source is an unknown.

## Checks before hand-over

- Every answered row has a class and a source.
- Every unknown is blank in the buyer's file and appears in a tracked request with a due date.
- No row mentions a future feature, a date for one, a price or a discount.
- Answers to related questions agree with each other.
- The log has all four dates (received, sent to owners, answered, returned).

## Artefacts

- `deals/<buyer>/questionnaire-<date>.<ext>`: the buyer's file with answers.
- `deals/<buyer>/questionnaire-log.md`: dates, classes per row, sources, requests to owners.
- `answer-library/`: new approved answers, each with source and date.

## Hand-over

- **To the account executive:** the finished file and the log; the account executive sends it.
- **To the proposal and RFP writer:** technical sections for a tender, with sources; the writer owns the tender document.
- **To the product owner:** a list of questions classed «not supported», as product feedback.

## Sources

Built on the Sourcegraph handbook (archived), security reviews page (Apache License 2.0; Sourcegraph, Inc. and contributors). Changed by harnsy. Built on the sales-engineer skill references, RFP response guide, in github.com/alirezarezvani/claude-skills (MIT, © 2025 Alireza Rezvani), adapted; the «planned» answer class left out. Built on the Sales Engineer agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors), adapted. Adapted from the draft-response skill in github.com/anthropics/knowledge-work-plugins, customer-support folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Scope from the O*NET 31.0 Database, 41-9031.00 Sales Engineers. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
