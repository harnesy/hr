---
name: processing-record
description: Build or update an organisation's record of what personal data it handles and why: an inventory of systems and vendors, a short questionnaire per team, a comparison of written policies with real practice, one record line per purpose, every unknown marked with who must answer, and questions for the lawyer. Use when no record exists, a new tool or vendor arrives, or at the yearly review. Drafts only; the owner and the lawyer decide.
---

# Processing record

A record of processing is a written map of the personal data an organisation handles: whose data, what, why, who receives it, how long it is kept and how it is protected. Laws such as the EU and UK GDPR require one from many organisations, and every privacy notice and data request depends on it. This skill drafts the record from what the owner and the teams state; it never fills a gap with a typical answer.

**Route:** owner's request (new record, new tool, yearly review) → **processing-record** → owner and lawyer review → basis for `policy-draft` (privacy notice) and `data-request-prep`.

## When to use

- The organisation has no record, or one nobody trusts.
- A new tool, vendor, product feature or kind of data arrives.
- The yearly review, or before a privacy notice is rewritten.

## Inputs

- **Jurisdiction first:** where the organisation is established, where the people whose data it handles are, and which law the owner believes applies (EU GDPR, UK GDPR, another). For any other country, the law is written as a question for the lawyer and no rule is stated.
- **The role:** controller (decides why and how data is used), processor (handles data for someone else), or both. If unclear, it is a question for the lawyer.
- The owner, the lawyer, and a contact in each team.
- Existing notices, policies, vendor contracts and any earlier record.

## Steps

1. **List systems and vendors.** Every system that holds personal data, who runs it (including outside vendors and their role), where it runs (country, cloud, vendor), and how data moves between systems and to other parties. Draw the flow as a simple map.
2. **Ask each team a short questionnaire:** what do you use personal data for; about whom; which items exactly; who gets it, inside and outside; how long do you keep it; how is it protected. Then talk to whoever runs IT security, whoever sets retention, and whoever handles data-sharing agreements.
3. **Compare paper with practice.** Read the existing notices, policies and contracts and note every place where they differ from what the teams say they do.
4. **Fill the record, one line per purpose,** each with its own people, data items, recipients, transfers abroad, retention and safeguards. A single generic line («contact details of customers and suppliers») for everything is not enough.
   - For a controller, the EU GDPR Article 30(1) fields: name and contact details, purposes, categories of people and of data, recipients, transfers to other countries and their safeguards, retention periods where possible, and a general description of security measures where possible.
   - For a processor, Article 30(2): the processor and each controller, the kinds of processing for each controller, transfers and safeguards, security measures where possible.
   - The record is kept in writing; an electronic form counts (Art. 30(3)).
5. **Mark every unknown** as «unknown — ask <person>», never with a guess.
6. **Write the questions for the lawyer:** lawful basis per purpose, transfers abroad, whether the size exception applies (step 7), and anything about the role.
7. **The size exception.** The 2016 text of Article 30(5) relieves organisations with fewer than 250 staff, unless the processing is likely to be risky for people, is not occasional, or includes special-category or criminal-offence data. Write it as a question: which of these apply? It may have changed: check the current consolidated text with the lawyer. Never write that the organisation does not need a record.
8. **Set the review:** a date, and the events that trigger an update (new tool, new vendor, new purpose).

## Checks before hand-over

- Every purpose has people, data, recipients and retention, or «unknown» with an owner.
- Every vendor appears both in the inventory and as a recipient.
- Every gap between paper and practice is listed.
- Every law fact names its article or official page and the date it was checked; ICO pages carry their date and the «under review» banner where shown.
- No line says the organisation meets the law or is free of a duty.

## Artefacts

- `privacy/record.csv` (or `.md`): one row per purpose with the fields above.
- `privacy/data-map.md`: systems, vendors and flows.
- `privacy/gaps.md`: unknowns with owners, paper-versus-practice differences, questions for the lawyer.

## Hand-over

- **To the owner and the lawyer:** the record, the map and the gaps, for review and decisions.
- **To the contract reviewer:** questions about the data terms in vendor contracts; this skill supplies the facts about the data flows those terms describe.
- **To the data engineer:** questions about where data sits and how it moves, when a team cannot answer.
- **To `policy-draft` and `data-request-prep`:** the reviewed record.

## Sources

Built on: Information Commission’s Office, Documentation guidance (under review, checked 8 October 2026), licensed under the Open Government Licence. The pages carry the banner «Due to changes made by the Data (Use and Access) Act, this guidance is under review and may be subject to change.» Also built on the NIST Privacy Framework, Version 1.0 (16 January 2020), category ID.IM-P (inventory and mapping), a work of the U.S. government. Facts only, not text: Regulation (EU) 2016/679 (OJ L 119, 4.5.2016), Article 30, read 8 October 2026. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
