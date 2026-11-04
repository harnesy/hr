---
name: stale-sweep
description: Sweep a backlog for stale items - no activity for the owner's number of days, or overtaken by a later decision - and propose close, refresh or keep for each with the reason and evidence, a kind draft closing comment that thanks the reporter, grouped by owner. Changes nothing in the tracker; the owner approves line by line. Use when a backlog has grown hard to read, or on the owner's regular rhythm.
---

# Stale sweep

A backlog full of items nobody will ever do hides the ones that matter, and leaves reporters waiting for an answer that never comes. This skill finds the items that have gone quiet or been overtaken, reads each one, and proposes close, refresh or keep, each with a reason the owner can check in seconds and a comment the reporter will find fair.

**Route:** a backlog and the owner's rules → **stale-sweep** → the owner's yes or no per line → (if asked) applying the approved lines.

## When to use

- When a backlog has grown hard to read, or on a rhythm the owner sets.
- Before a planning or refinement session, to shorten the list.
- Not for triaging new incoming items, and not for setting priorities (the product owner does that).

## Inputs

- Read access to the tracker or an export (CSV) with item id, title, status, last activity date, labels.
- The owner's rules: the number of days that counts as stale (asked, never assumed), labels or items never to propose, how long a waiting-for-reply item waits.
- Recent decisions: roadmap changes, closed epics, replaced components, decision records.

## Steps

1. **Get the rules** from the backlog's owner and write them at the top of the file.
2. **List quiet items:** no activity for the owner's number of days (the script below helps with an export).
3. **List overtaken items:** the feature was dropped, the component replaced, the question answered elsewhere; link the decision.
4. **Read each candidate in full:** opening message, comments, links.
5. **Propose one of three:** close (reason and a link to the superseding item, decision or documented scope); refresh (what is out of date and the question to ask the reporter); keep (why it still matters).
6. **Draft the comment** for each close or refresh: thank the reporter, give the reason, point to where things went, say what would reopen the question.
7. **Group the proposals by owner** and send each owner one table.
8. **Wait for a yes or no per line.** Apply approved lines only if the owner asks you to, in writing.

## Rules

- **Nothing changes without the owner.** No close, edit, label or comment is posted before a written yes for that line.
- **Evidence beside every proposal:** last activity date, the superseding item or decision, the link.
- **Kind and specific comments.** Thank the reporter, say why, point somewhere.
- **The never-propose list is respected.**
- **Disagreement is answered, not overridden.** If a reporter objects to a close, explain politely and ask for new information; the owner decides.

## Checks before hand-over

- The owner's rules are written at the top.
- Every proposal has a reason and evidence.
- Every close or refresh has a draft comment.
- Nothing was changed in the tracker.

## Artefacts

- `backlog/stale-<date>.md`: rules, table (item, last activity, proposal, reason, evidence, draft comment), grouped by owner.

## Tools

`scripts/stale_list.py` lists items with no activity for at least N days from a CSV export. It is read-only and prints a table; `--days` is required (the owner's rule). Example: `python3 scripts/stale_list.py export.csv --days 90 --id id --title title --updated updated --status status --open-status open,new --skip-label-col labels --skip-label keep --csv-out stale.csv`. Columns are named with flags; `--today YYYY-MM-DD` fixes the reference date; `-` reads standard input. It stops with exit code 2 on a missing column, an unreadable date or a missing file. The list is a set of candidates: each one is still read in full before a proposal.

## Hand-over

- **To the backlog's owner:** the table, for a yes or no per line.
- **To the QA engineer:** stale bug reports that may still be real, for a reproduction attempt.
- **To `duplicate-merge`:** candidates that turn out to repeat another item.

## Sources

Built on the Python Developer's Guide, triage pages «Triaging an issue», «Issue tracker» and «Labels» (python/devguide at 734d750; Python Software Foundation; CC0 1.0), adapted: read the first message and comments, pending items close unless the reporter replies, stale means inactive for a while, explain a close politely and do not reopen without new information. Built on Open Source Guides, «Best practices for maintainers» (© Open Source Guides authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: written vision and scope, close what will not be done quickly and kindly with a reason, automation for routine reminders, thank people. Content based on github.com/github/opensource.guide used under the CC-BY-4.0 license. Built on 18F Product Guide, «Roadmap» and «Build» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: the backlog as a prioritised list of user value, priorities set by the product owner.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
