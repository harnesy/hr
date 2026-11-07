---
name: plugin-submission-report
description: Write the one report per plugin submission that the person decides on: verdict first, the check and code review results, the card table, the enable view, the card, findings for the author as one list, a recommendation and the decision request (Publish, Back to the author, Reject). Also prepares a revocation for the person's word. Use after plugin-card-check.
---

# Plugin submission report

The person decides whether a plugin is published; this report is what they decide on. It holds one submission, starts with the recommendation, and ends with the question. Everything in between is evidence they can check without opening the plugin.

**Route:** plugin-card-check → **plugin-submission-report** → the person's word → those who hold the catalog's keys act on it.

Write it in the person's language; the card inside it stays in English. Send it to whoever the work came from (its lead, or the person).

## Template

```markdown
# Plugin submission: <publisher>/<name>@<version> — <title>

**Recommendation: <Publish | Back to the author | Reject | Not yet: waiting for the code review>.** <the reason in one sentence>

## Plugin
- <publisher>/<name>@<version>, where it is (folder or submission link), author.
- Files: <from the check's files>. README, licence, screenshots: <present or missing>.

## Automatic check
- harnsy <version>: `harnsy plugin check <folder> --json --publisher <publisher>`
- Result: passed, or the error line as it is.
- needs: […]; linked: <true|false>; entries: […].

## Code review
- <approved | changes asked | not done yet>, by the catalog's code reviewer, <link or date>.
- Without an approval the plugin is not verified, and publishing is not recommended.

## Card against the plugin
| Claim | Evidence | Result |
| --- | --- | --- |

## What the person sees when enabling
- Rights in plain words, one line each.
- The linked sentence, or «not linked».
- Consent tick: needed / not needed, and why.

## Card (English, for the catalog page)
> **<title>**
> What it does. For whom. An example.
> **What it asks and why.** One line per right.
> **What it does not do.**
> (After an approved code review only:) Verified: harnsy's AI security reviewer read this version's code and found that it matches what it declares and that project data leaves only to the declared hosts. It is a review of one version, not a guarantee against bugs.

## Other
- Licence: <name, or missing>. Credits for text and pictures it is built on.
- Screenshots: this version, no personal data or secrets.
- Keys, proofs, tokens in the submission: none (if any: see «Stop» below).

## Findings for the author
1. <claim> — <evidence> — <the fix>.
Fixed: <which, after which round>.

## Decision
Waiting for your word: «Publish», «Back to the author» or «Reject». Submitted: <date and time>.
```

## Rules for each part

- **Recommendation first.** One of four, then one sentence. «Publish» only when the check passed, the code review approved this exact version, the card table has no open fix, and the licence is there.
- **Findings as one list.** Every finding for the author in one message, each with the claim, the evidence and the fix, so the author fixes everything in one round. A second round only for real changes, and only on those findings.
- **No guessing.** A part you could not check says «not checked» and why.
- **Never** write «secure», «safe» or «guaranteed», and never call a version verified before its code review approved it. Once it is approved, «verified» is said only in the template's sentence, word for word.
- **Record the word.** When the person answers, add their decision and the time from submission to decision. Until then, nothing is merged, signed or published.

## Stop: a key, proof or token in a submission

Stop the report. Tell the person at once: which file, what kind of secret (not its value). The pull request is public: removing the file does not erase it from the history, so the author must treat the key as leaked and replace it. Do not copy it into the report, a note or a message. The author removes it from the submission; a proof is prepared again on the author's node. Never ask an author for a key or a proof.

## Revocation

When a plugin is reported, or a published version looks harmful:

1. Collect the evidence: the report, the version, what was seen, where.
2. Prepare the change, do not make it:
   - the revoked line `<publisher>/<name>@<version>` for the catalog's revoked list;
   - the file to remove: the version's `.harnsy` in the catalog's packs, when the person decides the file goes too.
3. Tell the person at once, with the evidence and what revoking does: the version is turned off in every project that enabled it when the node next reads the catalog, and cannot be enabled again; a computer that is offline, or has the catalog reading switched off, learns of it only when it can read the list. Do not promise a time.
4. Act only on the person's word; the change is made by whoever holds the catalog's keys. Record the decision.

## Hand-over

- **To the person** (through whoever the work came from): the report, and later the recorded decision.
- **To the author:** the findings list, in the author's language, after the person agreed to send it back. It starts with «Written by an AI agent (the catalog curator).» For «Back to the author» and «Reject» it ends with: the rule it rests on (the line of the contributor terms or CONTRIBUTING), that an AI agent wrote it, that a person decides, and «Comment on the pull request, or write to hello@harnsy.dev; a person looks at it again.»

## Sources

harnsy documentation 0.11.0: docs/plugin-catalog-v1.md and llms/plugins.txt (read 4 Nov 2026). Described in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence. No scripts are carried with this skill.
