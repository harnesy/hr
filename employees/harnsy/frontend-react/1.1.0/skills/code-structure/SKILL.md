---
name: code-structure
description: Keep a codebase in small, findable pieces with one home for shared code. Use before the first change in a repository (a baseline structure scan, and a five-line plan when the change adds a module, a public interface or a dependency) and again before hand-over (the scan delta goes into the hand-over note). For any employee who writes code; the UI section covers web frontends, mobile apps and shop or site themes.
---

# Code structure

Code gets hard to change one small step at a time: a file grows by twenty lines, a helper is written again because nobody searched, a new screen copies the dialog of the last one. This skill makes those steps visible. Every rule below is a number that asks for a split or a one-line reason, a search the agent shows, or an artefact in the hand-over. A scan script measures the numbers so that the hand-over can show the structure did not get worse.

**Route:** before the first change: baseline scan, and a plan of at most five lines when A1 applies. While working: the rules below. Before hand-over: a second scan compared with the baseline, and the delta in the hand-over note.

## When to use

- Starting work in a repository that is new to you, or coming back to one after months away.
- Any change that adds a file, folder, module, component, public interface or dependency.
- Before handing over any change that touched code.

## Inputs

- The repository at the branch the work starts from, and the task.
- The project's written rules (readme, contributing guide, architecture notes) and its configured lints.
- Python 3.11 or newer for `scripts/structure_scan.py` (standard library only, no network, read-only).

## How to read the numbers

- **The project's written rules and its configured lints win** over every number here. Where the project already chose a layout (for example folders by kind), follow it and say so in the hand-over.
- **Trigger:** past the number, split, or give a one-line reason in the hand-over.
- **HARD:** do not make the number worse without an OK from the software architect, or the lead/owner when the team has none.
- Lines are non-blank lines. Tests and generated files are not counted. Only programming-language files are measured; configuration, SQL and data files are not.

## Steps

1. **Read the project's rules** on layout, size and shared code, and its lint settings.
2. **Baseline:** `python3 scripts/structure_scan.py <repo> --json baseline.json`. Keep the baseline outside the change (a temporary folder) unless the project keeps one in the repository.
3. **Plan, when A1 applies:** at most five lines on the work item before the first commit.
4. **Search before writing** a helper or a UI element (A6, C1). Keep the commands and their hits.
5. **Work by the rules below.** A HARD limit you cannot meet, or anything listed in E, stops the work until the OK is given.
6. **Compare:** `python3 scripts/structure_scan.py <repo> --compare baseline.json`, with the same flags as the baseline. Fix what got worse, or write the reason.
7. **Hand over** with the artefacts below.

## Common rules (A)

- **A1 Plan first** when the change adds a module, package or top-level folder; adds or changes a public interface (exported API, route group, event, schema, CLI command); touches three or more modules; adds a dependency; or takes more than about a day. The plan: modules touched, new interfaces, where the code will live, and one alternative that was considered and dropped.
- **A2 Files:** over 300 lines is a trigger. A brand-new file over 500 needs the OK named under HARD. Over 800 is HARD: such a file does not grow. Go packages often keep larger cohesive files; the reason path covers them.
- **A3 Functions:** over 50 lines or nested deeper than three levels is a trigger. Over 100 is HARD: a new function stays at or under 100; an existing one over 100 does not grow without the OK named under HARD, and its split is a follow-up item (F). For the trigger, judge the whole function the change touches, not only the added lines; a few added lines can be what tips it. One function per action beats one switch that handles every action.
- **A4 Folders:** a folder with 20 or more non-test source files takes no new file; open a sub-module. A homogeneous set (plugins, migrations, generated code) is an exception named in the hand-over.
- **A5 By feature:** group code by feature (billing, tasks), not by kind (handlers, models), unless the project chose kind. The plan names the feature folder. No module or layer added for a guessed future need.
- **A6 One home for shared code** (a shared or platform folder the project names). Before writing a helper, search for one and put the command and its hits in the hand-over. Code used by three or more modules moves to the shared home.
- **A7 Third copy:** the third copy of a block (ten or more similar lines) or of a UI element is extracted now or becomes a follow-up item. The scan misses copies shorter than ten lines, so this rule rests on the search of A6 and C1: show the command and its hits.
- **A8 State and size of types:** no mutable global or package-level state outside the start-up wiring; pass dependencies in. A type with more than 40 methods is split by feature behind small interfaces.
- **A9 Structure tests survive moves:** a test that checks every module finds them from the repository root through the language's loader or a glob, never through fixed file names or one folder.
- **A10 Scan delta in the hand-over:** files over A2, longest functions, folders over A4, new near-duplicate names. No metric gets worse without a stated reason.

