---
name: release-notes
description: Write release notes for the people who use the software, in plain words, drawn from the changelog section of one version; say what changed, who it affects, whether anyone must act and where to read more, and promise nothing that is not in the release. The owner approves and publishes. Use for every release that users, administrators or support will notice.
---

# Release notes

Release notes tell users what a new version means for them. They are a short, chosen selection from the changelog, written in everyday words, with clear instructions when someone has to do something. This skill drafts them; the owner approves and publishes them.

**Route:** the version's changelog section → **release-notes** → the owner and product manager review → the owner publishes at release time.
Before this skill: an approved changelog section for the version. After it: a draft for approval; publishing belongs to the owner.

## When to use

- Every release with changes that users, administrators, operators or support will notice.
- A security or bug-fix release that asks users to act.

## Inputs

- The changelog section for the version.
- The audiences: end users, administrators or operators, integrators, support staff.
- Links to documentation for each notable change.
- The release date, only as fixed by the owner.

## Rules

- Written for users, in plain words. No internal names, ticket numbers or team names unless users know them.
- Drawn from the changelog; the changelog stays the full record. Nothing appears in the notes that is not in the release.
- No future features or dates promised, and no dates of other teams.
- No promised uptime, speed or saving. A measured improvement may be described only as measured, with how, and only if the owner agrees to include it.
- Generated drafts (from commits or request titles) are a start; a person chooses and rewrites.
- The agent drafts; the owner approves and publishes. The agent never publishes or announces a release itself.

## Steps

1. **Pick what needs a note:** anything a user or operator can see or must handle: changes to screens, commands, APIs or configuration, changed behaviour, deprecations and removals, fixes of known issues, security fixes. Leave out tests, build changes and fixes for bugs that were never released.
2. **Group by audience or by importance:** start with anything that requires action, then the main new features, then changes and fixes.
3. **Write each note** in the past tense and plain words. For each, say:
   - what kind of change it is (added, changed, fixed, deprecated, removed);
   - what it means for the reader;
   - whether the reader must do anything, and how («Action required: …»);
   - the exact feature, setting, field or command it touches;
   - where to read more (a documentation link).
4. **Add the essentials** for upgrading: required steps, any downtime notice the owner has approved, and where to get help.
5. **Check every claim** against the changelog and the release itself; remove anything that is planned but not shipped.
6. **Read it as a user:** is the purpose of each change clear, and does each note matter to someone? Rewrite or remove notes that fail.
7. **Send for review** to the product manager and the owner; apply their changes.
8. **Hand to the owner** for publishing at release time, in the channels they choose.

## Checks before hand-over

- Every note matches something in the release and its changelog.
- Notes that need action say so first and explain how.
- Plain words, past tense, documentation links where useful.
- No promised futures, other teams' dates, uptime, speed or saving.
- Nothing was published by the agent.

## Artefacts

- `releases/<version>-notes.md`: the draft for approval.

## Hand-over

- **To the release owner:** the draft for approval and publishing.
- **To the product manager:** wording, emphasis and what to highlight.
- **To support:** the notes and prepared answers for expected questions.
- **To the API technical writer:** changes that need updates in the reference or migration guides.

## Sources

Built on «Keep a Changelog» 2.0.0 (github.com/olivierlacan/keep-a-changelog, commit 08d0df5; © 2014 Olivier Lacan and contributors, MIT licence), adapted. Built on the Kubernetes contributor guide, «Adding Release Notes» (github.com/kubernetes/community, commit 1490663; © The Kubernetes Authors, Apache License 2.0), changed. Built on 18F Guides, «Software launch checklist» (github.com/18F/guides, commit debc24b; US General Services Administration, public domain in the US and CC0 1.0 elsewhere), adapted; no endorsement by GSA is implied.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
