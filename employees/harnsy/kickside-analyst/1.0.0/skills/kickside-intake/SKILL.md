---
name: kickside-intake
description: Turn a non-technical client's wish about their KickSide platform - requests from a site, a CRM, payments, staff logins and roles, approvals, documents, an assistant - into at most five plain questions in the client's language and a map of each need to what KickSide already has, modules the owner already has or a new module, every item with its source from the installed list, the catalog or a readme; flag paid modules, outside services with their own terms and every wish for staff or other extra accounts to the owner. Use when a client or the owner brings a new wish, or when someone names a module from memory.
---

# Client intake for a KickSide platform

A client says «I want to take requests from my site». Behind it are a list of requests, someone who must learn about a new one, stages, a form on a site, maybe spam. The client knows their business, not modules. This skill gets the few answers that matter, takes a sensible working answer for the rest, and sorts every need into one of three buckets before anyone writes code:

- **Ready**: KickSide already does it; the KickSide specialist sets it up without code.
- **The owner's**: a module the owner already has does it (for example a lead form, payments or backups); it is installed and configured once it is released.
- **New**: nothing does it; the KickSide module developer builds a module, the KickSide frontend developer its screens.

**Route:** a wish → **kickside-intake** → kickside-acceptance-criteria → the owner's OK → the client.

## Inputs

- The client's words, quoted as written, and the language they used.
- Which copy this is for (dev, test or the client's live copy) and who can read its installed-module list (usually the KickSide specialist).
- The owner's notes: what was already promised, what is off the table.

## Steps

1. **Quote the wish.** Write the client's words at the top of the item, unchanged. Below, one line: the problem as the client sees it («new requests get lost in email»).
   Check: the quote is verbatim; the problem line has no technical words.
2. **Get the facts of the copy.** Ask the KickSide specialist for the installed-module list of the client's copy (module id and version, one per line). For what can be added, read the public module catalog in the KickSide documentation (`reference/modules.md`) or the module's page on the Hub (hub.wippy.ai) (read from S2, not tried). For what a module does, read its readme. Never map a need from memory.
   Check: every module you will name has a source: the installed list, the catalog row or the readme.
3. **Pick the questions.** Take the bank for the wish below, choose at most five, and drop any the owner's notes or earlier answers already settle. Each question must be answerable from the business: «who should see a new request?», never «which scope?».
   Check: five or fewer; no technical word; each one changes what gets built.
4. **Ask in the client's language.** One short message: why you ask (one line), the numbered questions, and «for anything you skip I will assume the usual and show you». Offer choices where you can («a) only you, b) all managers, c) someone else»).
   Check: sent through the channel the owner set; no estimate, date or price in it.
5. **Write said and assumed apart.** Said: the client's answers, quoted. Assumed: a working answer for every question not answered, each marked «please confirm».
   Check: no assumption is written as the client's words.
6. **Map each need.** A table: need in the client's words | bucket (ready, the owner's, new) | how it is covered | source. Use the map below as the starting point and confirm each row against step 2.
   Check: every row has a bucket and a source; a «ready» row names an installed module or one in the catalog; an «owner's» row says whether that module is released yet (ask the KickSide module developer); a «new» row says why nothing ready fits.
7. **Flag what the owner must see first.** Paid modules or modules with their own terms; outside services the client must sign up for and pay (a payment service, a model provider for an assistant, a messenger); any wish for staff or other extra accounts (below). Send these to the owner before the client chooses.
   Check: each flag names the module or service and why it matters, in two lines.
8. **Hand on.** Pass the map and answers to kickside-acceptance-criteria.

## Question banks (choose at most five)

**Requests from a site (leads).** What should a request contain (name, phone, email, message, anything else)? Who should see a new request, and how should they learn about it? What happens next: which stages does a request go through? Which builder or developer runs your site, and can they paste a small piece of code? Roughly how many requests a day?

**CRM, «keep my clients in one place».** What do you keep now and where (a spreadsheet, another CRM, email)? Which kinds of records: clients, companies, deals, orders? Which fields matter for each? Who may see and change them? Should old records be moved in?

**Payments.** What do you sell: fixed prices, or an amount per order or invoice? Which payment service do you use or want, and do you have an account with it? How does a customer pay: on your site, or by a link you send? Who may make a refund? Does the law where you work require a receipt from the payment service (ask your accountant)?

**Staff logins and roles.** Which groups of people will sign in (sales, managers, accountant)? What may each group see and do, and what must it never see? Should they sign in with a password or with a work account from a sign-in provider? Who adds and removes people when staff change?

**Approvals.** What needs approval (a discount, an expense, a refund)? Who approves, and who stands in when they are away? What happens on yes and on no? What if nobody answers in time?

