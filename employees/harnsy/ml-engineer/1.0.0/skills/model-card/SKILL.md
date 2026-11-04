---
name: model-card
description: Write a short, honest report for a machine-learning or statistical model: what it is for and not for, the data it learned from, how it was evaluated (split by group where possible), its limits and known bias, and who to contact. Use before a model is shared, deployed or handed to another team, and after each new version.
---

# Model card

A model card tells the people who will use, deploy or be affected by a model what it does, how well it was measured to work, and where it fails. It states results as measured on named data; it never promises how well the model will do in the future.

**Route:** analysis-notebook or eval-harness → **model-card** → review by the owner (and the privacy specialist when personal data is involved) → deploy-with-rollback or hand-over.
Before this skill: a trained model and its evaluation. After it: the card travels with every version of the model.

## When to use

- Before a model is deployed, published or handed to another team.
- When a model is retrained or its data changes: the card gets a new version.
- When someone asks «can we use this model for X?».

## Inputs

- The model and its version, the code that trained it, the training and evaluation data versions.
- Evaluation results, ideally split by the groups that matter for its use.
- The intended users and the decisions the model will support.

## Rules

- Measured, not promised: every result names the data it was measured on and the date. No claim of future accuracy.
- Limits and known bias are written as plainly as the strengths.
- Training data with personal data goes to the privacy specialist before the model is shared or deployed.
- The card is versioned with the model; an old card never describes a new version.

## Steps

1. **Details:** name, version, date, type of model, who built it, licence, contact.
2. **Intended use:** the users, the task and the decisions it supports. **Out of scope:** uses it was not built or tested for, and uses that would be harmful.
3. **Training data:** what it is, where it comes from, the period, its version, how it was cleaned or filtered, and whether it contains personal data (and the privacy specialist's view).
4. **Training procedure:** in short — preprocessing, main settings, seed, compute used.
5. **Evaluation:**
   - the evaluation data and why it represents the intended use;
   - the metrics and why they fit the decision;
   - results with their uncertainty (an interval or standard error);
   - results split by relevant groups (for example region, device, language, customer type, and protected groups where the data and the law of the country allow) — a model that is good on average can be poor for one group.
6. **Bias, risks and limits:** where it is weak, which groups it serves worse, what happens when it is wrong, and what users should do about it.
7. **Recommendations:** monitoring after deployment, when to retrain, when a person must check the output.
8. **Review:** the model owner checks the card; the privacy specialist when personal data is involved.

## Checks before hand-over

- Intended and out-of-scope uses are both written.
- Data sources, versions and personal-data status are stated.
- Every result has its data, date and uncertainty; group results are shown or their absence explained.
- Limits and known bias are stated; nothing promises future accuracy.
- The card version matches the model version.

## Artefacts

- `MODEL_CARD.md` (or `model-card-<version>.md`) stored with the model in the model registry or repository.

## Hand-over

- **To the model owner and the product manager:** the card for review before deployment.
- **To the ML engineer:** the card as part of the release (see `deploy-with-rollback`).
- **To the privacy specialist:** the data section when personal data is involved.
- **To the users of the model:** the card, with every version.

## Sources

Built on the Hugging Face Hub documentation «Model Cards» and the annotated model card template (github.com/huggingface/hub-docs, commit 1567596, and github.com/huggingface/huggingface_hub, commit 8abbfe5; Apache License 2.0, © Hugging Face), adapted. Built on «The AQuA Book» (2025, https://www.gov.uk/guidance/the-aqua-book). Contains public sector information licensed under the Open Government Licence v3.0.

Text © 2026 Pavel Buchnev (harnsy). Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). The names «harnsy» and «hr.harnsy.dev» are not covered by this licence.
