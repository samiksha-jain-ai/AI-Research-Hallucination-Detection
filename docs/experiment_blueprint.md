# Prompt 07 — Frozen Experiment Blueprint

**Study:** Response-level token-uncertainty aggregation for hallucination detection  
**Status:** Protocol frozen provisionally, pending dataset/environment checks; no new results are claimed  
**Platform:** Google Colab; same-day implementation target  
**Protocol version:** 1.0 (2026-11-07)

## 1. Research question and scope

On the same labelled question–answer pairs, does the **90th percentile of answer-token negative log-likelihood (NLL)** produce higher **Average Precision (AP)** for hallucination detection than **mean answer-token NLL**?

This is a **response-level** aggregation comparison motivated by the earlier G1 token-to-claim aggregation gap. It is **not** a claim-level study, a new detector architecture, a replication of semantic entropy, or evidence of novel methodology.

**Hypothesis:** Upper-tail NLL may emphasize unusually surprising answer tokens, improving ranking of hallucination-labelled responses. The hypothesis can be rejected; no result is presumed.

## 2. Dataset and provenance

- Primary candidate: HaluEval `general_data.json` from https://github.com/RUCAIBox/HaluEval (paper: https://aclanthology.org/2023.emnlp-main.397/).
- Expected fields from documentation: `user_query`, `chatgpt_response`, `hallucination_label` (Yes/No). **Inspect actual downloaded schema** before using it; no field name is assumed without checking.
- Positive class: **Yes = 1** (hallucination), **No = 0**.
- Preserve raw record index and generate a stable row ID; record source URL, retrieval date, file hash, observed schema, missing values, class counts, duplicate counts and license/redistribution conditions.
- Do not publish raw dataset until its terms have been checked. Do not mix HaluEval general and QA splits.

## 3. Frozen sampling and split protocol

- Target **600 eligible examples** for the same-day run, if available; predeclared fallback **300** only if Colab runtime/memory makes 600 infeasible. Record the reason **before** looking at test performance. If class counts are insufficient, report and adapt before scoring.
- Use random seed **42**. Sample without replacement, stratified by label when possible.
- Deduplicate exact (normalized query, normalized answer) pairs **before** sampling. Inspect repeated questions; if a question occurs in multiple records, keep all its records in one partition to prevent group leakage.
- Split by question group where needed, aiming for **70% train/exploration, 15% validation, 15% test** with approximate class stratification. If group-aware stratification cannot satisfy both constraints, prioritize zero group overlap and record actual sizes and class counts.
- Freeze and export `split_assignments.csv` before model scoring. Do not inspect test labels or scores to tune methods or thresholds.
- All methods must use the **same test row IDs**. Any dropped rows and reasons must be recorded; evaluate on their common intersection.

## 4. Model and token-scoring definition

- Candidate scoring model: Hugging Face `distilgpt2` (record exact repository revision / commit hash from the downloaded configuration and tokenizer, dependencies, device and precision).
- This model **did not generate** the original ChatGPT answers. Scores are **surrogate cross-model likelihoods**, not the original generator's confidence or calibrated hallucination probabilities.
- Construct one deterministic context template per row, e.g. `Question: {user_query}\nAnswer: {chatgpt_response}`. Use the same template for every row; log it.
- **Answer-only token NLL:** tokenize the prefix and prefix-plus-answer carefully. Tokenization at the prefix/answer boundary may merge tokens; verify the boundary or use an explicit stable separator and an offset-aware tokenizer. Compute next-token log probabilities for only the answer tokens, excluding prompt, padding, and any artificially appended EOS tokens. Use teacher forcing, not newly generated answers.
- Respect the model's context length (DistilGPT-2 typically 1024 positions): choose a deterministic truncation rule that preserves the scored answer and enough question context, and log any truncated or skipped cases. Do not silently truncate away labelled answer content.
- For scored answer tokens with NLL values `n_1,...,n_T`, define `mean_nll = sum(n_i)/T` and `p90_nll = empirical 90th percentile(n_i)`; `answer_length = T`.
- Primary direction: **higher score → more likely hallucination**. Do not reverse the direction based on test outcomes. A sensitivity analysis may be explicitly labelled post hoc.
- Reject/flag empty answers, zero scored tokens, nonfinite NLLs and invalid labels.

