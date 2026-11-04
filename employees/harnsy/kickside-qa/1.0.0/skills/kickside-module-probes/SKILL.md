---
name: kickside-module-probes
description: Probe the lead-form, payment and backup modules the owner has, where risk hides - a public lead form (validation, spam traps, rate limit, markup shown as text), payments in the provider's sandbox only (paid, failed, refunds as the module offers them, forged or repeated notifications refused or counted once, card data never on KickSide pages) and a backup restore drill on a fresh staging copy with counts compared. A checklist from the sources, not a tried run. Use when such a module is new, changed or about to reach a client.
---

# Lead form, payments and backups

Three kinds of module carry the client's money, the client's leads and the client's way back: a public lead form, a payment module and a backup module the owner has. Each has a quiet failure: a public form that fills the CRM with spam or lets a script into the screen, a payment marked paid by a notification nobody signed, a backup that restores without the key that opens its secrets. This skill probes each on the dev or staging copy, never on the client's copy and never with real money. It is a checklist built from S2 and each provider's sandbox documentation, not a tried run: none of its scenarios has been run on a copy yet, and the module's own readme decides its fields, limits, statuses and routes.

**Route:** a lead-form, payment or backup module in an acceptance plan → **kickside-module-probes** → kickside-acceptance for the report.
Before this skill: the module installed on a dev or staging copy; its readme for its own limits, fields and statuses; the owner's OK. After it: each scenario passed or failed with evidence, and the restore drill's numbers.

## When to use

- A lead-form, payment or backup module is new, changed, or about to be installed for a client.
- A client asks whether spam, a fake payment or a lost server can hurt them.

## Inputs

- The module's readme and the analyst's criteria: form fields, the stated rate limit, payment statuses, the backup schedule and contents.
- The copy's address in `$BASE`; a role token from kickside-role-checks for checking results.
- For payments: the provider's sandbox (test mode) account, whose keys the owner enters into the copy; you never see them.

## Lead form

The form takes posts from the client's website without a session, so it sits on an intentional public route and must not trust anything the request says about who sent it. Steps 1-6 are a checklist read from S2 (public routes, webhook ingress), not tried; the form module's readme names its fields, traps and limit.

1. **A valid lead.** Post one with fake data the way the site snippet does. Check: the lead appears in the CRM with every field; the event the module promises (for example «new lead», which an automation can turn into a notice) shows in its history.
2. **Validation.** A missing required field, a wrong type, an oversized field, an empty body. Check: each is refused with a clear 4xx, and the lead count does not change.
3. **Spam traps.** Fill the trap field the module documents (a hidden field, a too-fast submit, or what its readme names). Check: refused or silently dropped as the readme says, and no lead created.
4. **Markup stays text.** Put HTML and a script tag into a text field. Check: the CRM screen shows the characters as text and nothing runs. If anything runs, stop and go to the Application security reviewer at once.
5. **Rate limit.** Send a small burst a few posts past the stated limit from one client, then wait out the window and post again. Check: posts past the limit are refused with the code the module's readme names, the lead count equals the accepted posts, and posting works again after the window. On staging behind your reverse proxy, ask the KickSide DevOps engineer how the client address reaches the copy: a limit that counts the proxy's address blocks every visitor at once.
6. **No identity from the request.** A field that claims a user, a group or an owner. Check: the lead is owned as the module defines, never by what the post claims.

Keep bursts small and only against the dev or staging copy; never against the client's copy, the client's live site or anyone else's service.

## Payments (sandbox only)

A payment module that sends the buyer to the provider's hosted checkout keeps card data off KickSide; the provider tells the copy the result through a notification that the module must verify. Steps 2-8 are a checklist read from S2 (public callbacks and signature checks, inbox approvals) and the provider's sandbox documentation, not tried; follow the module's readme where it differs.

