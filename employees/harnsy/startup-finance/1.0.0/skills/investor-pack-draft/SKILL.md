---
name: investor-pack-draft
description: Draft an investor update or fundraising pack for a founder: every number traced to its source and date, projections shown only as labelled scenarios with their assumptions, gross and net retention together, ownership marked as an estimate, and a list of statements for the founder's lawyer and accountant to read. Use when a founder prepares an update or a raise. The founder decides and sends; nothing goes to investors from this skill.
---

# Investor pack draft

What a company tells investors are the company's own statements, and in many countries securities rules apply to them. This skill drafts the pack so that every claim can be traced and checked; the founder and the founder's lawyer decide what goes out. It gives no advice on how much to raise, on terms, on valuation or on investing.

**Route:** `unit-economics` + `scenario-model` + ownership estimate → **investor-pack-draft** → founder's lawyer (and accountant) read → the founder decides and sends.

## When to use

- A regular update to existing investors.
- A pack or memo for a planned raise.
- A founder asks for help with «the numbers slide».

## Inputs

- **Jurisdiction:** the company's country, the investors' countries, and who the founder's lawyer is (licensed in the company's country). Ask first.
- The latest `unit-economics` reading and `scenario-model` outputs, with their dates.
- The ownership estimate inputs, if ownership is shown (share register, instruments and their terms, side letters, planned round and option pool).
- The founder's message: what the pack is for and who reads it.

## Steps

1. **Settle the jurisdiction.** If the company raises in the US, use the dated US facts below. Anywhere else, write: «securities rules apply to investor materials in most countries; ask your lawyer», and name no rule.
2. **Collect the facts:** metrics from `unit-economics`, scenarios from `scenario-model`, and the ownership estimate. Each number keeps its source and date.
3. **Draft the sections** the founder asked for (for example: what happened, key numbers, what is next, what help is wanted). Footnote every number to its source and date.
4. **Show projections only as scenarios:** base, downside and upside, each with its assumptions and trigger event, labelled «scenario, not a forecast». A wish such as «we will reach X by year Y» is not drafted as a promise; offer the scenario page instead.
5. **Show retention honestly:** gross retention and customer churn next to net retention, wherever net appears.
6. **Ownership:** show it as an estimate until the round is priced and signed; list the cases the estimate does not handle. Standard instrument forms are used unchanged; extra rights belong in a separate side letter; both are for the lawyer.
7. **List statements for review:** every forward-looking claim, every comparison with competitors, ownership, use of funds, and any market-size figure, each with the reviewer it needs (lawyer or accountant).
8. **For a US raise, add the dated facts** (SEC pages, last reviewed 17 March 2026): every securities sale, even one that needs no registration, falls under the federal antifraud rules, and the company answers for false or misleading statements made by it or for it, spoken or written; public advertising of a private round under Rule 506(c) is allowed only when every buyer is an accredited investor and the company takes reasonable steps to check that. Questions about any of this go to the founder's lawyer.

## Checks before hand-over

- No number without a source and a date.
- No promise of growth, returns or value; no word that calls the result certain, free of risk or approved by any authority.
- Projections appear only as labelled scenarios with assumptions.
- Gross retention appears wherever net retention does.
- Ownership is marked as an estimate.
- The review list is complete, and the draft says nothing is to be sent before the lawyer has read it.

## Artefacts

- `investor-pack/<date>/draft.md`: outline and text for slides or a memo.
- `investor-pack/<date>/data-appendix.csv`: every number with its source and date.
- `investor-pack/<date>/review-list.md`: statements for the lawyer and the accountant, and open questions.

## Hand-over

- **To the founder and the founder's lawyer:** the draft, the appendix and the review list. The founder decides what is sent, to whom and when; the agent sends nothing.
- **To the accountant:** questions about historical figures.
- **To `scenario-model` or `unit-economics`:** any number that needs rebuilding.

## Sources

Source: U.S. Securities and Exchange Commission, Exempt Offerings FAQ and Rule 506(c) pages (last reviewed 17 Mar 2026); facts restated for US raises only. Ownership inputs adapted from the cap-table skill in github.com/1984vc/cap-table (MIT, © 2024 1984 Ventures); retention presentation adapted from the unit-economics skill in github.com/anthropics/financial-services-plugins (© Anthropic, PBC; Apache License 2.0), changed by harnsy; scenario labelling from the finance-fpa-analyst agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors). Further reading, ideas only: Y Combinator's Documents page on standard financing forms. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
