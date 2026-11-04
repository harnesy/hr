---
name: renewal-prep
description: Prepare a contract renewal for the account owner about three months before the end date: confirm the current contact, pull contract dates, usage with its assumptions, escalations, people changes and classified billing issues, label the renewal fine, watch or in danger with the signals behind it, and list record fixes as proposals. Use for every renewal in the coming quarter. Never proposes a price, discount, credit or refund.
---

# Renewal preparation

A renewal should never surprise anyone. This skill builds a renewal calendar, prepares each renewal early with an honest picture of use and risk, and hands the account owner a brief to decide from. Renewal is not the moment to push for more; growth comes from use, after the customer has reached the agreed value.

**Route:** renewal calendar and `account-health-review` → **renewal-prep** → brief to the account owner → the owner talks to the customer and decides terms → record fixes through `crm-change-proposal`.

## When to use

- Monthly, for every renewal whose end date falls in the next three months or so.
- When a renewal is already in danger earlier than that.
- Not for pricing or negotiation: those belong to the account owner.

## Inputs

- Contract dates and scope (start, end, notice period) from the contract or the CRM, with the date read.
- The latest health review and the success plan.
- Product use over the contract period, with how it was measured.
- Open escalations and tickets.
- People changes at the customer (main contact, sponsor, signer).
- Billing issues as shared by the billing owner, without card details.

## Steps

1. **Build the calendar.** Every renewal in the window with its end date and notice date. Record hygiene goes in a separate list: renewals with no record, missing amounts, end dates that do not match the contract.
2. **Confirm the contact.** The person who signed last time may have moved; find who decides now, from the people list and recent meetings.
3. **Pull the facts.** Usage history with its assumptions (what counts as active, which period), open escalations, people changes, open commitments from both sides, billing issues classified (likely duplicate charge, real extra seats, failed payment, missing self-service, product failure).
4. **Label the renewal:**
   - **fine**: steady or growing use, contacts active, no open escalation;
   - **watch**: one risk signal, or important facts unknown;
   - **in danger**: several risk signals, or the main contact or signer gone with no replacement.
   List the signals behind the label, risk and reassuring alike (active talks about new teams, a multi-year history).
5. **Estimate the need honestly.** From real use and the customer's plans: the same scope, less, or more. If use is below the contract, say so; the owner decides what to do with that.
6. **Write the brief** for the account owner: dates, label with signals, usage with assumptions, open commitments, risks, the need estimate, and questions to ask the customer.
7. **When nobody answers:** a dated sequence of contact attempts for the owner (main contact, then sponsor, then signer) and a note on the notice date.
8. **Record fixes** go through `crm-change-proposal`.

## Rules

- **No money talk from the agent.** No price, discount, credit, refund or penalty is proposed to the customer. The brief may list options for the owner; the owner decides.
- **No pressure.** Nothing in a draft message threatens the customer with losing a discount or a deadline that is not in the contract.
- **No roadmap promises** to secure a renewal.
- **Expansion only after value.** Growth is noted for the owner only when the customer has reached the agreed value.

## Checks before hand-over

- Every renewal in the window has a label with its signals.
- Usage numbers state what was counted and over which period.
- The current decision maker is named or marked unknown.
- No draft for the customer contains a price, discount, credit or refund.
- Record problems are in a proposal, not fixed.

## Artefacts

- `customers/renewals-<quarter>.md`: the calendar and hygiene list.
- `customers/<account>/renewal-brief-<date>.md`: the brief.

## Hand-over

- **To the account owner:** the brief; the owner leads the renewal conversation and decides terms.
- **To the billing owner:** classified billing issues.
- **To the revenue operations specialist through `crm-change-proposal`:** record fixes.

## Sources

Adapted from the renewal-radar skill in github.com/anthropics/knowledge-work-plugins, sales folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Built on the PostHog handbook, /contents/ folder, renewals page (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted; its discount-pressure step left out. Built on the Customer Success Manager agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors), ideas retold. Built on the customer-billing-ops skill in github.com/affaan-m/ECC (MIT, © 2026 Affaan Mustafa), adapted: classification and hand-over only.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