1. **Sandbox only.** Confirm with the owner that the copy holds test-mode keys. Live keys on a test copy stop the work. Check: the owner's answer is quoted.
2. **No card data on KickSide.** Open the pay link from an order. Check: it leads to the provider's own page; no KickSide page has a card number field; the network log shows no card data sent to the copy.
3. **Paid.** Pay with the provider's documented test card for success. Check: after the notification, the order shows paid, once.
4. **Failed and abandoned.** A test card that the provider declines; a checkout closed without paying. Check: the order never shows paid; it shows the status the readme names.
5. **Refunds, as the module offers them.** When the module's readme says a refund waits for a person's approval (for example in the Inbox), ask for one: it must wait. Reject it: nothing is refunded. Ask again and approve it: the provider's sandbox shows the refund and the order shows refunded. When the module offers no refund, mark the row not applicable.
6. **Forged notifications are refused.** Send the module's notification route a notification with a wrong signature, with none, and with a body changed after signing; and, for a provider that does not sign its notifications, a fake «succeeded» for an order that was never paid. Check: each is refused or ignored, the order's status does not change, and no event is written. An accepted forgery goes to the Application security reviewer at once.
7. **Repeats count once.** Send the same valid notification twice, and an older one after a newer one. Check: one status change; the order does not move backwards.
8. **Wrong amount or currency.** A valid notification whose amount or currency differs from the order. Check: not marked paid.

Never use a real card or real money, and never point a test at the provider's live mode.

## Backup restore drill

A backup is proven only by a restore. The drill runs on a fresh staging copy from the KickSide DevOps engineer, never over the client's copy. Steps 1-4 are a checklist (what a backup set holds read from S2's instance folder; the health check tried in S4), not a tried run; the backup module's readme and the DevOps runbook decide the details.

1. **Before.** On the source copy, write down the counts that matter (leads, orders, users, files), the installed-module list, and one stored secret that works (a connection's test, or a payment sandbox check). Check: the numbers are in your notes.
2. **The backup set.** List what the backup holds: the app database, the registry history, the uploaded files, and, stored apart from them, the key file. Check: the key is not inside the same archive as the data; the backup's time is known.
3. **Restore.** The KickSide DevOps engineer restores into the fresh copy by the runbook; time it from start to healthy. Check: `curl -s "$BASE/api/public/health"` answers healthy on the restored copy.
4. **Compare.** Sign in; the counts, the installed list and the files match the «before» numbers taken at backup time. The stored secret still works, which proves the right key came back. Check: every number matches, or the gap is listed.
5. **Report.** The backup's age at restore (how much work would be lost) and the time to restore, both in plain words, and anything missing.

## Rules (each with its check)

- **Dev or staging copy only; sandbox only; fake data only.** Check: the copy and the provider mode are named in the evidence.
- **Small bursts, own copy.** Check: the burst size and target are in your notes.
- **A security finding goes out at once.** Script that runs, a forgery that is accepted, a secret that shows. Check: the reviewer is named on the item with the time.
- **The restore is the KickSide DevOps engineer's; the comparison is yours.** Check: the runbook used and the numbers compared are in the report.
- **No secrets in evidence.** Sandbox keys, notification secrets and the key file never appear. Check: search the evidence; nothing found.

## Do not promise

- That the form stops every spammer: it stops what the probes showed.
- Provider behaviour beyond its sandbox: live mode is checked by the owner with the provider.
- A restore time for the client's server: the drill measures the staging copy.

## Hand-over

- **To the KickSide module developer:** failed scenarios, with the request (secrets cut out) and the answer.
- **To the Application security reviewer:** script from a form field, an accepted forged notification, card data on a KickSide page.
- **To the KickSide DevOps engineer:** a backup without the key, a key inside the data archive, a failed restore, a reverse proxy hiding client addresses.
- **To the owner:** sandbox keys to enter; live keys found on a test copy.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: S2 the KickSide app and its developer handbook (github.com/kicksideai/kickside, commit b7e0106; KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI: public callbacks and signature checks, webhook ingress, inbox approvals, the instance folder) and S1 the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0). Provider specifics come from each provider's sandbox documentation; S4: the health check as tried in the KickSide specialist's trial on Wippy 0.3.51a with KickSide 0.2.18. The scenarios are a checklist from these sources, not a tried run.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
