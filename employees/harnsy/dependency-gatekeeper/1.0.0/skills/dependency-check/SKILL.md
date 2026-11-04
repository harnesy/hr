---
name: dependency-check
description: Check one exact library, tool or outside service before it is adopted - authentic source (not a look-alike name or personal fork), maintenance in the last twelve months, releases and maintainers, review and CI signals, security policy and response, advisories for the exact version read as affected ranges with aliases and withdrawn records, interface stability, secure defaults, size and indirect dependencies, install-time scripts, licence present (flagged, not judged), adoption, and a trial in an isolated environment - on a one-page card with a source and read date per row. Use when a team wants to add a dependency and nothing already in use fits.
---

# Dependency check

A new dependency brings its own code, its own dependencies and its own future: upgrades, advisories, maybe a maintainer who walks away. This skill checks one exact candidate, the version that would be installed and the place it would come from, and writes the facts on one page with a source and a date for each, so the verdict rests on evidence rather than reputation.

**Route:** one candidate (name, version, source) and its intended use → **dependency-check** → `exit-cost` → verdict card → licence flag to the open source licence specialist.

## When to use

- When a team wants to add a library, tool or outside service and the already-have check found nothing in use that fits.
- When an existing dependency is about to be upgraded by a major version or replaced.
- Not as an ongoing audit of all dependencies (the application security reviewer's work), and not for licence compatibility (the open source licence specialist).

## Inputs

- The candidate: name, exact version, the source it would be installed from.
- What it is for, in one sentence, and how deeply it would be used.
- Read access to the project's lock files.

## Steps

1. **Authenticity:** the name matches the project's own source and package listing; not a look-alike spelling, not a personal fork. Note the project's own source link.
2. **Maintenance:** commits and releases in the last twelve months, the date of the latest release, how many active maintainers and from how many organisations; an archived project is the weakest signal. A small finished utility may need little activity: note it, do not punish it.
3. **Version signal:** whether the version string marks the project as unstable (0.x, alpha, beta, release candidate).
4. **Quality signals:** review before merge, tests run in CI on changes, a security policy, a licence file present, build dependencies pinned, an update tool in use.
5. **Advisories for the exact version:** search the advisory databases; for each record read the affected range (introduced, fixed, last affected), aliases (the same flaw under another id) and status (a withdrawn record is not a finding). A version is affected only inside a range.
6. **Security response:** how fast past advisories were fixed, whether older release lines get fixes, whether there is long-term support.
7. **Stability:** whether the public interface changes often, and whether there is a written policy for breaking changes; an unstable interface makes later security upgrades costly.
8. **Defaults and footprint:** secure defaults; size; how many indirect dependencies it pulls in and how current they are; install-time scripts; anything new that would run in production.
9. **Licence:** that one is present and named; flag it for the open source licence specialist, without judging compatibility.
10. **Adoption:** real use by others, as a sign only.
11. **Trial:** install it in an isolated environment, look quickly through the code for unfinished or suspicious parts, obfuscated values and unexpected network calls at install time.
12. **Write the card,** one row per check, with the finding, the source and the date read.

## Rules

- **The exact version** from the exact source; nothing about «the library in general».
- **Sources and dates on every row.** A fact without a source is marked «not found».
- **Scores are signs.** No automated score is presented as a verdict on its own.
- **Read-only.** Nothing is added to the project; the trial runs in an isolated environment, never in production or on a shared machine.
- **Licence flagged, not judged.**

## Checks before hand-over

- Every row has a finding, a source and a read date, or «not found».
- Advisories are reported with range, aliases and status against the exact version.
- The licence is flagged for the open source licence specialist.
- Nothing was installed outside the isolated environment.

## Artefacts

- `deps/<name>-<version>-check.md`: the one-page card.

## Hand-over

- **To `exit-cost`:** the card, for the cost of leaving.
- **To the open source licence specialist:** the licence flag.
- **To the application security reviewer:** anything that needs a deep code or security review.

## Sources

Built on the Concise Guide for Evaluating Open Source Software (OpenSSF Best Practices Working Group; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: necessity, authenticity, maintenance and release signals, maintainers, version stability, security response, vulnerabilities, interface stability, secure defaults, licence, adoption, isolated trial, indirect dependencies, quick code look. Built on the OpenSSF Scorecard checks documentation and the OSV schema (OpenSSF Scorecard Authors and OSV schema contributors; Apache License 2.0, https://www.apache.org/licenses/LICENSE-2.0), modified: signals and their blind spots, affected ranges, aliases and withdrawn records. Built on the GOV.UK Service Manual, «Managing software dependencies» (Government Digital Service, Crown copyright), adapted: trust the specific version, test before trusting. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Guides, «Dependency remediation» (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: choices when no fixed version exists.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
