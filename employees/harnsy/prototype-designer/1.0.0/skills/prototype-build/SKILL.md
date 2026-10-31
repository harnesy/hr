---
name: prototype-build
description: Build a throwaway clickable prototype (paper or plain HTML) that lets a person try one task end to end, on invented data, with a visible «prototype» marker on every page, shared only behind a password or locally, and a list of what is faked. Use after the question and the pass and fail signals are written, to test an idea before anyone specifies or builds it.
---

# Prototype build

A prototype is a question you can click. It exists to learn whether an idea works before anyone spends time specifying or building it, and it is thrown away afterwards. This skill builds the smallest prototype that answers the question in the test plan, makes sure nobody can mistake it for a real service, and lists exactly where it is faked.

**Route:** an idea and its chosen variant → test plan with the question and signals (`prototype-test-plan`) → **prototype-build** → sessions → findings → the ui designer specs the real screens; the product team decides.

## When to use

- An idea needs people's reactions before it is specified: a new flow, a page layout, a form, a new feature.
- The test plan names one question and the signals for pass and fail.
- Not for a production feature, a demo for buyers, or a design spec: those belong to the frontend developer, the sales engineer and the ui designer.

## Inputs

- The question the prototype answers, and the pass and fail signals, from the test plan.
- The chosen variant (from comparing two or three variants first) and the task participants will try.
- The kinds of data the screens need (names, amounts, dates, statuses), never the data itself.

## Steps

1. **Pick the fidelity.** Paper sketches answer questions about structure and order; clickable HTML pages answer questions about flow and wording and behave most like the finished thing. Choose the roughest kind that can answer the question.
2. **List the pages.** Only the pages a person needs to try the task from start to end. Anything the question does not need stays out, or is a dead end marked «not part of this prototype».
3. **Invent the data.** Made-up people, companies, amounts and dates, shaped like the real ones in fields and volume, and labelled as sample data. No real personal data, no production data, no real logins, not even «just for the test».
4. **Build rough on purpose.** Structure, wording and flow come first; polish waits. Use plain HTML and CSS or the team's prototyping kit; no connection to live systems, no real payments, no real email.
5. **Mark it.** Every page shows a visible «prototype» marker that cannot be missed. The page title says «prototype» too.
6. **Fake honestly.** Search, saving, payment and messages may be faked; list every faked part and what it does (for example «search always returns the same three results»).
7. **Share safely.** Run it locally on the session machine, or put it behind a password on a host that search engines cannot index. Never share it on a public link.
8. **Dry-run the task** once yourself, then once with a colleague who has not seen it, and fix dead ends that would stop the session for the wrong reason.

## Rules

- **Throwaway.** Prototype code is not secure, not built for load and never copied into the product. The findings travel to the ui designer; the code does not.
- **Invented data only.** If someone offers real customer records to make it realistic, decline and build invented records shaped like them.
- **No live systems.** The prototype reads and writes nothing real. Any change a live product seems to need is a proposal for its owner (current state, change, expected effect, how to undo it).
- **One question.** A prototype that tries to answer several questions answers none of them clearly; build a second prototype instead.

## Checks before hand-over

- Every page shows the «prototype» marker.
- All data is invented and labelled as sample data.
- The faked-parts list is complete, and the dry run found no dead end in the task.
- The prototype is local or behind a password, and not indexed.
- The question and signals from the test plan are written at the top of the faked-parts list.

## Artefacts

- `prototypes/<idea>/`: the pages (or photos of the paper sketches).
- `prototypes/<idea>/README.md`: the question, the signals, the task, the faked-parts list, where it runs and the password holder.

## Hand-over

- **To whoever runs the sessions** (the same agent with `prototype-test-plan`, or the ux researcher): the link or files and the README.
- **To the ui designer, after the round:** the findings, never the prototype code.
- **To the product manager:** the README, so the decision-maker knows what was and was not tested.

## Sources

Built on the GOV.UK Service Manual, «Making prototypes» (Government Digital Service, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Methods, «Prototyping» (18F, U.S. General Services Administration; CC0 1.0), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
