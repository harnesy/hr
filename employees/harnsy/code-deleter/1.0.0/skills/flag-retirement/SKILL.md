---
name: flag-retirement
description: Review old feature flags and write the steps to retire the ones that no longer switch anything - for each flag its current value per environment from the flag source, last change, owner and kind, the candidates (fully on or fully off everywhere for the agreed period, no planned change), and removal steps that keep the live path, delete the other path, the flag check and its tests, with the flag service changed last and by a person. Use when flags pile up, before a large change in flagged code, or on a regular clean-up rhythm.
---

# Flag retirement

A feature flag is a switch in the code. Rollout and experiment flags are meant to be temporary: once the feature is fully on, or the experiment has ended, the switch no longer decides anything, but both paths stay in the code and both still have to be tested. Each on/off flag doubles the combinations to test. This skill finds the flags that no longer switch anything and writes the steps to remove them safely. It never changes a flag.

**Route:** the flag list from code search and the flag source → **flag-retirement** → the owner agrees per flag → one `safe-removal-pr` per flag → a person removes the flag from the flag service after the merge.

## When to use

- When the number of flags keeps growing, or nobody can say what some of them do.
- Before a large change in code that is full of flag checks.
- On a regular clean-up rhythm agreed with the team.
- Not to decide whether a feature should be on or off: that is the product owner's decision.

## Inputs

- Every flag the code reads, found by searching for the flag client's calls.
- The flag configuration from the flag source: an export, read-only access, or the owner's list. Values per environment and change history.
- Who owns each flag, from the flag source, the history or the team.

## Steps

1. **List the flags** the code reads, with the files and the number of checks for each. Note flags in the flag source that the code no longer reads, and code checks for flags the source does not know.
2. **Read the current value per environment** from the flag source, not from memory or defaults, and when each last changed.
3. **Name the owner** of each flag, or write «unknown — ask».
4. **Name the kind:** rollout and experiment flags should be short-lived; permission switches and emergency off-switches can be long-lived by design. For a long-lived one, ask whether it belongs in configuration or in the permission system instead of a flag.
5. **Mark the candidates:** short-lived flags fully on, or fully off, in every environment for the period the team agreed (for example 30 days), with no planned change.
6. **Write the removal steps** for each candidate: keep the path that is live; delete the other path, the flag check and the tests of the deleted path; remove configuration keys only the flag used; run the full test suite; and as the last step, after the merge and a release, a person deletes the flag from the flag service.
7. **Count what goes:** checks removed, code paths removed, tests removed, and the test combinations that disappear.
8. **Write the revert** for each: reverting the pull request brings back both paths; the flag entry stays in the flag service until the release is confirmed.

## Rules

- **The agent never changes a flag** in any environment; the flag service is read-only for it.
- **Values come from the source.** A value that could not be confirmed is marked «unconfirmed», and the flag is not a candidate until it is.
- **Code first, flag service last.** Deleting a flag the code still reads changes behaviour; deleting the code first does not.
- **The owner agrees per flag.** No candidate goes to a pull request without the owner's OK.
- **One flag per pull request**, so each can be reverted alone.

## Checks before hand-over

- Every flag has value per environment (confirmed or «unconfirmed»), last change, owner, kind and candidate status.
- Every candidate has removal steps ending with the flag service change by a person, and a revert.
- No flag was changed by the agent.

## Artefacts

- `cleanup/<date>-flags.md`: table of flag, values per environment, last change, owner, kind, candidate yes or no with the reason, removal steps, revert, and the counts.

## Hand-over

- **To the code owner:** the candidates, for an OK per flag.
- **To `safe-removal-pr`:** each agreed candidate, one pull request per flag.
- **To the flag owner:** the flag service change, after the merge and the release.
- **To `dead-code-scan`:** code that becomes unreachable once a flag is gone, for the next scan.

## Sources

An own procedure. Built on the GOV.UK Service Manual, «Manage your software configuration», «Maintaining version control in coding» and «Retiring your service» (Government Digital Service, Crown copyright), adapted: configuration kept and changed like code, small changes grouped by purpose and reviewed, temporary code removed once everyone has moved. Contains public sector information licensed under the Open Government Licence v3.0. Built on The Go Blog, «Finding unreachable functions with deadcode» (The Go Authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: code that becomes unreachable is removed together with what only it used.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
