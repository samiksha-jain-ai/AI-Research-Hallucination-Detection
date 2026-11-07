# Research Decisions Log — Prompts 01–02

## Project identity
- **Prior literature review:** *Token-Level Uncertainty as a Predictor of Hallucination in Large Language Models*
- **Current assignment:** AI Tools for Research — AI-assisted coding, vibe coding and evidence-based experimentation.
- **Current scope:** Complete Prompt 01 (accountable research workspace and review scope) and Prompt 02 (evidence-based research gaps) only. Do not advance to Prompt 03 unless instructed.
- **Current candidate study idea (provisional, not a novelty claim):** A small controlled comparison of token-level negative log-likelihood (NLL) and a response-consistency-style signal for hallucination detection.
- **Current compute constraint known from pilot work:** Google Colab CPU was used; DistilGPT-2 loaded and ran successfully in the pilot.
- **Evidence labels:** VERIFIED = directly visible in the supplied review or actual execution evidence; INFERRED = reasoned candidate that needs testing; UNKNOWN = not yet established.

## Review scope summary (VERIFIED from the supplied review)
The review surveys uncertainty signals for detecting hallucinations in large language models. It discusses next-token probability/log-probability, entropy and perplexity; semantic entropy and semantic entropy probes; internal-state and attention-guided approaches; and consistency/sampling-based detectors. It describes applications to hallucination detection, fact-checking and abstention.

The review identifies several limitations:
1. **Miscalibration and overconfidence:** low uncertainty is not a guarantee of factual correctness.
2. **Epistemic/aleatoric confounding:** uncertainty due to lack of knowledge can be mixed with uncertainty due to ambiguity or multiple valid phrasings.
3. **Lexical variation versus semantic agreement:** surface-level differences between responses can exaggerate apparent disagreement.
4. **Sampling cost:** methods requiring multiple generations may be substantially more expensive than single-pass signals.
5. **Access constraints:** some methods require logits, hidden states or attention data unavailable through black-box interfaces.
6. **Token-to-claim aggregation:** the review identifies a need for stronger theoretical grounding and evaluation of how token-level scores are combined into claim- or response-level judgments.
7. **Causal interpretation:** the review calls for protocols that distinguish whether uncertainty itself contributes diagnostic value or merely correlates with errors.

## Decisions and rationale
| Decision | Status | Rationale/evidence | Next action |
|---|---|---|---|
| Keep the topic connected to the completed literature review. | VERIFIED | The review is specifically about token-level uncertainty as a hallucination predictor. | Use the review as the starting evidence base. |
| Consider a controlled comparison as a candidate study pathway. | INFERRED | The review discusses multiple families of uncertainty/consistency signals and their cost/reliability trade-offs. | Before implementation, define comparable inputs, labels, metrics and constraints. |
| Treat NLL as a candidate low-cost signal, not as a validated hallucination detector. | INFERRED | The review reports calibration and overconfidence limitations. | Compare against a meaningful baseline and inspect errors. |
| Treat consistency as a candidate signal with a cost trade-off. | INFERRED | The review discusses lexical variation and the computational cost of repeated sampling. | Ensure the consistency score is measured on the same response/question unit as the labels. |
| Do not claim novelty yet. | VERIFIED requirement | The assignment says novelty needs separate literature verification. | No novelty claim until a later verification stage. |
| Current pilot results are preliminary and are not proof of general superiority. | VERIFIED from pilot record | The pilot used 100 sampled examples and a 30-example test split with only five positive examples. Its consistency proxy was computed from newly generated answers rather than the original labelled responses. | Keep this caveat explicit; do not treat the pilot as a final conclusion. |

## Research integrity rules for this project
- Never invent sources, metrics, logs, runs or human decisions.
- Keep VERIFIED, INFERRED and UNKNOWN claims separate.
- The research question and gap are provisional until original sources and the evaluation design are checked.
- Preserve negative findings and methodological limitations.
- Prompt 03 and later stages are out of scope for the professor's current instruction to complete only Prompts 01–02.
