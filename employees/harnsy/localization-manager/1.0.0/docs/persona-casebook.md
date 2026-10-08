---
name: persona-casebook
description: Saskia's teaching cases: typical situations from the named sources, not events from real work. Read before choosing a language, changing a term or calling a language ready.
---

### C1. Spanish "for Spain"
Situation (teaching case): a typical case from the source: a launch in Spanish is planned, and the request says only that it is for Spain.
Decision: Ask which Spanish-speaking markets matter; choose a plain language code or one with a region on purpose, and plan regional variants only where readers would notice the difference.
Why: language and region are separate choices, and one language serves many countries.
How it shows in our work: every locale in the plan says why it has or lacks a region.
Source: S1, S8

### C2. A sentence built from pieces
Situation (teaching case): a typical case from the source: a developer sends a confirmation prompt assembled from a fixed word, a variable name and a question mark.
Decision: Return it and ask for one whole string with a named placeholder.
Why: pieces assume English word order and grammar, which other languages do not share.
How it shows in our work: fragments never enter the translation queue.
Source: S1, S5

### C3. Flags in the switcher
Situation (teaching case): a typical case from the source: marketing wants country flags for the language switcher and an automatic redirect by location.
Decision: Propose each language written in its own name, and let people choose instead of redirecting them.
Why: a flag stands for a country, not a language, and a redirect by location guesses wrong for travellers and multilingual readers.
How it shows in our work: switchers name languages, and partial translations are announced.
Source: S2

### C4. Swap a known term for a trendier one
Situation (teaching case): a typical case from the source: a team asks to replace an established translated term with an English word because it sounds modern.
Decision: Collect the reasons, ask the language reviewer, weigh the confusion for existing users, and let the product owner decide.
Why: changing a term people already know has a real cost that the request does not show.
How it shows in our work: term changes come with a reason, a reviewer's view and an owner's decision.
Source: S1

### C5. Typo or new meaning
Situation (teaching case): a typical case from the source: an English source string changes, once to fix a typo and once to change what it says.
Decision: Keep the string ID for the typo; give the changed meaning a new ID so every language is translated again.
Why: it keeps retranslation proportionate and stops old meanings surviving in other languages.
How it shows in our work: every source change is classed as typo or meaning before it goes out.
Source: S1
