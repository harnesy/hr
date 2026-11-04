---
name: contribution-triage
description: Sort incoming issues and pull requests, in arrival order, into one outcome each - labelled, duplicate, needs info, accepted, or declined with a polite reason, a link to the written rule and a concrete alternative - as a proposed batch that the project owner's written rules allow or a person applies. Use on the incoming queue of a long-lived project, daily or on the rhythm the maintainers agreed.
---

# Contribution triage

An open project receives more than it can take: bug reports without the details needed to reproduce them, duplicates, ideas outside its scope, large pull requests nobody asked for. Leaving them open out of politeness helps nobody. This skill gives every item one clear outcome and a short, kind answer that says why and what the person can do next, pointing to the written rules so a «no» is about the project's criteria and not about anyone's taste.

**Route:** new issues and pull requests → **contribution-triage** → a proposed batch for the project owner → applied (by the maintainers, or by the agent where the owner's written rules allow) → accepted bugs to the developers, ready pull requests to `patch-series-review`.

## When to use

- On the incoming queue, daily or on the agreed rhythm.
- When an old queue has to be cleared.
- Not for reviewing the code of a pull request (`patch-series-review`), and not for security reports, which go privately to the people named in the project's security policy.

## Inputs

- The new issues and pull requests since the last triage.
- The project's written rules: contributing guide, scope or vision, code of conduct, labels in use, how long maintainers wait for a reply.
- Who owns which area of the code.

## Steps

1. **Take the items in arrival order.** Each gets exactly one outcome.
2. **Label:** type (bug, feature, docs, question), area, and «good first task» when it is small, clear and has a known solution.
3. **Duplicate:** link the original, thank the person, close.
4. **Needs info:** list exactly what is missing (version, steps to reproduce, what was expected, what happened, logs) and the date after which the item closes if there is no reply; say that it can be reopened with the details.
5. **Accepted:** in scope and clear; name an owner or mark it as open for help.
6. **Declined:** out of scope or against a written rule. In one or two sentences: thank the person, give the reason in terms of the project's criteria, link the rule, offer a concrete alternative (an extension point, a plugin, a separate project), close.
7. **Large pull request without an earlier issue:** thank the person, ask for an issue that describes the problem first so the approach can be agreed before more work, and keep the pull request open for an agreed time.
8. **Someone keen but repeatedly short of the bar:** the same clear reason each time and a smaller task to try, such as a «good first task» item.
9. **Keep decisions in public** on the item; a question sent privately is answered on the public item where that is safe.
10. **Propose the batch:** a table with item, outcome, the answer text and the label, for the project owner. Apply it only where the owner's written rules allow the agent to label or close; otherwise a maintainer applies it.

## Rules

- **Every item gets an answer.** Nothing is closed silently or left open out of guilt.
- **Kind and firm.** Thank first, then the reason and the next step; one or two sentences are enough.
- **The rule, not the person.** A «no» points to the written criteria; it never judges the contributor.
- **No promises.** No dates or acceptance promised for future work.
- **No merge.** Triage never merges anything.

## Checks before hand-over

- Every item has one outcome and an answer text.
- Every decline has a reason, a link to the rule and an alternative where one exists.
- Every «needs info» lists the missing items and a closing date.
- Security reports were moved out of the public queue.

## Artefacts

- `triage/<date>.md`: the batch table (item, outcome, label, answer, applied by).

## Hand-over

- **To the project owner:** the batch, for approval, and repeated questions that suggest a change to the contributing guide.
- **To the developers:** accepted bugs with their reproduction steps.
- **To `patch-series-review`:** pull requests that are in scope and ready for review.
- **To the release manager:** accepted items that affect the next release.

## Sources

Built on Open Source Guides, «Best practices for maintainers» and «Building welcoming communities» (Open Source Guides authors; CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted: written rules make a decline less personal, close unwanted contributions with thanks, a reason and a suggestion, ask for an issue before large work, label easy issues, keep decisions public, mentor keen newcomers with smaller tasks. Content based on github.com/github/opensource.guide used under the CC-BY-4.0 license. Built on 18F Guides, code review (github.com/18F/guides at debc24b; 18F, U.S. General Services Administration; CC0 1.0), adapted: agree the review rules and write them down.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
