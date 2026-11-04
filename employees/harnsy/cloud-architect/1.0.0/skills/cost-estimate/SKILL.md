---
name: cost-estimate
description: Estimate what a cloud setup or an option would cost to run, from listed usage assumptions and prices read from the provider's official price list or price API (with date, region, SKU, currency and link), plus the work to run it; show what drives the cost and which levers exist, without promising a bill or a saving. Use when comparing designs, before a large infrastructure change, or when spending needs explaining.
---

# Cost estimate

A cost estimate is only as good as its assumptions and its price sources. This skill lists what will be used, finds each unit price in the provider's own price list, multiplies, adds the cost of running the thing, and says plainly what could move the result. It never promises a bill or a saving.

**Route:** a design, an option or a current bill → **cost-estimate** → an estimate with assumptions and sources → the owner or architect uses it in a decision.
Before this skill: what is to be run, where and for how long. After it: a dated estimate; decisions belong to the owner.

## When to use

- Comparing options in design-it-twice.
- Before an infrastructure change that adds or removes noticeable capacity.
- When a bill rose and someone needs to know what drives it.
- When planning a budget for a new service.

## Inputs

- The components: compute, storage, databases, networking, logging and monitoring, managed services.
- Usage assumptions: running hours, request or transaction volumes, data stored and its growth, data moved out or between regions, number of environments.
- Region or country where it must run, and any data-location rule.
- Read access to the current bill or usage reports, if the estimate is about something that already runs.

## Rules

- This skill text carries no prices. In a live answer, every price is a fact read from the provider's official price list or price API, shown with the read date, region, SKU or meter name, currency and URL, and labelled «list price on <date>, before discounts and tax; your bill may differ».
- Never copy a price page; quote only the figures used.
- Every estimate lists its assumptions next to the result. A figure without its assumption is not shown.
- Never promise a bill, a saving or a percentage reduction. Levers are options with their risks, not commitments.
- Contract prices, discounts or credits are used only when the owner provides them, and are marked as such.
- Read-only on billing and cloud accounts.

## Steps

1. **List the components** and for each the billing unit: time running, requests or transactions, stored volume, data moved.
2. **Write the usage assumptions** per component, with where each number came from (current metrics, the product manager's forecast, a load-test result) and a low and high case.
3. **Name the cost drivers** that are easy to miss: log and metric storage and retention, the database type, encryption and key management, backups, data leaving the cloud or crossing regions, the chosen region itself, idle non-production environments.
4. **Read the prices** from the provider's official price list or price API for the stated region and currency. Record date, SKU or meter, unit, currency and URL for each.
5. **Pick the purchase model** per component and say why: pay-as-you-go (flexible), spare or interruptible capacity (cheaper, can be taken away at short notice, only for work that tolerates it), or a commitment or up-front purchase (cheaper per unit, less flexible, a risk if usage falls).
6. **Calculate** in a table: quantity × unit price = line cost, for the low and the high case.
7. **Add the cost of running it:** hours of patching, monitoring, scaling, upgrades and on-call, and indirect costs such as the effect of an outage or of data loss. Use hours where money figures are not available.
8. **Show sensitivity:** which two or three assumptions move the total most, and what happens if each is off by a lot.
9. **List levers** as options, each with its risk: right-size over-provisioned resources, scale with demand, switch off non-production outside working hours, remove idle resources, move rarely read data to cheaper storage tiers, change the purchase model.
10. **Propose controls:** tags or labels so each cost has an owner, and spend alerts at agreed levels. Applying them is an infra-change-proposal.

## Checks before hand-over

- Every price has date, region, SKU, currency, URL and the «list price» label.
- Assumptions sit next to the figures, with low and high cases.
- Running effort and indirect costs are included, not only list prices.
- No promised bill or saving appears anywhere.
- The estimate says what it does not cover.

## Artefacts

- `cost/<topic>-<date>.md`: components, assumptions, price sources, calculation table, running effort, sensitivity, levers.
- `cost/<topic>-<date>.csv`: the calculation table, if the owner wants a spreadsheet.

## Hand-over

- **To the owner or budget holder:** the estimate and its assumptions.
- **To the cloud architect or software architect:** figures for the options paper or decision record.
- **To devops or the Kubernetes platform engineer:** proposed tags, alerts and right-sizing, as change proposals.
- **To the product manager:** the usage assumptions to confirm.

## Tools

The provider's official price calculator, price list files or retail price API (read-only, no account needed for list prices), and read-only access to the billing export or usage reports. A spreadsheet or a short script to multiply quantities by unit prices.

## Sources

Built on GOV.UK «Managing your spending in the cloud» (GDS and CDDO, Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on the Google Cloud Well-Architected Framework, cost optimization pillar and «Align cloud spending with business value» (Google LLC, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
