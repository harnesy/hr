---
name: changelog
description: Keep a changelog for developers and integrators, newest version first, each version with its date and its changes sorted into Added, Changed, Deprecated, Removed, Fixed and Security, breaking changes marked, and an Unreleased section on top; curated from the merged work, never a pasted commit log. The owner approves and publishes. Use with every release and whenever a notable change is merged.
---

# Changelog

A changelog is the full record of notable changes, version by version, for people who build on the software. This skill gathers what was merged, keeps only what matters to them, sorts it into fixed types, marks anything that breaks existing use, and keeps the file in order. The owner approves and publishes it.

**Route:** merged changes → **changelog** (Unreleased section) → at release, the section becomes a dated version → the owner approves and publishes → **release-notes** are drawn from it.
Before this skill: the merged work since the last version. After it: an updated changelog file for the owner's review.

## When to use

- When a notable change is merged: add it to Unreleased.
- At release time: turn Unreleased into the new version.
- When a project has no changelog yet: start one from now on, and fill in past versions if the owner wants.

## Inputs

- The list of merged changes since the last version: commits, pull or merge requests, linked tickets.
- The version scheme the project uses and the new version number, from the owner.
- The previous changelog, if there is one.

## Rules

- Written for developers and integrators. Plain, short entries; one change per line.
- Newest version first. An Unreleased section stays at the top.
- Each version heading has the version and its release date (year-month-day), filled in when the owner publishes.
- Six types only: Added, Changed, Deprecated, Removed, Fixed, Security. Dependency updates appear only by their effect, under the right type.
- Breaking changes are marked in the entry itself, with what users must do or a link to upgrade steps. Deprecation comes before removal, with the version that will remove it, if known.
- Curate, do not paste the commit log. Leave out tests, build tooling and fixes for bugs that were never released.
- Nothing is listed that is not in the release. No future dates or features are promised.
- The agent drafts; the owner approves and publishes. The agent never tags a version or publishes the file itself.

## Steps

1. **Collect** the merged changes since the last version. Generated lists from commit messages or request titles are a starting point only.
2. **Filter:** keep what someone using or integrating the software would notice: interfaces, behaviour, configuration, output formats, performance characteristics, deprecations, removals, fixes of released bugs, security fixes.
3. **Sort** every entry under exactly one of the six types. Name the area it touches (for example «API», «CLI», «config») when that helps the reader.
4. **Write each entry** in plain words, saying what changed and why it matters; link the ticket or documentation.
5. **Mark breaking changes** and add a short upgrade note or a link to a migration guide.
6. **Check against the release:** every entry matches something actually in the version, and nothing notable in the version is missing.
7. **At release,** rename Unreleased to the version and date given by the owner, add comparison links between versions if the project uses them, and open a new empty Unreleased section.
8. **Mark a withdrawn version** as yanked, with the reason, instead of deleting it.
9. **Run mechanical checks** if the project has them: headings, dates, links, order. Wording stays a human review.
10. **Send for approval** to the owner, together with the diff of the file.

## Checks before hand-over

- Newest first, Unreleased on top, each version dated.
- Every entry is under one of the six types; breaking changes are marked.
- No commit-log dump, no internal-only changes, no promised futures.
- Every entry matches something in the release.
- Nothing was tagged or published by the agent.

## Artefacts

- `CHANGELOG.md` in the repository root (or the project's existing changelog file), updated.
- The diff of the file for the owner's review.

## Hand-over

- **To the release owner:** the updated changelog for approval and publishing.
- **To the API technical writer:** API changes, deprecations and breaking changes for the reference docs and migration guides.
- **To the release-notes skill or the product manager:** the version section as the source for release notes.
- **To the security reviewer:** Security entries before they are published.

## Sources

Built on «Keep a Changelog» 2.0.0 (github.com/olivierlacan/keep-a-changelog, commit 08d0df5; © 2014 Olivier Lacan and contributors, MIT licence), adapted. Built on the Kubernetes contributor guide, «Adding Release Notes» (github.com/kubernetes/community, commit 1490663; © The Kubernetes Authors, Apache License 2.0), changed.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
