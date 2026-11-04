---
name: strangler-slice
description: Replace a legacy system one slice at a time behind a routing layer that sends each request to the old or the new part, compares their answers before switching, sets a switch-off date per slice and keeps routing back as the way to undo. Use when a legacy system is too large or risky to replace in one go.
---

# Strangler slice

Replacing a whole legacy system at once is a big bet. This skill puts a routing layer in front of the old system and moves one small piece of behaviour at a time to new code. Each slice is compared with the old answers before it takes real traffic, has its own switch-off date, and can be undone by routing back.

**Route:** a legacy system to replace → characterization-tests → **strangler-slice** (one slice per round) → the owner approves each switch → the old part is retired when nothing calls it.
Before this skill: an owner who wants the old system gone, and tests that pin its current behaviour. After it: one slice moved, compared and switched, with the old path still available until its switch-off date.

## When to use

- A legacy system must be replaced, but a single cut-over would be too risky.
- The old system can be reached through a boundary that a routing layer can sit in front of (an API, a set of URLs, a message queue).
- Callers need to move at different speeds.

## Inputs

- A map of the legacy system: callers, data stores, batch jobs, integrations, contracts and their end dates.
- Characterization tests or recorded answers for the behaviour to be moved.
- The owner of the old system and the owners of the main callers.

## Rules

- A routing layer sits in front; callers talk to it, not to the old system directly.
- One slice at a time. A slice is small, has a clear boundary and can be switched on its own.
- Before a slice takes real traffic, old and new answer the same requests and their answers are compared.
- Each slice has a switch-off date for its old path, agreed with stakeholders, with slack, and kept away from contract end dates.
- Rollback for a slice is routing back to the old path. The old path stays working until its switch-off date.
- Routing changes on live systems are proposals (current state → change → expected effect → undo), applied only after the owner's OK.
- The routing layer must not become a bottleneck or a single point of failure; its capacity and failover are planned.

## Steps

1. **Map what you touch:** list the parts of the legacy system the work affects and who depends on them. Compare the scale of this change with other ways to reach the same data or behaviour; sometimes a smaller route exists.
2. **Agree the plan** with the owner and stakeholders: the order of slices, a switch-off date for each, slack in the dates, and no switch near a contract end.
3. **Put the routing layer in front:** a wrapper API, a proxy or a façade that at first sends everything to the old system. Move callers onto it at their own pace. Plan its capacity, monitoring and failover.
4. **Choose the first slice:** small, low risk, with a clear boundary and good recorded answers.
5. **Plan shared data:** which side owns writes for the slice's data, how the other side reads it, and how both stay consistent while both run.
6. **Build the new slice,** with the characterization tests as its first acceptance check. A realistic prototype comes first if the approach is untested.
7. **Compare in the background:** send the same requests to old and new, return the old answer to callers, log every difference. Explain or fix each difference with the owner.
8. **Propose the switch** for that slice: current routing, new routing (a small share of traffic first, if the layer allows), expected effect, and the undo (route back). Apply after the owner's OK.
9. **Watch and widen:** compare error rates and answers after the switch; route back at the first sign of trouble.
10. **Retire the old path** on its switch-off date, once routing logs show nothing calls it any more. Record it.
11. **Repeat** for the next slice. When every caller and slice has moved, remove the routing layer if it no longer adds value.

## Checks before hand-over

- Callers reach the slice only through the routing layer.
- Old and new answers were compared, and every difference is explained.
- The switch was a proposal with undo, approved by the owner.
- The slice has a switch-off date, and the old path still works until then.
- The routing layer has capacity, monitoring and failover.

## Artefacts

- `modernisation/map.md`: the legacy map, callers, data, contract dates.
- `modernisation/plan.md`: slices in order, owners, switch-off dates.
- `modernisation/slice-<name>.md`: boundary, data plan, comparison results, switch proposal, rollback, retirement date.

## Hand-over

- **To the owner of the old system:** the plan, each switch proposal and each retirement.
- **To the software architect:** the routing layer design and the slice boundaries.
- **To devops or the Kubernetes platform engineer:** routing changes as infra-change-proposals.
- **To the database engineer:** the shared-data plan for each slice.
- **To the QA engineer:** the comparison results.
- **To caller teams:** when to move to the routing layer and when the old path goes away.

## Sources

Built on GOV.UK Service Manual «Moving away from legacy systems» (Crown copyright), adapted. Contains public sector information licensed under the Open Government Licence v3.0. Built on 18F Guides, Federal Field Guide, «Basic principles of modern software design» (github.com/18F/guides, commit debc24b; US General Services Administration, public domain in the US and CC0 1.0 elsewhere), adapted; no endorsement by GSA is implied.

The slice-by-slice replacement idea is widely known as the strangler fig pattern (Martin Fowler); described here in our own words.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
