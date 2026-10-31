---
name: customer-onboarding-plan
description: Turn a signed deal into an onboarding plan both sides follow: a shared goal in one sentence, week-by-week steps for the customer and for us, kickoff prerequisites and deliverables, a success review after the first month, a later check-in, success measures, contacts and an issues and risk log. Use at every new signing or restart of a customer account. For new employees use onboarding-plan instead.
---

# Customer onboarding plan

The first weeks after signing decide whether a customer reaches the value they paid for. This skill takes the sales handover, agrees a shared goal with the customer, and writes a plan in which both sides have dated steps, so that «onboarded» means the agreed scope works, not that the calls ended.

**Route:** handover from the account executive (and the trial readout from the sales engineer) → **customer-onboarding-plan** → kickoff → weekly steps → success review → `account-health-review` from then on.

## When to use

- A new customer has signed.
- An existing customer restarts after a long pause, adds a new team, or changes their main contact.
- Not for new employees (that is `onboarding-plan`, a different audience) and not for trials before signing (`trial-plan`).

## Inputs

Ask the account executive for the handover; do not start without it:

- **People on both sides:** the sponsor, the main contact, daily users, the technical contact, who signs.
- **Commitments made in the sale:** anything promised, with who promised it.
- **Success criteria** from the trial or the sale, and the customer's own goals in their words.
- **Open risks and the issues log** from the trial.
- **The contract scope:** what is included, so nothing outside it is planned.

## Steps

1. **Check the handover.** Missing people, commitments or criteria go back to the account executive as questions before kickoff.
2. **Draft the shared goal** in one sentence, in the customer's terms, with a date: what will work, for whom, by when.
3. **Plan the kickoff.** Prerequisites (access granted, data connected, people invited), the agenda, and the deliverables of each session. The customer confirms the goal at kickoff.
4. **Write the weeks.** For each week: what the customer does, what we do, the owner on each side, the date. Aim for a first real result early.
5. **Set the measures.** How both sides will know the goal is reached (a report used weekly, a number of active users, a process moved over). Measures come from the customer's goals, not from a generic list.
6. **Plan the success review** after the first month: goal against measures, what is blocked, what changes. Plan a later check-in some weeks after that.
7. **Contacts and rhythm.** Who to call for what, meeting frequency, and what each side can expect from the other (response times as agreed in the contract, not new promises).
8. **Start the logs.** An issues log and a risk log travel with the account from day one.
9. **Draft messages, do not send.** The kickoff invitation and the plan go out from the account owner or the named contact person.

## Rules

- **Within the contract.** Nothing outside the contract scope is planned or promised; extra needs go to the account executive.
- **No promises about the product.** A missing feature goes to the product owner with the customer's use case; no date is given.
- **Customer data minimum.** The plan names roles and work emails only as needed; no exports, passwords or card details are copied into it.
- **Done means working.** Onboarding ends when the agreed scope works, confirmed at the success review.

## Checks before hand-over

- The shared goal has a date and the customer's words.
- Every week has steps on both sides with owners and dates.
- Kickoff prerequisites and deliverables are listed.
- Measures, the success review and the later check-in are dated.
- The issues and risk logs exist.

## Artefacts

- `customers/<account>/onboarding-plan.md`: goal, weeks, measures, review dates, contacts, expectations.
- `customers/<account>/issues-log.md` and `risk-log.md`.
- `customers/<account>/kickoff-invite-draft.md`.

## Hand-over

- **To the account owner and the customer's main contact:** the plan, as a draft for the account owner to send.
- **To the product owner:** feature gaps with the customer's use case.
- **To `account-health-review`:** the goal and measures, which become the «value delivered» dimension.

## Sources

Built on the PostHog handbook, /contents/ folder, customer onboarding, onboarding success plan and account allocation pages (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted. Built on the Customer Success Manager agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors), ideas retold. Built on the Sourcegraph handbook (archived), implementation handoff page (Apache License 2.0; Sourcegraph, Inc. and contributors). Changed by harnsy. Scope from the O*NET 31.0 Database, 41-3091.00 Sales Representatives of Services (nearest occupation). This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
