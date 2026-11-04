---
name: eval-harness
description: Build a repeatable evaluation for a model or AI system: a versioned evaluation set kept out of training, scorers for each kind of failure, a baseline run first, and every score reported with its uncertainty and the full configuration logged. Use before changing a model, prompt or retrieval setup, and before comparing two versions.
---

# Eval harness

An evaluation is a fixed test that a model or AI system runs through, so that a change can be judged by evidence instead of impressions. This skill builds that test, runs the current version as the baseline, and reports scores with their uncertainty so small differences are not mistaken for progress.

**Route:** a change to a model or system → **eval-harness** (baseline first) → the change → eval-harness again → model-card → deploy-with-rollback.
Before this skill: the task the system must do and examples of good and bad outputs. After it: comparable scores for the decision owner and the model card.

## When to use

- Before changing a model, its prompt, its settings or its retrieval data.
- When two versions or two vendors must be compared.
- On a schedule, to catch drift in a deployed system.

## Inputs

- The task, the users, and what a good and a bad output look like, from the product manager or domain owner.
- Example inputs from real use (with personal data removed or replaced), and known failures.
- The current version of the system, to run as the baseline.

## Rules

- The evaluation set is versioned and kept out of training and tuning data. If items leak into training, the set is replaced.
- Build the evaluation before changing the system, and run the current version first.
- Every score is reported with its uncertainty: a confidence interval or standard error; for pass/fail rates an interval suited to proportions; for grouped items, errors that respect the groups.
- Every run writes a log with the full configuration (model version, settings, prompt, data version, seed, date) so it can be re-run and compared.
- Personal data in examples is removed or replaced; the privacy specialist decides when unsure.
- No promised quality: results are «measured on set X version Y on date Z».

## Steps

1. **Define the task:** the input, the expected output or the qualities of a good one, and the main kinds of failure, from looking at real outputs.
2. **Build the set:** cover common cases, hard cases, and each kind of failure; record where each item came from; split off a hidden part for final checks. Version it.
3. **Choose scorers:** exact or rule-based checks first (format, required facts, forbidden content); a model-based grader only where rules cannot judge, and then check it against a sample of human labels and report how often it agrees on passes and on failures.
4. **Name one headline metric** that matches the decision, plus a few secondary ones.
5. **Run the baseline** several times when outputs vary, and record how the runs are combined.
6. **Run the change** with the same set, scorers and settings except the one thing being changed.
7. **Compare:** the difference with its uncertainty, per kind of failure and per group; read a sample of changed outputs by hand.
8. **Report:** what improved, what got worse, how sure we are, and what the set does not cover.

## Checks before hand-over

- The set is versioned and confirmed out of training data.
- The baseline was run first with the same configuration.
- Every score has its uncertainty; small differences inside the uncertainty are called «no clear difference».
- Logs with full configuration exist for every run.
- Model-based graders were checked against human labels.

## Artefacts

- `evals/<task>/set-v<N>/`: items with their origin; the hidden part kept apart.
- `evals/<task>/scorers/`: scorer code.
- `evals/<task>/runs/<date>-<version>.log`: full configuration and scores.
- `evals/<task>/report-<date>.md`: comparison and recommendation.

## Hand-over

- **To the product manager or model owner:** the report; they decide whether the change goes forward.
- **To `model-card`:** the evaluation section for the version being released.
- **To the data scientist:** failure kinds that need new data or a different approach.

## Sources

Built on the Inspect AI documentation: scorers, metrics and eval logs (github.com/UKGovernmentBEIS/inspect_ai, commit 4acfd20; MIT, © 2024 UK AI Security Institute), adapted.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