## 5. Comparators

| Score/control | Exact role | Training required? |
|---|---|---|
| Mean answer-token NLL | Primary uncertainty baseline | No |
| 90th-percentile answer-token NLL | Proposed aggregation comparison | No |
| Answer-token count | Length-only confound control | No |
| Constant majority-class prediction | Trivial classification reference | Determine majority from train only |

These are **two uncertainty aggregation methods and two simple controls**, not two independently reproduced published detector systems. Make this distinction in the submission.

## 6. Metrics and decision rules

**Primary metric:** sklearn `average_precision_score(y_test, score)` for Yes=1; report AP for both NLL methods and `delta_AP = AP_p90 - AP_mean` on identical held-out test rows. The predeclared comparison favors p90 if delta_AP > 0; report its magnitude and uncertainty, and do not call it statistically significant without appropriate evidence.

**Secondary:** AUROC where both labels exist; precision, recall, F1 and confusion matrix from thresholds selected **on validation**; class prevalence and sample sizes; runtime and model/device details. A constant-score AP equals positive prevalence under sklearn's convention, useful as a no-skill ranking reference. A majority-class *classifier* is evaluated separately for accuracy/F1; do not conflate it with a ranking method.

For a paired uncertainty estimate, use **1,000 paired bootstrap resamples of test rows** with seed 42, recomputing AP difference and a percentile 95% interval; state that it is exploratory and potentially unstable on small/imbalanced samples. If too few positive/negative cases exist, state the limitation.

**Thresholds:** choose per-score threshold maximizing validation F1; freeze thresholds before test predictions. Do not choose a threshold on the test set. If a validation class is absent, do not force threshold metrics.

## 7. Error analysis and validity

- Save per-row scores, true labels, split IDs and predicted labels for all evaluated rows.
- Report false positives and false negatives, and a few anonymized/short excerpts with human interpretation; do not treat a model's own explanation as ground truth.
- Compare score behavior across answer-length bins defined using train/validation distributions, not optimized on test outcomes.
- Check score correlation with length; inspect very short and very long answers.
- Record limitations: label subjectivity; response-level labels; cross-model surrogate uncertainty; dataset class imbalance; small same-day sample; prompt formatting sensitivity; no external validation; no claim-level alignment.

## 8. Planned output files

```
project/
  README.md
  requirements.txt
  configs/experiment_config.json
  data/README.md
  notebooks/experiment.ipynb
  results/dataset_audit.json
  results/split_assignments.csv
  results/per_response_scores.csv
  results/validation_thresholds.json
  results/test_metrics.json
  results/bootstrap_ap_difference.csv
  results/error_analysis.csv
  results/figures/
  baseline_validation.md
  research_decisions.md
  ai_assistance_log.md
```

Do not fabricate files or numerical contents: outputs above are **planned** until the notebook actually runs.

## 9. Execution checkpoints

**Prompt 08:** In Colab, install dependencies, check GPU/CPU, download/inspect dataset, validate tokenizer and model on one answer. **STOP and request genuine Colab output** before continuing.

**Prompt 09:** Implement dataset audit, frozen split, answer-only token NLL, aggregation and save score CSV in separate verified steps. Do not proceed if alignment tests fail.

**Prompt 10:** Verify baseline against a hand-checkable tiny example and actual outputs.

**Prompts 11–14:** Debug genuine logs, run full comparison, analyze actual scores and write results without invention.

## 10. Change-control log

Any change after this protocol must be recorded with date, reason, affected outputs and whether test results had already been inspected. Resource-driven reductions are permitted but must be disclosed. The final report should distinguish **predeclared** from **post hoc** analyses.

## 11. Decision

**CONDITIONAL GO:** This protocol is suitable for a small Colab feasibility study once the data schema, terms, model access and answer-only scoring alignment pass actual tests. Novelty remains unverified; no performance result is claimed.

**Writing note:** This document is an AI-assisted planning artifact. Review and adapt the wording to accurately describe the work you personally perform; no AI-detector percentage is guaranteed.
