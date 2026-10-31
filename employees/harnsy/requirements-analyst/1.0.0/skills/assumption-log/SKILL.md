---
name: assumption-log
description: Keep a log of things believed true without evidence - one row per assumption with the statement, who said it (or «inferred»), evidence for and against, the risk if it is wrong, how to check it, possible harm to users, owner, status and date - so that open questions become visible, owned, checkable working assumptions instead of silent guesses. Use whenever a question stays unanswered or an answer rests on opinion. For things that may happen in future, use a risk log instead.
---

# Assumption log

An assumption is something a plan treats as true without evidence yet. Every plan has some; the trouble starts when nobody can see which ones. This skill writes each one down, says who holds it and how it could be checked, and keeps its status up to date until it is confirmed or dropped.

An assumption is not a risk: an assumption is believed true now without proof («shop staff use tablets»); a risk is something that may happen («the supplier may be late»). Keep risks in a risk log.

**Route:** open points from a round of questions, a spec, a plan or a meeting → **assumption-log** → checks run by their owners → confirmed rows move into the problem statement, spec or plan they came from.

## When to use

- A question stays unanswered after the agreed rounds.
- An answer comes from opinion, not from users or data.
- A plan, a spec or an estimate depends on something nobody has checked.

## Inputs

- The open points and opinions, with who said them.
- Any evidence already at hand (research notes, data, support tickets).

## Steps

1. **Write the statement** as a plain sentence that could be true or false: «Most buyers order from a phone.»
2. **Name the source:** who said it, or «nobody — inferred» when it was read between the lines.
3. **Evidence for and against,** each with where it comes from. «None yet» is a valid entry.
4. **Risk if wrong:** what breaks or is wasted if the statement is false, rated high, medium or low.
5. **Harm check** for high rows: what could go wrong for users, or for people outside the team, if it is false.
6. **How to check:** the cheapest way to find out (look at data, ask five users, test a prototype, ask the person who knows).
7. **Owner and date:** one named owner who will check or decide, and the date logged.
8. **Status:** open, confirmed (with the evidence), or dropped (with the reason). Change status only with a new entry in the row's history, never by deleting.
9. **Review** the log before each planning meeting: high-risk open rows first.

## Rules

- **No assumption without an owner.**
- **The analyst does not confirm its own guesses.** Confirmation needs evidence or the owner's decision.
- **Append, do not erase.** Status changes are added with a date; the history stays.
- **Plain sentences.** One assumption per row; split compound ones.

## Checks before hand-over

- Every row has a statement, source, risk, check, owner, status and date.
- Every high-risk row has a harm check and a planned check.
- No row is marked confirmed without its evidence.

## Artefacts

- `requirements/<request>/assumptions.md`: the table, IDs A1, A2, …, with each row's history underneath.

## Hand-over

- **To the product manager:** the log, sorted by risk, to decide which assumptions are checked first.
- **To the ux researcher:** rows that need evidence from users.
- **To the author of the problem statement, spec or plan:** confirmed rows, and the IDs of the open ones it depends on.

## Sources

Built on the GOV.UK Service Manual, «Learning about users and their needs» (Government Digital Service, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Methods, «Stakeholder and user interviews» (18F, U.S. General Services Administration; CC0 1.0), adapted. Built on «Algorithms» (1st edition, 2019) by Jeff Erickson, section on specifying the problem (CC BY 4.0; algorithms.wtf), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
