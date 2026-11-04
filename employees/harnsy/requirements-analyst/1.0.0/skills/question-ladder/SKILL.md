---
name: question-ladder
description: Stress-test a request or a draft spec by questions, one at a time - for each key term or claim ask for a definition, an example, a case that would break it, show where two answers clash and ask what follows; answers recorded in the person's own words with a status; never answered for the person; a stop after the agreed rounds (three by default) with open points passed on as working assumptions. Use before anyone plans work on a request.
---

# Question ladder

Most requests rest on words that mean different things to different people («active customer», «real time», «simple») and on claims nobody has checked. This skill climbs the same ladder of questions for each key term or claim until the meaning holds or everyone can see it does not, while the person answering stays the owner of every answer.

**Route:** a request or draft spec → **question-ladder** → open points → `assumption-log` → `problem-statement` → the business analyst and the product manager.

## When to use

- A request arrives that could be read in more than one way.
- A draft spec is about to be planned and nobody has questioned its key terms.
- Two people use the same word and seem to mean different things.
- Not for interviewing users about their lives and work in general: that is research, for the ux researcher.

## Inputs

- The request or the draft spec.
- Who can answer (the requester, stakeholders), and that they agreed to take part.
- How many rounds there is time for (three by default) and the deadline.

## Steps

1. **Pick the rungs' targets.** Underline the key terms and the claims the request depends on. Start with the one that the most work hangs on.
2. **Explain the purpose without steering.** Say what the questions are for, and that there are no right answers to guess.
3. **Climb one rung at a time,** one question per message, and wait for the answer:
   - **Definition:** «What do you mean by …?»
   - **Example:** «Could you give one real example from the last month?»
   - **Counter-example:** offer a case that would break the definition and ask whether it counts.
   - **Contradiction:** where two answers do not fit together, show both side by side and ask which holds, or whether both are needed.
   - **Consequence:** «If that is so, what follows for …?»
4. **Follow the answer.** Ask «why is that?» and «how do you handle it today?»; allow silence; do not rush to the next rung.
5. **Record each question** with the answer in the person's own words and a status: settled, open, or contradicts #n. Never write «so you mean X» unless the person agrees to X.
6. **Ask about people.** What is assumed about the users, and how the result could harm someone if it goes wrong.
7. **Stop on time.** After the agreed rounds, stop. List what is settled and what is open, and pass every open point to `assumption-log`.

## Rules

- **Never answer for the person.** An unanswered question becomes a marked working assumption with an owner, never a guess written as an answer.
- **One question at a time.** Several questions at once get one answer.
- **Their words, not yours.** Answers are recorded as said.
- **No traps.** Counter-examples and contradictions are shown to clarify, never to embarrass anyone.
- **Consent and privacy.** Only people who agreed take part; no personal details the work does not need; no recording without consent.

## Checks before hand-over

- Every key term has a definition and at least one example, or is marked open.
- Every contradiction found is shown with both answers.
- No answer in the record was written by the analyst.
- The rounds used and the open points are listed at the end.

## Artefacts

- `requirements/<request>/questions.md`: numbered questions, answers in the person's words, status, rounds used, open points.

## Hand-over

- **To `assumption-log`:** every open point.
- **To the business analyst:** the question record, for the spec.
- **To the product manager:** contradictions that need a decision.

## Sources

Built on 18F Methods, «Stakeholder and user interviews» (18F, U.S. General Services Administration; CC0 1.0), adapted. The order of questions (definition, example, counter-example, contradiction) follows the questioning method widely known from classical philosophy; described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
