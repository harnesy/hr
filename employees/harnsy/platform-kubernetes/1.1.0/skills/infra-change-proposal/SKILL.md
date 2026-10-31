---
name: infra-change-proposal
description: Turn a wanted change to live infrastructure (cluster objects, nodes, networks, cloud resources, settings) into a written proposal with the current state, the change, the expected effect and the way to undo it, backed by a dry-run diff, the disruption it causes and its effect on cost, so the owner can approve it before anything is applied. Use before any apply, delete, scale, drain, cordon, restart, upgrade or configuration change on a shared or production system.
---

# Infrastructure change proposal

Live infrastructure is changed on paper first. This skill writes one change as a short, reviewable proposal: what is there now, what will be different, what should happen as a result, and how to get back. The owner reads it, approves or rejects it, and only then is it applied.

**Route:** a finding (health check, incident, request, upgrade notice) → **infra-change-proposal** → the owner approves → the change is applied in the agreed window → checked against the expected effect, or undone.
Before this skill: a reason to change something live. After it: an approved or rejected proposal, and an applied-change record.

## When to use

- Anything that would apply, delete, scale, drain, cordon, restart, upgrade or reconfigure part of a shared or production system.
- A fix suggested by a cluster health check or by a debugging session.
- A planned version upgrade of the cluster, its nodes or an add-on.
- A change to network rules, access rights, secrets handling or storage.

## Inputs

- The reason for the change and the evidence behind it.
- Read access to the live system to capture its current state.
- The desired configuration as files under version control, not as commands typed by hand.
- Who owns the system, who owns the applications running on it, and who approves changes; the agreed change windows.

## Rules

- Read-only on live systems until the owner says yes. Capturing state, diffs and dry runs are allowed; applying is not.
- Every proposal has four parts: current state → change → expected effect → undo.
- The change lives in a file that can be reviewed and diffed. A one-off command is written out in full in the proposal and treated the same way.
- Anything that cannot be undone (deleting a volume, dropping data, rotating a key that clients still use) is marked in bold and needs a backup or a tested alternative first.
- Cost effects are stated in resource units (nodes, CPU, memory, storage, traffic). Money figures come only from a cost estimate made with the cost-estimate skill.
- No promise of uptime, speed or saving. The expected effect is what the change is meant to do and how that will be checked.

## Steps

1. **State the reason** in two or three sentences and link the evidence: a health-check finding, an incident note, a request.
2. **Capture the current state, read-only:** export the live definitions of every object or setting the change touches; note versions, replica and node counts, and the health signals that matter now (errors, restarts, resource use). Save them next to the proposal.
3. **Write the change as a file** in the repository that holds the configuration. Keep the change as small as possible; split unrelated changes into separate proposals.
4. **Show the effect before applying it:** run a diff of the file against the live system, using a server-side dry run where the platform offers one, and attach the output. Say what the diff cannot show: data inside volumes, external DNS, systems outside the cluster.
5. **Describe the disruption:** what restarts, moves or gets evicted; whether the disruption budgets on affected workloads still leave enough healthy replicas; which application owners are touched; how long it should take. A node drain or upgrade is a voluntary disruption, so plan it with the application owners, not around them.
6. **State the cost effect** in resource units: more or fewer nodes, larger disks, more log volume, extra traffic between zones or regions. Ask the cloud architect for a cost estimate if the change is large.
7. **Write the undo:** the exact steps to go back, the saved copy of the previous definitions, how long it takes, who can do it, and the signal that triggers it. Mark any step that cannot be undone.
8. **Name the decision level:** the system owner decides most changes; escalate to the platform or architecture owner when the change affects a shared platform, sets a precedent for other teams, or adds notable cost or technical debt.
9. **Submit and wait.** Record who approved, when, and for which window. A rejection is recorded too, with the reason.
10. **After approval,** the change is applied by the owner, or by this role only if the owner explicitly assigns it, exactly as written and inside the window. Then compare the live state with the expected effect; if they differ, follow the undo steps and report.

## Checks before hand-over

- The proposal has current state, change, expected effect and undo, with the saved «before» definitions attached.
- A diff or dry-run output is attached, and its blind spots are named.
- Disruption, affected owners and disruption budgets are covered.
- Irreversible steps are marked and have a backup plan.
- Nothing was applied before the recorded approval.

## Artefacts

- `changes/<date>-<short-name>.md`: reason, current state, change, expected effect, disruption, cost effect, undo, approval.
- `changes/<date>-<short-name>.before/`: exported live definitions.
- `changes/<date>-<short-name>.diff`: diff or dry-run output.

## Hand-over

- **To the system owner:** the proposal for approval.
- **To devops or the SRE on call:** the approved change, the window, the checks after applying and the undo steps.
- **To application owners:** the disruption they will see and when.
- **To the database engineer:** changes that touch stateful workloads, volumes or backups.
- **To the security reviewer:** changes to access rights, network rules or secrets.
- **To the cloud architect:** changes with a notable cost effect.

## Tools

A cluster CLI with read-only credentials for capturing state and running diffs; write credentials stay with the owner unless assigned for one approved change. Examples for a Kubernetes cluster:

```sh
kubectl get deployment web -n shop -o yaml > before/deployment-web.yaml
kubectl diff -f changes/web-replicas.yaml
kubectl apply --dry-run=server -f changes/web-replicas.yaml
kubectl get poddisruptionbudgets -A
```

## Sources

Built on the Kubernetes documentation, «Declarative Management of Kubernetes Objects Using Configuration Files», «Disruptions» and «Specifying a Disruption Budget for your Application» (github.com/kubernetes/website, commit da4702f; © The Kubernetes Authors, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), changed. Built on GOV.UK «Architectural Decision Record Framework» (DSIT and GDS) and «Managing your spending in the cloud» (GDS and CDDO), Crown copyright, adapted. Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
