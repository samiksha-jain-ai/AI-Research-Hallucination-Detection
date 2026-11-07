# Token-level uncertainty for hallucination prediction — experimental follow-up

**Status:** Research coursework, reproducibility package from actual Colab artifacts; **not a fully independently verified source-level reproduction**. This is the second (experimental) paper following a separate literature review. Prompt 16 identified unresolved issues in original source-ID recovery, original-row recomputation, and citation verification.

## Question and findings

Does the 90th percentile of token negative log-likelihood (p90 NLL) rank hallucinated answers better than mean NLL? We scored 600 sampled HaluEval general-data responses using DistilGPT-2 as a **surrogate** uncertainty model, split 420 train / 90 validation / 90 held-out test, seed 42. On validation, p90 was selected by average precision (AP). On test, mean NLL AP **0.22342**, p90 NLL AP **0.20328**, and answer length AP **0.17771**. The primary contrast was **negative** (p90 minus mean AP = -0.02014); exploratory paired bootstrap 95% interval **[-0.10752, 0.05195]**. This is not evidence of a statistically established improvement. See `results/results.csv` and `results/evaluation_summary.md`.

## Layout

- `notebooks/`: original stage-specific Colab notebooks for environment, dataset, scoring, verification, selection and test evaluation
- `data/`: derived score CSVs and provenance caveats; no original response text
- `scripts/evaluate_scores.py`: recomputes AP and AUROC from score CSVs, with integrity checks
- `results/`: actual Colab outputs, bootstrap audit, tables and PNG/PDF figures
- `configs/`: initial blueprint (contains **planned** settings, not necessarily executed ones); actual selection in `results/frozen_comparison_protocol.json`
- `paper/`: revised ACM-format **draft**, bibliography requiring source verification
- `docs/`: debugging decisions, research blueprint, results discussion and critical peer review

## Reproduce metrics from the saved scores

From repository root, in a Python environment:

```bash
python -m pip install -r requirements.txt
python scripts/evaluate_scores.py --data-dir data --output results/recomputed_results.csv
```

The metric script was actually run during packaging and matched the existing test metrics (see `results/metric_reproduction_check.txt`). The installation command is **[TEST REQUIRED]** in a clean independent environment. Do not interpret metric reproduction as independent verification of original text-to-score computation.

## Full scoring reproduction — additional work needed

1. Inspect `notebooks/Prompt_08_Environment.ipynb` and record your current Python/PyTorch/Transformers/GPU versions. Historical Colab environment observed: Python 3.13.16, torch 2.14.1+cu130, transformers 4.57.6, Tesla T4; **not pinned or retested** in a clean environment.
2. Obtain `general_data.json` from the HaluEval source and verify its terms. Run the Prompt 09A notebook, which uses seed 42 and a stratified 600-row sample. **[TEST REQUIRED]** on a fresh Colab runtime; it did not preserve original IDs.
3. Run Prompt 09B to score responses with `distilgpt2`; download its scored ZIP. **[TEST REQUIRED]** for a fresh end-to-end run.
4. Run Prompt 10 to validate and repair synthetic IDs; inspect boundary-token exclusion and its effect. Original-row audit was skipped in the recorded run.
5. Use Prompt 12 for validation-only selection and Prompt 13 for final held-out test metrics. The frozen selection is `p90_nll`. Do not tune on test.

## Reproduce manuscript

`paper/main.tex` and `paper/references.bib` are the ACM experimental draft. The original review source was not incorporated into this repository. ACM class/template availability may be required; compile in Overleaf with the corresponding ACM template. **[TEST REQUIRED]** from this repository alone. All bibliography entries must be checked against original publications before submission.

## Limitations and safeguards

- Original HaluEval IDs and response text are absent from score files. Synthetic split-prefixed IDs prove only uniqueness of the exported records, not source-level independence.
- DistilGPT-2 did not generate the labelled answers; its NLL is surrogate likelihood, not the original generator's confidence.
- 90 test rows, 17 positives; exploratory bootstrap interval spans zero.
- The independent arithmetic smoke audit passed; full original-row recomputation was **not performed**.
- Dataset redistribution/license and publication metadata require verification. No credentials, API keys, original raw dataset, or model weights included.
- The first review is distinct from this experimental follow-up. Research claims are limited to this sampled setup.

## Reproduction checklist

- [ ] Confirm HaluEval source and license
- [ ] Create clean environment; install dependencies and document versions
- [x] Recompute AP/AUROC from provided score files using metric script
- [ ] Recover source IDs and independently check split overlap
- [ ] Recompute representative original-row token NLL values
- [ ] Verify bibliography and compile manuscript with ACM class
- [ ] Confirm all files and commands on a second machine

## Attribution

Research design, Colab execution and verification evidence are from the student's coursework; AI assistance was used for code generation, debugging, analysis and writing. See `docs/debugging_log.md` and `research_decisions.md`. Cite the HaluEval dataset and relevant methods using their verified original publications before public release. **License for this new repository: not yet selected**; do not assume third-party files are licensed for redistribution.
