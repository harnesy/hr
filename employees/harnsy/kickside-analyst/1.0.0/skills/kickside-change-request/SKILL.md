---
name: kickside-change-request
description: Sort a client's new or different ask against the agreed KickSide task - a fault (a passed criterion now fails), a change (a criterion must change) or a new wish - give its impact on the copies and the modules, a new estimate in agent-team hours, a change log entry, and let the client decide through the owner. Use when the client asks for something during building, testing or after the handover, or says it does not work as expected.
---

# Change requests on agreed KickSide work

«Can you also add a field?», «it doesn't work», «actually managers should see payments». Each sounds small; each means something different for the team. A fault is the team's to fix against what was agreed. A change moves the agreement and needs the client's choice with its cost in hours. A new wish is a new task. Mixing them up either hides work from the client or argues with them about a bug. This skill sorts the ask first.

**Route:** the client's ask → **kickside-change-request** → (fault) the KickSide QA tester / (change) the owner's OK and the client's choice / (new) kickside-intake.

## Inputs

- The client's words, quoted.
- The agreed task: its version, criteria and Later list.
- Where the work stands: building, testing, handed over, or live on the client's server.

## Steps

1. **Quote and restate.** Write the client's words on the item, then one line in plain words: «you want managers to see payments too».
   Check: restated without technical words; if unsure, ask one question back before sorting.
2. **Sort it.**
   - **Fault:** an agreed criterion that passed now fails, or something the task says it does, it does not. Example: requests from the form stopped arriving.
   - **Change:** what the client wants differs from an agreed criterion or first-version line. Example: managers should now see payments, where a criterion said they must not.
   - **New wish:** not covered by the task at all, or on its Later list. Example: accept payments by bank transfer.
   Check: the item names the criterion number or Later line it compares with, or says «not in the task».
3. **Fault.** Send it to the KickSide QA tester with the client's words and the criterion number to reproduce on the dev or test copy. Tell the client in one line: «we are checking it; it is part of what was agreed». No new estimate.
   Check: the tester's result is linked on the item before anyone tells the client it is fixed.
4. **Change: size the impact.** Ask the right teammate, do not guess:
   - setup without code only (a field, a view, a group, a workflow step): the KickSide specialist; it moves to the client's copy as configuration (for example the CRM schema export and import, or the platform's component transfer; read from S2 and S3, not tried), with no new module version;
   - a module's behaviour or screen: the KickSide module developer or the KickSide frontend developer; it means a new module version, tests, the tester's checks, and a release to the client's server by the KickSide DevOps engineer with a backup first;
   - access for staff: send it to the owner first; extra accounts come only after the Application security reviewer has cleared that copy (see kickside-intake).
   Write: what changes, which criteria change (old and new text), which copies it touches, and an estimate in agent-team hours with a range.
   Check: old and new criterion text side by side; the estimate has a range and no date or price.
5. **Change: let the client decide.** Send the impact to the owner; after the owner's OK and price, the client chooses: do it now, put it in Later, or drop it. A change asked mid-testing waits until the current round ends, unless the owner says otherwise, so the tester checks one agreed version at a time.
   Check: the client's choice is quoted on the item.
6. **Record it.** Add a line to the change log at the bottom of the task: date, the client's words, sort, decision, new task version. On «do it now», raise the version (v1 → v2), update the criteria, and tell the KickSide QA tester which criteria to check again.
   Check: the task's version, criteria and change log agree.
7. **New wish.** Start kickside-intake with the client's words; link it from this item.
   Check: the new item exists and is linked.

## Change log (at the bottom of the task)

```
| Date | Client said | Sort | Decision | Task version |
|------|-------------|------|----------|--------------|
| ...  | "..."       | change (C7) | do now, owner OK | v2 |
```

## Rules (each with its check)

- **Sort before answering.** Check: every ask on the item has fault, change or new next to it.
- **A fault costs the client nothing new.** Check: no estimate attached to a fault.
- **A change waits for the client's choice.** Nobody builds it on «sounds small». Check: the choice is quoted before the lead hands it on.
- **One agreed version at a time.** Check: the tester's report names the task version it checked.
- **Client data stays put.** Reproduce faults on the dev or test copy with made-up data; ask the client for steps, not for their records. Check: no real personal data on the item.
- **No dates or prices.** Check: none in your text; the owner's price comes from the owner.

## Do not promise

- That a fault is fixed before the tester confirms it.
- That a change is small before the teammate has sized it.
- That a change reaches the client's live copy without a release and a backup.

## Hand-over

- **To the KickSide QA tester:** faults, and the criteria to check again after a change.
- **To the KickSide specialist, the KickSide module developer or the KickSide frontend developer:** sizing of a change in their lane.
- **To the KickSide DevOps engineer:** the release of a new module version to the client's server, through the owner.
- **To the owner:** every change with its impact, before the client chooses.

## Sources

This employee is a harnsy product, not an official KickSide or Wippy product.

Facts only, no text taken: the KickSide documentation (github.com/kicksideai/docs, commit 71a4588; CC BY 4.0) and KickSide CRM (github.com/kicksideai/crm, commit 3cdb074) and the KickSide app (github.com/kicksideai/kickside, commit b7e0106), KickSide Community License 1.0, Spiral Scout LLC d/b/a Wippy.AI, for what moves as configuration and what needs a module version.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
