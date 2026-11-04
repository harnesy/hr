---
name: cluster-health-check
description: Look at a running container cluster strictly read-only (list, describe, logs, events, resource use) and report what is unhealthy, with evidence, likely cause and a suggested fix written as a change proposal. Use on a schedule, after an alert, before and after a planned change, or when workloads are pending, restarting or not ready.
---

# Cluster health check

A health check only looks. It lists nodes and workloads, reads their conditions, events and logs, compares resource requests with what the nodes can give, and writes down what is wrong and why it is probably wrong. Every fix it suggests leaves as a separate change proposal for the owner.

**Route:** a schedule, an alert or a planned change → **cluster-health-check** → a findings report → each fix as an infra-change-proposal → the owner decides.
Before this skill: read-only access to the cluster and a list of what normally runs there. After it: a dated report; fixes belong to the change proposals.

## When to use

- On a regular schedule, so slow problems are seen before they turn into outages.
- After an alert, to find which part is unhealthy.
- Just before and just after a planned change, to compare the two states.
- When workloads stay pending, keep restarting, or never become ready.

## Inputs

- Read-only credentials for the cluster (list, describe, logs, events, resource metrics).
- What should be running: namespaces, workloads, expected replica counts, owners.
- Earlier reports, if any, to compare against.

## Rules

- Strictly read-only. Allowed: get or list, describe, logs, events, top. Never apply, delete, edit, patch, drain, cordon, scale, restart, exec into a container or port-forward to production data.
- Any action that would change the cluster becomes an infra-change-proposal: current state → change → expected effect → undo, applied only after the owner's OK.
- Where a metric source is missing, the report says «not measured» instead of guessing.
- Logs are quoted briefly and with secrets, tokens and personal data removed.

## Steps

1. **Confirm access is read-only** and note the cluster, the time and the credentials' scope at the top of the report.
2. **Nodes:** list them and check each one is ready. For any node that is not, describe it and read its conditions (memory, disk or process-count pressure, network not available) and its recent events. Note nodes that are cordoned or have unusual taints.
3. **Control plane and system add-ons:** check that the API answers, that system components (DNS, networking, storage drivers, metrics) are running, and read their recent logs if something looks off.
4. **Workloads:** list pods that are not running or not ready across all namespaces. For each group:
   - pending → describe it and read the scheduling events: not enough CPU or memory, no node matching its selectors or tolerations, a volume that cannot attach;
   - restarting or crash-looping → read the logs of the current and the previous container, the exit reason, and whether it was killed for using too much memory;
   - running but not ready → check its readiness probe and what the probe calls.
5. **Probes:** look for probes that cause harm: a liveness probe that fails while the app is merely busy or still starting (endless restarts), a readiness probe that depends on another service (whole fleets marked not ready at once), no startup probe on a slow-starting app.
6. **Resources:** compare the sum of requests with each node's allocatable capacity; list workloads with no requests or limits; compare actual use (if metrics exist) with requests to spot starved or wasted capacity. Note that going over a memory limit ends the container, while going over a CPU limit only slows it down.
7. **Disruption safety:** list disruption budgets that currently allow zero evictions, and single-replica workloads that a node drain would take down.
8. **Recent events:** read cluster-wide warnings from the last hours and group repeats.
9. **Map findings to failure modes:** a lost node, a network split, an unreachable API server, lost storage, or a misconfigured workload. For each, say what users would notice and what usually helps.
10. **Write the report:** per finding, severity, evidence (command and short output), likely cause, who owns it, and the suggested fix as a linked change proposal. Compare with the previous report.

## Checks before hand-over

- Only read commands were used; the report lists them.
- Each finding has evidence, a likely cause, an owner and a severity.
- Metrics that were unavailable are marked «not measured».
- Every suggested fix is written as a proposal, not done.
- Secrets and personal data are removed from quoted logs.

## Artefacts

- `health/<cluster>-<date>.md`: scope, findings, evidence, causes, owners, suggested proposals, comparison with the last report.
- `changes/<date>-<short-name>.md`: one infra-change-proposal per suggested fix.

## Hand-over

- **To the cluster owner:** the report and the proposals for decision.
- **To the SRE on call:** findings that affect users now.
- **To application owners (developers, devops):** findings in their workloads, such as bad probes or missing requests.
- **To the database engineer:** storage and stateful workload findings.
- **To the security reviewer:** unexpected privileges, exposed services or secrets seen in logs.

## Tools

A cluster CLI with a read-only role, plus the cluster's metrics add-on if installed. Examples for a Kubernetes cluster:

```sh
kubectl get nodes -o wide
kubectl describe node <node>
kubectl get pods -A --field-selector=status.phase!=Running
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --previous
kubectl get events -A --sort-by=.lastTimestamp
kubectl top nodes
kubectl get poddisruptionbudgets -A
```

## Sources

Built on the Kubernetes documentation, «Troubleshooting Clusters», «Monitor Node Health», «Debug Pods», «Resource Management for Pods and Containers», «Configure Liveness, Readiness and Startup Probes» and «Disruptions» (github.com/kubernetes/website, commit da4702f; © The Kubernetes Authors, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), changed. This page includes information from the O*NET 31.0 Database by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the CC BY 4.0 license. O*NET® is a trademark of USDOL/ETA. harnsy has modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