**Documents and an assistant.** Which documents (contracts, price lists, instructions)? Who uploads them and who reads them? Should an assistant answer questions from them, and to whom: staff or customers?

**«I don't want to lose data».** How much work could you bear to lose: an hour, a day? Where may copies be kept? Who should be told if a copy fails?

## Map: typical needs and where they live

Confirm each row against the copy (step 2); versions and catalogs change. Every row was read from the sources named, none was tried on a copy.

| Need | Bucket | How | Source |
|---|---|---|---|
| Records with fields, stages, a table and a board | Ready | CRM module from the Hub; starts with an empty schema, the KickSide specialist defines objects, fields and views | CRM readme; docs `using/crm.md` (read from S2 and S3, not tried) |
| Move existing clients in | Ready | Data Sync automation into CRM, or CRM agent tools; schema export/import moves the schema, not records | docs `using/crm.md` (read from S2, not tried) |
| A notice when something happens | Ready | Automation or workflow; the channel (messenger, email) depends on the connections installed | docs `using/automations-and-workflows.md`, `using/connections.md` (read from S2, not tried) |
| Someone approves before a step goes on | Ready | Workflow with a review step that puts an item in the Inbox and waits | docs `using/inbox.md`, `using/automations-and-workflows.md` (read from S2, not tried) |
| Staff accounts, groups, what each may open | Ready | System → Users, System → Security → Scopes; one sign-in provider ships in the app, others from the Hub | docs `using/users.md`; app lock (read from S1 and S2, not tried) |
| Documents stored, searched, answered by an assistant | Ready | Uploads, a knowledge base (module plus an engine from the Hub), an agent with a knowledge capability and a model | docs `using/knowledge.md`, `using/agents.md` (read from S2, not tried) |
| A form on the client's site that drops requests into CRM | The owner's | A lead-form module the owner has, or a new one. The platform's webhooks need a secret in a request header, so a browser form cannot hold it; if the client's site has its own server that can add the header, the webhooks module may do and nothing is built | webhooks module in the app (read from S1, not tried); that module's readme |
| Online payments | The owner's | A payment module the owner has, for one payment service. Check in its readme that checkout is hosted by the payment service (card data never touches KickSide), that notifications are signed and checked and that refunds go through approval; a second service is usually extra work | that module's readme |
| Scheduled backups with a tested restore | The owner's | A backup module the owner has, plus the KickSide DevOps engineer on the server; S3 storage exists as a component | that module's readme; components repo (read from S5, not tried) |
| A rule or screen nothing above covers | New | A module from the module template, built by the KickSide module developer, screens by the KickSide frontend developer | handbook: find before build, application patterns |

## What to flag to the owner

- **Staff and other extra accounts.** Treat every copy as untrusted toward its host. Extra accounts come only after the Application security reviewer has cleared that copy. Any wish for staff logins goes to the owner first: ask the KickSide specialist what ordinary users' policies allow on that copy, and tell the owner before anyone adds users. Whether staff sign in is the owner's and the client's decision.
- **An assistant needs a model.** An agent answers only with a model provider and its key; the provider's usage is billed to whoever owns the key.
- **Outside services.** A payment service, a messenger or an email provider has its own contract, terms and fees; the client signs up, not us.

## Rules (each with its check)

- **Five questions at most per round.** Check: count them.
- **No module from memory.** Check: every module id in the map has a source.
- **Said and assumed apart.** Check: every assumption carries «please confirm».
- **Ready before the owner's, the owner's before new.** Check: every «new» row says why nothing ready fits.
- **Flags to the owner before the client chooses.** Check: the owner's reply is on the item.
- **No real client data.** Ask for made-up examples of a request or a record. Check: no real names, phones or emails in the item.
- **No secrets.** Never ask the client to send keys or passwords; ask them to have them ready. Check: search the item for anything that looks like a key.

## Do not promise

- That a module the owner has is ready when it is not released yet.
- That a ready module is installed on this copy before the installed list says so.
- A date, a price, or anything the owner has not agreed.

## Hand-over

- **To the KickSide specialist:** the installed-module list request; later, «ready» setup work.
- **To the KickSide module developer:** whether a module the owner has is released; a «new» row to size.
- **To the owner:** the flags, before the client chooses.
- **To the Application security reviewer, through the owner:** a copy where staff accounts are wished, before anyone adds users.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0), the KickSide app with its developer handbook and lock (github.com/kicksideai/kickside, commit b7e0106), KickSide CRM (github.com/kicksideai/crm, commit 3cdb074) and KickSide components (github.com/kicksideai/components, commit bc5e866), all KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI. Interview ideas from 18F Methods (CC0 1.0).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
