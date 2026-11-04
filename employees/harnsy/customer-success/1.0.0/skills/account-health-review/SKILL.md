---
name: account-health-review
description: Review a customer account's health from evidence: relationship, engagement trend, product use, support load, billing state and value delivered against the success plan, each with its source and date and unknowns named; written at-risk criteria, an at-risk note when one is met, and a review-meeting kit when a review is due. Use monthly per account and whenever a warning sign appears. CRM flags change only by proposal.
---

# Account health review

A health score summarises; it does not explain, and it moves late. This skill looks at each part of an account's health with dated evidence, flags risk early by written criteria, and prepares the account owner to act. It never guesses what it cannot see.

**Route:** usage data, tickets, billing state, meeting notes → **account-health-review** → at-risk note to the account owner and help from others → CRM flag changes through `crm-change-proposal` → `renewal-prep` when the end date nears.

## When to use

- Monthly for every active account.
- When a warning sign appears: usage falling, fewer active people, the main contact leaving, tickets rising, meetings missed, a failed payment or visits to the billing page.
- Before a business review meeting with the customer.
- Not for a single support ticket (the support team handles it) and not for prices or terms (the account owner).

## Inputs

- The success plan from `customer-onboarding-plan`: goal and measures.
- Product use over time (an export or read access), with its date.
- Support tickets for the period, and any escalations.
- Billing state as the billing owner shares it (paid, overdue, failed), without card details.
- Notes from calls and meetings, and the people list.
- The team's written at-risk criteria. If none exist, draft them for the owner to approve before flagging anyone.

## Steps

1. **Rate each dimension** as fine, needs attention, at risk or unknown, with the evidence and its date:
   - **Relationship:** contacts active, sponsor reachable, the main contact still there.
   - **Engagement trend:** meetings held or missed, replies, logins over time.
   - **Product use:** active users and the features tied to their goal, over time.
   - **Support load:** ticket count and severity trend, open escalations.
   - **Billing state:** as shared by the billing owner.
   - **Value delivered:** progress against the success plan's measures.
   Anything not visible is «unknown», with what would make it visible.
2. **List signals with dates.** Risk signals and opportunity signals (a new team asking for access, growing use), each with the date seen.
3. **Apply the at-risk criteria.** If one is met, write the at-risk note: what triggered it, what is known, what help is needed, what is being done and by whom.
4. **Bring help, keep the owner.** Escalation adds people (support, product, a senior sponsor); the account owner stays the owner.
5. **Billing issues are sorted, not fixed.** Classify (likely duplicate charge, real extra seats, failed payment, a missing self-service control, a product failure behind the complaint) and hand to the billing owner with invoice ids only.
6. **Prepare the review-meeting kit** when one is due: value delivered in the customer's own measures, adoption, open items and last commitments, what the next period should achieve, who should attend. The meeting is about outcomes and the next period, not a recap of features.
7. **Propose flag changes.** Any change to health fields or flags in the CRM goes through `crm-change-proposal` with the evidence.

## Rules

- **Evidence over score.** A green score with silent users is not green.
- **Unknown is an answer.** Never fill a dimension by guess.
- **No promises.** No feature, date, price, discount, credit or refund is offered to make an account healthier.
- **Customer data minimum.** Counts and trends, not personal details; no card data or exports in notes.

## Checks before hand-over

- Every dimension has a rating with evidence and a date, or «unknown» with what is missing.
- Signals carry dates.
- An at-risk note exists whenever a written criterion is met.
- Proposed CRM changes are in a proposal, not applied.

## Artefacts

- `customers/<account>/health-<date>.md`: dimensions, signals, verdict, at-risk note.
- `customers/<account>/review-kit-<date>.md`: the meeting kit, when due.

## Hand-over

- **To the account owner:** the review and any at-risk note.
- **To the support team lead:** ticket patterns behind a support-load rating.
- **To the billing owner:** classified billing issues.
- **To `crm-change-proposal`:** health flag changes.
- **To `renewal-prep`:** the latest review, when the end date is within about three months.

## Sources

Adapted from the customer-health skill in github.com/anthropics/knowledge-work-plugins, sales folder (© Anthropic, PBC; Apache License 2.0). Changed by harnsy. Built on the PostHog handbook, /contents/ folder, health tracking and risk mitigation and churn prevention pages (MIT for /contents/, © 2020-2025 PostHog Inc.), adapted. Built on the Customer Success Manager agent in github.com/msitarzewski/agency-agents (MIT, © 2025 AgentLand Contributors), ideas retold. Built on the customer-billing-ops skill in github.com/affaan-m/ECC (MIT, © 2026 Affaan Mustafa), adapted: classification and hand-over only.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
