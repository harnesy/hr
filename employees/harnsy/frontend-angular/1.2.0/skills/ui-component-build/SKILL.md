---
name: ui-component-build
description: Build one user interface component from a design spec, inside the project's existing component library and design tokens; define its inputs, outputs and every state (empty, loading, error, long text, disabled, success), make it usable by keyboard and screen reader with visible focus and readable contrast, let it adapt from the narrowest width up and to user preferences such as dark mode and reduced motion, and cover it with tests. Use when a new component or a substantial change to one is needed in a web frontend.
---

# UI component build

A component is finished when it behaves well in every situation a user can reach, not only in the one shown on the mockup. This skill starts from the spec and the components that already exist, lists all the states and inputs before writing code, builds with the project's tokens and patterns, and checks keyboard use, screen reader output and narrow screens before calling it done.

**Route:** a design spec or a request from the designer → **ui-component-build** → the component with tests → browser-check at desktop and phone widths → the reviewer and the QA tester; visual questions go back to the designer.
Before this skill: a spec, or at least a description and an example of where the component is used. After it: a reviewed component with tests and a short note of its states and decisions.

## When to use

- A new component, or a change that adds states, inputs or behaviour to an existing one.
- A screen that needs a pattern the library does not have yet (first check that it really does not).

## Inputs

- The design spec: layout, sizes as tokens, states, content rules, interaction. If the spec is missing a state, ask the designer rather than invent it.
- The existing component library, design tokens, theme files and style guide of the project.
- Where the component will be used, with real examples of content (shortest and longest).

## Rules

- Reuse before building: search the library for a component that does the job or can be extended.
- Use the project's tokens and existing styles for colour, spacing, type and radius. No raw values where a token exists. Match the existing look; do not invent a new one.
- Design every state: empty, loading, error, success, disabled, and long or missing content. A state the spec does not cover is a question for the designer.
- Semantic markup first; ARIA attributes only where native elements cannot express the role or state.
- Every interactive part is reachable and usable by keyboard, has an accessible name, shows a visible focus indicator, and keeps a readable contrast in every theme.
- Build for the narrowest width first and let the content decide where the layout changes, not a list of device sizes.
- Respect user preferences: colour scheme, reduced motion, increased contrast, larger text.
- No new dependency without the owner's OK.

## Steps

1. **Read the spec and the library.** Find the closest existing component and the tokens the spec uses. Note any gap between spec and library.
2. **Write the contract:** inputs (with types and defaults), outputs or events, content slots, and the list of states. Agree it with the designer if it is not obvious from the spec.
3. **Write tests for the contract first** where the project tests components: rendering per state, input changes, events emitted, keyboard interaction (see tdd-slice).
4. **Build the structure** with semantic elements: buttons for actions, links for navigation, lists for lists, headings in order, labels tied to their fields.
5. **Style it** with the project's tokens and theming, scoped to the component so styles do not leak in or out. Use the theme's custom properties so dark mode and other themes work without extra rules.
6. **Add every state,** including loading placeholders that keep the layout stable, error messages that say what to do next, and long text that wraps or truncates the way the spec says.
7. **Make it accessible:** keyboard order and keys that match the pattern (for example arrow keys inside a menu or tab list), focus moved deliberately after actions that change the view, names and states exposed to assistive technology, motion that stops when the user asks for reduced motion.
8. **Make it responsive:** check from the narrowest width up; change layout where the content needs it; make sure nothing overflows or hides a control.
9. **Run the project's checks** (format, lint, tests) and fix what is new.
10. **Look at it in a browser** with browser-check, at both widths, with the keyboard, and compare with the spec.
11. **Write the component note** and hand over.

## Checks before hand-over

- Every state in the contract renders and is covered by a test.
- Keyboard-only use works; focus is always visible; every control has an accessible name.
- Only tokens and existing styles are used; any new token is a proposal for the designer.
- The component works at the narrowest supported width and in each theme.
- The project's format, lint and test commands pass.

## Artefacts

- The component, its tests and its styles, as one reviewable change.
- A short component note (in the library's docs or the change description): inputs, outputs, states, accessibility behaviour, open questions for the designer.
- Screenshots from browser-check.

## Hand-over

- **To the designer UI:** screenshots of every state, gaps found in the spec, any new token proposed.
- **To the reviewer:** the change, the tests and the component note.
- **To the QA tester:** the states and keyboard behaviour to test, and the places the component is used.
- **To the accessibility engineer,** when the team has one: complex widgets such as menus, dialogs and data grids.

## Per stack

- **Angular:** check the Angular version first; patterns such as signal-based inputs and outputs and the newer template control flow depend on it. Generate the component with the CLI the way the project does. Declare inputs and outputs on the component; keep templates simple and move logic into the class. Styles are scoped to the component by default through view encapsulation; style the component's own element through the host selector, and avoid turning encapsulation off. Bind ARIA attributes with attribute binding; after a route change, move focus to the main heading or content so screen reader users know where they are. Use the project's accessibility helpers (for example the Angular CDK's focus and keyboard utilities) instead of writing new ones. Component tests use the test bed, a component fixture and, for interaction, component harnesses.
- **React and Vue:** the same steps; follow the project's existing component and styling approach.
- **Plain CSS:** media queries at the widths where the content needs a change; the `prefers-color-scheme` media feature for dark mode, which also works for the browser's theme colour and inside SVG icons; theme values as custom properties, redefined per scheme, so selectors are not written twice.

## Sources

Built on agent-skills, «frontend-ui-engineering» (github.com/addyosmani/agent-skills, commit 1401c8b; © 2025 Addy Osmani, MIT licence), adapted. Built on Angular documentation, «Styling components», «Accessibility in Angular», «Angular coding style guide» and «Basics of testing components» (angular/angular, commit 97e6aa4; https://angular.dev; © Google LLC, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on the «angular-developer» skill (github.com/angular/angular, commit 97e6aa4, skills/dev-skills/angular-developer; © 2026 Google LLC, MIT licence), adapted. Built on web.dev «Learn Responsive Design»: «Media queries», «Theming» and «User interface patterns» (Google LLC, CC BY 4.0), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
