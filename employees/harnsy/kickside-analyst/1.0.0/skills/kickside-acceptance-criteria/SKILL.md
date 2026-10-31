---
name: kickside-acceptance-criteria
description: Write a short KickSide task a tester can check - the smallest useful version and a Later list, acceptance criteria per role with an action and a visible answer, refusals included, checks after a restart, what the client must provide (test keys of a payment service, a domain, who gets access), and an estimate in agent-team hours with a range, never a date or a price. Use after intake, when a wish is understood and must become an agreed task, or when existing criteria are vague.
---

# Tasks and acceptance criteria for KickSide work

A task is agreed when the client can read it in five minutes and say yes, and the KickSide QA tester can check every line in the running copy without asking anyone. The common ways a task fails: it carries everything the client ever mentioned, its criteria describe the admin's view only, and nobody wrote down that the client must bring test keys of their payment service. This skill writes the task so none of that happens.

**Route:** kickside-intake → **kickside-acceptance-criteria** → the owner's OK → the client's yes → the lead hands it to the builders.

## Inputs

- From intake: the client's words, said and assumed, the ready / owner's / new map with sources, the owner's flags and replies.
- The roles that will use the result (owner of the business, manager, accountant, a visitor of the site, nobody signed in).

## Steps

1. **Cut to the smallest useful version.** Ask: what is the least that helps the client on day one? Keep that. Everything else goes to **Later**, one line each, in the client's words. A wish that bundles several parts (requests, payments, staff) becomes one task per part, with an order: what others depend on comes first.
   Check: the task fits one screen; Later is written down, not lost.
2. **Write the task with these parts, in this order.**
   - Title in the client's words.
   - The client asked: the quote.
   - Problem: one line from the client's side.
   - First version: three to six bullets of what it will do.
   - Later: what it will not do yet.
   - How it is covered: the ready / owner's / new table from intake, with sources.
   - Acceptance criteria (step 3).
   - The client provides (step 5).
   - Estimate (step 6).
   - Open questions and assumptions still to confirm.
   - Who does what: lanes (below).
   Check: every part is present; none says «TBD» without an open question behind it.
3. **Write criteria per role.** Each criterion: role, what they do, what they see. Number them. For every role write at least one allowed action and one refusal. Add one check after a restart of the copy for anything stored, and one on a phone-width screen for anything a visitor of the site sees.
   Form: «C3. As a manager, I open Requests and see the new request from the site form within a minute, with name, phone and message.»
   Refusal form: «C7. As a manager, I open Payments: the page is not in my menu, and its address opened directly refuses me.»
   Check: each criterion can be judged true or false by someone who was not in the conversation; no criterion says «works well», «fast» or «user-friendly» without a number.
4. **Add the checks the kind of work always needs.**
   - Site form: a valid request lands with every field; an empty required field is refused with a message; the same request sent twice does not make two records, or the task says it may; a flood of requests is slowed down.
   - Payments: in the payment service's test mode only; a paid order turns «paid»; a failed or cancelled payment does not; a notification with a wrong signature is refused and changes nothing; a refund needs the approval that was agreed; no card number is ever entered in or stored by KickSide.
   - Staff and roles: each group sees only its pages; a person removed from a group loses access; signing in with a wrong password is refused.
   - Approvals: yes and no both lead somewhere; an item waits in the approver's Inbox until answered; what happens when nobody answers is stated.
   - Backups: a copy is made on schedule; a restore onto a test copy brings the data back; a failed copy tells the person named.
   - Anything stored: still there after a restart.
   Check: every criterion that applies is in the list or crossed out with a reason.
5. **List what the client provides.** Only what the team cannot make itself: the account and **test (sandbox) keys** of the payment service, entered by the owner or the client into the platform, never sent; later the live keys the same way; the domain name and who manages it; the list of people and their groups; who on the client's side says «go live»; made-up sample data if real-looking examples help.
   Check: each item says who provides it and how; none asks for a secret in chat or by email.
6. **Estimate in agent-team hours.** Give a range (low to high) and what it covers: building, tests on SQLite and Postgres where data is touched, checks by the tester, handover. Base it on hours measured on similar work; where the team has none yet, ask the builders in each lane for their range and say the estimate is a first guess. Write «estimate, not a price or a date: the owner prices, the client decides».
   Check: a range, what it covers, the sentence about price and date.
7. **Owner, then client.** Send the task to the owner for an OK; after it, send the short version to the client in their language: first version, Later, what they provide, open questions. The estimate goes with the owner's price, from the owner, unless the owner says otherwise.
   Check: the owner's OK is on the item before the client sees the task.
8. **Freeze it.** Once the client says yes, the task is version 1. Any change after that goes through kickside-change-request.
   Check: the client's yes is quoted on the item, with its date.

## Rules (each with its check)

- **Smallest useful version first.** Check: Later is not empty for any wish bigger than one feature.
- **Every role, allowed and refused.** Check: count roles and refusals.
- **Testable in the running copy.** Each criterion names something the tester can see in the page or the answer. Check: no criterion depends on reading code.
- **Test mode for money.** Payment criteria use the payment service's test mode until the client says go live. Check: the word «test» is in every payment criterion.
- **Hours, not dates or prices.** Check: no date, no currency in the estimate.
- **No real data, no secrets in the task.** Check: sample data is made up; no key in the text.

## Do not promise

- That a criterion passes before the tester ran it.
- That «Later» items are planned: they are only written down.
- That an estimate holds if the scope changes.

## Lanes in the task

- Setup without code (CRM objects, views, workflows, users and roles): the KickSide specialist.
- A module, new or changed: the KickSide module developer.
- Its screens: the KickSide frontend developer.
- The checks and screenshots: the KickSide QA tester, against these criteria.
- Server, domain, HTTPS, backups, release to the client's server: the KickSide DevOps engineer.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0), the KickSide app and its developer handbook (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI) and the KickSide module template (github.com/kicksideai/module, commit 37d16de; MIT, © 2026 Wippy). Ideas on stories and testable conditions from the GOV.UK Service Manual (OGL v3.0) and agent-skills by Addy Osmani (MIT).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
