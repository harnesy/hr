---
name: job-post
description: Turn a new opening into a written intake, job-related criteria and a job post draft the hiring manager approves. Use when a team needs to hire for a role and nothing is written yet, or when an old post must be rewritten before it is reused.
---

# Job post

The intake and the criteria are the contract for the whole hiring round. Screening, interviews and the decision all use them, so they are written before the post and before anyone applies.

**Route:** opening → **job-post** → public-sourcing (if asked) → screening-notes → interviews → the person's decision.
Before this skill: a work item from the hiring manager or the HR generalist. After it: the approved criteria go to `screening-notes`, the approved post to the person who publishes it.

## When to use

- A team wants to hire and there is no written description of the role yet.
- An old job post is about to be reused: the work has changed, or the post asks for things the work does not need.

## Inputs

Ask the hiring manager. Do not write the post without these:

- **Country** (and region) where the person will work, and the kind of contract. Hiring rules differ by country; open questions go to the HR generalist and a professional.
- **The work:** what this person will do in the first months, and what changes when they succeed.
- **Must-haves:** the few things a person cannot do the work without.
- **Nice-to-haves:** things that help but can be learned.
- **Pay band:** set by the owner. Never invent or estimate one.
- **Stages:** the interview steps planned, and who takes part in each.
- **Adjustments:** how a candidate asks for an adjustment or another way to apply, and who handles it.

## Steps

1. **Run the intake.** Ask the questions above and write the answers down as `intake.md`. Mark any answer that is a guess.
2. **Write the criteria.** Turn the must-haves into 3–6 criteria, each one something an application or interview can show. For each, write what evidence would show it. Remove anything that is not needed for the work.
3. **Test each criterion.** Ask: does the work really need this? Could someone do the work well without it? Is it a stand-in for a trait (age, sex, origin, health, family status, religion and the like)? Fixed numbers of years, a particular degree, «native speaker» and «young team» usually fail this test; rewrite them as the skill the work needs.
4. **Write the post.** Order: what the team does; what the person will work on and the outcomes expected; must-haves (short); nice-to-haves (labelled as such); pay band from the owner; how the process runs (stages, rough timing); how to ask for an adjustment; if an AI tool helps in the process, a plain sentence saying so (wording from the owner).
5. **Read it for exclusion.** Look for words that state or imply a preference for or against a group, gendered job titles, physical demands the job does not have, and requirements that would put off qualified people. Fix them and list what you changed.
6. **Send for approval.** The hiring manager approves the criteria and the post. Record the approved version and date. A later change to the criteria during the round needs a new approval and applies to every candidate.

## Checks before hand-over

- Every criterion is job-related and has its evidence written next to it.
- No protected trait, and no stand-in for one, is in the criteria or the post.
- The pay band came from the owner, word for word.
- The post says how to ask for an adjustment.
- The criteria are approved and dated before the first application is read.

## Artefacts

- `intake.md`: the intake answers, with guesses marked.
- `criteria.md`: approved criteria, each with the evidence that shows it; version and approval date.
- `job-post.md`: the post draft, with a list of wording changes made in step 5.

## Hand-over

- **To the hiring manager:** the post and criteria for approval. The person publishes the post; the agent never does.
- **To the interview designer:** the approved criteria, so interview questions and scoring guides match them.
- **To the recruiter's `screening-notes`:** the approved criteria.
- **To the HR generalist:** any open question about the rules of the country.

## Sources

Built on the PostHog handbook people pages (MIT, © 2020-2025 PostHog Inc.), the Sourcegraph handbook talent pages (Apache License 2.0, © 2021 Felix Frederick Becker), «Structured Interviews: A Practical Guide» (U.S. OPM, 2008, US government work; method only) and GOV.UK «Employers: preventing discrimination» (UK). Contains public sector information licensed under the Open Government Licence v3.0. All adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
