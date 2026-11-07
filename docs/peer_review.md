# Prompt 16 — Technical Peer Review and Revision Log

**Manuscript reviewed:** *Does High-Loss Token Aggregation Improve Hallucination Ranking? A Controlled Study with Surrogate Language-Model Uncertainty* (revised ACM draft, 10 pages, Prompt 15).

**Review status:** Major revision. This is an assessment of the supplied PDF and LaTeX, not an independent rerun of the experiments or verification of external publications.

## Summary and contribution assessment

The manuscript follows the author's earlier literature review and investigates whether the 90th percentile (P90) of DistilGPT-2 answer-token NLL ranks HaluEval hallucinations better than mean NLL. The 600-example sample is split 420/90/90. P90 was selected on validation AP (0.2827 versus 0.2460), but test AP was lower (0.2033 versus 0.2234). The reported paired bootstrap interval for the difference spans zero. Reporting this negative result is appropriate. The study is a narrow controlled comparison, **not** a novel hallucination detector or reproduction of the cited semantic-entropy systems.

## Major concerns

| ID | Location | Concern and why it matters | Concrete remedy | Status |
|---|---|---|---|---|
| M1 | pp. 2–3, §4.1 and §4.3; p. 8, §10 | The original HaluEval IDs were discarded and replaced by split-specific IDs. Unique synthetic IDs do **not** prove unique original source records or prevent exact answer duplicates across partitions. | Match each split's question/answer/label to the downloaded source dataset, resolve ambiguous matches, save source-ID mapping and recheck source-level disjointness and duplicates. | Open |
| M2 | p. 3, §4.3; pp. 8–9, §10–11 | The NLL audit verifies equivalence of two arithmetic expressions on a synthetic example, but not that original response text, token boundaries, and stored scores agree. | Recompute mean/P90/length on a prespecified stratified subset from the saved original split CSVs using the same model and tokenizer; record tolerances and differences. | Open |
| M3 | pp. 2–3, §4; p. 9, §11 | Reproducibility relies on prior notebook/ZIP artifacts that are not bundled with this manuscript. Dataset retrieval URL, precise package versions, split code, scoring command and run instructions need a public repository. | Include README, requirements, exact dataset acquisition/checksum, seed and split script, scoring/evaluation notebooks, frozen protocol, logs and figure-generation commands. Mark untested commands. | Open |
| M4 | pp. 1–2, §2; p. 10, References | Manuscript explicitly states references require independent verification; abbreviated author lists and bibliographic fields could be wrong. | Verify titles, authors, venues, years and DOI/URL from primary publication records; keep a source-verification ledger. | Open |
| M5 | pp. 2–4, §3–5 | The methods are fair on the *same* examples and scorer, but the distinction between a surrogate likelihood and generator-native uncertainty is central to external validity. The small test set has only 17 positives. | Keep limitations prominent; do not generalize the observed ordering beyond this sample or describe the study as reproducing a published detector. Consider an additional seed or scorer only as a future experiment, not an unperformed result. | Partly addressed; retain |

## Minor concerns

| ID | Location | Concern | Remedy | Status |
|---|---|---|---|---|
| m1 | p. 2, Eq. (1) | The PDF renders the prompt–answer separator as `nAnswer:` instead of a clear newline delimiter. | Use a verbatim/code listing or define `x = "Question: {q}\\nAnswer: {a}"` in a text-safe form, and verify the compiled PDF. | Open |
| m2 | pp. 6–9, §§7–11 | Discussion, evaluation cautions and reproducibility limitations are repeated, reducing focus in a 10-page manuscript. | Consolidate overlapping sections, leaving Methods, Results, Discussion, Limitations and Reproducibility clearly separated. | Open |
| m3 | pp. 3–5, Tables 1–3 | Tables give rounded values but do not cite exact artifact names next to each table. | Add table footnotes or a reproducibility appendix mapping each table to CSV fields and scripts. | Open |
| m4 | pp. 4–5, Figs. 1–2 | Figure captions state they came from executed Prompt 13 evaluation, but the manuscript does not include figure-generation commands. | Include script path and precise input artifact in caption or reproducibility section. | Open |
| m5 | p. 1 and bibliography | ACM draft includes manuscript-status boilerplate and personal/institution metadata requiring confirmation. | Confirm required ACM format, author affiliation, contact details and any required course statement before submission. | Open |

## Integrity and numerical consistency checks from manuscript

- Test: 90 rows, 17 positives; prevalence = 17/90 ≈ 0.1889.
- Test AP: mean NLL 0.2234, P90 0.2033, answer length 0.1777.
- Test AUROC: mean NLL 0.4972, P90 0.5044, answer length 0.3284.
- Test AP difference P90 − mean ≈ −0.0201; reported bootstrap 95% interval [−0.10752, 0.05195].
- Validation AP: mean NLL 0.2460, P90 0.2827, consistent with validation-based selection.
- The test length subgroups total 49 + 41 = 90 and positives total 12 + 5 = 17.
- These are **internal consistency observations from the manuscript**, not independent recomputation of source CSVs.

## Prioritized revision checklist

- [ ] **1.** Reconstruct source-level identity and prove partition disjointness (M1).
- [ ] **2.** Independently rescore a prespecified subset of original rows (M2).
- [ ] **3.** Package and test end-to-end reproduction instructions (M3).
- [ ] **4.** Verify each bibliography entry against a primary source (M4).
- [ ] **5.** Correct the displayed prompt string in Eq. (1) (m1).
- [ ] **6.** Consolidate repeated text and add artifact provenance for tables/figures (m2–m4).
- [ ] **7.** Recompile, inspect final PDF, and complete author/template checks (m5).

## Author-response table (draft, not claims of completed revisions)

| Reviewer issue | Proposed author response | Evidence needed before marking resolved |
|---|---|---|
| M1 — Source ID provenance | We agree and will reconstruct an auditable source-record mapping rather than treating synthetic IDs as original IDs. | Mapping CSV, collision/duplicate audit log |
| M2 — Score recomputation | We will independently recompute selected original examples and compare token counts, mean NLL and P90 NLL to stored scores. | Actual recomputation output and tolerance report |
| M3 — Reproducibility | We will provide the notebooks, scripts, dependency versions, frozen protocol and documented data acquisition process. | Public repository and successful reproduction run |
| M4 — Citations | We will verify all bibliography entries against original publication records and correct inaccuracies. | Verified citation ledger and updated `.bib` |
| m1 — Equation rendering | We will correct the literal newline notation and inspect the compiled PDF. | Updated `.tex` and rendered page 2 |
| m2–m4 — Structure/provenance | We will remove duplication and identify exact CSV/plot inputs. | Revised manuscript and figure/table provenance |

## Recommendation

**Major revision, not rejection.** The central negative-result claim is appropriately cautious and the reported tables are internally coherent. The strongest outstanding threats concern source-record identity, independent score validation and a self-contained reproduction package. The review is grounded in the submitted manuscript and does not claim that fixes, new experiments or citation checks have been completed.

## AI-assistance log entry

**Task:** Critical review of Prompt 15 ACM manuscript. **Tool:** ChatGPT (GPT-6). **Inputs:** Revised Prompt 15 PDF and LaTeX source; assignment Prompt 16 requirements. **AI proposal:** Major/minor issue list, remedies and draft author responses. **Human action required:** Inspect each concern, perform revisions and independent tests, retain genuine outputs. **Verification:** PDF/LaTeX inspection only; no model run or external bibliography verification performed. **Outcome:** Review report and open revision checklist.
