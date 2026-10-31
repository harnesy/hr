---
name: state-matrix
description: Build a grid of every component on a screen against every state it needs - hover, focus, active, disabled with a reason, loading, empty, error, dark theme, long text, narrow screen - trigger each state, and mark it present, missing or broken with a screenshot; accessibility-looking rows are flagged for the accessibility engineer, not judged. Review only. Use on any new or changed component or screen, especially when the mockup shows only the happy state.
---

# State matrix

Mockups usually show one moment: the list full of tidy data, the form filled in correctly. Users meet the other moments too: the empty list, the slow network, the error, the name that is twice as long as expected, the phone held upright, the dark theme. This skill lists every component on the screen against every state it needs, makes each state happen, and records whether it exists and looks right.

**Route:** the component list of a screen → **state-matrix** (screenshots from `browser-check`) → missing states to the frontend developer, undefined states to the ui designer.

## When to use

- On any new or changed component or screen.
- When the mockup shows only the happy state.
- Not as an accessibility audit: rows that touch accessibility are flagged and handed over.

## Inputs

- The screen as a local build or preview, and its component list.
- The spec, including any states it defines.
- Test data or a test account that can produce empty, error and long-text cases.

## Steps

1. **List the components** on the screen that people interact with or that show data: buttons, inputs, lists, tables, cards, menus, dialogs, messages.
2. **Set the states** for each, from this list where they apply: resting, hover, focus, active (pressed), disabled with a reason shown, loading, empty, error, success, dark theme, long text or translation, narrow screen (390 px wide).
3. **Trigger each state:** test data for empty and long text (a name of 120 characters, a number with many digits), a throttled network or a stopped test server for loading and error, the keyboard for focus, the dark colour scheme option of `browser-check` for dark theme, the 390 px capture for narrow screens.
4. **Mark each cell** present, missing, broken or not needed, with a screenshot for present and broken cells and a one-line note for broken ones (what is wrong, value found, value expected).
5. **Check the rules the system sets:** a control looks usable and changes visibly between resting, hover and pressed; focus is visible on every background; an unavailable action says why and how to make it available; inputs show focus clearly.
6. **Flag accessibility-looking rows** for the accessibility engineer, without a verdict: focus hidden behind a sticky bar, content that needs sideways scrolling at narrow width, text that breaks with larger spacing or zoom, targets that are small or close together, boundaries hard to tell from the background.
7. **Split the gaps:** a state the spec defines but the build lacks goes to the frontend; a state the spec never defined goes to the designer as a question.

## Rules

- **Every cell has a mark.** An unchecked state is written «not checked», with the reason.
- **Evidence for every present or broken cell:** a screenshot and the width and theme it shows.
- **Review, never change.** No code, style or test data in a shared environment is changed.
- **No accessibility verdict.** Flagged rows are checks for the accessibility engineer, never «passes» or «fails».

## Checks before hand-over

- Every component has every relevant state marked.
- Present and broken cells have screenshots; broken cells have a note with values.
- Spec gaps are split from build gaps.
- Accessibility-looking rows are flagged and listed for hand-over.

## Artefacts

- `polish/<screen>-states.md`: the grid (components × states), the notes, and links to screenshots.

## Hand-over

- **To the frontend developer:** missing and broken states.
- **To the ui designer:** states the spec does not define.
- **To the accessibility engineer:** the flagged rows with their evidence.
- **To the QA engineer:** the states that could not be triggered locally.

## Sources

Built on the U.S. Web Design System, button guidance and state tokens (designsystem.digital.gov; GSA Technology Transformation Services; CC0 1.0), adapted: distinct resting, hover and active states, a visible focus state, an unavailable action that explains why, state colour families. Built on the GOV.UK Design System, «Focus states» (Government Digital Service, Crown copyright), adapted: focus visible against every background, a clearer border on focused inputs, changed components reuse the system's focus values. Built on the GOV.UK Service Manual, «Designing for different browsers and devices» and «Making sure your service works well on mobile» (Crown copyright), adapted: screen sizes and browsers people actually use. Contains public sector information licensed under the Open Government Licence v3.0. The design system's source repository is under the MIT licence, Copyright (c) 2017 Crown Copyright (Government Digital Service).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