## Backend (B)

- **B1 Thin edges:** a handler, CLI command or job parses input, makes one call into the domain and responds. More than about 30 lines of logic there moves down.
- **B2** Each feature registers its own routes; one entry file lists the features.
- **B3** Storage sits behind a boundary owned by each feature, sized to its callers; no single store that every feature calls. An interface appears when a second implementation or a real test boundary needs it, not by reflex.
- **B4** Expose the smallest surface callers need; a small interface over a lot of hidden work is the goal. Never import another module's internals. A new dependency edge between modules, or a cycle, goes to E.
- **B5** Platform-specific code lives in one module behind an interface.

## UI section (C): web frontends, mobile apps, themes

Mobile screens, views and their state follow C1-C7 in full. **Themes (shop and site themes, for example Shopify or WordPress):** C1, C2 (shared snippets, blocks, template parts), the C3 sizes and C5 (theme settings and CSS variables as tokens) apply; a catalog page and render tests are only proposed as a follow-up item, never set up unasked.

- **C1 Search the library first** and list the reused components in the hand-over. Extend a component (a prop, slot or variant) before copying it. Show the search, for example `grep -rn "clipboard.writeText" src/` before writing a copy button.
- **C2 Shared UI on the second copy:** no shared library yet and a second similar element appears (dialog, menu, tabs, segmented control, empty state, copy button, toast, search box): create a shared UI folder with all states of the element, and a catalog page where each state can be seen outside the app (Storybook, for example, or the project's own demo route). Shared building blocks hold markup and other building blocks, never app state. The scan cannot see small inline copies, so this rule rests on the search of C1: show the command and its hits.
- **C3 Component size:** over 200 lines (styles not counted) is a trigger. Over 600 is HARD: a new component stays at or under 600; an existing one over 600 does not grow without the OK named under HARD, and its split is a follow-up item (F). More than five boolean props, or more than ten props: use variants or composition (children, slots) instead of flags. A component cares about one thing.
- **C4 Logic out of components:** fetching, polling (paused while the tab is hidden), Escape, outside-click and focus-trap handling, timers, validation and data shaping go into shared hooks, composables or services. Each one does one concrete job.
- **C5 Tokens** for colour, spacing, type, radius and shadow. A raw value where a token exists is a defect; a missing token is a proposal to the designer, not an invented value.
- **C6 Folders by feature or screen.** A4 applies to the source root too. One component per file; a child that only makes sense inside one parent is named after it.
- **C7 Render test per state** for every shared component, where the project tests components; where it does not, say so and propose one follow-up item.

## Per-stack idioms (D)

Lint names are facts, defaults as of October 2026. Turning a lint on at the numbers above is a proposal to the project, never a silent config change.

- **Go:** a package per feature under `internal/`; `main` only wires; small interfaces declared by the consumer; no `init` ordering tricks. golangci-lint `funlen`, `gocognit`.
- **Python:** a package per feature; explicit exports in `__init__`, no logic there; module-level names are constants. ruff `PLR0915`, `C901`.
- **TypeScript / Node:** a feature folder with one index export file; no deep imports into other features; loose types only at I/O edges. ESLint `max-lines`, `max-lines-per-function` (defaults 300 and 50).
- **Java / Kotlin:** package by feature, package-private by default; folders mirror packages. Checkstyle `MethodLength`, `FileLength`; detekt `LongMethod`, `LargeClass`.
- **.NET:** a folder or project per feature; `internal` by default; dependency registration per feature. CA1502, CA1506.
- **PHP:** a PSR-4 namespace per feature; thin controllers; no static service locators. PHPMD `ExcessiveMethodLength`, `ExcessiveClassLength`.
- **Ruby:** logic in service or plain Ruby objects, not in models or controllers. RuboCop `Metrics/MethodLength`, `Metrics/ClassLength`.
- **Rust:** a module per feature; private or `pub(crate)` by default; a separate crate when ownership asks for it. clippy `too_many_lines`.
- **C / C++:** one header per component; internal headers not installed; no globals across translation units. clang-tidy `readability-function-size`.
- **Mobile:** feature modules; thin screens, state in a view model or store; a design-system module (C2). detekt; SwiftLint `function_body_length`, `file_length`, `type_body_length`.
- **React:** hooks hold logic; composition through children before boolean flags. **Vue:** single-file components plus composables, props down and events up, no mixins. **Angular:** standalone pieces per feature, services for logic, a shared UI folder.

## When to call the software architect (E)

Call the software architect, or the lead/owner when the team has none, **before writing code** for: a new module or top-level folder; a new or changed public interface; a new edge between modules or a cycle; moving or splitting a module; a new runtime dependency or storage choice; a HARD limit the change cannot meet.

What comes back: a decision record (the problem, two real options, the choice, its consequences), the target layout, and the migration as separate items that each keep behaviour unchanged.

## New project vs existing repository (F)

- **New project, on the first day:** write the layout (modules, the shared home, the entry point) in the readme or an architecture note; the first feature gets its own module; the shared UI folder and catalog page come with the first screen; propose the size lints at the A2, A3 and C3 numbers; keep a scan baseline. For a minimum viable product the list shrinks to the layout note, the lints and the baseline; the shared UI folder appears at the second similar element (C2), and a missing catalog page is written down as a shortcut with its risk and a follow-up item.
- **Existing large repository: a ratchet, not a clean-up.** Take the baseline; every change keeps each metric at or below it: no new file over the limit, no growth of a file over 800, no new file in a folder of 20 or more. Tidy only the code the change touches. Larger splits become follow-up items, each landing on its own and keeping behaviour unchanged. First make the safety net move-proof (A9, UI tests in CI). Never a silent big refactor, and no structural tidying mixed into a feature or a fix.

## The scan (G)

`scripts/structure_scan.py` ranks a repository by size. Commands:

- `python3 scripts/structure_scan.py <repo> --json baseline.json` writes the baseline and prints the Markdown report.
- `python3 scripts/structure_scan.py <repo> --compare baseline.json` adds the delta; rows that got worse are marked, and so are a function, component or file over its HARD limit that grew and a new file over 500 (`--new-file-hard`), which needs the OK. It always exits 0 unless `--fail-on-worse` is given.
- `--exclude GLOB` (repeatable) leaves out paths, file names or folders, for example generated clients or data shipped as code. Name each exclusion in the hand-over.
- `--dupes` adds repeated blocks of ten lines across files.
- `--include-tests` counts test files as source, for work where the tests are the product.
- `--include-data` scans the data folders skipped by default (locales, i18n, lang, translations, fixtures, testdata); the report's Skipped line always shows how many files each held. A locales, i18n, lang or translations folder that holds a function is scanned as code, and the Skipped line names it.

What it measures: lines per file; non-test source files per folder; function length and nesting per language (Go: from `func` at column 0 to the closing brace at column 0; Python and Ruby: from `def` to the next line at the same or lower indent; brace languages: from the signature to the matching brace after strings and comments are removed; Vue and Svelte: template and script, styles left out); methods per type; UI component size; near-duplicate file names (the same name after common abbreviations such as Btn and Button, or one letter apart for names under ten letters, two for longer ones); optionally repeated ten-line blocks. It skips vendored code, installed packages, build output, lockfiles, minified files and files marked as generated.

What it does **not** claim: correctness, true complexity, true duplicates, coupling or design quality. Its numbers are heuristic, about ±10%. Name and block matches are hints that rank where to look, never a verdict; people decide. **Inline copies shorter than the ten-line window are not found:** a three-line copy-to-clipboard handler repeated in many components shows nowhere in the report. Search for them by hand, for example `grep -rn "clipboard.writeText" src/` or the API call the copies share, and show the command and its hits (C1, A6).

## Checks before hand-over

- The baseline and the final scan used the same flags; every exclusion is named.
- No metric got worse, or each worse row has a one-line reason.
- No HARD limit got worse without the OK, and the OK is quoted with who gave it.
- The plan exists when A1 applies, and is dated before the first commit.
- Each new helper or UI element comes with the search that preceded it.
- Larger structural work found on the way is filed as follow-up items, not done silently.

## Artefacts

- The scan delta table from `--compare`, with a reason next to each worse row.
- The plan of at most five lines, when A1 applies.
- The search commands with their hits, and the list of reused components (C1).
- Follow-up items: what grew, what to split next, the missing catalog page or tests.

## Hand-over

- **To the reviewer or the requester:** the change with the artefacts above.
- **To the software architect, or the lead/owner when the team has none:** the E cases and any HARD limit that the change could not meet, before the code is written.
- **To the designer:** proposals for new tokens (C5).

## Sources

No endorsement by these projects or their authors is implied.

Built on «Google Engineering Practices Documentation», review guides (github.com/google/eng-practices, commit 3bb3ec2; © Google, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), adapted. Built on «Google Style Guides»: Go best practices and decisions, Python and C++ guides on function length (github.com/google/styleguide, commit f43b95b; © Google, CC BY 3.0, https://creativecommons.org/licenses/by/3.0/), adapted. Built on React documentation, «Thinking in React», «Reusing Logic with Custom Hooks», «Passing Props to a Component» (github.com/reactjs/react.dev, commit 046f17d; © Meta Platforms, Inc., CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted. Built on Vue documentation, style guide and «Composables» (github.com/vuejs/docs, commit 40aa88a; © Yuxi (Evan) You and Vue documentation contributors, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/; no images), adapted. Built on Angular documentation, «Style guide» (angular/angular, commit 97e6aa4, adev/src/content/best-practices/style-guide.md; https://angular.dev/style-guide; © Google LLC, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Facts only (no text taken): «Effective Go» and «Organizing a Go module» (go.dev; The Go Authors, CC BY 4.0); PEP 8 (its authors, public domain); Rust API Guidelines and the Rust documentation on modules (The Rust Project Developers, MIT or Apache-2.0); Kotlin coding conventions (JetBrains, Apache-2.0); .NET code analysis rules CA1502 and CA1506 (Microsoft, CC BY 4.0). Lint and rule names and defaults of golangci-lint, ruff, ESLint, Checkstyle, detekt, PHPMD, RuboCop, clippy, clang-tidy and SwiftLint are facts as of October 2026. Ideas only (no text taken): Go Code Review Comments (Go Wiki); Storybook documentation, «Why Storybook?» and «How to write stories» (Storybook, MIT), named only as an example of a catalog page. General software-design practice from published books, described in our own words.

Text © 2026 Pavel Buchnev (harnsy), licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), except passages adapted from the CC BY 3.0 sources above, which stay under CC BY 3.0. Scripts in scripts/ are under the MIT licence (see LICENSE). The names «harnsy» and «hr.harnsy.dev» are not covered by these licences.
