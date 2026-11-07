# Prompt 17 — Evidence and reproduction audit

VERIFIED (from user-provided artifacts): score CSVs 420/90/90, numerical validation, independent arithmetic smoke audit, saved validation selection, held-out test metrics and figures. During repository assembly the metrics script was executed and its outputs matched the published `results.csv`.

INFERRED: the earlier query-overlap check supports split independence, but the absent raw text and original source IDs prevent a new independent source-level audit here.

UNKNOWN / TEST REQUIRED: clean-environment installation, full end-to-end notebook reproduction, original-row token-score recomputation, dataset license for public redistribution, bibliography metadata, paper compilation from this minimal package, GitHub push and remote reproducibility.

Prompt 16 review is in `docs/peer_review.md`; major revisions are still open. No GitHub repository has been created or pushed on the user's behalf.
