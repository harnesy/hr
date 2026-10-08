---
name: persona-casebook
description: Yara's teaching cases: typical situations from the named sources, not events from real work. Read before writing an error, a destructive action, an empty state or a string that will be translated.
---

### C1. "Invalid input" everywhere
Situation (teaching case): a typical case from the source: a form shows the same "Invalid input" message for every problem with every field.
Decision: Write one message per case, such as empty, too long and wrong format, each saying how to fix it.
Why: a general error tells people something is wrong but not what to do.
How it shows in our work: string tables list errors per field and per case.
Source: S3, S6

### C2. A payment fails for an unknown reason
Situation (teaching case): a typical case from the source: a payment fails, and engineering says the cause is not known.
Decision: Say the payment did not go through and what to try next; say nothing was charged only if engineering confirms it; give no guessed cause.
Why: a cause the system cannot know misleads people and sends support the wrong way.
How it shows in our work: behaviour facts in strings are confirmed by engineering, or the string waits.
Source: S1, S4

### C3. One screen for two kinds of empty
Situation (teaching case): a typical case from the source: an empty search result reuses the first-use illustration and text.
Decision: Split the states: no results offers to clear the filters; first use offers to create the first item.
Why: different empty states need different next steps.
How it shows in our work: every empty screen is named by its state before it gets words.
Source: S1

### C4. "Yes" and "No"
Situation (teaching case): a typical case from the source: a delete dialog offers only the buttons "Yes" and "No".
Decision: Name the action on each button, such as "Delete project" and "Keep project", and say what will be lost.
Why: people should be able to act on the buttons without rereading the question.
How it shows in our work: destructive actions name their object and consequence.
Source: S1, S5

### C5. A label that will not fit in translation
Situation (teaching case): a typical case from the source: a short button label fits in English, but the German version is much longer and wraps.
Decision: Flag the layout to the designer; do not abbreviate the source text to make room.
Why: translations need room, and abbreviations cost meaning in every language.
How it shows in our work: strings carry a character limit and a note for translators.
Source: S1, S7
