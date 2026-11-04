---
name: deploy-with-rollback
description: Release a new version of a model or service as a reviewed proposal with a tested way back: named versions, a written rollback plan, a gradual rollout watched against stop criteria, and the owner's approval before any production change. Use whenever a model, service or configuration goes to production.
---

# Deploy with rollback

A release is safe when going back is as easy as going forward. This skill prepares a production change so the owner can approve it knowing the current state, the change, the expected effect and the exact way to undo it, and then watches the rollout against criteria written in advance.

**Route:** a tested version (with its model-card or release notes) → **deploy-with-rollback** → the owner approves → gradual rollout → full release or rollback.
Before this skill: a version that passed its tests or evaluation. After it: the release record, or a rollback with its reason.

## When to use

- A new model version, service version or configuration is ready for production.
- A rollback is needed and must be done calmly and recorded.

## Inputs

- The new version, its tests or evaluation results, and its model card or release notes.
- The current production version and how production chooses which version to use (a named alias, a tag, a revision of the deployment).
- The metrics that show the system is healthy (errors, latency, the business metric the model affects) and their normal range.
- Who owns production and approves changes; who is on call.

## Rules

- Production changes only after the owner's approval, as a proposal: current state → change → expected effect → undo.
- Production points to a named version or alias, never to «latest». A release moves the pointer; a rollback moves it back.
- The previous known-good version stays available until the new one is accepted.
- The rollback plan is written and tried (in a test environment, or by a dry run) before the release.
- Stop criteria are written before the rollout starts; when one is hit, roll back first and investigate after.
- Personal data in logs and monitoring stays minimal and aggregated.

## Steps

1. **Register the version** with its lineage: the code, the data version, the training or build run, and its card or notes.
2. **Write the proposal:**
   - current: which version is live and its health metrics;
   - change: the new version, how traffic moves to it (for example a small share first, then more);
   - expected effect: on health metrics and the business metric, with the evidence from tests or evaluation;
   - undo: the exact steps to point production back to the previous version, how long it takes, who can do it.
3. **Write the stop criteria:** which metric, by how much, over what time, stops the rollout.
4. **Test the rollback** in a test environment or with a dry run; record the result.
5. **Get approval** from the production owner; record who approved and when.
6. **Roll out gradually:** start with a small share or a canary, watch the health metrics and the stop criteria, wait the agreed time, then widen. Watch the rollout status; a rollout that does not progress in the agreed time counts as failed.
7. **Finish or roll back:** if all criteria hold, complete the release and keep the previous version available for the agreed period. If a criterion is hit, move production back to the previous version, confirm health, and write what happened.

## Checks before hand-over

- The proposal has current, change, effect and undo, and the owner approved it.
- The rollback was tested before the release.
- Stop criteria were written before the rollout and watched during it.
- The release record names the versions, times, approver and outcome.

## Artefacts

- `releases/<date>-<version>.md`: proposal, approval, stop criteria, rollback test, rollout log, outcome.

## Hand-over

- **To the production owner** (often devops or the engineering lead): the proposal for approval.
- **To devops or the SRE on call:** the rollout plan, stop criteria and rollback steps.
- **To the product manager:** the outcome and any effect on the business metric.
- **To the data scientist:** problems seen in production that need a model change.

## Sources

Built on the MLflow documentation, Model Registry (github.com/mlflow/mlflow, commit d1796b7; Apache License 2.0, Copyright 2018 Databricks, Inc.), adapted. Built on the Kubernetes documentation, «Deployments» (github.com/kubernetes/website, commit da4702f; © The Kubernetes Authors, CC BY 4.0, https://creativecommons.org/licenses/by/4.0/), changed.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
