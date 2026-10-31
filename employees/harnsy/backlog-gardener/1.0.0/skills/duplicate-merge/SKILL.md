---
name: duplicate-merge
description: Find groups of backlog items about the same problem, read each in full, propose one survivor with the reason (most information, most watchers or oldest), list exactly what moves over (steps, environment, new facts, watchers, labels, links), draft the pointer comments, and mark related items that are not duplicates. Merges and closes nothing; the owner approves. Use during a backlog sweep or when the same request keeps coming back.
---

# Duplicate merge

The same problem filed three times splits the discussion, the evidence and the watchers three ways. This skill finds those groups, picks the item that should carry on, and lists exactly what the others hold that must not be lost, so the owner can approve the merge with one look.

**Route:** a backlog → **duplicate-merge** → the owner's yes or no per group → (if asked) applying the approved merges.

## When to use

- During a backlog sweep, or when the same request keeps coming back.
- When a new item looks familiar and someone asks whether it already exists.
- Not for judging whether a request should be done at all (that is the product owner's).

## Inputs

- Read access to the tracker or an export with item id, title, description, created date, watchers or followers, labels, links.
- Search access to find items with the same error text or wording.

## Steps

1. **Find candidate groups:** same symptom, same request, same error text, same area of the product. Title similarity (the script below) is a lead, not a verdict.
2. **Read every item in the group in full,** comments included.
3. **Decide duplicate or related:** the same problem is a duplicate; a similar problem with a different cause or request is related. Related items get a link, not a merge.
4. **Propose the survivor:** the item with the most information, the most watchers, or the oldest, and say which reason applied.
5. **List what moves over** from each other item: steps to reproduce, environment details, comments with new facts, watchers, labels, links.
6. **Draft the pointer comments** for the items that would close: thank the reporter and link the survivor.
7. **Send the groups to the owner** for a yes or no per group.

## Rules

- **Nothing is lost.** Every useful fact in a closing item is on the move-over list.
- **One survivor per group, with the reason.**
- **Related is not duplicate.** When in doubt, link and ask.
- **Nothing merged or closed** before the owner's written yes.

## Checks before hand-over

- Every item in every group was read in full.
- Each group has one survivor, a reason and a move-over list.
- Related items are marked as such.
- Nothing was changed in the tracker.

## Artefacts

- `backlog/duplicates-<date>.md`: groups, survivor and reason, move-over list, draft comments, related items.

## Tools

`scripts/similar_titles.py` lists pairs and groups of items whose titles are similar, from a CSV export. It is read-only. Example: `python3 scripts/similar_titles.py export.csv --id id --title title --min 0.8 --csv-out pairs.csv`. `--min` is the similarity from 0 to 1 (default 0.8); `-` reads standard input; at most 5000 items per run. It stops with exit code 2 on a missing column or file. Similar titles only point to items worth reading; different titles can still be duplicates, so search the error text too.

## Hand-over

- **To the backlog's owner:** the groups, for a yes or no per group.
- **To the QA engineer:** groups where it is unclear whether two bugs share a cause.

## Sources

Built on the Python Developer's Guide, triage pages «Triaging an issue» and «Issue tracker» (python/devguide at 734d750; Python Software Foundation; CC0 1.0), adapted: search for duplicates before triage, close a duplicate pointing to the surviving item. Built on Open Source Guides, «Best practices for maintainers» (© Open Source Guides authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: link to earlier discussion, keep the conversation in one public place. Content based on github.com/github/opensource.guide used under the CC-BY-4.0 license.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. The script in `scripts/` is © 2026 Pavel Buchnev (harnsy), MIT License (see LICENSE).
