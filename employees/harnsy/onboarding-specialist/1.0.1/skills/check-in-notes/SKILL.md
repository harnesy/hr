---
name: check-in-notes
description: Prepare and record two-way onboarding check-ins at about 30, 60 and 90 days: questions both sides answer beforehand, notes with facts and agreed actions only, visible to the newcomer and kept inside the onboarding project. Use before and after each check-in. Never a rating or a probation verdict.
---

# Check-in notes

A check-in asks how the start is going, from both sides, early enough to fix things. The notes are short: what was said about the work and what both sides agreed to do. They are never a verdict on the person.

**Route:** approved plan (from `onboarding-plan`) → **check-in-notes** at about 30, 60 and 90 days → open actions tracked → at day 90, the notes go to the manager who runs ongoing one-to-ones.

## When to use

- A few days before each check-in, to send the questions.
- Right after each check-in, to write the notes and the actions.
- Not for probation decisions, ratings or pay: those belong to the manager and HR.
- Not for ongoing one-to-ones after day 90: those belong to the manager.

## Inputs

- The plan and the expectations the manager set.
- Open actions from the last check-in.
- Feedback from peers, if the manager asked for it, as written by those peers.

## Steps

1. **Send questions to both sides** a few days ahead.
   - To the newcomer: how is it going; what is clear and what is not; what would help; anything worrying.
   - To the manager: what is going well; what to focus on next; anything the newcomer should hear now rather than later.
2. **Keep the rhythm.** If a check-in has to move, move it; do not drop it. The newcomer's topics come first.
3. **Write the notes after the meeting.** For each topic: what was said about the work, as facts («first pull request merged on day 9», «release steps still unclear»). Then the agreed actions, each with an owner and a date.
4. **Leave out** opinions about the person, guesses about motives, and anything about health, family, or other protected or private matters, even if it came up. If the newcomer raised something private and wants an adjustment, note only that they were told who to talk to (the HR generalist or the manager).
5. **Share.** The newcomer sees what the manager writes. Notes stay inside the onboarding project; they are not copied to other projects or channels.
6. **Track actions** to done, and carry open ones into the next check-in.
7. **At day 90,** write a short summary of open actions for the manager who continues the one-to-ones, and ask the newcomer what to improve for the next person.

## Rules

- Facts and agreed actions only. No ratings, scores or probation language.
- Never mention or guess a protected trait; a gap or a past change of career is not a concern to record.
- Notes are visible to the newcomer and stay inside the project.

## Checks before hand-over

- Every note is a fact about the work or an agreed action with owner and date.
- Nothing private, protected or speculative is written down.
- The newcomer has access to the notes.
- Open actions from the previous check-in are closed or carried forward.

## Artefacts

- `onboarding/<newcomer-ref>/check-in-<30|60|90>.md`: questions, notes, actions.
- `onboarding/<newcomer-ref>/actions.md`: open actions with owner, date and status.

## Hand-over

- **To the manager:** the notes and open actions after each check-in. The manager decides anything about the person, with the HR generalist where needed.
- **To the newcomer:** the same notes.
- **At day 90, to the manager or engineering manager** who runs ongoing one-to-ones: the open-actions summary.

## Sources

Built on the Sourcegraph handbook (archived) onboarding feedback milestones and onboarding reviews pages (© 2021 Felix Frederick Becker; Apache License 2.0; changed by harnsy), the PostHog handbook, onboarding (© 2020-2025 PostHog Inc.; MIT for the /contents/ folder), and the TTS Handbook one-on-ones page (Technology Transformation Services, GSA; CC0 1.0). All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
