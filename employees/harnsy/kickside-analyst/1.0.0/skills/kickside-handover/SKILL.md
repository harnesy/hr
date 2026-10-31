---
name: kickside-handover
description: Hand checked KickSide work back to a non-technical client in plain words and their language - what it does, how to use it step by step, what the tester checked with screenshots from a copy with made-up data, what is left, what the client must do (enter live keys, add staff, say go live) and how to ask for a change; no jargon, each needed term glossed once, sent only after the owner's OK. Use when the KickSide QA tester has passed a task.
---

# Handing the work back to the client

The client did not see the work being built. The handover is the first time they meet it, often on a phone, between other things. It must answer four questions in this order: what can I do now, how, what did you check, what must I do. It says only what the tester saw in the running copy; anything else is «not checked» or «left».

**Route:** the KickSide QA tester's passed report → **kickside-handover** → the owner's OK → the client.

## Inputs

- The agreed task (version and date) and its acceptance criteria.
- The tester's report: each criterion passed or failed, how it was checked, screenshots, the copy and version it ran on.
- What is left from the builders (anything not done) and from the KickSide DevOps engineer (release to the client's server, backups).

## Steps

1. **Check the ground.** Every criterion of the task must be «passed» in the tester's report, or the handover lists it under «left» with the reason. A criterion with no result is not passed.
   Check: a table criterion → result → screenshot; no gaps.
2. **Pick the screenshots.** One per thing the client will do, from the dev or test copy with made-up data. A screenshot from the client's live copy only with every person's name, phone, email and amount hidden, and only with the owner's OK. Crop to what matters; add a short caption in the client's language.
   Check: no real personal data, no key, token or password visible anywhere in a picture (look at the address bar and the corners too).
3. **Write it in the client's language, in this order.**
   1. **What you can do now.** Two or three sentences, in the client's words from the task. «Requests from your site now land in KickSide, and your managers get a notice for each new one.»
   2. **How to use it.** Numbered steps a person follows with the screen in front of them, one action per step, the button or menu named exactly as it appears. A screenshot next to the step it shows.
   3. **What we checked.** A short list in plain words, one line per criterion group: «A manager sees new requests and cannot open payments.» Add «checked on <copy>, <date>» once.
   4. **What is left.** Anything not done or not checked, with the reason and who it waits for.
   5. **What you need to do.** Only the client's actions: enter the live keys of your payment service yourself in the platform; tell us who should get an account; say «go live» when ready. Never ask them to send a key or a password.
   6. **How to ask for a change.** One line: write what you want in your own words, as with the first request; we will say whether it fits what was agreed, and what it takes.
   Check: the order is kept; each part is three to eight lines; no part is missing (write «nothing» where empty).
4. **Remove jargon.** Read it as someone who has never heard of KickSide. Replace every technical word with an everyday one. Where a term is needed (CRM, Inbox, workflow), gloss it once in one phrase at first use: «Inbox, the list of things waiting for your decision». No module ids, versions, file names, ports or commands; those stay in the team's item.
   Check: search for words like module, endpoint, scope, webhook, migration, token, deploy; each one is gone or glossed.
5. **Owner's OK, then send.** Send the draft to the owner. After the OK, send it to the client through the channel the owner set.
   Check: the owner's OK is on the item before the client gets it.
6. **Close the item.** Record on the item: the handover sent (date), the client's reply, anything the client raised (to kickside-change-request), and what waits for the client.
   Check: the item says done / how checked / left.

## A short template (fill in the client's language)

```
<Title in the client's words>

What you can do now
...

How to use it
1. ...  [screenshot 1]
2. ...

What we checked (on the test copy, <date>)
- ...

What is left
- ... (waits for ...)

What you need to do
- ...

To ask for a change: write what you want in your own words.
```

## Rules (each with its check)

- **Only what was checked.** Check: every line in «What we checked» maps to a passed criterion.
- **No personal data or secrets in screenshots.** Check: each picture looked at in full.
- **Plain words.** Check: the jargon search in step 4 finds nothing unglossed.
- **No date or price.** A go-live date is the client's word; a price is the owner's. Check: neither appears unless the owner wrote it.
- **The client's actions are the client's.** Live keys, staff accounts and go live are done or said by the client or the owner. Check: no step in which the team enters a live key.

## Do not promise

- That something works on the client's live copy when it was checked on the test copy: say where it was checked.
- Support terms, response times or warranties: those are the owner's.
- That a change is small before kickside-change-request has sized it.

## Hand-over

- **To the KickSide DevOps engineer:** the release to the client's server once the client says go live, through the owner.
- **To the KickSide QA tester:** anything the client reports as not working, with the client's words.
- **To the owner:** the client's reply, and any wish for more work.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0) for the names of pages a client meets. Our team's rules on client data, secrets and checks in the running copy. Plain-language ideas from GOV.UK content design guidance (OGL v3.0).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
