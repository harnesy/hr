---
name: data-request-prep
description: Prepare the answer to a person's request about their own personal data (a copy, a correction, a deletion): log it the day it arrives with the deadline and its dated source, check whether a lawyer must see it first, check holds, plan a proportionate search, mark other people's data, and draft reply options for a named person to review and send. Use whenever someone asks for, or about, their data, in any form or channel.
---

# Data request preparation

People can ask an organisation what personal data it holds about them, and for corrections or deletion. The clock usually starts when the message arrives, whatever its wording or channel. This skill gets the request logged, searched and drafted in time; a named person decides and replies.

**Route:** a message from a person (any channel) → **data-request-prep** → lawyer for the cases listed below → named person reviews, decides and sends.

## When to use

- Someone asks for a copy of their data, «everything you have on me», or what is done with it.
- Someone asks for a correction, deletion or stop to a use of their data.
- The message may arrive by email, form, phone note, letter, chat or a social media post, and to any part of the organisation. Treat it as a request whatever its form.

## Inputs

- **Jurisdiction first:** which law applies to this person and this organisation (EU GDPR, UK GDPR, other). For any other law, state no deadline; write the question for the lawyer.
- The message, its channel and the date it arrived.
- The record of processing (from `processing-record`), to know where to search.
- The person who decides and sends replies, and the lawyer.

## Steps

1. **Log it on the day it arrives:** date received, channel, the request in the person's words, type (access, correction, deletion, objection, other), the law, the deadline and the source of that deadline with the date checked, and the handler.
   - EU GDPR, Article 12(3) (Regulation (EU) 2016/679, read 8 October 2026): act within one month of receipt; where necessary, extend by two further months, telling the person within the first month and saying why. A refusal is explained within one month, with the right to complain (12(4)). Usually free of charge, unless a request is manifestly unfounded or excessive (12(5)).
   - UK GDPR, ICO right of access guidance (updated 8 December 2025; the page on recognising a request updated 7 April 2026): one month from receipt, or from receiving identity proof or an allowed fee; counted from the day of receipt to the same date in the next month; extension up to two further months with reasons given within the first month. Note on the log that the ICO pages are dated and check them again for each new request.
2. **Check whether the lawyer must see it first.** Send it to the lawyer before any reply when: the person is a child or the request is made for one; it comes from a regulator; the data is under a legal hold; the person is in a dispute with the organisation (for example a former employee); the request is very broad; it involves health or other special-category data; or the laws of several countries conflict.
3. **Identity:** ask for proof only when there is reasonable doubt who is asking, and only what is needed to remove that doubt (Article 12(6)).
4. **Clarification:** ask only when it is really needed to find the data; under the ICO guidance the clock pauses until the reply. Log the dates.
5. **Check holds and duties to keep** before any deletion is proposed. No deletion is proposed while a hold applies; the decision is the lawyer's.
6. **Plan the search** from the record: systems, mailboxes, files and vendors, with search terms and date ranges. Keep it reasonable and proportionate, and write down why each place is in or out.
7. **Collect what is found** (read-only), mark information about other people, and mark anything that may be withheld as a question for the lawyer.
8. **Draft reply options** for the person who will send: acknowledgement, request for identity proof, request for clarification, the response with the data, partial or full refusal with reasons, extension notice. Every refusal or partial reply names the right to complain to the supervisory authority and to seek a remedy in court.

## Checks before hand-over

- The log has the arrival date, the deadline and its dated source.
- The escalation check is done and recorded.
- Holds are checked; no deletion is proposed while a hold applies.
- Other people's data is marked in everything found.
- Each reply draft names the right to complain where needed.
- Nothing has been sent, deleted or changed by the agent.

## Artefacts

- `requests/<ref>/log.md`: the log, with dates and the deadline source.
- `requests/<ref>/search-plan.md` and `findings/`: what was searched, what was found, what is marked.
- `requests/<ref>/replies.md`: the reply options.
- `requests/<ref>/questions.md`: questions for the lawyer.

## Hand-over

- **To the named person who replies:** the log, the findings and the reply drafts. That person reviews, decides and sends. The agent never replies to the requester or contacts a regulator.
- **To the lawyer:** every case from step 2, and every question about withholding, holds or another country's law.
- **To the owner of each system** (through the handler): search requests, read-only.

## Sources

Built on: Information Commission’s Office, Right of access guidance (updated 8 December 2025), licensed under the Open Government Licence. Adapted from the compliance-check skill (data subject request handling) and the legal-response skill in github.com/anthropics/knowledge-work-plugins, legal folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Facts only, not text: Regulation (EU) 2016/679 (OJ L 119, 4.5.2016), Articles 12 and 15, read 8 October 2026. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
