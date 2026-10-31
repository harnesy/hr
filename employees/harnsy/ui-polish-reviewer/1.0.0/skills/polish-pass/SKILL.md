---
name: polish-pass
description: Compare a built screen with its spec element by element - spacing, alignment, type size, weight and line height, colour, radius, shadow, icon size - and write every finding with a screenshot crop, the element, the value found, the value expected, the design token and the fix, ranked by how visible it is to users; the spec's own gaps listed apart. Review only, no code changes. Use when a screen or component is built and before it is called done.
---

# Polish pass

A screen can pass its tests and still look unfinished: a gap of 12 pixels where the spec says 16, a heading one step too small, a colour picked by eye instead of from the palette. Each difference is small; together they make a product look careless. This skill measures the built screen against the spec and writes exact findings the frontend can fix in one pass, each with the number found and the number expected.

**Route:** a built screen, its spec and the token list → `browser-check` for screenshots → **polish-pass** → fixes by the frontend developer → a second pass on the changed findings.

## When to use

- When a screen or a component is built and before it is called done.
- After a redesign, a token change or a new theme.
- Not for usability against heuristics (the UX auditor) and not as an accessibility audit (the accessibility engineer).

## Inputs

- The built interface, as a local build or preview that can be run; never a live site.
- The spec or mockup with its measurements, and the agreed widths.
- The product's token list: colours, spacing, type scale, line heights, radii, shadows.

## Steps

1. **Capture the screens** with `browser-check` at the agreed widths, in the states the spec shows. Note the commit.
2. **Form your own view** against the spec before reading notes from the build's author.
3. **Compare element by element,** top to bottom: spacing between and inside elements, alignment to the grid, type (family, size, weight, line height), line length, colour, radius, shadow, icon size, image crops.
4. **Measure, do not estimate:** read the computed values from the browser's developer tools or the screenshot at known scale.
5. **Write one finding per difference:**
   - **where** — screen, width, element;
   - **found** — the value measured;
   - **expected** — the value in the spec and the token it belongs to (for example spacing token 2, 16 px);
   - **fix** — the exact change, naming the token to use instead of a raw number;
   - **evidence** — the screenshot crop.
6. **Check against the system's rules:** spacing in multiples of the base unit, line heights in the scale's steps, type sizes from the scale. A value outside the token set is a finding even where the spec is silent.
7. **Keep spec gaps apart:** where the spec gives no value or contradicts itself, write a question for the designer instead of a finding against the build.
8. **Rank the findings:** first those above the fold and on components used on many screens, then repeated small ones, then one-off details.

## Rules

- **Two values or no finding.** Every finding has the value found and the value expected.
- **Tokens over numbers.** Where a token exists, the fix names it.
- **Review, never change.** Nothing in the code, styles or tokens is changed by this skill.
- **About the screen, never the person** who built it.
- **Not an accessibility audit.** Low contrast, small targets or missing focus seen on the way are passed to the accessibility engineer as checks, without a verdict.

## Checks before hand-over

- Every finding has where, found, expected, fix and a screenshot crop.
- Tokens are named wherever they exist.
- Spec gaps are listed separately as questions.
- Findings are ranked and the commit, widths and browsers are named.

## Artefacts

- `polish/<screen>-<date>.md`: the findings table, the spec questions, and the screenshots it links to.

## Hand-over

- **To the frontend developer:** the ranked findings.
- **To the ui designer:** the spec gaps and contradictions.
- **To the design system keeper:** values that are needed but have no token.
- **To the accessibility engineer:** anything that looks like an accessibility problem, with the evidence.

## Sources

Built on the U.S. Web Design System, design tokens, spacing units, typesetting and state tokens (designsystem.digital.gov; GSA Technology Transformation Services; CC0 1.0), adapted: a small fixed set of allowed values for colour, spacing, type and line length, spacing in multiples of 8 px. Built on the GOV.UK Design System, «Spacing», «Layout» and «Type scale» (Government Digital Service, Crown copyright), adapted: spacing scales, line heights in fixed steps, readable line length, new styles aligned with the existing scale. Contains public sector information licensed under the Open Government Licence v3.0. The source repository is under the MIT licence, Copyright (c) 2017 Crown Copyright (Government Digital Service).

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
