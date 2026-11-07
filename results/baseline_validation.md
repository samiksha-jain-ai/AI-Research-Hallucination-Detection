# Prompt 10 — Final Baseline Validation

## Scope
Score-file integrity, ID repair, independent NLL arithmetic smoke test, optional original-row recomputation. No predictive performance evaluated.

## Verified checks
- score_integrity: PASS
- id_integrity: PASS
- independent_arithmetic_smoke: PASS
- smoke_max_abs_difference: 0.0
- original_row_audit: NOT PERFORMED

## Data splits
- train: 420 rows; labels {'0': 343, '1': 77}; boundary-crossing rows 420.
- validation: 90 rows; labels {'0': 76, '1': 14}; boundary-crossing rows 90.
- test: 90 rows; labels {'0': 73, '1': 17}; boundary-crossing rows 90.

## Limitations
- Split-specific row IDs are not original HaluEval source IDs.
- Question-overlap audit is supported by the earlier Prompt 09A run, not independently rechecked using score-only files.
- The first token crossing the prompt/answer boundary was excluded by the scoring protocol.
- DistilGPT-2 is a surrogate scorer, not the model that generated the labelled responses.
- Full 600-row independent recomputation was not performed.
